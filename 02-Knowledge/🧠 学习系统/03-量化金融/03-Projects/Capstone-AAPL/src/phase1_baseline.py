from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {"date", "adj_close"}


def validate_prices(data: pd.DataFrame, slow_window: int) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    if slow_window < 2:
        raise ValueError("slow_window must be at least 2")

    clean = data.loc[:, ["date", "adj_close"]].copy()
    clean["date"] = pd.to_datetime(clean["date"], errors="raise")
    clean["adj_close"] = pd.to_numeric(clean["adj_close"], errors="raise")

    if clean["date"].duplicated().any():
        raise ValueError("date must be unique")
    if not clean["date"].is_monotonic_increasing:
        raise ValueError("date must be strictly increasing")
    if clean["adj_close"].isna().any() or (clean["adj_close"] <= 0).any():
        raise ValueError("adj_close must be positive and non-missing")
    if len(clean) < slow_window + 2:
        raise ValueError("not enough observations for the slow window")
    return clean


def max_drawdown(equity: pd.Series) -> float:
    drawdown = equity / equity.cummax() - 1.0
    return float(drawdown.min())


def build_baseline(
    data: pd.DataFrame,
    fast_window: int = 5,
    slow_window: int = 20,
    cost_bps: float = 10.0,
) -> tuple[pd.DataFrame, dict[str, float | int | str]]:
    if not 1 <= fast_window < slow_window:
        raise ValueError("windows must satisfy 1 <= fast_window < slow_window")
    if cost_bps < 0:
        raise ValueError("cost_bps cannot be negative")

    frame = validate_prices(data, slow_window)
    frame["asset_return"] = frame["adj_close"].pct_change()
    frame["fast_sma"] = frame["adj_close"].rolling(fast_window).mean()
    frame["slow_sma"] = frame["adj_close"].rolling(slow_window).mean()
    frame["signal"] = (frame["fast_sma"] > frame["slow_sma"]).astype(float)

    # Signal is known after the current close; the position applies one period later.
    frame["position"] = frame["signal"].shift(1).fillna(0.0)
    frame["turnover"] = frame["position"].diff().abs().fillna(frame["position"].abs())
    frame["strategy_return"] = (
        frame["position"] * frame["asset_return"]
        - frame["turnover"] * cost_bps / 10_000.0
    ).fillna(0.0)
    frame["equity"] = (1.0 + frame["strategy_return"]).cumprod()
    frame["drawdown"] = frame["equity"] / frame["equity"].cummax() - 1.0

    volatility = frame["strategy_return"].std(ddof=1) * np.sqrt(252)
    metrics: dict[str, float | int | str] = {
        "start_date": frame["date"].iloc[0].date().isoformat(),
        "end_date": frame["date"].iloc[-1].date().isoformat(),
        "observations": int(len(frame)),
        "fast_window": int(fast_window),
        "slow_window": int(slow_window),
        "cost_bps": float(cost_bps),
        "total_return": float(frame["equity"].iloc[-1] - 1.0),
        "max_drawdown": max_drawdown(frame["equity"]),
        "annualized_volatility": float(volatility),
        "total_turnover": float(frame["turnover"].sum()),
    }
    return frame, metrics


def make_demo_prices(periods: int = 100) -> pd.DataFrame:
    dates = pd.bdate_range("2024-01-02", periods=periods)
    steps = 0.0005 + 0.008 * np.sin(np.arange(periods) / 5.0)
    prices = 100.0 * np.exp(np.cumsum(steps))
    return pd.DataFrame({"date": dates, "adj_close": prices})


def run_pipeline(
    data: pd.DataFrame,
    output_dir: Path,
    fast_window: int,
    slow_window: int,
    cost_bps: float,
) -> dict[str, float | int | str]:
    frame, metrics = build_baseline(data, fast_window, slow_window, cost_bps)
    output_dir.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_dir / "equity_curve.csv", index=False)
    (output_dir / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the no-look-ahead Phase 1 baseline.")
    parser.add_argument("--input", type=Path, help="CSV with date and adj_close columns")
    parser.add_argument("--output", type=Path, default=Path("artifacts"))
    parser.add_argument("--fast-window", type=int, default=5)
    parser.add_argument("--slow-window", type=int, default=20)
    parser.add_argument("--cost-bps", type=float, default=10.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = pd.read_csv(args.input) if args.input else make_demo_prices()
    metrics = run_pipeline(
        data=data,
        output_dir=args.output,
        fast_window=args.fast_window,
        slow_window=args.slow_window,
        cost_bps=args.cost_bps,
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

