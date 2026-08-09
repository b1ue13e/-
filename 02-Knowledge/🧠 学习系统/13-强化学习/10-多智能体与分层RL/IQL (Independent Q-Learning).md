---
created: 2026-08-07
type: study
course: "强化学习"
title: "IQL (Independent Q-Learning)"
topic: "IQL (Independent Q-Learning)"
stage_moc: "[[🧭 阶段10-多智能体与分层RL]]"
flow: knowledge
kind: concept
status: learning
importance: "B"
tags: [学习, 强化学习]
upstream: ["[[多智能体RL概述]]", "[[Q-Learning算法]]"]
concept: ["IQL", "独立Q", "非平稳", "基线"]
sources:
  - "Tan 1993 (Multi-Agent RL); 经典 MARL baseline"
---
# IQL (Independent Q-Learning)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`MARL 综述`
> 对应阶段：[[🧭 阶段10-多智能体与分层RL|返回阶段页]]

## 动机
最简单 MARL：每个智能体当成独立单智能体跑 Q-Learning，忽略他人。虽理论不保证（环境非平稳），但实践中常作为强基线。

## 正式定义 / 公式
对每个智能体 i 维护 Q_i(s_i, a_i)，按标准 Q-Learning 更新：Q_i ← Q_i + α[ r_i + γ·max Q_i(s_i',·) − Q_i ]。

## 最小手算例子
两智能体各用 IQL。联合最优在 (a1,a2) 得 1；agent1 单独看 a1 在 agent2 选 a1 时得 0、选 a2 时得 1，于是 agent1 偏好 a1；同理 agent2 偏好 a2，恰收敛到 (a1,a2) 得 1（合作被独立学习"偶然"达成，非保证）。

## 对比与常见错误
- 与 MADDPG：IQL 完全去中心、无中心 Critic；简单但不处理非平稳协作信号。
- 常见错误：期望 IQL 保证收敛（非平稳下不保证）；状态用全局 s 破坏去中心假设。

## 闭卷自测
1. IQL 对每个智能体做了什么简化假设？
2. 为何 IQL 理论上不保证收敛？

## 直觉：先忽略队友、各自学 Q
完全协作 MARL 若把别人的动作塞进自己的 Q 会遇“非平稳性”（别人在变）。IQL 最朴素：每个 Agent 独立跑 Q-learning，把别人当环境一部分，用局部观测。便宜、易并行，但忽略协调、易陷入错误均衡。常作多智能体基线，再上 VDN/QMIX 做价值分解——后者用单调混合网络在保持分散执行的同时学到协调。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
```
