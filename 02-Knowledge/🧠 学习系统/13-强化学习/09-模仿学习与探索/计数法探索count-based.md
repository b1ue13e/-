---
created: 2026-08-07
type: study
course: "强化学习"
title: "计数法探索 (Count-based Exploration)"
topic: "计数法探索 (Count-based Exploration)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: algorithm
status: learning
importance: "B"
tags: [学习, 强化学习, 探索, 计数]
upstream: ["[[探索与利用基础]]", "[[内在奖励与好奇心]]"]
concept: ["count-based", "伪计数", "内在奖励", "访问计数"]
sources:
  - "Bellemare et al. 2016 (Unifying Count-based Exploration); Strehl & Littman 2008"
---
# 计数法探索 (Count-based Exploration)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
最朴素的探索："去访问次数少的状态"。表格任务里这直接可数；但深度 RL 状态是高维连续的，几乎不会重复访问同一状态，朴素计数恒为 1、失效。于是有了**伪计数（pseudo-count）**：用密度模型把"邻近状态"也算作"访问过"，给没见过的区域注入内在奖励。

## 正式定义 / 公式
内在奖励正比于访问"新奇度"：

  r_int(s,a) = β / sqrt(N(s,a))      （表格）
  r_int(s) = β · (ρ̃(s))^{−1/2} − β  （伪计数，ρ̃ 由密度模型得到）

伪计数通过预测模型 p(s) 在见到 s 前后的变化近似：Ñ(s) ≈ p(s)(1−p(s))/|∇p(s)|。密度模型可以是 PixelCNN、哈希、或能量模型。

## 最小手算例子
迷宫里某条走廊只走过 1 次，N=1 → 内在奖励大，智能体被吸引再去探；走过 100 次的房间 N 大 → 奖励≈0，智能体转向别处。伪计数让"颜色相近的像素画面"共享计数，避免"每个画面都算新"的尴尬。

## 对比与常见错误
- 与 RND/ICM（预测误差法）：计数法靠密度，预测误差法靠"学不会的程度"，本质都衡量新奇度但机制不同。
- 与 ε-贪婪：计数法是**定向、状态感知**的探索，ε-贪婪是盲目随机。
- **常见错误**：密度模型过强→所有状态都被判"见过"，伪计数塌缩；过弱→全算新，乱逛。

## 闭卷自测
1. 为何高维连续状态下朴素计数失效？伪计数靠什么近似"访问次数"？
2. 计数法探索与 RND 的新奇度信号有何异同？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
