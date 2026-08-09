---
created: 2026-08-07
type: study
course: "强化学习"
title: "HAC 分层 Actor-Critic (Hierarchical Actor-Critic)"
topic: "HAC 分层 Actor-Critic (Hierarchical Actor-Critic)"
stage_moc: "[[🧭 阶段10-多智能体与分层RL]]"
flow: knowledge
kind: algorithm
status: learning
importance: "B"
tags: [学习, 强化学习, 分层, HAC]
upstream: ["[[分层RL概述与temporal abstraction]]", "[[后见之明经验回放HER]]"]
concept: ["HAC", "显式子目标", "层级HER", "离策略"]
sources:
  - "Levy et al. 2019 (HAC)"
---
# HAC 分层 Actor-Critic (Hierarchical Actor-Critic)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段10-多智能体与分层RL|返回阶段页]]

## 动机
FeUdal 用隐方向，但"子目标不可解释、难调试"。HAC 改为**显式状态子目标（sub-goal = 某状态）**，多层 Actor-Critic 串成链：高层定子目标 g，低层去达成的状态要接近 g。它最大的亮点是**把 HER（后见之明）用到层级上**——即使子目标没达成，也能用实际到达状态重标，解决稀疏奖励。

## 正式定义 / 公式
- 层级：策略 π₁(高层)→子目标 g，π₂(中层)→子子目标，… ，π_L(底层)→动作；各层都是 Actor-Critic。
- **内部奖励**：第 k 层当它给定的子目标被第 k+1 层"达成"（距离 < 阈值）时给 +1，否则 0——把"达成子目标"变成稠密信号。
- **层级 HER**：第 k 层的一条转移 (s, g, s') 若 g 没达成，重标 g' = s'（实际到达），奖励变正。类似地让高层也能从失败中学。
- 离策略（DDDPG 式）训练，样本效率高。

## 最小手算例子
机械臂把方块放到架子第二层：最高层子目标="方块到架子前"，中层="方块抬高到层高"，底层="关节动作"。若底层只把方块抬到一半（没达中层子目标），HAC 把中层子目标重标为"实际半高"→中层这次转移变成功，学到"如何到半高"，逐步拼出完整动作链。

## 对比与常见错误
- 与 FeUdal：HAC 子目标可解释（状态）、配层级 HER；FeUdal 隐方向、无 HER。
- 与 HER：HAC 把 HER 推广到多层级，而非单层。
- **常见错误**：达成阈值设太严→内部奖励几乎为 0；层级过多→梯度/信用在层间稀释。

## 闭卷自测
1. HAC 的"内部奖励"和"层级 HER"分别在解决什么？
2. 相比 FeUdal，HAC 的子目标表示有何优劣？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
