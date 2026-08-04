---
title: "拟牛顿法 BFGS 算法 (BFGS Quasi-Newton Method)"
course: "07-最优化方法"
tags:
  - 最优化方法
  - 拟牛顿法
  - BFGS
  - Hessian逆近似
  - 二阶优化
  - 割线方程
type: knowledge_card
status: completed
created: 2026-08-01
---

# 拟牛顿法 BFGS 算法 (BFGS Quasi-Newton Method)

## 1. 拟牛顿法 BFGS 算法的定义与核心动机

**拟牛顿法 BFGS 算法 (BFGS Quasi-Newton Method)** 的核心定义是：一种通过仅利用一阶梯度信息维护一个对称正定的**黑塞矩阵逆矩阵近似 $B_k \approx 
abla^2 f(\mathbf{x}_k)^{-1}$**，以避免显式计算和求逆真实 Hessian 矩阵的无约束二阶凸优化算法。由 Broyden, Fletcher, Goldfarb 和 Shanno 于 1970 年独立共同提出。

**基本性质与核心动机**：标准牛顿法具有超线性（二次）收敛速度，但需要每次迭代计算 $n \times n$ 的 Hessian 矩阵并求解线性方程组，时间复杂度高达 $O(n^3)$。拟牛顿法 BFGS 算法将单次迭代复杂度降低至 $O(n^2)$，且保持了超线性的收敛速率，是无约束非线性最优化中最常用、最稳健的算法。

---

## 2. 割线方程与 BFGS 逆矩阵更新公式形式化推导

**割线方程 (Secant Equation) 假设**：
设当前步迭代变量位移 $\mathbf{s}_k = \mathbf{x}_{k+1} - \mathbf{x}_k$，梯度差值为 $\mathbf{y}_k = \mathbf{g}_{k+1} - \mathbf{g}_k$（其中 $\mathbf{g}_k = 
abla f(\mathbf{x}_k)$）。

对一阶梯度在 $\mathbf{x}_{k+1}$ 处做一阶泰勒展开：
$$\mathbf{g}_{k+1} - \mathbf{g}_k \approx 
abla^2 f(\mathbf{x}_{k+1}) (\mathbf{x}_{k+1} - \mathbf{x}_k) \Rightarrow \mathbf{y}_k = B_{k+1} \mathbf{s}_k$$

设 $H_k = B_k^{-1}$ 为 Hessian 逆矩阵的近似，则割线方程逆矩阵形式为：
$$H_{k+1} \mathbf{y}_k = \mathbf{s}_k$$

**BFGS 秩-2 逆修正矩阵推导**：
假设更新量为秩-2 修正 $H_{k+1} = H_k + \Delta H_k = H_k + \alpha \mathbf{u} \mathbf{u}^T + \beta \mathbf{v} \mathbf{v}^T$。代入割线方程并通过 Sherman-Morrison-Woodbury 公式求逆，推导出经典 **BFGS 逆更新公式**：

$$H_{k+1} = \left( \mathbf{I} - \frac{\mathbf{s}_k \mathbf{y}_k^T}{\mathbf{y}_k^T \mathbf{s}_k} 
ight) H_k \left( \mathbf{I} - \frac{\mathbf{y}_k \mathbf{s}_k^T}{\mathbf{y}_k^T \mathbf{s}_k} 
ight) + \frac{\mathbf{s}_k \mathbf{s}_k^T}{\mathbf{y}_k^T \mathbf{s}_k}$$

**正定性保持推导**：只要线搜索满足 Wolfe 条件（保证曲率条件 $\mathbf{y}_k^T \mathbf{s}_k > 0$），若 $H_k$ 正定，则推导出的 $H_{k+1}$ 必保持**严格对称正定**，从而保证搜索方向 $\mathbf{d}_k = -H_k \mathbf{g}_k$ 永远是严格下降方向。

---

## 3. 拟牛顿法 BFGS 与梯度下降及标准牛顿法对比

| 维度 | 一阶梯度下降 (GD / Adam) | 标准牛顿法 (Newton's Method) | 拟牛顿法 BFGS 算法 |
|:---|:---|:---|:---|
| **用到的阶数信息** | 仅一阶梯度 $
abla f$ | 一阶梯度 + **二阶 Hessian $
abla^2 f$** | **仅一阶梯度** (近似二阶) |
| **单次迭代复杂度** | **$O(n)$** | $O(n^3)$ (求逆 $H^{-1}$) | **$O(n^2)$** (矩阵向量乘法) |
| **局部收敛速度** | 一阶线性收敛 | **二阶二次收敛** | **超线性收敛** |
| **搜索方向** | 最速下降方向 $-\mathbf{g}$ | 二阶牛顿方向 $-
abla^2 f^{-1} \mathbf{g}$ | **拟牛顿方向 $-H_k \mathbf{g}$** |
| **大规模扩展性** | 极佳 | 极差 | 通过 **L-BFGS** 实现有限内存扩展 |

**局限（误区与反例）**：若步长选择不当破坏了曲率条件 $\mathbf{y}_k^T \mathbf{s}_k \le 0$，BFGS 正定性可能丧失；对超高维参数 ($n > 10^6$)，存储 $n \times n$ 的 $H_k$ 仍会爆内存，必须改用存储最近 $m$ 组向量的 L-BFGS 算法。

关联知识点推荐：[[凸优化与拉格朗日对偶]]、[[梯度下降与Adam优化器]]、[[均方误差MSE与Huber损失]]、[[红黑树]]。

---

## 4. Python 手写 BFGS 算法二阶优化自测断言

```python
import numpy as np

def bfgs_optimize(f, grad_f, x0: np.ndarray, max_iter: int = 100) -> tuple:
    """
    手写拟牛顿法 BFGS 算法求解无约束极小化 min f(x)
    H_k 近似 Hessian 逆矩阵
    """
    x = x0.copy().astype(float)
    n = len(x)
    H = np.eye(n)  # 初始初始化为单位阵

    for k in range(max_iter):
        g = grad_f(x)
        if np.linalg.norm(g) < 1e-6:
            break

        # 搜索方向 d = -H * g
        d = -H @ g

        # 简易回溯线搜索 (Backtracking Line Search) 满足 Armijo 条件
        alpha = 1.0
        c1 = 1e-4
        while f(x + alpha * d) > f(x) + c1 * alpha * np.dot(g, d):
            alpha *= 0.5

        x_next = x + alpha * d
        s = x_next - x
        g_next = grad_f(x_next)
        y = g_next - g

        ys = np.dot(y, s)
        if ys > 1e-10:  # 曲率条件
            I = np.eye(n)
            rho = 1.0 / ys
            H = (I - rho * np.outer(s, y)) @ H @ (I - rho * np.outer(y, s)) + rho * np.outer(s, s)

        x = x_next

    return x, float(f(x))

if __name__ == "__main__":
    # 二次函数 f(x, y) = (x-3)^2 + 2*(y+1)^2, 最优解 (3.0, -1.0), f_opt = 0.0
    def f(x): return (x[0] - 3.0)**2 + 2.0 * (x[1] + 1.0)**2
    def grad_f(x): return np.array([2.0 * (x[0] - 3.0), 4.0 * (x[1] + 1.0)])

    x0 = np.array([0.0, 0.0])
    x_opt, f_opt = bfgs_optimize(f, grad_f, x0)

    # 自测验证 1: BFGS 收敛位置极高精度断言
    assert np.allclose(x_opt, [3.0, -1.0], atol=1e-5), f"BFGS 未收敛到最优点: {x_opt}"

    # 自测验证 2: 最优目标值趋近零断言
    assert abs(f_opt - 0.0) < 1e-8

    print(f"拟牛顿法 BFGS 算法收敛位置: x* = {x_opt.round(4)}, f* = {f_opt:.8f}")
    print("拟牛顿法 BFGS 算法单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Nocedal, J., & Wright, S. J. (2006). *Numerical Optimization* (2nd ed.). Springer. Chapter 6 (Quasi-Newton Methods). ISBN: 978-0387303031. DOI: https://doi.org/10.1007/978-0-387-40065-5
- Broyden, C. G. (1970). The convergence of a class of double-rank minimization algorithms. *Journal of the Institute of Mathematics and its Applications*, 6(1), 76-90. DOI: https://doi.org/10.1093/imamat/6.1.76
- Fletcher, R. (1970). A new approach to variable metric algorithms. *The Computer Journal*, 13(3), 317-322. DOI: https://doi.org/10.1093/comjnl/13.3.317
- Goldfarb, D. (1970). A family of variable-metric methods derived by variational means. *Mathematics of Computation*, 24(109), 23-26. DOI: https://doi.org/10.1090/S0025-5718-1970-0258249-6
- Shanno, D. F. (1970). Conditioning of quasi-Newton methods for function minimization. *Mathematics of Computation*, 24(111), 647-656. DOI: https://doi.org/10.1090/S0025-5718-1970-0274029-X
