---
type: study
topic: "近端梯度与FISTA"
course: "07-最优化方法"
created: 2026-08-06
status: completed
flow: knowledge
kind: concept
stage_moc: "[[🧭 阶段4-现代一阶与随机优化]]"
upstream:
  - "[[最优化方法-次梯度方法]]"
  - "[[最优化方法-一阶方法收敛性分析]]"
difficulty: advanced
---
# 最优化方法-近端梯度与FISTA



## 1. 这个知识点解决什么问题？
> **我们遇到了什么麻烦**：
考虑如下**复合优化问题** (Composite Optimization)：
$$ \min_x F(x) = g(x) + h(x) $$
其中：
- $g(x)$ 是凸且连续可导的（平滑，例如 MSE 损失）。
- $h(x)$ 是凸但**不可导**的（非平滑，例如 L1 范数 $\|x\|_1$ 正则化，用于产生稀疏解）。

如果直接对 $F(x)$ 使用次梯度下降，不仅收敛极慢（$\mathcal{O}(1/\sqrt{k})$），而且往往无法得到严格的稀疏解，因为次梯度的震荡会破坏 $x$ 准确落在 0 上的机会。我们希望有一种方法，能享受 $g(x)$ 平滑性带来的快速下降，又能精确且高效地处理 $h(x)$ 的不可导特性。

---
## 2. 为什么它重要？它有什么用？
- **连接大图景**：它是非平滑优化的一阶方法基石。它巧妙地将牛顿法中“二次逼近”的思想与拉格朗日乘子法/正则化结合。
- **实际应用场景**：
  - **LASSO 回归** (L1 正则化特征选择)。
  - **图像处理** (Total Variation 去噪，ISTA/FISTA 极其常用)。
  - **推荐系统** (核范数正则化的矩阵补全)。
- **高频题型/任务**：推导各类函数的近端算子 (Proximal Operator) 的闭式解，证明 ISTA 的单步下降引理，理解 FISTA 加速的动量构造。

---
## 3. 学它之前需要哪些前置知识？
1. **[[最优化方法-一阶方法收敛性分析]]**：平滑函数的二次上界逼近（Lipschitz 梯度）。
2. **[[最优化方法-次梯度方法]]**：理解非平滑函数最优性条件（$0 \in \partial F(x)$）。
3. **动量加速**：Nesterov 加速梯度方法的基本思想。

---
## 4. 用直觉语言解释它
> «"先顺着平坦的路走一步，然后再被拉扯回有约束的规则区域。"»
- **直觉类比/几何图像**：
  近端梯度下降分为两步：
  1. **梯度步 (Gradient Step)**：只看平滑项 $g(x)$，闭上眼睛先沿着梯度方向迈出一步，到达一个中间点。
  2. **近端步 (Proximal Step)**：这个中间点可能偏离了非平滑项 $h(x)$ 鼓励的区域（比如 L1 鼓励稀疏性，它希望坐标等于 0）。近端算子的作用就像一个“黑洞”或者“投影仪”，它在“距离刚才中间点不要太远”和“尽量最小化 $h(x)$”之间寻找一个折中，将中间点拉向特定结构（如将小数值直接强行置零，实现截断）。
- **一句话直觉本质**：用二次函数在当前点逼近平滑部分 $g(x)$，并在此二次代理模型上精确求解加上非平滑部分 $h(x)$ 后的解析最优解。

---
## 5. 正式定义、核心公式、符号解释
### 1. 近端算子 (Proximal Operator)
对于闭凸函数 $h(x)$ 和参数 $t > 0$，定义近端算子为：
$$ \text{prox}_{th}(v) = \arg\min_x \left( h(x) + \frac{1}{2t} \|x - v\|_2^2 \right) $$
**解释**：寻找一个点 $x$，使得 $h(x)$ 尽量小，同时不偏离给定的点 $v$ 太多。

### 2. 近端梯度下降 (ISTA)
迭代公式：
$$ x_{k+1} = \text{prox}_{t_k h} \left( x_k - t_k \nabla g(x_k) \right) $$
其中 $t_k$ 是步长（可以恒定为 $1/L$ 或回溯线搜索决定）。
当 $h(x) = \lambda \|x\|_1$ 时，这被称为 ISTA (Iterative Shrinkage-Thresholding Algorithm)。

### 3. FISTA (Fast ISTA)
Nesterov 提出的加速版本，引入了巧妙的动量序列。
初始化 $y_1 = x_0$, $t_1 = 1$。
在第 $k \ge 1$ 步：
1. $x_k = \text{prox}_{L^{-1} h} \left( y_k - \frac{1}{L} \nabla g(y_k) \right)$  (标准的 ISTA 更新，但在评估点 $y_k$ 上进行)
2. $t_{k+1} = \frac{1 + \sqrt{1 + 4t_k^2}}{2}$
3. $y_{k+1} = x_k + \frac{t_k - 1}{t_{k+1}} (x_k - x_{k-1})$  (外推/动量步)

### 4. 符号说明表
| 符号 | 含义 |
|---|---|
| $g(x)$ | 平滑目标项 (梯度 $L$-Lipschitz 连续) |
| $h(x)$ | 非平滑正则项 (需容易求近端算子) |
| $\text{prox}_{th}$ | $h$ 缩放 $t$ 倍的近端算子 |
| $L$ | $g(x)$ 的 Lipschitz 常数 |
| $y_k$ | FISTA 中的外推评估点 |

---
## 6. 推导思路和思想来源
- **核心动机：Majorization-Minimization (MM) 思想**
  因为 $g(x)$ 的梯度是 $L$-Lipschitz 连续的，我们在 $x_k$ 处有一个全局的二次上界：
  $$ g(x) \le g(x_k) + \langle \nabla g(x_k), x - x_k \rangle + \frac{L}{2} \|x - x_k\|_2^2 $$
  由于我们要最小化 $F(x) = g(x) + h(x)$，我们将上面这个比较难搞的 $g(x)$ 替换成它的二次上界：
  $$ x_{k+1} = \arg\min_x \left( g(x_k) + \langle \nabla g(x_k), x - x_k \rangle + \frac{L}{2} \|x - x_k\|_2^2 + h(x) \right) $$
  通过配方法，忽略与 $x$ 无关的常数项，上式等价于：
  $$ x_{k+1} = \arg\min_x \left( \frac{L}{2} \left\| x - (x_k - \frac{1}{L}\nabla g(x_k)) \right\|_2^2 + h(x) \right) $$
  令 $v = x_k - \frac{1}{L}\nabla g(x_k)$（这恰好是只针对 $g$ 做一次梯度下降的中间结果），上式恰好就是近端算子的定义：
  $$ x_{k+1} = \text{prox}_{\frac{1}{L} h} (v) $$
- **为什么自然得到此结论**：这非常优雅。我们把本来极其复杂的耦合在一起的非平滑优化，拆解成两步：一步纯粹的平滑梯度下降，一步针对非平滑项的解析投影（要求 $h$ 结构简单）。

---
## 7. 例子：基础 → 中等 → 实际应用
### 例子 1：基础例子（L1 范数的近端算子 / 软阈值）
设 $h(x) = \lambda \|x\|_1$，求 $\text{prox}_{th}(v)$。
$$ \arg\min_x \left( \lambda \|x\|_1 + \frac{1}{2t} \|x - v\|_2^2 \right) $$
由于各项在各个维度上是解耦的，考虑标量形式：$\min_{x_i} \left( \lambda |x_i| + \frac{1}{2t} (x_i - v_i)^2 \right)$。
通过对 $x_i > 0, x_i < 0, x_i = 0$ 分别求导，我们得到闭式解——**软阈值算子 (Soft-Thresholding)**：
$$ x_i^* = S_{\lambda t}(v_i) = \text{sign}(v_i) \max(|v_i| - \lambda t, 0) $$
**直觉**：如果梯度步走完后的值 $v_i$ 在 $[-\lambda t, \lambda t]$ 之间，那就强制置 0（这就是 LASSO 产生稀疏性的直接原因）；如果超出了这个范围，就把它向 0 的方向收缩 $\lambda t$ 的大小。

### 例子 2：投影算子作为近端算子的特例
考虑示性函数 $h(x) = I_C(x)$，即如果 $x \in C$ 则为 0，否则为 $\infty$。
则 $\text{prox}_{th}(v) = \arg\min_x \left( I_C(x) + \frac{1}{2t} \|x - v\|_2^2 \right) = \arg\min_{x \in C} \|x - v\|_2^2$。
这就是将 $v$ 投影到凸集 $C$ 上的正交投影算子 $\Pi_C(v)$。
所以，**投影梯度下降法 (Projected Gradient Descent)** 只是近端梯度法的一个特例！

### 例子 3：Python 实现 LASSO 问题的 FISTA
解决 $\min_x \frac{1}{2}\|Ax - b\|_2^2 + \lambda \|x\|_1$

```python
import numpy as np

def soft_thresholding(v, t):
    return np.sign(v) * np.maximum(np.abs(v) - t, 0)

def fista_lasso(A, b, lmbda, max_iter=1000, tol=1e-6):
    L = np.linalg.norm(A, ord=2)**2 # Lipschitz constant (最大特征值)
    step_size = 1.0 / L
    
    n_features = A.shape[1]
    x = np.zeros(n_features)
    y = np.zeros(n_features)
    t = 1.0
    
    for k in range(max_iter):
        x_old = x.copy()
        
        # 1. Gradient step at point y
        grad_g = A.T @ (A @ y - b)
        v = y - step_size * grad_g
        
        # 2. Proximal step (Soft-thresholding)
        x = soft_thresholding(v, step_size * lmbda)
        
        # Check convergence
        if np.linalg.norm(x - x_old) < tol:
            break
            
        # 3. FISTA Momentum update
        t_next = (1 + np.sqrt(1 + 4 * t**2)) / 2
        y = x + ((t - 1) / t_next) * (x - x_old)
        t = t_next
        
    return x
```

---
## 8. 常见误区和易混概念
### 误区 1：只要有不可导项，都应该用近端梯度法
**纠正**：近端梯度法要求非平滑项 $h(x)$ 的近端算子必须是**容易计算的（最好有解析解）**。如果 $h(x)$ 非常复杂（比如复杂的重叠组范数），求解它本身的近端算子需要内层迭代，代价极其高昂，这种情况下可能需要考虑 ADMM 或交替优化方法。

### 概念对比表
| 方法 | 目标函数形式 | 收敛速度 | 能否产生精确零/稀疏解 |
|---|---|---|---|
| **次梯度法 (Subgradient)** | $F(x)$ (不可导) | $\mathcal{O}(1/\sqrt{k})$ (极慢) | 难（一直震荡） |
| **ISTA** | $g(x) + h(x)$ | $\mathcal{O}(1/k)$ (平稳) | 能（近端算子直接截断） |
| **FISTA** | $g(x) + h(x)$ | $\mathcal{O}(1/k^2)$ (最优) | 能（加速收敛） |

---
## 9. 相关知识点与 Obsidian 双链建议
### 上游依赖
- [[最优化方法-一阶方法收敛性分析]]
- [[最优化方法-次梯度方法]]
- [[最优化方法-凸集与凸函数]]

### 下游延伸
- [[最优化方法-增广拉格朗日与ADMM]] (用于更复杂的近端算子分解)
- [[最优化方法-在线优化与镜像下降]]

### 横向关联
- [[最优化方法-凸优化与拉格朗日对偶]]：对偶分解与近端方法的关系。

---
## 10. 闭卷复现任务
1. 写出近端算子 $\text{prox}_{th}(v)$ 的定义公式。
2. 从二次上界逼近（MM算法思想）推导 ISTA 的更新公式。
3. 推导并画出 L1 范数 $h(x) = \lambda |x|$ 的近端算子闭式解。
4. 默写 FISTA 的三步更新循环公式，特别是动量系数 $t_k$ 的生成规律。

---
## 11. 自测题：5 道

> [!question]- 1. FISTA 中的评估点 $y_k$ 是如何通过上一次的结果和动量构造的？为什么不能直接在 $x_k$ 处求梯度？
> **答案**：评估点由 $y_{k+1} = x_k + \frac{t_k - 1}{t_{k+1}} (x_k - x_{k-1})$ 构造。这被称为 Nesterov 动量外推。
> 如果直接在 $x_k$ 处求梯度，那就是普通的 ISTA，没有利用历史前进方向的动能。通过在 $x_k$ 加上一个“按预期继续往前走”的动量，在预期的位置 $y_k$ 提前计算梯度进行修正，这是 Nesterov 加速法的核心，能将收敛率从 $\mathcal{O}(1/k)$ 提升到最优的 $\mathcal{O}(1/k^2)$。

> [!question]- 2. 如果将 $h(x) = 0$，近端梯度下降会退化为什么算法？
> **答案**：如果 $h(x) = 0$，那么近端算子为 $\arg\min_x \frac{1}{2t} \|x - v\|_2^2$，其解直接就是 $v$。
> 此时更新规则变为 $x_{k+1} = x_k - t_k \nabla g(x_k)$。
> 因此，算法直接退化为普通的梯度下降 (Gradient Descent)。

> [!question]- 3. 什么是 Ridge 回归的正则项？求 L2 正则项 $h(x) = \frac{\lambda}{2} \|x\|_2^2$ 的近端算子。
> **答案**：目标是求解 $\arg\min_x \left( \frac{\lambda}{2} \|x\|_2^2 + \frac{1}{2t} \|x - v\|_2^2 \right)$。
> 这是对 $x$ 的凸可导函数，直接求导令其为 0：
> $\lambda x + \frac{1}{t} (x - v) = 0$
> $(\lambda + \frac{1}{t}) x = \frac{1}{t} v$
> $x = \frac{1}{1 + \lambda t} v$
> 这个算子只是将输入 $v$ 简单的做了一个比例缩小（Shrinkage），没有像 L1 那样产生绝对的 0（截断），因此 L2 正则化不能产生稀疏解。

> [!question]- 4. 证明近端算子 $\text{prox}_{h}(v)$ 必然存在且唯一。（假设 $h$ 是闭的正常凸函数）
> **答案**：近端算子是优化问题 $\min_x \left( h(x) + \frac{1}{2} \|x - v\|_2^2 \right)$ 的解。
> 目标函数由两部分组成。$h(x)$ 是凸函数。$\frac{1}{2}\|x-v\|_2^2$ 是一元二次函数，不仅是凸的，而且是**强凸 (Strongly Convex)** 的。
> 根据凸分析基本定理，闭强凸函数在整个空间上必然有且仅有一个全局最小值点。因此，近端算子的解必然存在且唯一。

> [!question]- 5. 假设对于某个特别复杂的 $h(x)$，我们找不到近端算子的解析解，只能用迭代法去逼近它。在 FISTA 中使用这种“非精确”的近端算子会怎样？
> **答案**：这被称为 Inexact FISTA。如果在每一步近端计算中存在较大的误差，FISTA 那极其敏感的动量加速机制会放大这些误差，导致严重的震荡甚至完全发散（无法维持 $\mathcal{O}(1/k^2)$ 的收敛率）。相比之下，普通的 ISTA（无动量）对非精确近端步骤的容忍度更高。因此，FISTA 仅在近端算子能精确（或极高精度极低成本）计算时才推荐使用。

---

## ⚠️ 常见陷阱与避坑指南

> [!CAUTION]
> 1. **FISTA 动量系数的计算错误**：FISTA (Fast Iterative Shrinkage-Thresholding Algorithm) 的动量更新步必须严格按照 $t_{k+1} = \frac{1 + \sqrt{1 + 4 t_k^2}}{2}$ 更新，且外推组合系数为 $\beta_k = \frac{t_k - 1}{t_{k+1}}$。错误的动量更新会导致振荡发散。
> 2. **Non-monotonicity 现象与 Restart 机制**：FISTA 在优化过程中可能出现函数值剧烈回弹。推荐引入 Monotone FISTA 或在检测到 $(x_k - x_{k-1})^T (y_k - x_k) > 0$ 时重置动量 $t_k = 1$。

## 🃏 Anki 卡片

Q: 近端算子 (Proximal Operator) $\mathbf{prox}_{\gamma h}(x)$ 的标准数学表达式是什么？
A: $\mathbf{prox}_{\gamma h}(x) = \arg\min_{y} \left( h(y) + \frac{1}{2\gamma} \|y - x\|_2^2 
ight)$。它在极小化函数 $h(y)$ 的同时惩罚远离 $x$ 的位移。
<!-- id: opt-prox-01 -->

Q: $L_1$ 正则项 $h(y) = \lambda \|y\|_1$ 的近端算子对应的闭式解算子是什么？
A: 软阈值算子 (Soft-Thresholding Operator) $S_{\gamma \lambda}(x)$：$[S_{\tau}(x)]_i = \mathbf{sign}(x_i) \max(|x_i| - \tau, 0)$。
<!-- id: opt-prox-02 -->


---
Q: Lasso 问题 $f(w) = \frac{1}{2}\|Xw - y\|^2 + \lambda \|w\|_1$ 的近端算子（Proximal Operator）显式解是什么？
A: 软阈值算子（Soft Thresholding）：$\text{prox}_{\gamma \lambda}(u)_i = \text{sign}(u_i) \max(|u_i| - \gamma \lambda, 0)$。
<!-- id: opt-fista-03 -->

## 学完后可以完成


```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
