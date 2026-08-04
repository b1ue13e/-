---
title: "最优化方法-题型-内点法与ADMM求解器手撕阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "最优化方法作业"
course: "07-最优化方法"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["凸优化", "KKT条件", "ADMM算法"]
prerequisites: ["[[07-最优化方法/01-数学基础/🔧 第一阶段：数学基础|最优化方法学习路径]]"]
related: ["[[机器学习-题型-李宏毅式分类与深层模型阶梯作业]]"]
upstream: ["[[07-最优化方法/01-数学基础/🔧 第一阶段：数学基础|最优化方法学习路径]]"]
downstream: []
tags: [学习, 07-最优化方法, 作业, 实战, 阶梯作业]
aliases: ["EE364a-HW-求解器作业"]
---

# 最优化方法 - HW03：内点法与 ADMM 求解器手撕阶梯作业

> 🎯 **作业目标**：手写 Backtracking Line Search 梯度下降、拟牛顿法 (L-BFGS) 与交替方向乘子法 (ADMM)，求解分布式 Lasso 与全变分去噪问题。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-opt/hw03_convex_opt.ipynb`
- **开源标杆仓库**：[cvxgrp/cvxpy](https://github.com/cvxgrp/cvxpy) (Stanford EE364a Boyd)
- **核心依赖**：`cvxpy`, `numpy`, `scipy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标残差 / 收敛度 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 求解精度 1e-4 | 使用 CVXPY 建模二次规划 (QP) 与线性规划 (LP) 问题并调用 ECOS / OSQP 求解。 |
| 🟡 **L2 - Medium Baseline** | 迭代步数 < 100 | **手写梯度下降法**（带 Backtracking Line Search）与标准牛顿法（计算 Hessian 矩阵与 KKT 系统）。 |
| 🔴 **L3 - Strong Baseline** | **手撕 L-BFGS & 障碍法** | 手写拟牛顿法 L-BFGS 与内点障碍法 (Barrier Method) 求解二次约束二次规划 (QCQP)。 |
| 👑 **L4 - Boss Baseline** | **手撕 ADMM 分布式求解** | 从零手撕 ADMM (Alternating Direction Method of Multipliers) 算法求解图像 Total Variation 去噪。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_admm_lasso_against_cvxpy():
    from opt_solvers import admm_lasso
    import cvxpy as cp
    
    # 构造标准数据
    X = np.random.randn(50, 20)
    y = np.random.randn(50)
    gamma = 0.1
    
    # CVXPY 参考标杆
    beta_var = cp.Variable(20)
    prob = cp.Problem(cp.Minimize(0.5 * cp.sum_squares(X @ beta_var - y) + gamma * cp.norm1(beta_var)))
    prob.solve()
    ref_beta = beta_var.value
    
    # 自写 ADMM
    my_beta = admm_lasso(X, y, gamma=gamma, rho=1.0, max_iter=2000)
    
    np.testing.assert_allclose(my_beta, ref_beta, atol=1e-3, err_msg="ADMM 解必须与 CVXPY 标杆求解器收敛结果一致")
```

---

## 🃏 Anki 卡片

- Q: ADMM (交替方向乘子法) 为什么特别适合求解高维 $L_1$ 正则化 (如 Lasso) 和分布式优化问题？
- A: ADMM 将原问题拆分为两个交替更新的子问题：一个子问题依赖二次可导项（有解析解或线性方程求解），另一个子问题针对非光滑 $L_1$ 项（使用软阈值算子 Soft Thresholding 极快求解），实现了变量解耦与并行扩展。
