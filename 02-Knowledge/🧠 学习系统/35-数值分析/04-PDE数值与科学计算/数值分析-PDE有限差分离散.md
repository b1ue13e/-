---
type: study
topic: "PDE有限差分离散"
course: "数值分析"
created: 2026-08-08
updated: 2026-08-08
status: completed
stage_moc: "[[🧭 阶段4-PDE数值与科学计算]]"
upstream: ["[[数值分析-前置-泰勒展开与截断误差]]", "[[数值分析-LU分解与数值稳定性]]"]
flow: knowledge
kind: concept
tags: [学习, 数值分析, 偏微分方程, 有限差分, 5点模板, Poisson方程, CSR稀疏]
---

# 数值分析-PDE有限差分离散

> “偏微分方程（PDE）离散化是整个数值分析的终极综合舞台。空间微分算子通过 Taylor 展开转化为离散代数网格，将无穷维函数微积分精确映射为超大规模稀疏线性系统 $A u = f$。”

---

## 1. 严密数学推导与 5 点差分模板

考虑二维经典 Poisson 椭圆边值问题：
$$-\Delta u = -\left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right) = f(x, y), \quad (x, y) \in \Omega = (0, 1)^2$$
边界条件为 Dirichlet 边界 $u|_{\partial \Omega} = g(x, y)$。

### 1.1 均匀网格离散化
在单位正方形上划分 $N \times N$ 等距网格，步长 $h = \frac{1}{N}$，网格节点为 $(x_i, y_j) = (ih, jh)$（$0 \le i, j \le N$）。
在内部节点 $(x_i, y_j)$ 处，利用前置知识中的二阶中心差分 Taylor 展开：
$$-\frac{\partial^2 u}{\partial x^2}(x_i, y_j) = -\frac{u_{i+1, j} - 2u_{i, j} + u_{i-1, j}}{h^2} + \frac{h^2}{12} \frac{\partial^4 u}{\partial x^4}(\xi_{i,j})$$
$$-\frac{\partial^2 u}{\partial y^2}(x_i, y_j) = -\frac{u_{i, j+1} - 2u_{i, j} + u_{i, j-1}}{h^2} + \frac{h^2}{12} \frac{\partial^4 u}{\partial y^4}(\eta_{i,j})$$

### 1.2 标准二维五点差分模板（5-Point Stencil）
$$-\Delta_h u_{i,j} = \frac{4u_{i,j} - u_{i+1,j} - u_{i-1,j} - u_{i,j+1} - u_{i,j-1}}{h^2} = f_{i,j} + O(h^2)$$
局部截断误差严格为空间**二阶精度 $O(h^2)$**。

---

## 2. 离散线性系统的 Kronecker 积与代数结构

将内部 $(N-1)^2$ 个未知数按字典序（自然行优先序）排成列向量 $U$。
离散 Laplace 算子矩阵 $A \in \mathbb{R}^{(N-1)^2 \times (N-1)^2}$ 可通过一维差分矩阵 $T_1 = \operatorname{tridiag}(-1, 2, -1)$ 的 **Kronecker 积**精确紧凑表达：
$$A = \frac{1}{h^2} \left( I \otimes T_1 + T_1 \otimes I \right)$$

### 2.1 矩阵代数特征
1. **对称正定（Symmetric Positive Definite, SPD）**：$A = A^T$ 且对任意非零向量 $x^T A x > 0$；
2. **严格对角占优与 M-矩阵**：非对角元全非正，对角元严格为正，满足离散最大值原理（Discrete Maximum Principle）；
3. **谱结构与解析特征值**：
   $$\lambda_{k, l} = \frac{4}{h^2} \left( \sin^2 \frac{k \pi h}{2} + \sin^2 \frac{l \pi h}{2} \right), \quad 1 \le k, l \le N-1$$
   - 最小特征值：$\lambda_{\min} \approx 2 \pi^2$；最大特征值：$\lambda_{\max} \approx \frac{8}{h^2} = 8 N^2$；
   - 谱条件数：$\kappa_2(A) = \frac{\lambda_{\max}}{\lambda_{\min}} = O(h^{-2}) = O(N^2)$。网格每加密一倍，直接求解与未预条件迭代求解难度飙升 4 倍！

---

## 3. 边界条件处理：Dirichlet vs 虚拟点 Neumann

1. **Dirichlet 边界**：将已知边界点的值直接移至右端源项 $f_{i,j}$ 中，保持离散未知数严格在内部网格；
2. **Neumann 边界（无通量 $\left. \frac{\partial u}{\partial x} \right|_{x=0} = 0$）**：
   - 引入外部虚拟点（Ghost Point）$u_{-1, j}$；
   - 利用中心差分 $\frac{u_{1, j} - u_{-1, j}}{2h} = 0 \implies u_{-1, j} = u_{1, j}$；
   - 代入差分模板消除虚拟点，从而在边界处保持严格二阶截断误差 $O(h^2)$。

---

## 4. SciPy CSR 稀疏组装与求解实现

```python
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

def solve_poisson_2d(f_func, g_boundary, N):
    """求解 -Laplace(u) = f 在 (0,1)^2 上带 Dirichlet 边界"""
    h = 1.0 / N
    x = np.linspace(0, 1, N + 1)
    y = np.linspace(0, 1, N + 1)
    X, Y = np.meshgrid(x, y)
    
    n_internal = N - 1
    # 1. 构造一维二阶差分矩阵
    main_diag = 2.0 * np.ones(n_internal)
    off_diag = -1.0 * np.ones(n_internal - 1)
    T1 = sp.diags([off_diag, main_diag, off_diag], [-1, 0, 1], shape=(n_internal, n_internal))
    
    # 2. Kronecker 积组装二维稀疏矩阵 A
    I = sp.eye(n_internal)
    A = (sp.kron(I, T1) + sp.kron(T1, I)) / (h**2)
    A = A.tocsr()
    
    # 3. 组装右端项并吸纳 Dirichlet 边界
    F = f_func(X[1:-1, 1:-1], Y[1:-1, 1:-1])
    b = F.flatten()
    
    # 边界吸收
    b_mat = F.copy()
    # 底部/顶部
    b_mat[0, :] += g_boundary(x[1:-1], 0) / (h**2)
    b_mat[-1, :] += g_boundary(x[1:-1], 1) / (h**2)
    # 左侧/右侧
    b_mat[:, 0] += g_boundary(0, y[1:-1]) / (h**2)
    b_mat[:, -1] += g_boundary(1, y[1:-1]) / (h**2)
    b = b_mat.flatten()
    
    # 4. 稀疏线性求解
    u_internal = spla.spsolve(A, b)
    
    # 组装完整解网格
    U = np.zeros((N + 1, N + 1))
    U[1:-1, 1:-1] = u_internal.reshape((n_internal, n_internal))
    # 填边界
    U[0, :] = g_boundary(x, 0)
    U[-1, :] = g_boundary(x, 1)
    U[:, 0] = g_boundary(0, y)
    U[:, -1] = g_boundary(1, y)
    
    return X, Y, U

if __name__ == "__main__":
    # 测试解 u(x, y) = sin(pi*x)*sin(pi*y), -Laplace(u) = 2*pi^2 * sin(pi*x)*sin(pi*y)
    f_src = lambda x, y: 2.0 * (np.pi**2) * np.sin(np.pi * x) * np.sin(np.pi * y)
    g_bc = lambda x, y: np.zeros_like(x)
    
    X, Y, U_calc = solve_poisson_2d(f_src, g_bc, N=64)
    U_exact = np.sin(np.pi * X) * np.sin(np.pi * Y)
    err = np.max(np.abs(U_calc - U_exact))
    print(f"64x64 网格 2D Poisson 最大绝对误差: {err:.2e} (符合 O(h^2) 收敛阶)")
```

---

## 5. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---

## 6. 检索练习与自测

1. 证明二维 Poisson 差分矩阵 $A$ 是不可约对称正定矩阵（Irreducible SPD）。
2. 写出九点差分模板（9-Point Compact Stencil），并解释它如何将各向同性截断误差提升至四阶精度 $O(h^4)$。
3. 为什么当网格规模 $N \ge 512$ 时，直接求解 `spsolve`（基于稀疏 LU / SuperLU）的内存占用会急剧上升，而必须转向 Krylov 预条件迭代法？
