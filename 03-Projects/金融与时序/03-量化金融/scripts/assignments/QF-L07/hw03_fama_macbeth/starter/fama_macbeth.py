from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_fama_macbeth_summary(asset_panel_csv: Path, factor_panel_csv: Path) -> dict[str, object]:
    asset_rows = _read_rows(asset_panel_csv)
    factor_rows = _read_rows(factor_panel_csv)

    grouped_target: dict[str, list[float]] = defaultdict(list)
    grouped_factor: dict[str, list[float]] = defaultdict(list)
    for row in asset_rows:
        grouped_target[row["asset"]].append(float(row["target"]))
        grouped_factor[row["asset"]].append(float(row["factor_1"]))

    assets = sorted(grouped_target)
    exposure_summary = []
    cross_section_premium = []
    for asset in assets:
        avg_target = sum(grouped_target[asset]) / len(grouped_target[asset])
        avg_factor = sum(grouped_factor[asset]) / len(grouped_factor[asset])
        exposure_summary.append(
            {
                "asset": asset,
                "avg_factor_loading": round(avg_factor, 6),
                "avg_target_return": round(avg_target, 6),
            }
        )
        cross_section_premium.append(avg_factor * avg_target)

    return {
        "asset_count": len(assets),
        "factor_row_count": len(factor_rows),
        "risk_premium_proxy": round(sum(cross_section_premium) / len(cross_section_premium), 6),
        "exposure_summary": exposure_summary,
    }
