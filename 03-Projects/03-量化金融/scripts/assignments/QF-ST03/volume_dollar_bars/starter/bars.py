from __future__ import annotations

import csv
from pathlib import Path


def _close_bar(rows: list[dict[str, object]]) -> dict[str, object]:
    prices = [float(row["price"]) for row in rows]
    sizes = [float(row["size"]) for row in rows]
    return {
        "start": rows[0]["timestamp"],
        "end": rows[-1]["timestamp"],
        "open": prices[0],
        "high": max(prices),
        "low": min(prices),
        "close": prices[-1],
        "volume": round(sum(sizes), 8),
        "dollar_value": round(sum(price * size for price, size in zip(prices, sizes)), 8),
        "ticks": len(rows),
    }


def _build_bars(
    rows: list[dict[str, object]], metric: str, threshold: float
) -> list[dict[str, object]]:
    bars: list[dict[str, object]] = []
    current: list[dict[str, object]] = []
    accumulated = 0.0
    for row in rows:
        current.append(row)
        size = float(row["size"])
        accumulated += size if metric == "volume" else size * float(row["price"])
        if accumulated >= threshold:
            bars.append(_close_bar(current))
            current = []
            accumulated = 0.0
    if current:
        bars.append(_close_bar(current))
    return bars


def build_bar_summary(
    ticks_csv: Path, volume_threshold: float | None = None, dollar_threshold: float | None = None
) -> dict[str, object]:
    with ticks_csv.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    if not rows:
        raise ValueError("tick input must not be empty")

    timestamps = [row["timestamp"] for row in rows]
    if timestamps != sorted(timestamps):
        raise ValueError("ticks must be sorted by timestamp")
    if any(float(row["price"]) <= 0 or float(row["size"]) <= 0 for row in rows):
        raise ValueError("tick prices and sizes must be positive")

    total_volume = sum(float(row["size"]) for row in rows)
    total_dollar = sum(float(row["size"]) * float(row["price"]) for row in rows)
    if volume_threshold is None:
        volume_threshold = total_volume / 3.0
    if dollar_threshold is None:
        dollar_threshold = total_dollar / 3.0
    if volume_threshold <= 0 or dollar_threshold <= 0:
        raise ValueError("bar thresholds must be positive")
    volume_bars = _build_bars(rows, "volume", volume_threshold)
    dollar_bars = _build_bars(rows, "dollar", dollar_threshold)

    return {
        "method": "threshold_activity_bars",
        "tick_count": len(rows),
        "total_volume": round(total_volume, 8),
        "total_dollar": round(total_dollar, 8),
        "volume_threshold": round(volume_threshold, 8),
        "dollar_threshold": round(dollar_threshold, 8),
        "volume_bars": volume_bars,
        "dollar_bars": dollar_bars,
        "volume_conserved": abs(sum(bar["volume"] for bar in volume_bars) - total_volume) < 1e-10,
        "dollar_conserved": abs(sum(bar["dollar_value"] for bar in dollar_bars) - total_dollar) < 1e-8,
    }
