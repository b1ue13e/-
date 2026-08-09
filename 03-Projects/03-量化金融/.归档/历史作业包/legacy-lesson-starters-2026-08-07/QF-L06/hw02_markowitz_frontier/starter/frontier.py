from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path


def load_returns(path: Path) -> dict[str, list[float]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            grouped[row["asset"]].append(float(row["value"]))
    return dict(grouped)


def summarize_frontier(returns_csv: Path) -> dict[str, object]:
    grouped = load_returns(returns_csv)
    assets = sorted(grouped)
    asset_stats = []
    inverse_vol_raw: dict[str, float] = {}
    sharpe_proxy_raw: dict[str, float] = {}

    for asset in assets:
        series = grouped[asset]
        mean_return = sum(series) / len(series)
        variance = sum((x - mean_return) ** 2 for x in series) / max(len(series), 1)
        volatility = math.sqrt(variance) if variance > 0 else abs(mean_return) if mean_return != 0 else 1.0
        inverse_vol_raw[asset] = 1.0 / volatility if volatility else 0.0
        sharpe_proxy_raw[asset] = mean_return / volatility if volatility else 0.0
        asset_stats.append(
            {
                "asset": asset,
                "observations": len(series),
                "mean_return": round(mean_return, 6),
                "volatility_proxy": round(volatility, 6),
            }
        )

    equal_weight = {asset: round(1.0 / len(assets), 6) for asset in assets}
    inv_sum = sum(inverse_vol_raw.values()) or 1.0
    inverse_vol_weight = {asset: round(value / inv_sum, 6) for asset, value in inverse_vol_raw.items()}
    sharpe_sum = sum(max(value, 0.0) for value in sharpe_proxy_raw.values()) or 1.0
    tangency_proxy = {
        asset: round(max(value, 0.0) / sharpe_sum, 6) for asset, value in sharpe_proxy_raw.items()
    }

    return {
        "assets": assets,
        "asset_stats": asset_stats,
        "equal_weight": equal_weight,
        "inverse_vol_weight": inverse_vol_weight,
        "tangency_proxy": tangency_proxy,
    }
