---
created: 2026-08-07
type: study
course: "强化学习"
title: "MAPPO (Multi-Agent PPO)"
topic: "MAPPO (Multi-Agent PPO)"
stage_moc: "[[🧭 阶段10-多智能体与分层RL]]"
flow: knowledge
kind: algorithm
status: learning
importance: "A"
tags: [学习, 强化学习, 多智能体, 策略梯度]
upstream: ["[[CTDE范式]]", "[[PPO近端策略优化]]"]
concept: ["MAPPO", "多智能体PPO", "中心化 Critic", "TRPO/PPO"]
sources:
  - "Yu et al. 2021 (MAPPO, the Surprising Effectiveness)"
---
# MAPPO (Multi-Agent PPO)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段10-多智能体与分层RL|返回阶段页]]

## 动机
一个反直觉事实（Yu et al. 2021）：在很多合作 MARL 任务上，简单的 **MAPPO（把 PPO 配上一个中心化 Critic）** 能打过一堆复杂的价值分解算法。MAPPO 几乎是 MARL 的"默认基线"——理解它，就握住了现代合作多智能体的入场券。

## 正式定义 / 公式
- 每个 Agent i 有独立 Actor π_i(a_i|o_i; θ_i)，用 PPO 的 clip 目标更新。
- 一个**中心化 Critic** V(s) 吃全局状态 s（训练期），估计基线/优势；执行期只留 Actor。
- 优势用 GAE 在全局值上算：A_i = GAE(γ,λ; r_global, V(s))。多 Agent 共享全局奖励做信用分配的"粗粒度"，Actor 各自优化。
- 常用技巧：参数共享（同构 Agent 共用 θ_i）、值函数归一化、大 batch。

## 最小手算例子
多智能体粒子环境（MPE）追捕：5 个 Agent 合作围住目标。MAPPO 用全局奖励"目标被围住 +1"训练中心 Critic，各 Agent 的 Actor 据自己观测决定移动；相比 QMIX 需精细值分解，MAPPO 直接靠 PPO 稳定性 + 中心 Critic 就收敛快、稳。

## 对比与常见错误
- 与 QMIX/VDN：MAPPO 是策略梯度系（on-policy、需交互），值分解是 Q-learning 系（可 off-policy）；MAPPO 实现简单、调参少。
- 与 MADDPG：MAPPO 用离散/连续都行、PPO 比 DDPG 稳；MADDPG 是 off-policy 样本效率更高但更脆。
- **常见错误**：中心 Critic 在执行期被误用（应丢弃）；忽略参数共享导致同构 Agent 学不齐；GAE λ 设错。

## 闭卷自测
1. MAPPO 相比单智能体 PPO 改了什么（中心化 Critic 怎么用）？
2. 为何 MAPPO 常比复杂值分解算法更实用？它的主要短板是什么？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
