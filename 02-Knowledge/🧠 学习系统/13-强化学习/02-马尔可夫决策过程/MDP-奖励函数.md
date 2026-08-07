---
type: study
topic: "MDP-奖励函数"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["MDP", "奖励函数"]
upstream: ["[[奖励函数]]", "[[MDP-状态空间]]"]
tags: [学习, 强化学习]
---

# MDP-奖励函数

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：MDP 五元组
> 前置：[[奖励函数]] · [[MDP-状态空间]]

## 动机

奖励函数 $R$ 是 MDP 五元组中定义"学习目标"的分量；它把"好行为"编码成标量信号。

## 正式定义 / 公式

- 期望形式：$R(s,a)=\mathbb{E}[R_{t+1}\mid S_t=s,A_t=a]$，或 $R(s,a,s')=\mathbb{E}[R_{t+1}\mid s,a,s']$。
- 与阶段 1 [[奖励函数]] 一致，只是现在明确处于 MDP 框架（依赖 $s,a$）。
- 奖励塑造（reward shaping）常在此设计（见 [[奖励设计与环境工程]]）。

## 最小手算例子

迷宫：每步 −1（鼓励快），到达终点 +10，撞墙 −5。

## 对比与常见错误

- **奖励 $\neq$ 回报**：奖励是单步，回报是折扣累积。
- **奖励黑客**：错误塑造会引出非预期最优行为。

## 闭卷自测
- MDP 的 $R(s,a)$ 与阶段 1 的奖励函数是什么关系？
- 为何设计奖励要小心"奖励黑客"？

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 相关下游知识

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```
