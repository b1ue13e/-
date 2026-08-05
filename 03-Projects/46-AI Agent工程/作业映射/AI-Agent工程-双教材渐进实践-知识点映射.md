---
type: project
topic: "AI Agent工程双教材渐进实践映射"
created: 2026-08-06
status: active
progress: 0%
tags: [项目, 46-AI Agent工程, 教材融合, 作业映射]
flow: project
kind: moc
source: "Original exercises aligned to Microsoft AI Agents for Beginners and Datawhale Hello-Agents; not official assignments"
---

# AI Agent 工程：双教材渐进实践知识点映射

> [!warning] 来源边界
> 以下均为本库原创练习，不是 Microsoft、Datawhale 或 Berkeley 官方作业，也不复制其答案。练习吸收两教材的能力目标，并复用本库可运行的 `local-acceptance/` 作为脚手架。

## 1. 共同规则

每项练习依次完成五步：

1. **预测**：运行前写下预期状态、输出和失败点。
2. **手算**：用一个小输入手工走完状态/预算/指标。
3. **运行**：执行标准库微型代码或 `local-acceptance/` 测试。
4. **故障注入**：至少破坏一个参数、证据、工具、权限或终止条件。
5. **迁移**：换领域/工具，不能只改变量名或 Prompt。

每项保留：任务规格、代码/配置、测试输出、失败轨迹、修复说明、一次闭卷复述。

## 2. 练习总表

| 编号 | 原创练习 | 对应知识点 | 两教材来源定位 | 难度 | 验收 |
| :--- | :--- | :--- | :--- | :---: | :--- |
| P0 | 消息与工具契约 kata | [[AI-Agent-前置-消息JSON异常与单元测试]]、[[AI-Agent-工具调用与结构化契约]] | MS 01/04；Hello 1/7 | ⭐ | 未知工具、非法参数失败关闭 |
| P1 | 有限 ReAct 天气台 | [[AI-Agent-边界与感知行动循环]]、[[AI-Agent-ReAct推理行动范式]] | MS 01/03；Hello 4 | ⭐⭐ | 最多 3 步，有观察、有停止理由 |
| P2 | 状态机与框架替换 | [[AI-Agent-规划状态与工作流编排]]、[[AI-Agent-框架选型与最小运行时]] | MS 02/07/14；Hello 5-7 | ⭐⭐ | fake runtime 与框架适配测试分层 |
| P3 | 上下文预算与污染防护 | [[AI-Agent-上下文工程-选择压缩隔离]]、[[AI-Agent-记忆与检索增强生成]] | MS 05/12/13；Hello 8/9 | ⭐⭐⭐ | 必选规则保留，注入不改变权限 |
| P4 | 反思式证据报告 | [[AI-Agent-反思与元认知-校验修正停止]] | MS 09；Hello 4.4 | ⭐⭐⭐ | 确定性验证优先，2 轮内通过或升级 |
| P5 | MCP/A2A 边界模拟 | [[AI-Agent-协议-MCP与A2A互操作]]、[[AI-Agent-多智能体协作与消息协议]] | MS 08/11；Hello 10 | ⭐⭐⭐ | tool 与 remote task 生命周期分离 |
| P6 | 四层评测包 | [[AI-Agent-评测与基准-任务轨迹成本]]、[[AI-Agent-安全威胁建模与系统评测]] | MS 06/10；Hello 12 | ⭐⭐⭐ | 任务/轨迹/安全/成本均有指标 |
| P7A | 受限旅行助手迁移 | [[AI-Agent工程-结课项目]]、`guided-labs/curriculum_labs.py::plan_trip` | MS 03/08/11；Hello 13 | ⭐⭐⭐ | 预算、证据、审批 digest、幂等与失败关闭 |
| P7B | 赛博小镇离线模拟 | `guided-labs/curriculum_labs.py::tick_town` | MS 08/13；Hello 15 | ⭐⭐⭐ | NPC 状态、事件转移、记忆上限可复现 |
| P7C | 受限深度研究迁移 | [[AI-Agent工程-结课项目]]、`guided-labs/curriculum_labs.py::research_report` | MS capstone guide；Hello 14/16 | ⭐⭐⭐⭐ | 引用、trace、审批、恢复、对抗测试齐全 |
| P8 | 奖励投机审计（选修） | [[AI-Agent-Agentic-RL与自改进边界]]、`guided-labs/curriculum_labs.py::reward_audit` | MS 09/13；Hello 11 | ⭐⭐⭐⭐ | 找出至少 2 条 reward hacking 路径 |

## 3. 分项任务与最小知识点

### P0 消息与工具契约 kata

**任务**：给 `calculator`、`lookup_order` 两个 fake tool 定义 JSON-like schema、权限、成功与错误返回；模型用预制决策字典替代。

**最小知识点**：
- [ ] [[AI-Agent-前置-消息JSON异常与单元测试]]
- [ ] [[AI-Agent-工具调用与结构化契约]]

**故障注入**：未知工具、缺字段、错误类型、工具超时、工具返回畸形 JSON。

**Gate**：`python -m unittest -v` 全绿；测试断言错误类别，而不只断言“抛异常”。

### P1 有限 ReAct 天气台

**任务**：用预制 observation 完成“比较两个城市温度”任务，轨迹为 Thought/Action/Observation 的可观察状态，不记录不可审计的隐藏推理文本。

**最小知识点**：
- [ ] [[AI-Agent-边界与感知行动循环]]
- [ ] [[AI-Agent-ReAct推理行动范式]]

**故障注入**：城市不存在、观察过期、模型重复调用、3 步耗尽。

**Gate**：能说明何时降级为固定工作流；步数耗尽返回明确失败，不伪造答案。

### P2 状态机与框架替换

**任务**：把 P1 改为 `validate -> fetch_a -> fetch_b -> compare -> finish`，先用本地 runtime，再写一个只负责类型转换的框架 adapter 设计。

**最小知识点**：
- [ ] [[AI-Agent-规划状态与工作流编排]]
- [ ] [[AI-Agent-框架选型与最小运行时]]

**故障注入**：重复消息、checkpoint 后恢复、旧版本 adapter 字段变化。

**Gate**：业务状态不含框架私有对象；替换 adapter 后核心测试不改。

### P3 上下文预算与污染防护

**任务**：在 800 token 预算中装配不可变规则、当前状态、两份相互冲突证据和一段不可信网页。

**最小知识点**：
- [ ] [[AI-Agent-上下文工程-选择压缩隔离]]
- [ ] [[AI-Agent-记忆与检索增强生成]]

**手算要求**：列出每项 token、可信度、来源 ID、选择/拒绝理由。

**故障注入**：间接注入、陈旧记忆、摘要漏掉否定词、必选项超预算。

**Gate**：不可信内容可作为证据但不能改变工具权限；摘要能回溯原 artifact。

### P4 反思式证据报告

**任务**：生成包含 `claim`、`source_id`、`confidence` 的 3 条事实报告；验证器检查 schema、引用存在和支持关系。

**最小知识点**：
- [ ] [[AI-Agent-反思与元认知-校验修正停止]]
- [ ] [[AI-Agent-评测与基准-任务轨迹成本]]

**故障注入**：缺引用、引用不支持、连续两轮无进展、成本预算耗尽。

**Gate**：反馈包含失败类别和证据；无法修复时升级，不生成假引用。

### P5 MCP/A2A 边界模拟

**任务**：本地 `search` 作为 MCP-like tool；远程 `writer` 作为 A2A-like Agent，返回有状态 Task 和 Artifact。先做概念模拟，再按实践时的官方规范选 SDK。

**最小知识点**：
- [ ] [[AI-Agent-协议-MCP与A2A互操作]]
- [ ] [[AI-Agent-多智能体协作与消息协议]]

**故障注入**：未声明 skill、HTTP endpoint、任务取消、伪造 artifact、server 描述注入。

**Gate**：能在图中标出 host、server、remote agent 和四个信任边界；协议字段有核验日期。

### P6 四层评测包

**任务**：为 P0-P5 选一个系统建立 20 正常、10 异常、10 对抗样本。

**最小知识点**：
- [ ] [[AI-Agent-评测与基准-任务轨迹成本]]
- [ ] [[AI-Agent-安全威胁建模与系统评测]]
- [ ] [[AI-Agent-可观测性与生产运行-轨迹审批恢复]]

**必须报告**：TSR、ToolAcc、ASR、FRR、平均/P95 步数或延迟、人工接管率、失败分类。

**Gate**：逐样本结果可查；安全出现危险效果即失败，不能被总平均掩盖。

### P7A 旅行助手迁移

**任务**：在静态航班/酒店数据上完成预算约束行程规划；预订是高风险动作，必须先生成 action digest，等待批准后才返回 booked。

**实际 starter 与反馈**：`03-Projects/46-AI Agent工程/guided-labs/curriculum_labs.py::plan_trip`，测试 `test_p7a_*`。

**故障注入**：未知目的地、超预算、未审批、重复 request ID。

**Gate**：所有未审批动作返回 `awaiting_approval`；不能接入真实支付；保留预算、证据和审批记录。

### P7B 赛博小镇离线模拟

**任务**：先用确定性状态机表示 NPC、事件、情绪和记忆上限，再设计未来接入 LLM 的接口；不以游戏画面或自由文本作为验收依据。

**实际 starter 与反馈**：`03-Projects/46-AI Agent工程/guided-labs/curriculum_labs.py::tick_town`，测试 `test_p7b_*`。

**故障注入**：未知事件、重复事件、过期记忆、越界 NPC ID。

**Gate**：相同输入可重放得到相同状态；消息、状态、隐私和失败均可测试。

### P7C 受限深度研究迁移

**任务**：从 `local-acceptance/agent_runtime.py` 迁移为课程资料研究 Agent：只读搜索本库、整理 source ID、生成带引用报告；外部网页、写文件和发布动作分别设权限。

**实际 starter 与反馈**：`03-Projects/46-AI Agent工程/guided-labs/curriculum_labs.py::research_report`，测试 `test_p7_*`；端到端迁移仍使用 `local-acceptance/` 的状态、trace 和安全边界。

**最小知识点**：P0-P6 全部。

**故障注入**：来源冲突、网页注入、越界路径、工具超时、报告生成中断、checkpoint 恢复、重复发布请求。

**Gate**：使用 [[AI-Agent工程-结课项目]] 的 10 分量规，至少 8/10，且安全维度必须 2 分。

### P8 奖励投机审计（选修）

**任务**：不训练模型；先为 P7 定义轨迹奖励，构造至少两条“总分高但行为坏”的轨迹，再修奖励和上线门。

**最小知识点**：
- [ ] [[AI-Agent-Agentic-RL与自改进边界]]
- [ ] [[AI-Agent-评测与基准-任务轨迹成本]]

**Gate**：训练集、回归集、盲测集分开；记录奖励分量；候选策略不能自动进入生产。

## 4. 渐隐支架

| 层级 | 提供什么 | 学习者必须完成什么 |
| :--- | :--- | :--- |
| Worked example | 主题卡中的完整微型代码与输出 | 预测输出、逐行解释、改一个输入 |
| Completion | 保留接口、测试和一半控制流 | 补全缺口并通过故障测试 |
| Independent | 只给任务、威胁和 Gate | 自主实现、记录取舍 |
| Transfer | 换领域、数据和工具 | 证明不是变量改名，重新做 eval |

## 5. 实际文件与预期输出

| 层级 | 文件 | 运行命令 | 预期 |
| :--- | :--- | :--- | :--- |
| Worked | `guided-labs/curriculum_labs.py` | `python curriculum_labs.py` | 输出有限循环、旅行审批和小镇状态 |
| Feedback | `guided-labs/test_curriculum_labs.py` | `python -m unittest -v` | P0–P8 的 10 个确定性测试全绿 |
| Completion | 复制单个函数到个人文件，只改一个策略点 | 运行对应 `test_p*_` | 失败类别明确，修复后输出与 Gate 一致 |
| Independent | 只保留课后习题册的任务、数据和验收 | 自己建立文件 | 不引用 worked 实现也能通过同类测试 |
| Transfer | 选择旅行/小镇/深度研究之一换领域 | 重建 eval spec | 正常/异常/对抗样本与原领域不同 |

详见：[[AI Agent 工程双教材课后习题册-Microsoft]]、[[AI Agent 工程双教材课后习题册-Hello-Agents]]、`03-Projects/46-AI Agent工程/guided-labs/README.md`。

连续两次失败只回退一层，并在学习记录写下失败类别；不要从迁移任务直接退回“重看整章”。

## 5. 学习证据索引

| 日期 | 练习 | 层级 | 测试结果 | 失败类别 | 闭卷复述 | 下一次间隔复习 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| | | | | | | |
