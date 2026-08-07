---
type: study
topic: "QLvsSARSA-策略"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["QLvsSARSA-策略", "Q-Learning vs SARSA：策略类型"]
upstream: ["[[QL-异策略]]", "[[SARSA-同策略]]"]
tags: [学习, 强化学习]
---

# QLvsSARSA-策略

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
两者最易混淆的一点：学习时的"策略类型"。这决定了它们学到的是"哪种"最优。

## 正式定义 / 公式
- Q-learning：Off-Policy，学贪心最优 π*（不依赖行为策略）。
- SARSA：On-Policy，学行为策略（如 ε-greedy）下的价值。

## 最小手算例子
<!-- NUMEX2 -->更新所用动作不同：Q-learning 目标取 maxₐ'Q(s',a')（ε=0 贪心）；SARSA 用实际下一步 a'∼π(ε=0.1)。同 ε 下二者更新量不同，SARSA 把探索噪声纳入目标。

同一悬崖环境：Q-learning 评估"最优路径"（贴边走，最短但危险）；SARSA 评估"ε-greedy 实际会走的路径"（略远离悬崖，更保守）。

## 对比与常见错误
- 常见错误：认为"两者最终策略一样"——Q-learning 收敛到真正贪心最优；SARSA 收敛到其行为策略下最优（若 ε 不趋 0 则偏保守）。

## 闭卷自测
1. 两者在 on/off-policy 上的区别？
2. 这导致学到的策略有何不同？
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
