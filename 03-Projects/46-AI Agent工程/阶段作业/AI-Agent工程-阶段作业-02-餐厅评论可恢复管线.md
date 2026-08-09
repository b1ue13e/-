---
type: project
project_type: homework
topic: "餐厅评论可恢复管线"
course: "AI Agent工程"
assignment_id: "AI-Agent工程-S02"
assignment_level: stage
assignment_format: lab
stage_id: "02"
requires: ["[[AI-Agent-框架选型与最小运行时]]", "[[AI-Agent-规划状态与工作流编排]]", "[[AI-Agent-框架-AutoGen官方Lab版本补丁]]", "[[AI-Agent-工具调用与结构化契约]]", "[[AI-Agent-多智能体协作与消息协议]]"]
source_type: official_assignment
source: "UC Berkeley LLM Agents MOOC Fall 2024 Lab 01 public objective; 本文件是非官方中文任务摘要与本地等价验收"
source_url: "https://rdi.berkeley.edu/llm-agents-mooc/assets/instructions.pdf"
accessed: 2026-08-06
license: "公开说明许可未统一声明；starter逐文件许可证[待验证]；本文件不复制题面、starter或答案"
created: 2026-08-06
status: planned
flow: project
tags: [作业, 阶段作业, 46-AI Agent工程, Berkeley, AutoGen]
---

# AI Agent 工程阶段作业 02：餐厅评论可恢复管线

> [!warning] 身份边界
> Berkeley F24 Lab 01 的公开目标是用 AutoGen 构建餐厅评论分析评分管线，历史公开门槛为公共测试 3/4。本任务保留这一事实和官方链接，但采用课程原创本地数据与测试；本地通过不冒充 Berkeley 成绩。

## 学习目标

实现 intake → retrieve → score → aggregate → finalize 状态机，隔离业务逻辑与框架 adapter，并验证中断恢复等价。

## 任务背景与边界

输入餐厅名，读取本地评论，抽取 1–5 分并聚合。未知餐厅、畸形评分、恶意评论和中断必须显式处理。默认使用 `scripts/agent_runtime.py` 离线基线；官方 AutoGen 0.2 环境只有在取得合法 starter 后另建虚拟环境。

## 详细题目与里程碑

1. **M1 纯函数**：实体归一化、评论检索、分数解析和聚合，各自有边界测试。
2. **M2 状态机**：每阶段记录输入/输出/错误/下一状态，限制重试和总步数。
3. **M3 handoff**：消息含 sender、recipient、task、artifact、request_id；重复请求幂等。
4. **M4 恢复**：在 score 后写 checkpoint，中断后恢复，最终结果与不中断执行一致。
5. **M5 框架桥**：只在历史兼容环境把本地接口映射到 AutoGen 0.2；核心测试不引用框架私有类型。

## 任务分层

- **基础要求**：纯函数、显式状态机、唯一证据 ID、有限重试和 checkpoint 恢复等价全部通过。
- **必要提示**：先验证标准库控制面；框架桥是 adapter，不得把框架对象写入可持久化业务状态。
- **常见错误**：重复值证据使用 `list.index` 产生 ID 碰撞、恢复后重复副作用、异常被吞成空分数。
- **可选进阶**：在合法独立环境运行历史 AutoGen smoke；缺依赖时记录未验证，不影响本地基础任务。

## 环境与复现

- 本地：Python 3.11+ 标准库，在项目根执行 `python -m unittest discover -s tests -v`。
- 历史官方兼容：`autogen-agentchat==0.2.40` 仅是本库已烟测候选；若合法 starter 声明不同精确版本，以 starter 为准。
- 数据为课程原创静态评论；无 GPU。真实模型/API 另层记录密钥与费用，不进入离线通过声明。

## 提交产物

源码、测试、状态图、两条 checkpoint、去敏 trace、依赖锁定、官方/本地结果分栏记录。

## 验收标准与 Rubric

纯函数与契约 20 分、状态/终止 25 分、handoff 15 分、恢复等价 20 分、故障与恶意证据测试 15 分、版本边界 5 分。总分 ≥85；框架版本混装、无限重试或伪报官方成绩直接不通过。

## 引导、自检与后续

先跑本地离线测试，再考虑官方环境；解析与聚合不要交给模型碰运气。通过后进入 [[🧭 阶段3-上下文记忆与校验]]。
