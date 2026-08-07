---
type: study
topic: "MDP-状态空间"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["MDP", "状态空间"]
upstream: ["[[状态空间]]"]
tags: [学习, 强化学习]
---

# MDP-状态空间

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：MDP 五元组
> 前置：[[状态空间]]

## 动机

状态空间 $\mathcal{S}$ 是 MDP 五元组的第一个分量，也是"智能体感知到的世界"在 MDP 框架下的精确落点。

## 正式定义 / 公式

- **MDP 五元组** $(\mathcal{S},\mathcal{A},P,R,\gamma)$；其中 $\mathcal{S}$ 为所有可能状态的集合。
- 在 MDP 中，状态必须满足**马尔可夫性**：足以预测未来，无需更早历史。
- 离散 MDP：$\mathcal{S}$ 有限或可数；连续 MDP：$\mathcal{S}\subset\mathbb{R}^n$。

## 最小手算例子

$4\times4$ 网格世界：$\mathcal{S}=\{1,\dots,16\}$（含终止格）。状态就是格子编号。

## 对比与常见错误

- **状态 $\neq$ 观测**：POMDP 中观测 $o$ 不等于 $s$（见 [[POMDP]]）。
- **状态不满足马尔可夫性**：信息不足时需把历史拼入状态（见 [[状态设计]]）。

## 闭卷自测
- 写出 MDP 五元组。
- MDP 中状态必须满足什么性质？不满足会怎样？

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
