---
title: "EKF步骤"
type: concept
course: "控制与机器人学"
stage_moc: "[[🧭 阶段10-状态估计]]"
flow: knowledge
kind: concept
importance: "A"
status: completed
created: 2026-08-07
updated: 2026-08-07
tags: [学习, 控制与机器人学, 状态估计]
upstream:
  - "[[EKF非线性状态估计]]"
  - "[[线性化]]"
concept: ["EKF算法", "递推步骤"]
prerequisites: ["EKF非线性状态估计", "线性化", "雅可比计算"]
related: ["预测步", "更新步", "局部线性化"]
---

# EKF步骤

> **一句话**:EKF 的完整流程——初始化后,"非线性预测 + 雅可比 + 线性更新"循环往复,与 KF 结构一一对应。

## 完整算法

**初始化**:$\hat{\mathbf{x}}_0, P_0$

**循环 k = 0,1,2,...:**

### 预测步(时间更新)
1. 状态传播:$\hat{\mathbf{x}}_{k+1}^- = f(\hat{\mathbf{x}}_k, \mathbf{u}_k)$
2. 计算雅可比:$F_k = \partial f/\partial \mathbf{x}|_{\hat{\mathbf{x}}_k}$
3. 协方差传播:$P_{k+1}^- = F_k P_k F_k^\top + Q$

### 更新步(测量更新,有测量时)
4. 预测测量:$\hat{\mathbf{z}} = h(\hat{\mathbf{x}}_{k+1}^-)$
5. 计算雅可比:$H_k = \partial h/\partial \mathbf{x}|_{\hat{\mathbf{x}}^-}$
6. 新息:$r = \mathbf{z}_k - \hat{\mathbf{z}}$
7. 增益:$K = P^- H_k^\top (H_k P^- H_k^\top + R)^{-1}$
8. 状态更新:$\hat{\mathbf{x}}^+ = \hat{\mathbf{x}}^- + K r$
9. 协方差更新:$P^+ = (I - K H_k) P^-$

## 与 KF 的对应

| KF | EKF |
|:---|:---|
| $A\hat{\mathbf{x}}$ | $f(\hat{\mathbf{x}})$ |
| $A$ | $F_k$(雅可比) |
| $H\hat{\mathbf{x}}$ | $h(\hat{\mathbf{x}})$ |
| $H$ | $H_k$(雅可比) |

**结构完全一致,只是用雅可比替换系统矩阵**。

## 工程注意

| 注意 | 说明 |
|:---|:---|
| 雅可比精度 | 数值差分 vs 解析,解析更稳(见[[雅可比计算]]) |
| 测量缺失 | 只跑预测步(与[[采样率差异]]配合) |
| 发散监控 | 新息检验(见[[故障检测]]) |

## 自检

- [ ] EKF 九步流程?
- [ ] EKF 与 KF 的结构对应?
- [ ] 无测量时 EKF 如何运行?
