---
created: 2026-08-07
type: study
course: "强化学习"
title: "DPO (Direct Preference Optimization)"
topic: "DPO (Direct Preference Optimization)"
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
status: learning
importance: "A"
tags: [学习, 强化学习]
upstream: ["[[RLHF-PPO阶段]]", "[[RLHF-PPO阶段]]"]
concept: ["DPO", "偏好优化", "直接策略优化", "无需奖励模型在线"]
sources:
  - "Rafailov et al., 2023, 'Direct Preference Optimization'"
---
# DPO (Direct Preference Optimization)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`RLHF / DPO 原文`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
RLHF 用 PPO 在奖励模型上做 RL，流程复杂、不稳定。DPO 证明：在 Bradley-Terry 偏好模型下，最优策略可写成关于参考策略与偏好数据的闭式，直接用监督式损失优化，免去显式 RL。

## 正式定义 / 公式
损失 L_DPO = −E_{(x,y_w,y_l)}[ log σ( β·(log π_θ(y_w|x) − log π_ref(y_w|x)) − β·(log π_θ(y_l|x) − log π_ref(y_l|x)) ) ]，β 为温度。

## 最小手算例子
偏好对 (y_w 胜 y_l)。设 log π_θ(y_w)=−1.0, log π_ref(y_w)=−1.2；log π_θ(y_l)=−2.0, log π_ref(y_l)=−1.5；β=0.5。
差值 = 0.5·[ (−1.0+1.2) − (−2.0+1.5) ] = 0.5·(0.2 − (−0.5)) = 0.5·0.7 = 0.35。
σ(0.35)=0.586，损失 = −ln0.586 = 0.534。提升 y_w 概率、压低 y_l 即降低损失。

## 对比与常见错误
- 与 RLHF-PPO：DPO 无独立奖励模型在线优化、无 PPO 的 on-policy 采样与 KL 约束工程；等价于在隐式奖励上做梯度。
- 常见错误：忘记 β 的温度作用；用非偏好数据（需成对 y_w / y_l）。

## 闭卷自测
1. DPO 为何无需显式 RL 循环？
2. β 的作用与过大/过小后果？

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
