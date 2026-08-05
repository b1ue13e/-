from __future__ import annotations

import argparse
import json
from math import log
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm


def validate_input(data: pd.DataFrame) -> pd.DataFrame:
    required = {"date", "return"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    frame = data.loc[:, ["date", "return"]].copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    frame["return"] = pd.to_numeric(frame["return"], errors="raise")
    if frame["date"].duplicated().any() or not frame["date"].is_monotonic_increasing:
        raise ValueError("date must be unique and strictly increasing")
    if len(frame) < 100 or not np.isfinite(frame["return"]).all():
        raise ValueError("at least 100 finite returns are required")
    return frame


def kupiec_test(violations, expected_probability):
    observed = np.asarray(violations, dtype=bool)
    if len(observed) == 0 or not 0 < expected_probability < 1:
        raise ValueError("invalid violations or expected probability")
    count = int(observed.sum())
    total = int(len(observed))
    observed_probability = count / total

    def log_term(number, probability):
        return 0.0 if number == 0 else number * log(probability)

    null_log_likelihood = (
        log_term(count, expected_probability)
        + log_term(total - count, 1.0 - expected_probability)
    )
    if count in (0, total):
        alternative_log_likelihood = 0.0
    else:
        alternative_log_likelihood = (
            log_term(count, observed_probability)
            + log_term(total - count, 1.0 - observed_probability)
        )
    likelihood_ratio = max(
        0.0,
        -2.0 * (null_log_likelihood - alternative_log_likelihood),
    )
    return {
        "observations": total,
        "violations": count,
        "violation_rate": observed_probability,
        "expected_rate": float(expected_probability),
        "likelihood_ratio": float(likelihood_ratio),
        "p_value": float(chi2.sf(likelihood_ratio, df=1)),
    }


def evaluate_dynamic_var(data, confidence=0.99, window=60, train_fraction=0.8):
    frame = validate_input(data)
    if not 0.5 <= train_fraction < 1.0:
        raise ValueError("train_fraction must satisfy 0.5 <= value < 1")
    if not 0.9 <= confidence < 1.0:
        raise ValueError("confidence must satisfy 0.9 <= value < 1")
    if window < 20:
        raise ValueError("window must be at least 20")

    split = int(len(frame) * train_fraction)
    if split < window or len(frame) - split < 10:
        raise ValueError("time split is too small")
    values = frame["return"].to_numpy()
    normal_quantile = norm.ppf(confidence)
    rows = []
    for index in range(split, len(frame)):
        history = values[index - window:index]
        normal_var = max(
            0.0,
            normal_quantile * float(np.std(history, ddof=1)) - float(np.mean(history)),
        )
        historical_var = max(0.0, -float(np.quantile(history, 1.0 - confidence)))
        loss = -float(values[index])
        rows.append({
            "date": frame["date"].iloc[index].strftime("%Y-%m-%d"),
            "return": float(values[index]),
            "loss": loss,
            "normal_var": normal_var,
            "historical_var": historical_var,
            "normal_violation": loss > normal_var,
            "historical_violation": loss > historical_var,
        })
    forecasts = pd.DataFrame(rows)
    expected_probability = 1.0 - confidence
    return {
        "split": split,
        "forecasts": forecasts,
        "normal_kupiec": kupiec_test(forecasts["normal_violation"], expected_probability),
        "historical_kupiec": kupiec_test(
            forecasts["historical_violation"], expected_probability
        ),
    }


def make_demo_data(observations=1_000, seed=42):
    rng = np.random.default_rng(seed)
    volatility = np.where(np.arange(observations) < observations // 2, 0.01, 0.025)
    returns = 0.0002 + volatility * rng.standard_t(df=6, size=observations)
    return pd.DataFrame({
        "date": pd.bdate_range("2020-01-02", periods=observations),
        "return": returns,
    })


def run_pipeline(data, output_dir, confidence=0.99, window=60, train_fraction=0.8):
    result = evaluate_dynamic_var(data, confidence, window, train_fraction)
    metrics = {
        "confidence": float(confidence),
        "window": int(window),
        "train_observations": int(result["split"]),
        "test_observations": int(len(result["forecasts"])),
        "normal_kupiec": result["normal_kupiec"],
        "historical_kupiec": result["historical_kupiec"],
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "var_metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    result["forecasts"].to_csv(output_dir / "var_forecasts.csv", index=False)
    return metrics


def parse_args():
    parser = argparse.ArgumentParser(description="Run the HW06 dynamic VaR lab.")
    parser.add_argument("--input", type=Path, help="CSV with date and return columns")
    parser.add_argument("--output", type=Path, default=Path("artifacts"))
    parser.add_argument("--confidence", type=float, default=0.99)
    parser.add_argument("--window", type=int, default=60)
    parser.add_argument("--train-fraction", type=float, default=0.8)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()
    data = pd.read_csv(args.input) if args.input else make_demo_data(seed=args.seed)
    metrics = run_pipeline(
        data,
        args.output,
        args.confidence,
        args.window,
        args.train_fraction,
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

