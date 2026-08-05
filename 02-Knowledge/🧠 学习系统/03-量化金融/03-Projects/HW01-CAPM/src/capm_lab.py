from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {"date", "asset_return", "market_return"}


@dataclass(frozen=True)
class CapmFit:
    alpha: float
    beta: float
    alpha_se: float
    beta_se: float
    alpha_t: float
    beta_t: float
    r_squared: float
    residual_variance: float


def validate_data(data: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    frame = data.loc[:, sorted(REQUIRED_COLUMNS)].copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    for column in ("asset_return", "market_return"):
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    if frame["date"].duplicated().any() or not frame["date"].is_monotonic_increasing:
        raise ValueError("date must be unique and strictly increasing")
    if frame[["asset_return", "market_return"]].isna().any().any():
        raise ValueError("returns must be finite and non-missing")
    if not np.isfinite(frame[["asset_return", "market_return"]].to_numpy()).all():
        raise ValueError("returns must be finite")
    if len(frame) < 20:
        raise ValueError("at least 20 observations are required")
    return frame


def fit_capm(asset_return, market_return) -> CapmFit:
    asset = np.asarray(asset_return, dtype=float)
    market = np.asarray(market_return, dtype=float)
    if len(asset) != len(market) or len(asset) < 3:
        raise ValueError("asset and market returns must have equal length >= 3")
    design = np.column_stack([np.ones(len(market)), market])
    if np.linalg.matrix_rank(design) < 2:
        raise ValueError("market return has no variation")
    coefficients, _, _, _ = np.linalg.lstsq(design, asset, rcond=None)
    residuals = asset - design @ coefficients
    degrees_of_freedom = len(asset) - design.shape[1]
    residual_variance = float(np.sum(residuals**2) / degrees_of_freedom)
    covariance = residual_variance * np.linalg.inv(design.T @ design)
    standard_errors = np.sqrt(np.diag(covariance))
    total_sum_squares = np.sum((asset - asset.mean()) ** 2)
    r_squared = 1.0 - np.sum(residuals**2) / total_sum_squares
    return CapmFit(
        alpha=float(coefficients[0]),
        beta=float(coefficients[1]),
        alpha_se=float(standard_errors[0]),
        beta_se=float(standard_errors[1]),
        alpha_t=float(coefficients[0] / standard_errors[0]),
        beta_t=float(coefficients[1] / standard_errors[1]),
        r_squared=float(r_squared),
        residual_variance=residual_variance,
    )


def make_demo_data(observations=400, seed=42):
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2022-01-03", periods=observations)
    market = rng.normal(0.0003, 0.01, observations)
    asset = 0.0002 + 1.2 * market + rng.normal(0.0, 0.008, observations)
    return pd.DataFrame({"date": dates, "asset_return": asset, "market_return": market})


def run_pipeline(data, output_dir, train_fraction=0.8):
    frame = validate_data(data)
    if not 0.5 <= train_fraction < 1.0:
        raise ValueError("train_fraction must satisfy 0.5 <= value < 1")
    split = int(len(frame) * train_fraction)
    train, test = frame.iloc[:split], frame.iloc[split:]
    fit = fit_capm(train["asset_return"], train["market_return"])
    predictions = fit.alpha + fit.beta * test["market_return"].to_numpy()
    baseline_prediction = np.full(len(test), train["asset_return"].mean())
    model_mse = float(np.mean((test["asset_return"] - predictions) ** 2))
    baseline_mse = float(np.mean((test["asset_return"] - baseline_prediction) ** 2))
    metrics = {
        "observations": int(len(frame)),
        "train_observations": int(len(train)),
        "test_observations": int(len(test)),
        "alpha": fit.alpha,
        "beta": fit.beta,
        "alpha_se": fit.alpha_se,
        "beta_se": fit.beta_se,
        "alpha_t": fit.alpha_t,
        "beta_t": fit.beta_t,
        "r_squared": fit.r_squared,
        "test_mse": model_mse,
        "mean_baseline_mse": baseline_mse,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    pd.DataFrame({
        "date": test["date"].dt.strftime("%Y-%m-%d"),
        "actual_asset_return": test["asset_return"].to_numpy(),
        "market_return": test["market_return"].to_numpy(),
        "capm_prediction": predictions,
        "mean_baseline_prediction": baseline_prediction,
    }).to_csv(output_dir / "test_predictions.csv", index=False)
    return metrics


def parse_args():
    parser = argparse.ArgumentParser(description="Run the reproducible HW01 CAPM lab.")
    parser.add_argument("--input", type=Path, help="CSV with date, asset_return, market_return")
    parser.add_argument("--output", type=Path, default=Path("artifacts"))
    parser.add_argument("--train-fraction", type=float, default=0.8)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()
    data = pd.read_csv(args.input) if args.input else make_demo_data(seed=args.seed)
    metrics = run_pipeline(data, args.output, args.train_fraction)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

