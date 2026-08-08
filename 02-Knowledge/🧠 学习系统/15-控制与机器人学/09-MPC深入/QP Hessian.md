---
type: study
topic: "QP Hessian"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-08
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段9-MPC深入]]"
flow: knowledge
kind: concept
concept: ["Hessian", "正定性", "Toeplitz结构"]
prerequisites: ["QP标准形式", "预测方程"]
related: ["QP标准形式", "稀疏QP", "MPC代价函数"]
upstream: ["[[QP标准形式]]"]
source: "Borrelli, Predictive Control；OSQP 文档"
tags: [学习, 控制与机器人学, MPC]
---

# QP Hessian

> **一句话**：QP 的 $H$ 矩阵（Hessian）编码了"代价曲面"的曲率——$H = \Gamma^\top \bar{Q} \Gamma + \bar{R}$，正定性决定问题是否凸、求解是否唯一。

## 0. 为什么学它

$H$ 是 QP 装配的核心：它决定解的唯一性（正定 → 唯一全局最优）、条件数（影响求解速度）与稀疏结构（影响内存）。看懂 $H$ 的结构，才能理解"为什么 MPC 的 QP 好解"。

## 1. Hessian 的构成

$$H = \Gamma^\top \bar{Q} \Gamma + \bar{R}$$

- $\Gamma$：受控响应矩阵（下三角 Toeplitz，见[[预测方程]]）；
- $\bar{Q}$：块对角状态权重（$\text{blkdiag}(Q,\dots,Q)$）；
- $\bar{R}$：块对角控制权重（$\text{blkdiag}(R,\dots,R)$）。

## 2. 正定性与凸性

- 若 $R \succ 0$，则 $\bar{R} \succ 0$ → $H \succ 0$（严格正定）→ QP 严格凸 → **唯一全局最优**；
- 若 $R \succeq 0$ 但 $\Gamma$ 不满秩（某些状态不可控）→ $H$ 半正定 → 解不唯一。

## 3. 最小可手算例子（标量 H）

**题目**：$N=2$，标量系统 $\Gamma = [1; 2]$（两步增益），$Q = 3$，$R = 1$。求 $H$。

**步骤**：
1. $\bar{Q} = \text{blkdiag}(3,3)$，$\Gamma = [1, 2]^\top$；
2. $\Gamma^\top \bar{Q} \Gamma = 1\cdot3\cdot1 + 2\cdot3\cdot2 = 3 + 12 = 15$；
3. $H = 15 + 1 = 16 > 0$ 正定——问题凸，解唯一。

**含义**：$H$ 的数值大小反映"代价曲面"有多陡，影响求解器收敛步数。

## 4. 结构特性

| 特性 | 说明 |
|:---|:---|
| 带状/块结构 | $\Gamma$ 下三角 → $H$ 带状（见[[稀疏QP]]） |
| 时不变 | 无约束时 $H$ 固定，可预分解加速 |
| 条件数 | 权重悬殊 → 病态 → 预条件（见[[一阶QP]]） |

## 5. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| $H$ 任意正定即可 | $H$ 由模型+权重决定，不能随意设 |
| $H$ 必须严格正定 | $R \succ 0$ 通常保证；半正定时解不唯一需处理 |
| $H$ 每次重算 | 无约束/固定参考时 $H$ 固定，可缓存 |

## 6. 检索练习（闭卷）

1. 写出 $H$ 的构成公式；
2. 手算标量 $H$；
3. 说明正定性与凸性关系。

## 7. 通过标准

- 能写出 $H$ 构成；
- 能手算 $H$；
- 能解释正定性。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；下次复习：重做 H 手算。
