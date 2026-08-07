---
type: study
topic: "IS-稳定"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["IS-稳定", "IS 稳定性"]
upstream: ["[[IS-比率]]"]
tags: [学习, 强化学习]
---

# IS-稳定

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
理解为何重要性权重需要被控制，才能引出 PPO 的裁剪动机。

## 正式定义 / 公式
稳定性来自"两策略不要太远"：若 μ 与 π_θ 接近，ρ_t≈1，权重波动小；否则 ρ(τ) 可能趋于 0 或 ∞，梯度爆炸/消失。

## 最小手算例子
ρ_t 在 0.5–2.0 之间时训练平稳；若个别 ρ_t=50，单样本主导梯度。

## 对比与常见错误
- 与 IS-问题：稳定是目标，问题是偏离时的后果。
- 常见错误：放任比率无界——这正是 PPO 用 clip 限制它的原因。

## 闭卷自测
1. 为何重要性权重需要被限制？
2. 权重无界会带来什么后果？
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
