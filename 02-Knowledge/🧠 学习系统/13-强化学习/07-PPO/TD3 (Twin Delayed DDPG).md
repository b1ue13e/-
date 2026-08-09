---
created: 2026-08-07
type: study
course: "强化学习"
title: "TD3 (Twin Delayed DDPG)"
topic: "TD3 (Twin Delayed DDPG)"
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
status: learning
importance: "A"
tags: [学习, 强化学习]
upstream: ["[[DDPG深度确定性策略梯度(DDPG)]]"]
concept: ["TD3", "双Q网络", "延迟策略更新", "目标策略平滑"]
sources:
  - "Fujimoto et al., 2018, 'Addressing Function Approximation Error in Actor-Critic Iterative Methods'"
---
# TD3 (Twin Delayed DDPG)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`Spinning Up / TD3 原文`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
DDPG 在连续控制上常出现 Q 值过估计、训练抖动。TD3 在 DDPG 上加三个技巧抑制过估计与方差：**双 Q 网络取 min**、**延迟更新策略**、**目标策略平滑**。

## 正式定义 / 公式
两个 Critic：Q_{θ1}, Q_{θ2}。Critic 目标取两者较小值：
y = r + γ · min( Q_{θ1'}(s', ã), Q_{θ2'}(s', ã) )，其中 ã = π_{φ'}(s') + clip(ε, −c, c)，ε ~ N(0, σ)。
Actor（策略网络）每 d 步才更新一次（延迟），Critic 正常更新。

## 最小手算例子
设 Q_{θ1'}(s',·)=3.0, Q_{θ2'}(s',·)=1.0（过估计使 Q1' 偏高）。则 min=1.0，目标 y = −1 + 0.99×1.0 = −0.01。
若只用单个 Q（如 DDPG）则 y = −1 + 0.99×3.0 = 1.97，明显被高估。双 Q 把目标从 1.97 拉回 −0.01。

## 对比与常见错误
- 与 DDPG：TD3 = DDPG + 三技巧，同框架更稳定，不是新范式。
- 常见错误：把 min 误写成 max；或忘记延迟更新，使策略随 Critic 噪声抖动。

## 闭卷自测
1. TD3 为何用两个 Q 网络并取 min？
2. 目标策略平滑怎么做？加噪为何能降方差？

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
