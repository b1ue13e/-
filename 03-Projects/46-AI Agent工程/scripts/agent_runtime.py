"""Deterministic Agent runtime used by the local teaching acceptance gate."""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import ipaddress
import json
import secrets
import socket
import time
import urllib.request
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Protocol
from urllib.parse import urlparse

try:
    from .restaurant_pipeline import Review, aggregate_score, select_reviews
except ImportError:  # Supports direct execution from the scripts directory.
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
    argument_types: dict[str, type] = field(default_factory=dict)
    result_validator: Callable[[object], bool] | None = None


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


class HttpDecisionModel:
    """HTTP adapter for a provider-specific decision service.

    The service must return ``{"action": str, "tool": str | null}``. This
    verifies the network and response boundary without claiming compatibility
    with a specific model provider.
    """

    def __init__(
        self,
        endpoint: str,
        *,
        api_token: str | None = None,
        timeout: float = 10.0,
        max_response_bytes: int = 65_536,
        allow_http_localhost: bool = False,
        name: str = "http-decision-model",
    ) -> None:
        parsed = urlparse(endpoint)
        local_hosts = {"localhost", "127.0.0.1", "::1"}
        secure = parsed.scheme == "https"
        local_http = (
            allow_http_localhost
            and parsed.scheme == "http"
            and (parsed.hostname or "").casefold() in local_hosts
        )
        if not parsed.hostname or not (secure or local_http):
            raise ValueError("decision endpoint must use HTTPS, except explicit localhost tests")
        if timeout <= 0 or max_response_bytes <= 0:
            raise ValueError("timeout and max_response_bytes must be positive")
        self.endpoint = endpoint
        self.api_token = api_token
        self.timeout = timeout
        self.max_response_bytes = max_response_bytes
        self.name = name

    def decide(self, stage: str, observation: dict[str, object]) -> Decision:
        payload = json.dumps(
            {"stage": stage, "observation": observation},
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        request = urllib.request.Request(self.endpoint, data=payload, headers=headers, method="POST")

        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args: object, **kwargs: object) -> None:
                return None

        opener = urllib.request.build_opener(NoRedirect)
        with opener.open(request, timeout=self.timeout) as response:
            content_type = response.headers.get_content_type()
            if content_type != "application/json":
                raise ValueError(f"decision endpoint returned {content_type}, expected application/json")
            raw = response.read(self.max_response_bytes + 1)
        if len(raw) > self.max_response_bytes:
            raise ValueError("decision response exceeded the size limit")
        body = json.loads(raw.decode("utf-8"))
        if not isinstance(body, dict) or not isinstance(body.get("action"), str):
            raise ValueError("decision response must contain a string action")
        tool = body.get("tool")
        if tool is not None and not isinstance(tool, str):
            raise ValueError("decision response tool must be a string or null")
        return Decision(body["action"], tool)


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools))

    def register(self, spec: ToolSpec) -> None:
        if spec.name in self._tools:
            raise ValueError(f"duplicate tool: {spec.name}")
        undeclared_types = set(spec.argument_types) - set(spec.required_args)
        if undeclared_types:
            raise ValueError(f"type rules reference undeclared arguments: {sorted(undeclared_types)}")
        self._tools[spec.name] = spec

    def call(self, name: str, **kwargs: object) -> object:
        if name not in self._tools:
            raise KeyError(f"unregistered tool: {name}")
        spec = self._tools[name]
        required, provided = set(spec.required_args), set(kwargs)
        if required != provided:
            raise ValueError(f"{name} expects {sorted(required)}, received {sorted(provided)}")
        for argument, expected_type in spec.argument_types.items():
            if argument in kwargs and not isinstance(kwargs[argument], expected_type):
                raise TypeError(f"{name}.{argument} must be {expected_type.__name__}")
        result = spec.handler(**kwargs)
        if spec.result_validator is not None and not spec.result_validator(result):
            raise TypeError(f"{name} returned a value outside its declared contract")
        return result


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
        self.registry.register(
            ToolSpec(
                "retrieve_reviews",
                ("reviews", "restaurant"),
                _retrieve_tool,
                {"reviews": list, "restaurant": str},
                lambda result: isinstance(result, list) and all(isinstance(item, Review) for item in result),
            )
        )
        self.registry.register(
            ToolSpec(
                "aggregate_scores",
                ("scores",),
                _aggregate_tool,
                {"scores": list},
                lambda result: result is None or isinstance(result, float),
            )
        )
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
            selected_object_ids = {id(review) for review in selected}
            state.evidence_ids = [
                f"review-{index}"
                for index, review in enumerate(self.reviews)
                if id(review) in selected_object_ids
            ]
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

    def approval_resource(self, relative: str) -> str:
        return self.resolve(relative).relative_to(self.root).as_posix()

    @staticmethod
    def approval_parameters(content: str) -> dict[str, object]:
        encoded = content.encode("utf-8")
        return {"bytes": len(encoded), "sha256": hashlib.sha256(encoded).hexdigest()}

    def write_text(
        self,
        relative: str,
        content: str,
        *,
        approval_gate: "ApprovalGate" | None = None,
        receipt: str | None = None,
    ) -> None:
        if approval_gate is None or receipt is None:
            raise PermissionError("write requires an approved receipt")
        resource = self.approval_resource(relative)
        approval_gate.consume(
            receipt,
            "workspace_write",
            resource,
            self.approval_parameters(content),
        )
        target = self.resolve(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


class ApprovalGate:
    """Issues short-lived, single-use receipts bound to complete action parameters."""

    def __init__(
        self,
        *,
        secret: bytes | None = None,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self._secret = secret or secrets.token_bytes(32)
        if len(self._secret) < 32:
            raise ValueError("approval secret must contain at least 32 bytes")
        self._clock = clock
        self._requests: dict[str, dict[str, object]] = {}
        self._consumed_nonces: set[str] = set()

    @staticmethod
    def _canonical_parameters(parameters: dict[str, object] | None) -> dict[str, object]:
        normalized = parameters or {}
        serialized = json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return json.loads(serialized)

    def _encode_receipt(self, payload: dict[str, object]) -> str:
        raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        signature = hmac.new(self._secret, raw, hashlib.sha256).digest()
        encoded_payload = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
        encoded_signature = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")
        return f"{encoded_payload}.{encoded_signature}"

    def _decode_receipt(self, receipt: str) -> dict[str, object]:
        try:
            encoded_payload, encoded_signature = receipt.split(".", 1)
            raw = base64.urlsafe_b64decode(encoded_payload + "=" * (-len(encoded_payload) % 4))
            signature = base64.urlsafe_b64decode(encoded_signature + "=" * (-len(encoded_signature) % 4))
        except (ValueError, TypeError, binascii.Error, UnicodeError, json.JSONDecodeError) as error:
            raise PermissionError("approval receipt is malformed") from error
        expected = hmac.new(self._secret, raw, hashlib.sha256).digest()
        if not hmac.compare_digest(signature, expected):
            raise PermissionError("approval receipt integrity check failed")
        payload = json.loads(raw.decode("utf-8"))
        if not isinstance(payload, dict):
            raise PermissionError("approval receipt payload is invalid")
        return payload

    def request(
        self,
        action: str,
        resource: str,
        parameters: dict[str, object] | None = None,
        *,
        expires_in: float = 300.0,
    ) -> str:
        if expires_in <= 0:
            raise ValueError("expires_in must be positive")
        request_id = f"approval-{uuid.uuid4().hex}"
        normalized = self._canonical_parameters(parameters)
        self._requests[request_id] = {
            "status": "pending",
            "action": action,
            "resource": resource,
            "parameters": normalized,
            "nonce": secrets.token_urlsafe(18),
            "issued_at": self._clock(),
            "expires_at": self._clock() + expires_in,
        }
        return request_id

    def approve(self, request_id: str) -> str:
        request = self._requests.get(request_id)
        if request is None or request["status"] != "pending":
            raise KeyError("unknown approval request")
        if self._clock() >= float(request["expires_at"]):
            request["status"] = "expired"
            raise PermissionError("approval request expired")
        request["status"] = "approved"
        payload = {"version": 1, "request_id": request_id, **request}
        payload.pop("status")
        return self._encode_receipt(payload)

    def consume(
        self,
        receipt: str,
        action: str,
        resource: str,
        parameters: dict[str, object] | None = None,
    ) -> None:
        payload = self._decode_receipt(receipt)
        request_id = payload.get("request_id")
        request = self._requests.get(str(request_id))
        if request is None or request["status"] != "approved":
            raise PermissionError("action is not approved")
        normalized = self._canonical_parameters(parameters)
        if (
            payload.get("version") != 1
            or payload.get("action") != action
            or payload.get("resource") != resource
            or payload.get("parameters") != normalized
            or request.get("action") != action
            or request.get("resource") != resource
            or request.get("parameters") != normalized
        ):
            raise PermissionError("approval does not match action and resource")
        if self._clock() >= float(payload["expires_at"]):
            request["status"] = "expired"
            raise PermissionError("approval request expired")
        nonce = str(payload.get("nonce", ""))
        if not nonce or nonce != request.get("nonce") or nonce in self._consumed_nonces:
            raise PermissionError("approval receipt was replayed or is unknown")
        self._consumed_nonces.add(nonce)
        request["status"] = "consumed"


class BrowserTool:
    """HTTPS-only, redirect-free browser boundary with bounded responses."""

    def __init__(
        self,
        allowed_hosts: set[str],
        transport: Callable[[str, str, bytes | None], str] | None = None,
        *,
        max_response_bytes: int = 1_000_000,
    ) -> None:
        if not allowed_hosts or max_response_bytes <= 0:
            raise ValueError("allowed_hosts and a positive response limit are required")
        self.allowed_hosts = {host.casefold() for host in allowed_hosts}
        self.max_response_bytes = max_response_bytes
        self._uses_default_transport = transport is None
        self.transport = transport or self._default_transport

    def _default_transport(self, method: str, url: str, body: bytes | None) -> str:
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args: object, **kwargs: object) -> None:
                return None

        request = urllib.request.Request(
            url,
            data=body if method == "POST" else None,
            headers={"Accept": "application/json, text/plain"},
            method=method,
        )
        opener = urllib.request.build_opener(NoRedirect)
        with opener.open(request, timeout=10) as response:
            content_type = response.headers.get_content_type()
            if not (content_type.startswith("text/") or content_type == "application/json"):
                raise ValueError(f"unsupported browser content type: {content_type}")
            raw = response.read(self.max_response_bytes + 1)
        if len(raw) > self.max_response_bytes:
            raise ValueError("browser response exceeded the size limit")
        return raw.decode("utf-8", errors="replace")

    def _validate_url(self, url: str) -> None:
        try:
            parsed = urlparse(url)
            port = parsed.port
        except ValueError as error:
            raise PermissionError("browser URL has an invalid authority") from error
        hostname = (parsed.hostname or "").casefold()
        if (
            parsed.scheme != "https"
            or port not in (None, 443)
            or parsed.username is not None
            or parsed.password is not None
            or hostname not in self.allowed_hosts
        ):
            raise PermissionError("browser URL is outside the HTTPS allowlist")
        if self._uses_default_transport:
            try:
                addresses = {
                    item[4][0]
                    for item in socket.getaddrinfo(hostname, 443, type=socket.SOCK_STREAM)
                }
            except OSError as error:
                raise PermissionError("browser host resolution failed") from error
            if not addresses:
                raise PermissionError("browser host did not resolve")
            for address in addresses:
                ip = ipaddress.ip_address(address)
                if not ip.is_global:
                    raise PermissionError("browser host resolves to a non-public address")

    def get(self, url: str) -> str:
        self._validate_url(url)
        return self.transport("GET", url, None)

    @staticmethod
    def approval_parameters(body: bytes) -> dict[str, object]:
        return {"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}

    def submit(self, url: str, body: bytes, approval_gate: ApprovalGate, receipt: str) -> str:
        self._validate_url(url)
        approval_gate.consume(receipt, "browser_submit", url, self.approval_parameters(body))
        return self.transport("POST", url, body)
