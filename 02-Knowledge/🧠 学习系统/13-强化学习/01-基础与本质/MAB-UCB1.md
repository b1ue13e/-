---
type: study
topic: "MAB-UCB1"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["MAB", "UCB1"]
upstream: ["[[MAB-问题定义]]", "[[UCB算法]]"]
tags: [学习, 强化学习]
---

# MAB-UCB1

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：多臂老虎机
> 前置：[[MAB-问题定义]] · [[UCB算法]]

## 动机

UCB1 是老虎机场景下 UCB 的最经典实例化，给出可证明的次线性遗憾上界。

## 正式定义 / 公式

- 先每臂各拉 1 次初始化。
- 第 $t$ 步选 $A_t=\arg\max_a\left[\hat Q_t(a)+\sqrt{2\ln t/N_t(a)}\right]$。
- 观测奖励并更新 $\hat Q,N$。

## 最小手算例子

对奖励有界 $[0,1]$，UCB1 的累计遗憾以高概率 $O(\sqrt{kt\ln t})$，远优于固定 $\varepsilon$ 的 $O(T)$。

## 对比与常见错误

- **初始化不全**：跳过"每臂先 1 次"会除零或偏置。
- **照搬连续奖励**：UCB1 证明假设有界奖励，未归一化时需先缩放。

## 闭卷自测
- UCB1 与通用 UCB 的关系？
- 为何必须先每臂初始化一次？

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
