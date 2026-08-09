# AI Agent 工程测试

从 `03-Projects/46-AI Agent工程/` 执行：

```powershell
python -m unittest discover -s tests -v
```

## 覆盖

- `test_curriculum_labs.py`：11 个形成性实验测试。
- `test_eval.py`：2 个评测数据集与 20/10/10 Gate 测试。
- `test_limited_agent.py`：6 个受限循环边界测试。
- `test_local_acceptance.py`：28 个端到端离线验收测试，含本机 HTTP decision adapter。

2026-08-08 当前验证为 47/47 通过。该结果支持本地标准库实现和本机回环 HTTP adapter；不等于 Berkeley 隐藏测试、Microsoft Foundry、真实模型、MCP/A2A 服务或生产环境已验证。
