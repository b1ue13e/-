---
type: index
topic: "AI Agent基础与受限循环"
course: "AI Agent工程"
created: 2026-08-06
status: active
tags: [索引, 学习, 46-AI Agent工程, Agent基础]
flow: knowledge
kind: moc
assessment_exempt: true
assessment_exempt_reason: "阶段导航页由阶段验收统一承担，不作为独立知识卡验收。"
---

# 🧭 阶段 1：Agent 基础与受限循环

## 为什么现在学

先判断任务是否真的需要 Agent，再把自主性限制在可观察、可停止的循环内；否则后续框架只会放大模糊边界。

## 学习目标

- 区分聊天、固定工作流与 Agent。
- 手算一次 Thought/Action/Observation 状态转移。
- 为工具建立可校验 schema、权限和错误语义。

## 学习顺序

1. [[AI-Agent-边界与感知行动循环]]：定义环境、状态、动作与停止。
2. [[AI-Agent-ReAct推理行动范式]]：理解观察何时改变下一步动作。
3. [[AI-Agent-工具调用与结构化契约]]：把动作收敛为可信执行层可验证的请求。

## 阶段验收与作业

- **课后作业**：[[AI-Agent工程-课后作业-02-受限循环与工具契约]]。
- **阶段作业**：[[AI-Agent工程-阶段作业-01-有限ReAct工具台]]。
- **通过标准**：未知工具、非法参数和步数耗尽均失败关闭；能解释何时降级为固定工作流。
- **下一阶段**：通过后进入 [[🧭 阶段2-运行时规划与状态]]。

