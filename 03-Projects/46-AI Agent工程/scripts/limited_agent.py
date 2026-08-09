"""
AI Agent工程 L02: 受限循环与工具契约核心实现
"""
from dataclasses import dataclass, field
from typing import Any, Callable
import json

class AgentStatus:
    SUCCESS = "SUCCESS"
    UNKNOWN_TOOL = "UNKNOWN_TOOL"
    REPEATED_ACTION_STOP = "REPEATED_ACTION_STOP"
    INVALID_ARGUMENT = "INVALID_ARGUMENT"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    PERMISSION_DENIED = "PERMISSION_DENIED"

@dataclass
class ToolSchema:
    name: str
    description: str
    func: Callable
    permission: str = "READ_ONLY"
    argument_types: dict[str, type] = field(default_factory=dict)

@dataclass
class AgentStepTrace:
    step: int
    tool_name: str
    args: dict[str, Any]
    observation: Any
    status: str

class LimitedAgentLoop:
    def __init__(self, max_steps: int = 3):
        if max_steps <= 0:
            raise ValueError("max_steps must be positive")
        self.max_steps = max_steps
        self.tools: dict[str, ToolSchema] = {}

    def register_tool(self, tool: ToolSchema) -> None:
        if tool.name in self.tools:
            raise ValueError(f"duplicate tool: {tool.name}")
        self.tools[tool.name] = tool

    def run(self, goal: str, action_provider: Callable[[int, list[AgentStepTrace]], dict[str, Any]]) -> dict[str, Any]:
        if not isinstance(goal, str) or not goal.strip():
            raise ValueError("goal must be a non-empty string")
        traces: list[AgentStepTrace] = []
        previous_action: tuple[str, str] | None = None

        for step_idx in range(1, self.max_steps + 1):
            action_req = action_provider(step_idx, traces)
            if not isinstance(action_req, dict):
                return {"status": AgentStatus.INVALID_ARGUMENT, "traces": traces, "result": None}
            tool_name = action_req.get("tool")
            args = action_req.get("args", {})
            if not isinstance(args, dict):
                trace = AgentStepTrace(step_idx, str(tool_name), {}, None, AgentStatus.INVALID_ARGUMENT)
                traces.append(trace)
                return {"status": AgentStatus.INVALID_ARGUMENT, "traces": traces, "result": None}

            # 1. 检查未知工具
            if tool_name not in self.tools:
                trace = AgentStepTrace(step_idx, str(tool_name), args, None, AgentStatus.UNKNOWN_TOOL)
                traces.append(trace)
                return {"status": AgentStatus.UNKNOWN_TOOL, "traces": traces, "result": None}

            tool_schema = self.tools[tool_name]

            # 2. 检查权限
            if tool_schema.permission != "READ_ONLY":
                trace = AgentStepTrace(step_idx, tool_name, args, None, AgentStatus.PERMISSION_DENIED)
                traces.append(trace)
                return {"status": AgentStatus.PERMISSION_DENIED, "traces": traces, "result": None}

            # 3. 检查重复动作
            try:
                action_key = (tool_name, json.dumps(args, sort_keys=True))
            except (TypeError, ValueError):
                trace = AgentStepTrace(step_idx, tool_name, args, None, AgentStatus.INVALID_ARGUMENT)
                traces.append(trace)
                return {"status": AgentStatus.INVALID_ARGUMENT, "traces": traces, "result": None}
            if action_key == previous_action:
                trace = AgentStepTrace(step_idx, tool_name, args, None, AgentStatus.REPEATED_ACTION_STOP)
                traces.append(trace)
                return {"status": AgentStatus.REPEATED_ACTION_STOP, "traces": traces, "result": None}
            previous_action = action_key

            for argument, expected_type in tool_schema.argument_types.items():
                if argument not in args or not isinstance(args[argument], expected_type):
                    trace = AgentStepTrace(step_idx, tool_name, args, None, AgentStatus.INVALID_ARGUMENT)
                    traces.append(trace)
                    return {"status": AgentStatus.INVALID_ARGUMENT, "traces": traces, "result": None}

            # 4. 执行工具
            try:
                obs = tool_schema.func(**args)
            except Exception as e:
                trace = AgentStepTrace(step_idx, tool_name, args, str(e), AgentStatus.INVALID_ARGUMENT)
                traces.append(trace)
                return {"status": AgentStatus.INVALID_ARGUMENT, "traces": traces, "result": None}

            trace = AgentStepTrace(step_idx, tool_name, args, obs, AgentStatus.SUCCESS)
            traces.append(trace)

            if isinstance(obs, dict) and obs.get("is_final", False):
                return {"status": AgentStatus.SUCCESS, "traces": traces, "result": obs.get("result")}

        return {"status": AgentStatus.BUDGET_EXHAUSTED, "traces": traces, "result": None}


def get_temperature(city: str) -> dict[str, Any]:
    db = {
        "Beijing": {"city": "Beijing", "temp_c": 20.0, "status": "SUCCESS"},
        "Shanghai": {"city": "Shanghai", "temp_c": 24.0, "status": "SUCCESS"},
        "Guangzhou": {"city": "Guangzhou", "temp_c": 28.0, "status": "SUCCESS"},
    }
    if city not in db:
        raise ValueError(f"UNKNOWN_CITY: {city}")
    return db[city]
