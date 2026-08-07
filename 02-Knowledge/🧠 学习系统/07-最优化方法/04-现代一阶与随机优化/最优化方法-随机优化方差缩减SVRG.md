---
type: study
topic: "随机优化方差缩减SVRG"
course: "07-最优化方法"
created: 2026-08-06
status: completed
flow: knowledge
kind: concept
stage_moc: "[[🧭 阶段4-现代一阶与随机优化]]"
upstream:
  - "[[最优化方法-SGD与随机优化]]"
  - "[[最优化方法-一阶方法收敛性分析]]"
---
# 最优化方法-随机优化方差缩减SVRG

## §01 学习引导：为什么 SGD 会震荡，SVRG 如何消除震荡？

**解决什么问题**：[[最优化方法-SGD与随机优化]] 用单样本梯度 $\nabla f_{i}(w)$ 代替全梯度 $\nabla P(w)$，每步开销降为 $\mathcal{O}(d)$，但**梯度估计的方差不随迭代趋于 0**——即使 $w_k$ 已收敛到最优解附近，随机梯度仍在波动，常数步长下只能收敛到最优值的一个邻域，线性收敛到精确解需要步长衰减到 0（此时收敛变为次线性）。

**关键思想（方差缩减）**：SVRG（Johnson & Zhang 2013）维护一个**定期更新的快照点 $\tilde{w}$**（每 $m$ 步刷新一次），并缓存其精确全梯度 $\mu = \nabla P(\tilde{w})$。随机步使用修正后的梯度：
\[
v_t = \nabla f_{i_t}(w_t) - \nabla f_{i_t}(\tilde{w}) + \mu
\]
当 $w_t \to w^*$ 且 $\tilde{w} \to w^*$ 时，前两项相互抵消，$\mathrm{Var}(v_t) \to 0$，从而**在常数步长下实现线性收敛**（对强凸光滑问题）。

**学完能做什么**：能写出 SVRG 的外循环/内循环双环流程并解释快照梯度的作用；能证明 $v_t$ 是 $\nabla P(w_t)$ 的无偏估计；能对比 SGD、SAG/SAGA 与 SVRG 的方差行为；能实现 SVRG 并在逻辑回归上验证线性收敛。

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
## §04 手算例子：方差缩减的直觉验证

**问题**：两个样本的均方误差 $f_1(w) = \frac{1}{2}(w-1)^2$，$f_2(w) = \frac{1}{2}(w+1)^2$，$P(w) = \frac{1}{2}(f_1 + f_2) = \frac{1}{2}w^2 + \frac{1}{2}$，最优解 $w^* = 0$。

**快照点** $\tilde{w} = 1$：$\mu = \nabla P(1) = 1$。

**随机步**（$w_t = 1$，采样 $i=1$）：
- 单样本梯度：$\nabla f_1(1) = 1 - 1 = 0$；
- 快照点单样本梯度：$\nabla f_1(\tilde{w}) = \nabla f_1(1) = 0$；
- SVRG 估计：$v_t = 0 - 0 + 1 = 1$；
- 对比真实梯度：$\nabla P(1) = 1$ —— 两者一致，方差为 0！

**再看**（$w_t$ 靠近最优解 $w = 0.1$，采样 $i=2$）：
- $\nabla f_2(0.1) = 0.1 + 1 = 1.1$；
- $\nabla f_2(1) = 2$；
- $v_t = 1.1 - 2 + 1 = 0.1 = \nabla P(0.1)$。

无论采哪个样本，$v_t$ 都精确等于真实全梯度——这就是方差缩减：**单样本梯度的大波动被"减去快照点处同一样本梯度"抵消**，只剩真实梯度方向。

---
## §05 收敛性直觉：为什么能线性收敛

SGD 的方差 $\mathrm{Var}(\nabla f_i(w))$ 在 $w^*$ 处不趋于 0（等于 $\mathrm{Var}(\nabla f_i(w^*))$），所以常数步长下参数在最优解附近"打转"（方差平台）。SVRG 的估计量方差满足：

$$ \mathrm{Var}(v_t) \le \mathrm{Var}(\nabla f_i(w_t)) - \mathrm{Var}(\nabla f_i(\tilde{w})) + 2L \|w_t - \tilde{w}\| \cdot \mathbb{E}\|v_t\| $$

随 $w_t, \tilde{w} \to w^*$，方差上界趋于 0。结合强凸性（$P$ 有二次下界），在常数步长 $\eta < \frac{1}{4L}$ 下可得递推 $\mathbb{E}[P(w_s) - P(w^*)] \le \rho \cdot \mathbb{E}[P(w_{s-1}) - P(w^*)]$（$\rho < 1$），即**几何线性收敛**。直观理解：方差被"消灭"后，随机算法恢复到确定性梯度下降的收敛品质，但每步成本仍是 $\mathcal{O}(d)$。

---
## §06 常见误区与易混概念

- **误区 1：SVRG 每次迭代都要算全梯度**
  全梯度 $\mu$ 只在**外循环每 $m$ 步**算一次（$\mathcal{O}(nd)$）；内循环 $m$ 步全是 $\mathcal{O}(d)$ 随机步。平均每步成本 $\approx \mathcal{O}(d)$，与 SGD 同阶。

- **误区 2：SVRG 的 $v_t$ 是有偏估计**
  $v_t$ 是**无偏**的：$\mathbb{E}_{i_t}[v_t] = \nabla P(w_t)$（见自测题 2 的证明）。它不牺牲无偏性，只压缩方差。

- **误区 3：SVRG 一定优于 SAG/SAGA**
  内存上 SVRG 更优（$\mathcal{O}(d)$ vs $\mathcal{O}(nd)$），但 SAGA 支持**单循环 + 自适应步长**、天然适合非独立同分布流式数据；SVRG 需要快照点刷新，对非平稳流（在线学习）不直接适用。

### 概念对比表

| 方法 | 梯度估计 | 方差随迭代 | 内存 | 收敛率（强凸） | 适用场景 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SGD | $\nabla f_i$ | 恒定 >0 | $\mathcal{O}(d)$ | 次线性（需衰减步长） | 大规模流式 |
| SVRG | $v_t = \nabla f_i - \nabla f_i(\tilde{w}) + \mu$ | $\to 0$ | $\mathcal{O}(d)$ | 线性 | 离线批量 |
| SAGA | $v_t = \nabla f_i - \alpha_i + \text{avg}$ | $\to 0$ | $\mathcal{O}(nd)$ | 线性 | 离线 + 流式 |

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
