---
type: study
topic: "Gamma=1"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["折扣", "Gamma=1"]
upstream: ["[[MDP-折扣因子]]"]
tags: [学习, 强化学习]
---

# Gamma=1

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：折扣因子 γ
> 前置：[[MDP-折扣因子]]

## 动机

$\gamma=1$ 让远近奖励同等重要；理解它何时可用、何时发散，是正确选折扣的前提。

## 正式定义 / 公式

- $\gamma=1$：$G_t=\sum_{k} r_{t+k+1}$，未来与现在同等权重。
- **可用**：有限时域 / 回合制（项数有限，不发散）。
- **不可用**：无限时域（级数发散，价值无定义）。

## 最小手算例子

下棋（有限回合）可用 $\gamma=1$，回报即总目数；持续任务则不行。

## 对比与常见错误

- **无限时域设 $\gamma=1$**：回报发散，算法无定义。
- **以为 $\gamma=1$ 总最优**：长期噪声/循环会让学习不稳。

## 闭卷自测
- $\gamma=1$ 在哪种任务下安全？哪种下危险？
- 无限时域用 $\gamma=1$ 会怎样？

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
