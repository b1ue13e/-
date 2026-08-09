from __future__ import annotations

import csv
from pathlib import Path


def build_bar_summary(ticks_csv: Path) -> dict[str, object]:
    with ticks_csv.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    total_volume = sum(float(row["size"]) for row in rows)
    total_dollar = sum(float(row["size"]) * float(row["price"]) for row in rows)
    volume_threshold = total_volume / 2
    dollar_threshold = total_dollar / 2

    volume_bars = 0
    dollar_bars = 0
    cum_volume = 0.0
    cum_dollar = 0.0
    for row in rows:
        size = float(row["size"])
        dollar_value = size * float(row["price"])
        cum_volume += size
        cum_dollar += dollar_value
        if cum_volume >= volume_threshold:
            volume_bars += 1
            cum_volume = 0.0
        if cum_dollar >= dollar_threshold:
            dollar_bars += 1
            cum_dollar = 0.0

    return {
        "tick_count": len(rows),
        "total_volume": round(total_volume, 6),
        "total_dollar": round(total_dollar, 6),
        "volume_bar_count": volume_bars,
        "dollar_bar_count": dollar_bars,
    }
