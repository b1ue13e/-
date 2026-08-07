---
title: "非线性车辆MPC"
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
  - "[[线性车辆MPC]]"
  - "[[非线性预测]]"
concept: ["NMPC", "非线性优化"]
prerequisites: ["线性车辆MPC", "非线性预测"]
related: ["非线性预测", "线性车辆MPC", "显式MPC"]
---

# 非线性车辆MPC

> **一句话**:直接用非线性车辆模型做预测控制(NMPC)——大偏差、极限工况(漂移、紧急避障)下线性 MPC 失效时,NMPC 能救场,但计算代价大。

## 何时需要 NMPC

| 场景 | 线性 MPC | NMPC |
|:---|:---|:---|
| 正常跟踪 | ✅ | 杀鸡用牛刀 |
| 大航向偏差 | ❌ 线性化失效 | ✅ |
| 漂移/极限 | ❌ | ✅(轮胎非线性) |
| 紧急避障 | 勉强 | ✅ |

## 问题形式

$$\min_u \sum \ell(\mathbf{x}_k, \mathbf{u}_k) \quad \text{s.t.} \quad \mathbf{x}_{k+1} = f(\mathbf{x}_k, \mathbf{u}_k), \; \mathbf{x} \in \mathcal{X}, \; u \in \mathcal{U}$$

$f$:非线性车辆模型(自行车 + 魔术公式轮胎,见[[魔术公式]]/[[车辆动力学]])

## 求解方法

| 方法 | 思路 |
|:---|:---|
| 序贯二次规划(SQP) | 每迭代线性化 → 子 QP |
| 实时迭代(RTI) | 每步只做一次 SQP 迭代(热启动) |
| 直接配点/打靶 | 离散化为 NLP 求解 |
| acados/CasADi | 现代高效 NMPC 框架 |

## 关键难点

- **非凸性**:多局部最优,初值敏感 → 热启动至关重要(见[[热启动]])
- **计算量**:每周期解 NLP,实时压力大
- **实现复杂度**:雅可比/黑塞计算、求解器集成

## 工程取舍

- 先线性 MPC 打底,必要时 NMPC 增强
- 或:线性 MPC + 约束/限幅兜底(工程主流)
- 硬件升级(高性能 ECU)时 NMPC 才可行

## 自检

- [ ] NMPC 与线性 MPC 的适用边界?
- [ ] 常用求解方法?
- [ ] 工程上如何取舍?
