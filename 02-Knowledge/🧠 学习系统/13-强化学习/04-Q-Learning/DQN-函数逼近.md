---
type: study
topic: "DQN-函数逼近"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["DQN-函数逼近", "DQN 函数逼近"]
upstream: ["[[Q函数-定义]]", "[[局限-维度灾难]]"]
tags: [学习, 强化学习]
---

# DQN-函数逼近

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
表格 Q 在状态/动作空间大时爆内存（维度灾难）。DQN 用神经网络 Q(s,a;θ) 近似 Q 函数，泛化到未见状态。

## 正式定义 / 公式
用神经网络 Q_θ(s, a)（或 Q_θ(s) 输出各动作 Q 值）近似最优动作价值：
Q* (s,a) ≈ Q_θ(s,a)
训练目标：让 Q_θ 逼近 TD 目标 y = r + γ max_{a'} Q_{θ^-}(s', a')。

## 最小手算例子
CartPole：状态是 4 维连续向量，无法建表。DQN 用小型 MLP 输入状态、输出 |A| 个 Q 值，端到端学习。

## 对比与常见错误
- 与表格 Q-learning：表格需枚举状态；DQN 靠网络泛化，但训练更不稳（相关性、非平稳目标）。
- 常见错误：直接把表格 Q-learning 的"每个 (s,a) 独立更新"照搬到 NN——NN 需要批次、稳定目标（见经验回放/目标网络）。

## 闭卷自测
1. 为什么 DQN 需要函数逼近？
2. DQN 用网络近似的是什么？
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
