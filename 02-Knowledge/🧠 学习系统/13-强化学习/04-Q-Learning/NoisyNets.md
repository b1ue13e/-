---
type: study
topic: "NoisyNets"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["NoisyNets", "Noisy Networks"]
upstream: ["[[DQN-函数逼近]]", "[[探索与利用]]"]
tags: [学习, 强化学习]
---

# NoisyNets

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
ε-greedy 的探索与"当前状态"无关，且衰减后探索减弱。Noisy Nets 把探索"装进网络参数"：每层加参数化噪声，状态相关的探索、训练末自动减弱。

## 正式定义 / 公式
权重替换为 W = μ + σ ⊙ ε，其中 ε 是随机噪声（每前向采样），μ、σ 是可学习参数。
训练时 σ 被优化，使网络学会"在哪里该有随机性"；推理/部署时可关噪声取确定性。

## 最小手算例子
<!-- NUMEX2 -->NoisyNet：权重 = μ+σ⊙ε（ε 每步重采样），σ 可学习。例 σ 初始 0.1，训练后关键连接 σ→0（确定性）、探索连接 σ 保留。

Noisy DQN 不再用 ε-greedy，仅靠参数噪声探索；训练后期 σ 自动趋小，探索自然衰减。

## 对比与常见错误
- 与 ε-greedy：ε-greedy 与状态无关、需手调衰减；Noisy Nets 状态相关、自动衰减、可端到端学习。
- 常见错误：部署时忘了关噪声——线上应用应取 μ（确定性）以保证稳定。

## 闭卷自测
1. Noisy Nets 如何实现探索？
2. 与 ε-greedy 比有何优势？
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
