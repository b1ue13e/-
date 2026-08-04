---
title: "运筹学-题型-单纯形法与分支定界TSP阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "运筹学作业"
course: "29-运筹学"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: intermediate
importance: A
concept: ["运筹学", "单纯形法", "分支定界", "整数规划"]
prerequisites: ["[[07-最优化方法/01-数学基础/🔧 第一阶段：数学基础|最优化方法]]"]
related: ["[[最优化方法-题型-内点法与ADMM求解器手撕阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/29-运筹学/🗺️ 运筹学学习路径|运筹学学习路径]]"]
downstream: []
tags: [学习, 29-运筹学, 作业, 实战, 阶梯作业]
aliases: ["OR-HW01-单纯形与分支定界作业"]
---

# 运筹学 - HW01：单纯形法与分支定界 TSP 阶梯作业

> 🎯 **作业目标**：使用 PuLP 建模 LP/MILP 问题、手写表格式单纯形法 (Simplex Method)，并实现分支定界法 (Branch & Bound) 求解 TSP 旅行商问题。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-or/hw01_simplex_bb.ipynb`
- **开源标杆仓库**：[google/or-tools](https://github.com/google/or-tools) / `coin-or/pulp`
- **核心依赖**：`pulp`, `scipy`, `numpy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | PuLP 求解器通过 | 使用 PuLP 建模生产排程与资源分配线性规划，调用 CBC 求解器获得最优解。 |
| 🟡 **L2 - Medium Baseline** | 进基出基迭代无误 | **手写表格式单纯形法 (Tableau Simplex Method)**，正确判定退化与无界解。 |
| 🔴 **L3 - Strong Baseline** | 剪枝策略正确 | **手撕分支定界法 (Branch and Bound)** 求解 0-1 背包问题与 TSP (旅行商问题)。 |
| 👑 **L4 - Boss Baseline** | 求解规模 > 1000 变量 | 实现 Column Generation (列生成) 算法与 Dantzig-Wolfe 分解求解 Cutting Stock 下料问题。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_manual_simplex_vs_scipy():
    from or_solvers import manual_simplex
    from scipy.optimize import linprog
    
    c = np.array([-1, -2])
    A = np.array([[1, 1], [1, 3]])
    b = np.array([4, 9])
    
    # 手写单纯形求解
    res_my = manual_simplex(c, A, b)
    res_scipy = linprog(c, A_ub=A, b_ub=b, method='highs')
    
    np.testing.assert_allclose(res_my.fun, res_scipy.fun, atol=1e-5, err_msg="手写单纯形法最小值必须与 scipy.optimize.linprog 求解一致")
```

---

## 🃏 Anki 卡片

- Q: 在整数规划分支定界法 (Branch and Bound) 中，决定一个节点被剪枝 (Pruning) 的三种可能情况是什么？
- A: 1) **可行性剪枝**：松弛 LP 子问题不可行；2) **界限剪枝**：松弛 LP 子问题的最优目标值劣于当前已知的最佳整数可行解（下界/上界）；3) **整数解剪枝**：松弛 LP 解直接为整数解，更新当前最佳解并停止分支。
