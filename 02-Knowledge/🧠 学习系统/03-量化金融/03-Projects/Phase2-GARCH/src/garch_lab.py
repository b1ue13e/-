from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from math import exp, log
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize


PERSISTENCE_CAP = 0.999
MIN_VARIANCE = 1e-10


@dataclass(frozen=True)
class GarchFit:
    omega: float
    alpha: float
    beta: float
    success: bool
    message: str
    negative_log_likelihood: float
    conditional_variance: np.ndarray


def validate_returns(returns) -> np.ndarray:
    values = np.asarray(returns, dtype=float)
    if values.ndim != 1 or len(values) < 100:
        raise ValueError("returns must be a one-dimensional series with at least 100 rows")
    if not np.isfinite(values).all():
        raise ValueError("returns must be finite and non-missing")
    if np.var(values) <= MIN_VARIANCE:
        raise ValueError("returns must have positive variance")
    return values


def validate_dates(dates, length: int):
    if dates is None:
        return pd.RangeIndex(length, name="observation_index")
    index = pd.DatetimeIndex(pd.to_datetime(dates, errors="raise"))
    if len(index) != length:
        raise ValueError("dates and returns must have the same length")
    if index.has_duplicates or not index.is_monotonic_increasing:
        raise ValueError("dates must be unique and strictly increasing")
    return index


def transformed_parameters(theta) -> tuple[float, float, float]:
    omega = exp(float(np.clip(theta[0], -30.0, 30.0)))
    alpha_weight = exp(float(np.clip(theta[1], -20.0, 20.0)))
    beta_weight = exp(float(np.clip(theta[2], -20.0, 20.0)))
    denominator = 1.0 + alpha_weight + beta_weight
    alpha = PERSISTENCE_CAP * alpha_weight / denominator
    beta = PERSISTENCE_CAP * beta_weight / denominator
    return omega, alpha, beta


def conditional_variance(returns, omega, alpha, beta) -> np.ndarray:
    values = np.asarray(returns, dtype=float)
    variances = np.empty_like(values)
    variances[0] = max(float(np.var(values, ddof=1)), MIN_VARIANCE)
    for index in range(1, len(values)):
        variances[index] = (
            omega
            + alpha * values[index - 1] ** 2
            + beta * variances[index - 1]
        )
        variances[index] = max(variances[index], MIN_VARIANCE)
    return variances


def gaussian_negative_log_likelihood(theta, returns) -> float:
    omega, alpha, beta = transformed_parameters(theta)
    variances = conditional_variance(returns, omega, alpha, beta)
    return float(
        0.5
        * np.sum(
            np.log(2.0 * np.pi)
            + np.log(variances)
            + np.asarray(returns) ** 2 / variances
        )
    )


def fit_garch(returns) -> GarchFit:
    values = validate_returns(returns)
    sample_variance = float(np.var(values, ddof=1))
    alpha_start, beta_start = 0.08, 0.87
    remainder = PERSISTENCE_CAP - alpha_start - beta_start
    initial = np.array([
        log(max(sample_variance * (1.0 - alpha_start - beta_start), MIN_VARIANCE)),
        log(alpha_start / remainder),
        log(beta_start / remainder),
    ])
    result = minimize(
        gaussian_negative_log_likelihood,
        initial,
        args=(values,),
        method="L-BFGS-B",
        options={"maxiter": 1_000, "ftol": 1e-10},
    )
    omega, alpha, beta = transformed_parameters(result.x)
    variances = conditional_variance(values, omega, alpha, beta)
    return GarchFit(
        omega=omega,
        alpha=alpha,
        beta=beta,
        success=bool(result.success),
        message=str(result.message),
        negative_log_likelihood=float(result.fun),
        conditional_variance=variances,
    )


def simulate_garch(
    observations=1_500,
    omega=0.05,
    alpha=0.08,
    beta=0.87,
    burn_in=500,
    seed=42,
):
    if min(observations, burn_in) < 1 or omega <= 0 or min(alpha, beta) < 0:
        raise ValueError("invalid simulation parameters")
    if alpha + beta >= 1:
        raise ValueError("simulation requires alpha + beta < 1")

    rng = np.random.default_rng(seed)
    total = observations + burn_in
    returns = np.empty(total)
    variances = np.empty(total)
    variances[0] = omega / (1.0 - alpha - beta)
    returns[0] = np.sqrt(variances[0]) * rng.standard_normal()
    for index in range(1, total):
        variances[index] = (
            omega
            + alpha * returns[index - 1] ** 2
            + beta * variances[index - 1]
        )
        returns[index] = np.sqrt(variances[index]) * rng.standard_normal()
    return returns[burn_in:], variances[burn_in:]


def qlike_loss(realized_squared, forecast_variance) -> float:
    realized = np.asarray(realized_squared, dtype=float)
    forecast = np.maximum(np.asarray(forecast_variance, dtype=float), MIN_VARIANCE)
    return float(np.mean(np.log(forecast) + realized / forecast))


def evaluate_out_of_sample(returns, train_fraction=0.8, rolling_window=20, dates=None):
    values = validate_returns(returns)
    index = validate_dates(dates, len(values))
    if not 0.5 <= train_fraction < 1.0:
        raise ValueError("train_fraction must satisfy 0.5 <= value < 1")
    if rolling_window < 5:
        raise ValueError("rolling_window must be at least 5")

    split = int(len(values) * train_fraction)
    raw_train, raw_test = values[:split], values[split:]
    training_mean = float(raw_train.mean())
    train, test = raw_train - training_mean, raw_test - training_mean
    if len(train) <= rolling_window or len(test) < 10:
        raise ValueError("time split is too small for evaluation")

    fit = fit_garch(train)
    if not fit.success:
        raise RuntimeError(f"GARCH optimizer failed: {fit.message}")
    previous_return = train[-1]
    previous_variance = fit.conditional_variance[-1]
    history = list(train)
    garch_forecasts = []
    rolling_forecasts = []

    for actual_return in test:
        next_variance = (
            fit.omega
            + fit.alpha * previous_return**2
            + fit.beta * previous_variance
        )
        garch_forecasts.append(max(next_variance, MIN_VARIANCE))
        rolling_forecasts.append(float(np.var(history[-rolling_window:], ddof=1)))

        history.append(float(actual_return))
        previous_return = float(actual_return)
        previous_variance = next_variance

    garch_forecasts = np.asarray(garch_forecasts)
    rolling_forecasts = np.asarray(rolling_forecasts)
    realized_squared = test**2
    return {
        "fit": fit,
        "split": split,
        "training_mean": training_mean,
        "test_returns": raw_test,
        "test_innovations": test,
        "test_index": index[split:],
        "garch_forecasts": garch_forecasts,
        "rolling_forecasts": rolling_forecasts,
        "garch_qlike": qlike_loss(realized_squared, garch_forecasts),
        "rolling_qlike": qlike_loss(realized_squared, rolling_forecasts),
    }


def run_pipeline(
    returns,
    output_dir,
    train_fraction=0.8,
    rolling_window=20,
    data_mode="user_csv",
    dates=None,
):
    result = evaluate_out_of_sample(returns, train_fraction, rolling_window, dates)
    fit = result["fit"]
    metrics = {
        "data_mode": data_mode,
        "return_unit": "percent",
        "mean_model": "constant estimated on training split only",
        "training_mean": result["training_mean"],
        "observations": int(len(returns)),
        "train_observations": int(result["split"]),
        "test_observations": int(len(result["test_returns"])),
        "omega": fit.omega,
        "alpha": fit.alpha,
        "beta": fit.beta,
        "persistence": fit.alpha + fit.beta,
        "optimizer_success": fit.success,
        "optimizer_message": fit.message,
        "negative_log_likelihood": fit.negative_log_likelihood,
        "garch_qlike": result["garch_qlike"],
        "rolling_qlike": result["rolling_qlike"],
        "rolling_window": int(rolling_window),
    }

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "phase2_metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    forecast_frame = pd.DataFrame({
        "actual_return": result["test_returns"],
        "innovation": result["test_innovations"],
        "realized_squared_innovation": result["test_innovations"] ** 2,
        "garch_variance_forecast": result["garch_forecasts"],
        "rolling_variance_forecast": result["rolling_forecasts"],
    })
    if isinstance(result["test_index"], pd.DatetimeIndex):
        forecast_frame.insert(0, "date", result["test_index"].strftime("%Y-%m-%d"))
    else:
        forecast_frame.insert(0, "observation_index", result["test_index"])
    forecast_frame.to_csv(output_dir / "phase2_forecasts.csv", index=False)
    return metrics


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Phase 2 GARCH lab.")
    parser.add_argument("--input", type=Path, help="CSV containing a return column")
    parser.add_argument("--output", type=Path, default=Path("artifacts"))
    parser.add_argument("--train-fraction", type=float, default=0.8)
    parser.add_argument("--rolling-window", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()
    if args.input:
        frame = pd.read_csv(args.input)
        if "return" not in frame.columns:
            raise ValueError("input CSV must contain a return column")
        returns = frame["return"].to_numpy(dtype=float)
        dates = frame["date"].tolist() if "date" in frame.columns else None
        data_mode = "user_csv"
    else:
        returns, _ = simulate_garch(seed=args.seed)
        dates = None
        data_mode = "simulated_garch"

    metrics = run_pipeline(
        returns,
        args.output,
        args.train_fraction,
        args.rolling_window,
        data_mode,
        dates,
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
