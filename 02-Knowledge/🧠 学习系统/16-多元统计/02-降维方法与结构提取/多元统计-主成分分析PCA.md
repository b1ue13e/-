---
type: study
topic: "主成分分析 PCA"
course: "16-多元统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段2-降维方法与结构提取]]"
upstream: ["[[多元统计-前置-正定矩阵与谱分解]]"]
flow: knowledge
kind: derivation
difficulty: intermediate
concept: ["主成分分析", "PCA", "SVD", "Eckart-Young定理", "方差贡献率", "碎石图"]
tags: [学习, 多元统计, 降维, 线性代数, 无监督学习, SVD]
---

# 多元统计-主成分分析PCA

## 1. 为什么需要主成分分析？

当数据具有 $p$ 个指标且变量间存在显著相关性时，直接分析会遇到：
1. **多重共线性**导致回归或估计失真；
2. **高维可视化极其困难**；
3. **信息重叠浪费计算资源**。

**主成分分析 (PCA)** 的核心哲学：通过**正交坐标旋转**，将原本相关的 $p$ 个变量线性组合为一组**互不相关 (正交)** 的新综合变量 $Y_1, Y_2, \dots, Y_p$，并按**方差由大到小依次排列**，从而实现最大方差保留与最优低维逼近。

---

## 2. 数学推导：最大方差与低秩逼近双重视角

### 2.1 视角一：最大化投影方差与正交拉格朗日求解

设标准化随机向量 $\mathbf{X} \in \mathbb{R}^p$，协方差/相关矩阵为 $\mathbf{\Sigma}$（特征值 $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_p \ge 0$，对应正交特征向量 $\mathbf{e}_1, \dots, \mathbf{e}_p$）。

**第一主成分 $Y_1 = \mathbf{e}_1^T \mathbf{X}$**：
目标为最大化方差 $\operatorname{Var}(Y_1) = \mathbf{e}_1^T \mathbf{\Sigma} \mathbf{e}_1$，约束条件为 $\|\mathbf{e}_1\|^2 = 1$。
构造拉格朗日函数 $L(\mathbf{e}_1, \lambda_1) = \mathbf{e}_1^T \mathbf{\Sigma} \mathbf{e}_1 - \lambda_1 (\mathbf{e}_1^T \mathbf{e}_1 - 1)$，求导得：
$$\nabla_{\mathbf{e}_1} L = 2 \mathbf{\Sigma} \mathbf{e}_1 - 2 \lambda_1 \mathbf{e}_1 = \mathbf{0} \implies \mathbf{\Sigma} \mathbf{e}_1 = \lambda_1 \mathbf{e}_1$$
代回可得最大方差 $\operatorname{Var}(Y_1) = \mathbf{e}_1^T \mathbf{\Sigma} \mathbf{e}_1 = \lambda_1$，即取最大特征值对应的特征向量。

**第二主成分 $Y_2 = \mathbf{e}_2^T \mathbf{X}$**：
寻找与 $Y_1$ 不相关（正交）且方差最大的新方向。约束条件为 $\|\mathbf{e}_2\|^2 = 1$ 且 $\operatorname{Cov}(Y_1, Y_2) = \mathbf{e}_1^T \mathbf{\Sigma} \mathbf{e}_2 = 0 \iff \mathbf{e}_1^T \mathbf{e}_2 = 0$。
构造双约束拉格朗日函数：
$$L(\mathbf{e}_2, \lambda_2, \phi) = \mathbf{e}_2^T \mathbf{\Sigma} \mathbf{e}_2 - \lambda_2 (\mathbf{e}_2^T \mathbf{e}_2 - 1) - \phi (\mathbf{e}_1^T \mathbf{e}_2)$$
求导得 $2 \mathbf{\Sigma} \mathbf{e}_2 - 2 \lambda_2 \mathbf{e}_2 - \phi \mathbf{e}_1 = \mathbf{0}$。左乘 $\mathbf{e}_1^T$，注意到 $\mathbf{e}_1^T \mathbf{\Sigma} \mathbf{e}_2 = 0$ 且 $\mathbf{e}_1^T \mathbf{e}_2 = 0$，立得 $\phi = 0$。
由此化简为 $\mathbf{\Sigma} \mathbf{e}_2 = \lambda_2 \mathbf{e}_2$，即 $\mathbf{e}_2$ 为第二大特征值对应的正交特征向量！数学归纳可得 $Y_k = \mathbf{e}_k^T \mathbf{X}$。

### 2.2 视角二：Eckart-Young-Mirsky 最优低秩重构定理

设标准化数据矩阵 $\mathbf{Z} \in \mathbb{R}^{n \times p}$ 的 SVD 分解为 $\mathbf{Z} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$。
寻找秩为 $k < p$ 的最佳逼近矩阵 $\hat{\mathbf{Z}}_k$，使 Frobenius 范数重构误差最小：
$$\min_{\operatorname{rank}(\mathbf{A})=k} \|\mathbf{Z} - \mathbf{A}\|_F^2 = \sum_{j=k+1}^p \sigma_j^2$$
根据 Eckart-Young 定理，最优低秩解恰好为前 $k$ 个奇异值的截断：
$$\hat{\mathbf{Z}}_k = \sum_{j=1}^k \sigma_j \mathbf{u}_j \mathbf{v}_j^T = \mathbf{Z} \mathbf{V}_k \mathbf{V}_k^T$$
其中 $\mathbf{V}_k \in \mathbb{R}^{p \times k}$ 即为主成分载荷矩阵，$\mathbf{Z}\mathbf{V}_k$ 即为主成分得分矩阵。

---

## 3. 统计量与重要性质

1. **总方差守恒**：$\sum_{j=1}^p \operatorname{Var}(X_j) = \operatorname{tr}(\mathbf{\Sigma}) = \sum_{j=1}^p \lambda_j$；
2. **方差贡献率**：第 $k$ 主成分的解释比例为 $\frac{\lambda_k}{\sum_{j=1}^p \lambda_j}$；
3. **主成分载荷 (Loadings)**：原始特征 $X_i$ 与主成分 $Y_j$ 的相关系数 $\operatorname{Corr}(X_i, Y_j) = \frac{e_{ij}\sqrt{\lambda_j}}{\sqrt{\sigma_{ii}}}$；
4. **标准化与协方差 PCA 的区别**：若原始变量量纲差异巨大，必须基于相关矩阵 $\mathbf{R}$ 进行 PCA（相当于标准化到均值 0 方差 1）。

---

## 4. Python 实战代码：UCI 葡萄酒数据集 SVD-PCA 降维

```python
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, r"f:\-\03-Projects\16-多元统计\scripts")
from load_data import load_wine_data
from mva_toolkit import pca_fit

# 1. 加载葡萄酒 13 维化学指标数据
df_wine = load_wine_data()
X = df_wine.drop(columns=['Cultivar']).values

# 2. 运行 SVD-PCA 降维
res_pca = pca_fit(X, n_components=3, standardize=True)

print("=== UCI 葡萄酒 13 维特征 SVD-PCA 降维分析 ===")
print("前 3 特征值 (Lambda):", np.round(res_pca['explained_variance'], 3))
print("前 3 主成分方差贡献率:", np.round(res_pca['explained_variance_ratio'], 4))
print(f"前 3 主成分累积方差贡献率: {res_pca['cumulative_variance_ratio'][-1]*100:.2f}%")
print("\n第一主成分载荷 (前 5 特征):", np.round(res_pca['components'][0, :5], 3))

assert res_pca['cumulative_variance_ratio'][-1] > 0.65
print("✅ SVD-PCA 降维与 Eckart-Young 低秩逼近计算通过！")
```

---

## 5. 检索自测练习

1. 证明对任意正交矩阵 $\mathbf{V}_k$（$\mathbf{V}_k^T\mathbf{V}_k = \mathbf{I}_k$），投影后样本的痕 $\operatorname{tr}(\operatorname{Cov}(\mathbf{Z}\mathbf{V}_k)) = \sum_{j=1}^k \lambda_j$。
2. 解释为什么直接对未标准化的数据做 PCA 会导致方差极大的变量盲目霸占第一主成分？

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
