---
title: "联合MPC设计"
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
  - "[[横向MPC设计]]"
  - "[[纵向MPC设计]]"
concept: ["纵横向联合", "耦合MPC"]
prerequisites: ["横向MPC设计", "纵向MPC设计", "Frenet耦合"]
related: ["耦合MPC", "横向MPC设计", "纵向MPC设计"]
---

# 联合MPC设计

> **一句话**:横向 MPC 与纵向 MPC 合成一个联合优化——油门刹车与方向盘共享模型和约束,把纵横向耦合(摩擦圆)显式处理好。

## 联合状态与控制

$$\mathbf{x} = [s, \dot s, d, \dot d, \delta, \dot\delta], \quad \mathbf{u} = [a, j_\delta]$$

- 纵向:位置/速度/加速度($s, \dot s, a$)
- 横向:偏移/横向速度($d, \dot d$)+ 转向($\delta$)
- 控制:纵向加速度 $a$ + 转向率 $j_\delta$

## 联合模型的必要性

- 摩擦圆:纵向 $a_x$ 与横向 $a_y$ 共享附着(见[[Frenet耦合]])
- 速度耦合:横向动力学矩阵随 $v$ 变
- 参考同步:换道 + 减速同时发生

## 代价与约束

| 项 | 内容 |
|:---|:---|
| 代价 | 横纵误差 + 控制量 + jerk |
| 硬约束 | 转向幅值/速率、速度上限 |
| 软约束 | 加速度(摩擦圆)、车道边界 |
| 耦合约束 | $a_x^2 + a_y^2 \le (\mu g)^2$(可凸化) |

## 设计权衡

| 方案 | 优点 | 缺点 |
|:---|:---|:---|
| 独立横纵 MPC | 简单、实时 | 忽略耦合 |
| 联合 MPC(线性) | 显式耦合、QP 可解 | 状态维度高、计算重 |
| 联合 NMPC | 全模型 | 更重 |

## 工程实践

- 联合 MPC 常见于换道、紧急避障
- 常规巡航:独立横纵(算力省)
- 调度:根据场景切换(见[[增益调度]])

## 自检

- [ ] 联合 MPC 的状态与控制维度?
- [ ] 耦合约束如何表达?
- [ ] 与独立横纵 MPC 的取舍?
