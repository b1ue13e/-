---
created: 2026-08-07
type: study
course: "强化学习"
title: "值分解 VDN (Value Decomposition Networks)"
topic: "值分解 VDN (Value Decomposition Networks)"
stage_moc: "[[🧭 阶段10-多智能体与分层RL]]"
flow: knowledge
kind: algorithm
status: learning
importance: "B"
tags: [学习, 强化学习, 多智能体, 值分解]
upstream: ["[[CTDE范式]]", "[[多智能体任务分类与合作范式]]"]
concept: ["VDN", "加性值分解", "IQL", "信用分配"]
sources:
  - "Sunehag et al. 2017 (VDN)"
---
# 值分解 VDN (Value Decomposition Networks)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段10-多智能体与分层RL|返回阶段页]]

## 动机
合作多智能体里，全局 Q(s,a₁..aₙ) 随 Agent 数指数爆炸。VDN 提出一个极简但有效的假设：**联合 Q 可拆成每个 Agent 局部 Q 之和**。这样既能中心化训练（用全局奖励算 TD 误差），又能去中心化执行（各 Agent 只看自己的 Q_i 贪婪选动作），是值分解家族的开山之作。

## 正式定义 / 公式
加性分解：

  Q_tot(s, a₁..aₙ) = Σ_i Q_i(s, a_i; θ_i)

训练：用全局奖励 r 与联合 TD 目标更新 Σ_i Q_i；因加法对 a_i 分离，执行时每个 Agent i 可直接 argmax_{a_i} Q_i(s,a_i)。参数 θ_i 各 Agent 独立、可并行。

## 最小手算例子
两 Agent 合作搬箱子，全局奖励只在两人同时到位时 +1。VDN 把 Q_tot 拆成 Q₁+Q₂：训练时全局 +1 的梯度同时提升 Q₁、Q₂ 关于各自动作的值，慢慢学会"各自走向正确位置"。执行时两人只看自己的 Q 贪婪走，无需通信。

## 对比与常见错误
- 与 IQL：IQL 没有 Q_tot 约束，各 Q_i 独立学、无全局信用分配；VDN 通过加性约束隐式做信用分配。
- 与 QMIX：QMIX 用混合网络做**单调**非线性组合（表达能力更强），VDN 只是纯加法（最弱但最稳）。
- **常见错误**：在非加性可分解的任务上硬用 VDN→表达力不足、次优；Agent 数极大时 Q_i 仍需各自网络规模够。

## 闭卷自测
1. VDN 对联合 Q 做了什么关键假设？它如何实现"中心训练、去中心执行"？
2. VDN 相比 IQL 多了什么、相比 QMIX 少了什么？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
