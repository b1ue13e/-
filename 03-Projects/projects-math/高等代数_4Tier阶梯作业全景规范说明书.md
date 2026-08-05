---
title: "高等代数 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "高等代数 4-Tier 阶梯作业规范"
course: "高等代数"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [高等代数, 4Tier作业, 阶梯作业, 编程实战, PyTest, MIT1806]
---

# 📐 高等代数 4-Tier 阶梯作业全景规范说明书 (MIT 18.06SC & Hefferon 范式)

> 本说明书为 **09-高等代数** 路径（基于 Hefferon 《Linear Algebra》、Strang 与 MIT 18.06SC）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ NumPy / SciPy `linalg` 调包 / 基础矩阵乘法 / 高斯消元手算
🟡 L2 - Medium Baseline   │ 向量空间基变换 / 矩阵秩 (Rank) / 特征值与特征向量求解
🔴 L3 - Strong Baseline   │ [核心] 不调用 linalg 库，从零手撕 Gram-Schmidt 正交化 / QR 分解 / SVD 奇异值分解
👑 L4 - Boss Baseline     │ 谱定理 (Spectral Theorem) 形式化证明 / 伪逆 (Moore-Penrose Pseudoinverse) 求解
```

---

## 🎯 高等代数阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 高斯消元与 LU 分解 (Gaussian Elimination & LU Decomposition)
- **开源溯源**：MIT 18.06SC Unit 1 / Hefferon Ch 1
- 🟢 **L1**: 使用 NumPy `np.linalg.solve` 求解线性方程组 $Ax = b$。
- 🟡 **L2**: 手算 3x3 矩阵的高斯-约当消元过程，求逆矩阵 $A^{-1}$。
- 🔴 **L3 (手撕核心)**：**从零手撕带行交换 (Partial Pivoting) 的 $PA = LU$ 分解算法**。
- 👑 **L4**: 实现 Cholesky 分解 $A = L L^T$（针对对称正定矩阵）。

### 2. HW02 - 向量空间与 Gram-Schmidt 正交化 (Orthogonality & QR Decomposition)
- **开源溯源**：MIT 18.06SC Unit 2 / Hefferon Ch 3
- 🟢 **L1**: 使用 SciPy `linalg.qr` 计算矩阵的 QR 分解 $A = QR$。
- 🟡 **L2**: 计算正交投影矩阵 $P = A(A^T A)^{-1} A^T$ 并证明 $P^2 = P$。
- 🔴 **L3 (手撕核心)**：**从零手撕 改进型 Gram-Schmidt (Modified Gram-Schmidt, MGS) 正交化算法**（防止数值不稳定导致的正交性丧失）。
- 👑 **L4**: 实现 Householder 变换进行数值稳健的 QR 分解。

### 3. HW03 - 特征值、特征向量与幂迭代 (Eigenvalues & Power Iteration)
- **开源溯源**：MIT 18.06SC Unit 3 / Hefferon Ch 5
- 🟢 **L1**: 使用 `np.linalg.eig` 求解对称矩阵的特征值与特征向量。
- 🟡 **L2**: 验证矩阵对角化 $A = S \Lambda S^{-1}$ 与迹/行列式性质 ($\text{tr}(A) = \sum \lambda_i$)。
- 🔴 **L3 (手撕核心)**：**从零手撕 Power Iteration (幂迭代) 与 Inverse Power Iteration 算法**（用于求解主特征值与对应主特征向量）。
- 👑 **L4**: 实现 QR 算法 (QR Algorithm) 求解所有特征值。

### 4. HW04 - 奇异值分解与主成分分析 (Singular Value Decomposition - SVD)
- **开源溯源**：MIT 18.06SC Unit 3 / Axler Ch 7
- 🟢 **L1**: 使用 `np.linalg.svd` 求解矩阵的 $U, \Sigma, V^T$ 并可视化低秩逼近。
- 🟡 **L2**: 证明 $A^T A$ 的特征向量对应 $V$ 的列向量，$\sigma_i = \sqrt{\lambda_i}$。
- 🔴 **L3 (手撕核心)**：**手撕基于 $A^T A$ 特征分解的 SVD 矩阵构造算法与低秩矩阵剪裁 (Truncated SVD)**。
- 👑 **L4**: 在 Lean 4 / Coq 中完成复希尔伯特空间谱定理的形式化证明。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-math/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-math/tests/test_hw01_lu.py
pytest 03-Projects/projects-math/tests/test_hw02_qr.py
pytest 03-Projects/projects-math/tests/test_hw04_svd.py
```
