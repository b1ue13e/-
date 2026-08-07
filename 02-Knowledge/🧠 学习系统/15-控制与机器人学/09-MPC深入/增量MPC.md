---
title: "增量MPC"
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
  - "[[离散状态空间]]"
concept: ["增量控制", "积分内置"]
prerequisites: ["离散状态空间"]
related: ["MPC积分", "输入速率约束", "松弛变量"]
---

# 增量MPC

> **一句话**:用控制量的"变化量"$\Delta u$ 代替"控制量"$u$ 作为决策变量——积分作用、抗饱和、速率约束一次全解决。

## 增量形式

定义 $\Delta \mathbf{u}_k = \mathbf{u}_k - \mathbf{u}_{k-1}$,增广状态:

$$\tilde{\mathbf{x}}_k = \begin{bmatrix} \mathbf{x}_k \\ \mathbf{u}_{k-1} \end{bmatrix}$$

$$\tilde{\mathbf{x}}_{k+1} = \begin{bmatrix} A & B \\ 0 & I \end{bmatrix} \tilde{\mathbf{x}}_k + \begin{bmatrix} B \\ I \end{bmatrix} \Delta \mathbf{u}_k$$

代价中惩罚 $\Delta \mathbf{u}$ 而非 $\mathbf{u}$。

## 增量 MPC 的四大好处

| 好处 | 机制 |
|:---|:---|
| 积分作用 | 状态含 $u_{k-1}$ → 输出通道有积分 → 无稳态误差 |
| 抗饱和 | 饱和时 $\Delta u$ 自动为 0,无积分累积问题 |
| 速率约束 | $\Delta u$ 直接受幅值约束 = 输入速率约束(见[[输入速率约束]]) |
| 平滑 | 惩罚 $\Delta u$ → 控制量变化平缓 |

## 约束表达

- 幅值约束:$u_{min} \le u_{k-1} + \sum \Delta u_i \le u_{max}$(关于 $\Delta u$ 的线性约束)
- 速率约束:$\Delta u_{min} \le \Delta u \le \Delta u_{max}$

## 工程地位

**增量 MPC 是工业/车辆 MPC 的默认形态**:
- 线性车辆 MPC 普遍用增量模型(见[[线性车辆MPC]])
- 与扰动模型配合,稳态精度 + 鲁棒性兼得

## 自检

- [ ] 增量模型的状态增广方式?
- [ ] 增量 MPC 为何天然抗饱和?
- [ ] 速率约束如何用增量表达?
