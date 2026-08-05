---
type: index
topic: "AI Agent工程"
tags: [索引, 学习, 46-AI Agent工程, AI-Agent]
created: 2026-08-05
status: active
flow: knowledge
kind: moc
source_of_truth: true
source: "UC Berkeley CS 194/294-196 Large Language Model Agents (Fall 2024)"
---

# 🗺️ AI Agent 工程学习路径

> [!abstract] 学习结果
> 从“会调用聊天模型”走到“能设计、实现、测试和约束一个可复现的智能体系统”。课程以 UC Berkeley CS 194/294-196 Fall 2024 为理论主线，以其公开 Lab 01–03 为官方作业验收，以 Stanford CS224V 和 Apache-2.0 的 Hugging Face Agents Course 作公开补充。

## 0. 使用边界

- **官方课程/作业**：仅链接、概括目标并建立知识映射，不复制答案、隐藏测试或受限讲义正文。
- **本库教学卡**：均为根据公开一手来源重新组织的原创中文教学内容，不冒充学校原讲义。
- **框架版本**：框架只是实现手段；先掌握循环、状态、工具契约、评测与安全，再学习 AutoGen、smolagents、LangGraph 等具体 API。
- **成本与密钥**：所有主题卡都提供可运行的 Python 标准库微型实现；官方 Lab 可能需要模型 API、AutoGen 或在线服务。

## 1. 前置诊断（先做再学）

闭卷回答；任一项不会就先看 [[AI-Agent工程-作业必需与全面知识清单]] 的“前置补给”。

1. Python 函数如何用类型、异常和测试表达输入输出契约？
2. system / user / tool 消息承担什么不同职责？
3. 为什么一次 LLM 调用不等于 Agent？
4. 为什么最终答案正确仍不足以证明 Agent 可靠？
5. Prompt injection 与普通“越狱”有什么不同？

## 2. 主线阶段

| 阶段 | 核心问题 | 主题卡 | 最小产出 | 对应官方作业 |
| :--- | :--- | :--- | :--- | :--- |
| 1. 定义边界 | 什么才是 Agent？何时不该用 Agent？ | [[AI-Agent-边界与感知行动循环]] | 状态机式最小 Agent | Lab 01 前置 |
| 2. 推理与行动 | 如何把“想”与“做”交替组织？ | [[AI-Agent-ReAct推理行动范式]] | 受限 ReAct 轨迹 | Lab 01 前置 |
| 3. 可靠用工具 | 如何让模型发出可校验动作？ | [[AI-Agent-工具调用与结构化契约]] | 工具注册表与参数校验 | Lab 01 必需 |
| 4. 拆解流程 | 如何把长任务变成可恢复工作流？ | [[AI-Agent-规划状态与工作流编排]] | DAG/状态机管线 | Lab 01 必需 |
| 5. 取得外部证据 | 如何管理上下文、短期状态与长期知识？ | [[AI-Agent-记忆与检索增强生成]] | 可引用的小型 RAG | Lab 01 全面 |
| 6. 分工协作 | 何时多 Agent 比单 Agent 更合理？ | [[AI-Agent-多智能体协作与消息协议]] | 角色分离评分管线 | Lab 01 必需 |
| 7. 证明可用 | 如何攻击、保护并量化可靠性？ | [[AI-Agent-安全威胁建模与系统评测]] | 攻防测试矩阵 | Lab 02/03 必需 |

## 3. 官方作业主线

Berkeley 的公开说明给出三份 Lab、任务方向和通过门槛；本库不保存解答。

| 官方作业 | 官方目标 | 本库映射 |
| :--- | :--- | :--- |
| Lab 01 — Restaurant Review Pipeline | 用 AutoGen 构建餐厅评论分析与评分管线；公开测试通过至少 3/4 | [[Berkeley-Lab01-Restaurant-Review-Pipeline-知识点映射]] |
| Lab 02 — Writing LLM Attacks | 编写攻击提示；隐藏测试至少通过 1/2 | [[Berkeley-Lab02-Writing-LLM-Attacks-知识点映射]] |
| Lab 03 — Defending Against LLM Attacks | 编写防御提示；隐藏攻击测试至少通过 1/3 | [[Berkeley-Lab03-Defending-Against-LLM-Attacks-知识点映射]] |

官方总说明：<https://rdi.berkeley.edu/llm-agents-mooc/assets/instructions.pdf>

## 4. 两条完成路径

### 最小作业路径（先交出可验收结果）

1. [[AI-Agent-边界与感知行动循环]]
2. [[AI-Agent-工具调用与结构化契约]]
3. [[AI-Agent-规划状态与工作流编排]]
4. [[AI-Agent-多智能体协作与消息协议]]
5. 完成 Lab 01
6. [[AI-Agent-安全威胁建模与系统评测]]
7. 完成 Lab 02 → Lab 03

### 全面掌握路径（不止通过测试）

按 1→7 全部完成，并为每个实验保留：任务定义、数据样例、轨迹、失败分类、指标、成本、随机种子/模型版本和复现实录。

## 5. 验收门

- [ ] **Gate A · 概念**：能说明 Agent 与工作流、聊天机器人、工具函数的边界。
- [ ] **Gate B · 实现**：标准库最小 Agent、工具注册表和工作流示例均能运行。
- [ ] **Gate C · 作业**：按官方测试和提交规范自行完成三份 Lab，不读取他人答案。
- [ ] **Gate D · 可靠性**：至少建立 10 个正常测试、5 个异常测试、5 个对抗测试。
- [ ] **Gate E · 复盘**：能从轨迹定位失败属于模型、工具、编排、数据还是权限层。

## 6. 课程资源与治理

- 资源授权、公开性和使用风险：[[AI-Agent工程-开源课程与作业资源索引]]
- 作业必需知识与全面知识的分层矩阵：[[AI-Agent工程-作业必需与全面知识清单]]

## 7. 学习记录

| 日期 | 卡片/作业 | 闭卷结果 | 失败样例 | 下一步 |
| :--- | :--- | :--- | :--- | :--- |
| | | | | |

