---
type: study
topic: "赋范空间与Banach空间"
course: "泛函分析"
created: 2026-08-09
updated: 2026-08-09
status: active
stage_moc: "[[🧭 阶段1-赋范空间基础]]"
flow: knowledge
kind: derivation
difficulty: intermediate
concept: ["赋范空间", "Banach空间", "完备性", "等价范数", "Riesz引理", "单位球非紧性", "绝对收敛级数准则"]
prerequisites: ["度量空间完备化与稠密性", "实分析Lp空间与Holder不等式"]
upstream: ["[[泛函分析-前置-度量空间完备化与稠密性]]", "[[泛函分析-前置-实分析Lp空间与Holder不等式]]"]
tags: [学习, 数学, 泛函分析, 赋范空间, Banach空间, Riesz引理, 空间几何]
proof_mode: true
source: "MIT 18.102 Lec 1-2; Erwin Kreyszig, Chapter 2.1-2.4"
source_url: "https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0"
---

# 泛函分析-赋范空间与Banach空间

> 所属阶段：[[🧭 阶段1-赋范空间基础|第一阶段：赋范空间基础]]
> 目标：理解线性结构与拓扑度量的融合，掌握绝对收敛级数完备性判据与 Riesz 几乎正交引理，建立无穷维空间单位球非紧性的核心几何心智模型。

---

## 0. 知识定位与无穷维危机

### 1. 为什么需要 Banach 空间？
纯代数只有加法数乘，没有极限；纯度量空间只有距离，没有线性运算。**赋范空间**将代数结构与几何长度合二为一，而 **Banach 空间**则进一步要求解析完备性（任意 Cauchy 列必收敛于空间内部）。没有完备性，任何通过序列逼近求解微分方程（如 Picard/Newton 迭代法）的工具都会面临极限跳出解空间的崩溃。

### 2. 有限维直觉的全面破产（无穷维四大分水岭）
1. **闭球非紧危机**：在有限维中，闭单位球必为紧集（Bolzano-Weierstrass）；在无穷维中，闭单位球**绝非紧集**，有界序列无法直接提取强收敛子列！
2. **范数不等价**：在有限维中所有范数互相等价；在无穷维中，强弱范数千差万别（如 $C[0,1]$ 上的 $L^1$ 范数与 $L^\infty$ 范数）。
3. **非闭子空间遍地**：在无穷维中，存在大量非闭的稠密线性子空间（如多项式空间 $\mathcal{P}[0,1] \subset C[0,1]$）。

---

## 1. 核心定义与公理体系

### 1. 赋范线性空间 (Normed Linear Space)
设 $X$ 是数域 $\mathbb{K}$ ($\mathbb{R}$ 或 $\mathbb{C}$) 上的向量空间。映射 $\|\cdot\|: X \to [0, \infty)$ 称为 $X$ 上的**范数 (Norm)**，若满足以下三条公理：
1. **正定性**：$\|x\| \ge 0$，且 $\|x\| = 0 \iff x = 0$；
2. **绝对齐次性**：$\|\alpha x\| = |\alpha| \|x\|, \quad \forall \alpha \in \mathbb{K}, \ x \in X$；
3. **三角不等式**：$\|x + y\| \le \|x\| + \|y\|, \quad \forall x, y \in X$。

赋范空间 $(X, \|\cdot\|)$ 自然诱导平移不变度量：$d(x, y) = \|x - y\|$。

### 2. Banach 空间 (巴拿赫空间)
若赋范线性空间 $(X, \|\cdot\|)$ 关于诱导度量 $d(x,y) = \|x - y\|$ 是**完备的**（即 $X$ 中的任意 Cauchy 列都在 $X$ 中收敛），则称 $X$ 为 **Banach 空间**。

---

## 2. 核心定理陈述与证明重建

### 1. 核心判定定理：绝对收敛级数准则
**定理**：赋范空间 $X$ 是 Banach 空间，当且仅当 $X$ 中**每一个绝对收敛的级数都必定在 $X$ 中收敛**，即：
$$\sum_{n=1}^\infty \|x_n\| < \infty \implies \sum_{n=1}^\infty x_n \text{ 在 } X \text{ 中收敛}$$

**证明主线**：
1. **必要性 ($\implies$)**：设 $X$ 完备，$\sum \|x_n\| < \infty$。令部分和 $s_k = \sum_{n=1}^k x_n$。
   对 $m > k$，由三角不等式：
   $$\|s_m - s_k\| = \left\|\sum_{n=k+1}^m x_n\right\| \le \sum_{n=k+1}^m \|x_n\| \to 0 \quad (k \to \infty)$$
   故 $(s_k)$ 是 $X$ 中的 Cauchy 列。由完备性，级数收敛。
2. **充分性 ($\impliedby$)**：设任一绝对收敛级数收敛。取 $X$ 中任一 Cauchy 列 $(y_n)$。
   递推选取子列 $y_{n_k}$，满足 $\|y_{n_{k+1}} - y_{n_k}\| < 2^{-k}$。
   令 $x_1 = y_{n_1}, \ x_k = y_{n_k} - y_{n_{k-1}} \ (k \ge 2)$。
   则 $\sum_{k=1}^\infty \|x_k\| \le \|y_{n_1}\| + \sum_{k=1}^\infty 2^{-k} < \infty$。
   由条件，级数 $\sum x_k$ 收敛于某个 $y \in X$。其部分和即为子列 $y_{n_k} \to y$。
   由 Cauchy 列的性质，子列收敛蕴含全列收敛：$y_n \to y$。故 $X$ 完备。

---

### 2. 空间几何分水岭：Riesz 引理与单位球紧性定理
**Riesz 引理 (几乎正交引理)**：
设 $Y$ 为赋范空间 $X$ 的闭真子空间。则对任意 $\theta \in (0, 1)$，必定存在单位向量 $x_\theta \in X$（即 $\|x_\theta\| = 1$），使得：
$$\operatorname{dist}(x_\theta, Y) = \inf_{y \in Y} \|x_\theta - y\| \ge \theta$$

**定理 (有限维几何分水岭)**：
赋范线性空间 $X$ 的**闭单位球 $\overline{B(0, 1)}$ 是紧集 $\iff \dim X < \infty$**。

**证明主线 (无穷维闭球必非紧)**：
1. 若 $\dim X = \infty$，取任意单位向量 $e_1 \in X$。令 $Y_1 = \operatorname{span}\{e_1\}$，这是闭真子空间。
2. 取 $\theta = 1/2$，由 Riesz 引理存在单位向量 $e_2 \in X$ 满足 $\|e_2 - e_1\| \ge 1/2$。
3. 令 $Y_2 = \operatorname{span}\{e_1, e_2\}$，重复利用 Riesz 引理，递推构造单位向量序列 $(e_n)_{n=1}^\infty \subset \overline{B(0, 1)}$，满足：
   $$\|e_n - e_m\| \ge \frac{1}{2}, \quad \forall n \ne m$$
4. 序列 $(e_n)$ 中任意两点的距离都至少为 $1/2$，因此**绝不可能包含任何 Cauchy 子列或收敛子列**！
5. 故闭单位球 $\overline{B(0, 1)}$ 绝非序列紧集。证毕！

---

## 3. 经典反例库

### 反例 1：无穷维空间的子空间未必是闭子空间
- **空间**：$X = l^\infty$（有界序列空间赋上确界范数），取子空间 $c_{00}$（所有仅有有限项非零的序列）。
- **反例构造**：构造序列 $x^{(n)} = \left( 1, \frac{1}{2}, \frac{1}{3}, \dots, \frac{1}{n}, 0, 0, \dots \right) \in c_{00}$。
- **极限点**：在 $l^\infty$ 范数下，$x^{(n)} \to x = \left( 1, \frac{1}{2}, \frac{1}{3}, \dots, \frac{1}{k}, \dots \right)$。
- **结论**：$x \in c_0 \subset l^\infty$（无穷小序列），但 $x$ 有无穷多项非零，故 $x \notin c_{00}$。
  这表明：**$c_{00}$ 在 $l^\infty$ 中不是闭子空间，因此 $(c_{00}, \|\cdot\|_\infty)$ 不是 Banach 空间**。

---

## 4. 条件变式：有限维与无穷维的根本分水岭

| 变式维度 | 有限维赋范空间 | 无穷维赋范空间 |
| :--- | :--- | :--- |
| **完备性** | **总是完备的**（必为 Banach 空间） | **未必完备**（依赖范数选取） |
| **范数等价性** | **任意两个范数均等价**（拓扑唯一） | **存在大量互不等价的范数** |
| **闭球紧性** | **闭单位球必为紧集**（Bolzano-Weierstrass） | **闭单位球绝非紧集**（Riesz 引理） |
| **线性子空间闭性** | **任意线性子空间必定是闭子空间** | **存在非闭的稠密真子空间** |

---

## 5. 闭卷验收自测

- [ ] 能写出赋范空间 3 条公理与 Banach 空间定义。
- [ ] 能独立完成“绝对收敛级数收敛 $\iff$ 空间完备”的双向证明。
- [ ] 能写出 Riesz 几乎正交引理并推导为何无穷维空间闭单位球非紧。
- [ ] 能严格书写 $(C[a,b], \|\cdot\|_\infty)$ 完备性的“逐点极限 $\to$ 一致收敛 $\to$ 极限连续”三步法。
- [ ] 能准确说出有限维与无穷维在闭球紧性与范数等价性上的本质差异。

---

## 6. 分级习题

1. **基础题**：设 $X$ 是 Banach 空间，$M$ 是 $X$ 的闭线性子空间。定义商空间 $X/M$ 上的商范数 $\|[x]\|_{X/M} = \inf_{m \in M} \|x - m\|_X$。证明商范数满足范数公理。
2. **综合题**：继续上题，证明商空间 $(X/M, \|\cdot\|_{X/M})$ 必为 Banach 空间。

> [!question]- 习题解析
> 1. ① 正定性：显然 $\|[x]\| \ge 0$。若 $\|[x]\| = 0$，则存在序列 $m_k \in M$ 使得 $\|x - m_k\| \to 0$，即 $m_k \to x$。因 $M$ 是**闭集**，极限点 $x \in M \implies [x] = 0 + M$。② 绝对齐次性由 $\inf_{m \in M} \|\alpha x - m\| = |\alpha| \inf_{m^\prime \in M} \|x - m^\prime\|$ 直接得出。③ 三角不等式：对任意 $\varepsilon > 0$，取 $m_1, m_2 \in M$ 使 $\|x - m_1\| < \|[x]\| + \varepsilon, \|y - m_2\| < \|[y]\| + \varepsilon$，则 $\|[x+y]\| \le \|(x+y)-(m_1+m_2)\| \le \|x-m_1\| + \|y-m_2\| < \|[x]\| + \|[y]\| + 2\varepsilon$。令 $\varepsilon \to 0$ 即得。
> 2. 利用绝对收敛级数准则。设 $\sum_{k=1}^\infty \|[x_k]\| < \infty$。对每个 $k$，由商范数定义可选取代表元 $y_k \in [x_k]$ 使得 $\|y_k\|_X \le \|[x_k]\| + 2^{-k}$。则 $\sum_{k=1}^\infty \|y_k\|_X \le \sum \|[x_k]\| + 1 < \infty$。由于 $X$ 是 Banach 空间，级数在 $X$ 中绝对收敛并收敛到 $y \in X$。记 $[y] \in X/M$，易由商映射的连续性得 $\sum [x_k] = [y]$。故 $X/M$ 完备。

---

## 🃏 Anki 卡片

TARGET DECK: 泛函分析::01-赋范空间基础

Q: 什么是绝对收敛级数准则（Banach 空间的等价判定）？
A: 
赋范线性空间 $X$ 是 Banach 空间（完备），当且仅当 $X$ 中每一个绝对收敛的级数都必定在 $X$ 中收敛：
$$\sum_{n=1}^\infty \|x_n\| < \infty \implies \sum_{n=1}^\infty x_n \text{ 在 } X \text{ 中收敛}$$
<!--ID: 1723180000007-->

Q: 叙述 Riesz 几乎正交引理与闭单位球紧性的几何分水岭定理。
A: 
1. **Riesz 引理**：设 $Y \subsetneq X$ 为闭真子空间，$\forall \theta \in (0, 1), \exists x_\theta \in X (\|x_\theta\|=1)$ 使得 $\operatorname{dist}(x_\theta, Y) \ge \theta$。
2. **几何分水岭**：赋范空间 $X$ 的闭单位球 $\overline{B(0, 1)}$ 为紧集 $\iff \dim X < \infty$。
<!--ID: 1723180000008-->

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
