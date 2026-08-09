---
type: study
topic: "Hilbert空间与正交投影定理"
course: "泛函分析"
created: 2026-08-09
updated: 2026-08-09
status: active
stage_moc: "[[🧭 阶段2-Hilbert与基本定理]]"
flow: knowledge
kind: derivation
difficulty: intermediate
concept: ["内积空间", "Hilbert空间", "平行四边形律", "正交投影", "直和分解", "闭凸集投影", "变分不等式", "最佳逼近"]
prerequisites: ["赋范空间与Banach空间"]
upstream: ["[[泛函分析-赋范空间与Banach空间]]"]
tags: [学习, 数学, 泛函分析, Hilbert空间, 内积, 正交投影, 凸集投影, 变分不等式]
proof_mode: true
source: "MIT 18.102 Lec 3-4; Erwin Kreyszig, Chapter 3.1-3.4"
source_url: "https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0"
anki_deck: "泛函分析::02-Hilbert与基本定理"
---

# 泛函分析-Hilbert空间与正交投影定理

> 所属阶段：[[🧭 阶段2-Hilbert与基本定理|第二阶段：Hilbert与基本定理]]
> 目标：掌握内积诱导范数的平行四边形律判定，推导闭凸集正交投影的存在唯一性定理，建立 $H = M \oplus M^\perp$ 正交直和分解的几何心智模型。

---

## 0. 知识定位与无穷维欧氏几何

### 1. 为什么需要 Hilbert 空间？
一般的 Banach 空间只有“长度”，没有“角度”与“正交”。在一般赋范空间中，求一个点到子空间的最短距离点可能根本不存在，或者不唯一。
**Hilbert 空间引入内积结构 $\langle x, y \rangle$**，把欧几里得几何的“垂直/正交投影”完美推广到无穷维：
- 任意点到闭凸集的最短距离点**必定存在且绝对唯一**；
- 任意闭子空间均可实现空间的正交直和分解 $H = M \oplus M^\perp$；
- 它是傅里叶级数展开、量子力学态空间与有限元变分法（Céa 引理正交投影）的共同几何底座。

---

## 1. 内积空间与平行四边形律

### 1. 内积公理
映射 $\langle \cdot, \cdot \rangle: H \times H \to \mathbb{C}$ 满足：共轭对称性 $\langle x, y \rangle = \overline{\langle y, x \rangle}$、第一变元线性性、正定性 $\langle x, x \rangle \ge 0$ 且等于 0 当且仅当 $x = 0$。诱导范数 $\|x\| = \sqrt{\langle x, x \rangle}$。

### 2. Jordan-von Neumann 平行四边形律
**定理**：赋范空间 $(X, \|\cdot\|)$ 的范数可由内积诱导 $\iff$ 满足平行四边形恒等式：
$$\|x + y\|^2 + \|x - y\|^2 = 2\|x\|^2 + 2\|y\|^2, \quad \forall x, y \in X$$
*(极化恒等式：实空间中 $\langle x, y \rangle = \frac{1}{4}(\|x+y\|^2 - \|x-y\|^2)$)*。

---

## 2. 核心定理：闭凸集投影定理与正交直和分解

### 1. 闭凸集唯一投影定理
**定理**：设 $H$ 为实/复 Hilbert 空间，$K \subset H$ 为非空**闭凸集**。则对任意 $x \in H$，必定存在唯一的极小化点 $P_K(x) \in K$，使得：
$$\|x - P_K(x)\| = \operatorname{dist}(x, K) = \inf_{y \in K} \|x - y\|$$

**证明主线 (平行四边形律构造 Cauchy 极小化序列)**：
1. 设 $d = \inf_{y \in K} \|x - y\|$。取极小化序列 $(y_n) \subset K$ 满足 $\|x - y_n\| \to d$。
2. 由 $K$ 的凸性，$\frac{y_n + y_m}{2} \in K \implies \left\|x - \frac{y_n + y_m}{2}\right\| \ge d$。
3. 对向量 $u = x - y_n, v = x - y_m$ 应用平行四边形律：
   $$\|y_n - y_m\|^2 = \|u - v\|^2 = 2\|u\|^2 + 2\|v\|^2 - 4\left\|x - \frac{y_n + y_m}{2}\right\|^2 \le 2\|x - y_n\|^2 + 2\|x - y_m\|^2 - 4 d^2$$
4. 当 $m, n \to \infty$ 时，右端 $\to 2 d^2 + 2 d^2 - 4 d^2 = 0$！故 $(y_n)$ 是 Cauchy 列。
5. 由 $H$ 完备且 $K$ 封闭，极限 $y = \lim y_n \in K$ 存在且 $\|x - y\| = d$。唯一性由相同平行四边形等式立得！

---

### 2. 闭凸集投影的变分不等式刻画
**定理**：设 $K \subset H$ 为闭凸集，$x \in H, y \in K$。则：
$$y = P_K(x) \iff \operatorname{Re}\langle x - y, z - y \rangle \le 0, \quad \forall z \in K$$
*(几何直观：向量 $x - y$ 与集合内部方向 $z - y$ 夹角始终大于等于 90 度)*。

**推论 (闭子空间的正交分解)**：
若 $M \subset H$ 是**闭线性子空间**，变分不等式退化为严格正交性：
$$y = P_M(x) \iff x - y \perp M \iff H = M \oplus M^\perp$$

---

## 3. 经典反例库

### 反例 1：$l^p \ (p \ne 2)$ 与 $C[0, 1]$ 绝非 Hilbert 空间
- **检验**：在 $C[0, 1]$ 中取 $f(t) = 1, g(t) = t$。
  $\|f\|_\infty = 1, \|g\|_\infty = 1, \|f+g\|_\infty = 2, \|f-g\|_\infty = 1$。
  左边 $= 2^2 + 1^2 = 5 \ne 2(1^2) + 2(1^2) = 4$。
- **结论**：平行四边形律失效，极大范数无法由任何内积诱导！

---

## 4. 闭卷自测与练习

- [ ] 能在草稿纸上利用平行四边形律证明闭凸集极小化序列必为 Cauchy 列。
- [ ] 能写出闭凸集投影的变分不等式充要条件，并解释其钝角几何图像。
- [ ] 能证明 $P_M$ 是线性自伴投影算子（$P_M^2 = P_M = P_M^*$）。

---

## 🃏 Anki 卡片

TARGET DECK: 泛函分析::02-Hilbert与基本定理

Q: 叙述 Jordan-von Neumann 平行四边形律及其数学地位。
A: 
$$\|x+y\|^2 + \|x-y\|^2 = 2\|x\|^2 + 2\|y\|^2$$
它是赋范空间范数能够由内积诱导（即成为内积空间）的充要条件。
<!--ID: 1723180000012-->

Q: 叙述闭凸集投影定理与闭子空间正交直和分解定理。
A: 
1. **闭凸集投影**：Hilbert 空间中非空闭凸集 $K$ 存在唯一最近点 $P_K(x)$，满足 $\operatorname{Re}\langle x - P_K(x), z - P_K(x) \rangle \le 0 \ (\forall z \in K)$。
2. **正交分解**：对闭子空间 $M \subset H$，$H = M \oplus M^\perp$，且 $M^{\perp\perp} = M$。
<!--ID: 1723180000013-->

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
