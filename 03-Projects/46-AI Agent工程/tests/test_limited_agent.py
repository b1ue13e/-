import unittest

from scripts.limited_agent import AgentStatus, LimitedAgentLoop, ToolSchema, get_temperature

class TestLimitedAgentLoop(unittest.TestCase):
    def setUp(self):
        self.agent = LimitedAgentLoop(max_steps=3)
        self.agent.register_tool(ToolSchema(
            name="get_temperature",
            description="获取城市温度",
            func=get_temperature,
            permission="READ_ONLY",
            argument_types={"city": str},
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

    def test_non_mapping_action_and_wrong_argument_type_fail_closed(self):
        self.assertEqual(
            self.agent.run("坏动作", lambda step, traces: None)["status"],
            AgentStatus.INVALID_ARGUMENT,
        )
        self.assertEqual(
            self.agent.run(
                "坏参数",
                lambda step, traces: {"tool": "get_temperature", "args": {"city": 7}},
            )["status"],
            AgentStatus.INVALID_ARGUMENT,
        )

    def test_duplicate_tool_registration_is_rejected(self):
        with self.assertRaises(ValueError):
            self.agent.register_tool(
                ToolSchema("get_temperature", "duplicate", get_temperature)
            )

if __name__ == "__main__":
    unittest.main()
