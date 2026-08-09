---
type: study
topic: "迭代法CG与GMRES"
course: "数值分析"
created: 2026-08-08
status: ongoing
stage_moc: "[[🧭 阶段4-PDE数值与科学计算]]"
upstream: ["[[数值分析-PDE有限差分离散]]", "[[数值分析-QR分解与最小二乘]]"]
flow: knowledge
kind: concept
tags: [学习, 数值分析, Krylov子空间, 共轭梯度法, CG, GMRES, 预处理]
---

# 数值分析-迭代法CG与GMRES

> "对于源自三维 PDE 离散的数千万未知数稀疏方程组，直接法 LU 的内存填充（Fill-in）会导致内存爆炸。Krylov 子空间投影迭代法（CG / GMRES）每次只需一次稀疏矩阵向量乘法，是现代科学计算的绝对主干。"

---

## 1. 严密数学推导与 Krylov 子空间投影

给定初始解 $x_0$ 及残差 $r_0 = b - A x_0$。$k$ 阶 Krylov 子空间定义为：
$$\mathcal{K}_k(A, r_0) = \operatorname{span}\{r_0, A r_0, A^2 r_0, \dots, A^{k-1} r_0\}$$

### 1. 共轭梯度法 (Conjugate Gradient, CG)
专用于**对称正定矩阵（SPD）**。在 $\mathcal{K}_k(A, r_0)$ 中寻找解 $x_k$，使得误差在 $A$-范数下达到严格最小：
$$\|x_k - x^*\|_A = \min_{x \in x_0 + \mathcal{K}_k} \|x - x^*\|_A, \quad \|e\|_A = \sqrt{e^T A e}$$

**收敛误差上界定理**：
$$\|x_k - x^*\|_A \le 2 \left( \frac{\sqrt{\kappa_2(A)} - 1}{\sqrt{\kappa_2(A)} + 1} \right)^k \|x_0 - x^*\|_A$$
若条件数 $\kappa_2(A) = 10^4$，每迭代 1 步误差减少约 $2\% $；收敛所需步数 $k = O(\sqrt{\kappa_2(A)}) = O(N)$。

### 2. GMRES 算法（广义极小残差法）
用于**一般非对称非奇异矩阵**。通过 Arnoldi 过程构造 $\mathcal{K}_k(A, r_0)$ 的正交基 $V_k$，在每一步求解一个 $(k+1) \times k$ 的最小二乘问题：
$$\|b - A x_k\|_2 = \min_{x \in x_0 + \mathcal{K}_k} \|b - A x\|_2$$

### 3. 预条件技术（Preconditioning）
将系统改写为 $M^{-1} A x = M^{-1} b$。若预条件子 $M \approx A$ 使得 $\kappa(M^{-1}A) \approx 1$，CG 可以在极少步数内骤速收敛。常用预条件子包括 Jacobi（对角）、不完全 Cholesky（IC）和代数多重网格（AMG）。

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

1. 证明共轭梯度法生成的搜索方向序列 $\{p_k\}$ 互相满足 $A$-正交（共轭）性：$p_i^T A p_j = 0 (i \ne j)$。
2. 解释重启 GMRES（GMRES(m)）为什么必须设置重启步数 $m$，以及可能遭遇的停滞现象。
