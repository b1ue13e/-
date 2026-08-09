from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def build_baseline_summary(
    ohlcv_csv: Path, short_window: int = 5, long_window: int = 20, cost_rate: float = 0.0005
) -> dict[str, object]:
    if not 1 < short_window < long_window or cost_rate < 0:
        raise ValueError("invalid windows or cost rate")
    frame = pd.read_csv(ohlcv_csv, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
    required = {"date", "open", "high", "low", "close", "volume", "adjustment_factor"}
    if not required <= set(frame.columns) or len(frame) <= long_window:
        raise ValueError("OHLCV input lacks required fields or history")
    if frame["date"].duplicated().any() or not frame["date"].is_monotonic_increasing:
        raise ValueError("dates must be unique and increasing")
    if (frame[["open", "high", "low", "close", "adjustment_factor"]] <= 0).any().any():
        raise ValueError("prices and adjustment factors must be positive")
    if (frame["volume"] < 0).any():
        raise ValueError("volume must be non-negative; zero volume may represent a valid halt")

    adjusted_close = frame["close"] * frame["adjustment_factor"]
    adjusted_open = frame["open"] * frame["adjustment_factor"]
    short_average = adjusted_close.rolling(short_window).mean()
    long_average = adjusted_close.rolling(long_window).mean()
    signal = (short_average > long_average).astype(float)
    position = signal.shift(1).fillna(0.0)
    next_open_return = (adjusted_open.shift(-1) / adjusted_open - 1.0).fillna(0.0)
    turnover = position.diff().abs().fillna(position.abs())
    gross = position * next_open_return
    cost = turnover * cost_rate
    net = gross - cost
    equity = (1.0 + net).cumprod()
    drawdown = equity / equity.cummax() - 1.0
    leaky_gross = signal * next_open_return

    return {
        "method": "lagged_ma_baseline",
        "observations": len(frame),
        "short_window": short_window,
        "long_window": long_window,
        "cost_rate": cost_rate,
        "execution_protocol": "close_signal_next_open_entry_next_open_return",
        "gross_return_sum": round(float(gross.sum()), 10),
        "cost_sum": round(float(cost.sum()), 10),
        "net_return_sum": round(float(net.sum()), 10),
        "max_drawdown": round(float(drawdown.min()), 10),
        "signal_is_lagged": bool(np.allclose(position.iloc[1:].to_numpy(), signal.iloc[:-1].to_numpy())),
        "leakage_negative_control_differs": bool(not np.allclose(gross.to_numpy(), leaky_gross.to_numpy())),
        "net_identity_holds": bool(np.allclose(net.to_numpy(), gross.to_numpy() - cost.to_numpy())),
    }
