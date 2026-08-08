---
type: study
topic: "MPC车辆工程实现"
course: "控制与机器人学"
created: 2026-08-09
updated: 2026-08-09
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段11-工程实战]]"
flow: knowledge
kind: concept
concept: ["MPC实现", "滚动优化", "部署"]
prerequisites: ["模型预测控制(MPC)", "QP标准形式", "预测方程"]
related: ["横向控制工程实现", "优化求解器"]
upstream:
  - "[[模型预测控制(MPC)]]"
  - "[[QP标准形式]]"
source: "PythonRobotics（MIT）：model_predictive_speed_and_steering_control.py；CasADi 官方 MPC 示例"
tags: [学习, 控制与机器人学, 工程实战, MPC]
---

# MPC车辆工程实现

## 0. 为什么学它

阶段 9 学了 MPC 的理论（预测方程、QP、滚动优化），本卡解决**落地问题**：车辆模型怎么选、约束怎么进 QP、求解器怎么接、实车部署有哪些坑。它是阶段作业-09 的工程实现侧，也是"理论 MPC → 能跑的控制器"的最后一步。

## 1. 实现四步

1. **模型**：线性化/非线性车辆模型（自行车模型离散化），定状态 $[x, y, \psi, v]$、控制 $[\delta, a]$；
2. **预测方程**：把 N 步预测写成 $z = \Psi z_k + \Theta u$ 矩阵形式（见 [[预测方程|预测方程]]）；
3. **QP 装配**：代价函数 + 约束（输入幅值/速率、状态软约束）写成 QP 标准形式（见 [[QP标准形式|QP标准形式]]）；
4. **滚动求解**：每步解 QP，只执行第一步控制，窗口前移。

## 2. 最小可运行例子（CVXPY 一步 MPC）

```python
import cvxpy as cp
import numpy as np

N = 10          # 预测时域
A, B = np.array([[1., 0.1], [0., 1.]]), np.array([[0.], [0.1]])  # 一维速度模型
x0 = np.array([0.0, 0.0])   # [位置, 速度]
x_ref = 5.0     # 目标位置
Q, R = 1.0, 0.1

x = cp.Variable((2, N+1))
u = cp.Variable((1, N))
cost = sum(Q * (x[0, k] - x_ref)**2 + R * u[0, k]**2 for k in range(N))
constraints = [x[:, 0] == x0]
for k in range(N):
    constraints += [x[:, k+1] == A @ x[:, k] + B @ u[:, k]]
    constraints += [cp.abs(u[0, k]) <= 1.0]   # 输入幅值约束
prob = cp.Problem(cp.Minimize(cost), constraints)
prob.solve()
print("第一步控制:", u.value[0, 0])
```

**运行说明**：`pip install cvxpy numpy` 后运行；这是 MPC"预测 N 步 → 解 QP → 只取第一步"的最小闭环。

## 3. 部署要点

| 要点 | 说明 |
|:---|:---|
| 求解耗时 | 实时系统要测每步求解时间（见 [[优化求解器\|优化求解器]]） |
| 软约束 | 状态约束用软约束（松弛变量）避免不可行（见 [[松弛变量\|松弛变量]]） |
| 参数时变 | 车速变化 → 模型线性化点变化，需在线重线性化 |
| 传感器接入 | 用估计状态（EKF，见 [[导航定位\|导航定位]]）而非理想状态 |

## 4. 常见坑

| 坑 | 对策 |
|:---|:---|
| QP 不可行（约束过紧） | 加软约束/放宽约束/增大预测时域 |
| 求解超时 | 缩短时域 N、用 qpOASES/OSQP、热启动 |
| 模型失配 → 跟踪偏差 | 在线重线性化 + 前馈修正 |
| 滚动优化抖动 | 加控制增量代价（$\Delta u$ 惩罚） |

## 5. 检索练习（闭卷）

1. 说出 MPC 实现四步；
2. 跑通 CVXPY 最小 MPC 例子；
3. 软约束为什么必要？
4. 部署时求解耗时/模型时变怎么处理？

## 6. 通过标准

- 能装配车辆 MPC 的 QP 并跑通；
- 能做滚动优化闭环并测跟踪误差；
- 能处理不可行、超时、模型失配问题；
- 能把 MPC 接到估计器做闭环部署。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：用 PythonRobotics `model_predictive_speed_and_steering_control.py` 复现并扫预测时域；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；
- 关联：[[模型预测控制(MPC)\|模型预测控制]]、[[横向控制工程实现\|横向控制工程实现]]。
