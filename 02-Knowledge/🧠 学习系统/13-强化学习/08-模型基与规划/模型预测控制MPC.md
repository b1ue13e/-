---
created: 2026-08-07
type: study
course: "强化学习"
title: "模型预测控制 MPC (Model Predictive Control)"
topic: "模型预测控制 MPC (Model Predictive Control)"
stage_moc: "[[🧭 阶段8-模型基与规划]]"
flow: knowledge
kind: algorithm
status: learning
importance: "B"
tags: [学习, 强化学习, 模型基, 控制]
upstream: ["[[概率集成模型与PETS]]", "[[模型基RL概述]]"]
concept: ["MPC", "滚动优化", "receding horizon", "轨迹优化"]
sources:
  - "Camacho & Bordons 2007 (MPC textbook); control theory literature"
---
# 模型预测控制 MPC (Model Predictive Control)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段8-模型基与规划|返回阶段页]]

## 动机
MPC 来自控制理论，是"基于模型的决策时规划"最经典的范式：不学一个固定策略，而是**每一步都重新用模型往前搜一段最优轨迹，只执行第一步，然后滚动重规划**。这让它能即时响应扰动和模型误差——因为每步都"重新看一眼"。

## 正式定义 / 公式
在状态 s_t，求解一个有限 horizon 优化：

  a_{t:t+H−1}* = argmax_{a_.} Σ_{k=0}^{H−1} γ^k r(s_{t+k}, a_{t+k})

  受 s_{t+k+1} = f(s_{t+k}, a_{t+k})，可选约束 s∈𝒮, a∈𝒜

只执行 a_t*，环境推进到 s_{t+1}，再重解。优化可用 CEM、iLQR、梯度法或采样。模型 f 可以是学得的（PETS）或已知（经典控制）。

## 最小手算例子
自动驾驶跟车：每帧用车辆模型预测未来 2 秒的 (油门, 刹车) 序列，选让车距安全且舒适的那个序列的第一步；下一帧因前车突然减速，重新预测——MPC 自然刹住。若用固定策略则可能因训练时没见过该场景而出事。

## 对比与常见错误
- 与 Dyna/背景规划：MPC 是**决策时、在线、滚动**的；Dyna 是离线更新值函数。
- 与 PETS：PETS 本质是 MPC 的一种（用集成+CEM 做每步优化）。
- **常见错误**：horizon H 太长→实时算不动；H 太短→目光短浅；模型被扰动后不重规划→误差累积。

## 闭卷自测
1. MPC 为何"每步重规划"反而更抗扰动？
2. MPC 与学固定策略 π(a|s) 的根本区别？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
