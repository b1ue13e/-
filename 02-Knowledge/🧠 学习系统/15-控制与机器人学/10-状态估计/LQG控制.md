---
title: "LQG控制"
type: concept
course: "15-控制与机器人学"
stage_moc: "[[🧭 阶段10-状态估计]]"
flow: knowledge
kind: concept
importance: "A"
status: completed
created: 2026-08-07
updated: 2026-08-07
tags: [学习, 控制与机器人学, 状态估计]
upstream:
  - "[[原理陈述]]"
  - "[[LQR代价函数]]"
concept: ["LQG", "最优随机控制"]
prerequisites: ["原理陈述", "LQR代价函数", "卡尔曼滤波KalmanFilter"]
related: ["原理陈述", "闭环极点", "回路传递恢复"]
---

# LQG控制

> **一句话**:LQG = LQR(最优控制)+ Kalman 滤波(最优估计),由分离定理组合而成——线性高斯随机系统的最优输出反馈控制器。

## LQG 组成

$$\text{LQG} = \text{LQR} + \text{Kalman Filter}$$

| 部分 | 作用 | 设计 |
|:---|:---|:---|
| LQR | 状态反馈 $u = -Kx$(见[[LQR代价函数]]) | 解 ARE |
| Kalman | 状态估计 $\hat{x}$(见[[卡尔曼滤波KalmanFilter]]) | 解另一个 ARE |
| 组合 | $u = -K\hat{x}$ | 分离定理保证最优 |

## 问题设定

线性高斯系统 + 二次代价的随机最优控制:

$$dx = Ax dt + Bu dt + dw, \quad dz = Cx dt + dv$$

$$\min \mathbb{E} \int (x^\top Q x + u^\top R u) dt$$

## 两个 Riccati 方程

- 控制侧:LQR 的 ARE(见[[ARE]])→ $K$
- 估计侧:Kalman 的 ARE → $L$
- 对称结构:控制与估计对偶(见[[对偶原理]])

## LQG 的局限

| 局限 | 说明 |
|:---|:---|
| 无鲁棒性保证 | 模型误差下无稳定裕度(需 LTR,见[[回路传递恢复]]) |
| 高斯假设 | 非高斯非最优 |
| 线性假设 | 非线性需 NMPC+EKF 组合 |

## 工程地位

- LQG 是"状态估计 + 状态反馈"架构的教科书基准
- 车辆/飞行器/过程控制大量应用基础
- 分离原理使调试简单(见[[原理陈述]])

## 自检

- [ ] LQG 的组成与设计步骤?
- [ ] 两个 ARE 的对偶关系?
- [ ] LQG 的局限与对策?
