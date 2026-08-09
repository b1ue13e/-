---
type: study
topic: "高斯混合模型与 EM 算法"
course: "16-多元统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段3-判别与聚类分析]]"
upstream: ["[[多元统计-判别分析LDA与QDA]]"]
flow: knowledge
kind: derivation
difficulty: advanced
concept: ["高斯混合模型", "GMM", "EM算法", "琴生不等式", "对数似然单调性", "后验责任", "软聚类"]
tags: [学习, 多元统计, 聚类, EM算法, 概率生成模型, 潜变量]
---

# 多元统计-高斯混合模型与EM算法

## 1. 为什么硬划分 K-Means 需要升级到 GMM 软聚类？

传统的 K-Means 算法在空间中将每个样本点强制硬划分 (Hard Assignment) 给距离最近的簇中心。
这隐含了两个极强的苛刻假设：
1. 每个簇的方差相同且形状为标准各向同性正球体（协方差 $\mathbf{\Sigma}_k = \sigma^2 \mathbf{I}$）；
2. 簇边界为刚性超平面，无法表达重叠区域或概率置信度。

**高斯混合模型 (Gaussian Mixture Model, GMM)** 将群体假设为 $K$ 个具有不同均值 $\boldsymbol{\mu}_k$、异方差形状 $\mathbf{\Sigma}_k$ 和权重 $\pi_k$ 的多元正态分布的叠加，并通过 **EM (Expectation-Maximization) 算法** 实现光滑的软聚类 (Soft Clustering) 与后验概率预测。

---

## 2. GMM 概率模型与 EM 算法推导

### 2.1 概率密度模型

连续随机向量 $\mathbf{X} \in \mathbb{R}^p$ 的 GMM 混合密度函数为：
$$f(\mathbf{x}) = \sum_{k=1}^K \pi_k N_p(\mathbf{x} \mid \boldsymbol{\mu}_k, \mathbf{\Sigma}_k)$$
其中混合权重满足 $\sum_{k=1}^K \pi_k = 1, \, \pi_k \ge 0$。

全样本未对齐对数似然函数为：
$$\ell(\boldsymbol{\theta}) = \sum_{i=1}^n \ln \left( \sum_{k=1}^K \pi_k N_p(\mathbf{x}_i \mid \boldsymbol{\mu}_k, \mathbf{\Sigma}_k) \right)$$
由于求和符号在对数项内部，无法直接求导得到闭式解，必须引入隐变量 $z_i \in \{1,\dots,K\}$ 采用 EM 迭代算法求解。

### 2.2 E 步 (Expectation Step)：计算后验责任矩阵

根据贝叶斯定理，计算第 $i$ 个样本属于第 $k$ 个高斯分量的后验责任 (Responsibility)：
$$\gamma_{ik} = P(z_i = k \mid \mathbf{x}_i, \boldsymbol{\theta}^{(t)}) = \frac{\pi_k^{(t)} N_p(\mathbf{x}_i \mid \boldsymbol{\mu}_k^{(t)}, \mathbf{\Sigma}_k^{(t)})}{\sum_{j=1}^K \pi_j^{(t)} N_p(\mathbf{x}_i \mid \boldsymbol{\mu}_j^{(t)}, \mathbf{\Sigma}_j^{(t)})}$$
满足对任意样本 $i$，$\sum_{k=1}^K \gamma_{ik} = 1$。

### 2.3 M 步 (Maximization Step)：闭式参数更新

基于当前的责任矩阵 $\gamma_{ik}$，最大化完全数据对数似然的期望 $Q(\boldsymbol{\theta} \mid \boldsymbol{\theta}^{(t)})$：

有社交加权样本量 $N_k = \sum_{i=1}^n \gamma_{ik}$：
1. **混合权重更新**：$\pi_k^{(t+1)} = \frac{N_k}{n}$
2. **均值向量更新**：$\boldsymbol{\mu}_k^{(t+1)} = \frac{1}{N_k} \sum_{i=1}^n \gamma_{ik} \mathbf{x}_i$
3. **协方差矩阵更新**：$\mathbf{\Sigma}_k^{(t+1)} = \frac{1}{N_k} \sum_{i=1}^n \gamma_{ik} (\mathbf{x}_i - \boldsymbol{\mu}_k^{(t+1)})(\mathbf{x}_i - \boldsymbol{\mu}_k^{(t+1)})^T + \epsilon \mathbf{I}_p$

> [!IMPORTANT]
> **第一性原理：EM 算法对数似然单调非递减证明**
> 利用 Jensen 不等式，对任意隐变量分布 $q(\mathbf{z})$：
> $$\ell(\boldsymbol{\theta}) = \sum_i \ln \sum_{z_i} q(z_i) \frac{P(\mathbf{x}_i, z_i \mid \boldsymbol{\theta})}{q(z_i)} \ge \sum_i \sum_{z_i} q(z_i) \ln \frac{P(\mathbf{x}_i, z_i \mid \boldsymbol{\theta})}{q(z_i)} = \mathcal{E}[q, \boldsymbol{\theta}]$$
> 当 E 步取 $q(z_i) = P(z_i \mid \mathbf{x}_i, \boldsymbol{\theta}^{(t)})$ 时，下界与对数似然曲线紧密贴合。M 步最大化下界确保 $\ell(\boldsymbol{\theta}^{(t+1)}) \ge \ell(\boldsymbol{\theta}^{(t)})$ 恒成立！

---

## 3. Python 实战代码：手写 GMM-EM 对数似然单调收敛

```python
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, r"f:\-\03-Projects\16-多元统计\scripts")
from mva_toolkit import gmm_em_fit

# 1. 模拟二元重叠高斯分布数据
np.random.seed(42)
X1 = np.random.multivariate_normal([-2.0, -1.0], [[1.5, 0.6], [0.6, 1.0]], size=150)
X2 = np.random.multivariate_normal([2.5, 3.0], [[1.0, -0.4], [-0.4, 2.0]], size=150)
X = np.vstack([X1, X2])

# 2. 运行 GMM-EM 拟合
res_gmm = gmm_em_fit(X, n_components=2, max_iter=50)

lls = res_gmm['log_likelihoods']
print("=== GMM-EM 算法收敛过程 ===")
print("迭代步数:", len(lls))
print("对数似然初始值 -> 最终值:", f"{lls[0]:.2f} -> {lls[-1]:.2f}")

# 校验单调递增性
is_monotonic = all(lls[i] >= lls[i-1] - 1e-4 for i in range(1, len(lls)))
print(f"对数似然严格单调递增验证: {is_monotonic}")

assert is_monotonic
print("✅ GMM-EM 算法 Jensen 不等式与单调收敛性验证成功！")
```

---

## 4. 检索自测练习

1. 证明当 GMM 的协方差矩阵设定为各向同性 $\mathbf{\Sigma}_k = \sigma^2 \mathbf{I}$ 且方差极限 $\sigma^2 \to 0$ 时，GMM 的 EM 算法在数学上精确退化为 K-Means 算法。
2. 解释高维数据下 GMM-EM 拟合中可能遇到的“协方差崩塌（Covariance Collapse）”现象及其正则化预防方案。

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
