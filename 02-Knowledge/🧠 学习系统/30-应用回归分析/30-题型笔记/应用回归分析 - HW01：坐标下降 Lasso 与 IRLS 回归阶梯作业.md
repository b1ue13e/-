---
title: "应用回归分析-题型-坐标下降Lasso与IRLS回归阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "应用回归分析作业"
course: "30-应用回归分析"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: intermediate
importance: A
concept: ["应用回归分析", "OLS回归", "Lasso回归", "GLM"]
prerequisites: ["[[🗺️ 概率论与数理统计学习路径|概率统计]]"]
related: ["[[机器学习-题型-李宏毅式分类与深层模型阶梯作业]]"]
upstream: ["[[🗺️ 应用回归分析学习路径|应用回归分析学习路径]]"]
downstream: []
tags: [学习, 30-应用回归分析, 作业, 实战, 阶梯作业]
aliases: ["Regression-HW01-Lasso与IRLS作业"]
---

# 应用回归分析 - HW01：坐标下降 Lasso 与 IRLS 回归阶梯作业

> 🎯 **作业目标**：OLS 拟合诊断与 VIF 方差膨胀因子求解、手撕坐标下降法 (Coordinate Descent Lasso)，以及手写迭代加权最小二乘法 (IRLS) 求解 GLM。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-reg/hw01_lasso_irls.ipynb`
- **开源标杆仓库**：[Penn State STAT 501 / Stanford STATS 203](https://online.stat.psu.edu/stat501/)
- **核心依赖**：`statsmodels`, `scikit-learn`, `numpy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | OLS 参数解释无误 | `statsmodels` 拟合 OLS，绘制残差图诊断异方差性，解释 $R^2$ 与 p-value。 |
| 🟡 **L2 - Medium Baseline** | VIF 计算正确 | **手写 VIF (Variance Inflation Factor)** 多重共线性诊断算法。 |
| 🔴 **L3 - Strong Baseline** | 稀疏解求解收敛 | **手撕坐标下降法 (Coordinate Descent)** 实现 Lasso ($L_1$) 回归与 Soft Thresholding 算子。 |
| 👑 **L4 - Boss Baseline** | GLM 参数收敛 | **手撕迭代加权最小二乘法 (IRLS)** 求解 Logistic / Poisson 广义线性模型 (GLM)。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_coordinate_descent_lasso_sparsity():
    from reg_solvers import lasso_coordinate_descent
    X = np.random.randn(100, 20)
    # 真实参数只有前 3 个是非零
    true_beta = np.array([3.0, -2.0, 1.5] + [0.0]*17)
    y = X @ true_beta + np.random.normal(0, 0.1, 100)
    
    beta_est = lasso_coordinate_descent(X, y, alpha=0.2)
    # 期望估算出的参数中绝大部分为 0
    zero_count = np.sum(np.isclose(beta_est[3:], 0.0, atol=1e-2))
    assert zero_count >= 15, "Lasso 回归坐标下降法必须能够将绝大部分无关特征权重稀疏化为 0"
```

---

## 🃏 Anki 卡片

- Q: Lasso 回归中的软阈值算子 (Soft-Thresholding Operator) $S_\lambda(z) = \text{sign}(z) \max(|z| - \lambda, 0)$ 为何能产生系数稀疏性 (Sparsity)？
- A: 当目标函数的 $L_1$ 正则项在原点不可导时，软阈值算子会将绝对值小于阈值 $\lambda$ 的系数直接强行截断为绝对的零 0，从而实现自动化特征选择与稀疏解。
