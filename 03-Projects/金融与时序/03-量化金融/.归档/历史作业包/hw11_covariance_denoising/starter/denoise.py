from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


def build_denoise_summary(returns_csv: Path) -> dict[str, object]:
    grouped: dict[str, list[float]] = defaultdict(list)
    with returns_csv.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            grouped[row["asset"]].append(float(row["value"]))

    raw_variance = {}
    for asset, values in grouped.items():
        mean_value = sum(values) / len(values)
        raw_variance[asset] = sum((x - mean_value) ** 2 for x in values) / len(values)

    avg_variance = sum(raw_variance.values()) / len(raw_variance)
    denoised_variance = {asset: round((var + avg_variance) / 2, 6) for asset, var in raw_variance.items()}
    return {
        "asset_count": len(grouped),
        "raw_variance": {asset: round(var, 6) for asset, var in raw_variance.items()},
        "denoised_variance": denoised_variance,
        "shrinkage_target": round(avg_variance, 6),
    }
