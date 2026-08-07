---
title: "QP Hessian"
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
  - "[[QP标准形式]]"
concept: ["Hessian矩阵", "条件数"]
prerequisites: ["QP标准形式", "预测方程"]
related: ["QP标准形式", "稀疏QP", "一阶QP"]
---

# QP Hessian

> **一句话**:QP 的 Hessian $H$ 决定求解难度与解的品质——$H$ 的稀疏性、条件数直接影响"好不好解、解得快不快"。

## 定义

$$H = \Gamma^\top \bar{Q} \Gamma + \bar{R}$$

- $\Gamma$:预测矩阵(见[[预测方程]])
- $\bar{Q}, \bar{R}$:块对角化的权重矩阵

## 结构特点

- 维度:$N_c \cdot n_u \times N_c \cdot n_u$(随控制时域增长)
- 稀疏性:$\Gamma$ 是下三角 → $H$ 有带状结构(线性 MPC)
- 正定性:$H \succ 0$(因为 $\bar{R} \succ 0$)→ 唯一解

## 条件数与数值

$$\kappa(H) = \frac{\lambda_{max}}{\lambda_{min}}$$

| 问题 | 表现 |
|:---|:---|
| $\kappa$ 大(病态) | 求解慢、数值误差大 |
| $\kappa$ 小(良态) | 求解快、稳定 |

条件数大的来源:权重量级差异大($Q_{xx}$ 与 $R$ 差几个数量级)、采样时间过小。

## 工程处理

| 手段 | 说明 |
|:---|:---|
| 权重归一化 | 各状态单位归一,避免量级悬殊 |
| 预处理 | 对角缩放(P 尺度化) |
| 稀疏存储 | 利用带状结构,省内存(见[[稀疏QP]]) |

## 自检

- [ ] H 的表达式与结构?
- [ ] 条件数影响什么?
- [ ] 如何改善病态 Hessian?
