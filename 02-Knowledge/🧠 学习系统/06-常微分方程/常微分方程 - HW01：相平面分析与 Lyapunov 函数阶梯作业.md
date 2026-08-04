---
title: "常微分方程-题型-相平面分析与Lyapunov函数阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "常微分方程作业"
course: "06-常微分方程"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: intermediate
importance: A
concept: ["常微分方程", "相平面分析", "李雅普诺夫稳定性"]
prerequisites: ["[[🗺️ 常微分方程学习路径]]"]
related: ["[[最优化方法-题型-内点法与ADMM求解器手撕阶梯作业]]"]
upstream: ["[[🗺️ 常微分方程学习路径]]"]
downstream: []
tags: [学习, 06-常微分方程, 作业, 实战, 阶梯作业]
aliases: ["ODE-HW01-相平面与Lyapunov作业"]
---

# 常微分方程 - HW01：相平面分析与 Lyapunov 函数阶梯作业

> 🎯 **作业目标**：手算一阶与二阶线性 ODE、绘制自治系统相平面图 (Phase Portrait)，并构造 Lyapunov 函数证明非线性系统稳定性。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-ode/hw01_phase_portrait.ipynb`
- **开源标杆仓库**：[MIT 18.03 Differential Equations](https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/)
- **核心依赖**：`sympy`, `matplotlib`, `scipy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验收标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | SymPy 解析求解通过 | 用 SymPy 求解可分离变量 ODE 与一阶线性 ODE $y' + P(x)y = Q(x)$ 通解。 |
| 🟡 **L2 - Medium Baseline** | 奇点分类正确 (鞍点/焦点) | 使用 Python `matplotlib.quiver` 绘制二阶自治系统 $\dot{x} = Ax$ 的相平面轨迹图。 |
| 🔴 **L3 - Strong Baseline** | 渐近稳定性严格证明 | **构造 Lyapunov 函数 $V(x,y)$**，证明非线性系统（如带阻尼摆方程）在原点的渐近稳定性。 |
| 👑 **L4+ - 极客拓展** | 步长控制误差 $O(h^4)$ | **手写自适应步长 RK4 (Runge-Kutta)** 数值求解器，模拟洛伦兹吸引子 (Lorentz Attractor) 混沌轨迹。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_rk4_solver_accuracy():
    from ode_solvers import rk4_step
    # dy/dt = -2y, y(0)=1 => y(t) = exp(-2t)
    f = lambda t, y: -2 * y
    t0, y0, h = 0.0, 1.0, 0.1
    t1, y1 = rk4_step(f, t0, y0, h)
    
    expected = np.exp(-0.2)
    assert np.isclose(y1, expected, atol=1e-5), "RK4 单步计算误差必须小于 1e-5"
```

---

## 🃏 Anki 卡片

- Q: 李雅普诺夫 (Lyapunov) 第一方法（直接法）判定平衡状态渐近稳定的充要充分条件是什么？
- A: 若存在连续可微的正定函数 $V(x) > 0 (x \neq 0)$，使得其沿系统轨迹的导数 $\dot{V}(x) = \nabla V(x) \cdot f(x)$ 为严格负定 ($\dot{V}(x) < 0$)，则原点平衡态是渐近稳定的。
