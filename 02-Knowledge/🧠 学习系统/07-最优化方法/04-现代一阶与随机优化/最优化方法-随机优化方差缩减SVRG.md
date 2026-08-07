---
type: study
topic: 随机优化方差缩减SVRG
course: 07-最优化方法
created: 2026-08-06
status: completed
stage_moc: "[[🧭 阶段4-现代一阶与随机优化]]"
flow: knowledge
kind: derivation
upstream:
  - "[[最优化方法-SGD与随机优化]]"
  - "[[最优化方法-一阶方法收敛性分析]]"
tags:
  - 最优化
  - SVRG
  - 方差缩减
  - 随机梯度
  - 线性收敛
---
# 最优化方法 - 随机优化方差缩减 SVRG (Stochastic Variance Reduced Gradient)

> **核心地位**：在有限和目标函数最优化问题 $\min_{w} P(w) = \frac{1}{n} \sum_{i=1}^n f_i(w)$ 中，标准全梯度下降（GD）具有线性收敛速率 $\mathcal{O}(\rho^k)$ 但单步计算开销高达 $\mathcal{O}(n d)$；标准随机梯度下降（SGD）单步开销仅 $\mathcal{O}(d)$，但由于单样本梯度的方差瓶颈（Variance Floor），在常数步长下无法收敛到极小值，而在衰减步长下仅有次线性的慢速收敛 $\mathcal{O}(1/k)$。Roux、Johnson 与 Zhang 提出的 SVRG（随机梯度方差缩减）算法利用**控制变量法（Control Variates）**，结合快照点全梯度，实现了**单步 $\mathcal{O}(d)$ 计算开销与线性收敛速率 $\mathcal{O}(\rho^k)$ 的完美结合**。

---

## §01 算法动机：SGD 的方差瓶颈与控制变量法

设单样本随机梯度为 $\nabla f_{i_t}(w_t)$。由于 $i_t$ 是均匀随机采样的，其期望虽然是无偏估计 $\mathbb{E}[\nabla f_{i_t}(w_t)] = \nabla P(w_t)$，但其方差：
\[
\text{Var}(\nabla f_{i_t}(w_t)) = \mathbb{E}[\|\nabla f_{i_t}(w_t) - \nabla P(w_t)\|^2] \ne 0 \quad (\text{即使 } w_t \to w^*)
\]
由于方差在极小值点 $w^*$ 处依然大于 0，使用常数步长 $\eta$ 的 SGD 会在 $w^*$ 附近形成一个不可消除的“方差平台（Variance Floor）”，陷入随机震荡。

SVRG 引入**快照点 $\tilde{w}$（Snapshot Point）**与全梯度 $\mu = \nabla P(\tilde{w})$，构造全新的梯度估计量 $v_t$：
\[
v_t = \nabla f_{i_t}(w_t) - \nabla f_{i_t}(\tilde{w}) + \mu
\]

### 估计量无偏性与方差缩减特性：
1. **无偏性**：$\mathbb{E}[v_t] = \nabla P(w_t) - \nabla P(\tilde{w}) + \mu = \nabla P(w_t)$；
2. **方差趋于 0**：当迭代点 $w_t \to w^*$ 且快照点 $\tilde{w} \to w^*$ 时，$\nabla f_{i_t}(w_t) - \nabla f_{i_t}(\tilde{w}) \to 0$，使得 $\text{Var}(v_t) \to 0$！

---

## §02 SVRG 算法流程

```text
算法：SVRG (Stochastic Variance Reduced Gradient)
输入：初始参数 w_0，外循环次数 S，内循环步数 m，步长 η

对于 s = 1, 2, ..., S:
1. 记快照点 w~ = w_{s-1}
2. 计算快照点处的精确全梯度：
   μ = ∇P(w~) = (1 / n) ∑_{i=1}^n ∇f_i(w~)   (计算开销 O(n d))
3. 设内循环初始点 w_0^{(s)} = w~
4. For t = 0, 1, ..., m-1:
       随机采样 i_t ∈ {1, 2, ..., n}
       计算方差缩减梯度估计量：
       v_t = ∇f_{i_t}(w_t^{(s)}) - ∇f_{i_t}(w~) + μ   (计算开销 O(d))
       更新参数：w_{t+1}^{(s)} = w_t^{(s)} - η v_t
5. 选择新快照点：w_s = w_m^{(s)} (或内循环点的随机平均)
```

---

## §03 Python 代码实现 (SVRG Logistic Regression)

```python
import numpy as np

def svrg_logistic_regression(X, y, lmbda=0.01, m=100, eta=0.05, max_epochs=20):
    """SVRG 求解 L2 正则化逻辑回归"""
    N, d = X.shape
    w = np.zeros(d)
    w_hist = [w.copy()]
    
    for epoch in range(max_epochs):
        # 1. 外循环：计算快照点全梯度 μ
        w_snapshot = w.copy()
        z = X @ w_snapshot
        p = 1.0 / (1.0 + np.exp(-z))
        full_grad = (1.0 / N) * X.T @ (p - y) + lmbda * w_snapshot
        
        # 2. 内循环：m 步方差缩减随机更新
        for t in range(m):
            i = np.random.randint(0, N)
            xi, yi = X[i], y[i]
            
            p_t = 1.0 / (1.0 + np.exp(xi @ w))
            grad_t = (p_t - yi) * xi + lmbda * w
            
            p_snap = 1.0 / (1.0 + np.exp(xi @ w_snapshot))
            grad_snap = (p_snap - yi) * xi + lmbda * w_snapshot
            
            v_t = grad_t - grad_snap + full_grad
            w = w - eta * v_t
            
        w_hist.append(w.copy())
        
    return np.array(w_hist)
```

---

## 🎯 知识自测与主动回忆

> [!question]- 1. 为什么标准 SGD 在常数步长下无法精确收敛到极小点，而 SVRG 可以？
> **答案**：标准 SGD 的单样本梯度方差在极小点 $w^*$ 处依然大于 0，常数步长会导致参数在 $w^*$ 附近形成方差平台而持续震荡；SVRG 引入构造量 $v_t = \nabla f_{i_t}(w_t) - \nabla f_{i_t}(\tilde{w}) + \mu$，当 $w_t \to w^*$ 且快照点 $\tilde{w} \to w^*$ 时，$\nabla f_{i_t}(w_t) - \nabla f_{i_t}(\tilde{w}) \to 0$，使得梯度估计量方差自动收敛至 0，从而能在常数步长下实现精确收敛。

> [!question]- 2. SVRG 梯度的构造量 $v_t = \nabla f_{i_t}(w_t) - \nabla f_{i_t}(\tilde{w}) + \mu$ 是否为无偏估计？给出证明。
> **答案**：是的。计算条件期望：$\mathbb{E}_{i_t}[v_t] = \mathbb{E}_{i_t}[\nabla f_{i_t}(w_t)] - \mathbb{E}_{i_t}[\nabla f_{i_t}(\tilde{w})] + \mu = \nabla P(w_t) - \nabla P(\tilde{w}) + \nabla P(\tilde{w}) = \nabla P(w_t)$。因此 $v_t$ 是精确全梯度 $\nabla P(w_t)$ 的无偏估计。

> [!question]- 3. SVRG 的内循环步数 $m$ 通常如何选择？为什么选择 $m = \mathcal{O}(n)$？
> **答案**：内循环步数 $m$ 通常取为样本量 $n$ 的同数量级（如 $m \approx 2n$）。因为外循环计算一次全梯度开销为 $\mathcal{O}(n d)$，平摊到内循环 $m$ 次随机步中，平均每步开销仍维持在 $\mathcal{O}(d)$ 级别。

> [!question]- 4. SVRG 相比 SAG/SAGA 算法在内存开销上有何优势？
> **答案**：SAG 和 SAGA 需要保存并实时更新全量 $n$ 个历史梯度向量，内存开销为 $\mathcal{O}(n d)$，在海量数据大维度场景下难以承受；而 SVRG 仅保存一个快照点向量 $\tilde{w}$ 和全梯度 $\mu$，内存开销仅为 $\mathcal{O}(d)$。

> [!question]- 5. 强凸且 $L$-光滑条件下 SVRG 的收敛速率是多少？
> **答案**：SVRG 具备线性收敛速率 $\mathbb{E}[P(w_s) - P(w^*)] \le \rho^s (P(w_0) - P(w^*))$（其中衰减因子 $\rho < 1$），在固定常数步长下呈几何/指数级快速收敛。

---

## 🃏 Anki 卡片

Q: 写出 SVRG 算法中方差缩减梯度估计量 $v_t$ 的定义公式。
A: $v_t = \nabla f_{i_t}(w_t) - \nabla f_{i_t}(\tilde{w}) + \mu$ （其中 $\tilde{w}$ 为快照点，$\mu = \nabla P(\tilde{w})$ 为快照点全梯度）。
<!-- id: opt-svrg-01 -->

---

Q: 为什么 SVRG 的梯度估计量方差在趋近极小点时会收敛至 0？
A: 当 $w_t, \tilde{w} \to w^*$ 时，单样本梯度差 $\nabla f_{i_t}(w_t) - \nabla f_{i_t}(\tilde{w}) \to 0$，而全梯度 $\mu = \nabla P(\tilde{w}) \to 0$，导致 $\text{Var}(v_t) \to 0$。
<!-- id: opt-svrg-02 -->

---

Q: 相比 SAG/SAGA 算法，SVRG 在内存占用上的最大优势是什么？
A: SAG/SAGA 必须存储 $n$ 个历史梯度（内存 $\mathcal{O}(n d)$），而 SVRG 只需要存储 1 个快照点和全梯度（内存 $\mathcal{O}(d)$）。
<!-- id: opt-svrg-03 -->

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
