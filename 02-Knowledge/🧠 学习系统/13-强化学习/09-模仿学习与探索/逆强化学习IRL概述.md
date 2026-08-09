---
created: 2026-08-07
type: study
course: "强化学习"
title: "逆强化学习IRL概述 (Inverse RL Overview)"
topic: "逆强化学习IRL概述 (Inverse RL Overview)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: concept
status: learning
importance: "A"
tags: [学习, 强化学习, 模仿学习, IRL]
upstream: ["[[模仿学习概述]]", "[[MDP 与贝尔曼方程]]"]
concept: ["IRL", "奖励反推", "占用度量", "专家最优"]
sources:
  - "Ng & Russell 2000 (IRL); Abbeel & Ng 2004 (Apprenticeship)"
---
# 逆强化学习IRL概述 (Inverse RL Overview)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
有时连"专家怎么做"都难得，但我们知道专家是"最优"的。IRL 反过来：给定专家在 MDP（已知动力学）下的示范，推断专家遵循的**奖励函数 r**。得到 r 后，就能用标准 RL 训练出达到甚至超越专家的策略，且能泛化到未示范状态。

## 正式定义 / 公式
设专家策略 π_E 产生占用度量 ρ_E(s,a)。IRL 求 r 使得在 r 下 π_E 优于其它策略：

  r* = argmax_r [ 奖励让专家"看起来最优" ]，约束如
  E_{ρ_E}[r(s,a)] ≥ E_{ρ_π}[r(s,a)] + ε,  ∀π ≠ π_E

但 IRL **本质病态**：对任意 r，给 r+φ（φ 是任意势函数，满足 φ(s)=γφ(s')−φ(s)）都会产生相同最优策略——即奖励非唯一。因此实际 IRL 加正则（最大熵/特征期望匹配）来挑一个合理解。

## 最小手算例子
网格世界专家总走最短路径到目标。IRL 推断：奖励应在目标格 +10，其余 −1/步。但把奖励全部 +5（每步），最短路径仍最优——IRL 的非唯一性体现于此；最大熵 IRL 用"策略随机性最大化"打破歧义，选最简奖励。

## 对比与常见错误
- 与 BC：IRL 不直接克隆动作，而是学"为什么专家这样做"（奖励），泛化更好。
- 与 GAIL：GAIL 跳过显式 r，直接在占用度量上对抗；IRL 显式求 r 再 RL。
- **常见错误**：忽略奖励非唯一性，误以为 IRL 给出唯一 ground-truth 奖励。

## 闭卷自测
1. IRL 为什么是"病态/非唯一"问题？势函数不变性指什么？
2. IRL 比 BC 好在哪些场景？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
