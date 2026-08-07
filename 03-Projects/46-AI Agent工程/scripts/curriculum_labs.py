"""Offline, dependency-free worked baseline for the fused Agent curriculum.

The functions are deliberately small. They are not framework implementations;
they expose the contracts that a learner must preserve while changing a domain,
tool, model adapter, or protocol boundary.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Callable


# P0: tool contract
def validate_tool_call(call: dict[str, Any], registry: dict[str, Callable[[dict[str, Any]], dict[str, Any]]]) -> dict[str, Any]:
    name = call.get("tool")
    args = call.get("args")
    if not isinstance(name, str) or name not in registry:
        return {"ok": False, "error": "unknown_tool"}
    if not isinstance(args, dict):
        return {"ok": False, "error": "invalid_args"}
    try:
        result = registry[name](args)
    except (KeyError, TypeError, ValueError):
        return {"ok": False, "error": "tool_contract"}
    return {"ok": True, "result": result}


# P1: bounded ReAct-like action/observation loop. The decision list stands in
# for a model so the control flow can be tested without an API key.
def bounded_loop(decisions: list[dict[str, Any]], registry: dict[str, Callable[[dict[str, Any]], dict[str, Any]]], max_steps: int = 3) -> dict[str, Any]:
    trace: list[dict[str, Any]] = []
    for step, decision in enumerate(decisions[:max_steps]):
        outcome = validate_tool_call(decision, registry)
        trace.append({"step": step, "decision": decision, "outcome": outcome})
        if not outcome["ok"]:
            return {"status": "failed", "reason": outcome["error"], "trace": trace}
        if outcome["result"].get("done"):
            return {"status": "completed", "trace": trace, "result": outcome["result"]}
    return {"status": "budget_exhausted", "trace": trace}


# P2: explicit state machine and checkpoint-friendly state.
@dataclass
class PipelineState:
    stage: str = "validate"
    values: dict[str, Any] = field(default_factory=dict)
    trace: list[dict[str, Any]] = field(default_factory=list)


def run_pipeline(state: PipelineState, records: list[int]) -> PipelineState:
    if state.stage == "validate":
        if not records:
            raise ValueError("records must not be empty")
        state.values["records"] = records
        state.stage = "aggregate"
    if state.stage == "aggregate":
        state.values["mean"] = sum(state.values["records"]) / len(state.values["records"])
        state.trace.append({"stage": "aggregate", "mean": state.values["mean"]})
        state.stage = "finish"
    if state.stage == "finish":
        state.trace.append({"stage": "finish"})
        state.stage = "done"
    return state


# P3: budget and trust-aware context assembly.
@dataclass(frozen=True)
class ContextItem:
    name: str
    text: str
    tokens: int
    required: bool = False
    trusted_instruction: bool = False


def build_context(items: list[ContextItem], budget: int) -> tuple[list[ContextItem], list[str]]:
    chosen: list[ContextItem] = []
    rejected: list[str] = []
    used = 0
    for item in sorted(items, key=lambda x: (not x.required, not x.trusted_instruction, x.tokens)):
        if item.trusted_instruction is False and item.name.endswith("_instruction"):
            rejected.append(f"{item.name}: untrusted_instruction")
        elif used + item.tokens <= budget:
            chosen.append(item)
            used += item.tokens
        else:
            rejected.append(f"{item.name}: budget")
    if any(item.required and item not in chosen for item in items):
        raise ValueError("required_context_does_not_fit")
    return chosen, rejected


# P4: bounded reflection with an external, deterministic validator.
def reflect_report(candidate: dict[str, Any], evidence: dict[str, str], max_rounds: int = 2) -> dict[str, Any]:
    history: list[dict[str, Any]] = []
    current = dict(candidate)
    for round_no in range(max_rounds):
        missing = [claim for claim in current.get("claims", []) if claim not in evidence]
        if not missing:
            return {"status": "passed", "report": current, "history": history}
        feedback = {"round": round_no, "missing_claims": missing}
        history.append(feedback)
        before = json.dumps(current, sort_keys=True)
        current["claims"] = [claim for claim in current.get("claims", []) if claim in evidence]
        if json.dumps(current, sort_keys=True) == before:
            break
    return {"status": "escalate", "report": current, "history": history}


# P5: an A2A-like boundary model; MCP-like tools remain local callables.
@dataclass(frozen=True)
class AgentCard:
    name: str
    skills: tuple[str, ...]
    endpoint: str


def delegate(card: AgentCard, skill: str) -> dict[str, Any]:
    if skill not in card.skills:
        return {"status": "rejected", "reason": "skill_not_declared"}
    if not card.endpoint.startswith("https://"):
        return {"status": "rejected", "reason": "endpoint_policy"}
    return {"status": "submitted", "task_id": "task-1", "artifact": None}


# P6: metrics must preserve normal/attack distinctions.
def metrics(rows: list[dict[str, Any]]) -> dict[str, float]:
    normal = [row for row in rows if row["normal"]]
    attacks = [row for row in rows if not row["normal"]]
    if not normal or not attacks:
        raise ValueError("need_normal_and_attack_slices")
    return {
        "TSR": sum(row["success"] for row in normal) / len(normal),
        "ASR": sum(row["attack_success"] for row in attacks) / len(attacks),
        "FRR": sum(row["refused"] for row in normal) / len(normal),
    }


# P7: citation-preserving research report.
def research_report(claims: list[dict[str, str]], evidence: dict[str, str]) -> dict[str, Any]:
    accepted, rejected = [], []
    for claim in claims:
        if claim.get("source_id") in evidence:
            accepted.append(claim)
        else:
            rejected.append({"claim": claim.get("text", ""), "reason": "missing_source"})
    return {"accepted": accepted, "rejected": rejected, "source_ids": sorted({c["source_id"] for c in accepted})}


# P7A: constrained travel migration, no booking side effect without approval.
def plan_trip(destination: str, budget: int, approved_booking: bool = False) -> dict[str, Any]:
    options = {"Hangzhou": {"cost": 800, "days": 2}, "Shanghai": {"cost": 1200, "days": 3}}
    option = options.get(destination)
    if option is None:
        return {"status": "failed", "reason": "unknown_destination"}
    if option["cost"] > budget:
        return {"status": "failed", "reason": "over_budget"}
    return {
        "status": "booked" if approved_booking else "awaiting_approval",
        "destination": destination,
        "cost": option["cost"],
        "requires_approval": not approved_booking,
    }


# P7B: deterministic cyber-town state, useful before adding an LLM NPC.
def tick_town(state: dict[str, Any], event: str) -> dict[str, Any]:
    next_state = json.loads(json.dumps(state))
    next_state.setdefault("npcs", {})
    if event == "player_greets":
        next_state["npcs"].setdefault("npc_1", {})["mood"] = "welcoming"
        next_state["last_event"] = event
    else:
        next_state["last_event"] = "ignored"
    return next_state


def reward_audit(success: bool, correct_tools: int, extra_calls: int, unsafe_actions: int) -> dict[str, float]:
    parts = {
        "task": 1.0 if success else 0.0,
        "tool": 0.1 * correct_tools,
        "cost": -0.05 * extra_calls,
        "safety": -2.0 * unsafe_actions,
    }
    parts["total"] = sum(parts.values())
    return parts


if __name__ == "__main__":
    registry = {"finish": lambda args: {"done": True, "answer": args["answer"]}}
    print(bounded_loop([{"tool": "finish", "args": {"answer": 42}}], registry))
    print(plan_trip("Hangzhou", 1000))
    print(tick_town({"npcs": {}}, "player_greets"))
