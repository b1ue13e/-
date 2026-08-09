---
created: 2026-08-07
type: study
course: "强化学习"
title: "World Model (Dreamer)"
topic: "World Model (Dreamer)"
stage_moc: "[[🧭 阶段8-模型基与规划]]"
flow: knowledge
kind: concept
status: learning
importance: "B"
tags: [学习, 强化学习]
upstream: ["[[MuZero]]", "[[模型基RL概述]]"]
concept: ["World Model", "RSSM", "想象训练", "潜空间"]
sources:
  - "Ha & Schmidhuber 2018 (World Models); Hafner et al. 2019 (Dreamer)"
---
# World Model (Dreamer)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`World Models / Dreamer 原文`
> 对应阶段：[[🧭 阶段8-模型基与规划|返回阶段页]]

## 动机
高维观测（图像）直接学动态难。World Model 先在潜空间学一个紧凑世界模型（RSSM），再在"想象"的潜轨迹上训练策略，大幅降低规划维度。

## 正式定义 / 公式
RSSM：状态先验 p(s_t|s_{t-1},a_{t-1}) 与观测解码 q(s_t|s_{t-1},a_{t-1},o_t) 结合；策略在模型 rollout 的潜轨迹上用 Actor-Critic 更新。

## 最小手算例子
图像观测 64×64×3 = 12288 维；压缩到潜状态 30 维。在潜空间想象 50 步轨迹训练，每步真实交互成本仅原图的约 1/400，样本效率提升。

## 对比与常见错误
- 与 MuZero：都做潜空间规划；Dreamer 用 RSSM + 想象训练 AC，MuZero 用 MCTS。
- 常见错误：潜空间建模不足导致想象失真、策略在真实环境失效。

## 闭卷自测
1. World Model / Dreamer 为何要在潜空间做想象？
2. RSSM 中先验与后验的作用？

## 直觉：在“压缩后的世界”里想象
高维像素直接学动态又贵又难。World Model/Dreamer 先用 RSSM 把观测压成 30 维左右潜状态，再在潜轨迹上“想象”几十步训练 Actor-Critic。真实交互成本降到原图的约 1/400，样本效率大增。风险：潜空间建模不足会让“想象”失真、策略在真实环境失效——所以 RSSM 用先验+后验共同约束潜状态。

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
