---
type: study
topic: "RL基础-序列决策"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["RL基础", "序列决策", "马尔可夫性"]
upstream: ["[[状态空间]]", "[[动作空间]]"]
tags: [学习, 强化学习]
---

# RL基础-序列决策

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：RL概览
> 前置：[[状态空间]] · [[动作空间]]

## 动机

RL 不是单步决策，而是"序列决策"：当前选择影响未来状态，从而影响未来可做的选择与收益。

## 正式定义 / 公式

- **序列决策**：在状态序列 $s_0,a_0,r_1,s_1,\dots$ 中，逐时刻选动作以最大化累积回报。
- **马尔可夫性**（此处初识）：最优决策只依赖当前状态，使问题可分解（阶段 2 严格化）。
- 与单步预测区别：单步只看当前输入，序列决策要考虑长远后果。

## 最小手算例子

投资：今天买/卖影响明天持仓与收益，不能只看单日涨跌。

## 对比与常见错误

- **近视决策**：只优化即时奖励忽略长远（需折扣回报纠偏）。
- **忽略状态转移**：把序列当独立样本，丢失因果。

## 闭卷自测
- 序列决策与单步预测的根本区别？
- 马尔可夫性如何简化序列决策？

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
