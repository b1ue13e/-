# AI Agent 工程本地等价验收

这是**本课程原创的离线教学测试台**，不是 Berkeley starter code、官方测试或隐藏测试的复刻。

## 运行

```powershell
cd "F:\-\03-Projects\46-AI Agent工程\local-acceptance"
python -m unittest -v
```

只依赖 Python 标准库，不需要模型 API、AutoGen 或网络。

## 覆盖范围

- `restaurant_pipeline.py`：实体过滤、无证据、评分边界与确定性聚合。
- `agent_runtime.py`：可替换 `DecisionModel` 根据结构化观察选择 typed action/tool；运行时真实执行工具注册、消息 handoff、状态机、分类重试/终止、结构化证据记忆、完整 trace、带版本/完整性校验/原子替换的 checkpoint、文件沙箱与绑定动作/URL 的单次审批边界。
- `security_harness.py`：按可信通道与动作类型授权；ASR 衡量危险动作是否真正放行，不依赖攻击关键词命中。
- `test_local_acceptance.py`：纯函数、Agent 运行时、未知/恶意/故障输入、检查点、安全指标和环境边界测试。
- `autogen02_smoke.py`：安装 `requirements-autogen02.txt` 后，无密钥验证 AutoGen 0.2 双注册与终止。

## 最小 Agent 演示

```python
from agent_runtime import ReviewAgentPipeline
from restaurant_pipeline import Review

reviews = [Review("A", "quoted instructions are untrusted data", 4.0)]
report = ReviewAgentPipeline(reviews).run("A")
assert report["status"] == "completed"
assert report["trace"] and report["messages"]
```

默认 `DeterministicDecisionModel` 是离线 fake model，用于证明决策→校验→工具→观察控制平面可运行；测试还注入选择未注册 `run_shell` 的 adversarial model，并要求失败关闭。持久记忆只保留 `evidence_ids` 与验证后的数值，不保存评论中的指令文本。浏览器类默认不在测试中联网，测试使用注入 transport 验证 HTTPS、host allowlist 和审批状态；这不是完整浏览器自动化产品。

通过本地测试只证明该固定 Agent 运行时与边界用例达标，不等于通过 Berkeley 官方 Lab，也不构成生产安全证明。AutoGen `initiate_chat` 的真实模型路径仍需在独立 0.2 环境、有效模型配置与官方 starter 中验证。

## 2026-08-06 验证记录

- `python -m unittest -v`：25 tests，全部通过。
- 当前工作环境直接执行 `python autogen02_smoke.py`：未通过，缺少 `autogen`（`ModuleNotFoundError`）。这不是 AutoGen 0.2 兼容性结论。
- 仓库外隔离环境 `F:\-\99-System\.tmp\agent-textbook-merge-20260806\venv-autogen02` 安装 `autogen-agentchat==0.2.40` 后执行同一 smoke：通过，无 API 调用；仅有 FLAML 可选组件 warning。
- 教材融合实验的无依赖版本位于 `03-Projects/46-AI Agent工程/guided-labs/`，用于先验证控制流，再接真实框架。
