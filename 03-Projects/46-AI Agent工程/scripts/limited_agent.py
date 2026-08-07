"""
AI Agent工程 L02: 受限循环与工具契约核心实现
"""
from dataclasses import dataclass, field
from typing import Callable, Any, Dict, List, Optional
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

@dataclass
class AgentStepTrace:
    step: int
    tool_name: str
    args: Dict[str, Any]
    observation: Any
    status: str

class LimitedAgentLoop:
    def __init__(self, max_steps: int = 3):
        self.max_steps = max_steps
        self.tools: Dict[str, ToolSchema] = {}

    def register_tool(self, tool: ToolSchema) -> None:
        self.tools[tool.name] = tool

    def run(self, goal: str, action_provider: Callable[[int, List[AgentStepTrace]], Dict[str, Any]]) -> Dict[str, Any]:
        traces: List[AgentStepTrace] = []
        seen_actions = set()

        for step_idx in range(1, self.max_steps + 1):
            action_req = action_provider(step_idx, traces)
            tool_name = action_req.get("tool")
            args = action_req.get("args", {})

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
            action_key = (tool_name, json.dumps(args, sort_keys=True))
            if action_key in seen_actions:
                trace = AgentStepTrace(step_idx, tool_name, args, None, AgentStatus.REPEATED_ACTION_STOP)
                traces.append(trace)
                return {"status": AgentStatus.REPEATED_ACTION_STOP, "traces": traces, "result": None}
            seen_actions.add(action_key)

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


def get_temperature(city: str) -> Dict[str, Any]:
    db = {
        "Beijing": {"city": "Beijing", "temp_c": 20.0, "status": "SUCCESS"},
        "Shanghai": {"city": "Shanghai", "temp_c": 24.0, "status": "SUCCESS"},
        "Guangzhou": {"city": "Guangzhou", "temp_c": 28.0, "status": "SUCCESS"},
    }
    if city not in db:
        raise ValueError(f"UNKNOWN_CITY: {city}")
    return db[city]
