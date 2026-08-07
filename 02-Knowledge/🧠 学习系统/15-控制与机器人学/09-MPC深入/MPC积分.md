---
title: "MPC积分"
type: concept
course: "15-控制与机器人学"
stage_moc: "[[🧭 阶段9-MPC深入]]"
flow: knowledge
kind: concept
importance: "B"
status: completed
created: 2026-08-07
updated: 2026-08-07
tags: [学习, 控制与机器人学, MPC]
upstream:
  - "[[离散状态空间]]"
concept: ["积分作用", "无偏跟踪"]
prerequisites: ["离散状态空间", "MPC代价函数"]
related: ["增量MPC", "扰动模型", "MPC状态估计"]
---

# MPC积分

> **一句话**:模型失配/扰动会让 MPC 有稳态误差——把误差的积分(或扰动估计)加进模型,消除稳态偏差,这就是 MPC 的"积分作用"。

## 问题:MPC 为什么有稳态误差

MPC 基于模型优化,若模型与真实系统不一致(参数偏差、未建模扰动),输出将偏离参考且无法消除 → 稳态误差。

## 解决方案

### 1. 误差积分增广
状态增广积分项 $\mathbf{e}_I$:

$$\mathbf{e}_{I,k+1} = \mathbf{e}_{I,k} + \mathbf{e}_k \cdot \Delta t$$

代价加 $\|\mathbf{e}_I\|_{Q_I}^2$ → 类 PID 的积分作用,消除稳态误差。

### 2. 扰动模型(主流)
把常量扰动 $\mathbf{d}$ 增广为状态(见[[扰动模型]]):

$$\mathbf{x}_{k+1} = A\mathbf{x}_k + B\mathbf{u}_k + B_d \mathbf{d}_k, \quad \mathbf{d}_{k+1} = \mathbf{d}_k$$

用状态估计器(见[[MPC状态估计]])在线估计 $\mathbf{d}$ → 前馈补偿,稳态无偏。

## 对比

| 方法 | 优点 | 缺点 |
|:---|:---|:---|
| 积分增广 | 简单 | 易超调、抗饱和需额外处理 |
| 扰动模型 | 物理意义清晰、可前馈 | 需观测器、增广模型 |

## 与抗饱和的关系

积分项在约束激活时持续累积 → 积分饱和 → 需用增量形式/松弛处理(见[[增量MPC]]/[[松弛变量]])。

## 自检

- [ ] MPC 稳态误差的来源?
- [ ] 两种消除稳态误差的方法?
- [ ] 为什么扰动模型是主流方案?
