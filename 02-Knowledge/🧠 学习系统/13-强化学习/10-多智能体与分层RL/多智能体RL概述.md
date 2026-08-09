---
created: 2026-08-07
type: study
course: "强化学习"
title: "多智能体RL概述 (MARL)"
topic: "多智能体RL概述 (MARL)"
stage_moc: "[[🧭 阶段10-多智能体与分层RL]]"
flow: knowledge
kind: concept
status: learning
importance: "A"
tags: [学习, 强化学习]
upstream: ["[[MDP 与贝尔曼方程]]"]
concept: ["MARL", "去中心化", "合作", "博弈"]
sources:
  - "Busoniu et al. 2008 (MARL survey); Oroojlooy & Hajinezhad 2023"
---
# 多智能体RL概述 (MARL)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`MARL 综述`
> 对应阶段：[[🧭 阶段10-多智能体与分层RL|返回阶段页]]

## 动机
单智能体 MDP 扩展到多智能体：状态受所有智能体动作影响，环境对其他智能体是非平稳的。MARL 研究如何在这种环境下协同/竞争地学习。

## 正式定义 / 公式
多智能体 MDP（Dec-POMDP）：联合动作 A = × A_i，转移 P(s'|s, a_1..a_n)，每智能体有局部观测 o_i。目标可为联合回报 Σ_i r_i（合作）或各自（竞争）。

## 最小手算例子
两智能体各 2 动作，联合动作 4 种：(a1,a1)=0, (a1,a2)=1, (a2,a1)=1, (a2,a2)=−1。
合作目标 max 联合回报 → 选 (a1,a2) 或 (a2,a1) 得 1；若各自自私都选 a2 得 −1（囚徒困境式）。

## 对比与常见错误
- 与单智能体 MDP：非平稳性（对手也在学）是核心难点；需中心化训练-去中心化执行（CTDE）。
- 常见错误：忽略非平稳性直接套单智能体算法；把对手当固定环境。

## 闭卷自测
1. MARL 相比单智能体 MDP 的核心难点？
2. CTDE 是什么、解决什么？

## 直觉：多智能体带来“非平稳”与“通信”两个新问题
单智能体的环境是静态的；多智能体里别的 Agent 也在学，环境对你而言非平稳，朴素独立学习易震荡。主线分三：完全协作（值分解 QMIX）、完全竞争（Self-Play/Minimax）、混合（MADDPG）。还有通信（共享/显式消息）与奖励分配（credit assignment）两个横切难题——前者决定信息流、后者决定怎么把团队奖励分给个体。

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
