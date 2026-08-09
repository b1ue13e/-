---
type: study
topic: "DDPG深度确定性策略梯度(DDPG)"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["DDPG", "深度确定性策略梯度"]
upstream: ["[[Q函数（动作价值函数）]]", "[[经验回放与目标网络]]", "[[策略与策略空间]]", "[[经验回放与目标网络]]"]
tags: [学习, 强化学习]
---

# DDPG深度确定性策略梯度(DDPG)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
Q-Learning 适合离散动作，但连续动作下 argmax_a Q 不可解；DDPG 把 AC 与 DQN 技术结合处理连续控制。

## 正式定义 / 公式
确定性策略 μ_θ(s) 直接输出动作；critic 学 Q_φ(s,a)；更新借鉴 DQN：
- 经验回放存 (s,a,r,s')；
- 目标网络 μ'、Q' 软更新；
- actor 梯度 ∇_θ Q_φ(s, μ_θ(s))；
- 探索靠对动作加噪声（如 OU 过程），而非 ε-greedy。

## 最小手算例子
<!-- NUMEX -->确定性动作 a=μ(s)；探索靠加噪声 a=a+𝒩（OU 过程，σ=0.1）。目标 y=r+γ·Q'(s', μ'(s'))，其中 μ' 为目标策略网络，阻断自举相关性。目标网络软更新 θ'←τθ'+(1−τ)θ，τ=0.005。

MuJoCo 摆杆：μ 输出连续力矩，Q 评估 (s,力矩)，目标网络稳定 Bellman 目标。

## 对比与常见错误
- 与 AC：DDPG 是 off-policy 确定性 AC；与 DQN：借用了回放与目标网络。
- 常见错误：对连续动作用 ε-greedy——噪声更适合连续空间。

## 闭卷自测
1. DDPG 如何把 DQN 技术用到连续动作？
2. 它与标准 AC 的主要区别？
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
