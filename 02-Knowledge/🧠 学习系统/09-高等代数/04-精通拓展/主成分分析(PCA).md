---
title: "主成分分析 PCA (Principal Component Analysis)"
course: "09-高等代数"
tags:
  - 高等代数
  - 机器学习
  - PCA
  - 主成分分析
  - 协方差矩阵
  - 降维
type: knowledge_card
status: completed
created: 2026-08-01
---

# 主成分分析 PCA (Principal Component Analysis)

## 1. 主成分分析 PCA 的定义与双重视角

**主成分分析 PCA (Principal Component Analysis)** 的核心定义 is：一种通过正交变换将一组可能存在相关性的高维变量转换为少数几个线性无关的正交变量（称为主成分）的无监督线性降维算法。由 Karl Pearson (1901) 提出，并由 Harold Hotelling (1933) 发展。

**双重等价理论视角**：
1. **最大方差视角 (Maximum Variance)**：寻找投影方向 $\mathbf{w}$，使得数据投影后的方差最大化（保留最大的信息量）；
2. **最小重建误差视角 (Minimum Reconstruction Error)**：寻找正交子空间，使得原始样本点到该投影子空间的垂直欧氏距离平方和最小。

---

## 2. 最大方差法形式化推导与协方差矩阵特征分解

**数据预处理假设**：
设数据集矩阵为 $X \in \mathbb{R}^{N \times d}$，且已进行**中心化预处理**（即均值 $\boldsymbol{\mu} = \mathbf{0}$）。协方差矩阵为 $C = \frac{1}{N} X^T X \in \mathbb{R}^{d \times d}$。

**推导过程（最大方差与拉格朗日乘子）**：
1. 设单位投影向量为 $\mathbf{w} \in \mathbb{R}^d$（满足约束 $\|\mathbf{w}\|^2 = \mathbf{w}^T \mathbf{w} = 1$）；
2. 样本 $x_i$ 投影后的标量值为 $y_i = \mathbf{w}^T x_i$。投影后数据的方差为：
$$\text{Var}(y) = \frac{1}{N} \sum_{i=1}^N (\mathbf{w}^T x_i)^2 = \frac{1}{N} \mathbf{w}^T \left( \sum_{i=1}^N x_i x_i^T 
ight) \mathbf{w} = \mathbf{w}^T C \mathbf{w}$$
3. 构造拉格朗日目标优化函数：
$$L(\mathbf{w}, \lambda) = \mathbf{w}^T C \mathbf{w} + \lambda (1 - \mathbf{w}^T \mathbf{w})$$
4. 对 $\mathbf{w}$ 求偏导并令其为零：
$$\frac{\partial L}{\partial \mathbf{w}} = 2 C \mathbf{w} - 2 \lambda \mathbf{w} = \mathbf{0} \Rightarrow C \mathbf{w} = \lambda \mathbf{w}$$
5. **因此**，投影方向 $\mathbf{w}$ 恰好是协方差矩阵 $C$ 的**特征向量**，且方差 $\text{Var}(y) = \mathbf{w}^T C \mathbf{w} = \lambda \mathbf{w}^T \mathbf{w} = \lambda$ 即对应最大特征值！

---

## 3. PCA 与 SVD 降维实现对比

| 维度 | 基于协方差矩阵特征分解 (Standard PCA) | 基于奇异值分解 (SVD-based PCA) |
|:---|:---|:---|
| **计算对象** | $d \times d$ 协方差矩阵 $C = \frac{1}{N} X^T X$ | 直接对 $N \times d$ 中心化矩阵 $X$ 作 SVD |
| **计算复杂度** | $O(N d^2 + d^3)$ | $O(N d \min(N, d))$ |
| **数值稳定性** | 显式计算 $X^T X$ 会丢失精度（条件数平方倍恶化）| **数值精度高**（避免直接计算 $X^T X$）|
| **工业工程实现** | 很少直接使用（仅教学演示） | **Scikit-Learn `PCA` 默认底层实现** |

**局限（误区与反例）**：PCA 仅能提取**线性主成分**；若数据分布在非线性曲面上（如瑞士卷 Swiss Roll），PCA 降维会破坏拓扑结构，此时需使用核主成分分析 (Kernel PCA) 或 t-SNE / UMAP。

关联知识点推荐：[[特征值与特征向量]]、[[奇异值分解SVD]]、[[均方误差MSE与Huber损失]]、[[二次规划]]。

---

## 4. Python 手写 PCA 算法与方差贡献率自测断言

```python
import numpy as np

def pca_fit_transform(X: np.ndarray, n_components: int) -> tuple:
    """
    手写主成分分析 PCA 算法
    X: (N, d)
    """
    # 1. 中心化
    mean = np.mean(X, axis=0)
    X_centered = X - mean

    # 2. 协方差矩阵
    cov = np.cov(X_centered, rowvar=False)

    # 3. 特征值分解
    vals, vecs = np.linalg.eigh(cov)

    # 4. 按特征值降序排列
    sort_idx = np.argsort(vals)[::-1]
    vals = vals[sort_idx]
    vecs = vecs[:, sort_idx]

    # 5. 选择前 n_components
    components = vecs[:, :n_components]
    X_projected = X_centered @ components

    explained_variance_ratio = vals[:n_components] / np.sum(vals)
    return X_projected, components, explained_variance_ratio

if __name__ == "__main__":
    np.random.seed(42)
    # 产生高方差在 x 方向的 2D 数据
    x1 = np.random.normal(0, 5, 1000)
    x2 = np.random.normal(0, 1, 1000)
    X = np.column_stack([x1, x2])

    X_pca, comps, ratio = pca_fit_transform(X, n_components=1)

    # 自测验证 1: 第一主成分累积方差贡献率应 > 90%
    assert ratio[0] > 0.90, f"第一主成分解释方差比例应极高: {ratio[0]}"

    # 自测验证 2: 降维后输出维度断言
    assert X_pca.shape == (1000, 1)

    # 自测验证 3: 第一主成分方向应接近 x 轴 [1, 0]
    assert abs(comps[0, 0]) > 0.95, "第一主成分方向应平行于原始最大方差轴"

    print(f"主成分分析 PCA 降维成功: 第一主成分方差解释率 = {ratio[0]*100:.2f}%")
    print("主成分分析 PCA 单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Pearson, K. (1901). On lines and planes of closest fit to systems of points in space. *The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science*, 2(11), 559-572. DOI: https://doi.org/10.1080/14786440109462720
- Hotelling, H. (1933). Analysis of a complex of statistical variables into principal components. *Journal of Educational Psychology*, 24(6), 417-441. DOI: https://doi.org/10.1037/h0071325
- Jolliffe, I. T. (2002). *Principal Component Analysis* (2nd ed.). Springer. ISBN: 978-0387954424. DOI: https://doi.org/10.1007/b98835
