---
type: study
topic: "PG-目标函数"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["PG-目标函数", "策略梯度目标 J(θ)"]
upstream: ["[[策略梯度]]", "[[回报定义]]"]
tags: [学习, 强化学习]
---

# PG-目标函数

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
基于值的方法学 Q* 再贪心出策略；策略梯度则直接"参数化策略 π_θ 并最大化期望回报"，天然适配连续/随机策略。先明确要优化的目标函数。

## 正式定义 / 公式
目标（性能）函数：
J(θ) = E_{τ~π_θ} [ R(τ) ] = E [ Σ_t γ^t r_{t+1} ]
即在策略 π_θ 下采样轨迹 τ，对其折扣回报取期望。
优化目标：max_θ J(θ)。

## 最小手算例子
两动作 softmax 策略 π_θ：选 a1 得 +1、a2 得 0。J(θ) 即"选 a1 的概率 ×1"。增大 θ 提升 a1 概率即提升 J。

## 对比与常见错误
- 与值方法：值方法优化 Q 再派生策略；策略梯度直接优化策略参数。
- 常见错误：把 J(θ) 当成"单条轨迹回报"——目标是"期望"，优化用梯度而非单条样本直接爬。

## 闭卷自测
1. 策略梯度的目标函数 J(θ) 是什么？
2. 它和值方法的目标有何不同？
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
