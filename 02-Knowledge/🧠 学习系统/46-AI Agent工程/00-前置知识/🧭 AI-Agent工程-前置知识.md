---
type: index
topic: "AI Agent工程前置知识"
course: "AI Agent工程"
created: 2026-08-06
status: active
tags: [索引, 学习, 46-AI Agent工程, 前置知识]
flow: knowledge
kind: moc
assessment_exempt: true
assessment_exempt_reason: "阶段导航页由阶段验收统一承担，不作为独立知识卡验收。"
---

# 🧭 AI Agent 工程前置知识

## 为什么现在学

Agent 把模型不确定性接入真实代码。若不会处理消息、JSON、异常和测试替身，后续错误会被误判成“模型不够聪明”，也无法离线复现。

## 学习目标

- 区分模型、工具和编排层的输入输出。
- 用结构化错误而非模糊字符串表示失败。
- 用 fake model/tool 覆盖正常、空输入和畸形输入。

## 学习顺序

1. [[AI-Agent-前置-消息JSON异常与单元测试]]：先掌握消息、解析、异常和确定性测试。

## 阶段验收与作业

- **课后作业**：[[AI-Agent工程-课后作业-01-消息契约与测试]]。
- **通过标准**：能闭卷解释消息角色，写出 JSON 解析失败分支，并让正常/空值/格式错误测试全部通过。
- **下一阶段**：通过后进入 [[🧭 阶段1-Agent基础与受限循环]]。
