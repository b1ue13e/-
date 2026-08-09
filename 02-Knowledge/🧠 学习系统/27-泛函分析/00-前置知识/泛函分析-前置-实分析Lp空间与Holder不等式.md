---
type: study
topic: "实分析Lp空间与Holder不等式"
course: "泛函分析"
created: 2026-08-09
updated: 2026-08-09
status: active
stage_moc: "[[🧭 泛函分析-前置知识]]"
flow: knowledge
kind: derivation
difficulty: beginner
concept: ["Lp空间", "Holder不等式", "Minkowski不等式", "共轭指数", "Young不等式", "几乎处处等价类"]
prerequisites: ["微积分与极限", "Riemann/Lebesgue积分基础"]
tags: [学习, 数学, 泛函分析, 实分析, Lp空间, 不等式, 测度论]
proof_mode: true
source: "Haim Brezis, Functional Analysis, Sobolev Spaces and PDEs, Chapter 4; Erwin Kreyszig, Chapter 1"
source_url: "https://link.springer.com/book/10.1007/978-0-387-70914-7"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0"
---

# 泛函分析-前置-实分析Lp空间与Holder不等式

> 所属阶段：[[🧭 泛函分析-前置知识|00-前置知识]]
> 目标：打通从离散向量空间 $\mathbb{R}^n$ 到连续函数空间 $L^p(\Omega)$ 的度量底座，掌握 Young、Hölder 与 Minkowski 不等式的完整证明与心智模型。

---

## 0. 核心动机与小白避坑直觉

### 1. 从离散 $\mathbb{R}^n$ 到连续 $L^p(\Omega)$：为什么需要等价类？
在有限维中，向量 $x = (x_1, \dots, x_n)$ 的 $p$-范数是：
$$\|x\|_p = \left( \sum_{i=1}^n |x_i|^p \right)^{1/p}$$
很自然地，把连续函数 $f(x)$ 视为“无穷多个点的函数值构成的向量”，积分 $\int_\Omega |f(x)|^p dx$ 就是离散求和的连续极限。
- **🚨 致命陷阱**：如果直接定义 $\|f\|_{L^p} = \left( \int_\Omega |f(x)|^p dx \right)^{1/p}$，若 $f(x)$ 仅在单个孤立点处非零（例如 $f(0)=1$ 其余处为 $0$），则其积分 $\|f\|_{L^p} = 0$，但 $f \not\equiv 0$！这直接违反了范数正定性公理（$\|f\|=0 \implies f=0$）。
- **💡 解决方案（几乎处处等价类）**：在 $L^p$ 中，元素**不是单个函数，而是几乎处处（a.e.）相等的函数等价类**。只要两函数仅在零测集上不同，它们就是空间中的同一个“向量”。

### 2. 三角不等式的几何难关
对 $p > 1$，要证明 $\|f + g\|_{L^p} \le \|f\|_{L^p} + \|g\|_{L^p}$，直接展开 $(|f+g|)^p$ 无法拆开。必须引入：
$$\text{Young 不等式 (双曲线面积分割)} \implies \text{Hölder 不等式 (对偶内积上界)} \implies \text{Minkowski 不等式 (三角不等式)}$$

---

## 1. 共轭指数与 Young 不等式（图形面积直觉）

### 1. 共轭指数 (Conjugate Exponent)
设 $1 < p < \infty$。定义其共轭指数 $q$ 满足：
$$\frac{1}{p} + \frac{1}{q} = 1 \iff q = \frac{p}{p - 1} \iff (p-1)(q-1) = 1$$
- 当 $p = 2$ 时，$q = 2$（自身共轭，对应 Hilbert 空间 $L^2$）；
- 当 $p \to 1$ 时，$q \to \infty$（极限对偶对 $(L^1, L^\infty)$）。

### 2. Young 不等式证明与图像直觉
**定理**：设 $a, b \ge 0$，$1 < p, q < \infty$ 满足 $\frac{1}{p} + \frac{1}{q} = 1$。则：
$$a b \le \frac{a^p}{p} + \frac{b^q}{q}$$
等号成立当且仅当 $a^p = b^q$。

**证明（凸性法）**：
考虑严格下凸函数 $\varphi(t) = \exp(t)$。由指数函数的严格凸性，对任意 $\lambda = \frac{1}{p} \in (0, 1)$（对应 $1-\lambda = \frac{1}{q}$）：
$$\exp\left( \frac{1}{p} \ln(a^p) + \frac{1}{q} \ln(b^q) \right) \le \frac{1}{p} \exp(\ln(a^p)) + \frac{1}{q} \exp(\ln(b^q))$$
左边简化为 $\exp(\ln a + \ln b) = ab$，右边简化为 $\frac{a^p}{p} + \frac{b^q}{q}$。证毕！

---

## 2. 核心定理：Hölder 不等式与 Minkowski 不等式

### 1. Hölder 不等式 (Hölder's Inequality)
**定理**：设 $f \in L^p(\Omega), g \in L^q(\Omega)$，其中 $1 \le p \le \infty$ 且 $\frac{1}{p} + \frac{1}{q} = 1$。则乘积 $f g \in L^1(\Omega)$，且满足：
$$\int_\Omega |f(x) g(x)| d\mu \le \|f\|_{L^p} \|g\|_{L^q}$$
等号成立当且仅当存在非负常数 $\alpha, \beta$ 使得 $\alpha |f|^p = \beta |g|^q$ a.e.。

**手把手无跳步推导**：
1. 若 $\|f\|_{L^p} = 0$ 或 $\|g\|_{L^q} = 0$，不等式显然为 $0 \le 0$。
2. 构造**归一化单位向量**：令 $u(x) = \frac{|f(x)|}{\|f\|_{L^p}}$，$v(x) = \frac{|g(x)|}{\|g\|_{L^q}}$。
3. 对每个点 $x \in \Omega$，应用 Young 不等式（令 $a = u(x), b = v(x)$）：
   $$u(x) v(x) \le \frac{u(x)^p}{p} + \frac{v(x)^q}{q}$$
4. 两边对测度空间 $\Omega$ 积分：
   $$\int_\Omega u(x) v(x) d\mu \le \frac{1}{p} \int_\Omega u(x)^p d\mu + \frac{1}{q} \int_\Omega v(x)^q d\mu = \frac{1}{p} \cdot 1 + \frac{1}{q} \cdot 1 = \frac{1}{p} + \frac{1}{q} = 1$$
5. 代回 $u(x)$ 与 $v(x)$ 的定义，两边同乘 $\|f\|_{L^p} \|g\|_{L^q}$ 即得证！

---

### 2. Minkowski 不等式 ($L^p$ 空间的三角不等式)
**定理**：对任意 $1 \le p \le \infty$ 以及 $f, g \in L^p(\Omega)$：
$$\|f + g\|_{L^p} \le \|f\|_{L^p} + \|g\|_{L^p}$$

**证明**：
当 $p=1$ 或 $p=\infty$ 时由标量绝对值三角不等式直接成立。设 $1 < p < \infty$：
$$\|f + g\|_{L^p}^p = \int_\Omega |f + g|^p d\mu = \int_\Omega |f + g| \cdot |f + g|^{p-1} d\mu \le \int_\Omega |f| |f+g|^{p-1} d\mu + \int_\Omega |g| |f+g|^{p-1} d\mu$$
对右边两项分别应用 Hölder 不等式（注意共轭指数 $q = \frac{p}{p-1} \implies (p-1)q = p$）：
$$\int_\Omega |f| |f+g|^{p-1} d\mu \le \|f\|_{L^p} \left( \int_\Omega (|f+g|^{p-1})^q d\mu \right)^{1/q} = \|f\|_{L^p} \|f+g\|_{L^p}^{p/q} = \|f\|_{L^p} \|f+g\|_{L^p}^{p-1}$$
同理第二项 $\le \|g\|_{L^p} \|f+g\|_{L^p}^{p-1}$。
两项相加合并：
$$\|f + g\|_{L^p}^p \le \left( \|f\|_{L^p} + \|g\|_{L^p} \right) \|f+g\|_{L^p}^{p-1}$$
两边同除以 $\|f+g\|_{L^p}^{p-1}$，即得 $\|f + g\|_{L^p} \le \|f\|_{L^p} + \|g\|_{L^p}$！证毕！

---

## 3. 经典反例与认知对抗

### 反例 1：有界区域上 $L^p$ 空间的单调包含性在无穷测度空间彻底崩溃
- **有界区间情况 ($\Omega = (0, 1)$)**：若 $1 \le p_1 \le p_2 \le \infty$，由 Hölder 不等式（与常数函数 $1 \in L^{p_2/(p_2-p_1)}$ 作内积），必有 $L^{p_2}(0, 1) \subset L^{p_1}(0, 1)$。
- **全实轴情况 ($\Omega = \mathbb{R}$)**：包含关系**彻底失效**！
  - 函数 $f(x) = \frac{1}{\sqrt{x}} \mathbf{1}_{(0, 1)}(x) \in L^1(\mathbb{R})$ 但 $f \notin L^2(\mathbb{R})$（近原点奇异）；
  - 函数 $g(x) = \frac{1}{1 + |x|} \in L^2(\mathbb{R})$ 但 $g \notin L^1(\mathbb{R})$（无穷远衰减慢）。
- **结论**：**只有在有限测度空间中才有小 $p$ 空间包容大 $p$ 空间；在无界区域 $\mathbb{R}^d$ 上，$L^p$ 空间之间互不包含！**

---

## 4. 闭卷自测与练习

- [ ] 能在无提示情况下写出共轭指数定义式 $\frac{1}{p} + \frac{1}{q} = 1$ 与指数凸性证明 Young 不等式。
- [ ] 能利用单位化技巧从头推导 Hölder 不等式。
- [ ] 能通过拆分 $|f+g|^p = |f+g||f+g|^{p-1}$ 严格推导 Minkowski 三角不等式。
- [ ] 能举出 $\mathbb{R}$ 上属于 $L^2$ 但不属于 $L^1$ 的反例函数。

---

## 🃏 Anki 卡片

TARGET DECK: 泛函分析::00-前置知识

Q: 叙述 Hölder 不等式与 Minkowski 不等式的形式及其在泛函分析中的核心地位。
A: 
1. **Hölder 不等式**：$\int |f g| d\mu \le \|f\|_{L^p} \|g\|_{L^q}$（$\frac{1}{p} + \frac{1}{q} = 1$），它是无穷维空间对偶内积有界性的基石。
2. **Minkowski 不等式**：$\|f+g\|_{L^p} \le \|f\|_{L^p} + \|g\|_{L^p}$，它保证了 $L^p$ 范数满足向量空间的三角不等式公理。
<!--ID: 1723180000002-->

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
