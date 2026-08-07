---
type: study
topic: "MDP-折扣因子"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["MDP", "折扣因子"]
upstream: ["[[奖励函数]]"]
tags: [学习, 强化学习]
---

# MDP-折扣因子

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：MDP 五元组
> 前置：[[奖励函数]]

## 动机

折扣因子 $\gamma\in[0,1]$ 是 MDP 第五个分量，决定"多看重未来"；它让无限时域的回报收敛，并体现决策者的耐心。

## 正式定义 / 公式

- 回报 $G_t=\sum_{k=0}^{\infty}\gamma^k r_{t+k+1}$。
- $\gamma\to0$：近视、只管眼前；$\gamma\to1$：重视长远，但方差大、需 $\gamma<1$ 保证无限时域收敛。

## 最小手算例子

$\gamma=0.9$ 时第 10 步奖励权重仅 $0.9^{10}\approx0.35$；$\gamma=0.99$ 时仍有 $0.90$。

## 对比与常见错误

- **$\gamma=1$ 用于无限时域**：回报可能发散，须改用有限时域或平均奖励。
- **$\gamma$ 过大**：学习慢、方差大、易发散。

## 闭卷自测
- 为何无限时域必须用 $\gamma<1$？
- $\gamma$ 大小分别带来什么利弊？

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
