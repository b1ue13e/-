"""Deterministic Agent runtime used by the local teaching acceptance gate."""

from __future__ import annotations

import hashlib
import json
import time
import urllib.request
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Protocol
from urllib.parse import urlparse

from restaurant_pipeline import Review, aggregate_score, select_reviews


REQUIRED_STAGES = ("intake", "retrieve", "score", "aggregate", "finalize")


@dataclass(frozen=True)
class PipelineDefinition:
    stages: tuple[str, ...] = REQUIRED_STAGES

    def validate(self) -> None:
        if len(set(self.stages)) != len(self.stages):
            raise ValueError("pipeline stages must be unique")
        missing = [stage for stage in REQUIRED_STAGES if stage not in self.stages]
        if missing:
            raise ValueError(f"missing required stages: {missing}")
        positions = [self.stages.index(stage) for stage in REQUIRED_STAGES]
        if positions != sorted(positions):
            raise ValueError("required stages must preserve dependency order")


@dataclass(frozen=True)
class Message:
    sender: str
    recipient: str
    kind: str
    payload: dict[str, object]


@dataclass(frozen=True)
class TraceEvent:
    trace_id: str
    step: int
    stage: str
    actor: str
    action: str
    outcome: str
    tool: str | None = None
    latency_ms: float = 0.0
    cost: float = 0.0
    retry: int = 0
    policy_decision: str = "allow"


@dataclass(frozen=True)
class ToolSpec:
    name: str
    required_args: tuple[str, ...]
    handler: Callable[..., object]


@dataclass(frozen=True)
class Decision:
    action: str
    tool: str | None = None


class DecisionModel(Protocol):
    name: str

    def decide(self, stage: str, observation: dict[str, object]) -> Decision:
        """Choose the next typed action from a sanitized observation."""


class DeterministicDecisionModel:
    """Offline fake model used to test the Agent control plane."""

    name = "deterministic-fake-model"

    def decide(self, stage: str, observation: dict[str, object]) -> Decision:
        if stage == "intake" and not observation["has_query"]:
            return Decision("reject")
        if stage in {"score", "aggregate"} and observation["evidence_count"] == 0:
            return Decision("finish")
        decisions = {
            "intake": Decision("validate_query"),
            "retrieve": Decision("call_tool", "retrieve_reviews"),
            "score": Decision("validate_scores"),
            "aggregate": Decision("call_tool", "aggregate_scores"),
            "finalize": Decision("finish"),
        }
        if stage not in decisions:
            raise ValueError(f"no decision for stage: {stage}")
        return decisions[stage]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools))

    def register(self, spec: ToolSpec) -> None:
        if spec.name in self._tools:
            raise ValueError(f"duplicate tool: {spec.name}")
        self._tools[spec.name] = spec

    def call(self, name: str, **kwargs: object) -> object:
        if name not in self._tools:
            raise KeyError(f"unregistered tool: {name}")
        spec = self._tools[name]
        required, provided = set(spec.required_args), set(kwargs)
        if required != provided:
            raise ValueError(f"{name} expects {sorted(required)}, received {sorted(provided)}")
        return spec.handler(**kwargs)


def _retrieve_tool(reviews: list[Review], restaurant: str) -> list[Review]:
    return select_reviews(reviews, restaurant)


def _aggregate_tool(scores: list[float]) -> float | None:
    synthetic = [Review("selected", "content intentionally excluded", score) for score in scores]
    return aggregate_score(synthetic)


@dataclass
class AgentState:
    trace_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    query: str = ""
    stage: str = "intake"
    step: int = 0
    status: str = "idle"
    evidence_ids: list[str] = field(default_factory=list)
    evidence_scores: list[float] = field(default_factory=list)
    score: float | None = None
    retries: dict[str, int] = field(default_factory=dict)
    messages: list[Message] = field(default_factory=list)
    trace: list[TraceEvent] = field(default_factory=list)


class TransientStageError(RuntimeError):
    """Explicitly retryable stage failure used by adapters and fault tests."""


class ReviewAgentPipeline:
    """A bounded, inspectable multi-role Agent pipeline.

    Review text is untrusted evidence. The runtime never parses it as an action,
    stores it in long-term memory, or copies it into tool arguments.
    """

    def __init__(
        self,
        reviews: list[Review],
        definition: PipelineDefinition | None = None,
        max_steps: int = 10,
        retry_limit: int = 1,
        model: DecisionModel | None = None,
    ) -> None:
        self.reviews = reviews
        self.definition = definition or PipelineDefinition()
        self.definition.validate()
        if max_steps < len(REQUIRED_STAGES):
            raise ValueError("max_steps is too small for the required pipeline")
        self.max_steps = max_steps
        self.retry_limit = retry_limit
        self.model = model or DeterministicDecisionModel()
        self.registry = ToolRegistry()
        self.registry.register(ToolSpec("retrieve_reviews", ("reviews", "restaurant"), _retrieve_tool))
        self.registry.register(ToolSpec("aggregate_scores", ("scores",), _aggregate_tool))
        self.state = AgentState()
        self._step_started = time.perf_counter()

    def _event(
        self,
        actor: str,
        action: str,
        outcome: str,
        tool: str | None = None,
        policy_decision: str = "allow",
    ) -> None:
        self.state.trace.append(
            TraceEvent(
                self.state.trace_id,
                self.state.step,
                self.state.stage,
                actor,
                action,
                outcome,
                tool,
                round((time.perf_counter() - self._step_started) * 1000, 3),
                0.0,
                self.state.retries.get(self.state.stage, 0),
                policy_decision,
            )
        )

    def _handoff(self, sender: str, recipient: str, artifact: str) -> None:
        self.state.messages.append(Message(sender, recipient, "handoff", {"artifact": artifact, "stage": self.state.stage}))

    def _advance(self) -> None:
        current_index = self.definition.stages.index(self.state.stage)
        if current_index + 1 >= len(self.definition.stages):
            self.state.status = "completed"
            self.state.stage = "done"
        else:
            self.state.stage = self.definition.stages[current_index + 1]

    def _execute_stage(self) -> None:
        state = self.state
        observation = {
            "has_query": bool(state.query.strip()),
            "evidence_count": len(state.evidence_ids),
            "has_score": state.score is not None,
        }
        decision = self.model.decide(state.stage, observation)
        allowed_actions = {
            "intake": "validate_query",
            "retrieve": "call_tool",
            "score": "validate_scores",
            "aggregate": "call_tool",
            "finalize": "finish",
        }
        if decision.action != allowed_actions.get(state.stage):
            raise ValueError(f"action {decision.action} is not allowed in stage {state.stage}")

        if state.stage == "intake":
            if not state.query.strip():
                raise ValueError("restaurant query cannot be empty")
            self._handoff("coordinator", "retriever", "normalized_query")
            self._event("coordinator", "validate_query", "ok")
            self._advance()
            return

        if state.stage == "retrieve":
            if decision.tool is None:
                raise ValueError("retrieve decision requires a tool")
            selected = self.registry.call(decision.tool, reviews=self.reviews, restaurant=state.query)
            assert isinstance(selected, list)
            # Durable memory keeps identifiers and numeric evidence only, never review instructions.
            state.evidence_ids = [f"review-{self.reviews.index(review)}" for review in selected]
            state.evidence_scores = [review.score for review in selected]
            self._handoff("retriever", "scorer", "evidence_ids")
            self._event(self.model.name, "retrieve", f"{len(selected)} evidence items", decision.tool)
            if not selected:
                state.status = "no_evidence"
                state.stage = "done"
            else:
                self._advance()
            return

        if state.stage == "score":
            if any(not 1.0 <= score <= 5.0 for score in state.evidence_scores):
                raise ValueError("score outside [1, 5]")
            self._handoff("scorer", "aggregator", "validated_scores")
            self._event("scorer", "validate_scores", "ok")
            self._advance()
            return

        if state.stage == "aggregate":
            if decision.tool is None:
                raise ValueError("aggregate decision requires a tool")
            state.score = self.registry.call(decision.tool, scores=state.evidence_scores)
            self._handoff("aggregator", "coordinator", "aggregate_result")
            self._event(self.model.name, "aggregate", "ok", decision.tool)
            self._advance()
            return

        if state.stage == "finalize":
            self._event("coordinator", "finalize", "ok")
            self._advance()
            return

        raise ValueError(f"unknown stage: {state.stage}")

    def run(
        self,
        query: str | None = None,
        *,
        fault_budget: dict[str, int] | None = None,
        stop_after_steps: int | None = None,
        checkpoint_path: Path | None = None,
    ) -> dict[str, object]:
        if query is not None:
            if self.state.status not in {"idle", "paused"}:
                raise RuntimeError("cannot replace query after execution")
            self.state.query = query
        if not self.state.query:
            raise ValueError("query is required")
        self.state.status = "running"
        faults = fault_budget if fault_budget is not None else {}

        while self.state.status == "running" and self.state.step < self.max_steps:
            if stop_after_steps is not None and self.state.step >= stop_after_steps:
                self.state.status = "paused"
                break
            self.state.step += 1
            self._step_started = time.perf_counter()
            try:
                remaining_faults = faults.get(self.state.stage, 0)
                if remaining_faults > 0:
                    faults[self.state.stage] = remaining_faults - 1
                    raise TransientStageError(f"injected {self.state.stage} failure")
                self._execute_stage()
            except Exception as error:
                retries = self.state.retries.get(self.state.stage, 0) + 1
                self.state.retries[self.state.stage] = retries
                retryable = isinstance(error, (TransientStageError, TimeoutError, ConnectionError))
                self._event(
                    "runtime",
                    "stage_error",
                    type(error).__name__,
                    policy_decision="retry" if retryable and retries <= self.retry_limit else "fail_closed",
                )
                if not retryable or retries > self.retry_limit:
                    self.state.status = "failed"
                    self.state.stage = "done"
            if checkpoint_path is not None:
                self.save_checkpoint(checkpoint_path)

        if self.state.status == "running":
            self.state.status = "failed_budget"
            self._event("runtime", "step_budget", "exhausted")
        if checkpoint_path is not None:
            self.save_checkpoint(checkpoint_path)
        return self.result()

    def result(self) -> dict[str, object]:
        return {
            "query": self.state.query,
            "status": self.state.status,
            "score": self.state.score,
            "evidence_ids": list(self.state.evidence_ids),
            "steps": self.state.step,
            "messages": [asdict(message) for message in self.state.messages],
            "trace": [asdict(event) for event in self.state.trace],
        }

    def save_checkpoint(self, path: Path) -> None:
        state_payload = asdict(self.state)
        canonical = json.dumps(state_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        envelope = {
            "schema_version": 1,
            "sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
            "state": state_payload,
        }
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)

    @classmethod
    def from_checkpoint(cls, path: Path, reviews: list[Review], **kwargs: object) -> "ReviewAgentPipeline":
        envelope = json.loads(path.read_text(encoding="utf-8"))
        if envelope.get("schema_version") != 1:
            raise ValueError("unsupported checkpoint schema version")
        payload = envelope["state"]
        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        expected = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        if envelope.get("sha256") != expected:
            raise ValueError("checkpoint integrity check failed")
        runtime = cls(reviews, **kwargs)
        payload["messages"] = [Message(**message) for message in payload["messages"]]
        payload["trace"] = [TraceEvent(**event) for event in payload["trace"]]
        runtime.state = AgentState(**payload)
        if runtime.state.status == "paused":
            runtime.state.status = "running"
        return runtime


class SafeWorkspace:
    """Path-confined text workspace for Agent file tools."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def resolve(self, relative: str) -> Path:
        candidate = (self.root / relative).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise PermissionError("path escapes sandbox root")
        return candidate

    def read_text(self, relative: str) -> str:
        return self.resolve(relative).read_text(encoding="utf-8")

    def write_text(self, relative: str, content: str, *, approved: bool = False) -> None:
        if not approved:
            raise PermissionError("write requires explicit approval")
        target = self.resolve(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


class ApprovalGate:
    def __init__(self) -> None:
        self._requests: dict[str, dict[str, str]] = {}

    def request(self, action: str, resource: str) -> str:
        request_id = f"approval-{uuid.uuid4().hex}"
        self._requests[request_id] = {"status": "pending", "action": action, "resource": resource}
        return request_id

    def approve(self, request_id: str) -> None:
        request = self._requests.get(request_id)
        if request is None or request["status"] != "pending":
            raise KeyError("unknown approval request")
        request["status"] = "approved"

    def consume(self, request_id: str, action: str, resource: str) -> None:
        request = self._requests.get(request_id)
        if request is None or request["status"] != "approved":
            raise PermissionError("action is not approved")
        if request["action"] != action or request["resource"] != resource:
            raise PermissionError("approval does not match action and resource")
        request["status"] = "consumed"


class BrowserTool:
    """Allowlisted HTTPS browser boundary with injected transport for tests."""

    def __init__(self, allowed_hosts: set[str], transport: Callable[[str], str] | None = None) -> None:
        self.allowed_hosts = {host.casefold() for host in allowed_hosts}
        self.transport = transport or self._default_transport

    @staticmethod
    def _default_transport(url: str) -> str:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read().decode("utf-8", errors="replace")

    def get(self, url: str) -> str:
        parsed = urlparse(url)
        if parsed.scheme != "https" or (parsed.hostname or "").casefold() not in self.allowed_hosts:
            raise PermissionError("browser URL is outside the HTTPS allowlist")
        return self.transport(url)

    def submit(self, url: str, approval_gate: ApprovalGate, request_id: str) -> str:
        approval_gate.consume(request_id, "browser_submit", url)
        return self.get(url)
