---
type: study
topic: "多项式插值与Chebyshev节点"
course: "数值分析"
created: 2026-08-08
updated: 2026-08-08
status: completed
stage_moc: "[[🧭 阶段2-插值积分与逼近]]"
upstream: ["[[数值分析-前置-泰勒展开与截断误差]]"]
flow: knowledge
kind: concept
tags: [学习, 数值分析, 插值, Runge现象, Chebyshev节点, 重心拉格朗日]
---

# 数值分析-多项式插值与Chebyshev节点

> “在等距节点上进行高次多项式插值必定在区间两端产生剧烈振荡（Runge 现象）。Chebyshev 节点将采样点按余弦密度聚集于两端，结合重心 Lagrange 第二型公式，使得多项式插值在 $O(n)$ 复杂度下达到指数级几何收敛与向后稳定性。”

---

## 1. 严密数学定义与插值余项

设给定 $n+1$ 个互异节点 $x_0, x_1, \dots, x_n \in [a, b]$ 及对应函数值 $f_i = f(x_i)$。
存在唯一的次数不超过 $n$ 的代数多项式 $P_n(x)$ 满足 $P_n(x_i) = f(x_i)$。

### 1.1 插值余项定理（Cauchy-Lagrange 余项）
设 $f \in C^{n+1}[a, b]$，则对任意 $x \in [a, b]$，存在 $\xi \in (a, b)$ 使得：
$$R_n(x) = f(x) - P_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!} \omega_{n+1}(x)$$
其中 $\omega_{n+1}(x) = \prod_{j=0}^n (x - x_j)$ 称为**节点多项式**。

### 1.2 等距节点的 Runge 灾难与 Lebesgue 常数爆炸
当采用均匀等距网格 $x_j = a + j \frac{b-a}{n}$ 时，随着 $n \to \infty$：
- 节点多项式在区间边缘剧烈膨胀：$\max_{x \in [-1, 1]} |\omega_{n+1}(x)| \approx \frac{n!}{4 n^{n+1}} e^n$；
- 插值投影算子的 Lebesgue 常数指数级发散：$\Lambda_n = \max_x \sum_{j=0}^n |\ell_j(x)| = O(2^n / (n \ln n))$；
- 对经典 Runge 函数 $f(x) = \frac{1}{1 + 25x^2}$ 在 $[-1, 1]$ 上，$P_n(x)$ 在 $|x| > 0.726$ 处发生灾难性震荡发散！

---

## 2. Chebyshev 极小化定理与极值点

### 2.1 第一类 Chebyshev 多项式
定义在 $[-1, 1]$ 上：
$$T_n(x) = \cos(n \arccos x), \quad x \in [-1, 1]$$
满足三项递推关系：$T_0(x) = 1, \; T_1(x) = x, \; T_{n+1}(x) = 2x T_n(x) - T_{n-1}(x)$。
最高次项系数为 $2^{n-1}$（$n \ge 1$）。

### 2.2 极小极大最优性定理（Chebyshev Minimax Theorem）
在区间 $[-1, 1]$ 上所有最高次项系数为 1 的 $n$ 次多项式中，首一 Chebyshev 多项式 $\tilde{T}_n(x) = \frac{1}{2^{n-1}} T_n(x)$ 的无穷范数达到极小：
$$\min_{p_n \in \mathcal{P}_n^1} \max_{x \in [-1, 1]} |p_n(x)| = \max_{x \in [-1, 1]} |\tilde{T}_n(x)| = \frac{1}{2^{n-1}}$$

### 2.3 Chebyshev 插值节点与零点分布
选择 $T_{n+1}(x)$ 的 $n+1$ 个根作为插值节点：
$$x_k = \cos\left( \frac{2k+1}{2n+2} \pi \right), \quad k = 0, 1, \dots, n$$
此时 $\omega_{n+1}(x) = \tilde{T}_{n+1}(x)$，其上界被严格压制为 $\max |\omega_{n+1}(x)| = 2^{-n}$。
Lebesgue 常数仅为对数级缓慢增长：$\Lambda_n = O(\ln n)$，对一切在复平面 Bernstein 椭圆内解析的函数，Chebyshev 插值保证**指数级谱精度收敛（Spectral Convergence）**！

---

## 3. 重心拉格朗日插值第二型算法（Barycentric Lagrange Form II）

传统 Lagrange 插值复杂度为 $O(n^2)$ 且浮点不稳定。现代数值插值黄金标准是重心形式：
$$P_n(x) = \frac{\sum_{j=0}^n \frac{w_j}{x - x_j} f_j}{\sum_{j=0}^n \frac{w_j}{x - x_j}}$$
其中重心权重（Barycentric Weights）在 Chebyshev 零点节点下具有极简解析式：
$$w_j = (-1)^j \sin\left( \frac{2j+1}{2n+2} \pi \right)$$
计算任意一点 $x$ 仅需 $O(n)$ 次运算，且被证明具有**向后稳定性（Higham 2004）**。

```python
import numpy as np

class BarycentricChebyshevInterpolator:
    """基于 Chebyshev 零点节点的重心拉格朗日第二型插值器"""
    def __init__(self, f_func, n_points):
        self.n = n_points
        k = np.arange(self.n)
        # Chebyshev 根
        self.xk = np.cos((2 * k + 1) / (2 * self.n) * np.pi)
        self.fk = f_func(self.xk)
        # 重心权重
        self.wk = ((-1.0) ** k) * np.sin((2 * k + 1) / (2 * self.n) * np.pi)
        
    def evaluate(self, x_eval):
        x = np.asarray(x_eval, dtype=np.float64)
        # 处理与节点重合的特殊情况以防 0/0
        exact_match = (x[:, None] == self.xk[None, :])
        has_match = np.any(exact_match, axis=1)
        
        # 广播差值计算
        diff = x[:, None] - self.xk[None, :]
        with np.errstate(divide='ignore', invalid='ignore'):
            term = self.wk[None, :] / diff
            numer = np.sum(term * self.fk[None, :], axis=1)
            denom = np.sum(term, axis=1)
            result = numer / denom
            
        # 命中节点时直接取真值
        if np.any(has_match):
            for i in np.where(has_match)[0]:
                col = np.where(exact_match[i])[0][0]
                result[i] = self.fk[col]
                
        return result

# 验证 Runge 函数
if __name__ == "__main__":
    runge = lambda x: 1.0 / (1.0 + 25.0 * x**2)
    interp = BarycentricChebyshevInterpolator(runge, n_points=25)
    x_test = np.linspace(-1, 1, 1000)
    y_interp = interp.evaluate(x_test)
    y_true = runge(x_test)
    max_err = np.max(np.abs(y_interp - y_true))
    print(f"25点 Chebyshev 重心插值最大误差: {max_err:.2e} (完全消除 Runge 现象！)")
```

---

## 4. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---

## 5. 检索练习与自测

1. 利用第一类 Chebyshev 多项式的三角代换定义，证明其在区间 $[-1, 1]$ 上正交性：$\int_{-1}^1 T_m(x) T_n(x) \frac{1}{\sqrt{1-x^2}} dx = \frac{\pi}{2} \delta_{mn}$（$m,n \ge 1$）。
2. 写出第二类 Chebyshev 极值点（Chebyshev Lobatto 节点）的坐标公式，并说明为什么该节点在谱方法与微分矩阵构造中被广泛使用。
3. 为什么重心 Lagrange 公式第二型相比于第一型能够消除对节点多项式 $\ell(x) = \prod (x - x_j)$ 的显式评估？
