from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor


def validate_data(data: pd.DataFrame):
    if "date" not in data.columns or "target" not in data.columns:
        raise ValueError("data must contain date and target columns")
    features = sorted(column for column in data.columns if column.startswith("feature_"))
    if not features:
        raise ValueError("at least one feature_ column is required")
    frame = data.loc[:, ["date", *features, "target"]].copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    for column in [*features, "target"]:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    if frame["date"].duplicated().any() or not frame["date"].is_monotonic_increasing:
        raise ValueError("date must be unique and strictly increasing")
    if len(frame) < 100 or not np.isfinite(frame[[*features, "target"]]).all().all():
        raise ValueError("at least 100 finite rows are required")
    return frame, features


def make_demo_data(observations=500, seed=42):
    rng = np.random.default_rng(seed)
    trend = np.sin(np.arange(observations) / 15.0) + rng.normal(0, 0.15, observations)
    volatility = np.abs(rng.normal(0.8, 0.3, observations))
    target = (
        0.012 * (trend > 0.2)
        - 0.009 * (trend < -0.4)
        - 0.004 * volatility
        + rng.normal(0, 0.004, observations)
    )
    return pd.DataFrame({
        "date": pd.bdate_range("2021-01-04", periods=observations),
        "feature_trend": trend,
        "feature_volatility": volatility,
        "target": target,
    })


def chronological_slices(length, train_fraction=0.6, validation_fraction=0.2):
    if not 0.5 <= train_fraction < 0.8:
        raise ValueError("train_fraction must satisfy 0.5 <= value < 0.8")
    if not 0.1 <= validation_fraction <= 0.3:
        raise ValueError("validation_fraction must satisfy 0.1 <= value <= 0.3")
    train_end = int(length * train_fraction)
    validation_end = train_end + int(length * validation_fraction)
    if validation_end >= length:
        raise ValueError("time fractions leave no test rows")
    return slice(0, train_end), slice(train_end, validation_end), slice(validation_end, length)


def evaluate_tree_baseline(data, depths=(2, 3, 4), random_state=42):
    frame, features = validate_data(data)
    train_slice, validation_slice, test_slice = chronological_slices(len(frame))
    x = frame[features].to_numpy()
    y = frame["target"].to_numpy()
    if not depths or any(depth < 1 for depth in depths):
        raise ValueError("depths must contain positive integers")

    validation_scores = {}
    for depth in depths:
        candidate = DecisionTreeRegressor(max_depth=int(depth), random_state=random_state)
        candidate.fit(x[train_slice], y[train_slice])
        validation_scores[int(depth)] = float(
            mean_squared_error(y[validation_slice], candidate.predict(x[validation_slice]))
        )
    selected_depth = min(validation_scores, key=validation_scores.get)

    development_end = validation_slice.stop
    model = DecisionTreeRegressor(max_depth=selected_depth, random_state=random_state)
    model.fit(x[:development_end], y[:development_end])
    predictions = model.predict(x[test_slice])
    baseline = np.full(len(predictions), y[:development_end].mean())
    return {
        "frame": frame,
        "features": features,
        "model": model,
        "train_slice": train_slice,
        "validation_slice": validation_slice,
        "test_slice": test_slice,
        "selected_depth": int(selected_depth),
        "validation_scores": validation_scores,
        "predictions": predictions,
        "baseline_predictions": baseline,
        "test_mse": float(mean_squared_error(y[test_slice], predictions)),
        "baseline_mse": float(mean_squared_error(y[test_slice], baseline)),
    }


def run_pipeline(data, output_dir, depths=(2, 3, 4), random_state=42):
    result = evaluate_tree_baseline(data, depths, random_state)
    frame = result["frame"]
    test_slice = result["test_slice"]
    metrics = {
        "observations": int(len(frame)),
        "train_observations": int(result["train_slice"].stop),
        "validation_observations": int(
            result["validation_slice"].stop - result["validation_slice"].start
        ),
        "test_observations": int(test_slice.stop - test_slice.start),
        "selected_depth": result["selected_depth"],
        "validation_mse_by_depth": result["validation_scores"],
        "test_mse": result["test_mse"],
        "mean_baseline_mse": result["baseline_mse"],
        "feature_importance": dict(
            zip(result["features"], result["model"].feature_importances_.tolist())
        ),
        "random_state": int(random_state),
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "tree_metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    pd.DataFrame({
        "date": frame["date"].iloc[test_slice].dt.strftime("%Y-%m-%d"),
        "actual_target": frame["target"].iloc[test_slice].to_numpy(),
        "tree_prediction": result["predictions"],
        "mean_baseline_prediction": result["baseline_predictions"],
    }).to_csv(output_dir / "test_predictions.csv", index=False)
    return metrics


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Week 8 tree baseline.")
    parser.add_argument("--input", type=Path, help="CSV with date, target, feature_* columns")
    parser.add_argument("--output", type=Path, default=Path("artifacts"))
    parser.add_argument("--depths", type=int, nargs="+", default=[2, 3, 4])
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()
    data = pd.read_csv(args.input) if args.input else make_demo_data(seed=args.seed)
    metrics = run_pipeline(data, args.output, tuple(args.depths), args.seed)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

