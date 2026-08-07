---
type: study
topic: Nesterov加速梯度法
course: 07-最优化方法
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段4-现代一阶与随机优化]]"
flow: knowledge
kind: derivation
upstream:
  - "[[最优化方法-动量法与重球法]]"
  - "[[最优化方法-一阶方法收敛性分析]]"
tags:
  - 最优化
  - Nesterov加速
  - NAG
  - 估计序列
  - 凸优化理论下界
---
# 最优化方法 - Nesterov 加速梯度法 (NAG)

> **核心地位**：在光滑凸优化领域，标准梯度下降（GD）的收敛动量上限为 $\mathcal{O}(1/k)$。Yurii Nesterov 于 1983 年提出的 Nesterov 加速梯度法（Nesterov Accelerated Gradient, NAG）打破了这一传统瓶颈，利用“前瞻动量（Look-ahead Momentum）”与“估计序列（Estimating Sequences）”技术，将一阶方法的收敛速率推提升至 **$\mathcal{O}(1/k^2)$**，达到了黑盒一阶光滑凸优化的**理论下界（Optimal Lower Bound）**，被誉为现代一阶优化理论最重要的突破之一。

---

## §01 算法对比：重球法 vs Nesterov 动量

在 Polyak 重球法（Heavy-Ball Method）中，动量更新基于当前点 $x_k$ 计算梯度：
- **Polyak 重球法**：
  \[
  y_k = x_k + \beta_k (x_k - x_{k-1}), \quad x_{k+1} = y_k - \alpha \nabla f(x_k)
  \]
- **Nesterov 加速梯度法 (NAG)**：
  NAG 提出先沿动量方向进行“前瞻预判”，在探点 $y_k$ 处计算梯度：
  \[
  y_k = x_k + \beta_k (x_k - x_{k-1}), \quad x_{k+1} = y_k - \alpha \nabla f(y_k)
  \]

```text
几何直觉对比：
Polyak 重球：  x_k  ----动量β---->  y_k
               |
               └----梯度∇f(x_k)----> x_{k+1}  (冲过头风险大)

Nesterov NAG： x_k  ----动量β---->  y_k  ----前瞻梯度∇f(y_k)----> x_{k+1}
                                         (探点处修正，具备阻尼机制)
```

---

## §02 理论证明概要：从 $\mathcal{O}(1/k)$ 到 $\mathcal{O}(1/k^2)$

对于 $L$-光滑的 $F$-凸函数 $f(x)$，设定步长 $\alpha = 1/L$，动量系数随迭代次数动态更新：
\[
\lambda_0 = 0, \quad \lambda_{k+1} = \frac{1 + \sqrt{1 + 4\lambda_k^2}}{2}, \quad \beta_k = \frac{\lambda_k - 1}{\lambda_{k+1}}
\]

利用势能函数（Lyapunov Energy Function）或估计序列：
\[
\mathcal{E}_k = \lambda_k^2 (f(x_k) - f(x^*)) + \frac{L}{2} \| v_k - x^* \|^2
\]
可以严格证明势能单调递减 $\mathcal{E}_{k+1} \le \mathcal{E}_k$。由于 $\lambda_k \approx \frac{k+1}{2}$，得到残差界：
\[
f(x_k) - f(x^*) \le \frac{2 L \|x_0 - x^*\|^2}{(k+1)^2} = \mathcal{O}\left(\frac{1}{k^2}\right)
\]

---

## §03 Python 代码实现 (NAG vs 重球法)

```python
import numpy as np

def nesterov_accelerated_gradient(f, grad_f, x0, alpha=0.01, max_iters=200):
    """Nesterov 加速梯度法 (NAG)"""
    x = np.array(x0, dtype=float)
    x_prev = x.copy()
    history = [x.copy()]
    
    lambda_k = 0.0
    for k in range(1, max_iters + 1):
        lambda_next = (1.0 + np.sqrt(1.0 + 4.0 * lambda_k**2)) / 2.0
        beta = (lambda_k - 1.0) / lambda_next
        lambda_k = lambda_next
        
        # 1. 前瞻外推点 y_k
        y = x + beta * (x - x_prev)
        
        # 2. 在前瞻点计算梯度并更新
        x_next = y - alpha * grad_f(y)
        
        x_prev = x.copy()
        x = x_next
        history.append(x.copy())
        
    return x, np.array(history)
```

---

## 🎯 知识自测与主动回忆

> [!question]- 1. Nesterov 加速梯度法 (NAG) 与 Polyak 重球法最核心的区别是什么？
> **答案**：Polyak 重球法在当前位置 $x_k$ 处计算梯度；而 NAG 采用前瞻（Look-ahead）机制，先沿上一时刻动量外推得到探点 $y_k = x_k + \beta (x_k - x_{k-1})$，并在探点 $y_k$ 处计算梯度 $\nabla f(y_k)$。这种机制赋予了算法提前纠偏的阻尼响应能力。

> [!question]- 2. 对于 $L$-光滑凸函数，标准梯度下降与 Nesterov 加速法的收敛阶数分别是多少？
> **答案**：标准梯度下降在常数步长下的收敛速率为 $\mathcal{O}(1/k)$；Nesterov 加速梯度法将其提升至 $\mathcal{O}(1/k^2)$，且已证明该速率是一阶黑盒光滑凸优理论上不可逾越的理论下界。

> [!question]- 3. 为什么在强凸函数（$\mu$-strongly convex）下，NAG 的动量系数可以设为常数？
> **答案**：强凸函数具备全局二次下界，此时 NAG 选用常数动量系数 $\beta = \frac{\sqrt{L} - \sqrt{\mu}}{\sqrt{L} + \sqrt{\mu}} = \frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}$ 即可获得从 $\mathcal{O}(1 - 1/\kappa)^k$ 提升至 $\mathcal{O}(1 - 1/\sqrt{\kappa})^k$ 的指数级线性收敛加速。

> [!question]- 4. 什么是 Nesterov 估计序列 (Estimating Sequences) 技术？
> **答案**：Estimating Sequences 是 Nesterov 提出的一种证明方法，通过构建一族二次下界凸函数序列 $\phi_k(x) \le f(x)$，使得 $\phi_k(x^*)$ 逼近 $f(x^*)$，从而绕过传统的微分方程与简单能量分析，严谨证明 $\mathcal{O}(1/k^2)$ 速率。

> [!question]- 5. 在包含非光滑正则项的问题（如 Lasso 的 $L_1$ 范数）中，如何应用 Nesterov 加速思想？
> **答案**：将 Nesterov 加速思想与近端算子（Proximal Operator）结合，衍生出近端加速梯度算法（FISTA, Fast Iterative Shrinkage-Thresholding Algorithm），在保持免求导特性的同时同样达到 $\mathcal{O}(1/k^2)$ 收敛速率。

---

## 🃏 Anki 卡片

Q: 写出 Nesterov 加速梯度法 (NAG) 的两步迭代更新公式。
A: $y_k = x_k + \beta_k (x_k - x_{k-1})$ (前瞻探点)； $x_{k+1} = y_k - \alpha \nabla f(y_k)$ (探点梯度修正)。
<!-- id: opt-nag-01 -->

---

Q: 为什么 NAG 比 Polyak 重球法更容易在病态问题中避免震荡？
A: NAG 在动量前瞻点 $y_k$ 处评估梯度。如果上一步动量使点冲向山脊上方，探点 $y_k$ 处的梯度会立刻产生反方向阻尼制动，防止由于惯性盲目冲过头。
<!-- id: opt-nag-02 -->

---

Q: 在光滑凸优化中，NAG 将一阶方法的收敛复杂度降低到了什么界限？
A: 从梯度下降的 $\mathcal{O}(1/k)$ 降低到了 $\mathcal{O}(1/k^2)$，达到了黑盒一阶光滑凸优化理论下界。
<!-- id: opt-nag-03 -->

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
