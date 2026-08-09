---
type: study
topic: "Riesz表示定理与Lax-Milgram引理"
course: "泛函分析"
created: 2026-08-09
updated: 2026-08-09
status: active
stage_moc: "[[🧭 阶段2-Hilbert与基本定理]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: ["Riesz表示定理", "Lax-Milgram引理", "自对偶同构", "双线性型", "矫顽性", "PDE弱解存在性"]
prerequisites: ["Hilbert空间与正交投影定理", "有界线性算子与算子范数"]
upstream: ["[[泛函分析-Hilbert空间与正交投影定理]]", "[[泛函分析-有界线性算子与算子范数]]"]
tags: [学习, 数学, 泛函分析, Riesz表示定理, Lax-Milgram, 变分法, PDE, 对偶]
proof_mode: true
source: "MIT 18.102 Lec 8; Erwin Kreyszig, Chapter 3.8; Haim Brezis, Chapter 5"
source_url: "https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0"
---

# 泛函分析-Riesz表示定理与Lax-Milgram引理

> 所属阶段：[[🧭 阶段2-Hilbert与基本定理|第二阶段：Hilbert与基本定理]]
> 目标：掌握 Hilbert 空间自对偶同构 $H^* \cong H$ 的核空间正交补构造证明，推导 Lax-Milgram 引理在双线性型矫顽条件下的弱解存在唯一性定理。

---

## 0. 知识定位与对偶同构的突破

### 1. 连续线性泛函的具象化：Riesz 表示定理
在一般 Banach 空间中，对偶空间 $X^*$ 的元素是抽象的连续线性泛函，无法“画出来”。
**在 Hilbert 空间中，几何正交性带来终极具象化**：每一个连续线性泛函 $f \in H^*$，都可以被空间内部的一个**唯一的固定向量 $y \in H$ 精确代表**：
$$f(x) = \langle x, y \rangle, \quad \forall x \in H, \quad \text{且 } \|f\|_{H^*} = \|y\|_H$$
这意味着 Hilbert 空间是**等距反线性自对偶的**（$H^* \cong H$）。

### 2. 弱解理论的母机：Lax-Milgram 引理
偏微分方程的弱形式通常对应一个双线性型 $a(u, v) = f(v)$。若 $a(u, v)$ 不对称，内积结构失效。
**Lax-Milgram 引理**保证：只要 $a(u, v)$ 满足**连续性**与**矫顽性（Coercivity）**，无论其是否对称，变分弱解 $u \in H$ **必定存在、唯一，且连续依赖于右端载荷**！

---

## 1. Riesz-Fréchet 表示定理

### 1. 定理陈述
设 $H$ 为 Hilbert 空间。对任意连续线性泛函 $f \in H^*$，必定存在唯一的向量 $y_f \in H$，使得：
$$f(x) = \langle x, y_f \rangle, \quad \forall x \in H$$
且满足保范性：$\|y_f\|_H = \|f\|_{H^*}$。

### 2. 证明战略地图 (利用核空间正交补)
```
[连续线性泛函 f ∈ H*]
        │ 取其闭核子空间 M = ker(f)
        ▼
[正交直和分解: H = ker(f) ⊕ (ker(f))^⊥]
        │ 若 f ≠ 0，则 (ker(f))^⊥ 为一维子空间
        ▼
[选取非零向量 z ∈ (ker(f))^⊥，利用 f(x)z - f(z)x ∈ ker(f) 建立正交关联]
        │ 令代表元 y_f = (f(z)* / ||z||^2) * z
        ▼
[验证 f(x) = <x, y_f> 且 ||y_f|| = ||f||]
```

**手把手推导**：
1. 若 $f \equiv 0$，取 $y_f = 0$ 显然成立。
2. 设 $f \not\equiv 0$。则 $M = \ker(f) = f^{-1}(\{0\})$ 是 $H$ 的**闭真子空间**。
3. 由正交分解定理，$M^\perp \ne \{0\}$。取单位向量 $z_0 \in M^\perp$ 且 $\|z_0\| = 1$。
4. 对任意 $x \in H$，构造向量 $v = f(x) z_0 - f(z_0) x$。
   计算 $f(v) = f(x) f(z_0) - f(z_0) f(x) = 0 \implies v \in \ker(f) = M$。
5. 因为 $v \in M$ 而 $z_0 \in M^\perp$，两者必然正交：
   $$\langle v, z_0 \rangle = 0 \implies \langle f(x) z_0 - f(z_0) x, z_0 \rangle = 0 \implies f(x) \langle z_0, z_0 \rangle - f(z_0) \langle x, z_0 \rangle = 0$$
6. 因 $\|z_0\| = 1$，移项即得：
   $$f(x) = \langle x, \overline{f(z_0)} z_0 \rangle$$
7. 令代表元 $y_f = \overline{f(z_0)} z_0 \in H$，即严格实现 $f(x) = \langle x, y_f \rangle$。
8. 保范性：$|f(x)| \le \|x\| \|y_f\| \implies \|f\| \le \|y_f\|$；又 $f(y_f) = \langle y_f, y_f \rangle = \|y_f\|^2 \implies \|f\| \ge \|y_f\|$。故 $\|f\|_{H^*} = \|y_f\|_H$。唯一性由内积非退化立得！

---

## 2. Lax-Milgram 引理 (变分偏微分方程核心基石)

### 1. 定理陈述
设 $H$ 为实 Hilbert 空间。双线性型 $a: H \times H \to \mathbb{R}$ 满足：
1. **连续性 (有界性)**：存在 $C > 0$，使得 $|a(u, v)| \le C \|u\| \|v\|, \quad \forall u, v \in H$；
2. **矫顽性 (Coercivity / 椭圆性)**：存在 $\alpha > 0$，使得 $a(u, u) \ge \alpha \|u\|^2, \quad \forall u \in H$。

则对任意连续线性泛函 $f \in H^*$，**必定存在唯一的 $u \in H$**，满足变分方程：
$$a(u, v) = f(v), \quad \forall v \in H$$
且弱解满足先验稳定界：$\|u\|_H \le \frac{1}{\alpha} \|f\|_{H^*}$。

### 2. 证明主线 (构造诱导算子 + Banach 不动点 / 投影定理)
1. 对每个固定的 $u \in H$，映射 $v \mapsto a(u, v)$ 是 $H$ 上的连续线性泛函（由连续性界 $C \|u\|$）。
2. 由 Riesz 表示定理，存在唯一的向量 $A u \in H$，使得 $a(u, v) = \langle Au, v \rangle \ (\forall v \in H)$。
3. 易证 $A: H \to H$ 是有界线性算子，且 $\|A\| \le C$。
4. 由 Riesz 定理，右端项 $f(v) = \langle w, v \rangle$（其中 $w \in H$ 唯一）。
5. 原变分方程等价于算子方程：$Au = w$。要证解的存在唯一性，只需证 $A$ 是**全空间同构（满射且单射）**。
6. **单射与闭值域**：由矫顽性，$\alpha \|u\|^2 \le a(u, u) = \langle Au, u \rangle \le \|Au\| \|u\| \implies \|Au\| \ge \alpha \|u\|$。算子有下界，故 $A$ 单射且值域 $\operatorname{Im}(A)$ 为闭子空间。
7. **满射**：若 $\operatorname{Im}(A) \subsetneq H$，则存在非零 $z \in (\operatorname{Im}(A))^\perp$。
   此时 $\langle Au, z \rangle = 0 \ (\forall u \in H)$。取 $u = z$，得 $a(z, z) = \langle Az, z \rangle = 0 \implies \alpha \|z\|^2 \le 0 \implies z = 0$，矛盾！
8. 故 $\operatorname{Im}(A) = H$，$A$ 存在连续逆算子 $A^{-1}$，弱解 $u = A^{-1} w$ 唯一存在且 $\|u\| \le \frac{1}{\alpha}\|f\|$。证毕！

---

## 3. 闭卷自测与练习

- [ ] 能在无提示情况下完成 Riesz 表示定理中利用核空间正交补构造代表元 $y_f$ 的证明。
- [ ] 能推导 Lax-Milgram 引理中诱导算子 $A$ 满足 $\|Au\| \ge \alpha \|u\|$ 及其闭值域证明。
- [ ] 能解释为什么当双线性型 $a(u,v)$ 对称时，Lax-Milgram 弱解等价于能量泛函 $J(v) = \frac{1}{2}a(v,v) - f(v)$ 的唯一极小元。

---

## 🃏 Anki 卡片

TARGET DECK: 泛函分析::02-Hilbert与基本定理

Q: 叙述 Riesz-Fréchet 表示定理的核心结论。
A: 
对 Hilbert 空间 $H$ 上的任意连续线性泛函 $f \in H^*$，存在唯一的 $y_f \in H$ 使得 $f(x) = \langle x, y_f \rangle \ (\forall x \in H)$ 且 $\|y_f\|_H = \|f\|_{H^*}$。它确立了 Hilbert 空间的等距反线性自对偶同构 $H^* \cong H$。
<!--ID: 1723180000014-->

Q: 叙述 Lax-Milgram 引理的前提条件与核心结论。
A: 
1. **条件**：双线性型 $a(u,v)$ 满足连续性（$|a(u,v)| \le C\|u\|\|v\|$）与矫顽性（$a(u,u) \ge \alpha \|u\|^2$）。
2. **结论**：对任意 $f \in H^*$，存在唯一弱解 $u \in H$ 满足 $a(u,v)=f(v) \ (\forall v \in H)$，且 $\|u\| \le \frac{1}{\alpha}\|f\|_{H^*}$。
<!--ID: 1723180000015-->

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
