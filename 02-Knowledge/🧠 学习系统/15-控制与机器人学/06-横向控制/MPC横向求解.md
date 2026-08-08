---
type: study
topic: "MPC横向求解"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: derivation
concept: ["MPC横向", "QP求解", "滚动优化"]
prerequisites: ["MPC横向预测", "QP标准形式"]
related: ["MPC横向预测", "MPC横向约束"]
upstream: ["[[MPC横向预测]]"]
source: "PythonRobotics model_predictive_control.py; OSQP/CVXPY"
tags: [学习, 控制与机器人学, MPC横向]
---

# MPC横向求解

## 0. 为什么学它

预测、约束、代价都齐了，最后一步是**求解 QP**：在约束下最小化代价，得到最优转向序列，执行第一步，下周期重复。理解求解流程与实时性要求，才能把 MPC 跑在真实控制器上。

## 1. 核心求解流程

1. **组装 QP**：把预测方程代入代价 → $\min_z \frac12 z^\top H z + c^\top z$ s.t. $A_z z\le b_z$（$z$ 为转向序列）；
2. **求解**：用 QP 求解器（OSQP/quadprog/CVXPY）得 $z^*=(\delta_0^*,\dots,\delta_{N-1}^*)$；
3. **执行**：只应用 $\delta_0^*$；
4. **滚动**：下一采样周期用新状态重新组装求解（滚动时域）。

**实时性**：$N$ 与求解器速度决定周期；热启动（上周期解作初值）显著加速。

**代码示意**（PythonRobotics 思路）：每步 `solve_qp(H, f, constraints)` → 取首元素。

## 2. 最小可手算例子（概念验证）

**题目**：$N=10$，为何只执行 $\delta_0^*$？

**解**：模型有误差、扰动未知，后续最优解随新状态改变——"只执行第一步，重算下一串"（滚动）保证鲁棒性；全执行则误差累积 ✓。

**易错点**：未热启动导致求解慢；约束矩阵组装错误；忽略求解超时（早期终止，见 [[早期终止]]）。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 一次解完执行全程 | 滚动执行第一步 |
| 求解器随便用 | 需实时性评估（嵌入式用 OSQP 等） |
| 忽略初始可行解 | 热启动/可行初始解加速 |

## 4. 与后续知识连接

- [[QP标准形式]]、[[OSQP]]：求解工具；
- [[早期终止]]、[[热启动]]：实时技巧；
- [[滚动优化]]：一般机制。

## 5. 检索练习（闭卷）

1. 描述四步求解流程；
2. 解释滚动执行；
3. 说明热启动；
4. 实时性关键因素。

## 6. 通过标准

- 能组装并求解横向 QP；
- 能实现滚动优化；
- 能评估实时性。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重写流程；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
