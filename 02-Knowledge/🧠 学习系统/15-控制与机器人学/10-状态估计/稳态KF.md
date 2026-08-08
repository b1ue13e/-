---
title: "稳态KF"
type: concept
course: "控制与机器人学"
stage_moc: "[[🧭 阶段10-状态估计]]"
flow: knowledge
kind: concept
importance: "B"
status: completed
created: 2026-08-07
updated: 2026-08-07
tags: [学习, 控制与机器人学, 状态估计]
upstream:
  - "[[卡尔曼滤波KalmanFilter]]"
concept: ["稳态增益", "离线计算"]
prerequisites: ["卡尔曼滤波KalmanFilter", "卡尔曼增益"]
related: ["卡尔曼增益", "稳定性", "观测器结构"]
---

# 稳态KF

> **一句话**:时不变系统中,KF 增益会收敛到常值——预先把稳态增益算好,在线只做两步乘法,省掉矩阵运算,计算量大减。

## 现象

对时不变 $(A, H, Q, R)$,随着迭代:

$$P_k^- \to P_\infty, \quad P_k^+ \to P_\infty^+, \quad K_k \to K_\infty$$

增益收敛为常值(由离散代数 Riccati 方程 DARE 决定):

$$P_\infty = A P_\infty A^\top - A P_\infty H^\top (H P_\infty H^\top + R)^{-1} H P_\infty A^\top + Q$$

## 稳态 KF 的实现

在线只需:

$$\hat{\mathbf{x}}^+ = \hat{\mathbf{x}}^- + K_\infty (\mathbf{z} - H\hat{\mathbf{x}}^-)$$

等价于固定增益观测器(见[[观测器结构]]),无协方差更新。

## 优缺点

| 优点 | 缺点 |
|:---|:---|
| 计算量极小(嵌入式友好) | 参数变化时非最优 |
| 无数值问题 | 失去自适应能力 |
| 实时性确定 | 需要离线求解 DARE |

## 适用场景

- 时不变/弱时变系统(GPS 融合、电机)
- 计算受限平台
- 需求确定、噪声稳定

## 与自适应 KF 的关系

- 稳态 KF:固定增益(简单)
- 自适应 KF:在线调 $Q$/$R$ 或增益(复杂)
- 选择取决于系统时变性与算力

## 自检

- [ ] 稳态增益从何而来?
- [ ] 在线只做什么运算?
- [ ] 稳态 KF 的适用场景?
