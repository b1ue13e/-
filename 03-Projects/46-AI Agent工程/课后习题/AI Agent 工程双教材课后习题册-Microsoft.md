---
type: index
topic: "Microsoft AI Agents for Beginners 逐课习题册"
tags: [索引, 46-AI Agent工程, 课后习题, Microsoft]
created: 2026-08-06
status: active
flow: project
kind: moc
source: "Microsoft AI Agents for Beginners, commit 15ad10ca60577b75199c1ba828887ab7e66bac87, accessed 2026-08-06"
license_note: "Repository MIT; this companion is original Chinese task design and does not copy answers or hidden tests."
---

# Microsoft AI Agents for Beginners：逐课习题册

> [!warning] 使用边界
> 这不是 Microsoft 官方答案册。每题是本库原创的学习任务，依据对应 Lesson 的公开能力目标重新表述；外部服务、Azure、Foundry、模型和 Bing 依赖必须在自己的环境按官方说明配置。

## 统一答题格式

每题提交：任务规格、预测、代码/配置、终端输出、失败轨迹、修复、测试结果、一次闭卷复述。涉及 API 的题目记录实际版本和访问日期；没有密钥时使用 `guided-labs/curriculum_labs.py` 的离线替身。

## 逐课任务

| 题号 | 官方 Lesson | 中文任务摘要（原创） | 数据/入口 | 验收标准 | 我的答案/证据 |
| :---: | :--- | :--- | :--- | :--- | :--- |
| MS01 | [Intro to AI Agents](https://github.com/microsoft/ai-agents-for-beginners/tree/main/01-intro-to-ai-agents) | 为一个课程资料问答需求画环境、感知、行动和停止条件；给出一个不应使用 Agent 的基线。 | 任选 5 条本库课程笔记；无 API 可用 P1 | 边界、状态、工具、成功/失败可解释；基线可运行。 | |
| MS02 | [Explore Agentic Frameworks](https://github.com/microsoft/ai-agents-for-beginners/tree/main/02-explore-agentic-frameworks) | 比较自研最小 runtime、代码框架、低代码和托管服务，写出 6 个选型问题与否决理由。 | `AI-Agent-框架选型与最小运行时.md` | 需求先于框架；业务测试不依赖框架私有类型。 | |
| MS03 | [Design Principles](https://github.com/microsoft/ai-agents-for-beginners/tree/main/03-agentic-design-patterns) | 为一个旅行/研究请求画用户旅程、工具权限、异常路径和人工接管点。 | P7A 或 P7C | 至少一个降级路径；不可逆动作必须停在审批。 | |
| MS04 | [Tool Use](https://github.com/microsoft/ai-agents-for-beginners/tree/main/04-tool-use) | 定义两个窄职责工具的输入/输出 schema，注入未知工具、错误类型和超时。 | P0 `test_p0_*` | 参数错误失败关闭；错误可分类；不执行未注册工具。 | |
| MS05 | [Agentic RAG](https://github.com/microsoft/ai-agents-for-beginners/tree/main/05-agentic-rag) | 对 6 份课程资料做候选检索、重排、引用和一次失败修正；区分证据与指令。 | 本库 Markdown；P3/P7C | 每条陈述有 source ID；注入文本不能提权；找不到证据则报告不足。 | |
| MS06 | [Trustworthy Agents](https://github.com/microsoft/ai-agents-for-beginners/tree/main/06-building-trustworthy-agents) | 为一个只读诊断 Agent 写威胁模型和 HITL 矩阵，按危险效果而不是关键词评测。 | P6 对抗样本 | 资产、攻击者、边界、缓解和残余风险齐全；高风险动作必须审批。 | |
| MS07 | [Planning Design](https://github.com/microsoft/ai-agents-for-beginners/tree/main/07-planning-design) | 把“整理一份带引用报告”拆成有依赖的状态图，加入重规划、预算和终止。 | P2/P7C | 缺依赖不靠无限重试；checkpoint 恢复后结果等价。 | |
| MS08 | [Multi-agent](https://github.com/microsoft/ai-agents-for-beginners/tree/main/08-multi-agent) | 比较单 Agent 与专家分工版本，记录协调成本、消息、权限和失败归属。 | P5 + 课程资料 | 拆分有可测收益；sender/receiver/task/artifact 可追踪。 | |
| MS09 | [Metacognition](https://github.com/microsoft/ai-agents-for-beginners/tree/main/09-metacognition) | 用确定性 schema/引用验证器实现两轮反思；连续无进展必须升级。 | P4 `test_p4_*` | 反馈含失败类别和证据；不伪造引用；有轮数/成本停止。 | |
| MS10 | [Production](https://github.com/microsoft/ai-agents-for-beginners/tree/main/10-ai-agents-production) | 为 P6 记录 trace/span、模型/工具版本、延迟、token、费用和逐样本结果。 | P6 eval spec | 能从一条失败轨迹定位层级；报告 P95 与安全切片。 | |
| MS11 | [Agentic Protocols](https://github.com/microsoft/ai-agents-for-beginners/tree/main/11-agentic-protocols) | 用 P5 模拟一个 MCP-like 工具和 A2A-like 长任务；画能力发现、认证、取消和 artifact 流。 | P5 `test_p5_*`；实践前核对官方规范 | 能解释 MCP/A2A 边界；协议字段写核验日期。 | |
| MS12 | [Context Engineering](https://github.com/microsoft/ai-agents-for-beginners/tree/main/12-context-engineering) | 在固定预算内选择规则、状态、历史和证据，标出不可信分区、压缩损失和拒绝理由。 | P3 `test_p3_*` | 必选规则不被淘汰；摘要保留来源/未决项；注入不提权。 | |
| MS13 | [Agent Memory](https://github.com/microsoft/ai-agents-for-beginners/tree/main/13-agent-memory) | 为一个课程助手设计写入、读取、删除和敏感信息策略；用同一任务比较无记忆/有记忆。 | 本库课程资料 | 只保存有用且可删除事实；陈旧/污染记忆可定位。 | |
| MS14 | [Microsoft Agent Framework](https://github.com/microsoft/ai-agents-for-beginners/tree/main/14-microsoft-agent-framework) | 把 P2 的本地接口映射到框架概念，列出 adapter、版本、不可迁移行为和测试分层。 | P2；需 API 时记录版本 | 核心状态与测试不引用框架私有对象。 | |
| MS15 | [Computer Use Agents](https://github.com/microsoft/ai-agents-for-beginners/tree/main/15-browser-use) | 为只读网页任务定义 HTTPS allowlist；把提交/购买动作改成审批模拟并测试 URL 绑定。 | `local-acceptance` 环境边界测试 | 越界域名、重放审批和未批准提交失败关闭。 | |
| MS16 | [Scalable Agents](https://github.com/microsoft/ai-agents-for-beginners/tree/main/16-deploying-scalable-agents) | 写部署清单：状态外置、队列/背压、幂等、路由、canary、readiness、smoke 与 eval gate。 | `AI-Agent-部署与本地运行-伸缩路由烟测.md` | `python curriculum_labs.py` smoke 通过；能说明 smoke 不等于 eval。 | |
| MS17 | [Local Agents](https://github.com/microsoft/ai-agents-for-beginners/tree/main/17-creating-local-ai-agents) | 按数据分类设计本地/云路由；本地不可用时对受限数据安全失败，不自动外传。 | P7A/P7C；无本地模型时运行 route 单元测试 | 路由硬约束先于成本/能力；记录去敏与批准。 | |
| MS18 | [Cryptographic Receipts](https://github.com/microsoft/ai-agents-for-beginners/tree/main/18-securing-ai-agents) | 为一次高风险工具调用设计 canonical receipt、action/approval digest、签名/验签、哈希链和重放测试。 | `AI-Agent-安全审计-加密收据与审批绑定.md` | 篡改、参数偷换、过期、nonce 重放可检测；说明 Ed25519/JCS 生产库边界。 | |

## 版本与环境记录

- 锁定 commit：`15ad10ca60577b75199c1ba828887ab7e66bac87`。
- 访问日期：2026-08-06。
- 当前本地标准库实验不宣称已验证 Azure/Foundry 在线服务；真实 API 题要单独记录账号、模型和服务版本。
- AutoGen 0.2 桥接单独记录在 `local-acceptance/README.md`，导入失败时不得把离线测试当成官方环境通过。
