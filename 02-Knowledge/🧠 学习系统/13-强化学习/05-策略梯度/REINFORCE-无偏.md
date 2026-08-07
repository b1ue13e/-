---
type: study
topic: "REINFORCE-无偏"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["REINFORCE-无偏", "REINFORCE 无偏估计"]
upstream: ["[[REINFORCE-MC]]"]
tags: [学习, 强化学习]
---

# REINFORCE-无偏

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
"无偏"意味着估计量的期望等于真实梯度——这是 REINFORCE 的理论优点（虽高方差）。

## 正式定义 / 公式
在策略 π_θ 下采样，E[ Σ_t ∇log π(a_t|s_t) · G_t ] = ∇_θ J(θ)
即期望等于真梯度（用完整回报、正确重要性权重时）。

## 最小手算例子
<!-- NUMEX2 -->REINFORCE 梯度估计 ∇J≈(G_t−b)∇lnπ(a_t|s_t) 是无偏的（期望=真实策略梯度）。例：单样本 G=10,b=0 ⇒ 估计=10×∇lnπ；多样本均值→真实梯度，但单样本方差大。

单条轨迹的梯度是"噪声估计"，但无限多轨迹平均会收敛到真 ∇J。

## 对比与常见错误
- 与 TD 策略梯度：TD 用 bootstrap 回报也是有偏但低方差；REINFORCE 无偏但高方差。
- 常见错误：把"无偏"等同于"好用"——无偏但高方差仍需大量样本。

## 闭卷自测
1. REINFORCE 估计为什么无偏？
2. 无偏是否意味着低方差？
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
