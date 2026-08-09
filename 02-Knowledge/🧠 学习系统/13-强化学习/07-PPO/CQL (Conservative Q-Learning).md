---
created: 2026-08-07
type: study
course: "强化学习"
title: "CQL (Conservative Q-Learning)"
topic: "CQL (Conservative Q-Learning)"
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
status: learning
importance: "A"
tags: [学习, 强化学习]
upstream: ["[[离线 RL 与模仿学习]]", "[[DQN深度Q网络]]"]
concept: ["离线RL", "保守Q", "分布外", "惩罚"]
sources:
  - "Kumar et al., 2020, 'Conservative Q-Learning for Offline RL'"
---
# CQL (Conservative Q-Learning)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`Offline RL 综述 / CQL 原文`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
离线 RL 用固定数据集训练，标准 Q 学习会对"分布外(OOO)动作"过估计，导致外推误差与危险动作。CQL 在 Q 学习目标上加正则，主动压低 OOD 动作的 Q 值。

## 正式定义 / 公式
在 TD 损失上加正则项 R(θ) = E_{s~D, a~μ}[Q(s,a)] − E_{s~D, a~π_β}[Q(s,a)]，即"拉高数据内、压低数据外"。
总损失 = TD 损失 + α · R(θ)。

## 最小手算例子
数据集含动作 a1,a2：Q(a1)=5（数据内）、Q(a2)=0.2（数据内）；OOD 动作 a3 的 Q(a3)=8（过估计）。
CQL 正则把 Q(a3) 压向低值；若 α=1，目标使 Q(a3) 下降而 Q(a1),Q(a2) 上升。最终选动作时 a3 因 Q 被压低而不再被选中。

## 对比与常见错误
- 与 BCQ/TD3+BC：CQL 直接改 Q 正则，不改动作生成；BCQ 约束动作贴近数据集。
- 常见错误：α 太大使所有 Q 塌成常数、策略退化；α 太小 OOD 过估计仍在。

## 闭卷自测
1. CQL 正则项的直观作用是什么？
2. 为何离线 RL 必须处理 OOD 动作？

## 直觉：CQL 在“Q 值”侧压住 OOD
与 BCQ 相反，CQL 不动作生成，而是给 Q 学习目标加正则：拉高“数据内动作”的 Q、压低“数据外动作”的 Q，使盲目外推的高 Q 被强制降下来。温度 α 是旋钮——太大所有 Q 塌成常数、策略退化；太小 OOD 过估计仍在。CQL 因此常作为离线 RL 的强 baseline，且容易和回报最大化目标解耦调参。

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
