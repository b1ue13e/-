---
type: study
topic: "特征值问题与幂法QR算法"
course: "数值分析"
created: 2026-08-08
status: ongoing
stage_moc: "[[🧭 阶段1-误差与数值线代]]"
upstream: ["[[数值分析-QR分解与最小二乘]]"]
flow: knowledge
kind: concept
tags: [学习, 数值分析, 特征值, 幂法, 反幂法, QR算法]
---

# 数值分析-特征值问题与幂法QR算法

> "由 Abel-Ruffini 定理，五次以上代数方程无根式解。因此任何特征值算法都必须是迭代算法。QR 算法是矩阵谱计算的现代标准。"

---

## 1. 算法体系与数学原理

### 1. 幂迭代（Power Iteration）
用于求解模最大的主特征值 $\lambda_1$：
$$v_{k+1} = \frac{A v_k}{\|A v_k\|}, \quad \lambda^{(k)} = v_k^T A v_k$$
收敛速度为线性收敛，比率为 $\left| \frac{\lambda_2}{\lambda_1} \right|$。

### 2. 带位移反幂法（Inverse Iteration with Shift）
用于精确求解最接近 $\mu$ 的特征值 $\lambda$：
$$(A - \mu I) w_{k+1} = v_k, \quad v_{k+1} = \frac{w_{k+1}}{\|w_{k+1}\|}$$
收敛比率为 $\left| \frac{\lambda_i - \mu}{\lambda_j - \mu} \right|$。当 $\mu$ 逼近目标特征值时，发生超线性甚至立方收敛！

### 3. 对称 QR 算法（Symmetric QR Algorithm）
1. 先通过相似正交变换将 $A$ 化为三对角形式（Hessenberg 形式）$A_0 = Q_0^T A Q_0$；
2. 迭代执行带 Wilkinson 位移的 QR 分解：
   $$A_k - \mu_k I = Q_k R_k \implies A_{k+1} = R_k Q_k + \mu_k I = Q_k^T A_k Q_k$$
3. 非对角元以立方收敛速度迅速趋于 0，对角线上解耦出全部特征值。

---

## 2. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---

## 3. 检索练习与自测

1. 证明在 QR 算法中，$A_{k+1} = R_k Q_k$ 与 $A_k = Q_k R_k$ 具有完全相同的特征值。
2. 简述 Rayleigh 商迭代（Rayleigh Quotient Iteration）的定义并说明其局部收敛阶。
