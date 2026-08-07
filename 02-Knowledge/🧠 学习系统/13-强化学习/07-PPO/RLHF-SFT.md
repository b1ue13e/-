---
type: study
topic: "RLHF-SFT"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["RLHF-SFT", "监督微调"]
upstream: ["[[RLHF-背景]]"]
tags: [学习, 强化学习]
---

# RLHF-SFT

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
RLHF 的第一步：先让模型具备基本指令跟随能力。

## 正式定义 / 公式
SFT（Supervised Fine-Tuning）：在高质量 (prompt, 期望回答) 演示数据上用标准交叉熵微调预训练模型，得到初始策略 π_SFT。

## 最小手算例子
收集 10k 条"指令—优质回答"对，做若干 epoch 监督训练。

## 对比与常见错误
- 与 RLHF-背景：SFT 是 RLHF 流水线的第 1 步。
- 常见错误：用 SFT 直接替代 RLHF——SFT 缺乏"按人类偏好择优"的机制。

## 闭卷自测
1. SFT 在 RLHF 中扮演什么角色？
2. SFT 与后续 RL 阶段的关系？
## 学完后可以完成

```dataview
TABLE assignment_level, source_type FROM "03-Projects"
WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
```
