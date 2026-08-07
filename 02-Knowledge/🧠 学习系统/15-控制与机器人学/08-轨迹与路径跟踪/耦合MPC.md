---
title: "耦合MPC"
type: concept
course: "15-控制与机器人学"
stage_moc: "[[🧭 阶段8-轨迹与路径跟踪]]"
flow: knowledge
kind: concept
importance: "A"
status: completed
created: 2026-08-07
updated: 2026-08-07
tags: [学习, 控制与机器人学, 轨迹跟踪]
upstream:
  - "[[Frenet耦合]]"
  - "[[MPC横向预测]]"
concept: ["联合优化", "MPC"]
prerequisites: ["Frenet耦合", "MPC横向预测", "MPC横向代价"]
related: ["解耦控制", "MPC深入", "横向优化"]
---

# 耦合MPC

> **一句话**:把纵向 $s$ 和横向 $d$ 放进同一个优化里同时求——耦合 MPC 显式处理纵横向交互,是激烈工况下的"王炸"。

## 为什么需要耦合

解耦控制在常规工况够用,但:
- 摩擦圆耦合:急刹 + 转向 同时需求轮胎附着(见[[Frenet耦合]])
- 时间耦合:换道+减速同时发生时,纵横向轨迹共享动力学
- 紧急避障:必须"边减速边转向"

## 问题建模

以 $(s, d)$ 为状态,Frenet 系下的车辆模型:

$$\mathbf{x} = [s, \dot s, d, \dot d, \delta, \dot\delta]$$

$$\min_{u} \sum_{k=0}^{N-1} \big( \|\mathbf{x}_k - \mathbf{x}_{ref,k}\|_Q^2 + \|u_k\|_R^2 \big) + \|\mathbf{x}_N - \mathbf{x}_{ref,N}\|_P^2$$

$$\text{s.t. } \mathbf{x}_{k+1} = f(\mathbf{x}_k, u_k), \quad \mathbf{x} \in \mathcal{X}, \; u \in \mathcal{U}$$

## 关键设计点

| 要素 | 内容 |
|:---|:---|
| 模型 | 纵向 + 横向动力学联合(摩擦圆) |
| 约束 | 加速度/转向角/转向率/摩擦圆 |
| 代价 | 横纵误差 + 控制量 |
| 求解 | QP(线性化)/NLP(非线性) |

## 与解耦控制对比

| 维度 | 解耦 | 耦合 MPC |
|:---|:---|:---|
| 计算量 | 低(10Hz+ 轻松) | 高(20–50Hz 需优化) |
| 耦合处理 | 事后检查 | 显式建模 |
| 工况 | 常规 | 高速/紧急 |
| 调参 | 直观 | 权重矩阵复杂 |

## 工程现状

- 量产:解耦 + MPC 单通道为主
- 研究/高端:耦合 MPC(非线性 MPC)
- 混合:纵向独立 MPC + 横向 MPC 共享约束

## 自检

- [ ] 耦合 MPC 与解耦的核心差异?
- [ ] 状态向量与约束如何设计?
- [ ] 计算量为何是工程瓶颈?
