---
type: study
topic: "QP标准形式"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-08
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段9-MPC深入]]"
flow: knowledge
kind: concept
concept: ["二次规划", "标准形式", "Hessian"]
prerequisites: ["预测方程", "MPC代价函数"]
related: ["QP Hessian", "稀疏QP", "OSQP"]
upstream: ["[[09-MPC深入/预测方程]]", "[[09-MPC深入/MPC代价函数]]"]
source: "Borrelli, Predictive Control；OSQP 文档"
tags: [学习, 控制与机器人学, MPC]
---

# QP标准形式

> **一句话**：MPC 的优化问题经预测方程展开后，恰好是标准的二次规划(QP)——$U$ 的二次目标 + 线性约束，可以直接交给求解器。

## 0. 为什么学它

MPC 从"建模"到"求解"的必经桥梁：预测方程把代价变成 $U$ 的二次函数，约束变成线性不等式，从而可以调用成熟 QP 求解器（OSQP 等）。不会装配 QP，MPC 就停在"纸上公式"。

## 1. 标准 QP 形式

$$\min_{z} \frac{1}{2} z^\top H z + g^\top z$$

$$\text{s.t. } l_b \le A_c z \le u_b$$

- $z$：决策变量（预测时域内所有控制量 $U$）；
- $H \succ 0$：Hessian（半正定）；
- $g$：梯度（线性项）；
- $A_c$：约束矩阵，$l_b / u_b$ 上下界。

## 2. MPC 到 QP 的推导

由预测方程 $\mathbf{X} = \Phi\mathbf{x}_k + \Gamma \mathbf{U}$ 代入代价：

$$J = (\Phi\mathbf{x}_k + \Gamma \mathbf{U} - \mathbf{X}_{ref})^\top Q (\cdots) + \mathbf{U}^\top R \mathbf{U}$$

展开整理得：

$$H = \Gamma^\top \bar{Q} \Gamma + \bar{R}, \quad g = \Gamma^\top \bar{Q}(\Phi\mathbf{x}_k - \mathbf{X}_{ref})$$

## 3. 最小可手算例子（标量 QP 装配）

**题目**：$N=1$ 标量：$x_{k+1} = x_k + u$（$A=B=1$），$Q = 2$，$R = 1$，$x_{ref} = 5$，$x_k = 1$。求 $H$ 与 $g$。

**步骤**：
1. 预测：$x_{k+1} = 1 + u$；代价 $J = 2(1+u-5)^2 + u^2 = 2(u-4)^2 + u^2$；
2. 展开：$J = 3u^2 - 16u + 32$；
3. 对比标准形式：$H = 6$（$2\times$二次项系数），$g = -16$；$\min_u J$ 在 $u^* = -g/H = 16/6 \approx 2.67$。

**含义**：MPC 每周期做的就是把模型+代价+状态组装成 $(H, g)$ 交给求解器。

## 4. 约束映射

| MPC 约束 | QP 表达 |
|:---|:---|
| 输入幅值 | $U_{min} \le U \le U_{max}$（盒） |
| 输入速率 | 关于 $\Delta U$ 的线性约束 |
| 输出/状态 | $C\Phi\mathbf{x}_k + C\Gamma U$ 界约束 |

## 5. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| QP 只能处理无约束 | QP 专长就是约束二次规划 |
| $H$ 可以不半正定 | $H$ 非半正定问题非凸，求解器不保证 |
| 手写求解器 | 用成熟求解器（OSQP），重点在装配 |

## 6. 检索练习（闭卷）

1. 写出标准 QP 形式；
2. 手算一个标量 $H,g$ 装配；
3. 说明约束映射。

## 7. 通过标准

- 能写出 QP 形式；
- 能手算 $H,g$ 装配；
- 能映射 MPC 约束到 QP。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；下次复习：重做标量 QP 装配。
