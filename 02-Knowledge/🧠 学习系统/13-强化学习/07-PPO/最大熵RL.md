---
created: 2026-08-07
type: study
course: "强化学习"
title: "最大熵RL (Maximum Entropy RL)"
topic: "最大熵RL (Maximum Entropy RL)"
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
status: learning
importance: "B"
tags: [学习, 强化学习]
upstream: ["[[策略梯度定理与REINFORCE]]"]
concept: ["最大熵", "熵正则", "SAC", "softmax 策略"]
sources:
  - "Ziebart 2010 (MaxEnt IRL); Haarnoja et al., 2018 (SAC)"
---
# 最大熵RL (Maximum Entropy RL)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`Spinning Up / SAC 原文`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
标准 RL 只最大化期望回报，学出的策略可能脆弱、探索不足。最大熵 RL 在目标里加熵项：在拿到高回报的同时尽量随机，提升鲁棒性与探索。

## 正式定义 / 公式
目标 J(π) = Σ_t E_{(s_t,a_t)~π}[ r(s_t,a_t) + α · H(π(·|s_t)) ]，α ≥ 0 为温度。
最优策略呈 softmax 形式：π*(a|s) ∝ exp( Q*(s,a) / α )。

## 最小手算例子
两动作 Q=[2, 1]，α=1。归一化分母 Z = e^2 + e^1 = 7.389 + 2.718 = 10.107。
π(a1)=e^2 / Z = 0.731，π(a2)=e^1 / Z = 0.269。
熵 H = −(0.731·ln0.731 + 0.269·ln0.269) = 0.557。相比 argmax 策略（π=[1,0], 熵=0），最大熵策略保留了探索。

## 对比与常见错误
- 与标准策略梯度：多一个熵奖励项，梯度多一项 α·∇H。
- 常见错误：α 太大策略退化为接近均匀、回报崩；α 太小退化为确定性。

## 闭卷自测
1. 最大熵目标相比标准目标多了什么？温度 α 的作用？
2. α→0 与 α→∞ 分别得到什么策略？

## 直觉：把“随机性”写进目标本身
标准 RL 只追回报，学出的策略脆、易过拟合单一模式。最大熵 RL 在目标里加 α·H(π)，让策略“在拿到高回报的同时尽量随机”——既保探索又提鲁棒。最优策略呈 softmax π*(a|s)∝exp(Q/α)：α→0 退化确定性，α→∞ 退化均匀随机。SAC 是最大熵 RL 的代表，熵系数本身也常自适应调节。

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
