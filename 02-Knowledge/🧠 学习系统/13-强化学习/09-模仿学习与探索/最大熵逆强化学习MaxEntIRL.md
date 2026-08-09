---
created: 2026-08-07
type: study
course: "强化学习"
title: "最大熵逆强化学习 (MaxEnt IRL)"
topic: "最大熵逆强化学习 (MaxEnt IRL)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: algorithm
status: learning
importance: "B"
tags: [学习, 强化学习, IRL, 最大熵]
upstream: ["[[逆强化学习IRL概述]]", "[[V函数（状态价值函数）]]"]
concept: ["最大熵", "特征期望", "软最优", "配分函数"]
sources:
  - "Ziebart et al. 2008 (MaxEnt IRL)"
---
# 最大熵逆强化学习 (MaxEnt IRL)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
朴素 IRL 用"硬最优"假设（专家严格比其他策略好 ε），对噪声/次优示范很脆。最大熵 IRL 改为假设：**专家在奖励 r 下做"软最优"——在所有能解释示范的奖励中，选让轨迹分布最均匀（熵最大）的那个**，从而自然地容忍随机性并打破奖励歧义。

## 正式定义 / 公式
给定特征 φ(s,a)，轨迹 τ 的奖励为 Σ φ(s,a)。策略的分布按指数族：

  p(τ | r) = (1/Z) exp( Σ_t r(s_t,a_t) ) = (1/Z) exp( Σ_t θᵀφ(s_t,a_t) )

最大熵原则下，最优奖励参数 θ 使专家特征期望等于模型期望：

  E_{p_E}[φ] = E_{p(·|θ)}[φ]

通过对 θ 的梯度上升（梯度=专家特征期望 − 当前模型特征期望）求解；E 用软值迭代（soft value iteration）计算。

## 最小手算例子
自动驾驶变道示范有随机性。MaxEnt IRL 学到奖励后，不仅复现专家轨迹，还能生成"同样合理"的替代变道方式（熵高），而硬 IRL 会强行把不唯一奖励压成单一解、对示范噪声过拟合。

## 对比与常见错误
- 与朴素 IRL：软最优更鲁棒、输出概率策略；朴素 IRL 对次优数据敏感。
- 与 GAIL：MaxEnt IRL 显式求 r 再 RL；GAIL 直接对抗占用度量（AIRL 才把二者统一）。
- **常见错误**：用普通值迭代而非 soft value iteration 算期望特征 → 违背最大熵假设。

## 闭卷自测
1. 最大熵正则如何"打破" IRL 的奖励非唯一性？
2. MaxEnt IRL 的梯度等于什么两项之差？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
