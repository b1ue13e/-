---
title: "稀疏QP"
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
concept: ["稀疏结构", "带状矩阵"]
prerequisites: ["QP标准形式", "QP Hessian"]
related: ["QP Hessian", "OSQP", "MPC代码生成"]
---

# 稀疏QP

> **一句话**:MPC 的 QP 天然稀疏(带状/块对角)——利用稀疏结构,内存省 90% 以上、求解快数倍,这是大规模 MPC 可行的关键。

## 为什么 MPC 的 QP 稀疏

预测时域结构:
- $H = \Gamma^\top \bar{Q} \Gamma + \bar{R}$:$\Gamma$ 下三角 → $H$ 带状
- 约束矩阵 $A$:块对角(各步约束独立)+ 少量耦合
- 决策变量规模 $N_c \cdot n_u$:时域大时矩阵巨大但稀疏

## 稀疏 vs 稠密

| 维度 | 稠密表示 | 稀疏表示 |
|:---|:---|:---|
| 存储 | $n^2$ | $O(n)$(非零数) |
| 矩阵乘 | $O(n^2)$ | $O(nnz)$ |
| 求解(因子分解) | $O(n^3)$ | 接近 $O(n)$(带状) |

## 稀疏求解技术

- **带状 Cholesky / LDL**:预测问题结构固定,复用分解
- **结构利用**:变量排序(状态 vs 控制分组)减少带宽
- **Kronecker/块结构**:块操作代替逐元素

## 工程要点

| 要点 | 说明 |
|:---|:---|
| 求解器选择 | OSQP 等原生支持稀疏(见[[OSQP]]) |
| 代码生成 | 结构固定 → 生成专用代码(见[[MPC代码生成]]) |
| 内存预算 | 嵌入式 MPC 依赖稀疏存储 |

## 自检

- [ ] MPC 的 QP 为何稀疏?
- [ ] 稀疏表示的计算优势?
- [ ] 如何利用带状结构加速?
