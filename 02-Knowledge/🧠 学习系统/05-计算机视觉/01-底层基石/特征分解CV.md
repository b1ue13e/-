---
type: study
course: "05-计算机视觉"
topic: "特征分解 (Eigen Decomposition)"
created: 2026-08-06
status: planned
difficulty: intermediate
concept: ["特征值", "特征向量", "对角化", "PCA", "谱分解"]
prerequisites: ["线性代数基础CV"]
related: ["SVDCV", "傅里叶变换CV", "梯度下降CV"]
upstream: ["[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/线性代数基础CV]]"]
flow: knowledge
stage_moc: "[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/🏗️ 第一阶段：底层基石]]"
kind: concept
source: "《Mathematics for Machine Learning》Ch.4; Szeliski Ch.3"
tags: [学习, 计算机视觉, 线性代数, 特征分解]
---

# 特征分解 (Eigen Decomposition)

> 所属模块：[[02-Knowledge/🧠 学习系统/05-计算机视觉/🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/🏗️ 第一阶段：底层基石|第一阶段：底层基石]]
> 建议先看：[[线性代数基础CV]]

---

## 0. 类别：A 类核心概念

特征分解是 PCA、谱聚类、图卷积的基础。不理解特征值就无法理解"为什么 SVD 是最佳低秩近似"。

---

## 1. 直觉：矩阵的"不变方向"

一个矩阵 $\mathbf{A}$ 乘以向量 $\mathbf{v}$ 通常既改变方向又改变长度。但**某些特殊的 $\mathbf{v}$ 方向不变，只被缩放**：

$$\mathbf{A}\mathbf{v} = \lambda \mathbf{v}$$

- $\lambda$：**特征值**（放缩因子）
- $\mathbf{v}$：**特征向量**（不变方向）

> **物理直觉**：想象一个变换（拉伸/旋转/投影）。特征向量就是那些"只被拉伸、不被旋转"的特殊方向。特征值告诉你拉伸了多少。

---

## 2. 正式定义

设 $\mathbf{A} \in \mathbb{R}^{n \times n}$。若存在非零向量 $\mathbf{v} \in \mathbb{R}^n$ 和标量 $\lambda \in \mathbb{C}$ 满足 $\mathbf{A}\mathbf{v} = \lambda\mathbf{v}$，则 $\lambda$ 是 $\mathbf{A}$ 的特征值，$\mathbf{v}$ 是对应的特征向量。

等价地：$(\mathbf{A} - \lambda\mathbf{I})\mathbf{v} = \mathbf{0}$，有非零解 $\Leftrightarrow \det(\mathbf{A} - \lambda\mathbf{I}) = 0$（特征方程）。

### 对角化

若 $\mathbf{A}$ 有 $n$ 个线性独立的特征向量，则：

$$\mathbf{A} = \mathbf{V}\mathbf{\Lambda}\mathbf{V}^{-1}$$

其中 $\mathbf{V} = [\mathbf{v}_1 | \cdots | \mathbf{v}_n]$（特征向量矩阵），$\mathbf{\Lambda} = \text{diag}(\lambda_1, \ldots, \lambda_n)$。

**对称矩阵的特权**：若 $\mathbf{A} = \mathbf{A}^T$，则所有特征值都是实数，且 $\mathbf{V}$ 是**正交矩阵**（$\mathbf{V}^{-1} = \mathbf{V}^T$），即 $\mathbf{A} = \mathbf{V}\mathbf{\Lambda}\mathbf{V}^T$。

---

## 3. CV 中的核心应用

### 3.1 PCA（主成分分析）

PCA = 对协方差矩阵做特征分解，取前 $k$ 个最大特征值对应的特征向量作为主成分。

$$ \mathbf{\Sigma} = \frac{1}{n}\mathbf{X}^T\mathbf{X}, \quad \mathbf{\Sigma}\mathbf{v}_i = \lambda_i\mathbf{v}_i $$

- 特征值 $\lambda_i$ = 沿 $\mathbf{v}_i$ 方向的方差
- 降维 = 投影到最大的 $k$ 个特征值对应的方向

```python
import numpy as np

# 简单 PCA 示例
X = np.random.randn(100, 3)  # 100个样本，3维
X_centered = X - X.mean(axis=0)
cov = X_centered.T @ X_centered / (len(X) - 1)

eigenvalues, eigenvectors = np.linalg.eigh(cov)  # eigh 针对对称矩阵
# eigenvalues 升序排列，最大的特征值对应最大方差方向
idx = np.argsort(eigenvalues)[::-1]
print(f"Eigenvalues: {eigenvalues[idx]}")  # 预期：3个正数，降序
print(f"Top eigenvector: {eigenvectors[:, idx[0]]}")  # 第一主成分方向

# 降维到 2 维
X_pca = X_centered @ eigenvectors[:, idx[:2]]
print(f"Reduced shape: {X_pca.shape}")  # 预期 (100, 2)
```

### 3.2 图像协方差与 Eigenfaces

特征脸 (Eigenfaces) = 对人脸图像集的协方差矩阵做特征分解。每个特征向量是一张"平均脸"，任意人脸 = 平均脸 + 特征脸的线性组合。

### 3.3 谱聚类与图拉普拉斯

图拉普拉斯矩阵 $\mathbf{L} = \mathbf{D} - \mathbf{W}$ 的第二小特征值（Fiedler 值）对应的特征向量给出了图的**最优二分**方向。在图像分割中有广泛应用。

---

## 4. 条件变式：特征分解的存在性

| 矩阵类型 | 特征值 | 特征向量 | 对角化 |
|:---|:---|:---|:---|
| **任意方阵** | 可能复数 | 可能线性相关 | **不一定**可对角化 |
| **对称矩阵** | 全实数 | 正交（$\mathbf{V}^T\mathbf{V}=\mathbf{I}$） | ✅ 总是可对角化 |
| **正定矩阵** | 全正实数 | 正交 | ✅ |
| **正交矩阵** | $\lvert\lambda\rvert=1$ | 正交 | ✅ |

> **CV 中的好消息**：协方差矩阵、拉普拉斯矩阵都是对称的，保证特征分解稳定可靠。

---

## 5. 常见误区

- ❌ "所有矩阵都可以特征分解" — 只有方阵，且不一定可对角化（如 Jordan 块）
- ❌ "特征值一定是实数" — 旋转矩阵的特征值是复数 $e^{\pm i\theta}$
- ❌ "特征值越大越重要" — 在 PCA 中是对的（方差），但在其他场景不一定
- ❌ "特征向量是唯一的" — 任何非零倍数也是特征向量，通常归一化为单位长度

---

## 🧪 自测题

1. **(基础)** 矩阵 $\mathbf{A} = \begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}$ 的特征值和特征向量是什么？
   <details><summary>💡 提示</summary>特征值就是对角线元素：$\lambda_1=2, \lambda_2=3$。特征向量是标准基：$\mathbf{v}_1=[1,0]^T, \mathbf{v}_2=[0,1]^T$。对角矩阵的特征向量总是坐标轴方向。</details>

2. **(中等)** PCA 中为什么要取最大的特征值对应的特征向量，而不是最小的？
   <details><summary>💡 提示</summary>特征值 = 方差。最大特征值方向保留了最多的数据变化信息。取最小特征值意味着投影到数据几乎不变的维度上（信息丢失最大）。</details>

3. **(较难)** 如果协方差矩阵的某个特征值接近 0，这意味着什么？对 PCA 有什么影响？
   <details><summary>💡 提示</summary>特征值 ≈ 0 意味着数据在那个方向上几乎无变化（退化的维度）。PCA 可以安全地丢弃该维度（降维），因为不丢失信息。</details>

---

## 🧪 学完本节后可完成的作业

- 理解 [[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/SVDCV|SVD]] 之前必须先理解特征分解（SVD 是特征分解的推广）
---

## 学完后可以完成

- 完成卡内自测题与闭卷复现（特征值/特征向量）

> 该卡无直接课后/阶段作业：以卡内自测题与闭卷复现作为形成性验收；如需综合实践，可挂靠 HW06 开放课程项目或 CAP01。

## 🔗 知识图谱

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
