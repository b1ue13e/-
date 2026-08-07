---
type: study
topic: "SARSA-同策略"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["SARSA-同策略", "SARSA On-Policy"]
upstream: ["[[SARSA-更新]]", "[[策略-随机性]]"]
tags: [学习, 强化学习]
---

# SARSA-同策略

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
"On-Policy"意味着用来"学习/更新"的策略，和用来"与环境交互"的策略是同一个（如同一个 ε-greedy）。

## 正式定义 / 公式
SARSA 中行为策略 π_b = 目标策略 π（同一个）。更新用 π_b 选出的 a'，因此学到的是"在该探索策略（如 ε-greedy）下的价值"。

## 最小手算例子
若行为策略是 ε-greedy（ε=0.1），SARSA 也评估这个带噪声的策略——它知道有时会因探索而走错，于是学到的 Q 反映了"真实会怎么走"。

## 对比与常见错误
- 与 Q-learning（off-policy）：Q-learning 学的是贪心最优 Q*，不关心行为策略的探索。
- 常见错误：以为 on-policy 就"不能用探索"——行为策略本身可以带探索（ε-greedy），只是学与用同一策略。

## 闭卷自测
1. 什么是 on-policy？SARSA 如何体现？
2. on-policy 与探索是否矛盾？
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
