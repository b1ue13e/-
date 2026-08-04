from __future__ import annotations

import csv
import json
from pathlib import Path


REQUIRED_FIELDS = ("problem", "dataset", "metric", "baseline", "improvement", "success_threshold", "risks")


def _scores(path: Path) -> list[float]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return [float(row["score"]) for row in csv.DictReader(f)]


def run_smoke(plan_json: Path, baseline_csv: Path, improvement_csv: Path) -> dict[str, object]:
    plan = json.loads(plan_json.read_text(encoding="utf-8"))
    baseline_scores = _scores(baseline_csv)
    improvement_scores = _scores(improvement_csv)
    completeness = sum(1 for field in REQUIRED_FIELDS if field in plan and plan[field]) / len(REQUIRED_FIELDS)
    baseline_avg = sum(baseline_scores) / len(baseline_scores)
    improvement_avg = sum(improvement_scores) / len(improvement_scores)
    delta = improvement_avg - baseline_avg
    threshold = float(plan["success_threshold"])
    meets_threshold = improvement_avg >= threshold
    next_decision = "advance_to_final_report" if meets_threshold and delta > 0 else "revise_project_scope"
    return {
        "proposal_completeness": round(completeness, 4),
        "milestone_status": plan.get("milestone_status", "unknown"),
        "baseline_score": round(baseline_avg, 4),
        "improvement_score": round(improvement_avg, 4),
        "delta": round(delta, 4),
        "meets_success_threshold": meets_threshold,
        "next_decision": next_decision,
        "risk_count": len(plan.get("risks", [])),
    }
