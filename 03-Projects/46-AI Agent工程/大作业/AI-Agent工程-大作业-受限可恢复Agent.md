---
type: project
project_type: homework
topic: "受限可恢复Agent"
course: "AI Agent工程"
assignment_id: "AI-Agent工程-CAPSTONE"
assignment_level: capstone
assignment_format: project
stage_id: "06"
requires: ["[[AI-Agent-边界与感知行动循环]]", "[[AI-Agent-工具调用与结构化契约]]", "[[AI-Agent-规划状态与工作流编排]]", "[[AI-Agent-上下文工程-选择压缩隔离]]", "[[AI-Agent-记忆与检索增强生成]]", "[[AI-Agent-反思与元认知-校验修正停止]]", "[[AI-Agent-多智能体协作与消息协议]]", "[[AI-Agent-协议-MCP与A2A互操作]]", "[[AI-Agent-安全威胁建模与系统评测]]", "[[AI-Agent-环境交互-代码网页与沙箱执行]]", "[[AI-Agent-评测与基准-任务轨迹成本]]", "[[AI-Agent-可观测性与生产运行-轨迹审批恢复]]", "[[AI-Agent-部署与本地运行-伸缩路由烟测]]", "[[AI-Agent-安全审计-加密收据与审批绑定]]"]
source_type: local_integration_task
source: "课程原创大作业；融合 Microsoft AI Agents for Beginners、Datawhale Hello-Agents、Berkeley/Stanford公开能力目标"
source_url: "https://github.com/microsoft/ai-agents-for-beginners"
accessed: 2026-08-06
license: "任务文本原创；引用来源按教材挂载索引；不冒充任何学校官方作业"
created: 2026-08-06
status: planned
flow: project
tags: [作业, 大作业, 46-AI Agent工程, Agent系统]
---

# AI Agent 工程大作业：受限、可观察、可恢复 Agent

## 作业身份与学习目标

这是课程原创 `local_integration_task`。交付一个真实垂直任务的 Agent，证明它不仅能给出答案，还能在权限、错误、攻击和中断下安全停止或恢复。

完成后应能：定义 Agent 边界；实现模型/工具/状态/终止；管理上下文与证据；约束环境动作；以逐样本指标和 trace 证明行为；完成部署烟测与审批审计。

## 任务背景与范围

从以下之一选择并迁移，不得只改变量名或 Prompt：

1. **研究资料整理**：只读检索本地资料并生成带引用报告。
2. **只读运维诊断**：读取静态日志/指标，给出诊断与待审批处置建议。
3. **课程资料助手**：回答课程问题并生成学习计划，写入动作必须审批。

最小范围：1 个可替换模型接口、2–3 个窄职责工具、显式状态机、证据 ID、至少一个模拟高风险动作、checkpoint、trace 和离线 eval。不得接真实支付、生产发布或未经授权目标。

## 里程碑

### M0 任务规格与非 Agent 基线

- 写用户、环境、状态、动作、成功/失败/停止、成本和权限边界。
- 建一个固定工作流或检索基线，说明 Agent 的必要性。

### M1 契约与离线测试

- 模型 adapter、工具 registry、schema、结构化错误和 fake model/tool。
- 正常、空输入、畸形输入、未知工具、超时均有测试。

### M2 编排、上下文与记忆

- 状态机/DAG、预算、有限重试、幂等 request ID、checkpoint。
- 上下文有规则/状态/证据/不可信区；每条事实可回溯 source ID；记忆可过期和删除。

### M3 校验、协作与协议边界

- 确定性验证器优先，最多两轮修正，无进展升级。
- 多角色只有在带来可测收益时启用；消息含 sender/recipient/task/artifact。
- 工具接入与远程任务委托分开建模，不把本地模拟写成规范兼容声明。

### M4 安全与环境交互

- 威胁模型、路径沙箱、HTTPS allowlist、工具 ACL、敏感信息去除。
- 高风险动作绑定 action digest、approval digest、nonce 和过期时间；未审批、篡改和重放失败关闭。

### M5 评测、恢复与部署门

- 至少 20 正常、10 异常、10 对抗样本；逐样本可查。
- 报告 TSR、ToolAcc、ASR、FRR、平均/P95 步数或延迟、成本代理和人工接管率。
- 中断恢复与不中断结果等价；smoke/readiness/offline eval/canary gate 分开。

## 环境与复现

- 起点：`scripts/agent_runtime.py` 与 `tests/test_local_acceptance.py`；迁移后保留契约/边界测试语义。
- Python 3.11+；先用标准库与静态数据；真实模型集成是额外层，必须记录模型、参数、依赖、密钥配置方式、费用和访问日期。
- 建议结构：`README.md`、`requirements.txt`、`src/`、`tests/`、`data/`、`runs/`、`report.md`。
- 固定随机种子；报告硬件和预计运行时间；提交中不含密钥、个人数据或未去敏完整轨迹。

## 提交产物

1. 需求与威胁模型。
2. 源码、依赖锁定、数据说明与一键离线测试命令。
3. 正常/异常/对抗 eval 集及逐样本结果。
4. 状态图、权限图、两条代表性 trace、checkpoint 恢复证据。
5. 指标报告、失败分类、两项消融（无规划/无检索/无防护至少二选二）与已知限制。
6. 5–8 分钟演示或等价截图/终端记录；不得伪造运行结果。

## 验收标准与 Rubric

| 维度 | 分值 | 通过标准 |
| :--- | ---: | :--- |
| 边界与产品价值 | 15 | 用户结果、非 Agent 基线、权限与停止清楚 |
| 契约与正确性 | 15 | 工具真实执行，正常/异常测试逐项可查 |
| 状态、上下文与恢复 | 15 | 有预算、证据、幂等、checkpoint 与恢复等价 |
| 安全与审批 | 20 | 最小权限、沙箱、HITL、篡改/重放失败关闭 |
| 评测与可观测 | 20 | 四层指标、trace、失败归因、对抗切片完整 |
| 复现与解释 | 15 | 环境、命令、版本、成本、限制与消融齐全 |

总分 ≥85，且“安全与审批”必须 20/20；以下任一项直接不通过：越权真实动作、无来源事实、无限循环、伪造测试/API 结果、只有 UI/Prompt 无可执行逻辑、仅改名称未迁移。

## 引导与检查点

- **检查点 1**：先让 fake model/tool 全绿，再接真实模型。
- **检查点 2**：先证明正常路径，再故意注入超时、恶意证据、越界路径和中断。
- **检查点 3**：指标变化必须回到逐样本和 trace，不用平均分掩盖危险效果。
- **常见失败**：框架私有对象污染业务状态、审批未绑定参数、恢复重复副作用、引用存在但不支持、全拒绝导致虚假低 ASR。
- **提交前**：从干净目录按 README 重跑；检查无密钥；标明未验证的在线能力。

## 课程出口

通过后，将失败样本、薄弱知识和下一轮改进记录到课程审计与个人复习系统。大作业通过证明的是交付版本达到课程 Gate，不代表所有外部服务或生产环境已验证。
