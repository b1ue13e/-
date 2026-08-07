---
type: study
topic: "IS-约束"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["IS-约束", "KL 约束"]
upstream: ["[[IS-KL]]", "[[TRPO-信任区域]]"]
tags: [学习, 强化学习]
---

# IS-约束

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
把 KL 作为约束放进优化问题，就是 TRPO 信任区域的核心思想。

## 正式定义 / 公式
带 KL 约束的更新：
max_θ  E_{s~π_θ}[ A(s,a) ]   s.t.  KL(π_{θ_old} ‖ π_θ) ≤ δ
保证新策略与旧策略的 KL 不超过 δ，从而限制更新步幅、保证单调改进。

## 最小手算例子
δ=0.01：只允许在旧策略邻域内调整参数，避免一步走偏。

## 对比与常见错误
- 与 TRPO：这正是 TRPO 的数学形式。
- 常见错误：把约束当成惩罚项——TRPO 是硬约束（用共轭梯度求解）。

## 闭卷自测
1. KL 约束在优化问题中起什么作用？
2. 它与惩罚项有何区别？
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
