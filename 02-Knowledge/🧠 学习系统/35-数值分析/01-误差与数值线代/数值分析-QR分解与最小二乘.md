---
type: study
topic: "QR分解与最小二乘"
course: "数值分析"
created: 2026-08-08
status: ongoing
stage_moc: "[[🧭 阶段1-误差与数值线代]]"
upstream: ["[[数值分析-LU分解与数值稳定性]]"]
flow: knowledge
kind: concept
tags: [学习, 数值分析, QR分解, Householder, GramSchmidt, 最小二乘]
---

# 数值分析-QR分解与最小二乘

> "正交矩阵 $Q$ 保持欧几里得范数不变（$\|Qx\|_2 = \|x\|_2$），条件数恒为 1。Householder 反射是求解超定最小二乘问题最坚固的数值盾牌。"

---

## 1. 问题动机与核心价值

对于超定方程组 $Ax \approx b$（$m > n$），最小二乘问题目标为求 $\min_x \|b - Ax\|_2$。
经典正规方程法 $A^T A x = A^T b$ 会将矩阵条件数平方（$\kappa_2(A^T A) = \kappa_2(A)^2$），导致中等病态问题立即崩溃。
QR 分解将 $A$ 转化为正交矩阵 $Q$ 与上三角矩阵 $R$，直接避免了条件数平方灾难。

---

## 2. 严密数学推导与正交变换

### 1. 经典 Gram-Schmidt 与修正 Gram-Schmidt (MGS)
- 经典 GS（CGS）在浮点舍入下会迅速丧失正交性（$\operatorname{Loss of Orthogonality}$）；
- 修正 GS（MGS）通过立即将新正交化的向量从剩余所有向量中投影扣除，显著改善稳定性，但对病态矩阵仍可能丧失正交性。

### 2. Householder 反射（Householder Reflection）
构造镜面反射矩阵 $H = I - 2 \frac{v v^T}{v^T v}$，使得向量 $x$ 变换为 $H x = \pm \|x\|_2 e_1$。
令 $v = x + \operatorname{sgn}(x_1)\|x\|_2 e_1$（选符号以避免相消）。
对矩阵 $A$ 连续左乘 $n$ 个 Householder 矩阵：
$$Q^T A = H_n \dots H_2 H_1 A = \begin{bmatrix} R \\ 0 \end{bmatrix} \implies A = QR$$

---

## 3. 最小二乘求解对比

```python
import numpy as np

# 构造病态矩阵 A
m, n = 50, 10
t = np.linspace(0, 1, m)
A = np.vander(t, n) # Vandermonde 矩阵高度病态
b = np.exp(t)

# 1. 正规方程法 (Normal Equations)
x_normal = np.linalg.solve(A.T @ A, A.T @ b)

# 2. QR 分解法 (Householder)
Q, R = np.linalg.qr(A)
x_qr = np.linalg.solve(R, Q.T @ b)

print(f"A 条件数: {np.linalg.cond(A):.2e}")
print(f"A^T A 条件数: {np.linalg.cond(A.T @ A):.2e}")
print(f"QR 解与正规方程解范数差: {np.linalg.norm(x_qr - x_normal):.2e}")
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

1. 证明对任意单位反射向量 $u$（$\|u\|_2=1$），矩阵 $H = I - 2uu^T$ 是对称且正交的。
2. 解释为什么 Givens 旋转特别适用于大型稀疏矩阵或带状矩阵的 QR 分解。
