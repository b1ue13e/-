from __future__ import annotations

import csv
from pathlib import Path


def build_env_summary(market_state_csv: Path) -> dict[str, object]:
    with market_state_csv.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    feature_columns = [name for name in rows[0].keys() if name not in {"date", "position"}]
    action_space = {"type": "continuous", "low": -1.0, "high": 1.0}
    reward_proxy = round(sum(float(row.get("feature_1", 0.0)) for row in rows) / len(rows), 6)

    return {
        "observations": len(rows),
        "feature_columns": feature_columns,
        "position_column": "position",
        "action_space": action_space,
        "reward_proxy": reward_proxy,
    }
