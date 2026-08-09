---
type: index
topic: "AI Agent工程"
aliases: ["🗺️ 框架", "🛠️ 主线：AI Agent 工程", "🧭 AI-Agent工程课程学习与认知支架"]
tags: [索引, 学习, 46-AI Agent工程, AI-Agent]
created: 2026-08-05
status: active
flow: knowledge
kind: moc
source_of_truth: true
source: "UC Berkeley CS 194/294-196 F24/F25; Microsoft AI Agents for Beginners; Datawhale Hello-Agents"
accessed: 2026-08-06
license: "课程页许可逐项登记于教材挂载索引；本路径为原创融合导航"
assessment_exempt: true
assessment_exempt_reason: "课程唯一学习入口与阶段导航，不作为独立知识卡验收。"
---

# 🗺️ AI Agent 工程学习路径

> [!abstract] 学习结果
> 从“会调用聊天模型”走到“能设计、实现、测试和约束一个可复现的智能体系统”。课程以 Microsoft AI Agents for Beginners 的当前 18 Lesson 能力面作为 primary spine，以 Datawhale Hello-Agents 的中文原理和从零实现深度作为 co-spine；Berkeley Fall 2024 三个公开 Lab 仅作为历史官方作业与兼容实验补充。来源角色、许可、版本与取舍见 [[📚 教材挂载索引|教材挂载索引]]。

## 0. 使用边界

- **官方课程/作业**：仅链接、概括目标并建立知识映射，不复制答案、隐藏测试或受限讲义正文。
- **本库教学卡**：均为根据公开一手来源重新组织的原创中文教学内容，不冒充学校原讲义。
- **框架版本**：Microsoft 官方课程在 2026-08-06 已以 Microsoft Agent Framework / Foundry Agent Service V2 为当前代码主线；AutoGen 0.2 只为 Berkeley F24 Lab 建立隔离兼容环境，不能混写为当前官方推荐。
- **成本与密钥**：所有主题卡都提供可运行的 Python 标准库微型实现；官方 Lab 可能需要模型 API、AutoGen 或在线服务。
- **融合边界**：不复制两教材长代码或答案；吸收能力目标、对比维度和实践结构，重新组织为本库主题卡、故障注入和迁移任务。
- **动态规范**：MCP、A2A、框架和云部署会漂移；学习稳定概念，实践前按卡片核验日期重开官方规范。

## 1. 前置诊断（先做再学）

先确认已具备 Python、基础 ML/DL、LLM/Prompt/RAG；Berkeley F24 官方页明确鼓励类似 CS182/188/189 的机器学习经验。缺少模型与 RAG 基础先走 [[🗺️ 生成式AI基础与Prompt工程学习路径|生成式 AI 与 Prompt 工程]]，缺少 ML/DL 再补 [[🗺️ 机器学习学习路径|机器学习]]。

闭卷回答；工程题任一项不会先完成 [[AI-Agent-前置-消息JSON异常与单元测试]]：

1. Python 函数如何用类型、异常和测试表达输入输出契约？
2. system / user / tool 消息承担什么不同职责？
3. 为什么一次 LLM 调用不等于 Agent？
4. 为什么最终答案正确仍不足以证明 Agent 可靠？
5. Prompt injection 与普通“越狱”有什么不同？

## 2. 主线阶段

课程入口只维护阶段顺序；每个阶段 MOC 维护本阶段知识卡、目标、作业与出口。

1. [[🧭 AI-Agent工程-前置知识]]：消息、JSON、异常与测试替身；产出离线可复现契约测试。
2. [[🧭 阶段1-Agent基础与受限循环]]：Agent 边界、ReAct、工具契约；产出失败关闭的有限循环。
3. [[🧭 阶段2-运行时规划与状态]]：最小 runtime、状态机、多角色消息、框架隔离；产出可恢复管线。
4. [[🧭 阶段3-上下文记忆与校验]]：上下文预算、证据记忆、有限反思；产出带引用研究助手。
5. [[🧭 阶段4-协作协议与环境]]：MCP/A2A、威胁模型与沙箱；产出跨边界受限任务。
6. [[🧭 阶段5-评测与生产运行]]：四层评测、可观测与恢复；产出攻防评测包。
7. [[🧭 阶段6-部署审计与改进]]：伸缩路由、加密收据、奖励审计；产出课程大作业。

## 3. 官方作业主线

Berkeley 的公开说明给出三份 Lab、任务方向和通过门槛；本库不保存解答。

| 官方作业 | 官方目标 | 本库映射 |
| :--- | :--- | :--- |
| Lab 01 — Restaurant Review Pipeline | 用 AutoGen 构建餐厅评论分析与评分管线；历史公开门槛 3/4 | [[AI-Agent工程-阶段作业-02-餐厅评论可恢复管线]] |
| Lab 02 — Writing LLM Attacks | 编写攻击提示；历史隐藏门槛 1/2 | [[AI-Agent工程-阶段作业-05-Agent攻防与四层评测]] |
| Lab 03 — Defending Against LLM Attacks | 编写防御提示；历史隐藏门槛 1/3 | [[AI-Agent工程-阶段作业-05-Agent攻防与四层评测]] |

官方总说明：<https://rdi.berkeley.edu/llm-agents-mooc/assets/instructions.pdf>

> 上表数字是 Fall 2024 历史课程事实，不是当前本地 Gate。本课先在项目根运行 `python -m unittest discover -s tests -v`，再在官方环境仍可用时记录官方结果；绝不把本地测试冒充 Berkeley 成绩。

## 4. 两条完成路径

### 最小作业路径（先交出可验收结果）

1. [[AI-Agent-前置-消息JSON异常与单元测试]]
2. [[AI-Agent-边界与感知行动循环]]、[[AI-Agent-工具调用与结构化契约]]
3. [[AI-Agent-规划状态与工作流编排]]、[[AI-Agent-多智能体协作与消息协议]]
4. [[AI-Agent-框架-AutoGen官方Lab版本补丁]]
5. 本地 Agent runtime、恶意证据、有限终止和恢复测试全绿 → 官方 Lab 01
6. [[AI-Agent-安全威胁建模与系统评测]]
7. 本地攻防回归 → 官方 Lab 02/03

### 全面掌握路径（不止通过测试）

按阶段 0→6 完成核心主线，并完成 [[03-Projects/46-AI Agent工程/🧭 课程作业总索引|课程作业总索引]] 中的课后作业、阶段作业与 [[AI-Agent工程-大作业-受限可恢复Agent]]；Agentic RL 奖励审计为选修。每个实验保留任务定义、数据样例、轨迹、失败分类、指标、成本、随机种子/模型版本和复现实录。

## 5. 验收门

- [ ] **Gate A · 概念**：能说明 Agent 与工作流、聊天机器人、工具函数的边界。
- [ ] **Gate B · 实现**：标准库最小 Agent、工具注册表和工作流示例均能运行。
- [ ] **Gate C · 作业**：`python -m unittest -v` 全绿，且测试确实执行工具、handoff、状态、终止、trace、checkpoint 与安全边界；官方环境可用时再按官方规范自行完成三份 Lab，不读取他人答案。
- [ ] **Gate D · 可靠性**：至少建立 10 个正常测试、5 个异常测试、5 个对抗测试。
- [ ] **Gate E · 复盘**：能从轨迹定位失败属于模型、工具、编排、数据还是权限层。
- [ ] **Gate F · 迁移**：换领域和工具后仍通过测试；只改名称或 Prompt 不算迁移。
- [ ] **Gate G · 部署/审计**：部署 smoke 与离线 eval 分离；高风险动作可验证审批绑定或明确安全失败。

## 6. 学习节奏、渐隐与补救

- **建议时长**：有 Python、LLM 与 RAG 基础者 12 周；小白 16 周，每周 7–9 小时。Agentic RL 是选修，不用 GPU 阻塞核心路线。
- **每周闭环**：闭卷预测 → 最小讲解 → 手算 → 运行 → 故障注入 → 解释 → 跨领域迁移；“看懂”不计通过。
- **渐隐支架**：先运行 `scripts/` worked baseline；再保留接口与测试补全控制流；随后只看任务规格独立实现；最后换领域、数据与工具重建威胁和评测。
- **间隔检索**：次日、3 天、7 天、14 天闭卷复现；失败只回到具体先修卡，不重抄整章。
- **补救入口**：JSON/异常/测试薄弱回到 [[🧭 AI-Agent工程-前置知识]]；循环失控回到 [[AI-Agent-规划状态与工作流编排]]；长任务混乱回到 [[AI-Agent-上下文工程-选择压缩隔离]]；安全与评测混淆回到 [[AI-Agent-安全威胁建模与系统评测]]。

高阶验收统一检查边界、正确性、可观测、安全、恢复与迁移；安全为零时总分再高也不通过。

## 7. 课程资源与治理

- 资源授权、公开性、使用风险与多源融合自评：[[02-Knowledge/🧠 学习系统/46-AI Agent工程/📚 教材挂载索引|教材挂载索引]]
- Microsoft/Hello-Agents 逐章去向与去重依据：[[02-Knowledge/🧠 学习系统/46-AI Agent工程/📚 教材挂载索引|教材挂载索引]] 第 7–8 节
- 作业必需知识：由各作业 frontmatter 的 `requires` 维护并由知识卡反向派生
- 三级作业与故障注入：[[03-Projects/46-AI Agent工程/🧭 课程作业总索引|课程作业总索引]]
- 原创结课项目：[[AI-Agent工程-大作业-受限可恢复Agent]]

## 8. 学习记录

| 日期 | 卡片/作业 | 闭卷结果 | 失败样例 | 下一步 |
| :--- | :--- | :--- | :--- | :--- |
| | | | | |
