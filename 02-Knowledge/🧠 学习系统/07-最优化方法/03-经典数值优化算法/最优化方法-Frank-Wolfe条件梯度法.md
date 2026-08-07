---
type: study
topic: "Frank-Wolfe条件梯度法"
course: "07-最优化方法"
created: 2026-08-06
status: completed
flow: knowledge
kind: concept
stage_moc: "[[🧭 阶段3-经典数值优化算法]]"
upstream:
  - "[[最优化方法-约束优化-SQP与投影梯度法]]"
  - "[[最优化方法-凸集与凸函数]]"
---
# 最优化方法-Frank-Wolfe条件梯度法


## §02 算法步骤与收敛性分析

```text
算法：Frank-Wolfe (条件梯度法)
初始化：选择 x_0 ∈ C

对于 k = 0, 1, 2, ...
1. 计算梯度：g_k = ∇f(x_k)
2. 调用 LMO：s_k = argmin_{s ∈ C} <g_k, s>
3. 评价对偶间隙 (Duality Gap)：g_k = <g_k, x_k - s_k>  (自检停止条件)
4. 步长选择：γ_k = 2 / (k + 2)  或进行线搜索 γ_k = argmin_{γ ∈ [0,1]} f(x_k + γ(s_k - x_k))
5. 凸组合更新：x_{k+1} = x_k + γ_k (s_k - x_k)
```

对于具有曲率常数（Curvature Constant） $C_f$ 的光滑凸函数，Frank-Wolfe 算法保证收敛界：
\[
f(x_k) - f(x^*) \le \frac{2 C_f}{k+2} = \mathcal{O}\left(\frac{1}{k}\right)
\]

---
## §03 Python 代码实现 (Frank-Wolfe L1-范数球与低秩矩阵)

```python
import numpy as np

def frank_wolfe_l1_ball(f, grad_f, radius, dim, max_iters=200):
    """Frank-Wolfe 求解 L1 范数球约束问题: min_{||x||_1 <= radius} f(x)"""
    x = np.zeros(dim)
    history = []
    
    for k in range(max_iters):
        g = grad_f(x)
        
        # 1. LMO 在 L1 范数球上找最速极小点：对应梯度的极值方向 (1-sparse 向量)
        i_max = np.argmax(np.abs(g))
        s = np.zeros(dim)
        s[i_max] = -radius * np.sign(g[i_max])
        
        # 2. 对偶间隙 (Frank-Wolfe Duality Gap)
        duality_gap = np.dot(g, x - s)
        history.append((k, f(x), duality_gap))
        
        if duality_gap < 1e-5:
            break
            
        # 3. 默认衰减步长
        gamma = 2.0 / (k + 2.0)
        
        # 4. 凸组合更新
        x = (1.0 - gamma) * x + gamma * s
        
    return x, history
```

---
## 🎯 知识自测与主动回忆

> [!question]- 1. Frank-Wolfe 算法相比投影梯度法（PGD）的核心优势是什么？
> **答案**：Frank-Wolfe 算法完全免去（Projection-Free）了求二次投影算子的过程，将可行域上的子问题简化为求线性极小化预言机（LMO）。当可行域为核范数球或 $L_1$ 范数球时，LMO 仅需计算最大特征对或最大梯度分量，比投影（需全 SVD 或复杂排序）计算开销低数个数量级。

> [!question]- 2. 为什么 Frank-Wolfe 算法的迭代点 $x_k$ 天然具备稀疏性或低秩性？
> **答案**：算法每一步选择约束集 $\mathcal{C}$ 的一个极端顶点（Extreme Point / Atom） $s_k$，并通过 $x_{k+1} = (1-\gamma_k)x_k + \gamma_k s_k$ 进行凸组合。在第 $k$ 步，$x_k$ 至多是 $k+1$ 个原子顶点的线性组合。因此在 $L_1$ 范数球上 $x_k$ 极为稀疏，在核范数球上 $x_k$ 的秩至多为 $k$。

> [!question]- 3. 什么是 Frank-Wolfe 对偶间隙（Duality Gap）？它如何用作停止条件？
> **答案**：对偶间隙定义为 $G(x_k) = \max_{s \in \mathcal{C}} \langle \nabla f(x_k), x_k - s \rangle = \langle \nabla f(x_k), x_k - s_k \rangle$。由凸函数性质，显然有 $f(x_k) - f(x^*) \le G(x_k)$。因此 $G(x_k)$ 提供了原问题残差的严格上界，可以直接作为自检测与算法停止准则。

> [!question]- 4. Frank-Wolfe 算法在接近最优解时可能出现什么收敛瓶颈？如何改进？
> **答案**：标准 FW 在可行域边界处容易出现沿边界顶点的“之”字形震荡（Zig-zagging），导致收敛变慢。改进方案包括 Away-step Frank-Wolfe (AFW)、Pairwise Frank-Wolfe (PFW) 或 Fully-Corrective FW，允许从已有原子集中剔除过期顶点。

> [!question]- 5. 为什么 Frank-Wolfe 算法不适合无约束最优化问题？
> **答案**：如果可行域 $\mathcal{C} = \mathbb{R}^d$ 无界，线性极小化预言机 $\min_{s \in \mathbb{R}^d} \langle g, s \rangle$ 的目标函数无下界，导致 LMO 输出 $-\infty$。因此 Frank-Wolfe 必须要求可行域为有界的紧凸集（Compact Convex Set）。

---
## 🃏 Anki 卡片

Q: Frank-Wolfe 算法的核心更新公式是什么？如何保证可行性？
A: 找到 LMO 点 $s_k = \arg\min_{s \in \mathcal{C}} \langle \nabla f(x_k), s \rangle$，按凸组合更新 $x_{k+1} = (1-\gamma_k) x_k + \gamma_k s_k$（$\gamma_k = \frac{2}{k+2}$）。因为 $x_k, s_k \in \mathcal{C}$ 且为凸组合，故 $x_{k+1} \in \mathcal{C}$ 自动成立，完全免投影。
<!-- id: opt-fw-01 -->

---
Q: 写出 Frank-Wolfe 对偶间隙（Duality Gap）公式及其作用。
A: $G(x_k) = \langle \nabla f(x_k), x_k - s_k \rangle$。它是当前目标残差 $f(x_k) - f(x^*)$ 的上界，在算法运行中无需知道 $f(x^*)$ 即可直接作为准确的停止准则。
<!-- id: opt-fw-02 -->

---
Q: 为什么在 $L_1$ 范数球约束下，Frank-Wolfe 的 LMO 极易求解？
A: 在 $L_1$ 范数球上极小化线性函数，其解只需找到梯度绝对值最大的分量 $i^* = \arg\max |g_i|$，令 $s_{i^*} = -R \text{sign}(g_{i^*})$，其余维为 0。计算开销仅为 $\mathcal{O}(d)$，比投影算法快数十倍。
<!-- id: opt-fw-03 -->

---
## 学完后可以完成


```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
