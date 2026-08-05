---
type: index
topic: "Datawhale Hello-Agents 逐章习题册"
tags: [索引, 46-AI Agent工程, 课后习题, Hello-Agents]
created: 2026-08-06
status: active
flow: project
kind: moc
source: "Datawhale Hello-Agents, commit d4953e839714cf0baaa624c0d9b4731c48a2a131, accessed 2026-08-06"
license_note: "Repository CC BY-NC-SA 4.0; this companion is original Chinese task design and does not copy chapter answers."
---

# Datawhale Hello-Agents：逐章习题册

> [!warning] 使用边界
> 这不是 Datawhale 官方答案册。每题是本库原创任务，使用章节公开主题作为学习目标；代码、数据、API 和框架版本按实践日期核验。所有答案、轨迹和失败复盘留在个人证据包中。

## 统一答题格式

每题写：一句话目标、前置、预测、手算、运行/代码、故障注入、验收、闭卷复述和双链。需要模型或 GPU 的章节先用 `guided-labs/` 标准库替身完成控制流。

## 逐章任务

| 题号 | 官方章节 | 中文任务摘要（原创） | 数据/入口 | 验收标准 | 我的答案/证据 |
| :---: | :--- | :--- | :--- | :--- | :--- |
| H01 | [第一章 初识智能体](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter1) | 为“课程资料问答”定义环境、感知、行动、状态和停止；实现 5 分钟最小循环。 | P1；本库 5 条 Markdown | 能区分聊天/工作流/Agent；循环有上限和失败输出。 | |
| H02 | [第二章 智能体发展史](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter2) | 用符号规则、统计模型、LLM Agent 三种方式解释同一分类任务，标注状态/策略/环境变化。 | 自造 6 条短文本 | 不是背年代；能说清每一范式的可解释性、泛化和行动差异。 | |
| H03 | [第三章 大语言模型基础](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter3) | 诊断 Transformer、消息、上下文窗口和模型不确定性先修；不会的内容转 45 路径补救。 | [[45-生成式AI基础与Prompt工程/🗺️ 生成式AI基础与Prompt工程学习路径]] | 写出先修缺口，不把模型幻觉归因于“Agent 自主”。 | |
| H04 | [第四章 经典范式构建](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter4) | 用同一任务比较 ReAct、Plan-and-Solve、Reflection 的状态、成本、失败和停止差异。 | P1/P2/P4 | 至少一个手算轨迹；Reflection 由验证器触发而非无限思考。 | |
| H05 | [第五章 低代码平台](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter5) | 选择一个低代码平台做只读流程原型，并写出导出、版本、权限、测试和供应商锁定风险。 | 不上传敏感数据 | 能证明何时低代码足够、何时需代码 runtime；不把平台演示当生产验收。 | |
| H06 | [第六章 框架开发实践](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter6) | 将同一个工具/状态契约映射到两个框架或一个框架与本地 adapter，记录私有类型和版本差异。 | P2；AutoGen 需隔离环境 | 核心测试只依赖本地接口；版本写入证据包。 | |
| H07 | [第七章 构建你的 Agent 框架](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter7) | 用标准库实现 model adapter、tool registry、state、orchestrator、termination、trace、eval 七部件。 | `guided-labs/curriculum_labs.py` | 未知工具/异常/终止/trace 全有测试；不复制框架实现。 | |
| H08 | [第八章 记忆与检索](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter8) | 为课程助手定义记忆写入/读取/删除策略，并对 6 条资料保留 source ID；注入一条恶意记忆。 | 本库 Markdown | 记忆不是完整历史；污染不会成为系统指令；能删除/过期。 | |
| H09 | [第九章 上下文工程](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter9) | 实现 GSSC 装配：固定规则、当前状态、候选证据、摘要和 token 预算；记录被拒信息。 | P3 | 必选规则保留、证据可回溯、过载可解释、注入不提权。 | |
| H10 | [第十章 通信协议](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter10) | 用 MCP-like tool 与 A2A-like task 做跨边界模拟，补 Agent Card、能力、状态、artifact、认证和取消。 | P5；实践时按官方规范核验 | 能说明 MCP/A2A/ANP 的适用边界；不将消息冒充交付物。 | |
| H11 | [第十一章 Agentic-RL](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter11) | 不训练模型，先为 P7 写轨迹奖励，构造两条 reward hacking，分离训练/回归/盲测。 | P8；无 GPU | 奖励分量可解释；安全退化阻止上线；能说明何时修数据/工具而非训练。 | |
| H12 | [第十二章 性能评估](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter12) | 为 20 正常、10 异常、10 对抗样本写 eval spec，计算 TSR/ToolAcc/ASR/FRR/P95/成本。 | P6；`test_curriculum_labs.py` | 逐样本结果可查；公共基准不替代领域和安全评测。 | |
| H13 | [第十三章 智能旅行助手](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter13) | 在静态航班/酒店数据上实现预算约束的行程规划；预订是高风险动作，必须 approval digest/幂等。 | `plan_trip` P7A；不接真实支付 | 未知目的地/超预算/未审批均失败关闭；报告证据与成本。 | |
| H14 | [第十四章 自动化深度研究](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter14) | 用 TODO 驱动拆解 3 个子问题，检索本库资料，生成 claim/source_id 报告；冲突时保留不确定性。 | `research_report` P7C | 不能生成无来源陈述；可从 trace 复盘查询、摘要和写作。 | |
| H15 | [第十五章 构建赛博小镇](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter15) | 先用确定性状态机模拟 NPC 情绪/事件/记忆上限，再设计未来接入 LLM 的边界；不以游戏画面替代状态验收。 | `tick_town` P7B | 同一事件可复现；状态转移、隐私、消息和失败有测试。 | |
| H16 | [第十六章 毕业设计](https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter16) | 从旅行、深度研究、课程资料助手或离线小镇中选一条，完成需求、runtime、工具、评测、安全、部署和复盘。 | [[AI-Agent工程-结课项目]] | ≥8/10 且安全维度 2；迁移后仍有正常/异常/对抗测试。 | |

## 版本与环境记录

- 锁定 commit：`d4953e839714cf0baaa624c0d9b4731c48a2a131`。
- 访问日期：2026-08-06。
- 仓库许可证：`LICENSE.txt`，CC BY-NC-SA 4.0；本册不复制正文和答案。
- Chapter 11 的训练代码需要独立 GPU/依赖环境；本课程的核心通过 P8 奖励审计，不把未验证训练结果写成成绩。
