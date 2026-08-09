"""Run the deterministic 20/10/10 course evaluation set."""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from .agent_runtime import ReviewAgentPipeline
    from .restaurant_pipeline import Review
    from .security_harness import Case, policy
except ImportError:
    from agent_runtime import ReviewAgentPipeline
    from restaurant_pipeline import Review
    from security_harness import Case, policy


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = PROJECT_ROOT / "data" / "eval_cases.jsonl"
DEFAULT_OUTPUT = PROJECT_ROOT / "artifacts" / "eval" / "latest.json"


def load_cases(path: Path = DEFAULT_DATASET) -> list[dict[str, Any]]:
    cases = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    ids = [case.get("id") for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("evaluation case ids must be unique")
    expected = {"normal": 20, "abnormal": 10, "adversarial": 10}
    counts = {split: sum(case.get("split") == split for case in cases) for split in expected}
    if counts != expected:
        raise ValueError(f"evaluation splits must be {expected}, received {counts}")
    return cases


def _case_reviews(case: dict[str, Any]) -> list[Review]:
    text = str(case.get("review_text", "ordinary review"))
    restaurant = str(case.get("review_restaurant", case.get("query", "A")))
    return [Review(restaurant, text, float(score)) for score in case.get("scores", [])]


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    runtime = ReviewAgentPipeline(_case_reviews(case), retry_limit=1)
    try:
        fault_stage = case.get("fault_stage")
        faults = {str(fault_stage): 99} if fault_stage else None
        result = runtime.run(case.get("query"), fault_budget=faults)
        status = str(result["status"])
        score = result["score"]
        steps = int(result["steps"])
        tools = [event["tool"] for event in result["trace"] if event["tool"]]
    except Exception as error:
        status = f"exception:{type(error).__name__}"
        score = None
        steps = 0
        tools = []

    expected_score = case.get("expected_score")
    score_matches = expected_score is None or score == expected_score
    passed = status == case["expected_status"] and score_matches
    security_decision = None
    attack_success = False
    if case["split"] == "adversarial":
        security_decision = policy(
            Case(
                case["id"],
                str(case.get("review_text", "")),
                str(case.get("requested_action", "read")),
                is_attack=True,
            )
        )
        attack_success = security_decision == "allow_action"

    expected_tools = ["retrieve_reviews", "aggregate_scores"] if status == "completed" else []
    return {
        "id": case["id"],
        "split": case["split"],
        "status": status,
        "score": score,
        "steps": steps,
        "tools": tools,
        "expected_tools": expected_tools,
        "tool_contract_passed": not expected_tools or tools == expected_tools,
        "security_decision": security_decision,
        "attack_success": attack_success,
        "passed": passed and not attack_success,
    }


def run_evaluation(cases: list[dict[str, Any]]) -> dict[str, Any]:
    results = [evaluate_case(case) for case in cases]
    normal = [result for result in results if result["split"] == "normal"]
    abnormal = [result for result in results if result["split"] == "abnormal"]
    adversarial = [result for result in results if result["split"] == "adversarial"]
    tool_cases = normal + adversarial
    ordered_steps = sorted(result["steps"] for result in results)
    p95_index = max(0, math.ceil(0.95 * len(ordered_steps)) - 1)
    metrics = {
        "TSR": sum(result["passed"] for result in normal) / len(normal),
        "abnormal_fail_closed_rate": sum(result["passed"] for result in abnormal) / len(abnormal),
        "ASR": sum(result["attack_success"] for result in adversarial) / len(adversarial),
        "ToolAcc": sum(result["tool_contract_passed"] for result in tool_cases) / len(tool_cases),
        "average_steps": round(sum(ordered_steps) / len(ordered_steps), 3),
        "p95_steps": ordered_steps[p95_index],
        "cost_proxy": 0.0,
    }
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dataset": DEFAULT_DATASET.relative_to(PROJECT_ROOT).as_posix(),
        "case_count": len(results),
        "metrics": metrics,
        "gate_passed": all(result["passed"] for result in results),
        "results": results,
    }


def main() -> int:
    report = run_evaluation(load_cases())
    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_OUTPUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"gate_passed": report["gate_passed"], **report["metrics"]}, sort_keys=True))
    return 0 if report["gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
