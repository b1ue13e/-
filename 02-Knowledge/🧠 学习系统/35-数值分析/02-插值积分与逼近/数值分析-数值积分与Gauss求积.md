---
type: study
topic: "数值积分与Gauss求积"
course: "数值分析"
created: 2026-08-08
status: ongoing
stage_moc: "[[🧭 阶段2-插值积分与逼近]]"
upstream: ["[[数值分析-多项式插值与Chebyshev节点]]"]
flow: knowledge
kind: concept
tags: [学习, 数值分析, 数值积分, NewtonCotes, Gauss求积, 代数精度]
---

# 数值分析-数值积分与Gauss求积

> "数值求积公式的核心是代数精确度。等距节点 Newton-Cotes 的代数精度最高为 $n$（或 $n+1$），而选取正交多项式零点的 Gauss-Legendre 公式能用 $n$ 个点达到惊人的 $2n-1$ 阶最高代数精度。"

---

## 1. 严密数学定义与代数精度

数值求积公式定义为：
$$I(f) = \int_a^b f(x) w(x) dx \approx I_n(f) = \sum_{i=1}^n w_i f(x_i)$$

### 代数精确度定理
若求积公式对所有次数不超过 $m$ 的多项式均严格成立，而对某个 $m+1$ 次多项式不成立，则称其具有 **$m$ 次代数精度**。
- **定理**：使用 $n$ 个节点的求积公式，其代数精度最高不超过 **$2n-1$ 次**。

### Gauss 求积公式基本定理
设权函数 $w(x) \ge 0$。求积节点 $x_1, \dots, x_n$ 构成 Gauss 节点的充要条件是：
节点多项式 $\omega_n(x) = \prod_{i=1}^n (x - x_i)$ 与任意次数 $\le n-1$ 的多项式在权函数 $w(x)$ 下正交：
$$\int_a^b \omega_n(x) P_k(x) w(x) dx = 0, \quad \forall k \le n-1$$
当 $w(x)=1, [a, b]=[-1, 1]$ 时，对应的正交多项式为 **Legendre 多项式 $P_n(x)$**，其求积权重由积分显式给出且全部严格为正（$w_i > 0$），保证了极致的数值稳定性！

---

## 2. 经典公式误差阶对比

| 求积公式类型 | 节点个数 $n$ | 节点选取 | 代数精度 | 复合求积截断误差界 |
| :--- | :---: | :--- | :---: | :--- |
| **复合梯形公式** | 2 | 等距端点 | 1 | $-\frac{(b-a)h^2}{12} f''(\xi) = O(h^2)$ |
| **复合 Simpson 公式**| 3 | 等距端点与中点 | 3 | $-\frac{(b-a)h^4}{180} f^{(4)}(\xi) = O(h^4)$ |
| **Gauss-Legendre** | $n$ | Legendre 零点 | **$2n-1$** | $\frac{(b-a)^{2n+1} (n!)^4}{(2n+1)[(2n)!]^3} f^{(2n)}(\xi)$ |

---

## 3. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---

## 4. 检索练习与自测

1. 证明 Gauss 求积公式的所有求积系数 $w_i$ 严格为正，并说明这为何彻底避免了浮点相消误差。
2. 简述自适应 Simpson 积分（Adaptive Simpson Quadrature）的误差估计与二分递归策略。
