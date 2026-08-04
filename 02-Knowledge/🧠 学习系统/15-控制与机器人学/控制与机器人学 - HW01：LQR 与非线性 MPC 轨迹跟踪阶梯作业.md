---
title: "控制与机器人学-题型-LQR与非线性MPC轨迹跟踪阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "控制与机器人学作业"
course: "15-控制与机器人学"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["机器人学", "LQR控制", "MPC轨迹跟踪"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/17-机器学习/01-基础概念/🌱 第一阶段：基础概念|控制与机器人学学习路径]]"]
related: ["[[最优化方法-题型-内点法与ADMM求解器手撕阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/17-机器学习/01-基础概念/🌱 第一阶段：基础概念|控制与机器人学学习路径]]"]
downstream: []
tags: [学习, 15-控制与机器人学, 作业, 实战, 阶梯作业]
aliases: ["MIT-6.832-LQR与MPC作业"]
---

# 控制与机器人学 - HW01：LQR 与非线性 MPC 轨迹跟踪阶梯作业

> 🎯 **作业目标**：调节双足/倒立摆 PID 参数、求解 LQR (Linear Quadratic Regulator) 状态反馈矩阵，并在 Drake / PyBullet 仿真环境中实现 MPC 轨迹跟踪。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-robotics/hw01_lqr_mpc.ipynb`
- **开源标杆仓库**：[Drake-Course/Underactuated Robotics](https://underactuated.csail.mit.edu/) (MIT 6.832)
- **核心依赖**：`pydrake` / `pybullet`, `scipy`, `numpy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 稳定性指标 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 倒立摆维持 10s 不倒 | 搭建一维倒立摆系统 PID 控制器，调整 P, I, D 增益参数使其稳定在原点。 |
| 🟡 **L2 - Medium Baseline** | 求解代数 Riccati 方程 | 构建连续/离散时间状态空间模型 $\dot{x} = Ax + Bu$，手算求解 LQR 增益矩阵 $K$。 |
| 🔴 **L3 - Strong Baseline** | 轨迹跟踪误差 < 5cm | **在 Python/Drake 中实现非线性 MPC (Model Predictive Control)**，实时优化控制输入序列。 |
| 👑 **L4 - Boss Baseline** | 导航成功率 ≥ 95% | 结合 EKF-SLAM 在未知环境仿真中实现双足/四足机器人地图构建与自主避障导航。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_lqr_gain_matrix():
    from robotics_solvers import solve_lqr
    A = np.array([[0, 1], [0, -0.1]])
    B = np.array([[0], [1]])
    Q = np.eye(2)
    R = np.array([[1]])
    
    K = solve_lqr(A, B, Q, R)
    # 验证闭环系统 A - B*K 的特征值必须完全在左半平面 (稳定)
    eigvals = np.linalg.eigvals(A - B @ K)
    assert np.all(eigvals.real < 0), "LQR 闭环系统特征值必须具有负实部（渐近稳定）"
```

---

## 🃏 Anki 卡片

- Q: 为什么模型预测控制 (MPC) 相较于经典 LQR 控制在机器人复杂运动控制（如无人机避障/双足行走）中具有独特优势？
- A: LQR 仅适用于无约束线性系统；而 MPC 能够在预测时域内显式地将执行器物理限制（如电机最大转矩、速度上限）以及环境几何障碍物作为硬约束 (Hard Constraints) 纳入凸/非凸优化中求解。
