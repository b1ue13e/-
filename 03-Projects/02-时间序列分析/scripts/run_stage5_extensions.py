from __future__ import annotations

import argparse
import importlib.metadata
import json
import math
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.ensemble import HistGradientBoostingRegressor
from statsmodels.tsa.api import VAR
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.structural import UnobservedComponents


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "artifacts" / "stage5-extensions"
MODEL_NAMES = ["naive", "ar", "arimax", "var", "state_space", "ml_lag"]
EXOG_COLUMNS = ["cons_growth_lag1", "inv_growth_lag1", "tbilrate_lag1"]
ML_COLUMNS = [
    "gdp_growth_lag1",
    "gdp_growth_lag2",
    "gdp_growth_lag4",
    *EXOG_COLUMNS,
    "quarter_sin",
    "quarter_cos",
]
VECTOR_COLUMNS = ["gdp_growth", "cons_growth", "inv_growth"]
SEED = 20260807
VALIDATION_ORIGINS = 16
TEST_ORIGINS = 16


@dataclass(frozen=True)
class ForecastResult:
    prediction: float
    converged: bool


def package_version(name: str) -> str:
    return importlib.metadata.version(name)


def build_dataset() -> pd.DataFrame:
    raw = sm.datasets.macrodata.load_pandas().data.copy()
    labels = raw["year"].astype(int).astype(str) + "Q" + raw["quarter"].astype(int).astype(str)
    periods = pd.PeriodIndex(labels, freq="Q")
    frame = pd.DataFrame(index=periods)

    for output, source in (
        ("gdp_growth", "realgdp"),
        ("cons_growth", "realcons"),
        ("inv_growth", "realinv"),
    ):
        levels = pd.Series(raw[source].to_numpy(dtype=float), index=periods)
        frame[output] = 400.0 * np.log(levels).diff()

    frame["tbilrate"] = raw["tbilrate"].to_numpy(dtype=float)
    for column in ("gdp_growth", "cons_growth", "inv_growth", "tbilrate"):
        frame[f"{column}_lag1"] = frame[column].shift(1)
    frame["gdp_growth_lag2"] = frame["gdp_growth"].shift(2)
    frame["gdp_growth_lag4"] = frame["gdp_growth"].shift(4)
    frame["quarter_sin"] = np.sin(2.0 * np.pi * frame.index.quarter / 4.0)
    frame["quarter_cos"] = np.cos(2.0 * np.pi * frame.index.quarter / 4.0)
    return frame.dropna().copy()


def forecast_naive(train: pd.DataFrame, row: pd.DataFrame) -> ForecastResult:
    del row
    return ForecastResult(float(train["gdp_growth"].iloc[-1]), True)


def forecast_ar(train: pd.DataFrame, row: pd.DataFrame) -> ForecastResult:
    del row
    fit = AutoReg(
        train["gdp_growth"].to_numpy(),
        lags=[1, 2, 4],
        trend="c",
        old_names=False,
    ).fit()
    origin = len(train)
    prediction = float(fit.predict(start=origin, end=origin)[0])
    return ForecastResult(prediction, True)


def forecast_arimax(train: pd.DataFrame, row: pd.DataFrame) -> ForecastResult:
    fit = ARIMA(
        train["gdp_growth"].to_numpy(),
        exog=train[EXOG_COLUMNS].to_numpy(),
        order=(1, 0, 0),
        trend="c",
    ).fit()
    prediction = float(fit.forecast(1, exog=row[EXOG_COLUMNS].to_numpy())[0])
    converged = bool(fit.mle_retvals.get("converged", True))
    return ForecastResult(prediction, converged)


def forecast_var(train: pd.DataFrame, row: pd.DataFrame) -> ForecastResult:
    del row
    fit = VAR(train[VECTOR_COLUMNS]).fit(maxlags=1, trend="c")
    history = train[VECTOR_COLUMNS].to_numpy()[-fit.k_ar :]
    prediction = float(fit.forecast(history, steps=1)[0, 0])
    return ForecastResult(prediction, bool(fit.is_stable()))


def forecast_state_space(train: pd.DataFrame, row: pd.DataFrame) -> ForecastResult:
    del row
    fit = UnobservedComponents(
        train["gdp_growth"].to_numpy(),
        level=True,
        stochastic_level=True,
        autoregressive=1,
        irregular=True,
    ).fit(disp=False, maxiter=200)
    prediction = float(fit.forecast(1)[0])
    converged = bool(fit.mle_retvals.get("converged", True))
    return ForecastResult(prediction, converged)


def forecast_ml_lag(train: pd.DataFrame, row: pd.DataFrame) -> ForecastResult:
    fit = HistGradientBoostingRegressor(
        loss="squared_error",
        max_iter=100,
        max_depth=3,
        learning_rate=0.05,
        l2_regularization=0.1,
        random_state=SEED,
    ).fit(train[ML_COLUMNS], train["gdp_growth"])
    prediction = float(fit.predict(row[ML_COLUMNS])[0])
    return ForecastResult(prediction, True)


FORECASTERS: dict[str, Callable[[pd.DataFrame, pd.DataFrame], ForecastResult]] = {
    "naive": forecast_naive,
    "ar": forecast_ar,
    "arimax": forecast_arimax,
    "var": forecast_var,
    "state_space": forecast_state_space,
    "ml_lag": forecast_ml_lag,
}


def evaluate(
    frame: pd.DataFrame,
    origins: range,
    split: str,
    models: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    predictions: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    warning_rows: list[dict[str, object]] = []

    for origin in origins:
        train = frame.iloc[:origin]
        row = frame.iloc[[origin]]
        target = float(frame["gdp_growth"].iloc[origin])
        scale = float(np.mean(np.abs(np.diff(train["gdp_growth"].to_numpy()))))
        if not np.isfinite(scale) or scale <= 0:
            raise ValueError(f"Invalid MASE scale at origin {frame.index[origin]}")

        for model in models:
            try:
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter("always")
                    result = FORECASTERS[model](train, row)
                for item in caught:
                    warning_rows.append(
                        {
                            "split": split,
                            "origin": str(frame.index[origin]),
                            "model": model,
                            "category": item.category.__name__,
                            "message": str(item.message),
                        }
                    )
                if not result.converged:
                    raise RuntimeError("model did not converge or VAR roots were unstable")
                if not math.isfinite(result.prediction):
                    raise RuntimeError("model returned a non-finite prediction")

                error = target - result.prediction
                predictions.append(
                    {
                        "split": split,
                        "origin": str(frame.index[origin]),
                        "timestamp": str(frame.index[origin]),
                        "train_end": str(frame.index[origin - 1]),
                        "model": model,
                        "y_true": target,
                        "y_pred": result.prediction,
                        "error": error,
                        "abs_error": abs(error),
                        "squared_error": error**2,
                        "mase_scale": scale,
                        "scaled_error": abs(error) / scale,
                    }
                )
            except Exception as error:
                failures.append(
                    {
                        "split": split,
                        "origin": str(frame.index[origin]),
                        "model": model,
                        "error_type": type(error).__name__,
                        "message": str(error),
                    }
                )

    columns = [
        "split",
        "origin",
        "timestamp",
        "train_end",
        "model",
        "y_true",
        "y_pred",
        "error",
        "abs_error",
        "squared_error",
        "mase_scale",
        "scaled_error",
    ]
    failure_columns = ["split", "origin", "model", "error_type", "message"]
    warning_columns = ["split", "origin", "model", "category", "message"]
    return (
        pd.DataFrame(predictions, columns=columns),
        pd.DataFrame(failures, columns=failure_columns),
        pd.DataFrame(warning_rows, columns=warning_columns),
    )


def metric_table(predictions: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (split, model), group in predictions.groupby(["split", "model"], sort=True):
        rows.append(
            {
                "split": split,
                "model": model,
                "n_predictions": len(group),
                "mae": float(group["abs_error"].mean()),
                "rmse": float(np.sqrt(group["squared_error"].mean())),
                "mase": float(group["scaled_error"].mean()),
            }
        )
    return pd.DataFrame(rows).sort_values(["split", "rmse", "model"]).reset_index(drop=True)


def select_model(
    validation: pd.DataFrame,
    failures: pd.DataFrame,
    models: list[str],
    expected_origins: int,
) -> tuple[str, pd.DataFrame]:
    rows: list[dict[str, object]] = []
    for model in models:
        model_predictions = validation.loc[validation["model"] == model]
        failure_count = int(
            len(failures.loc[(failures["split"] == "validation") & (failures["model"] == model)])
        )
        prediction_count = int(len(model_predictions))
        eligible = prediction_count == expected_origins and failure_count == 0
        rmse = (
            float(np.sqrt(model_predictions["squared_error"].mean()))
            if prediction_count
            else float("nan")
        )
        rows.append(
            {
                "model": model,
                "prediction_count": prediction_count,
                "expected_prediction_count": expected_origins,
                "failure_count": failure_count,
                "eligible": eligible,
                "validation_rmse": rmse,
            }
        )

    selection = pd.DataFrame(rows)
    eligible = selection.loc[selection["eligible"]].sort_values(
        ["validation_rmse", "model"]
    )
    if eligible.empty:
        raise RuntimeError("No model completed every validation origin")
    selected = str(eligible.iloc[0]["model"])
    selection["selected"] = selection["model"].eq(selected)
    return selected, selection


def write_environment(path: Path) -> None:
    packages = ["numpy", "pandas", "scikit-learn", "statsmodels"]
    path.write_text(
        "\n".join(f"{package}=={package_version(package)}" for package in packages) + "\n",
        encoding="utf-8",
    )


def markdown_table(frame: pd.DataFrame, columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join(":---" if column in {"split", "model"} else "---:" for column in columns) + " |"
    rows = [header, divider]
    for record in frame[columns].to_dict("records"):
        values: list[str] = []
        for column in columns:
            value = record[column]
            if isinstance(value, float):
                values.append(f"{value:.4f}")
            else:
                values.append(str(value))
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join(rows)


def write_report(
    path: Path,
    manifest: dict[str, object],
    metrics: pd.DataFrame,
    selection: pd.DataFrame,
    failures: pd.DataFrame,
    warning_rows: pd.DataFrame,
) -> None:
    validation = metrics.loc[metrics["split"] == "validation"]
    test = metrics.loc[metrics["split"] == "test"]
    selected = str(manifest["selected_on_validation"])
    selected_row = selection.loc[selection["selected"]].iloc[0]
    text = f"""---
type: index
topic: "阶段 5 扩展模型同协议运行报告"
course: "时间序列分析"
created: 2026-08-07
status: active
flow: project
kind: moc
assessment_exempt: true
assessment_exempt_reason: "本页是自动生成的运行证据报告，不承担知识点或作业验收。"
tags: [运行证据, 时间序列分析, 阶段5]
---

# 阶段 5 扩展模型同协议运行报告

## 协议

- 数据：statsmodels macrodata，公共领域，1959Q1–2009Q3。
- 目标：季度实际 GDP 年化对数增长率。
- 信息边界：所有滞后和外生变量最多使用预测季度前一季度已知值。
- 验证原点：{manifest["validation_start"]} 至 {manifest["validation_end"]}，共 {manifest["validation_origins"]} 个。
- 最终测试原点：{manifest["test_start"]} 至 {manifest["test_end"]}，共 {manifest["test_origins"]} 个。
- 选择规则：候选必须完成全部验证原点且无失败，再按验证 RMSE 选择。
- 验证胜者：{selected}，验证 RMSE={float(selected_row["validation_rmse"]):.4f}。
- 最终测试只运行：{", ".join(manifest["final_test_models"])}。

## 验证结果

{markdown_table(validation, ["split", "model", "n_predictions", "mae", "rmse", "mase"])}

## 最终测试结果

{markdown_table(test, ["split", "model", "n_predictions", "mae", "rmse", "mase"])}

## 失败与警告

- 失败记录：{len(failures)}。
- 警告记录：{len(warning_rows)}。
- 失败不会从平均指标中静默删除；验证期缺少任一原点即失去选择资格。

## 解释边界

本报告只证明固定接口和同协议比较可以复算。它不证明扩展模型普遍优于经典基线，也不把预测关联解释为因果关系。若验证期胜者在最终测试不优于朴素基线，应保留负结果并降级。
"""
    path.write_text(text, encoding="utf-8")


def run(output_root: Path) -> dict[str, object]:
    output_root.mkdir(parents=True, exist_ok=True)
    frame = build_dataset()
    test_start = len(frame) - TEST_ORIGINS
    validation_start = test_start - VALIDATION_ORIGINS
    validation_origins = range(validation_start, test_start)
    test_origins = range(test_start, len(frame))

    validation, validation_failures, validation_warnings = evaluate(
        frame,
        validation_origins,
        "validation",
        MODEL_NAMES,
    )
    selected, selection = select_model(
        validation,
        validation_failures,
        MODEL_NAMES,
        VALIDATION_ORIGINS,
    )
    final_test_models = list(dict.fromkeys(["naive", selected]))
    test, test_failures, test_warnings = evaluate(
        frame,
        test_origins,
        "test",
        final_test_models,
    )

    predictions = pd.concat([validation, test], ignore_index=True)
    failures = pd.concat([validation_failures, test_failures], ignore_index=True)
    warning_rows = pd.concat([validation_warnings, test_warnings], ignore_index=True)
    metrics = metric_table(predictions)

    manifest: dict[str, object] = {
        "dataset": "statsmodels macrodata",
        "source_url": "https://www.statsmodels.org/stable/datasets/generated/macrodata.html",
        "license": "public domain",
        "source_observations": 203,
        "transformed_observations": len(frame),
        "target": "400 * log(real GDP).diff()",
        "frequency": "quarterly",
        "forecast_horizon": 1,
        "feature_timing": "all non-calendar predictors are lagged at least one quarter",
        "models": MODEL_NAMES,
        "validation_origins": VALIDATION_ORIGINS,
        "validation_start": str(frame.index[validation_start]),
        "validation_end": str(frame.index[test_start - 1]),
        "test_origins": TEST_ORIGINS,
        "test_start": str(frame.index[test_start]),
        "test_end": str(frame.index[-1]),
        "selection_policy": "complete every validation origin with zero failures, then minimize validation RMSE",
        "selected_on_validation": selected,
        "final_test_models": final_test_models,
        "seed": SEED,
        "command": "python scripts/run_stage5_extensions.py",
        "versions": {
            "numpy": package_version("numpy"),
            "pandas": package_version("pandas"),
            "scikit-learn": package_version("scikit-learn"),
            "statsmodels": package_version("statsmodels"),
        },
    }

    availability = pd.DataFrame(
        [
            {"feature": "gdp_growth_lag1", "available_at_origin": True, "used_by": "ar, ml_lag"},
            {"feature": "gdp_growth_lag2", "available_at_origin": True, "used_by": "ar, ml_lag"},
            {"feature": "gdp_growth_lag4", "available_at_origin": True, "used_by": "ar, ml_lag"},
            {"feature": "cons_growth_lag1", "available_at_origin": True, "used_by": "arimax, var, ml_lag"},
            {"feature": "inv_growth_lag1", "available_at_origin": True, "used_by": "arimax, var, ml_lag"},
            {"feature": "tbilrate_lag1", "available_at_origin": True, "used_by": "arimax, ml_lag"},
            {"feature": "quarter_sin/cos", "available_at_origin": True, "used_by": "ml_lag"},
        ]
    )

    predictions.to_csv(output_root / "predictions.csv", index=False)
    metrics.to_csv(output_root / "metrics.csv", index=False)
    selection.to_csv(output_root / "validation-model-selection.csv", index=False)
    failures.to_csv(output_root / "failures.csv", index=False)
    warning_rows.to_csv(output_root / "warnings.csv", index=False)
    availability.to_csv(output_root / "feature-availability.csv", index=False)
    (output_root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_environment(output_root / "environment.txt")
    write_report(
        output_root / "report.md",
        manifest,
        metrics,
        selection,
        failures,
        warning_rows,
    )
    (output_root / "run.log").write_text(
        "\n".join(
            [
                f"validation_prediction_rows={len(validation)}",
                f"test_prediction_rows={len(test)}",
                f"failure_rows={len(failures)}",
                f"warning_rows={len(warning_rows)}",
                f"selected_model={selected}",
                f"final_test_models={','.join(final_test_models)}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run stage 5 extension models under one frozen protocol.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Artifact output directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = run(args.output.resolve())
    print(
        json.dumps(
            {
                "output": str(args.output.resolve()),
                "selected_on_validation": manifest["selected_on_validation"],
                "final_test_models": manifest["final_test_models"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
