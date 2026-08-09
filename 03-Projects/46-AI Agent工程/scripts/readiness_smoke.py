"""Offline readiness smoke for imports, approvals, runtime, and eval data."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

try:
    from .agent_runtime import ApprovalGate, ReviewAgentPipeline, SafeWorkspace
    from .restaurant_pipeline import Review
    from .run_eval import load_cases, run_evaluation
except ImportError:
    from agent_runtime import ApprovalGate, ReviewAgentPipeline, SafeWorkspace
    from restaurant_pipeline import Review
    from run_eval import load_cases, run_evaluation


def run_readiness() -> dict[str, object]:
    runtime_result = ReviewAgentPipeline([Review("A", "stable evidence", 4.0)]).run("A")
    with tempfile.TemporaryDirectory() as directory:
        workspace = SafeWorkspace(Path(directory) / "workspace")
        content = "approved artifact"
        gate = ApprovalGate(secret=b"readiness-smoke-secret-value-32b")
        resource = workspace.approval_resource("artifact.txt")
        request_id = gate.request(
            "workspace_write",
            resource,
            workspace.approval_parameters(content),
        )
        receipt = gate.approve(request_id)
        workspace.write_text("artifact.txt", content, approval_gate=gate, receipt=receipt)
        write_ok = workspace.read_text("artifact.txt") == content

    evaluation = run_evaluation(load_cases())
    return {
        "status": "ready" if runtime_result["status"] == "completed" and write_ok and evaluation["gate_passed"] else "not_ready",
        "runtime_status": runtime_result["status"],
        "approval_write": write_ok,
        "eval_gate": evaluation["gate_passed"],
        "eval_cases": evaluation["case_count"],
    }


def main() -> int:
    result = run_readiness()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
