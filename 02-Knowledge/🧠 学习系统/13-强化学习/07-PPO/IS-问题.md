---
type: study
topic: "IS-问题"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["IS-问题", "IS 高方差"]
upstream: ["[[IS-稳定]]"]
tags: [学习, 强化学习]
---

# IS-问题

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
明确重要性采样的根本缺陷，才能理解 TRPO/PPO 为何要约束或裁剪。

## 正式定义 / 公式
主要问题：
1. 高方差：当 π 与 μ 支撑集或形状差异大时，ρ(τ) 方差爆炸；
2. 小权重主导消失：多数样本权重趋 0，有效样本极少；
3. 长轨迹累积使 ρ(τ) 进一步不稳定。

## 最小手算例子
10 步轨迹每步 ρ=1.1 → 乘积≈2.6；每步 ρ=0.9 → ≈0.35，分布严重偏斜。

## 对比与常见错误
- 与 IS-稳定：问题是偏离后的现象，稳定是缓解手段。
- 常见错误：以为 IS 永远无偏就好——无偏但方差爆炸同样无法训练。

## 闭卷自测
1. 重要性采样在 off-policy 下三大问题是什么？
2. 它们如何催生 TRPO/PPO 的设计？
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
