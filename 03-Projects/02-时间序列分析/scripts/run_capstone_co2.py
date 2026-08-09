from __future__ import annotations

import json
import platform
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels
from statsmodels.datasets import co2
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.stats.diagnostic import acorr_ljungbox
from sklearn.ensemble import HistGradientBoostingRegressor


REPO_ROOT = Path(__file__).resolve().parents[3]
PROJECT_ROOT = REPO_ROOT / "03-Projects" / "02-时间序列分析"
ARTIFACT_ROOT = PROJECT_ROOT / "artifacts" / "capstone-co2"
SEED = 20260806


def load_series() -> pd.Series:
    series = co2.load_pandas().data["co2"].resample("MS").mean().loc["1965":]
    if series.isna().any():
        raise ValueError("CO2 series still contains missing monthly values after 1965")
    series.name = "co2"
    return series


def normal_intervals(prediction: np.ndarray, scale: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    steps = np.sqrt(np.arange(1, len(prediction) + 1, dtype=float))
    standard_error = max(scale, 1e-8) * steps
    return (
        prediction - 1.2815515655 * standard_error,
        prediction + 1.2815515655 * standard_error,
        prediction - 1.9599639845 * standard_error,
        prediction + 1.9599639845 * standard_error,
    )


def forecast(model_name: str, train: pd.Series, horizon: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if model_name == "naive":
        prediction = np.repeat(float(train.iloc[-1]), horizon)
        scale = float(np.std(train.diff().dropna(), ddof=1))
        return (prediction, *normal_intervals(prediction, scale))
    if model_name == "seasonal_naive":
        prediction = np.resize(train.iloc[-12:].to_numpy(), horizon)
        scale = float(np.std(train.diff(12).dropna(), ddof=1))
        return (prediction, *normal_intervals(prediction, scale))
    if model_name == "ets":
        fit = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=12, initialization_method="estimated").fit(optimized=True)
        prediction = np.asarray(fit.forecast(horizon), dtype=float)
        scale = float(np.std(np.asarray(fit.resid), ddof=1))
        return (prediction, *normal_intervals(prediction, scale))
    if model_name == "arima":
        fit = ARIMA(train, order=(1, 1, 1), seasonal_order=(1, 0, 1, 12), trend="n").fit()
        if not bool(fit.mle_retvals.get("converged", True)):
            raise RuntimeError("ARIMA optimizer did not converge")
        forecast_result = fit.get_forecast(horizon)
        prediction = np.asarray(forecast_result.predicted_mean, dtype=float)
        interval80 = np.asarray(forecast_result.conf_int(alpha=0.20), dtype=float)
        interval95 = np.asarray(forecast_result.conf_int(alpha=0.05), dtype=float)
        return prediction, interval80[:, 0], interval80[:, 1], interval95[:, 0], interval95[:, 1]
    if model_name == "ml_lag":
        lag_order = [1, 2, 3, 12]
        frame = pd.DataFrame({f"lag_{lag}": train.shift(lag) for lag in lag_order}).dropna()
        target = train.loc[frame.index]
        model = HistGradientBoostingRegressor(max_iter=160, learning_rate=0.05, max_leaf_nodes=15, l2_regularization=0.1, random_state=SEED)
        model.fit(frame, target)
        history = train.to_list()
        values: list[float] = []
        for _ in range(horizon):
            features = pd.DataFrame([[history[-lag] for lag in lag_order]], columns=frame.columns)
            predicted = float(model.predict(features)[0])
            values.append(predicted)
            history.append(predicted)
        prediction = np.asarray(values, dtype=float)
        residuals = target.to_numpy(dtype=float) - model.predict(frame)
        scale = float(np.std(residuals, ddof=1))
        return (prediction, *normal_intervals(prediction, scale))
    raise ValueError(model_name)


def evaluate(
    series: pd.Series,
    split: str,
    origins: list[pd.Timestamp],
    horizon: int,
    models: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    warning_rows: list[dict[str, object]] = []
    for origin in origins:
        target = series.loc[origin:].iloc[:horizon]
        train = series.loc[:origin].iloc[:-1]
        if len(target) != horizon:
            continue
        for model_name in models:
            caught: list[warnings.WarningMessage] = []
            try:
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter("always")
                    predictions, lower80, upper80, lower95, upper95 = forecast(model_name, train, horizon)
                for step, (timestamp, actual, predicted, low80, high80, low95, high95) in enumerate(zip(target.index, target, predictions, lower80, upper80, lower95, upper95), start=1):
                    rows.append({"split": split, "origin": origin.date().isoformat(), "train_end": train.index[-1].date().isoformat(), "timestamp": timestamp.date().isoformat(), "horizon": step, "model": model_name, "actual": float(actual), "prediction": float(predicted), "error": float(actual - predicted), "lower80": float(low80), "upper80": float(high80), "lower95": float(low95), "upper95": float(high95), "covered80": bool(low80 <= actual <= high80), "covered95": bool(low95 <= actual <= high95)})
            except Exception as error:
                failures.append({"split": split, "origin": origin.date().isoformat(), "model": model_name, "error": repr(error)})
            for item in caught:
                warning_rows.append({"split": split, "origin": origin.date().isoformat(), "model": model_name, "category": item.category.__name__, "message": str(item.message)})
    return pd.DataFrame(rows), pd.DataFrame(failures), pd.DataFrame(warning_rows)


def metrics(predictions: pd.DataFrame) -> pd.DataFrame:
    grouped = predictions.groupby(["split", "model", "horizon"], as_index=False)
    return grouped.agg(
        mae=("error", lambda values: float(np.mean(np.abs(values)))),
        rmse=("error", lambda values: float(np.sqrt(np.mean(np.square(values))))),
        coverage80=("covered80", "mean"),
        coverage95=("covered95", "mean"),
        interval_width80=("upper80", lambda values: float(np.mean(values.to_numpy() - predictions.loc[values.index, "lower80"].to_numpy()))),
        interval_width95=("upper95", lambda values: float(np.mean(values.to_numpy() - predictions.loc[values.index, "lower95"].to_numpy()))),
        count=("error", "size"),
    )


def select_model(
    validation: pd.DataFrame,
    failures: pd.DataFrame,
    models: list[str],
    expected_origins: int,
    horizon: int,
) -> tuple[str, pd.DataFrame]:
    per_horizon = metrics(validation)
    scores = per_horizon.groupby("model", as_index=False)["rmse"].mean()
    prediction_counts = validation.groupby("model").size().reindex(models, fill_value=0)
    if failures.empty:
        failure_counts = pd.Series(0, index=models, dtype=int)
    else:
        failure_counts = failures.groupby("model").size().reindex(models, fill_value=0)

    selection = pd.DataFrame({
        "model": models,
        "prediction_count": [int(prediction_counts[model]) for model in models],
        "failure_count": [int(failure_counts[model]) for model in models],
    }).merge(scores, on="model", how="left")
    selection["expected_prediction_count"] = expected_origins * horizon
    selection["eligible"] = (
        (selection["prediction_count"] == selection["expected_prediction_count"])
        & (selection["failure_count"] == 0)
        & selection["rmse"].notna()
    )
    eligible = selection[selection["eligible"]].sort_values(["rmse", "model"])
    if eligible.empty:
        raise RuntimeError("No model completed every validation origin and horizon")
    selected_model = str(eligible.iloc[0]["model"])
    selection["selected"] = selection["model"].eq(selected_model)
    selection = selection.sort_values(["eligible", "rmse", "model"], ascending=[False, True, True], na_position="last")
    return selected_model, selection


def main() -> int:
    np.random.seed(SEED)
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    series = load_series()
    validation_origins = list(series.loc["1996-01":"2000-01"].index[::3])
    test_origins = list(series.loc["2001-01":"2001-01"].index)
    models = ["naive", "seasonal_naive", "ets", "arima", "ml_lag"]
    validation, validation_failures, validation_warnings = evaluate(series, "validation", validation_origins, 12, models)
    selected_model, selection = select_model(validation, validation_failures, models, len(validation_origins), 12)
    final_test_models = list(dict.fromkeys(["naive", "seasonal_naive", selected_model]))
    test, test_failures, test_warnings = evaluate(series, "test", test_origins, 12, final_test_models)
    predictions = pd.concat([validation, test], ignore_index=True)
    failures = pd.concat([validation_failures, test_failures], ignore_index=True)
    warning_log = pd.concat([validation_warnings, test_warnings], ignore_index=True)
    summary = metrics(predictions)
    selected_test = predictions[(predictions["split"] == "test") & (predictions["model"] == selected_model)].copy()
    selected_errors = selected_test["error"].to_numpy(dtype=float)
    diagnostic_lag = min(4, max(1, len(selected_errors) // 3))
    residual_diagnostics = pd.DataFrame([{
        "split": "test",
        "model": selected_model,
        "mean_error": float(np.mean(selected_errors)),
        "std_error": float(np.std(selected_errors, ddof=1)),
        "ljung_box_lag": diagnostic_lag,
        "ljung_box_pvalue": float(acorr_ljungbox(selected_errors, lags=[diagnostic_lag], return_df=True)["lb_pvalue"].iloc[0]),
        "worst_timestamp": str(selected_test.loc[selected_test["error"].abs().idxmax(), "timestamp"]),
        "worst_abs_error": float(selected_test["error"].abs().max()),
    }])
    predictions.to_csv(ARTIFACT_ROOT / "predictions.csv", index=False)
    summary.to_csv(ARTIFACT_ROOT / "metrics-by-horizon.csv", index=False)
    if failures.empty:
        failures = pd.DataFrame(columns=["split", "origin", "model", "error"])
    failures.to_csv(ARTIFACT_ROOT / "failures.csv", index=False)
    if warning_log.empty:
        warning_log = pd.DataFrame(columns=["split", "origin", "model", "category", "message"])
    warning_log.to_csv(ARTIFACT_ROOT / "warnings.csv", index=False)
    selection.to_csv(ARTIFACT_ROOT / "validation-model-selection.csv", index=False)
    residual_diagnostics.to_csv(ARTIFACT_ROOT / "residual-diagnostics.csv", index=False)
    manifest = {"dataset": "statsmodels.datasets.co2", "source_url": "https://www.statsmodels.org/stable/datasets/generated/co2.html", "data_license": "public domain per statsmodels dataset documentation", "frequency": "monthly start", "range": [str(series.index.min().date()), str(series.index.max().date())], "missing_months_after_1965": 0, "validation_origins": [str(x.date()) for x in validation_origins], "test_origin": [str(x.date()) for x in test_origins], "horizon": 12, "validation_models": models, "final_test_models": final_test_models, "selected_on_validation": selected_model, "seed": SEED, "python": platform.python_version(), "statsmodels": statsmodels.__version__, "sklearn": __import__("sklearn").__version__, "command": "python scripts/run_capstone_co2.py", "selection_policy": "A model is eligible only if it completes every validation origin and horizon without a fit failure", "test_policy": "Selection is frozen before the 2001 test run; test evaluates only naive baselines and the selected model", "interval_policy": "ETS/naive/ML intervals use training residual scale; ARIMA intervals use model forecast distribution", "diagnostic_policy": "Ljung-Box is descriptive on selected test errors; it does not retroactively tune the model"}
    (ARTIFACT_ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (ARTIFACT_ROOT / "environment.txt").write_text(
        "Python " + platform.python_version() + "\n"
        "numpy " + np.__version__ + "\n"
        "pandas " + pd.__version__ + "\n"
        "statsmodels " + statsmodels.__version__ + "\n"
        "scikit-learn " + __import__("sklearn").__version__ + "\n"
        "command: python scripts/run_capstone_co2.py\n",
        encoding="utf-8",
    )
    (ARTIFACT_ROOT / "run.log").write_text(
        json.dumps(
            {
                "seed": SEED,
                "prediction_rows": len(predictions),
                "failure_rows": len(failures),
                "warning_rows": len(warning_log),
                "selected_model": selected_model,
                "validation_failure_models": validation_failures["model"].tolist() if not validation_failures.empty else [],
                "final_test_models": final_test_models,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    ranking = "、".join(
        f"{row.model}={row.rmse:.3f}{'' if row.eligible else '（因失败/缺失不具备选择资格）'}"
        for row in selection.itertuples()
    )
    report = "\n".join(["---", "type: index", "topic: \"CO₂ Capstone 运行报告\"", "course: \"时间序列分析\"", "created: 2026-08-06", "updated: 2026-08-07", "status: active", "flow: project", "assessment_exempt: true", "assessment_exempt_reason: \"本页是脚本生成的参考运行证据，不是课程知识卡或学习者作业。\"", "generated_from: \"scripts/run_capstone_co2.py\"", "tags: [项目, 时间序列分析, 运行证据]", "---", "", "# CO₂ Capstone 运行报告", "", "- 数据来自 statsmodels 内置、标记为 public domain 的 CO₂ 数据，1965 年后按月聚合；原始数据中的早期缺失区间不进入实验。", "- 验证窗口：1996-01 至 2000-01，每三个月一个滚动原点；最终测试原点：2001-01；horizon=12。", "- 候选只有在完成全部验证原点和 horizon 且无拟合失败时才具备选择资格；优化未收敛按失败处理。", f"- 验证集按逐 horizon RMSE 的平均值选择模型：`{selected_model}`；选择完成后才运行最终测试。", f"- 验证平均 RMSE：{ranking}；失败候选不会通过少算困难窗口获得不公平优势。", f"- 最终测试只运行冻结的模型集合：{', '.join(final_test_models)}。", "- 点预测报告 MAE/RMSE；80%/95% 区间同时报告覆盖率和平均宽度。", "- Naive、Seasonal Naive、ETS 与 ML 区间采用训练残差尺度的正态近似；ARIMA 使用模型预测分布。该近似是本次最小复现的限制，不视为已完成严格校准。", "- `warnings.csv` 和 `failures.csv` 分别保留警告与失败；它们不会从选择证据中静默消失。", "- 选中模型测试误差的 Ljung–Box 只作描述性诊断，不能反向调参；最差窗口和误差摘要见 `residual-diagnostics.csv`。", "- 详细复算入口：`predictions.csv`、`metrics-by-horizon.csv`、`validation-model-selection.csv`、`residual-diagnostics.csv`、`warnings.csv`、`failures.csv`、`manifest.json`。", "", "本报告不把运行结果解释为普遍模型优越性；它只证明本课程 Capstone 的最小可复现执行路径。"])
    (ARTIFACT_ROOT / "report.md").write_text(report + "\n", encoding="utf-8")
    print(json.dumps({"artifact_root": str(ARTIFACT_ROOT), "prediction_rows": len(predictions), "failure_rows": len(failures), "warning_rows": len(warning_log), "selected_model": selected_model}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
