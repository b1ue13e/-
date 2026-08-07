---
title: "MPC代价函数"
type: concept
course: "15-控制与机器人学"
stage_moc: "[[🧭 阶段9-MPC深入]]"
flow: knowledge
kind: concept
importance: "A"
status: completed
created: 2026-08-07
updated: 2026-08-07
tags: [学习, 控制与机器人学, MPC]
upstream:
  - "[[模型预测控制(MPC)]]"
concept: ["二次代价", "权重矩阵"]
prerequisites: ["模型预测控制(MPC)", "预测方程"]
related: ["QP标准形式", "终端代价", "时域设计"]
---

# MPC代价函数

> **一句话**:MPC 的"目标函数"——状态误差与控制能耗的加权二次和,$Q$/$R$ 权重决定控制器"性格"。

## 标准形式

$$\min_{u} J = \sum_{k=0}^{N-1} \Big( \|\mathbf{x}_{k+1} - \mathbf{x}_{ref}\|_Q^2 + \|\mathbf{u}_k\|_R^2 \Big)$$

展开写:

$$J = \sum_{k=0}^{N-1} \big( \mathbf{e}_k^\top Q \mathbf{e}_k + \mathbf{u}_k^\top R \mathbf{u}_k \big), \quad \mathbf{e}_k = \mathbf{x}_{k+1} - \mathbf{x}_{ref,k+1}$$

## 权重矩阵

| 矩阵 | 作用 | 调参直觉 |
|:---|:---|:---|
| $Q \succeq 0$ | 状态误差惩罚 | $Q$ 大 → 跟踪紧、动作猛 |
| $R \succ 0$ | 控制量惩罚 | $R$ 大 → 省能耗、响应钝 |
| 对角项 | 各状态重要性 | 位置/航向/速度分别加权 |

## 终端项(稳定性关键)

$$J_N = \|\mathbf{x}_N - \mathbf{x}_{ref,N}\|_P^2$$

$P$ 为终端代价矩阵(见[[终端代价]]),弥补有限时域的"尾部截断"。

## 参考轨迹嵌入

$\mathbf{x}_{ref,k}$ 来自规划层(见[[参考轨迹]]);时变参考 → 代价含时变偏移项 → QP 的一次项。

## 调参经验

- 先固定 $R$,增大 $Q$ 观察响应
- 位置权重 > 速度权重(车辆典型)
- 权重 = 系统的"性格旋钮":重跟踪轻能耗 vs 轻跟踪重节能

## 自检

- [ ] 代价函数三项各是什么?
- [ ] $Q$/$R$ 的物理含义与调参方向?
- [ ] 终端项为何必要?
