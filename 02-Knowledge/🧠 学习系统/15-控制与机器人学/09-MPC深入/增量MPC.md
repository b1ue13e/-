---
type: study
topic: "增量MPC"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-08
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段9-MPC深入]]"
flow: knowledge
kind: concept
concept: ["增量控制", "积分内置", "抗饱和"]
prerequisites: ["离散状态空间"]
related: ["MPC积分", "输入速率约束", "松弛变量"]
upstream: ["[[09-MPC深入/离散状态空间]]"]
source: "Rawlings, Model Predictive Control；工业 MPC（DMC/QDMC 传统）"
tags: [学习, 控制与机器人学, MPC]
---

# 增量MPC

> **一句话**：用控制量的"变化量"$\Delta u$ 代替"控制量"$u$ 作为决策变量——积分作用、抗饱和、速率约束一次全解决。

## 0. 为什么学它

工业与车辆 MPC 的实际实现几乎都用增量形式——它不是理论炫技，而是解决三个真问题：稳态误差（积分）、约束饱和、速率约束。不掌握增量 MPC，就写不出能上车的 MPC。

## 1. 增量形式

定义 $\Delta \mathbf{u}_k = \mathbf{u}_k - \mathbf{u}_{k-1}$，增广状态：

$$\tilde{\mathbf{x}}_k = \begin{bmatrix} \mathbf{x}_k \\ \mathbf{u}_{k-1} \end{bmatrix}$$

$$\tilde{\mathbf{x}}_{k+1} = \begin{bmatrix} A & B \\ 0 & I \end{bmatrix} \tilde{\mathbf{x}}_k + \begin{bmatrix} B \\ I \end{bmatrix} \Delta \mathbf{u}_k$$

代价中惩罚 $\Delta \mathbf{u}$ 而非 $\mathbf{u}$。

## 2. 增量 MPC 的四大好处

| 好处 | 机制 |
|:---|:---|
| 积分作用 | 状态含 $u_{k-1}$ → 输出通道有积分 → 无稳态误差 |
| 抗饱和 | 饱和时 $\Delta u$ 自动为 0，无积分累积问题 |
| 速率约束 | $\Delta u$ 直接受幅值约束 = 输入速率约束（见[[输入速率约束]]） |
| 平滑 | 惩罚 $\Delta u$ → 控制量变化平缓 |

## 3. 最小可手算例子（抗饱和）

**题目**：$u$ 已饱和在上限 3，MPC 还想加码。增量形式如何处理？

**步骤**：
1. 当前 $u_{k-1} = 3$（饱和）；
2. 幅值约束：$3 + \Delta u \le 3 \Rightarrow \Delta u \le 0$；
3. 优化器只能选 $\Delta u \le 0$——**无法继续累积**，饱和即自动停止加码，恢复后立即响应。

**含义**：对比普通积分（饱和时继续累积导致 windup），增量形式天然免疫——这就是"增量 MPC 抗饱和"的机制。

## 4. 约束表达

- 幅值约束：$u_{min} \le u_{k-1} + \sum \Delta u_i \le u_{max}$（关于 $\Delta u$ 的线性约束）；
- 速率约束：$\Delta u_{min} \le \Delta u \le \Delta u_{max}$。

## 5. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 增量 MPC 更复杂 | 状态增广后 QP 结构更规整，实现并不复杂 |
| 增量只解决速率 | 积分/抗饱和/平滑一并解决 |
| 增量影响稳态 | 恰相反，增量内置积分 → 无偏 |

## 6. 工程地位

**增量 MPC 是工业/车辆 MPC 的默认形态**：
- 线性车辆 MPC 普遍用增量模型（见[[线性车辆MPC]]）；
- 与扰动模型配合，稳态精度 + 鲁棒性兼得。

## 7. 检索练习（闭卷）

1. 写出增量增广状态方程；
2. 手算饱和场景的 $\Delta u$ 限制；
3. 说明四大好处。

## 8. 通过标准

- 能写出增量模型；
- 能手算抗饱和机制；
- 能说明工程地位。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；下次复习：重做抗饱和手算。
