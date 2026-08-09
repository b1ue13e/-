---
created: 2026-08-07
type: study
course: "强化学习"
title: "RSSM与Dreamer系列 (Recurrent State-Space Model & Dreamer)"
topic: "RSSM与Dreamer系列 (Recurrent State-Space Model & Dreamer)"
stage_moc: "[[🧭 阶段8-模型基与规划]]"
flow: knowledge
kind: algorithm
status: learning
importance: "A"
tags: [学习, 强化学习, 模型基, 世界模型]
upstream: ["[[World Model (Dreamer)]]", "[[环境动态模型学习]]", "[[模型预测控制MPC]]"]
concept: ["RSSM", "Dreamer", "潜空间想象", "递归状态空间"]
sources:
  - "Hafner et al. 2019/2020/2023 (Dreamer v1/v2/v3); Haarnoja et al. SAC"
---
# RSSM与Dreamer系列 (Recurrent State-Space Model & Dreamer)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段8-模型基与规划|返回阶段页]]

## 动机
高维像素观测下直接学 (s,a)→s' 不现实。Dreamer 学一个**潜空间世界模型**：把图像压成隐状态 z，在隐状态里"做梦"训练策略，再用学到的策略在真实环境执行。RSSM（Recurrent State-Space Model）是其核心动力学，结合"确定性递归 h"与"随机隐状态 z"，兼顾长期依赖与随机性。

## 正式定义 / 公式
RSSM 每一步生成：
- 随机隐状态 z_t ~ p(z_t | h_t) ；确定性递归 h_t = f_φ(h_{t−1}, z_{t−1}, a_{t−1})
- 观测/奖励重建：x̂_t ~ p_θ(x_t|h_t,z_t)，r̂_t ~ p_θ(r_t|h_t,z_t)
- 推理后验：q_φ(z_t | h_t, x_t) 用于训练时
训练目标 = 观测重建 + 奖励重建 + KL 约束（后验与先验一致）。策略在**想象的轨迹**上用 AC/λ-return 训练（类似 SAC/PPO 的隐空间版），然后部署到真实环境只取第一步动作。

## 最小手算例子
DeepMind 的"从像素学走路"：智能体看到的是图像，RSSM 把图像编码成 z，在 z 里想象"向左走会怎样"，策略学会后真实执行，几小时游戏内经验就学会运动。相比从像素直接无模型训练，样本效率高一个量级。

## 对比与常见错误
- 与 MuZero：两者都在潜空间规划；MuZero 用 MCTS 搜索，Dreamer 用"想象 rollout + 梯度"训练策略（更偏 Dyna 式）。
- 与 PETS/MPC：Dreamer 学策略而非每步重规划，适合长 horizon 持续控制。
- **常见错误**：KL 权重过大→潜空间坍塌/信息丢失；过小→后验先验不一致、想象失真。

## 闭卷自测
1. RSSM 里"确定性递归 h"和"随机隐状态 z"分别记什么？为何要两个？
2. Dreamer 在真实环境执行时，世界模型起到什么作用？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
