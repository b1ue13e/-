---
title: "奇异值分解 SVD (Singular Value Decomposition)"
course: "09-高等代数"
tags:
  - 高等代数
  - 矩阵论
  - 奇异值分解
  - SVD
  - 正交变换
  - 低秩近似
type: knowledge_card
status: completed
created: 2026-08-01
---

# 奇异值分解 SVD (Singular Value Decomposition)

## 1. 奇异值分解 SVD 的定义与几何意义

**奇异值分解 SVD (Singular Value Decomposition)** 的核心定义是：将任意 $m \times n$ 实矩阵 $A$ 唯一因子分解为正交矩阵 $U$、对角矩阵 $\Sigma$ 和正交矩阵 $V^T$ 乘积的矩阵谱分解算法。由 Beltrami (1873) 和 Jordan (1874) 最初提出，并由 Eckart & Young (1936) 推广至矩阵近似。

**基本性质与几何意义**：
1. **任意矩阵通用性**：与仅适用于方阵的特征值分解不同，奇异值分解 SVD 适用于任何形状的长方形矩阵；
2. **三步几何变换**：将 $n$ 维空间中的单位超球体先进行旋转/反射 ($V^T$)，再沿主轴按奇异值 $\sigma_i$ 缩放 ($\Sigma$)，最后在 $m$ 维空间中再次旋转/反射 ($U$)；
3. **最佳低秩近似 (Eckart-Young 定理)**：截取前 $k$ 个最大奇异值构造的矩阵 $A_k = U_k \Sigma_k V_k^T$ 是原矩阵在 F-范数与 2-范数意义下的最佳 $k$-阶低秩逼近。

---

## 2. 奇异值 decomposition 形式化推导与 Eckart-Young 定理

**矩阵分解假设**：
设 $A \in \mathbb{R}^{m \times n}$，秩为 $r \le \min(m, n)$。

**推导过程（与对称阵 $A^T A$ / $A A^T$ 特征分解联系）**：
1. 构造对称半正定矩阵 $A^T A \in \mathbb{R}^{n \times n}$，其特征分解为：
$$A^T A = V \Lambda V^T, \quad \text{其中 } V = [\mathbf{v}_1, \dots, \mathbf{v}_n]$$
特征值为 $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_r > 0 = \dots = 0$；
2. 定义奇异值为 $\sigma_i = \sqrt{\lambda_i} > 0 \; (i=1,\dots,r)$。构造 $\mathbf{u}_i = \frac{1}{\sigma_i} A \mathbf{v}_i \in \mathbb{R}^m$；
3. 验证 $\mathbf{u}_i$ 的正交性：
$$\mathbf{u}_i^T \mathbf{u}_j = \frac{1}{\sigma_i \sigma_j} \mathbf{v}_i^T A^T A \mathbf{v}_j = \frac{1}{\sigma_i \sigma_j} \mathbf{v}_i^T (\lambda_j \mathbf{v}_j) = \frac{\lambda_j}{\sigma_i \sigma_j} \delta_{ij} = \delta_{ij}$$
4. **矩阵标准分解式**：扩充 $\mathbf{u}_i$ 与 $\mathbf{v}_j$ 构成完备正交基 $U \in \mathbb{R}^{m \times m}, V \in \mathbb{R}^{n \times n}$，则：
$$A = U \Sigma V^T$$
5. **因此**，$A A^T = U \Sigma \Sigma^T U^T$，即左奇异向量 $U$ 是 $A A^T$ 的特征向量，右奇异向量 $V$ 是 $A^T A$ 的特征向量。

---

## 3. 奇异值分解 SVD 与 特征值分解 (EVD) 对比

| 维度 | 奇异值分解 SVD | 特征值分解 EVD |
|:---|:---|:---|
| **适用矩阵范围** | **任意 $m \times n$ 实/复矩阵** | 仅适用于 $n \times n$ 方阵（且需可对角化） |
| **分解形式** | $A = U \Sigma V^T$ (左右两个不同正交阵) | $A = P \Lambda P^{-1}$ (同一个特征向量矩阵) |
| **向量正交性** | **$U, V$ 必为正交矩阵** | 仅在 $A$ 为对称阵时特征向量才正交 |
| **对角元素含义** | 奇异值 $\sigma_i \ge 0$ (实数且非负) | 特征值 $\lambda_i$ (可为复数或负数) |
| **工程应用** | 图像压缩、推荐系统 (SVD++)、PCA | 动力系统 stability、解微分方程组 |

**局限（误区与反例）**：奇异值不等于特征值（仅对对称半正定阵两者重合）；对大规模稀疏矩阵，全量 SVD 计算复杂度为 $O(m n \min(m, n))$，实践中采用随机化 SVD (Randomized SVD) 或 Lanczos 迭代法加速。

关联知识点推荐：[[特征值与特征向量]]、[[主成分分析PCA]]、[[凸优化与拉格朗日对偶]]、[[快速傅里叶变换FFT]]。

---

## 4. Python Numpy 矩阵 SVD 重构与低秩近似自测断言

```python
import numpy as np

def svd_low_rank_approx(A: np.ndarray, k: int) -> np.ndarray:
    """手动对矩阵 A 进行 k-阶低秩 SVD 近似重构"""
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    # 截取前 k 个奇异值
    Uk = U[:, :k]
    Sk = np.diag(S[:k])
    Vtk = Vt[:k, :]
    return Uk @ Sk @ Vtk

if __name__ == "__main__":
    np.random.seed(42)
    # 构造 5x4 秩为 2 的测试矩阵
    U_true = np.linalg.qr(np.random.randn(5, 2))[0]
    V_true = np.linalg.qr(np.random.randn(4, 2))[0]
    S_true = np.array([10.0, 3.0])
    A = U_true @ np.diag(S_true) @ V_true.T

    # 1. 检验全量 SVD 分解
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    assert np.allclose(S[:2], [10.0, 3.0]), "奇异值分解结果与真实奇异值不符"

    # 2. k=2 低秩重构断言 (应 100% 精确还原 A)
    A_rec = svd_low_rank_approx(A, k=2)
    assert np.allclose(A, A_rec, atol=1e-5), "k=2 时 SVD 应该完全重构矩阵 A"

    # 3. k=1 截断低秩误差断言
    A_k1 = svd_low_rank_approx(A, k=1)
    err = np.linalg.norm(A - A_k1, ord='fro')
    assert abs(err - 3.0) < 1e-4, f"F-范数截断误差应等于被忽略的奇异值 3.0, 实际: {err}"

    print(f"奇异值分解 SVD 计算成功! 奇异值: {S.round(2)}")
    print(f"k=1 低秩近似 Frobenius 范数残差: {err:.4f} (符合理论值 3.0)")
    print("奇异值分解 SVD 单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Strang, G. (2016). *Introduction to Linear Algebra* (5th ed.). Wellesley-Cambridge Press. Chapter 7 (Singular Value Decomposition). ISBN: 978-0980232776. URL: math.mit.edu/linearalgebra/
- Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations* (4th ed.). Johns Hopkins University Press. Chapter 2.4 (The Singular Value Decomposition). ISBN: 978-1421407944.
- Eckart, C., & Young, G. (1936). The approximation of one matrix by another of lower rank. *Psychometrika*, 1(3), 211-218. DOI: https://doi.org/10.1007/BF02288367
