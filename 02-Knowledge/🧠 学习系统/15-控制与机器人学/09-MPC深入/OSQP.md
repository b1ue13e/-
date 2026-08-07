---
title: "OSQP"
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
  - "[[一阶QP]]"
concept: ["ADMM求解器", "嵌入式优化"]
prerequisites: ["一阶QP", "QP标准形式"]
related: ["稀疏QP", "热启动", "MPC代码生成"]
---

# OSQP

> **一句话**:OSQP 是基于 ADMM 的开源 QP 求解器——为实时 MPC 而生:稀疏、可热启动、可提前终止,工业与学术界的事实标准。

## 什么是 OSQP

- **O**perator **S**plitting **Q**uadratic **P**rogram(算子分裂 QP)
- 基于 ADMM 的一阶方法
- 支持稀疏矩阵、不等式/等式约束、无导数要求

## 求解形式

$$\min \frac{1}{2} z^\top P z + q^\top z \quad \text{s.t.} \quad l \le Az \le u$$

## 核心优势

| 优势 | 机制 |
|:---|:---|
| 稀疏 | 只处理非零元素 → 大规模可行 |
| 热启动 | 上次解作初值(见[[热启动]]) |
| 提前终止 | 每迭代检查精度,达标即停(见[[早期终止]]) |
| 多项式复杂度 | 迭代与问题规模弱相关 |
| 跨平台 | C 实现,嵌入式可用 |

## 与 MPC 的配合

- 每周期组装 $P, q, A, l, u$(见[[QP标准形式]])
- 热启动:上一周期解直接传入
- 提前终止:控制周期内解不完 → 用当前迭代解(次优但可用)

## 代码生成与部署

- OSQP 支持生成独立 C 代码(见[[MPC代码生成]])
- 配合 CVXGEN/ECOS 生态,嵌入式 MPC 常用
- Python 接口:cvxpy 默认后端之一

## 自检

- [ ] OSQP 的算法基础与输入形式?
- [ ] 三大实时性优势?
- [ ] 嵌入式 MPC 如何部署 OSQP?
