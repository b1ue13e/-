---
type: study
topic: "贝尔曼-Q期望"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["贝尔曼-Q期望", "贝尔曼期望方程（Q）"]
upstream: ["[[Q函数-公式]]"]
tags: [学习, 强化学习]
---

# 贝尔曼-Q期望

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
Q 也有对应的期望方程，是 SARSA、Actor-Critic 的理论依据。

## 正式定义 / 公式
Q^π(s,a) = Σ_{s'} P(s'|s,a) [ R(s,a,s') + γ Σ_{a'} π(a'|s') Q^π(s',a') ]
第一步固定 a，之后动作由 π 决定，故对内层 a' 按 π 加权。

## 最小手算例子
2 状态：Q(s1,step)=1·[1+0.9·Σ_{a'}π(a'|s2)Q(s2,a')]=1+0.9·0=1。✓

## 对比与常见错误
- 常见错误：内层也写 max_{a'}——那是"最优"方程（Q-learning），期望方程必须用 π 加权。

## 闭卷自测
1. 默写贝尔曼期望方程（Q）。
2. 期望 vs 最优方程在内层动作上的区别？
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
