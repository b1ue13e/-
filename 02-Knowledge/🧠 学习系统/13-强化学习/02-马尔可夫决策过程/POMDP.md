---
type: study
topic: "POMDP"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["POMDP", "部分可观测"]
upstream: ["[[马尔可夫性质]]", "[[MDP-状态空间]]"]
tags: [学习, 强化学习]
---

# POMDP

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：MDP 扩展
> 前置：[[马尔可夫性质]] · [[MDP-状态空间]]

## 动机

真实 Agent 往往看不到真状态（摄像头像素≠状态）。POMDP 是 MDP 的部分可观测推广，是连接"理想 MDP"与"现实感知"的桥梁。

## 正式定义 / 公式

- **POMDP** = MDP + 观测：每步 Agent 收到观测 $o_t\sim O(\cdot\mid s_t,a_{t-1})$，看不到 $s_t$。
- 决策基于**信念状态** $b(s)=Pr(s\mid history)$；等价于在信念空间上做 MDP。

## 最小手算例子

带噪声摄像头的导航：像素为观测；真位置为状态；用 RNN/滤波维护信念后再决策。


量化：若真实状态有 4 种但观测只有 2 种，则必有至少 2 个状态共享同一观测（鸽巢原理），单帧像素无法区分，必须靠历史累积或信念状态 b(s) 来决策。
## 对比与常见错误

- **把观测当状态**：直接拿 $o$ 当 $s$ 会非马尔可夫，学偏。
- **忽视历史**：需用循环网络或粒子滤波维护信念。

## 闭卷自测
- POMDP 相比 MDP 多了什么？
- 为何"观测 $\neq$ 状态"会导致问题？

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
