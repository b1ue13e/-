---
created: 2026-08-07
type: study
course: "强化学习"
title: "BCQ (Batch-Constrained Q-learning)"
topic: "BCQ (Batch-Constrained Q-learning)"
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
status: learning
importance: "B"
tags: [学习, 强化学习]
upstream: ["[[离线 RL 与模仿学习]]"]
concept: ["离线RL", "批量约束", "生成动作", "扰动"]
sources:
  - "Fujimoto et al., 2019, 'Off-Policy Deep RL without Exploration'"
---
# BCQ (Batch-Constrained Q-learning)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`Offline RL 综述 / BCQ 原文`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
离线数据集只覆盖部分状态-动作对；对未见动作求值会外推出错。BCQ 限制策略只生成"接近数据集分布"的动作，从源头避免 OOD。

## 正式定义 / 公式
用 VAE 学数据动作分布 G_ω；加一个扰动网络 ξ_φ 在 decoder 输出附近微扰。
策略只从 { a : G_ω(s,a) > 阈值 } 中选 argmax Q，即 a = argmax_{ã∈{decode(z)+ξ}} Q(s, ã)。

## 最小手算例子
数据集动作集中在值 0.3 附近；VAE 生成候选 [0.25, 0.30, 0.35]，扰动后 [0.24, 0.31, 0.36]。
Q 值分别为 [1.2, 3.0, 1.5]，则选 0.31（Q=3.0）。远离数据的动作（如 0.9）被 G_ω 判为低似然而不候选，避免 OOD 高估。

## 对比与常见错误
- 与 CQL：BCQ 在"动作生成侧"约束，CQL 在"Q 值侧"惩罚。
- 常见错误：VAE 过拟合小数据集导致生成候选过少、策略退化为 BC。

## 闭卷自测
1. BCQ 用哪两个网络约束动作？各自作用？
2. BCQ 与 CQL 约束思路的根本差别？

## 直觉：BCQ 在“动作生成”侧堵住 OOD
离线 RL 的危险来自对数据集外动作的 Q 值外推高估。BCQ 用一个 VAE 学“数据动作长什么样”，再只允许策略在“靠近数据分布”的候选动作里挑 argmax Q，从源头避免选到没见过的危险动作。代价是 VAE 过拟合小数据集时候选过少、退化为 BC；扰动网络 ξ 的幅度也要调，太大失去约束、太小退化为单点。

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
