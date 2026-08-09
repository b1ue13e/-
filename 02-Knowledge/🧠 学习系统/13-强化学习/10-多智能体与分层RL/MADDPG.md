---
created: 2026-08-07
type: study
course: "强化学习"
title: "MADDPG (Multi-Agent DDPG)"
topic: "MADDPG (Multi-Agent DDPG)"
stage_moc: "[[🧭 阶段10-多智能体与分层RL]]"
flow: knowledge
kind: concept
status: learning
importance: "A"
tags: [学习, 强化学习]
upstream: ["[[多智能体RL概述]]", "[[DDPG深度确定性策略梯度(DDPG)]]"]
concept: ["MADDPG", "CTDE", "中心化Critic", "连续"]
sources:
  - "Lowe et al., 2017, 'Multi-Agent Actor-Critic for Mixed Cooperative-Competitive'"
---
# MADDPG (Multi-Agent DDPG)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`MADDPG 原文`
> 对应阶段：[[🧭 阶段10-多智能体与分层RL|返回阶段页]]

## 动机
IQL 在连续/协作任务中因非平稳而差。MADDPG 采用 CTDE：训练时 Critic 能看到所有智能体的状态动作（中心化），执行时每个 Actor 只看局部观测（去中心化）。

## 正式定义 / 公式
每个智能体 i 有 Actor π_i(o_i)；中心 Critic Q_i(o_1..o_n, a_1..a_n) 输入联合信息。更新用 DDPG 式，但梯度用中心 Critic。

## 最小手算例子
2 智能体协作推箱：Critic 输入 (o1,o2,a1,a2)，能区分"两人同推"vs"各推各的"，给协同动作更高 Q；
若只用各自 o_i，a1 看不到 a2 是否配合，Q 估计偏。中心化使协作信号进入梯度。

## 对比与常见错误
- 与 IQL/DDPG：多了中心 Critic（训练期）；DDPG 是单智能体版。
- 常见错误：执行期依赖全局观测（违反去中心）；Critic 输入缺某智能体动作。

## 闭卷自测
1. MADDPG 的 CTDE 如何体现？
2. 为何训练期 Critic 要看到所有智能体动作？

## 直觉：给每人对一个批评家，但用全局信息训
MADDPG 是 DDPG 的多智能体版：每个 Agent 有独立 actor，但 critic 训练时“偷看”所有 Agent 的观测与动作（集中训练、分散执行 CTDE）。这样 critic 能考虑到别人的策略、缓解非平稳；执行时只需局部观测。对混合合作/竞争都成立。代价：Agent 数多时 critic 维度爆炸，且需知道对手动作（训练期）。

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
