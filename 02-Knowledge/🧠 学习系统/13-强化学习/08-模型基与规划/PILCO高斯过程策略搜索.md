---
created: 2026-08-07
type: study
course: "强化学习"
title: "PILCO 高斯过程策略搜索 (PILCO)"
topic: "PILCO 高斯过程策略搜索 (PILCO)"
stage_moc: "[[🧭 阶段8-模型基与规划]]"
flow: knowledge
kind: algorithm
status: learning
importance: "B"
tags: [学习, 强化学习, 模型基, 高斯过程]
upstream: ["[[环境动态模型学习]]", "[[模型不确定性与贝叶斯模型]]"]
concept: ["PILCO", "高斯过程", "解析梯度", "样本效率"]
sources:
  - "Deisenroth & Rasmussen 2011 (PILCO)"
---
# PILCO 高斯过程策略搜索 (PILCO)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段8-模型基与规划|返回阶段页]]

## 动机
PILCO 是"极致样本效率"的标杆：用一个**高斯过程（GP）动力学模型**，把"长期期望回报"对策略参数的梯度**解析地**算出来，几十条真实数据就能学会摆杆平衡。它的核心是把不确定性**沿轨迹传播**，主动避开模型不确信的区域。

## 正式定义 / 公式
- 动力学：p(s_{t+1}|s_t,a_t) 由 GP 拟合，预测为高斯 N(μ, Σ)，其中 Σ 来自 GP 后验方差。
- 策略：参数化 π_ψ(a|s)（如带随机扰动的线性/ RBF 网络）。
- 目标：J(ψ)=Σ_t E_{s_t}[r(s_t)]，其中 s_t 的分布由 GP 模型+策略**逐层传播**（每一步都保留方差，得到随机轨迹分布）。
- 优化：对 ψ 求解析梯度 ∇_ψ J（利用高斯积分的可解析性），用梯度上升更新 ψ。

## 最小手算例子
CartPole：PILCO 用约 20 条真实轨迹（每条几秒）训练 GP，再解析优化策略，约十几轮真实交互即平衡。对比无模型 PPO 需数百万步——样本效率差 3~4 个数量级。代价是 GP 在状态维度高时计算昂贵。

## 对比与常见错误
- 与 PETS：都用概率模型+不确定性；PILCO 用 GP+解析梯度策略搜索，PETS 用 NN 集成+CEM 控制。
- 与 MBPO：PILCO 显式传播方差做保守优化；MBPO 用集成截断。
- **常见错误**：把 PILCO 的 GP 直接套到高维像素观测 → 维度灾难；它需要低维状态（常配状态重建）。

## 闭卷自测
1. PILCO 为什么能"解析地"求策略梯度？它依赖模型的什么性质？
2. 不确定性沿轨迹传播发挥了什么作用？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
