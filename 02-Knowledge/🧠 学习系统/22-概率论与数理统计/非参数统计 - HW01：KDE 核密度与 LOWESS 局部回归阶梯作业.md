---
title: "非参数统计-题型-KDE核密度与LOWESS局部回归阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "非参数统计作业"
course: "32-非参数统计"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: intermediate
importance: A
concept: ["非参数统计", "秩和检验", "KDE核密度", "LOWESS回归"]
prerequisites: ["[[🗺️ 概率论与数理统计学习路径|概率统计]]"]
related: ["[[应用回归分析-题型-坐标下降Lasso与IRLS回归阶梯作业]]"]
upstream: ["[[🗺️ 非参数统计学习路径|非参数统计学习路径]]"]
downstream: []
tags: [学习, 32-非参数统计, 作业, 实战, 阶梯作业]
aliases: ["Nonpar-HW01-KDE与LOWESS作业"]
---

# 非参数统计 - HW01：KDE 核密度与 LOWESS 局部回归阶梯作业

> 🎯 **作业目标**：手写 Wilcoxon 符号秩检验、核密度估计 (KDE)、局部加权回归 (LOWESS)，并实现 Nadaraya-Watson 核回归。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-nonpar/hw01_kde_lowess.ipynb`
- **开源标杆仓库**：[CMU 36-402 Advanced Data Analysis](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/)
- **核心依赖**：`statsmodels`, `scipy`, `numpy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | p-value 计算无误 | 手写 Wilcoxon 符号秩检验与 Mann-Whitney U 检验计算 p-value。 |
| 🟡 **L2 - Medium Baseline** | 密度函数积分等于 1 | **手写 Gaussian / Epanechnikov 核密度估计 (KDE)** 算法。 |
| 🔴 **L3 - Strong Baseline** | 拟合残差最小化 | **手撕 LOWESS (Locally Weighted Scatterplot Smoothing)** 局部加权二次回归。 |
| 👑 **L4 - Boss Baseline** | 最佳带宽选择 $h$ | **实现 Nadaraya-Watson 核回归**，并使用 Leave-One-Out 交叉验证 (LOOCV) 自动化搜索最佳带宽 $h$。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_kde_integration_property():
    from nonpar_solvers import manual_kde
    data = np.random.normal(0, 1, 100)
    
    grid = np.linspace(-4, 4, 1000)
    density = manual_kde(data, grid, kernel='gaussian', bandwidth=0.3)
    
    # 密度函数全空间积分必须逼近 1.0
    dx = grid[1] - grid[0]
    total_area = np.sum(density) * dx
    assert np.isclose(total_area, 1.0, atol=0.05), "KDE 估计出的密度函数全轴积分必须逼近 1.0"
```

---

## 🃏 Anki 卡片

- Q: 在核密度估计 (KDE) 中，选择“核函数 (Kernel)”与选择“带宽 (Bandwidth $h$)”哪一个对最终估计效果起决定性作用？
- A: 带宽 $h$ 对 KDE 效果起绝对决定性作用。$h$ 过大引发欠拟合（过度平滑）；$h$ 过小引发过拟合（高方差锯齿）。核函数形式（如高斯核或 Epanechnikov 核）仅对曲线光滑度有微小影响。
