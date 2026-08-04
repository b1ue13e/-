---
title: "多元统计-题型-Fisher判别分析与EM-GMM聚类阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "多元统计作业"
course: "16-多元统计"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: intermediate
importance: A
concept: ["多元统计", "PCA", "Fisher LDA", "EM算法"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/22-概率论与数理统计/🗺️ 概率论与数理统计学习路径|概率统计]]"]
related: ["[[机器学习-题型-李宏毅式分类与深层模型阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/17-机器学习/01-基础概念/🌱 第一阶段：基础概念|多元统计学习路径]]"]
downstream: []
tags: [学习, 16-多元统计, 作业, 实战, 阶梯作业]
aliases: ["MVA-HW01-PCA与EM聚类作业"]
---

# 多元统计 - HW01：Fisher 判别分析与 EM-GMM 聚类阶梯作业

> 🎯 **作业目标**：手写 SVD 分解 PCA、计算 Fisher 线性判别投影矩阵 (LDA)，以及实现高斯混合模型 (GMM) 的 EM 迭代求解。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-mva/hw01_pca_lda_gmm.ipynb`
- **开源标杆仓库**：[hardlyworking/MVA-labs](https://github.com/hardlyworking/MVA-labs) (Stanford STATS 200)
- **核心依赖**：`scikit-learn`, `numpy`, `scipy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | Mahalanobis 距离无误 | 计算多元正态样本均值向量、协方差矩阵与马氏距离 (Mahalanobis Distance)。 |
| 🟡 **L2 - Medium Baseline** | 解释方差比列正确 | **手写基于 SVD 的 PCA 算法**，绘制前 $k$ 个主成分的累积方差贡献率曲线。 |
| 🔴 **L3 - Strong Baseline** | 组间/组内方差最大化 | **手撕 Fisher 线性判别分析 (LDA)**：计算类间散布矩阵 $S_B$ 与类内散布矩阵 $S_W$ 的广义特征值。 |
| 👑 **L4 - Boss Baseline** | Log-Likelihood 单调递增 | **手撕高斯混合模型 EM 算法**：E 步计算后验概率 $\gamma_{ik}$，M 步更新均值、协方差与混合系数。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_pca_reconstruction_error():
    from mva_solvers import manual_pca
    X = np.random.randn(100, 10)
    
    X_reduced, components = manual_pca(X, n_components=3)
    assert X_reduced.shape == (100, 3)
    assert components.shape == (3, 10)
    # 主成分向量必须两两正交
    np.testing.assert_allclose(components @ components.T, np.eye(3), atol=1e-5)
```

---

## 🃏 Anki 卡片

- Q: 在 Fisher 线性判别分析 (LDA) 中，投影方向 $w$ 的最佳优化目标函数 $J(w)$ 是什么？
- A: Fisher LDA 的目标是最大化类间方差与类内方差的比值：$J(w) = \frac{w^T S_B w}{w^T S_W w}$。其最佳投影向量 $w$ 为矩阵 $S_W^{-1} S_B$ 的最大特征值对应的特征向量。
