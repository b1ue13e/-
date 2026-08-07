from __future__ import annotations

import csv
from pathlib import Path


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_audit_summary(strategy_csv: Path, parameter_csv: Path) -> dict[str, object]:
    strategy_rows = _read_csv(strategy_csv)
    parameter_rows = _read_csv(parameter_csv)

    returns = [float(row["value"]) for row in strategy_rows]
    scores = [float(row["score"]) for row in parameter_rows]
    best_score = max(scores)
    median_score = sorted(scores)[len(scores) // 2]
    pbo_proxy = sum(1 for score in scores if score < median_score) / len(scores)

    folds = [
        {"fold_id": 1, "train_end": strategy_rows[0]["date"], "embargo_days": 1},
        {"fold_id": 2, "train_end": strategy_rows[-1]["date"], "embargo_days": 1},
    ]
    return {
        "strategy_observations": len(strategy_rows),
        "parameter_runs": len(parameter_rows),
        "gross_return_sum": round(sum(returns), 6),
        "best_score": round(best_score, 6),
        "median_score": round(median_score, 6),
        "pbo_proxy": round(pbo_proxy, 6),
        "cpcv_folds": folds,
    }
