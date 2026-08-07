from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path


def _load_returns(path: Path) -> dict[str, list[float]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            grouped[row["asset"]].append(float(row["value"]))
    return dict(grouped)


def _variance(values: list[float]) -> float:
    mean_value = sum(values) / len(values)
    return sum((x - mean_value) ** 2 for x in values) / max(len(values), 1)


def build_hrp_proxy(returns_csv: Path) -> dict[str, object]:
    grouped = _load_returns(returns_csv)
    assets = sorted(grouped)
    cluster_order = sorted(assets, key=lambda asset: (_variance(grouped[asset]), asset))
    inverse_variance = {}
    for asset in assets:
        variance = _variance(grouped[asset])
        inverse_variance[asset] = 1.0 / (variance if variance > 0 else 1.0)

    total = sum(inverse_variance.values()) or 1.0
    hrp_proxy_weight = {asset: round(value / total, 6) for asset, value in inverse_variance.items()}
    equal_weight = {asset: round(1.0 / len(assets), 6) for asset in assets}
    return {
        "assets": assets,
        "cluster_order": cluster_order,
        "equal_weight": equal_weight,
        "hrp_proxy_weight": hrp_proxy_weight,
    }
