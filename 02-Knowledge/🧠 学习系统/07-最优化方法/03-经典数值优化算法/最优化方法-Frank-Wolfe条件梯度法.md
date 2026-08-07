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

## §01 为什么学？它解决什么问题？

**动机**：前面学过的投影梯度法（PGD，见 [[最优化方法-约束优化-SQP与投影梯度法]]）每步都要把迭代点投影回可行域 $\mathcal{C}$。当 $\mathcal{C}$ 是简单集合（盒子、球、单纯形）时投影很容易；但当 $\mathcal{C}$ 是**核范数球、L1 范数球、多面体顶点集合**等结构复杂集合时，投影算子本身就是一个昂贵的子问题（如核范数投影需要完整 SVD）。

**Frank-Wolfe（条件梯度法）** 的核心洞察：与其每步做"投影"这种非线性操作，不如把子问题换成**线性极小化预言机（Linear Minimization Oracle, LMO）**——在可行域上极小化一个线性函数 $\min_{s \in \mathcal{C}} \langle g, s \rangle$。对很多复杂约束，LMO 有闭式解（L1 球上就是找梯度最大分量，核范数球上是最大奇异向量），比投影便宜几个数量级。

**学完能做什么**：能说清 FW 与 PGD 的本质区别（LMO vs 投影）；能写出 L1 球/核范数球上的 LMO；能用对偶间隙做免 $f(x^*)$ 的停止判据；能解释为什么 FW 迭代点天然稀疏/低秩。

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
## §04 收敛性直觉与推导主线

**为什么收敛率是 $\mathcal{O}(1/k)$？** 设 $f$ 是 $C_f$-光滑凸函数（曲率常数 $C_f$ 上界其沿任意方向二阶变化），由光滑性不等式：

$$ f(y) \le f(x) + \langle \nabla f(x), y - x \rangle + \frac{C_f}{2} \|y - x\|^2 $$

代入 $y = x_{k+1} = x_k + \gamma_k(s_k - x_k)$，利用 LMO 最优性 $\langle \nabla f(x_k), s_k \rangle \le \langle \nabla f(x_k), x^* \rangle$ 和凸性 $\langle \nabla f(x_k), x_k - x^* \rangle \ge f(x_k) - f(x^*)$，得到递推：

$$ f(x_{k+1}) - f(x^*) \le (1 - \gamma_k)\left[f(x_k) - f(x^*)\right] + \frac{\gamma_k^2 C_f}{2} D^2 $$

取 $\gamma_k = \frac{2}{k+2}$ 并归纳可得 $f(x_k) - f(x^*) \le \frac{2 C_f D^2}{k+2} = \mathcal{O}(1/k)$。这个推导的每一步都是"光滑性 + LMO 最优性 + 凸性"三件套，理解它就能自己推出各类 FW 变体的界。

**为什么会产生 Zig-zag 震荡**：当 $x_k$ 靠近边界时，梯度方向几乎垂直于边界，LMO 不断在相邻两个顶点之间切换（"之"字形），步长 $\gamma_k$ 又很小，收敛变慢。Away-step FW 通过维护"离开方向"加速。

---
## §05 例子：手算 LMO 与一步更新

**问题**：$f(x) = (x_1 - 2)^2 + 3(x_2 - 1)^2$，可行域 $\mathcal{C} = \{x : |x_1| + |x_2| \le 1\}$（L1 球，半径 1），起点 $x_0 = (0, 0)$。

1. **梯度**：$\nabla f(x_0) = (2(x_1 - 2), 6(x_2 - 1)) = (-4, -6)$；
2. **LMO**：在 L1 球上极小化 $\langle g, s \rangle = -4s_1 - 6s_2$，取梯度绝对值最大分量 $i = 2$（$|g_2| = 6$），令 $s = (0, -\text{sign}(g_2) \times 1) = (0, -1)$；
3. **步长**：$\gamma_0 = 2/(0+2) = 1$；
4. **更新**：$x_1 = x_0 + 1 \times (s - x_0) = (0, -1)$；
5. **对偶间隙**：$G(x_0) = \langle (-4,-6), (0,0) - (0,-1) \rangle = 6$，说明 $f(x_0) - f(x^*) \le 6$（实际 $f(x_0) = 5$，$f^* = f(2,1) = 0$ 但不在可行域内，真实最优在边界上）。

可见 FW 一步就把点从原点拉到了可行域边界顶点，且全程不投影。

---
## §06 常见误区与易混概念

- **误区 1：FW 是投影梯度法的"改进版"**
  不是。两者是不同路线：PGD 每步"梯度步 + 投影"（保留流形外信息），FW 每步"LMO + 凸组合"（始终在流形内）。FW 的优势在 LMO 便宜的场景，不是普适更优。

- **误区 2：对偶间隙需要知道最优值 $f(x^*)$ 才能用**
  恰恰相反，$G(x_k) = \langle \nabla f(x_k), x_k - s_k \rangle$ 只依赖当前点与 LMO 解，**不需要** $f(x^*)$，这是它能做停止准则的原因。

- **误区 3：FW 适合无约束问题**
  无界可行域上 LMO 无解（线性函数在无界集上无下界），FW 只适用于**有界紧凸集**约束问题。

### 概念对比表

| 方法 | 每步子问题 | 约束类型 | 迭代点性质 | 收敛率 |
| :--- | :--- | :--- | :--- | :--- |
| 投影梯度 (PGD) | 二次投影 | 投影便宜 | 投影后可行 | 线性（强凸） |
| Frank-Wolfe | 线性 LMO | LMO 便宜 | 顶点稀疏/低秩 | $\mathcal{O}(1/k)$ |
| Away-step FW | 双 LMO | 同上 | 更少震荡 | 线性（部分情形） |

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
