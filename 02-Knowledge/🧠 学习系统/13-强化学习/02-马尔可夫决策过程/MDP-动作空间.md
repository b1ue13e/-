---
type: study
topic: "MDP-动作空间"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["MDP", "动作空间"]
upstream: ["[[动作空间]]"]
tags: [学习, 强化学习]
---

# MDP-动作空间

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：MDP 五元组
> 前置：[[动作空间]]

## 动机

动作空间 $\mathcal{A}$ 是 MDP 五元组第二个分量，决定 Agent 能如何干预环境；是否依赖状态影响算法实现。

## 正式定义 / 公式

- $\mathcal{A}$：所有可能动作的集合；可依赖状态记为 $\mathcal{A}(s)$。
- **离散动作**：有限集，如网格世界 $\{上,下,左,右\}$。
- **连续动作**：$\mathcal{A}\subset\mathbb{R}^n$，如力矩向量（见 [[连续MDP]]）。

## 最小手算例子

网格世界：$\mathcal{A}=\{N,S,E,W\}$；悬崖路问题中"下"会坠崖（负奖励）。


规模对比：网格世界 |A|=4（N,S,E,W），max_a Q(s,a) 只比 4 个数；连续控制如机械臂 A⊂R²（转向角,油门）乃至 R⁶（六关节力矩），动作不可枚举，Q-learning 的 max 直接失效。
## 对比与常见错误

- **忽略 $\mathcal{A}(s)$ 约束**：某些状态不可行动作需单独建模。
- **混淆动作与状态**：动作是干预，不是状态的一部分。

## 闭卷自测
- MDP 动作空间与阶段 1 的"动作空间"概念有何异同？
- 何为 $\mathcal{A}(s)$？为何需要它？

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
