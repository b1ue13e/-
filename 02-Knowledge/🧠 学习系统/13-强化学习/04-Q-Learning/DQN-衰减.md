---
type: study
topic: "DQN-衰减"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["DQN-衰减", "ε-greedy 衰减"]
upstream: ["[[DQN-函数逼近]]", "[[探索与利用]]"]
tags: [学习, 强化学习]
---

# DQN-衰减

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
DQN 行为策略通常是 ε-greedy 探索。固定 ε 难兼顾"早期多探索、后期多利用"——所以用 ε 衰减。

## 正式定义 / 公式
ε_t = max(ε_min, ε_0 · d^t)（指数衰减）或线性降到 ε_min。
前期 ε 大（多随机探索），后期 ε 小（多贪心利用）。

## 最小手算例子
ε 从 1.0 线性降到 0.1（如 10^5 步内）；前期大量随机尝试，后期基本贪心，策略收敛更稳。

## 对比与常见错误
- 与固定 ε：固定 0.1 长期仍随机，难达最优；衰减让后期更确定。
- 常见错误：衰减太快导致探索不足、错过好动作；太慢则训练慢。

## 闭卷自测
1. 为什么 DQN 用 ε 衰减而非固定 ε？
2. 衰减过快/过慢的代价？
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
