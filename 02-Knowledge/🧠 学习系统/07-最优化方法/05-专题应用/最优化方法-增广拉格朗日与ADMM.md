---
type: study
course: 07-最优化方法
topic: 增广拉格朗日与ADMM
created: '2026-08-06'
status: completed
flow: knowledge
kind: derivation
stage_moc: '[[🧭 阶段5-专题应用]]'
upstream:
  - '[[最优化方法-近端梯度与FISTA]]'
  - '[[最优化方法-凸优化与拉格朗日对偶]]'
---
﻿---

type: study
topic: 增广拉格朗日与ADMM
course: 07-最优化方法
created: 2026-08-05
status: ongoing
stage_moc: '[[🧭 阶段5-专题应用]]'
flow: knowledge
kind: concept
tags:
- 学习
- 最优化方法
difficulty: advanced
concept:
- 增广拉格朗日
- ADMM
- 算子分裂
prerequisites:
- 凸优化与拉格朗日对偶
- 强对偶与Slater条件
related:
- 近端梯度与FISTA
- 内点法原理

---


## 0. 学习边界
- **类别**：A+ 类 (现代大规模优化、分布式优化的绝对基石)
- **判断理由**：交替方向乘子法（Alternating Direction Method of Multipliers, ADMM）融合了对偶上升法的可分解性和增广拉格朗日方法（ALM）的良好收敛性。在机器学习、信号处理、统计学中的L1正则化问题（如LASSO）、分布式共识优化（Consensus Optimization）中，ADMM是首选框架之一。由于其易于实现并行化与分布式，它是解决大规模数据的现代优化必备技能。

---
## 1. 这个知识点解决什么问题？
> **我们遇到了什么麻烦**：
当我们面对一个带有复杂约束的凸优化问题：$\min f(x) + g(z) \quad \text{s.t. } Ax + Bz = c$ 时：
1. **直接拉格朗日对偶上升（Dual Ascent）**：可以分别对 $x$ 和 $z$ 并行求解，但在许多问题中不收敛，或者要求目标函数极其严格（强凸）。
2. **增广拉格朗日法（Method of Multipliers, ALM）**：引入二次惩罚项增强了收敛性（不要求强凸也能收敛），但二次项 $\|Ax+Bz-c\|^2$ 使得 $x$ 和 $z$ 耦合在了一起，破坏了可分解性，无法分块/分布式求解！
我们需要一种方法，既有 ALM 的强健收敛性，又有 Dual Ascent 的拆分/并行求解能力。

---
## 2. 为什么它重要？它有什么用？
- **连接大图景**：它是理解算子分裂（Operator Splitting）的核心。它连接了近端算法（Proximal Algorithms）与拉格朗日对偶。
- **实际应用场景**：
  - **LASSO等带有不可导项的优化**：将平滑项和不可导项分离。
  - **分布式机器学习**：数据分布在不同机器上（Consensus ADMM），每台机器只用本地数据算一个梯度/近端操作，最后通过一个主节点汇总（更新对偶变量）。
  - **图像去噪（TV正则化）**、稀疏主成分分析。
- **高频题型/任务**：
  - 将一个具体问题（如 LASSO 或 Basis Pursuit）改写为 ADMM 标准形式。
  - 推导 ADMM 的 x-update, z-update 和 dual update 步骤。
  - 用 Proximal Operator 表示 ADMM 的子问题。

---
## 3. 学它之前需要哪些前置知识？
1. **[[最优化方法-凸优化与拉格朗日对偶]]**：必须熟悉拉格朗日函数 $L(x, \lambda)$ 及对偶问题。
2. **[[最优化方法-近端梯度与FISTA]]**：理解 $\text{prox}_{f}(v) = \arg\min_x (f(x) + \frac{1}{2}\|x-v\|^2)$。

---
## 4. 用直觉语言解释它
> «"这东西其实就像……项目经理（对偶变量/乘子）协调前端团队 x 和后端团队 z。"»
- **直觉类比/几何图像**：
  - **Dual Ascent** 是项目经理发号施令，前端和后端各自独立干活，但经常对不齐接口。
  - **ALM** 是把前端和后端关进一个办公室强行让他们一起写代码（二次惩罚使得两者耦合），结果导致系统瘫痪（无法分布式求解）。
  - **ADMM** 则是：先让前端根据当前经理的要求和后端的进度干活（x-update），然后让后端根据前端刚给出的最新结果干活（z-update），最后经理根据两边最终接口的差距调整惩罚力度（对偶更新）。这就是**交替（Alternating）**的思想！
- **一句话直觉本质**：在增广拉格朗日框架下，放弃求全变量的绝对最小值，改为采用 Gauss-Seidel 风格的轮换极小化，从而恢复问题的可分性。

---
## 5. 正式定义、核心公式、符号解释
### 1. 核心模型与增广拉格朗日函数
标准 ADMM 解决的问题形式：
$$ \min_x \ f(x) + g(z) $$
$$ \text{s.t. } Ax + Bz = c $$
其中 $f$ 和 $g$ 均为凸函数。
**增广拉格朗日函数 (Augmented Lagrangian, AL)**：
$L_\rho(x, z, y) = f(x) + g(z) + y^T(Ax + Bz - c) + \frac{\rho}{2}\|Ax + Bz - c\|_2^2$
其中 $y$ 是对偶变量，$\rho > 0$ 是惩罚参数。

### 2. ADMM 三步迭代算法
ADMM 的迭代 $k \to k+1$ 包含三步：
1. **$x$-update**：极小化关于 $x$ 的 $L_\rho$（保持 $z^k, y^k$ 固定）：
   $x^{k+1} = \arg\min_x L_\rho(x, z^k, y^k)$
2. **$z$-update**：极小化关于 $z$ 的 $L_\rho$（使用最新的 $x^{k+1}$，保持 $y^k$ 固定）：
   $z^{k+1} = \arg\min_z L_\rho(x^{k+1}, z, y^k)$
3. **Dual-update (乘子更新)**：进行梯度上升：
   $y^{k+1} = y^k + \rho (Ax^{k+1} + Bz^{k+1} - c)$

### 3. Scaled Form (缩放形式)
在实际推导和编程中，通常采用更为简洁的 Scaled Form。令缩放后的对偶变量为 $u = (1/\rho)y$。
增广拉格朗日函数的惩罚项可以合并为：
$L_\rho = f(x) + g(z) + \frac{\rho}{2} \|Ax + Bz - c + u\|_2^2 - \frac{\rho}{2}\|u\|_2^2$
**Scaled ADMM 算法步骤**：
1. $x^{k+1} = \arg\min_x \left( f(x) + \frac{\rho}{2}\|Ax + Bz^k - c + u^k\|_2^2 \right)$
2. $z^{k+1} = \arg\min_z \left( g(z) + \frac{\rho}{2}\|Ax^{k+1} + Bz - c + u^k\|_2^2 \right)$
3. $u^{k+1} = u^k + (Ax^{k+1} + Bz^{k+1} - c)$

---
## 6. 推导思路和思想来源
- **基础法 1：对偶上升法**
  $L_0(x,z,y) = f(x)+g(z) + y^T(Ax+Bz-c)$。求极大极小。
  $x^{k+1}, z^{k+1} = \arg\min_{x,z} L_0(x,z,y^k)$ (由于没有二次项，可完全并行)。
  然后 $y^{k+1} = y^k + \alpha^k (Ax^{k+1} + Bz^{k+1} - c)$。但这要求严格凸性。
- **基础法 2：乘子法 (ALM)**
  加入 $\frac{\rho}{2}\|Ax+Bz-c\|^2$ 使得函数处处强凸。
  $(x^{k+1}, z^{k+1}) = \arg\min_{x,z} L_\rho(x, z, y^k)$。这步极小化难以拆分。
  然后更新 $y$。为什么 $y$ 的步长恰好是 $\rho$？因为这恰好使得 $Ax^{k+1} + Bz^{k+1} - c$ 趋近于 0（对偶可行性最优条件）。
- **合并两者的智慧：ADMM**
  不要一次性对 $(x,z)$ 联合极小化，而是拆分成两步：先固定 $z$ 优化 $x$，再固定最新的 $x$ 优化 $z$。这样既利用了 $\rho$ 带来的良好收敛性，又恢复了并行的可能（或易求解的子问题）。

---
## 7. 例子：基础 → 中等 → 实际应用
### 例子 1：LASSO 回归的 ADMM 形式
**问题**：$\min \frac{1}{2}\|Ax - b\|_2^2 + \lambda \|x\|_1$
**构造 ADMM 形式**：
引入辅助变量 $z$，使得 $\min \frac{1}{2}\|Ax - b\|_2^2 + \lambda \|z\|_1 \quad \text{s.t. } x - z = 0$。
这里 $f(x) = \frac{1}{2}\|Ax - b\|_2^2$, $g(z) = \lambda \|z\|_1$。矩阵 $A$在标准式中是 $I$, $B = -I$, $c=0$。
**迭代步骤推导 (Scaled Form)**：
1. **$x$-update**: $x^{k+1} = \arg\min_x \frac{1}{2}\|Ax - b\|_2^2 + \frac{\rho}{2}\|x - z^k + u^k\|_2^2$。这是一个二次函数，直接求导置零得：$(A^TA + \rho I)x = A^Tb + \rho(z^k - u^k)$。（这一步解线性方程组）。
2. **$z$-update**: $z^{k+1} = \arg\min_z \lambda \|z\|_1 + \frac{\rho}{2}\|x^{k+1} - z + u^k\|_2^2$。这正是 L1 范数的 Proximal 算子！其闭式解为**软阈值算子 (Soft-Thresholding)**：
   $z^{k+1} = S_{\lambda/\rho}(x^{k+1} + u^k)$，其中 $S_\kappa(a) = \text{sign}(a)\max(|a|-\kappa, 0)$。
3. **$u$-update**: $u^{k+1} = u^k + x^{k+1} - z^{k+1}$。

### 例子 2：Python 实现 LASSO ADMM
```python
import numpy as np

def soft_threshold(v, kappa):
    return np.sign(v) * np.maximum(np.abs(v) - kappa, 0)

def admm_lasso(A, b, lam, rho, max_iter=100):
    m, n = A.shape
    x = np.zeros(n)
    z = np.zeros(n)
    u = np.zeros(n)
    
    # Precompute A^T A + rho I
    AtA_plus_rho = A.T @ A + rho * np.eye(n)
    Atb = A.T @ b
    inv_matrix = np.linalg.inv(AtA_plus_rho) # In practice, use Cholesky decomposition

    for k in range(max_iter):
        # 1. x-update
        x = inv_matrix @ (Atb + rho * (z - u))
        # 2. z-update
        z = soft_threshold(x + u, lam / rho)
        # 3. u-update
        u = u + x - z
        
    return z

# Mock data
np.random.seed(0)
A = np.random.randn(50, 100)
x_true = np.zeros(100)
x_true[np.array([5, 96, 3])] = [5, -4, 3] # Sparse solution (nonzero entries at positions 5, 96, 3)
b = A @ x_true + 0.1 * np.random.randn(50)

x_admm = admm_lasso(A, b, lam=0.1, rho=1.0)
print(f"Non-zero entries in ADMM solution: {np.sum(np.abs(x_admm) > 1e-4)}")
```

---
## 8. 常见误区和易混概念
### 误区 1：认为 ADMM 像梯度下降一样能获得极高精度的解
**澄清**：ADMM 在实际中常被称作“收敛到中等精度很快，但收敛到高精度极慢”的算法。它主要用于大规模机器学习或统计推断，这些场景下不需要小数点后很多位的精度，而是需要快速达到一个不错的预测结果。对于高精度需求，应转用内点法。
### 误区 2：盲目调大惩罚参数 $\rho$ 以加快收敛
**澄清**：$\rho$ 权衡了“残差的可行性”和“目标函数的优化”。$\rho$ 过大导致对偶变量变化过于剧烈且 x-update, z-update 步长过短（滞留）；$\rho$ 过小导致长期不满足等式约束。实际中常使用 **自适应 $\rho$ 更新策略**（当原始残差过大时增大 $\rho$，当对偶残差过大时减小 $\rho$）。

---
## 9. 相关知识点与 Obsidian 双链建议
### 上游依赖
- [[最优化方法-凸优化与拉格朗日对偶]]
- [[最优化方法-近端梯度与FISTA]]：软阈值算子的来源。
### 下游延伸
- [[最优化方法-增广拉格朗日与ADMM]]：ADMM 在分布式系统中的扩展（每个机器算本地 loss，全局变量强制共识）。
- [[最优化方法-增广拉格朗日与ADMM]]：如何自动调整 $\rho$ 参数。
### 横向关联
- [[最优化方法-近端梯度与FISTA]]：另一种用于 L1 正则化的高效一阶算法。ADMM 和 FISTA 都是求解稀疏问题的利器。

---
## 10. 闭卷复现任务
1. 写出含有两个变量的凸优化问题的 ADMM 标准型，并写出增广拉格朗日函数 $L_\rho$。
2. 推导 Scaled Form，证明 $\frac{\rho}{2}\|Ax+Bz-c\|_2^2 + y^T(Ax+Bz-c)$ 可以被配方为 $\frac{\rho}{2}\|Ax+Bz-c+u\|_2^2 - \frac{\rho}{2}\|u\|_2^2$。
3. 从头默写 LASSO 问题的三个 ADMM 更新公式。

---
## 11. 自测题：5 道
> [!question]- 题目 1：在 ADMM 的 $y$（乘子）更新步中，为什么步长刚好是 $\rho$？
> **答案**：这一步来源于 ALM 的最优性条件。在极小化 $L_\rho(x,z,y^k)$ 时，对 $x$ 的导数为 $\nabla f(x^{k+1}) + A^T y^k + \rho A^T (Ax^{k+1} + Bz^{k+1} - c) = 0$。如果我们定义 $y^{k+1} = y^k + \rho(Ax^{k+1} + Bz^{k+1} - c)$，那么上述等式恰好变成了 $\nabla f(x^{k+1}) + A^T y^{k+1} = 0$，这恰好逼近原问题的拉格朗日稳态条件！这叫作拉格朗日乘子的优雅更新。

> [!question]- 题目 2：什么是 ADMM 中的原始残差 (Primal Residual) 和对偶残差 (Dual Residual)？
> **答案**：原始残差 $r^{k+1} = Ax^{k+1} + Bz^{k+1} - c$，它衡量了解违反约束的程度。对偶残差 $s^{k+1} = \rho A^T B (z^{k+1} - z^k)$，它衡量了由交替极小化带来的次优性偏离。ADMM 的收敛条件就是这两者同时趋于 0。

> [!question]- 题目 3：推导 Scaled Form 时的配方法详细步骤。
> **答案**：
$y^T r + \frac{\rho}{2}\|r\|^2$。令 $y = \rho u$，则原式为 $\rho u^T r + \frac{\rho}{2}\|r\|^2 = \frac{\rho}{2} (2 u^T r + \|r\|^2)$。
补充平方项 $\|u\|^2$，得 $\frac{\rho}{2} (\|r\|^2 + 2u^T r + \|u\|^2) - \frac{\rho}{2}\|u\|^2 = \frac{\rho}{2}\|r + u\|^2 - \frac{\rho}{2}\|u\|^2$。
即 $\frac{\rho}{2}\|Ax + Bz - c + u\|^2 - \frac{\rho}{2}\|u\|^2$。

> [!question]- 题目 4：在 Consensus ADMM（共识优化）中，约束的形式是怎样的？
> **答案**：目标函数是 $\min \sum_{i=1}^N f_i(x_i)$。由于我们要让所有本地变量 $x_i$ 都等于一个全局共享变量 $z$，所以约束为 $x_i - z = 0, \forall i$。这就完美的符合了 $Ax+Bz=0$ 的形式，其中 $x$ 是所有的本地变量拼接。

> [!question]- 题目 5：ADMM 与 Proximal Gradient Descent (PGD) 的区别？
> **答案**：对于 $f(x) + g(x)$ 问题（$f$ 光滑，$g$ 非光滑）：
PGD 需要 $f$ 在每一步可微且求梯度，然后对 $g$ 使用近端算子。
ADMM 是将其写为 $f(x) + g(z), x=z$。$x$-update 这一步是解一个含有 $f$ 的近端问题（或二次规划），而不是简单地求梯度（除非进一步做线性化，即 Linearized ADMM）。ADMM 的适用面比 PGD 更广，因为即使 $f$ 也不可微，只要 $f$ 和 $g$ 各自的近端算子容易求，ADMM 就可以工作。

---
## 12. 我的主动回忆区
### 我的闭卷复述
- (留白)
### 我的推导复现
- (留白)
### 我的错误与卡点
- (留白)
### 下次复习日期
- 2026-08-10

---
## 13. 给 Obsidian 的归档建议
- 归档路径：`02-Knowledge/🧠 学习系统/07-最优化方法/增广拉格朗日与ADMM.md`
- 建议将 “软阈值算子推导” 在《近端梯度》卡片中做详细展开，并通过双链关联到本卡片。

## ⚠️ 常见陷阱与避坑指南

> [!CAUTION]
> 1. **ADMM 惩罚参数 $
ho$ 的选取**：$
ho$ 太小会导致约束收敛极其缓慢，$
ho$ 太大则会压制目标函数的优化。推荐引入自适应 $
ho$ 更新策略（残差平衡法 Residual Balancing）：当原残差 $\|r_k\|_2 > 10 \|s_k\|_2$ 时调大 $
ho$，当对偶残差 $\|s_k\|_2 > 10 \|r_k\|_2$ 时调小 $
ho$。
> 2. **ADMM $x$-update 与 $y$-update 的顺序**：ADMM 是 Gauss-Seidel 类型的交替更新，必须先更新 $x_{k+1}$，再将最新的 $x_{k+1}$ 带入 $y_{k+1}$ 的求解中，最后更新对偶乘子 $u_{k+1}$。不可以并行同步更新 $x, y$（那属于 Jacobi 类型，易发散）。

## 🃏 Anki 卡片

Q: 交替方向乘子法 (ADMM) 的标准问题形式及其三大迭代更新步是什么？
A: 问题形式：$\min_{x, y} f(x) + g(y), \quad \text{s.t.} \quad A x + B y = c$。
更新步：
1) $x_{k+1} = \grg\min_x \left( f(x) + \frac{
ho}{2} \|A x + B y_k - c + u_k\|_2^2 
ight)$
2) $y_{k+1} = \grg\min_y \left( g(y) + \frac{
ho}{2} \|A x_{k+1} + B y - c + u_k\|_2^2 
ight)$
3) $u_{k+1} = u_k + A x_{k+1} + B y_{k+1} - c$
<!-- id: opt-admm-01 -->

Q: ADMM 中的原始残差 (Primal Residual) 与对偶残差 (Dual Residual) 的定义是什么？
A: 原始残差 $r_{k+1} = A x_{k+1} + B y_{k+1} - c$（量度约束违反程度）；
对偶残差 $s_{k+1} = 
ho A^T B (y_{k+1} - y_k)$（量度对偶平稳性误差）。当 $\|r_k\|_2 \le \epsilon_{\text{pri}}$ 且 $\|s_k\|_2 \le \epsilon_{\text{dual}}$ 时算法收敛。
<!-- id: opt-admm-02 -->


---

Q: ADMM (交替方向乘子法) 相比普通拉格朗日乘子法最大的结构优势是什么？
A: 将原变量拆分为 $x$ 与 $z$ 两个独立块，使复杂的耦合约束目标函数分解为可并行/交替求解的独立子问题。
<!-- id: opt-admm-03 -->

## 学完后可以完成

### 通过标准
- [ ] 能够完成核心推导与验证

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```


- [[07-最优化方法-大作业-大规模优化与ADMM并行求解器]]

