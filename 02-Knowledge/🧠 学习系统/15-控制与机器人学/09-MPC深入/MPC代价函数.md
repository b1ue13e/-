---
type: study
topic: "MPC代价函数"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-08
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段9-MPC深入]]"
flow: knowledge
kind: concept
concept: ["二次代价", "权重矩阵", "LQR"]
prerequisites: ["模型预测控制(MPC)", "预测方程"]
related: ["QP标准形式", "终端代价", "时域设计"]
upstream: ["[[模型预测控制(MPC)]]"]
source: "Rawlings, Model Predictive Control；Borrelli, Predictive Control"
tags: [学习, 控制与机器人学, MPC]
---

# MPC代价函数

> **一句话**：MPC 的"目标函数"——状态误差与控制能耗的加权二次和，$Q$/$R$ 权重决定控制器"性格"。

## 0. 为什么学它

代价函数是 MPC 优化的"裁判"：它决定控制器是"盯紧误差"还是"省着能耗"，也是 QP 装配的核心输入。$Q$/$R$ 不会调，MPC 要么动作太猛要么反应迟钝——本卡是阶段 5 LQR 代价的 MPC 推广。

## 1. 标准形式

$$\min_{u} J = \sum_{k=0}^{N-1} \Big( \lVert \mathbf{x}_{k+1} - \mathbf{x}_{ref} \rVert_Q^2 + \lVert \mathbf{u}_k \rVert_R^2 \Big)$$

展开写：

$$J = \sum_{k=0}^{N-1} \big( \mathbf{e}_k^\top Q \mathbf{e}_k + \mathbf{u}_k^\top R \mathbf{u}_k \big), \quad \mathbf{e}_k = \mathbf{x}_{k+1} - \mathbf{x}_{ref,k+1}$$

## 2. 权重矩阵

| 矩阵 | 作用 | 调参直觉 |
|:---|:---|:---|
| $Q \succeq 0$ | 状态误差惩罚 | $Q$ 大 → 跟踪紧、动作猛 |
| $R \succ 0$ | 控制量惩罚 | $R$ 大 → 省能耗、响应钝 |
| 对角项 | 各状态重要性 | 位置/航向/速度分别加权 |

## 3. 最小可手算例子（权重对比）

**题目**：标量系统，$Q \in \{1, 10\}$，$R = 1$，误差 $e = 2$，控制 $u = 1$。比较两种权重下的单步代价。

**步骤**：
1. $Q=1$：$J = 1\cdot2^2 + 1\cdot1^2 = 5$；
2. $Q=10$：$J = 10\cdot4 + 1 = 41$——误差被更重惩罚 → 优化器倾向更大 $u$ 压误差；
3. 结论：$Q/R$ 比值决定"误差 vs 能耗"的权衡，与 LQR 调参一致（见[[LQR调参]]）。

**含义**：代价函数是"性格旋钮"，同样的系统、不同的 $Q/R$ 得到完全不同的控制行为。

## 4. 终端项（稳定性关键）

$$J_N = \lVert \mathbf{x}_N - \mathbf{x}_{ref,N} \rVert_P^2$$

$P$ 为终端代价矩阵（见[[终端代价]]），弥补有限时域的"尾部截断"。

## 5. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 权重越大越好 | 权重过大 → 输入饱和、数值病态 |
| 只调 $Q$ 不动 $R$ | 有效参数是 $Q/R$ 比值与相对权重 |
| 忽略终端项 | 无终端项有限时域 MPC 可能不稳定 |

## 6. 检索练习（闭卷）

1. 写出 MPC 代价函数；
2. 手算 $Q/R$ 对比；
3. 说明终端项的作用。

## 7. 通过标准

- 能写出代价函数并解释三项；
- 能手算权重对比；
- 能解释终端项必要性。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；下次复习：重做权重手算。
