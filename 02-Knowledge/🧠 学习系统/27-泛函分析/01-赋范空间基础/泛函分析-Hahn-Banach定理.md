---
type: study
topic: "Hahn-Banach定理"
course: "泛函分析"
created: 2026-08-09
updated: 2026-08-09
status: active
stage_moc: "[[🧭 阶段1-赋范空间基础]]"
flow: knowledge
kind: derivation
difficulty: intermediate
concept: ["Hahn-Banach定理", "次线性泛函", "保范延拓", "对偶空间", "分离超平面", "Mazur定理", "Minkowski泛函"]
prerequisites: ["赋范空间与Banach空间", "有界线性算子与算子范数"]
upstream: ["[[泛函分析-赋范空间与Banach空间]]", "[[泛函分析-有界线性算子与算子范数]]"]
tags: [学习, 数学, 泛函分析, Hahn-Banach, 泛函延拓, 对偶空间, 超平面分离]
proof_mode: true
source: "MIT 18.102 Lec 7-8; Erwin Kreyszig, Chapter 4.1-4.3; Haim Brezis, Chapter 1"
source_url: "https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0"
---

# 泛函分析-Hahn-Banach定理

> 所属阶段：[[🧭 阶段1-赋范空间基础|第一阶段：赋范空间基础]]

---

## 0. 知识定位与核心价值

- **核心使命**：解决无穷维空间中连续线性泛函的“存在性与丰富性”根本问题。在无穷维抽象赋范空间中，我们无法像有限维那样通过标准正交基的坐标投影直接写出线性泛函；Hahn-Banach 定理保证了局部子空间上的线性泛函可以**无损保范延拓到全空间**，并在几何上保证了不相交凸集可被**超平面连续分离**。
- **不可替代性**：没有 Hahn-Banach 定理，连续对偶空间 $X^*$、二次对偶嵌入 $X \hookrightarrow X^{**}$、弱拓扑、分布理论以及凸优化对偶性全部失去存在性根基。

---

## 1. 问题驱动与几何动机

> **我们面临的核心困境**：
> 1. **非平凡泛函的存在危机**：给定一个抽象无穷维赋范空间 $X$，除了平凡的零泛函 $f \equiv 0$ 之外，我们如何确信空间上存在足够多的连续线性泛函？甚至对任意给定的非零向量 $x_0 \in X$，是否存在一个泛函 $f \in X^*$ 能精准“测出”它的长度（即 $f(x_0) = \|x_0\|$ 且 $\|f\| = 1$）？
> 2. **局部信息的全局延拓**：如果我们在子空间 $M \subset X$ 上构造了一个性质优良的连续线性泛函 $f_0: M \to \mathbb{R}$，能否在不放大其算子范数的前提下将其延拓为全空间泛函 $F: X \to \mathbb{R}$？
> 3. **几何切割问题**：在无穷维空间中，两个互不相交的凸集 $A$ 和 $B$，能否找到一个封闭的“超平面”（即某个连续线性泛函的等高线 $\{x \mid f(x) = \alpha\}$）将它们彻底隔开？

---

## 2. 前置知识准备

1. **[[泛函分析-赋范空间与Banach空间]]**：向量空间结构与范数公理。
2. **[[泛函分析-有界线性算子与算子范数]]**：算子范数 $\|f\|_{X^*} = \sup_{\|x\|\le 1} |f(x)|$。
3. **Zorn 引理 (偏序极大元公理)**：任何非空归纳偏序集必存在极大元。

---

## 3. 代数形式：次线性泛函与代数延拓定理

### 1. 次线性泛函 (Sublinear Functional)

设 $X$ 为实向量空间。映射 $p: X \to \mathbb{R}$ 称为**次线性泛函**，若满足：
1. **正齐次性**：$p(\alpha x) = \alpha p(x), \quad \forall \alpha > 0, \ x \in X$；
2. **次可加性**：$p(x + y) \le p(x) + p(y), \quad \forall x, y \in X$。

> 💡 **典型特例**：范数 $p(x) = \|x\|$、半范数 $p(x) = |f(x)|$ 以及凸集的 Minkowski 泛函均是次线性泛函。

---

### 2. Hahn-Banach 代数延拓定理

**定理陈述**：设 $X$ 为实向量空间，$p: X \to \mathbb{R}$ 为次线性泛函。设 $M$ 为 $X$ 的线性子空间，$f: M \to \mathbb{R}$ 为定义在 $M$ 上的线性泛函，且满足被控条件：
$$f(x) \le p(x), \quad \forall x \in M$$
则必定存在定义在全空间 $X$ 上的线性泛函 $F: X \to \mathbb{R}$，使得：
1. $\left.F\right|_M = f$（对所有 $x \in M$，$F(x) = f(x)$）；
2. $F(x) \le p(x), \quad \forall x \in X$。

---

### 3. 证明战略地图 (Proof Strategy Map)

```
[子空间 M 上的线性泛函 f] 
        │
        ▼ (第一步：单步一维延拓)
[选取 x_0 ∉ M，在 M ⊕ R*x_0 上寻找常数 c 使得 f(m)+t*c ≤ p(m+t*x_0)]
        │ 利用次加性构造上下确界夹逼区间 [sup A, inf B] ≠ ∅
        ▼
[一维延拓存在性确立]
        │
        ▼ (第二步：超限递推与 Zorn 引理)
[在所有保持被控性质的延拓偏序集中提取极大元 (X_max, F)]
        │ 若 X_max ≠ X 则与第一步产生的一维更大延拓矛盾
        ▼
[全空间延拓完成: X_max = X]
```

#### 手把手推导单步一维延拓

1. **形式设定**：取 $x_0 \in X \setminus M$。定义延拓 $\tilde{f}(m + t x_0) = f(m) + t c$。
2. **不等式约束**：
   - 当 $t > 0$ 时：$f(m) + t c \le p(m + t x_0) \implies c \le \frac{1}{t} [p(m + t x_0) - f(m)] = p(y + x_0) - f(y)$（令 $y = m/t \in M$）；
   - 当 $t < 0$ 时：令 $t = -s \ (s > 0)$，$f(m) - s c \le p(m - s x_0) \implies c \ge \frac{1}{s} [f(m) - p(m - s x_0)] = f(z) - p(z - x_0)$（令 $z = m/s \in M$）。
3. **上确界与下确界相容性验证**：
   任取 $y, z \in M$：
   $$f(z) + f(y) = f(z + y) \le p(z + y) = p(z - x_0 + y + x_0) \le p(z - x_0) + p(y + x_0)$$
   移项即得：
   $$f(z) - p(z - x_0) \le p(y + x_0) - f(y), \quad \forall y, z \in M$$
4. **夹逼结论**：
   $$\sup_{z \in M} [f(z) - p(z - x_0)] \le \inf_{y \in M} [p(y + x_0) - f(y)]$$
   区间非空！在此区间内任选实数 $c$，即完成一维子空间的合法延拓。

---

## 4. 赋范空间保范延拓与四大核心推论

在实/复赋范空间 $(X, \|\cdot\|)$ 中取次线性泛函 $p(x) = \|f\|_{M^*} \|x\|$，即可得到著名的**保范延拓定理**。

| 推论名称 | 数学陈述 | 几何与分析意义 |
| :--- | :--- | :--- |
| **推论 1 (保范延拓)** | 设 $M \subset X$ 为子空间，$f \in M^*$，则存在 $F \in X^*$ 使得 $\left.F\right|_M = f$ 且 $\|F\|_{X^*} = \|f\|_{M^*}$ | 局部连续测量可无损推广至全空间 |
| **推论 2 (点对偶支撑)** | $\forall x_0 \ne 0 \in X$，存在 $f \in X^*$ 满足 $\|f\|_{X^*} = 1$ 且 $f(x_0) = \|x_0\|$ | 每个向量的范数均可由对偶单位球面上的极值点精确取到 |
| **推论 3 (点分离性质)** | 若对所有 $f \in X^*$ 均有 $f(x) = f(y)$，则 $x = y$ | 连续线性泛函足以区分空间中任意两个不同点 |
| **推论 4 (二次对偶等距嵌入)** | 典范映射 $J: X \to X^{**}, \ J(x)(f) = f(x)$ 满足 $\|J(x)\|_{X^{**}} = \|x\|_X$ | 任意赋范空间均等距同构于其二次对偶的子空间 |

---

## 5. 几何形式：Minkowski 泛函与 Mazur 超平面分离定理

### 1. Minkowski 泛函（规范泛函）构造与性质

设 $C \subset X$ 是包含原点 $0$ 的**凸开集**。对任意 $x \in X$，定义其 Minkowski 泛函：
$$p_C(x) = \inf \left\{ t > 0 \ \middle|\ \frac{x}{t} \in C \right\}$$

- **正齐次性**：对 $\alpha > 0$，$p_C(\alpha x) = \alpha p_C(x)$；
- **次可加性**：若 $x/s \in C, y/t \in C$，由 $C$ 的凸性，$\frac{x+y}{s+t} = \frac{s}{s+t}\frac{x}{s} + \frac{t}{s+t}\frac{y}{t} \in C \implies p_C(x+y) \le s+t$，取下确界得 $p_C(x+y) \le p_C(x) + p_C(y)$；
- **开凸集刻画**：$C = \{ x \in X \mid p_C(x) < 1 \}$ 且 $p_C$ 连续（存在 $M > 0$ 使 $p_C(x) \le M \|x\|$）。

---

### 2. Mazur 超平面分离定理

设 $X$ 为实赋范空间，$A, B \subset X$ 为非空互不相交的凸集（$A \cap B = \emptyset$）。

1. **弱分离定理 (开集弱分离)**：
   若 $A$ 是**开集**，则存在非零连续线性泛函 $f \in X^*$ 及实数 $\alpha \in \mathbb{R}$，使得：
   $$f(x) < \alpha \le f(y), \quad \forall x \in A, \ \forall y \in B$$
   *(几何图像：开凸集 $A$ 落在开半空间内，凸集 $B$ 落在闭半空间内)*。

2. **强分离定理 (闭集与紧集强分离)**：
   若 $A$ 是**闭集**，$B$ 是**紧集**，则存在 $f \in X^*$ 及 $\varepsilon > 0$，使得：
   $$f(x) + \varepsilon \le \alpha \le f(y) - \varepsilon, \quad \forall x \in A, \ \forall y \in B$$
   *(几何图像：两个集合之间存在严格正厚度的“隔离带”)*。

---

## 6. 经典反例与认知对抗

### 反例 1：两闭凸集若均非紧，强分离可能彻底失效

- **空间**：Hilbert 序列空间 $l^2$。
- **闭凸集构造**：
  - $A = \{ x = (x_n) \in l^2 \mid x_n \ge 0, \ \forall n \ge 1 \}$（全正锥闭凸集）；
  - $B = \{ y = (y_n) \in l^2 \mid y_n = - \frac{1}{n} + n z_n, \ \text{其中 } z \in A \}$。
- **失效机制**：$A$ 与 $B$ 均为闭凸集且 $A \cap B = \emptyset$。但构造序列可证 $\operatorname{dist}(A, B) = \inf_{x \in A, y \in B} \|x - y\|_{l^2} = 0$。因此不存在任何连续线性泛函能在两集合间留出严格正间隙 $\varepsilon > 0$。
- **结论**：**强分离定理中“至少一个集合为紧集”的条件在无穷维中是绝对必需的，不可弱化为闭集！**

---

## 7. 闭卷验收自测

- [ ] 能在无提示情况下写出一维单步延拓中常数 $c$ 的构造式及相容性不等式推导。
- [ ] 能严格证明：$\|x\| = \sup_{f \in X^*, \|f\|=1} |f(x)|$。
- [ ] 能证明 Minkowski 泛函的次可加性，并解释为何 $p_C(x) < 1 \iff x \in C$。
- [ ] 能陈述 Mazur 弱分离与强分离定理的前提差异，并举出两闭集强分离失效的反例。

---

## 8. 分级习题

1. **基础题**：设 $X$ 是赋范空间，$M \subset X$ 是闭子空间，$x_0 \notin M$。令 $d = \operatorname{dist}(x_0, M) > 0$。证明：存在 $f \in X^*$ 满足 $\left.f\right|_M = 0$，$f(x_0) = 1$ 且 $\|f\|_{X^*} = \frac{1}{d}$。
2. **进阶题 (Mazur 引理与对偶闭性)**：设 $M \subset X$ 是线性子空间。证明：$M$ 是闭子空间 $\iff M = \{x \in X \mid f(x) = 0, \ \forall f \in M^0\}$（其中 $M^0$ 是 $M$ 的连续零化子）。

> [!question]- 习题解析
> 1. 在子空间 $M_1 = M \oplus \mathbb{R} x_0$ 上定义线性泛函 $f_0(m + t x_0) = t$。对任意 $m \in M, t \ne 0$：
>    $$\|m + t x_0\| = |t| \left\| \frac{m}{t} + x_0 \right\| \ge |t| d = |f_0(m + t x_0)| d$$
>    故 $|f_0(m + tx_0)| \le \frac{1}{d} \|m + tx_0\|$，即 $\|f_0\|_{M_1^*} \le 1/d$。由距离定义取序列 $m_k \in M$ 使 $\|x_0 - m_k\| \to d$，得 $\|f_0\| = 1/d$。由 Hahn-Banach 保范延拓即得全空间泛函 $f \in X^*$。
> 2. 记 $N = \{x \in X \mid f(x) = 0, \ \forall f \in M^0\} = \bigcap_{f \in M^0} \ker(f)$。因为每个 $\ker(f)$ 是闭集，交集 $N$ 必为闭集。显然 $M \subset N$。若 $M$ 闭且存在 $x_0 \in N \setminus M$，由第 1 题存在 $f \in X^*$ 使得 $\left.f\right|_M = 0 \implies f \in M^0$，但 $f(x_0) = 1 \ne 0$，这与 $x_0 \in N$ 矛盾！故 $M = N$。

---

## 🃏 Anki 卡片

TARGET DECK: 泛函分析::01-赋范空间基础

Q: Hahn-Banach 保范延拓定理的核心陈述是什么？它如何导出向量范数的对偶表示？
A: 
1. **保范延拓**：设 $M \subset X$ 为子空间，$f \in M^*$，则存在全空间泛函 $F \in X^*$ 满足 $\left.F\right|_M = f$ 且 $\|F\|_{X^*} = \|f\|_{M^*}$。
2. **对偶表示**：对任意 $x \in X$，$\|x\|_X = \max_{f \in X^*, \|f\|=1} |f(x)|$。
<!--ID: 1723180000009-->

Q: Mazur 凸集分离定理中，“弱分离”与“强分离”对集合拓扑性质的前提要求有何根本区别？
A: 
1. **弱分离**（$f(x) < \alpha \le f(y)$）：要求至少一个集合是**开凸集**；
2. **强分离**（$f(x) + \varepsilon \le \alpha \le f(y) - \varepsilon$）：要求一个集合是**闭凸集**，另一个集合必须是**紧凸集**（若两者仅为闭集，无穷维中可能因距离 $\operatorname{dist}(A,B)=0$ 而强分离失效）。
<!--ID: 1723180000010-->

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
