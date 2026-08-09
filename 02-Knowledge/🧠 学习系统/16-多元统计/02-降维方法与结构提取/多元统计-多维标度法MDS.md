---
type: study
topic: "多维标度法 MDS"
course: "16-多元统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段2-降维方法与结构提取]]"
upstream: ["[[多元统计-前置-正定矩阵与谱分解]]"]
flow: knowledge
kind: derivation
difficulty: intermediate
concept: ["多维标度法", "MDS", "Classical MDS", "双重中心化", "相异度矩阵", "Stress应变度"]
tags: [学习, 多元统计, 降维, 流形学习, 可视化]
---

# 多元统计-多维标度法MDS

## 1. 为什么无特征原始坐标时仍能降维？

在实际统计与心理学/市场调研中，我们常常**无法直接观测到对象的特征坐标 $\mathbf{X}$**，而只能获得对象两两之间的**距离或相异度矩阵 (Dissimilarity Matrix) $\mathbf{D} = (d_{ij})_{n \times n}$**（例如城市间行驶里程、消费者对品牌相似度的打分）。

**古典多维标度法 (Classical Metric MDS / Torgerson MDS)** 的核心目标：根据给定的 $n \times n$ 距离矩阵 $\mathbf{D}$，在低维空间 $\mathbb{R}^k$（通常 $k=2$ 或 $3$）中重新重构出 $n$ 个点的低维坐标 $\mathbf{Z} = [\mathbf{z}_1, \dots, \mathbf{z}_n]^T \in \mathbb{R}^{n \times k}$，使得低维空间中的欧氏距离 $\|\mathbf{z}_i - \mathbf{z}_j\|_2$ **最大程度保持原始相异度 $d_{ij}$**。

---

## 2. 古典 MDS 数学推导：双重中心化与内积矩阵

### 2.1 距离平方矩阵与内积矩阵的代数关系

假设低维中心化坐标为 $\mathbf{Z} \in \mathbb{R}^{n \times k}$（满足 $\sum_{i=1}^n \mathbf{z}_i = \mathbf{0}$）。定义内积矩阵 $\mathbf{B} = \mathbf{Z} \mathbf{Z}^T \in \mathbb{R}^{n \times n}$，其元素 $b_{ij} = \mathbf{z}_i^T \mathbf{z}_j$。
低维欧氏距离平方：
$$d_{ij}^2 = \|\mathbf{z}_i - \mathbf{z}_j\|^2 = (\mathbf{z}_i - \mathbf{z}_j)^T (\mathbf{z}_i - \mathbf{z}_j) = \mathbf{z}_i^T \mathbf{z}_i + \mathbf{z}_j^T \mathbf{z}_j - 2 \mathbf{z}_i^T \mathbf{z}_j = b_{ii} + b_{jj} - 2 b_{ij}$$

### 2.2 双重中心化矩阵 (Double Centering)

利用 $\mathbf{Z}$ 中心化条件（$\sum_{i=1}^n b_{ij} = \sum_{j=1}^n b_{ij} = 0$），可以通过对距离平方矩阵 $\mathbf{D}^{(2)} = (d_{ij}^2)$ 进行**双重中心化**显式恢复内积矩阵 $\mathbf{B}$：
$$\mathbf{B} = -\frac{1}{2} \mathbf{H}_n \mathbf{D}^{(2)} \mathbf{H}_n$$
其中中心化算子 $\mathbf{H}_n = \mathbf{I}_n - \frac{1}{n} \mathbf{1}_n \mathbf{1}_n^T$。

### 2.3 谱分解求解低维坐标

对实对称矩阵 $\mathbf{B}$ 进行谱分解：
$$\mathbf{B} = \mathbf{V} \boldsymbol{\Lambda} \mathbf{V}^T = \sum_{j=1}^n \lambda_j \mathbf{v}_j \mathbf{v}_j^T$$
保留前 $k$ 个最大正特征值 $\lambda_1 \ge \dots \ge \lambda_k > 0$ 及对应的特征向量 $\mathbf{V}_k = [\mathbf{v}_1, \dots, \mathbf{v}_k]$，则最优低维坐标为：
$$\mathbf{Z}_k = \mathbf{V}_k \boldsymbol{\Lambda}_k^{1/2}$$

> [!NOTE]
> **与 PCA 的等价性**：若原始距离 $\mathbf{D}$ 就是欧氏距离，则古典 MDS 得到的低维坐标 $\mathbf{Z}_k$ 与 PCA 降维投影坐标在刚体旋转意义下**完全严格等价**！

---

## 3. Python 实战代码：城市距离矩阵 MDS 几何坐标重构

```python
import sys
import numpy as np

sys.path.insert(0, r"f:\-\03-Projects\16-多元统计\scripts")
from mva_toolkit import mds_fit

# 构造 4 个平面的真实坐标: (0,0), (0,3), (4,0), (4,3)
X_true = np.array([
    [0.0, 0.0],
    [0.0, 3.0],
    [4.0, 0.0],
    [4.0, 3.0]
])

# 计算两两欧氏距离矩阵 D
D = np.linalg.norm(X_true[:, None, :] - X_true[None, :, :], axis=2)

# 运行古典 MDS 重构 2D 坐标
res_mds = mds_fit(D, n_components=2)
Z_reconstructed = res_mds['coordinates']

# 重构距离校验
D_reconstructed = np.linalg.norm(Z_reconstructed[:, None, :] - Z_reconstructed[None, :, :], axis=2)

print("=== 古典 MDS 距离重构校验 ===")
print("原始距离矩阵:\n", np.round(D, 2))
print("MDS 重构距离矩阵:\n", np.round(D_reconstructed, 2))

assert np.allclose(D, D_reconstructed, atol=1e-3)
print("✅ 古典 MDS 双重中心化与距离保持重构成功！")
```

---

## 4. 检索自测练习

1. 证明若距离矩阵 $\mathbf{D}^{(2)}$ 满足三角形不等式且完全由欧氏距离产生，则双重中心化矩阵 $\mathbf{B} = -\frac{1}{2} \mathbf{H}_n \mathbf{D}^{(2)} \mathbf{H}_n$ 必为半正定矩阵。
2. 解释非度量 MDS (Non-metric MDS / Sammon Mapping) 与古典 Metric MDS 在目标优化函数与距离单调性假设上的区别。

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
