import unittest
import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from limited_agent import LimitedAgentLoop, ToolSchema, AgentStatus, get_temperature

class TestLimitedAgentLoop(unittest.TestCase):
    def setUp(self):
        self.agent = LimitedAgentLoop(max_steps=3)
        self.agent.register_tool(ToolSchema(
            name="get_temperature",
            description="获取城市温度",
            func=get_temperature,
            permission="READ_ONLY"
        ))

    def test_normal_execution(self):
        def mock_provider(step, traces):
            if step == 1:
                return {"tool": "get_temperature", "args": {"city": "Beijing"}}
            elif step == 2:
                return {"tool": "get_temperature", "args": {"city": "Shanghai"}}
            else:
                return {"tool": "get_temperature", "args": {"city": "Guangzhou"}}

        res = self.agent.run("比较温度", mock_provider)
        self.assertEqual(len(res["traces"]), 3)
        self.assertEqual(res["traces"][0].observation["temp_c"], 20.0)

    def test_unknown_tool_interception(self):
        def mock_provider(step, traces):
            return {"tool": "exec_shell", "args": {"cmd": "ls"}}

        res = self.agent.run("危险操作", mock_provider)
        self.assertEqual(res["status"], AgentStatus.UNKNOWN_TOOL)

    def test_repeated_action_fusion(self):
        def mock_provider(step, traces):
            return {"tool": "get_temperature", "args": {"city": "Beijing"}}

        res = self.agent.run("重复动作", mock_provider)
        self.assertEqual(res["status"], AgentStatus.REPEATED_ACTION_STOP)

    def test_invalid_argument_handling(self):
        def mock_provider(step, traces):
            return {"tool": "get_temperature", "args": {"city": "UnknownCity"}}

        res = self.agent.run("未知城市", mock_provider)
        self.assertEqual(res["status"], AgentStatus.INVALID_ARGUMENT)

if __name__ == "__main__":
    unittest.main()
