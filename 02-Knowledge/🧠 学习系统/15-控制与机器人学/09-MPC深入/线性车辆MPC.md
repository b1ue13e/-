---
title: "线性车辆MPC"
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
  - "[[车辆线性化]]"
  - "[[模型预测控制(MPC)]]"
concept: ["线性化MPC", "时变线性化"]
prerequisites: ["车辆线性化", "模型预测控制(MPC)", "QP标准形式"]
related: ["横向MPC设计", "纵向MPC设计", "非线性车辆MPC"]
---

# 线性车辆MPC

> **一句话**:把非线性车辆模型在工作点线性化(或做误差模型),MPC 就变成标准 QP——实时、可靠、工程量产的主流形态。

## 为什么线性化

- 车辆模型非线性(见[[车辆动力学]]):轮胎、运动学非线性
- 非线性 MPC 计算重(见[[非线性车辆MPC]])
- 线性化后 = 标准 QP(见[[QP标准形式]])→ 实时求解

## 线性化方式

### 1. 工作点线性化(单点)
在参考点 $(\mathbf{x}_{ref}, \mathbf{u}_{ref})$ 处泰勒展开:

$$\dot{\tilde{\mathbf{x}}} = A \tilde{\mathbf{x}} + B \tilde{\mathbf{u}}$$

仅对参考附近有效。

### 2. 时变线性化(LTV-MPC,主流)
沿参考轨迹每步线性化:

$$\tilde{\mathbf{x}}_{k+1} = A_k \tilde{\mathbf{x}}_k + B_k \tilde{\mathbf{u}}_k$$

$A_k, B_k$ 随参考轨迹变化,每周期重算 → 实时性好、跟踪范围大。

### 3. 误差模型(常用)
直接建立误差状态(见[[车辆误差模型]]),天然线性化且自平衡。

## 对比

| 维度 | LTV-MPC | 非线性 MPC |
|:---|:---|:---|
| 求解 | QP(快) | NLP(慢) |
| 适用 | 参考轨迹附近 | 大偏差/极限工况 |
| 工程 | 量产主流 | 研究/高端 |

## 工程要点

- 增量形式 + 时变线性化 = 车辆 MPC 默认组合(见[[增量MPC]])
- 每周期重新组装 $A_k, B_k$(速度/曲率依赖)
- 线性化误差大时(急转向)需更细参考或切非线性

## 自检

- [ ] 三种线性化方式?
- [ ] LTV-MPC 为什么是量产主流?
- [ ] 与非线性 MPC 的取舍?
