---
created: 2026-08-07
type: study
course: "强化学习"
title: "CTDE范式 (Centralized Training Decentralized Execution)"
topic: "CTDE范式 (Centralized Training Decentralized Execution)"
stage_moc: "[[🧭 阶段10-多智能体与分层RL]]"
flow: knowledge
kind: concept
status: learning
importance: "A"
tags: [学习, 强化学习, 多智能体, CTDE]
upstream: ["[[多智能体RL概述]]", "[[多智能体任务分类与合作范式]]"]
concept: ["CTDE", "中心化 Critic", "去中心化执行", "非平稳性"]
sources:
  - "Foerster et al. 2016 (COMA); Lowe et al. 2017 (MADDPG); Oliehoek et al. 2008 (Dec-POMDP)"
---
# CTDE范式 (Centralized Training Decentralized Execution)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段10-多智能体与分层RL|返回阶段页]]

## 动机
多智能体合作里有个根本矛盾：**执行时每个智能体只有局部观测（必须去中心化），但训练时若能拿到全局信息（谁在哪儿、彼此意图）会学得快得多**。CTDE（Centralized Training, Decentralized Execution）就是解：训练用全局信息帮每个 Agent 学一个**只看局部的策略**，部署时各 Agent 独立跑、无需通信。

## 正式定义 / 公式
- **训练**：Critic 可访问联合观测 o=(o₁..oₙ) 与联合动作 a=(a₁..aₙ)，估计联合 Q 或优势；Actor π_i(a_i|o_i) 只吃自己的 o_i。
- **执行**：只保留 Actor，按 π_i(a_i|o_i) 各自决策，无中心节点。
- 关键约束（单调性/IQL 类）：训练时利用全局，但要保证"对个体策略的局部贪婪"与"全局最优"一致，否则训练/执行不一致（QMIX 用单调性保证）。

## 最小手算例子
足球多智能体：训练时中心 Critic 看到所有球员位置，能判断"传球是否明智"；但比赛中每个球员只能看自己视野。CTDE 让每个球员在训练中借助全局语境学到"局部观测→好动作"的映射，比赛时无需实时共享全图。

## 对比与常见错误
- 与 IQL（完全独立）：IQL 训练也不共享信息，但无法利用全局 credit assignment，协作任务易失败；CTDE 训练期用全局做信用分配。
- 与集中式执行：集中式要求部署也有中心，通信成本高、易单点失败；CTDE 避免。
- **常见错误**：Critic 用了全局但在执行期偷偷依赖全局→部署崩；或忽略单调性导致训练/执行目标错位。

## 闭卷自测
1. CTDE 的"训练"与"执行"阶段信息权限有何不同？为何这样设计？
2. 为什么需要"单调性"之类约束来连接中心训练与去中心执行？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
