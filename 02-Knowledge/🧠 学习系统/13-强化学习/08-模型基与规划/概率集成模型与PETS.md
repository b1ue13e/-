---
created: 2026-08-07
type: study
course: "强化学习"
title: "概率集成模型与 PETS (Probabilistic Ensemble & PETS)"
topic: "概率集成模型与 PETS (Probabilistic Ensemble & PETS)"
stage_moc: "[[🧭 阶段8-模型基与规划]]"
flow: knowledge
kind: algorithm
status: learning
importance: "A"
tags: [学习, 强化学习, 模型基, 不确定性]
upstream: ["[[环境动态模型学习]]", "[[复合误差与模型偏差]]"]
concept: ["集成模型", "概率动力学", "PETS", "CEM", "不确定性裁剪"]
sources:
  - "Chua et al. 2018 (PETS); Lakshminarayanan et al. 2017 (ensemble)"
---
# 概率集成模型与 PETS (Probabilistic Ensemble & PETS)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段8-模型基与规划|返回阶段页]]

## 动机
单点估计模型给不出"我有多不确定"，于是无法判断某次 rollout 是否漂到 OOD 区。PETS 用**概率集成（Probabilistic Ensemble）**：训练 N 个独立的神经网络，每个输出高斯分布，集成捕捉**偶发不确定性（aleatoric）**与**认知不确定性（epistemic）**。控制时用**交叉集成方法（CEM）**在模型里搜索动作序列，并用不确定度裁剪危险分支。

## 正式定义 / 公式
- 集成：第 i 个网络预测 p_i(s'|s,a)=N(μ_i, σ_i²)，整体预测取混合/乘积。若各网络对某 (s,a) 预测差异大 → 认知不确定度高（没见过的区域）。
- PETS 控制：从集成采样若干条动力学，用 CEM 优化一条 k 步动作序列 a_{1:k}，使期望回报最大；评价时把"高方差分支"的回报打折（惩罚不确定），避免策略钻模型漏洞。

## 最小手算例子
二维点质量控制：集成 5 个网络，在已充分探索区它们预测一致（σ 小）；在从未到过的角落，5 个网络 μ 分散（σ 大）。CEM 自然避开高 σ 分支，先选保守但可信的动作，等真实数据补进来再探索——这就是"用不确定性当安全护栏"。

## 对比与常见错误
- 与 MBPO：PETS 是**基于模型的控制**（规划即动作），MBPO 是**造数据喂无模型**。
- 与单网络模型：单网络无 σ，无法裁剪 OOD，更易被复合误差坑。
- **常见错误**：集成各网络初始化相同 → 退化为单模型；CEM 迭代次数太少导致动作序列次优。

## 闭卷自测
1. 概率集成如何同时表达两种不确定性？
2. PETS 用不确定度做了什么（为何要"裁剪"高方差分支）？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
