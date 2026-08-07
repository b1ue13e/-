---
title: "MPC状态估计"
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
  - "[[扰动模型]]"
  - "[[观测器结构]]"
concept: ["状态反馈", "观测器"]
prerequisites: ["扰动模型", "观测器结构"]
related: ["MPC积分", "EKF非线性状态估计", "卡尔曼滤波KalmanFilter"]
---

# MPC状态估计

> **一句话**:MPC 需要完整状态,但传感器测不全——状态估计器(观测器/KF/EKF)在线重建状态,MPC 与估计器"分离原理"式搭配。

## 为什么需要

- MPC 代价与约束都基于状态 $\mathbf{x}_k$
- 真实系统只能测部分状态(如只测位置,不测速度)
- 扰动模型增广后的 $\hat{\mathbf{d}}$ 也要估计(见[[扰动模型]])

## 常用估计器

| 估计器 | 适用 | 说明 |
|:---|:---|:---|
| Luenberger 观测器 | 线性、确定性 | $\hat{\mathbf{x}}^+ = A\hat{\mathbf{x}} + Bu + L(\mathbf{y} - C\hat{\mathbf{x}})$ |
| Kalman 滤波 | 线性 + 高斯噪声 | 最优估计,见[[卡尔曼滤波KalmanFilter]] |
| EKF | 非线性 | 线性化扩展,见[[EKF非线性状态估计]] |
| 无迹 KF / 粒子滤波 | 强非线性 | 计算重 |

## 分离结构

```
传感器 y_k → 状态估计器 → x̂_k, d̂_k → MPC 优化 → u_k
```

- 估计器与控制器**分离设计**(类似[[分离原理]])
- 估计质量直接影响 MPC 性能:估计噪声 → 控制抖动

## 工程要点

| 要点 | 说明 |
|:---|:---|
| 估计延迟 | 估计滞后 → MPC 用旧状态 → 需预测补偿 |
| 采样同步 | 估计器与 MPC 同频或快于 MPC |
| 故障 | 估计器发散 → 安全降级(切保守控制) |

## 自检

- [ ] MPC 为什么必须配状态估计?
- [ ] 常用估计器如何选择?
- [ ] 估计延迟对 MPC 的影响?
