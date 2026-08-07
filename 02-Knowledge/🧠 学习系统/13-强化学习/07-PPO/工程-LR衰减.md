---
type: study
topic: "工程-LR衰减"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["工程-LR衰减", "学习率衰减"]
upstream: ["[[PPO近端策略优化]]"]
tags: [学习, 强化学习]
---

# 工程-LR衰减

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
RL 训练后期需要更小的学习率来稳定收敛。

## 正式定义 / 公式
常见调度：线性衰减（从 LR₀ 线性降到 0）、余弦退火、分段常数。PPO 常配合 Adam，总步数内做线性 LR 衰减。

## 最小手算例子
1e-3 起始，训练 1e7 步线性降到 0。

## 对比与常见错误
- 与 工程-梯度裁剪：一个调步长、一个调梯度尺度。
- 常见错误：学习率固定不变——后期易在最优附近抖动。

## 闭卷自测
1. RL 中常用哪些 LR 调度？
2. 衰减为何有助于收敛？
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
