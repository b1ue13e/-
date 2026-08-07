---
type: study
topic: "拟牛顿法L-BFGS"
course: "07-最优化方法"
created: 2026-08-06
status: completed
flow: knowledge
kind: concept
stage_moc: "[[🧭 阶段3-经典数值优化算法]]"
upstream:
  - "[[最优化方法-拟牛顿法BFGS]]"
  - "[[最优化方法-牛顿法]]"
---
# 最优化方法-拟牛顿法L-BFGS


## §02 双循环递归算法 (Two-Loop Recursion) 详细推导

设初始基础矩阵为标量缩放矩阵 $H_k^{(0)} = \gamma_k I$，其中最佳缩放系数为：
\[
\gamma_k = \frac{s_{k-1}^\top y_{k-1}}{y_{k-1}^\top y_{k-1}}
\]

将 $H_k$ 展开为最近 $m$ 次更新的乘积形式后，利用递归结构可得出**双循环算法**：

```text
算法：L-BFGS Two-Loop Recursion 计算 search direction p_k = -H_k g_k
输入：当前梯度 g_k = ∇f(x_k)，历史向量对 {s_i, y_i}_{i=k-m}^{k-1}，ρ_i = 1 / (y_iᵀ s_i)

1. [第一循环：后向循环 (Backward Pass)]
   q = g_k
   For i = k-1 down to k-m:
       α_i = ρ_i * (s_iᵀ * q)
       q = q - α_i * y_i

2. [基础矩阵缩放 (Base Matrix Scaling)]
   γ_k = (s_{k-1}ᵀ y_{k-1}) / (y_{k-1}ᵀ y_{k-1})
   r = γ_k * q

3. [第二循环：前向循环 (Forward Pass)]
   For i = k-m to k-1:
       β = ρ_i * (y_iᵀ * r)
       r = r + s_i * (α_i - β)

输出：搜索方向 p_k = -r
```

---
## §03 Python 代码实现 (L-BFGS 双循环求解器)

```python
import numpy as np

def lbfgs_two_loop(g_k, s_hist, y_hist, m):
    """L-BFGS 双循环递归计算 -H_k * g_k"""
    k = len(s_hist)
    if k == 0:
        return -g_k
    
    q = g_k.copy()
    alphas = []
    
    # 确定历史窗口 [start_idx, k-1]
    start_idx = max(0, k - m)
    
    # 第一循环：后向 pass
    for i in range(k - 1, start_idx - 1, -1):
        s_i = s_hist[i]
        y_i = y_hist[i]
        rho_i = 1.0 / np.dot(y_i, s_i)
        alpha_i = rho_i * np.dot(s_i, q)
        alphas.append(alpha_i)
        q = q - alpha_i * y_i
        
    alphas.reverse() # 倒置以匹配正向索引
    
    # 基础矩阵缩放 γ_k
    gamma_k = np.dot(s_hist[-1], y_hist[-1]) / np.dot(y_hist[-1], y_hist[-1])
    r = gamma_k * q
    
    # 第二循环：前向 pass
    for idx, i in enumerate(range(start_idx, k)):
        s_i = s_hist[i]
        y_i = y_hist[i]
        rho_i = 1.0 / np.dot(y_i, s_i)
        alpha_i = alphas[idx]
        beta = rho_i * np.dot(y_i, r)
        r = r + s_i * (alpha_i - beta)
        
    return -r

def lbfgs_optimizer(f, grad_f, x0, m=5, max_iters=100, tol=1e-5):
    """L-BFGS 完整优化求解器"""
    x = np.array(x0, dtype=float)
    s_hist, y_hist = [], []
    history = []
    
    for k in range(max_iters):
        g = grad_f(x)
        g_norm = np.linalg.norm(g)
        history.append((k, f(x), g_norm))
        if g_norm < tol:
            break
            
        p = lbfgs_two_loop(g, s_hist, y_hist, m)
        
        # 回溯线搜索 (Armijo)
        alpha = 1.0
        c1 = 1e-4
        while f(x + alpha * p) > f(x) + c1 * alpha * np.dot(g, p):
            alpha *= 0.5
            if alpha < 1e-12:
                break
                
        x_next = x + alpha * p
        g_next = grad_f(x_next)
        
        s_k = x_next - x
        y_k = g_next - g
        
        if np.dot(y_k, s_k) > 1e-10:
            s_hist.append(s_k)
            y_hist.append(y_k)
            if len(s_hist) > m:
                s_hist.pop(0)
                y_hist.pop(0)
                
        x = x_next
        
    return x, history
```

---
## 🎯 知识自测与主动回忆

> [!question]- 1. L-BFGS 的空间和时间复杂度与标准 BFGS 有何根本区别？
> **答案**：标准 BFGS 显式保存 $d \times d$ 的海森逆矩阵 $H_k$，内存开销为 $\mathcal{O}(d^2)$，矩阵乘法运算复杂度为 $\mathcal{O}(d^2)$；L-BFGS 仅保存最近 $m$ 组高维向量，内存开销降至 $\mathcal{O}(m d)$，双循环递归点积计算开销降至 $\mathcal{O}(m d)$（$m \ll d$）。

> [!question]- 2. L-BFGS 算法中基础缩放因子 $\gamma_k = \frac{s_{k-1}^\top y_{k-1}}{y_{k-1}^\top y_{k-1}}$ 的物理意义是什么？
> **答案**：$\gamma_k$ 估计了海森逆矩阵沿最新搜索方向的特征值量级，将基础矩阵设为 $H_k^{(0)} = \gamma_k I$ 能在迭代初期极大改善拟牛顿方向的条件数，使线搜索步长 $\alpha=1$ 更容易被满足。

> [!question]- 3. 为什么在 L-BFGS 的双循环递归中，后向 Pass 计算的是 $\alpha_i$，前向 Pass 计算的是 $\beta$？
> **答案**：这是因为展开展开后的海森更新公式为对称夹心结构 $H_k = V_{k-1}^\top \dots V_{k-m}^\top H_k^{(0)} V_{k-m} \dots V_{k-1} + \dots$。右侧的 $V_{i}$ 作用于梯度 $g_k$ 需后向倒序执行；经基础矩阵 $\gamma_k I$ 缩放后，左侧的 $V_i^\top$ 需正向顺序作用回向量上。

> [!question]- 4. 如果在大规模非凸优化（如深度学习）中直接应用 L-BFGS，会遇到什么主要挑战？
> **答案**：1) 非凸场景下曲率条件 $y_k^\top s_k > 0$ 可能失效导致正定性丧失；2) 深度学习采用 Mini-batch 随机梯度，梯度的随机噪声会严重破坏割线方程 $y_k$ 的准确性。因此 DL 领域通常首选 Adam/SGD 或 L-BFGS 的随机平滑变体。

> [!question]- 5. L-BFGS 中的历史存储窗口大小 $m$ 通常如何选择？增大 $m$ 一定会改善性能吗？
> **答案**：工程上 $m$ 通常取 3 至 20 之间（如 5 或 10）。增大 $m$ 能够提供更精确的海森曲率估计，但也会线性增加单步点积计算量（$\mathcal{O}(m d)$）与内存开销；当 $m$ 超过一定阈值后，收敛收益边际递减，因此较小且固定的 $m$ 即可达到最优效率。

---
## 🃏 Anki 卡片

Q: L-BFGS 如何将拟牛顿法的存储和计算开销从 $\mathcal{O}(d^2)$ 降低到 $\mathcal{O}(m d)$？
A: 放弃显式保存 $d \times d$ 的海森逆矩阵 $H_k$，仅保留最近 $m$ 步的位移向量对 $\{s_i, y_i\}_{i=k-m}^{k-1}$，利用双循环递归算法（Two-Loop Recursion）直接计算拟牛顿方向 $p_k = -H_k g_k$。
<!-- id: opt-lbfgs-01 -->

---
Q: 写出 L-BFGS 双循环递归中基础标量缩放 $\gamma_k$ 的计算公式及作用。
A: $\gamma_k = \frac{s_{k-1}^\top y_{k-1}}{y_{k-1}^\top y_{k-1}}$。作用是用最新曲率信息缩放初始海森逆矩阵 $H_k^{(0)} = \gamma_k I$，大幅提升搜索方向条件数，使得默认步长 $\alpha=1$ 极易通过 Armijo 线搜索。
<!-- id: opt-lbfgs-02 -->

---
Q: L-BFGS 割线方程正定性成立的前置曲率条件是什么？若不满足如何处理？
A: 曲率条件为 $y_k^\top s_k > 0$。若由于非凸或数值误差导致 $y_k^\top s_k \le 10^{-10}$，则放弃保存当前的向量对 $(s_k, y_k)$（Skip Update），以保证矩阵正定性不被破坏。
<!-- id: opt-lbfgs-03 -->

---
## 学完后可以完成


```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
