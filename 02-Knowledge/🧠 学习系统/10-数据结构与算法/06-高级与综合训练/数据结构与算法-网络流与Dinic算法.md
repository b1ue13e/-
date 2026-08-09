---
title: "数据结构与算法-网络流与Dinic算法"
type: study
topic: "网络流与Dinic算法"
course: "数据结构与算法"
created: 2026-08-06
updated: 2026-08-07
status: completed
upstream:
  - "[[数据结构与算法-内存指针与数据结构底层形态]]"
stage_moc: "[[🧭 阶段6-高级与综合训练]]"
flow: knowledge
kind: concept
difficulty: advanced
sources:
  - title: "MIT 6.006 Introduction to Algorithms (Spring 2020)"
    url: "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
    locator: "Network Flow and Dinic's Algorithm"
    source_type: "open-textbook"
    verified_at: "2026-08-07"
concept:
  - "网络流"
  - "最大流最小割定理"
  - "Dinic算法"
  - "残量网络与增广路"
tags:
  - 学习
  - 数据结构与算法
  - 网络流
---

# 数据结构与算法-网络流与Dinic算法

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🧭 阶段6-高级与综合训练]]  
> **前置知识**：[[数据结构与算法-内存指针与数据结构底层形态]]

---

## 💡 问题动机与直观解析

流网络 (Flow Network) $G = (V, E, c)$ 是一个有向图，其中每条边 $(u, v)$ 具有非负的容量 $c(u, v)$。

网络流模型在水管流量输送、油气管道运输、交通流量控制、二分图最大匹配中是运筹优化的顶峰工具。

最核心问题是：从源点 (Source $s$) 到汇点 (Sink $t$)，在不超过所有边容量限制与满足**流量守恒 (Flow Conservation)** 的前提下，能够输送的**最大流量 (Max Flow)** 是多少？

---

## 📐 算法原理与最大流最小割定理

### 1. 核心数学概念

- **残量网络 (Residual Network $G_f$)**：由包含残余容量 $c_f(u, v) = c(u, v) - f(u, v)$ 的边构成的网络。
- **反向边 (Reverse Edge)**：为了提供“反悔机制”，每建立一条容量为 $c$ 的正向边，必须建立一条初始容量为 $0$ 的反向边。
- **增广路 (Augmenting Path)**：残量网络中从 $s$ 到 $t$ 的一条简单路径。

### 2. 最大流最小割定理 (Max-Flow Min-Cut Theorem)

**定理**：在一个流网络中，以下三个条件完全等价：
1. 流 $f$ 是网络中的最大流。
2. 残量网络 $G_f$ 中不存在任何从 $s$ 到 $t$ 的增广路。
3. 最大流的值等于网络中某个割 $(S, T)$ 的**最小割容量 (Capacity of Min-Cut)**。

---

## 💻 Dinic 算法机制与复杂度

Dinic 算法通过以下两大机制将 Ford-Fulkerson 的开销大幅优化至 $\mathcal{O}(|V|^2 |E|)$（在二分图最大匹配场景中更是低至 $\mathcal{O}(|E| \sqrt{|V|})$）：

1. **BFS 分层图 (Level Graph)**：构造 $s$ 到各节点的短距离分层，只沿着 $level[v] = level[u] + 1$ 的边进行增广，杜绝环路无效探索。
2. **DFS 多路增广与当前弧优化 (Current Arc Optimization)**：单次 DFS 沿着分层图同时推推送多路流量，并记录每个节点当前探索到了哪条边。

---

## 📝 检索练习与自测题

1. **思考题**：在网络流反向边的设计中，为什么当正向边推送了流量 $f$ 时，反向边的残余容量需要增加 $f$？（给予后续增广路“推回流量/反悔”的能力）。

---

## 🃏 Anki 卡片

- Q: 最大流最小割定理 (Max-Flow Min-Cut Theorem) 的核心结论是什么？
- A: 流网络中从源点 $s$ 到汇点 $t$ 的最大流量，数值上严格等于切断 $s$ 与 $t$ 连通性所需撤销边的最小容量和（最小割）。

---

## 🔗 学完后可以完成

### 🎯 对应实战作业 (点击直达)

```dataview
LIST FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
