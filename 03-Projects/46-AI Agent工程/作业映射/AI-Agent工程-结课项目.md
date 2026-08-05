---
type: project
topic: "AI Agent工程结课项目"
created: 2026-08-05
status: active
progress: 0%
tags: [项目, 46-AI Agent工程, 结课项目]
flow: project
kind: moc
source: "Original capstone aligned with Berkeley CS 194/294-196, Microsoft AI Agents for Beginners, Datawhale Hello-Agents, and Stanford CS224V learning objectives"
---

# AI Agent 工程结课项目

> 这是本课程原创项目，不是 Berkeley、Microsoft、Datawhale 或 Stanford 官方作业。目标是交付一个有真实工具但受限、可测试、可观察、可暂停和可恢复的垂直 Agent。

## 可运行 starter

从 `03-Projects/46-AI Agent工程/local-acceptance/agent_runtime.py` 开始，而不是空白搭建。该 starter 已实现工具注册、typed handoff、状态机、有限重试/终止、证据 ID 记忆、trace、JSON checkpoint、路径沙箱、HTTPS host allowlist 与审批门；`test_local_acceptance.py` 给出正常、异常、恶意证据、故障注入与恢复基线。

第一步先运行 `python -m unittest -v`。迁移项目必须替换餐厅领域工具与数据，同时保留契约/边界测试；仅改名称或 Prompt 不算迁移完成。

## 最小范围

选择“研究资料整理、只读运维诊断、课程资料问答”之一。必须有：1 个模型接口、2–3 个工具、显式状态机、引用证据、至少 1 个高风险动作的模拟审批。

## 里程碑与知识映射

| 里程碑 | 交付物 | 对应笔记 | Gate |
| :--- | :--- | :--- | :--- |
| M0 任务边界 | 非 Agent 基线、成功/失败定义 | [[AI-Agent-边界与感知行动循环]] | 说明为何需要 Agent |
| M1 契约与测试 | JSON schema、fake model/tool、本地回归测试 | [[AI-Agent-前置-消息JSON异常与单元测试]]、[[AI-Agent-工具调用与结构化契约]] | 离线全绿 |
| M2 编排 | 状态机、终止、预算、错误分支 | [[AI-Agent-规划状态与工作流编排]] | 无无限循环 |
| M3 上下文与证据 | 预算、信任分区、引用、记忆策略 | [[AI-Agent-上下文工程-选择压缩隔离]]、[[AI-Agent-记忆与检索增强生成]] | 来源可定位、注入不提权 |
| M4 校验与协作 | Reflection 停止、消息协议、协议边界 | [[AI-Agent-反思与元认知-校验修正停止]]、[[AI-Agent-多智能体协作与消息协议]]、[[AI-Agent-协议-MCP与A2A互操作]] | 无进展能停止或升级 |
| M5 安全 | 威胁模型、沙箱、审批、红队 | [[AI-Agent-环境交互-代码网页与沙箱执行]]、[[AI-Agent-安全威胁建模与系统评测]] | 安全维度不得为 0 |
| M6 评测与运行 | 四层评测、trace、幂等、恢复演练 | [[AI-Agent-评测与基准-任务轨迹成本]]、[[AI-Agent-可观测性与生产运行-轨迹审批恢复]] | 故障可定位与恢复 |

## 测试矩阵

- 正常任务 ≥20；异常输入 ≥10；对抗输入 ≥10。
- 报告端到端成功率、误拒率、越权动作率、平均步数、P95 延迟、token/费用和人工接管率。
- 做三项消融：无规划、无检索或无防护中的至少两项；解释变化而不只报数字。

## 10 分量规

| 维度 | 2 分标准 |
| :--- | :--- |
| 边界 | 状态、工具、权限、成功/停止条件明确 |
| 正确性 | 正常/异常/对抗测试齐全且逐样本可查 |
| 可观察 | trace 能定位到模型/工具/编排/数据/权限层 |
| 安全 | 最小权限、沙箱、审批、敏感信息去除 |
| 恢复 | 超时、有限重试、幂等、检查点与回滚演练 |

总分 ≥8/10 且安全维度 =2 才结课。

## 端到端验收命令

```powershell
cd "F:\-\03-Projects\46-AI Agent工程\local-acceptance"
python -m unittest -v
```

迁移后的测试必须额外覆盖：新工具 schema、未知实体、超时/重试、恶意检索内容、越界文件路径、未审批高风险动作、checkpoint 恢复和去敏 trace。真实模型集成另设测试层；离线全绿不代表 `initiate_chat` 或外部 API 已验证。
