---
created: 2026-08-07
type: study
course: "强化学习"
title: "行为克隆 BC (Behavior Cloning)"
topic: "行为克隆 BC (Behavior Cloning)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: concept
status: learning
importance: "A"
tags: [学习, 强化学习]
upstream: ["[[离线 RL 与模仿学习]]", "[[策略梯度定理与REINFORCE]]"]
concept: ["行为克隆", "监督学习", "专家示范", "分布偏移"]
sources:
  - "Pomerleau 1991 (ALVINN); 经典 IL 教程"
---
# 行为克隆 BC (Behavior Cloning)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`Imitation Learning 教程`
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
没有奖励信号时，能否直接从专家示范 (s,a) 学策略？BC 把 IL 当成监督学习：输入状态、输出专家动作，训练 π_θ(a|s) ≈ π_expert(a|s)。

## 正式定义 / 公式
最小化负对数似然 L = −E_{(s,a)~D}[ log π_θ(a|s) ]，D 为专家轨迹数据集。

## 最小手算例子
专家数据 1000 条 (s,a)，a 为离散 2 类：类1 有 700 条、类2 有 300 条。
BC 学 π 使训练集分类精度高；若验证集新状态 60% 属类2，但训练只见过 30%，BC 在类2 状态易错——暴露分布偏移。

## 对比与常见错误
- 与 DAgger/GAIL：BC 最简单但会"分布偏移"（错误累积）；后两者缓解。
- 常见错误：把 BC 当 RL（它没奖励、不做探索）；忽略状态分布不匹配。

## 闭卷自测
1. BC 本质是哪类学习问题？
2. 什么是 BC 的"分布偏移"？

## 直觉：监督学习视角的最简模仿
BC 把示范 (s,a) 当监督样本，直接学 π(a|s) 近似专家。实现最简单、常作基线。致命弱点：只对“专家访问过的状态”有标签；一旦策略犯错跑到 OOD 状态就无知、且错误会累积（compounding error），因为训练分布≠执行分布。它因此常被 DAgger/GAIL 改进——前者补标签、后者把分布匹配写进奖励。

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
