from __future__ import annotations

import csv
from pathlib import Path


def build_tail_risk_summary(returns_csv: Path) -> dict[str, object]:
    with returns_csv.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    returns = [float(row["value"]) for row in rows]
    sorted_returns = sorted(returns)
    threshold = sorted_returns[0]
    exceedances = [round(threshold - value, 6) for value in returns if value <= threshold]
    es_proxy = round(sum(sorted_returns[: max(1, len(sorted_returns) // 2)]) / max(1, len(sorted_returns) // 2), 6)

    return {
        "observations": len(returns),
        "threshold_proxy": round(threshold, 6),
        "tail_event_count": len(exceedances),
        "exceedances": exceedances,
        "es_proxy": es_proxy,
    }
