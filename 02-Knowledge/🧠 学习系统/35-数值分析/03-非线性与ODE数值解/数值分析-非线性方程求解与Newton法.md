---
type: study
topic: "非线性方程求解与Newton法"
course: "数值分析"
created: 2026-08-08
status: ongoing
stage_moc: "[[🧭 阶段3-非线性与ODE数值解]]"
upstream: ["[[数值分析-LU分解与数值稳定性]]", "[[数值分析-前置-泰勒展开与截断误差]]"]
flow: knowledge
kind: concept
tags: [学习, 数值分析, 非线性方程, Newton法, 二次收敛, 阻尼Newton]
---

# 数值分析-非线性方程求解与Newton法

> "求解非线性方程 $f(x)=0$ 的本质是用局部线性化（切线）不断逼近曲面交点。Newton 法在单根附近享有二次收敛的惊人速度，但初值敏感；阻尼线搜索是保证全局收敛的护栏。"

---

## 1. 严密数学推导与收敛性定理

### 一维 Newton-Raphson 迭代
$$x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}$$

### 局部二次收敛性定理
设 $f \in C^2[a, b]$，$f(x^*) = 0$ 且 $f'(x^*) \ne 0$（单根）。利用 Taylor 展开：
$$0 = f(x^*) = f(x_k) + f'(x_k)(x^* - x_k) + \frac{1}{2} f''(\xi_k)(x^* - x_k)^2$$
两端同除以 $f'(x_k)$ 并结合 Newton 迭代式得：
$$e_{k+1} = x_{k+1} - x^* = \frac{f''(\xi_k)}{2 f'(x_k)} e_k^2$$
当 $x_k$ 充分靠近 $x^*$ 时，$\lim_{k \to \infty} \frac{|e_{k+1}|}{|e_k|^2} = \frac{|f''(x^*)|}{2|f'(x^*)|} < \infty$，即**严格二次局部收敛**。

### 多维非线性方程组与阻尼 Newton
对于系统 $F(x) = 0, F: \mathbb{R}^n \to \mathbb{R}^n$：
1. 求解线性增量方程组：$J_F(x_k) \Delta x_k = -F(x_k)$（通过带主元 LU 求解）；
2. 阻尼线搜索：寻找步长 $\alpha_k \in (0, 1]$ 满足 Armijo 准则：
   $$\|F(x_k + \alpha_k \Delta x_k)\|_2 < \|F(x_k)\|_2$$
3. 更新解：$x_{k+1} = x_k + \alpha_k \Delta x_k$。

---

## 2. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---

## 3. 检索练习与自测

1. 证明若 $x^*$ 是 $m$ 重根（$m > 1$），标准 Newton 法退化为线性收敛，并写出恢复二次收敛的修正公式。
2. 解释拟 Newton 法（如 BFGS / Broyden）的核心思想及为什么避免每次计算精确 Jacobi 矩阵。
