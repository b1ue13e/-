---
created: 2026-08-07
type: study
course: "强化学习"
title: "RND (Random Network Distillation)"
topic: "RND (Random Network Distillation)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: concept
status: learning
importance: "B"
tags: [学习, 强化学习]
upstream: ["[[内在奖励与好奇心]]"]
concept: ["RND", "随机网络", "预测误差", "探索"]
sources:
  - "Burda et al., 2018, 'Exploration by Random Network Distillation'"
---
# RND (Random Network Distillation)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`RND 原文`
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
用"预测随机网络输出"的误差作为内在奖励：新状态预测误差大 → 奖励高，激励探索未见状态；已见状态误差小 → 奖励低，自然退火。

## 正式定义 / 公式
固定随机网络 f(x) 与目标网络 f^(x)（训练预测 f）；r_int = || f^(x) − f(x) ||²。状态越新，f^ 预测越差，r_int 越大。

## 最小手算例子
新状态 x_new：f(x)=[0.3, 0.7]，f^ 初训不足输出 [0.1, 0.9]，误差² = (0.2² + 0.2²) = 0.08 → 高内在奖励；
老状态 x_old：f^(x_old) ≈ f(x_old) = [0.5, 0.5]，误差 ≈ 0 → 奖励 ≈ 0。

## 对比与常见错误
- 与 ICM/计数：RND 无需环境动力学模型，仅用随机网络蒸馏，简单稳定。
- 常见错误：目标网络被"记住"所有状态（需足够容量/正则）；把 r_int 当作最终优化目标。

## 闭卷自测
1. RND 如何用随机网络产生探索信号？
2. 为何已访问状态的内在奖励会自然衰减？

## 直觉：用“预测不准”当好奇心
RND 维护两个网络：目标网络（随机固定）对观测出特征，预测网络去拟合它。对“没见过的状态”预测误差大→ intrinsic reward 高→Agent 主动去探索。这样探索驱动由“新颖性”而非外部奖励，能在稀疏奖励环境里自发覆盖状态空间。注意预测误差需归一化防饱和，否则后期探索动力消失。

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
