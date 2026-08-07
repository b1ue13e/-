---
type: study
topic: "TRPO-单调"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TRPO-单调", "TRPO 单调改进"]
upstream: ["[[TRPO-信任区域]]", "[[策略梯度]]"]
tags: [学习, 强化学习]
---

# TRPO-单调

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
TRPO 的理论底气：在信任域内更新能保证"性能单调不降"（近似）。

## 正式定义 / 公式
单调改进定理：若 KL 约束满足，则 J(θ_new) ≥ J(θ_old) − 常数·KL，保证每步不大幅变差。
这是 TRPO/PPO "稳定"的理论依据。

## 最小手算例子
<!-- NUMEX2 -->单调改进定理：若 KL(π_new‖π_old)≤δ，则 η(π_new)≥η(π_old)−C·δ²（带下界）。取 δ=0.01 ⇒ 每步性能下降有上限，迭代近似单调上升。

每步满足 KL 约束后，性能至少不显著下降；配合足够大的有效步长，稳步提升。

## 对比与常见错误
- 与 REINFORCE 不稳定：单调保证从机制上避免崩溃。
- 常见错误：把"单调"当"每步必涨"——它保证不显著变差，非保证必涨。

## 闭卷自测
1. TRPO 的单调改进保证是什么？
2. 它为何能避免崩溃？
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
