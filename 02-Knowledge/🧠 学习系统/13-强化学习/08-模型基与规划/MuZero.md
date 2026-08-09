---
created: 2026-08-07
type: study
course: "强化学习"
title: "MuZero"
topic: "MuZero"
stage_moc: "[[🧭 阶段8-模型基与规划]]"
flow: knowledge
kind: concept
status: learning
importance: "B"
tags: [学习, 强化学习]
upstream: ["[[Dyna算法]]", "[[蒙特卡洛方法]]"]
concept: ["MuZero", "隐含状态", "规划树", "无模型动态"]
sources:
  - "Schrittwieser et al., 2020, 'Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model'"
---
# MuZero

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`MuZero 原文`
> 对应阶段：[[🧭 阶段8-模型基与规划|返回阶段页]]

## 动机
AlphaZero 需已知环境规则（棋类），无法用于未知环境。MuZero 不学显式状态转移，而学一个"隐含状态"的动力学 + 价值/策略头，仅用返回信号在隐含空间做 MCTS 规划。

## 正式定义 / 公式
表征 h(s)→h_0；动态 g(h_k, a_k)→(h_{k+1}, r_k)；策略 p(h_k)、价值 v(h_k)。规划在序列 (h, a, r) 上用 MCTS，目标是 max 累积回报。

## 最小手算例子
在 Atari 上 MuZero 用同一套架构在 57 款游戏达到超人；示意：每步做 800 次 MCTS 仿真，选访问最多动作。隐含状态维度 256，避免显式像素建模。

## 对比与常见错误
- 与 Dyna/AlphaZero：MuZero 不需要环境模型（无显式 P），在 latent 规划。
- 常见错误：把 MuZero 误认为"已知规则"方法（它恰恰不需要）。

## 闭卷自测
1. MuZero 与 AlphaZero 关键区别？
2. 为何要在"隐含状态"而非原始状态上规划？

## 直觉：不知道规则也能规划
AlphaZero 需要已知转移（棋类规则）；MuZero 不学显式 P，只学“隐含状态”的动力学 g 与策略/价值头 p,v，全部在 latent 空间做 MCTS。这样它既能规划（像 AlphaZero）又适用于未知环境（像 Atari）。关键卖点：规划不依赖可解释的状态，只依赖能预测回报的隐表征——这正是它泛化强的根源。

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
