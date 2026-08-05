---
title: "迭代法CG与GMRES"
date: "2026-08-03"
created: 2026-08-03
type: concept
course: "数值分析"
importance: "A"
tags: [学习, 数值分析]
upstream: [LU分解与数值稳定性, QR分解与最小二乘, 特征值问题与幂法QR算法]
downstream: [预处理与Krylov方法, 稀疏线性方程组, 大规模最小二乘]
status: learning
concept: ["Krylov子空间", "共轭梯度法", "GMRES"]
prerequisites: ["稀疏矩阵存储", "Arnoldi 过程", "最小二乘", "条件数"]
related: ["LU分解与数值稳定性", "QR分解与最小二乘", "特征值问题与幂法QR算法"]
flow: project
kind: concept
template: Obsidian单知识点深度学习模板
---

# 迭代法CG与GMRES

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：$n$ 达百万级时直接法 $O(n^3)$ 不可行（存储 $O(n^2)$ 先爆），Krylov 子空间迭代法（CG/GMRES）是稀疏大规模线性系统的**唯一工程出路**；HW05 要求对 SPD 跑 CG、非对称跑 GMRES 并报告残差收敛曲线与预处理收益（见 [[🧭 开源作业体系-数值分析]]），收敛性的条件数依赖是理解"为什么要预处理"的关键。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> $Ax=b$ 用 [[LU分解与数值稳定性]] 直接法：复杂度 $O(n^3)$、存储 $O(n^2)$——$n=10^6$ 时存储 $8\times10^{12}$ 字节直接爆内存；但 PDE 离散、网络、图问题中 $A$ **稀疏**（每行仅 5-20 个非零元），矩阵乘向量只要 $O(nnz)$。因此必须引入：**Krylov 子空间迭代法**——只反复做"矩阵乘向量 + 少量向量运算"，在 $k$ 维子空间 $\mathcal{K}_k=\operatorname{span}\{b,Ab,\dots,A^{k-1}b\}$ 中找近似解；**CG**（对称正定）、**GMRES**（一般矩阵）是两大主力。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：直接法（LU/QR，$O(n^3)$）是"一把梭"，迭代法（$O(nnz)\times$ 迭代步数）是"稀疏大系统的生存之道"；Krylov 子空间思想承上（幂法就是 $\mathcal{K}_k$ 里最朴素的一维用法，见 [[特征值问题与幂法QR算法]]）启下（Arnoldi 同时用于特征值问题）。预处理（Jacobi/ILU）让收敛速度摆脱条件数的枷锁。
- **实际应用场景**：有限元/有限差分 PDE 求解（FEM 刚度矩阵 SPD → CG 是默认选择）、流体/结构仿真、图与网络分析（PageRank 用幂法同族思想）、深度学习二阶优化（CG 解 Newton 步）、`scipy.sparse.linalg.cg/gmres`。**高频题型/任务**：解释 CG 的"共轭方向 + 残差正交"双重条件；GMRES 的 Arnoldi 最小二乘结构；用 $\kappa(A)$ 预测 CG 迭代步数（$k\propto\sqrt{\kappa}\log(1/\epsilon)$）；比较直接法 vs 迭代法选型；设计预处理实验。

---

## 3. 学它之前需要哪些前置知识？

1. **[[LU分解与数值稳定性]]**：直接法的代价与稳定性是迭代法的对照基准；ILU 预处理直接借用 LU 分解思想；[[QR分解与最小二乘]]：GMRES 每步解一个最小二乘问题（$H_k$ 上用 QR），Krylov 基的正交化就是 Gram-Schmidt/Arnoldi。
2. **[[特征值问题与幂法QR算法]]**：$A^kv_0$ 的谱展开与特征值比——Krylov 收敛性分析的同款工具；[[误差与数值线代-条件与稳定-condition number]]：收敛速度如何依赖条件数。

---

## 4. 用直觉语言解释它

> «"Krylov 子空间就像顺着河流找下游"：只靠反复乘 $A$（每次乘就是"流一步"），把 $b$ 冲出来的轨迹 $\{b,Ab,A^2b,\dots\}$ 张成一个不断长大的子空间，近似解就在这个子空间里"挑最好的"——CG 挑"误差在 $A$-范数下最小"的，GMRES 挑"残差 2-范数最小"的。矩阵乘向量是唯一重活，稀疏时每次只要 $O(nnz)$，所以迭代几十步就比 $O(n^3)$ 直接法便宜。"»（参考：Trefethen & Bau, Lecture 32-38）

- **直觉类比**：CG = 在越来越大的 Krylov 子空间里做"共轭方向上的精确一维最优"——每步选一个与之前所有方向 $A$-正交的新方向（"共轭"），步长使误差在该方向最小；GMRES = "在子空间里做最小二乘投影"，残差必然单调不增。
- **为什么很自然**：$x_k=x_0+\mathcal{K}_k(A,r_0)$ 只用了"乘 $A$"这个最便宜的运算；子空间每步只扩一维，正交化保证基稳定（Arnoldi）。**一句话直觉本质**：**"迭代法用'反复乘 $A$'替代'分解 $A$'：CG 是 SPD 下的共轭方向最优（误差 $A$-范数最小），GMRES 是一般矩阵下的子空间最小二乘（残差单调下降）；收敛速度由条件数/谱决定，预处理把 $\kappa$ 压小就提速。"**

---

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义
- **Krylov 子空间**：$\mathcal{K}_k(A,r_0)=\operatorname{span}\{r_0,Ar_0,\dots,A^{k-1}r_0\}$，迭代解 $x_k\in x_0+\mathcal{K}_k$。
- **CG（共轭梯度法）**：$A$ 对称正定时，$x_k$ 使 $\|x-x_k\|_A$ 在 $x_0+\mathcal{K}_k$ 上最小；残差 $r_k=b-Ax_k$ 与 $\mathcal{K}_k$ 正交；每步只需 1 次 matvec、5 个向量，存储 $O(n)$。
- **GMRES（广义最小残差）**：一般矩阵（可非对称、可不定），$x_k$ 使 $\|b-Ax_k\|_2$ 在 $x_0+\mathcal{K}_k$ 上最小；用 **Arnoldi 过程**（修正 Gram-Schmidt）构造正交基 $V_k$ 与 Hessenberg 矩阵 $H_k$，残差单调不增；存储 $O(kn)$，需重启（GMRES(m)）。

### 2. 核心公式
$$\mathcal{K}_k(A,r_0)=\operatorname{span}\{r_0,Ar_0,\dots,A^{k-1}r_0\},\qquad x_k\in x_0+\mathcal{K}_k$$
$$\text{CG：}\|x-x_k\|_A=\min_{x\in x_0+\mathcal{K}_k}\|x-x_0\|_A,\qquad \frac{\|x-x_k\|_A}{\|x-x_0\|_A}\le 2\left(\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}\right)^k$$
$$\text{GMRES：}\|b-Ax_k\|_2=\min_{x\in x_0+\mathcal{K}_k}\|b-Ax\|_2,\qquad \text{Arnoldi: }AV_k=V_{k+1}\underline{H}_k$$
$$\text{Arnoldi 分解：}AV_k=V_{k+1}\bar{H}_k,\quad V_k^TV_k=I_k,\quad \bar{H}_k\in\mathbb{R}^{(k+1)\times k}\ \text{上 Hessenberg}$$

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\mathcal{K}_k$ | $k$ 维 Krylov 子空间 | $\mathbb{R}^n$ 的子空间 | 由 $r_0$ 反复乘 $A$ 生成 |
| $r_k$ | 残差 $b-Ax_k$ | $\mathbb{R}^n$ | CG 中与 $\mathcal{K}_k$ 正交 |
| $\|x\|_A$ | $A$-范数 $\sqrt{x^TAx}$ | SPD 下为范数 | CG 的度量 |
| $\kappa(A)$ | 2-范数条件数 | $\ge1$ | CG 收敛界只依赖 $\kappa$ |
| $V_k,\bar{H}_k$ | Arnoldi 正交基 / Hessenberg | $V_k^TV_k=I$ | GMRES 的核心结构 |
| $nnz$ | 非零元个数 | $\ll n^2$（稀疏） | 每次 matvec 代价 $O(nnz)$ |

### 4. 常见变体与适用条件
- **变体**：CG（SPD）、BiCGSTAB / GMRES(m)（一般矩阵）、MINRES（对称不定）、Lanczos（对称特征值）、预处理版 PCG/PGMRES。**适用条件**：CG 要求 $A$ 对称正定（否则"共轭方向"失效）；GMRES 对任意非奇异矩阵收敛（$k\le n$ 时有限步终止），但步数多时存储爆炸。**限制**：$\kappa$ 大时 CG/GMRES 都慢——必须预处理（Jacobi、SSOR、ILU、多重网格）；矩阵乘积 $Ax$ 必须廉价（稀疏/结构化），稠密小矩阵直接用 LU。

---

## 6. 推导思路和思想来源

- **最初困难**：直接法对 $n\gg10^5$ 的稀疏系统存储和浮点量都是灾难；古典迭代（[[误差与数值线代-线性方程组-Jacobi]]/GS）收敛慢且依赖谱半径 $\rho<1$ 的强条件。**关键"转念"**（Hestenes-Stiefel 1952 / Saad-Schultz 1986）：**不固定迭代格式，而是在"乘 $A$ 生成的子空间"里做最优投影**——把"解方程"变成"子空间上的优化问题"，且子空间逐维生长时只需增量更新（共轭方向 / Arnoldi 正交基）。
- **推导主线**：幂法启示（$A^kr_0$ 携带谱信息）→ Krylov 子空间 $\mathcal{K}_k$ → 投影条件（Petrov-Galerkin）→ SPD 时能量范数最小化 → CG 三递推（$x,p,r$，共轭方向 $p_k^TAp_j=0$）→ 收敛界由 Chebyshev 多项式最优逼近导出（$\kappa$ 的平方根！）→ 一般矩阵改为残差最小化 → Arnoldi 正交化把问题化为 $(k+1)\times k$ 最小二乘 → 每步用 Givens 旋转增量解之（GMRES）。CG 的 $\sqrt{\kappa}$ 而非 $\kappa$ 来自 Chebyshev 多项式在区间 $[\lambda_{\min},\lambda_{\max}]$ 上的最优性——**谱越聚集收敛越快，这就是预处理的理论依据**。**为什么自然**：最小化 $\|x-x_k\|_A$ 等价于误差在 $\mathcal{K}_k$ 的 $A$-正交补上投影，Chebyshev 加速使收敛率从 $(\kappa-1)/(\kappa+1)$ 提升到 $(\sqrt\kappa-1)/(\sqrt\kappa+1)$；GMRES 的 Arnoldi 分解把 $n$ 维问题压成 $k$ 维 Hessenberg 最小二乘——"正交化 + 最小二乘"正是 [[QR分解与最小二乘]] 的复用。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）
- **题目**：$A=\begin{pmatrix}2&0\\0&4\end{pmatrix}$，$b=(2,4)^T$，$x_0=0$。CG 第一步后 $x_1$ 是多少？
- **解题思路与关键步骤**：$r_0=b=(2,4)^T$，$p_0=r_0$；$\alpha_0=r_0^Tr_0/(p_0^TAp_0)=(4+16)/(2\cdot4+4\cdot16)=20/72=5/18$；$x_1=x_0+\alpha_0p_0=(10/18,20/18)^T=(5/9,10/9)^T$。因 $A$ 对角、$b$ 恰沿两个特征方向，理论上两步收敛（$n=2$）。
- **最终答案**：$x_1=(5/9,10/9)^T$，残差 $r_1=(2-10/9,4-40/9)^T=(8/9,-4/9)^T$，与 $p_0$ 正交（$r_1^Tp_0=16/9-16/9=0$）。**易错点**：$\alpha$ 用 $A$-内积 $p^TAp$ 而非 $p^Tp$；忘记"共轭方向"条件 $p_k^TAp_j=0$。
- **🤔 追问**：若 $A$ 改为 $\begin{pmatrix}2&100\\100&4\end{pmatrix}$（不定）？——$\|x\|_A$ 不再是范数，CG 的"最小化"无意义，算法发散或振荡，必须换 GMRES/MINRES。

### 例子 2：中等例子（条件判断与多步推理）
- **题目与完整解答**：$A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$（SPD，$\lambda=1,3$，$\kappa=3$），$b=(3,3)^T$，$x_0=0$。CG 两步应精确收敛（$n=2$）：$r_0=(3,3)^T$，$\alpha_0=r_0^Tr_0/(p_0^TAp_0)=18/(2\cdot9+2\cdot9)=18/36=1/2$，$x_1=(1.5,1.5)^T$，$r_1=(3,3)^T-(3,3)^T=0$——**一步就收敛**，因为 $b$ 恰是特征向量 $(1,1)^T$ 的倍数（谱信息全在 $r_0$ 里）。若 $b=(3,1)^T$：$r_1\ne0$，第二步沿 $p_1=r_1+\beta_0p_0$ 补完，两步收敛。**易错点**：以为"迭代步数 = 矩阵规模"；实际 CG 步数由**谱聚集程度**（$\kappa$ 与特征值分布）决定，$b$ 靠近少数特征方向时远少于 $n$ 步。

### 例子 3：实际应用例子（真实场景/代码）
```python
import numpy as np

def cg(A, b, x0=None, tol=1e-10, maxit=1000):
    x = np.zeros_like(b) if x0 is None else x0.copy()
    r = b - A @ x; p = r.copy(); rs = r @ r
    for k in range(maxit):
        Ap = A @ p
        alpha = rs / (p @ Ap)
        x += alpha * p
        r -= alpha * Ap
        rs_new = r @ r
        if np.sqrt(rs_new) < tol: return x, k + 1
        beta = rs_new / rs; p = r + beta * p; rs = rs_new
    return x, maxit

n = 2000
A = np.zeros((n, n))                      # 1D 泊松:三对角 SPD
np.fill_diagonal(A, 2.0)
np.fill_diagonal(A[1:], -1.0); np.fill_diagonal(A[:, 1:], -1.0)
b = np.random.default_rng(0).normal(size=n)
x, it = cg(A, b)
ref = np.linalg.solve(A, b)
print(f"CG: {it} 步, 相对误差 {np.linalg.norm(x-ref)/np.linalg.norm(ref):.2e} (κ≈4n²/π²≈{np.linalg.cond(A):.0f})")
```
- **观察与解读**：1D 泊松 $\kappa\approx4n^2/\pi^2\approx1.6\times10^6$，理论步数 $\propto\sqrt\kappa\approx1300$——CG 实际约几百步收敛；**加 Jacobi/ILU 预处理后步数降到 $\sim\sqrt{\kappa_{\text{pre}}}$**（HW05 验收点：报告残差收敛曲线 + 预处理前后对比）。**🤔 追问**：换 2D 泊松（五对角）？$\kappa\sim n$（$n$ 为每维网格数），步数随网格细化增长——这就是多重网格/预处理的动机。

---

## 8. 常见误区和易混概念

### 误区 1：以为"CG 可以解任何 $Ax=b$"
- **错误直觉**：梯度下降思想通用，CG 也是"沿着梯度走"，非对称矩阵也能用。**为什么错**：CG 依赖 $A$-内积 $\langle x,y\rangle_A=x^TAy$ 是内积（需 SPD）与三递推（短递推）——非对称时 $A$-正交性丢失，短递推不稳定，收敛性无保证。**正确理解**：对称正定 → CG/MINRES；一般矩阵 → GMRES（长递推，每步全正交化）或 BiCGSTAB。

### 误区 2：以为"GMRES 每步都更贵所以不如直接法"
- **错误直觉**：GMRES 每步做 Arnoldi 正交化 $O(kn)$，$k$ 大时开销大，不如 LU 一次搞定。**为什么错**：直接法 $O(n^3)$ 且**填充**让稀疏矩阵变稠密（$L,U$ 的非零元可远多于 $A$）；GMRES 每步只 $O(nnz)$ matvec + $O(kn)$ 正交化，且通常 $k\ll n$；步数超限可用**重启**（GMRES(m)）与**预处理**控制。**正确理解**：稠密小矩阵用直接法，稀疏大矩阵用迭代法；"谁快"取决于 $nnz$、$n$ 与迭代步数的三方权衡。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| CG | SPD 线性系统 | 短递推、$O(n)$ 存储、误差 $A$-范数最小 | FEM 刚度阵、扩散方程 |
| GMRES | 一般矩阵 | Arnoldi+最小二乘、残差单调、存储 $O(kn)$ | 对流主导 PDE、非对称网络 |
| MINRES | 对称不定 | 短递推变体 | 鞍点问题（Stokes） |
| 直接法（LU） | 任意方阵 | $O(n^3)$、需主元、填充 | 稠密/中小规模（见 [[LU分解与数值稳定性]]） |
| 幂法 | 最大特征值 | Krylov 子空间 $k=1$ 的朴素版 | PageRank（见 [[特征值问题与幂法QR算法]]） |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[LU分解与数值稳定性]]：直接法基准与 ILU 预处理（"不完全 LU"即截断填充的 LU）；HW05 直接法 vs 迭代法对比实验的对照；[[QR分解与最小二乘]]：GMRES 每步的最小二乘求解（Givens/QR 处理 $\bar{H}_k$），Arnoldi = 带 Hessenberg 结构的修正 Gram-Schmidt。
- [[特征值问题与幂法QR算法]]：$A^kr_0$ 谱展开同源；Lanczos/Arnoldi 同时是特征值算法。

### 下游延伸
- 预处理与 Krylov 方法（Jacobi/SSOR/ILU/多重网格）：收敛速度的工程开关（待建卡）；稀疏线性方程组（[[误差与数值线代-线性方程组-Jacobi]]、[[误差与数值线代-线性方程组-GS]]）：古典迭代是 Krylov 的前史，收敛条件 $\rho<1$ 对比 CG 的 $\kappa$ 依赖。

### 横向关联
- [[误差与数值线代-条件与稳定-condition number]] ↔ 本知识点：$\sqrt\kappa$ 收敛界是"条件数决定迭代步数"的定量版本；[[浮点算术与误差分析]] ↔ 本知识点：迭代法的停止准则用**残差**而非真误差——残差小 ≠ 误差小（病态时），与 LU 的误区同构。

### 应用场景
- [[🧭 开源作业体系-数值分析]]：HW05 对 SPD 跑 CG、非对称跑 GMRES，报告残差收敛曲线、条件数影响与预处理收益；[[03-Projects/课程作业/35-数值分析/课程作业总表|作业单元挂载]]。

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
- [ ] 1. 用一句话说清楚它解决什么问题。
- [ ] 2. 用直觉语言解释 Krylov 子空间与 CG/GMRES（«"顺着河流找下游…"»）。
- [ ] 3. 写出 $\mathcal{K}_k$ 定义与 CG/GMRES 的最优性条件。
- [ ] 4. 写出 CG 收敛界与 GMRES 的 Arnoldi 分解公式。
- [ ] 5. 解释"共轭方向"与"残差正交"两个条件。
- [ ] 6. 讲出"CG 为什么依赖 SPD、$\sqrt\kappa$ 从哪来"的推导主线。
- [ ] 7. 手算 2×2 CG 一步并验证残差正交。
- [ ] 8. 说出 CG/GMRES/直接法选型的两个误区。
- [ ] 9. 说出它与 LU、QR、幂法三个知识点的关系。
- [ ] 10. 说出一个真实应用场景（FEM/`scipy.sparse.linalg.cg`/深度学习二阶优化）。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | Krylov 子空间与 CG 适用条件 |
| 2 | 公式运用 | 基础 | 手算 CG 一步 |
| 3 | 条件判断 | 中等 | CG vs GMRES 选型 |
| 4 | 变式/综合 | 中等 | $\sqrt\kappa$ 收敛界与预处理 |
| 5 | 开放/证明/建模 | 较难 | 设计 GMRES 实验验证残差单调性（HW05 口径） |

### 题目与解析

#### 1. 为什么 CG 只适用于对称正定矩阵？非对称时哪个量不再是内积？
> [!question]- 答案解析
> - **答案**：CG 的收敛分析依赖 $\langle x,y\rangle_A=x^TAy$ 是内积（$\|x\|_A$ 是范数），且共轭方向 $p_i^TAp_j=0$ 需要 $A$ 对称；非对称时 $A$-内积不对称、能量范数无定义，短递推失效。非对称矩阵改用 GMRES（残差 2-范数最小化）或 BiCGSTAB。
> - **解析**：SPD ⇔ $\|x\|_A$ 是范数 ⇔ "误差 $A$-范数最小"有意义。易错：把"对称"和"正定"分开记——对称不定用 MINRES，非对称用 GMRES。 `#自测题/基础`

#### 2. 对 $A=\begin{pmatrix}3&0\\0&6\end{pmatrix}$、$b=(3,6)^T$、$x_0=0$，手算 CG 第一步。
> [!question]- 答案解析
> - **答案**：$r_0=p_0=(3,6)^T$；$\alpha_0=r_0^Tr_0/(p_0^TAp_0)=(9+36)/(3\cdot9+6\cdot36)=45/243=5/27$；$x_1=(5/9,10/9)^T$；$Ax_1=(5/3,20/3)^T$，$r_1=(4/3,-2/3)^T$；验证 $r_1^Tr_0=4-4=0$ ✓（残差与 $\mathcal{K}_1$ 正交）。
> - **解析**：$\alpha$ 分母是 $A$-内积 $p^TAp$（不是 $p^Tp$）；$\beta$ 用普通内积 $r^Tr$。易错：$\alpha$ 分母写成 $p^Tp$、或手算符号出错——**务必逐项验算残差正交性**（$r_1^Tr_0=0$）作为自检。本例 $A$ 对角且 $b$ 沿两特征方向，第二步必精确收敛（$n=2$）。

#### 3. 一个 $10^6\times10^6$ 稀疏非对称矩阵（每行 7 个非零元），选 CG、GMRES 还是 LU？为什么？
> [!question]- 答案解析
> - **答案**：GMRES（或 BiCGSTAB）——矩阵非对称，CG 不适用；LU 的 $O(n^3)$ 与填充在 $10^6$ 规模下不可行（存储即爆）。配 ILU 预处理控制步数与存储，必要时 GMRES(m) 重启。**解析**：选型三问：对称吗（CG/MINRES）？稀疏吗（迭代法）？条件数可控吗（预处理）？易错：因"GMRES 存储 $O(kn)$"而犹豫——重启 + 预处理是标准解，且 $k\ll n$ 时仍远小于 LU 的填充。

#### 4. CG 收敛界 $\|x-x_k\|_A\le2\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^k\|x-x_0\|_A$ 说明什么？预处理为何有效？
> [!question]- 答案解析
> - **答案**：收敛率由 $\sqrt\kappa$ 决定：$\kappa=10^6$ 时每步因子 $\approx(10^3-1)/(10^3+1)\approx0.998$，约 $k\approx\frac12\sqrt\kappa\ln(2/\epsilon)\approx6900$ 步；若预处理把 $\kappa$ 压到 10，因子 $\approx0.52$，约 30 步。**预处理（Jacobi/ILU）等价于解 $M^{-1}Ax=M^{-1}b$ 且 $\kappa(M^{-1}A)\ll\kappa(A)$**。**解析**：$\sqrt\kappa$ 来自 Chebyshev 多项式在谱区间上的最优逼近——特征值越聚集越快。易错：把"条件数大"仅归咎于算法，忽视"先预处理再迭代"是工程标配。

#### 5. 设计实验：对非对称矩阵验证"GMRES 残差单调不增、CG 残差不单调"，并与 LU 直接法对照（HW05 口径）。
> [!question]- 答案解析
> - **答案**：取 $A=\begin{pmatrix}2&-1\\0&2\end{pmatrix}+$ 随机扰动（非对称）与随机 $b$；跑自实现 GMRES（Arnoldi + 每步 Givens 旋转解 $\min\|e_1-\bar H_k y\|$）记录 $\|r_k\|_2$ 序列（应单调不增）；同 $b$ 跑 CG（预期发散或振荡）。对照 `np.linalg.solve` 的真解，报告 $\|x_k-x_{\text{true}}\|/\|x_{\text{true}}\|$ 与残差两条曲线，并说明"残差小≠误差小"（条件数大时）。**解析**：GMRES 残差单调由最小二乘最优性保证（每步子空间扩大，最优残差不增）；CG 只保证 $A$-范数误差单调，残差可振荡——这是两类算法最直观的判别实验。易错：只用 `scipy.sparse.linalg` 现成函数不做自实现与高精度对照，违反验收口径。

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

### 我的推导复现
> 不看上文，尝试写出核心公式或推导主线：

### 我的错误与卡点
-

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/35-数值分析/`
- **关联已有笔记**：[[🧭 开源作业体系-数值分析]]、[[LU分解与数值稳定性]]、[[QR分解与最小二乘]]、[[特征值问题与幂法QR算法]]、[[浮点算术与误差分析]]、[[误差与数值线代-线性方程组-Jacobi]]、[[误差与数值线代-线性方程组-GS]]、[[误差与数值线代-条件与稳定-condition number]]；**建议标签**：`#学习` `#数值分析` `#迭代法` `#Krylov子空间` `#CG` `#GMRES` `#概念`
- **拆分建议**：收敛性证明（Chebyshev 最优逼近）可拆"推导笔记"；预处理实验可拆到 HW05 作业单元；若深入特征值应用，Arnoldi/Lanczos 可挂靠 [[特征值问题与幂法QR算法]]。
