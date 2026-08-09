---
created: 2026-08-07
type: study
course: "强化学习"
title: "Dyna-Q与背景规划 (Dyna-Q & Background Planning)"
topic: "Dyna-Q与背景规划 (Dyna-Q & Background Planning)"
stage_moc: "[[🧭 阶段8-模型基与规划]]"
flow: knowledge
kind: algorithm
status: learning
importance: "A"
tags: [学习, 强化学习, 模型基]
upstream: ["[[模型基RL概述]]", "[[Dyna算法]]", "[[Q-Learning算法]]"]
concept: ["Dyna-Q", "背景规划", "优先遍历", "仿真经验"]
sources:
  - "Sutton & Barto Ch.8.2; Peng & Williams 1993 (Dyna-Q)"
---
# Dyna-Q与背景规划 (Dyna-Q & Background Planning)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`Sutton & Barto Ch.8.2`
> 对应阶段：[[🧭 阶段8-模型基与规划|返回阶段页]]

## 动机
Dyna 是"用模型生成仿真经验"的思想，Dyna-Q 是它在**表格型 Q-learning** 上的具体实现。它把所有想象出来的经验都灌进同一个 Q 表——这叫**背景规划（background planning）**：模型在后台持续把"假数据"喂给规划器，无需等待真实交互。朴素 Dyna 随机采样仿真状态，效率低：关键状态很少被抽中。于是有了**优先遍历（prioritized sweeping）**来加速。

## 正式定义 / 公式
表格版 Dyna-Q，每收到一次真实转移 (s,a,r,s')：
1. **直接 RL**：Q(s,a) ← Q(s,a) + α[r + γ max_a' Q(s',a') − Q(s,a)]；同时把模型更新为 Model(s,a) ← (r, s')。
2. **规划 k 次**：随机取一条历史 (s̄,ā)，用 Model 生成 (r̄, s̄')，再做同样的 Q 更新。

优先遍历改法：维护一个按 |ΔQ| 排序的"待更新"优先队列。刚经历真实转移、Q 变化大的状态先更新，并把"指向它的前驱状态"也入队——模型误差沿反向边快速传播，而非随机游走。

## 最小手算例子
GridWorld 起始在左上。真实走一步后 k=5：
- 随机采样：5 次可能全中离目标很远的状态，Q 几乎没动到关键路径。
- 优先遍历：刚更新的状态邻居被排进队列，1 轮就波及通往目标的格子，几轮内最优路径浮现。
同样的交互预算下，优先遍历收敛更快。

## 对比与常见错误
- 与纯 Q-Learning：Dyna-Q 用模型"白嫖"额外更新，样本效率更高。
- 与决策时规划（如 MCTS）：背景规划离线更新值函数；决策时规划在线针对当前状态搜索。
- **常见错误**：模型还没 warmup 就用仿真数据狂更新（此时模型是错的，Q 被带偏）；k 过大让模型误差累积污染 Q。

## 闭卷自测
1. 背景规划与决策时规划（decision-time planning）的核心区别？
2. 优先遍历为何比随机仿真收敛快？它依赖什么额外信息（前驱关系）？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
