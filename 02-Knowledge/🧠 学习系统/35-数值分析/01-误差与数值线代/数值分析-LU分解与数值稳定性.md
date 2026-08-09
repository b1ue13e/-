---
type: study
topic: "LU分解与数值稳定性"
course: "数值分析"
created: 2026-08-08
status: ongoing
stage_moc: "[[🧭 阶段1-误差与数值线代]]"
upstream: ["[[数值分析-后向误差与稳定性分析]]"]
flow: knowledge
kind: concept
tags: [学习, 数值分析, LU分解, 高斯消元, 列主元, 增长因子]
---

# 数值分析-LU分解与数值稳定性

> "高斯消元本质上是矩阵三角分解 $PA=LU$。列主元选择（Partial Pivoting）是压制元素增长因子、保证直接法后向稳定的唯一生命线。"

---

## 1. 问题动机与核心价值

求解非奇异线性方程组 $Ax = b$ 最直接的方法是高斯消元。
如果不进行行交换，当主元位置出现极小数（如 $10^{-20}$）时，倍加系数 $l_{ik} = a_{ik}/a_{kk}$ 产生天文级放大，导致后续矩阵元素剧烈膨胀，低位有效数字被彻底覆盖。

---

## 2. 严密数学推导与算法流程

### 列选主元 LU 分解定理
对于任意非奇异方阵 $A \in \mathbb{R}^{n \times n}$，存在置换矩阵 $P$、单位下三角矩阵 $L$（满足 $|l_{ij}| \le 1$）以及非奇异上三角矩阵 $U$，使得：
$$PA = LU$$

### 后向误差界与增长因子
计算机实际计算得到的 $\hat{L}, \hat{U}$ 精确满足：
$$\hat{L}\hat{U} = PA + \Delta A, \quad \frac{\|\Delta A\|_\infty}{\|A\|_\infty} \le n \gamma_n \rho$$
其中 $\rho$ 称为**增长因子（Growth Factor）**：
$$\rho = \frac{\max_{i,j,k} |a_{ij}^{(k)}|}{\max_{i,j} |a_{ij}|}$$
- 未选主元时，$\rho$ 可以无界大；
- 列选主元时，$|l_{ij}| \le 1$，理论最坏界为 $\rho \le 2^{n-1}$，但在实际应用中 $\rho \approx n^{2/3}$，算法高度后向稳定。

---

## 3. Python 算法实现

```python
import numpy as np

def lu_factor_pivot(A):
    """带列主元的 LU 分解 PA = LU"""
    A = A.copy().astype(np.float64)
    n = A.shape[0]
    P = np.eye(n)
    
    for k in range(n - 1):
        # 选取列绝对值最大元素作为主元
        p = np.argmax(np.abs(A[k:, k])) + k
        if p != k:
            A[[k, p], :] = A[[p, k], :]
            P[[k, p], :] = P[[p, k], :]
        
        if np.abs(A[k, k]) < 1e-15:
            raise ValueError("矩阵数值奇异")
            
        # 消元并原地存储 L 和 U
        A[k+1:, k] /= A[k, k]
        A[k+1:, k+1:] -= np.outer(A[k+1:, k], A[k, k+1:])
        
    L = np.tril(A, -1) + np.eye(n)
    U = np.triu(A)
    return P, L, U
```

---

## 4. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---

## 5. 检索练习与自测

1. 构造一个 $2 \times 2$ 矩阵，演示不选主元时由于舍入误差产生的完全错误解，以及列选主元后得到的精确解。
2. 简述解线性方程组 $Ax=b$ 时，利用 $PA=LU$ 进行前向回代与后向回代的计算复杂度。
