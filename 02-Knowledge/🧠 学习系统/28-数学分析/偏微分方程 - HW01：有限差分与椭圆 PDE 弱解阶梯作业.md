---
title: "偏微分方程-题型-有限差分与椭圆PDE弱解阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "偏微分方程作业"
course: "34-偏微分方程"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["偏微分方程", "分离变量法", "有限差分法", "弱解"]
prerequisites: ["[[🗺️ 数学分析学习路径|数学分析]]"]
related: ["[[数值分析-题型-LU分解与共轭梯度法求解器阶梯作业]]"]
upstream: ["[[🗺️ 偏微分方程学习路径|偏微分方程学习路径]]"]
downstream: []
tags: [学习, 34-偏微分方程, 作业, 实战, 阶梯作业]
aliases: ["PDE-HW01-FDM与弱解作业"]
---

# 偏微分方程 - HW01：有限差分与椭圆 PDE 弱解阶梯作业

> 🎯 **作业目标**：分离变量法求解热传导方程、编写有限差分 (FDM) 求解二维 Poisson 方程，并证明 Lax-Milgram 定理。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-pde/hw01_fdm_poisson.ipynb`
- **开源标杆仓库**：[FEniCS Project (Finite Element Method)](https://fenicsproject.org/) / SciPy PDE Solvers
- **核心依赖**：`scipy`, `numpy`, `matplotlib`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | Fourier 级数解收敛 | 分离变量法求解一维热传导方程 $\frac{\partial u}{\partial t} = k \frac{\partial^2 u}{\partial x^2}$ 级数解。 |
| 🟡 **L2 - Medium Baseline** | 差分误差 $O(h^2)$ | **有限差分法 (FDM)** 编写 Python 脚本模拟二维 Laplace / Poisson 方程网格解。 |
| 🔴 **L3 - Strong Baseline** | 严密弱解存在性证明 | 严格书写 **2D 椭圆型 PDE 弱解存在唯一性** (Lax-Milgram 定理与 Sobolev 空间 $H_0^1$)。 |
| 👑 **L4 - Boss Baseline** | FEM 有限元求解 | 使用 FEniCS 库编写有限元 (FEM) 求解器，对复杂多边形边界 PDE 求解。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_fdm_poisson_solver():
    from pde_solvers import solve_poisson_2d_fdm
    # 在 [0,1]x[0,1] 网格上求解 -Laplacian(u) = 1, 边界 u=0
    N = 50
    u_grid = solve_poisson_2d_fdm(N=N, source_val=1.0)
    
    assert u_grid.shape == (N, N)
    # 中心点应当具有最大正向响应
    assert u_grid[N//2, N//2] > u_grid[5, 5] > 0.0
```

---

## 🃏 Anki 卡片

- Q: 偏微分方程中的“弱解 (Weak Solution)”概念为何比古典解 (Classical Solution) 更具普遍性与工程适用性？
- A: 古典解要求函数具有足够阶数的连续偏导数；而弱解通过分部积分将导数转移到光滑测试函数 (Test Function) 上，允许在 Sobolev 空间中包含跳跃不连续点或外力冲击（如激波或点源输入），极大地扩展了 PDE 的可解范围。
