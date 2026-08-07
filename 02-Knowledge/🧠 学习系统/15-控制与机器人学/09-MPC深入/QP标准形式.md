---
title: "QP标准形式"
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
  - "[[预测方程]]"
  - "[[MPC代价函数]]"
concept: ["二次规划", "标准形式"]
prerequisites: ["预测方程", "MPC代价函数"]
related: ["QP Hessian", "稀疏QP", "OSQP"]
---

# QP标准形式

> **一句话**:MPC 的优化问题经预测方程展开后,恰好是标准的二次规划(QP)——$U$ 的二次目标 + 线性约束,可以直接交给求解器。

## 标准 QP 形式

$$\min_{z} \frac{1}{2} z^\top H z + g^\top z$$

$$\text{s.t. } l_b \le A_c z \le u_b$$

- $z$:决策变量(预测时域内所有控制量 $U$)
- $H \succ 0$:Hessian(半正定)
- $g$:梯度(线性项)
- $A_c$:约束矩阵,$l_b / u_b$ 上下界

## MPC 到 QP 的推导

由预测方程 $\mathbf{X} = \Phi\mathbf{x}_k + \Gamma \mathbf{U}$ 代入代价:

$$J = (\Phi\mathbf{x}_k + \Gamma \mathbf{U} - \mathbf{X}_{ref})^\top Q (\cdots) + \mathbf{U}^\top R \mathbf{U}$$

展开整理得:

$$H = \Gamma^\top \bar{Q} \Gamma + \bar{R}, \quad g = \Gamma^\top \bar{Q}(\Phi\mathbf{x}_k - \mathbf{X}_{ref})$$

## 约束映射

| MPC 约束 | QP 表达 |
|:---|:---|
| 输入幅值 | $U_{min} \le U \le U_{max}$(盒) |
| 输入速率 | 关于 $\Delta U$ 的线性约束 |
| 输出/状态 | $C\Phi\mathbf{x}_k + C\Gamma U$ 界约束 |

## 求解器输入

现代求解器(OSQP 等,见[[OSQP]])接受:

```
(P, q, A, l, u)  # 二次项、一次项、约束矩阵、下界、上界
```

## 自检

- [ ] 标准 QP 的数学形式?
- [ ] MPC 代价如何变成 $H$/$g$?
- [ ] MPC 约束如何映射到 QP?
