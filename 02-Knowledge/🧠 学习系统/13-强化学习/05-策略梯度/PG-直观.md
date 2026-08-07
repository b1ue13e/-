---
type: study
topic: "PG-直观"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["PG-直观", "策略梯度直观"]
upstream: ["[[PG-梯度]]"]
tags: [学习, 强化学习]
---

# PG-直观

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
给梯度一个直觉：它像"用回报给动作打分后，把概率推向高分动作"。

## 正式定义 / 公式
∇_θ J ≈ (1/N) Σ (∇_θ log π_θ(a|s)) · G
- G 高且动作概率低 → 大幅增大该动作概率；
- G 低 → 减小该动作概率。
相当于"用回报作为权重"做监督式似然上升。

## 最小手算例子
两动作中 a1 总拿高回报，则梯度持续把 π(a1) 推高；a2 回报低则被压低，最终策略偏向 a1。

## 对比与常见错误
- 常见错误：认为梯度"直接复制动作"——它只调整概率，动作本身是采样得到。

## 闭卷自测
1. 用一句话解释策略梯度的直觉。
2. 回报 G 在梯度里扮演什么角色？
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
