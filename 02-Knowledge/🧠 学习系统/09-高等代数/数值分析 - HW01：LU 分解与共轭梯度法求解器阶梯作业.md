---
title: "数值分析-题型-LU分解与共轭梯度法求解器阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "数值分析作业"
course: "35-数值分析"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: intermediate
importance: A
concept: ["数值分析", "LU分解", "共轭梯度法", "RK4数值解"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/09-高等代数/🗺️ 高等代数学习路径|高等代数]]"]
related: ["[[最优化方法-题型-内点法与ADMM求解器手撕阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/28-数学分析/🗺️ 数学分析学习路径|数值分析学习路径]]"]
downstream: []
tags: [学习, 35-数值分析, 作业, 实战, 阶梯作业]
aliases: ["Num-HW01-LU与CG求解器作业"]
---

# 数值分析 - HW01：LU 分解与共轭梯度法求解器阶梯作业

> 🎯 **作业目标**：手写 Newton-Raphson 求根、带主元的 LU / Gram-Schmidt QR 分解、Cubic Spline 插值以及共轭梯度法 (Conjugate Gradient) 求解器。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-num/hw01_lu_cg.ipynb`
- **开源标杆仓库**：[UC Berkeley Python Numerical Methods](https://pythonnumericalmethods.berkeley.edu/)
- **核心依赖**：`scipy`, `numpy`, `matplotlib`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 迭代收敛 1e-6 | 实现二分法与牛顿-拉夫逊法 (Newton-Raphson) 求解高次方程根。 |
| 🟡 **L2 - Medium Baseline** | 相对误差 < 1e-5 | **手写带全选主元的 LU 分解** 与 Gram-Schmidt QR 矩阵数值分解。 |
| 🔴 **L3 - Strong Baseline** | 样条连续可微 $C^2$ | **手写三次样条 (Cubic Spline) 插值** 与 4 阶 Runge-Kutta (RK4) 求解微分方程。 |
| 👑 **L4 - Boss Baseline** | 迭代步数 < $N$ | **手撕共轭梯度法 (Conjugate Gradient)** 求解超大规模稀疏正定矩阵方程 $Ax = b$。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_conjugate_gradient_solver():
    from num_solvers import conjugate_gradient
    # 构造正定对称矩阵 A
    A_raw = np.random.randn(20, 20)
    A = A_raw.T @ A_raw + np.eye(20)
    b = np.random.randn(20)
    
    x_cg = conjugate_gradient(A, b, tol=1e-6)
    x_exact = np.linalg.solve(A, b)
    
    np.testing.assert_allclose(x_cg, x_exact, atol=1e-5, err_msg="CG 算法求解结果必须与 np.linalg.solve 解完全一致")
```

---

## 🃏 Anki 卡片

- Q: 为什么共轭梯度法 (Conjugate Gradient, CG) 求解 $N \times N$ 正定对称矩阵 $Ax=b$ 时，比普通最速下降法 (Steepest Descent) 收敛快得多？
- A: 最速下降法的搜索方向在窄谷中容易产生“之”字形折线震荡；而 CG 法保证搜索方向关于矩阵 $A$ 相互 $A$-正交 (Conjugate)，每个方向仅需搜索一次，在理论上最多 $N$ 步即可精确收敛。
