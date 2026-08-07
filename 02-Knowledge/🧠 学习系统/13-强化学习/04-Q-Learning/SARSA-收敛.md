---
type: study
topic: "SARSA-收敛"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["SARSA-收敛", "SARSA 收敛性"]
upstream: ["[[SARSA-更新]]"]
tags: [学习, 强化学习]
---

# SARSA-收敛

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
SARSA 在什么条件下能收敛到"该策略下"的最优？答案是满足 GLIE（贪婪极限最优探索）。

## 正式定义 / 公式
GLIE（Greedy in the Limit with Infinite Exploration）：
- 所有状态-动作对被无限次访问；
- 行为策略随时间趋近贪心。
在此条件下，SARSA 收敛到最优动作价值（对所用的渐进贪心策略而言）。

## 最小手算例子
ε-greedy 取 ε_t = 1/t：保证无限探索（GLIE 第一点）且最终趋近贪心（第二点）→ SARSA 收敛到最优。

## 对比与常见错误
- 常见错误：固定 ε（如恒 0.1）也期望收敛到最优——固定 ε 不满足"极限贪心"，通常只收敛到 ε-贪心策略下的次优。

## 闭卷自测
1. SARSA 收敛需要什么条件？
2. 为什么固定 ε 通常只收敛到次优？
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
