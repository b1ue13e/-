---
type: study
topic: "QL-最大化偏差"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["QL-最大化偏差", "maximization bias"]
upstream: ["[[QL-更新]]", "[[Q函数-最优]]"]
tags: [学习, 强化学习]
---

# QL-最大化偏差

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
Q-learning 更新里的 max 操作会系统性"过估计"价值——因为在对噪声估值取最大时，噪声被放大。这叫最大化偏差。

## 正式定义 / 公式
若 Q(s,a) 的估计含零均值噪声 ε，则 E[max_a(Q*(s,a)+ε)] ≥ max_a Q*(s,a)。
即 max 会挑出"噪声恰好为正"的动作，导致高估。

## 最小手算例子
两动作 Q 真值都为 0，但估计含噪声：Q(s,a1)=+0.5, Q(s,a2)=−0.5。max 取 a1 得 0.5 > 0（真值）。
Q-learning 据此认为 a1 更优，实际两者一样——被噪声误导。

## 对比与常见错误
- 与 SARSA：SARSA 用行为策略的 a'（非 max）也会过估计但程度通常更小；DDQN 专门修 Q-learning 的此偏差。
- 常见错误：认为 max 偏差"无害"——在动作多、噪声大时会被显著误导，影响最终策略。

## 闭卷自测
1. 什么是最大化偏差？来源是什么？
2. 哪个算法专门缓解它？
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
