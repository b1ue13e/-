---
created: 2026-08-07
type: study
course: "强化学习"
title: "模型基RL概述 (Model-based RL)"
topic: "模型基RL概述 (Model-based RL)"
stage_moc: "[[🧭 阶段8-模型基与规划]]"
flow: knowledge
kind: concept
status: learning
importance: "A"
tags: [学习, 强化学习]
upstream: ["[[MDP 与贝尔曼方程]]", "[[动态规划：策略与值迭代]]"]
concept: ["模型基", "环境模型", "规划", "样本效率"]
sources:
  - "Sutton & Barto Ch.8; Moerland et al., 2023 (Model-based RL survey)"
---
# 模型基RL概述 (Model-based RL)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`Sutton & Barto Ch.8`
> 对应阶段：[[🧭 阶段8-模型基与规划|返回阶段页]]

## 动机
无模型 RL（Q-learning/PPO）样本效率低，需海量交互。模型基 RL 先学一个环境动态模型 P(s'|s,a)，再用模型"想象"地规划，大幅提升样本效率。

## 正式定义 / 公式
学模型 f_φ : (s,a) → (s', r)；策略优化可在真实或"模型生成"的轨迹上做。目标仍 max E[G]，但更新可利用模型。

## 最小手算例子
无模型需 N=1e6 步学到某 GridWorld 最优；模型基先花 1e4 步学模型，再用模型规划 1e4 步，总交互 2e4 步达相近性能——样本效率约 50× 提升（示意值）。

## 对比与常见错误
- 与无模型：样本效率高但受模型误差影响（"模型偏差"）；无模型更稳健但慢。
- 常见错误：在误差大的模型上过度规划（compounding error 累积）。

## 闭卷自测
1. 模型基 RL 的核心思想？相比无模型的取舍？
2. 模型误差如何随规划步数累积？

## 直觉：用“想象”换样本
无模型 RL（Q/PPO）靠海量真实交互；模型基 RL 先学 f:(s,a)→(s',r)，再用它生成仿真轨迹来规划，样本效率可高一个数量级。代价是“model bias”：模型误差会在多步规划里复利放大（compounding error）。实践上常限制规划 horizon、用集成估计不确定性来兜底，或走“基于模型的策略优化(MBPO)”折中路线。

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
