---
type: study
topic: "Gamma=0"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["折扣", "Gamma=0"]
upstream: ["[[MDP-折扣因子]]"]
tags: [学习, 强化学习]
---

# Gamma=0

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：折扣因子 γ
> 前置：[[MDP-折扣因子]]

## 动机

$\gamma=0$ 是折扣因子的极端：只看眼前。它是理解折扣作用的"对照组"。

## 正式定义 / 公式

- $\gamma=0$ 时 $G_t=r_{t+1}$：只优化下一步即时奖励，完全不顾未来。
- 对应**贪心策略**：每步选即时收益最高的动作。

## 最小手算例子

贪心走迷宫：每步选"离终点欧氏距离最近"的动作，可能卡在局部凹坑。


算一笔：三步奖励 [5,3,10]，γ=0 时 G=5+0·3+0²·10=5（只取第一步）；若 γ=0.9 则 G=5+0.9·3+0.81·10=15.8。γ=0 把后两步共 13 分收益全丢掉，故只看眼前。
## 对比与常见错误

- **以为贪心总好**：局部最优 $\neq$ 全局最优；迷宫/长程任务必失败。
- **与 $\gamma\to0$ 混淆**：极限行为类似，但 $\gamma=0$ 严格只取一步。

## 闭卷自测
- $\gamma=0$ 时回报等于什么？
- 为何纯贪心常得不到最优策略？

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
