---
type: study
topic: "Lax-Milgram定理与椭圆弱解存在性"
course: "偏微分方程"
created: 2026-08-08
status: completed
stage_moc: "[[🧭 阶段4-现代变分弱解与数值计算]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: ["Lax-Milgram定理", "双线性形式", "强制性", "能量最小化", "Galerkin逼近", "Cea引理"]
upstream: ["[[偏微分方程-弱导数Sobolev空间与变分形式]]"]
tags: [学习, 偏微分方程, 变分法, Lax-Milgram, 椭圆方程, 存在唯一性]
---

# Lax-Milgram 定理与椭圆弱解存在性

> 所属阶段 MOC：[[04-现代变分弱解与数值计算/🧭 阶段4-现代变分弱解与数值计算|🧭 阶段 4：现代变分弱解与数值计算]]  
> 学习定位：掌握现代偏微分方程弱解存在唯一性核心判据——Lax-Milgram 定理，严格证明二阶变系数椭圆型方程变分弱解的适定性与能量极小化原理。

---

## 1. 核心问题与物理直觉

在线性代数中，对于正定对称矩阵 $A$，线性方程组 $A x = b$ 不仅有唯一解，而且解 $x$ 恰好是能量二次型泛函 $J(y) = \frac{1}{2}y^T A y - y^T b$ 的唯一全局极小值点（最小位能原理）。
当问题推广到无穷维希尔伯特空间（如函数空间 $H_0^1(\Omega)$）时，微分算子往往是非对称或变系数的。**Lax-Milgram 定理**巧妙地利用 Riesz 空间表示引理与 Banach 压缩映射原理，给出了非对称双线性变分方程 $a(u, v) = \ell(v)$ 解的存在性、唯一性与先验能量估计的完备定理。

---

## 2. 正式数学表述与定理证明

### 2.1 Lax-Milgram 定理陈述
设 $H$ 为实 Hilbert 空间，具有内积 $\langle \cdot, \cdot \rangle_H$ 与诱导范数 $\|\cdot\|_H$。设 $a: H \times H \to \mathbb{R}$ 为双线性形式，$\ell: H \to \mathbb{R}$ 为连续线性泛函（即 $\ell \in H^*$）。
若 $a(\cdot, \cdot)$ 满足以下两个核心条件：
1. **有界性 / 连续性 (Boundedness / Continuity)**：
   存在常数 $M > 0$，使得对任意 $u, v \in H$：
   $$|a(u, v)| \le M \|u\|_H \|v\|_H$$
2. **强制性 / 椭圆性 (Coercivity / Ellipticity)**：
   存在常数 $\alpha > 0$，使得对任意 $u \in H$：
   $$a(u, u) \ge \alpha \|u\|_H^2$$
则变分问题：求 $u \in H$ 满足：
$$a(u, v) = \ell(v), \quad \forall v \in H$$
**存在唯一解 $u \in H$**，并且解满足先验连续依赖估计（稳定性）：
$$\|u\|_H \le \frac{1}{\alpha} \|\ell\|_{H^*}$$

---

### 2.2 严格证明全过程（基于 Riesz 表示引理）

**证明步骤**：
1. **定义诱导算子**：对每一个固定的 $u \in H$，映射 $v \mapsto a(u, v)$ 是 $H$ 上的有界线性泛函（界为 $M\|u\|_H$）。根据 **Riesz 表示引理**，存在唯一的元素 $A u \in H$ 使得：
   $$a(u, v) = \langle A u, v \rangle_H, \quad \forall v \in H$$
   容易验证 $A: H \to H$ 是有界线性算子，且 $\|A\|_{op} \le M$。
2. **转化问题**：同理，对有界线性泛函 $\ell \in H^*$，由 Riesz 定理存在唯一的 $w \in H$ 使得 $\ell(v) = \langle w, v \rangle_H$ 且 $\|w\|_H = \|\ell\|_{H^*}$。原变分问题等价于在 $H$ 中求解算子方程：
   $$A u = w$$
3. **证明 $A$ 是单射且值域闭合**：
   由强制性条件，对任意 $u \in H$：
   $$\alpha \|u\|_H^2 \le a(u, u) = \langle A u, u \rangle_H \le \|A u\|_H \|u\|_H \implies \|A u\|_H \ge \alpha \|u\|_H$$
   这表明 $A$ 具有正下界：$A$ 必为单射，且算子值域 $R(A)$ 在 $H$ 中是闭子空间。
4. **证明值域全满 $R(A) = H$**：
   若 $R(A) \neq H$，由投影定理存在非零向量 $z \in R(A)^\perp (z \neq 0)$，使得对所有 $u \in H$ 成立 $\langle A u, z \rangle_H = 0$。
   特别取 $u = z$，则有 $\langle A z, z \rangle_H = a(z, z) = 0$。
   但由强制性 $\alpha \|z\|_H^2 \le a(z, z) = 0 \implies z = 0$，与 $z \neq 0$ 矛盾！故 $R(A) = H$。
5. **逆算子连续性与先验估计**：
   $A$ 为双射，存在有界逆算子 $A^{-1}$，且 $\|u\|_H = \|A^{-1} w\|_H \le \frac{1}{\alpha} \|w\|_H = \frac{1}{\alpha} \|\ell\|_{H^*}$。证毕。

---

## 3. 应用于一般二阶散度型变系数椭圆方程

考虑定解问题：
$$\begin{cases} -\sum_{i,j=1}^n \frac{\partial}{\partial x_i}\left( a_{ij}(x)\frac{\partial u}{\partial x_j} \right) + c(x)u = f(x), & x \in \Omega \\ u(x) = 0, & x \in \partial \Omega \end{cases}$$
其中系数满足：
1. **一致椭圆性**：$\sum_{i,j=1}^n a_{ij}(x)\xi_i \xi_j \ge \theta |\xi|^2 \, (\theta > 0), \forall \xi \in \mathbb{R}^n$。
2. **有界性**：$a_{ij}, c \in L^\infty(\Omega), |a_{ij}(x)| \le K$。
3. **零阶项非负**：$c(x) \ge 0$ a.e. in $\Omega$。

**验证双线性形式在 $H_0^1(\Omega)$ 上的条件**：
- 双线性形式：$a(u, v) = \int_\Omega \left( \sum a_{ij} \frac{\partial u}{\partial x_j}\frac{\partial v}{\partial x_i} + c u v \right) dx$。
- **连续性**：$|a(u, v)| \le K \|\nabla u\|_{L^2} \|\nabla v\|_{L^2} + \|c\|_{L^\infty} \|u\|_{L^2} \|v\|_{L^2} \le M \|u\|_{H^1} \|v\|_{H^1}$。
- **强制性**：利用一致椭圆性与 $c \ge 0$ 及 Poincaré 不等式：
  $$a(u, u) = \int_\Omega \left( \sum a_{ij} \frac{\partial u}{\partial x_j}\frac{\partial u}{\partial x_i} + c u^2 \right) dx \ge \theta \int_\Omega |\nabla u|^2 dx = \theta \|\nabla u\|_{L^2}^2 \ge \alpha \|u\|_{H_0^1}^2$$
- 由 Lax-Milgram 定理，弱解存在且唯一。

---

## 4. 离散化投影：Galerkin 逼近与 Céa 引理

设 $V_h \subset H_0^1(\Omega)$ 为有限元多项式基函数张成的有限维子空间。
离散问题：求 $u_h \in V_h$ 使得 $a(u_h, v_h) = \ell(v_h), \forall v_h \in V_h$。
- **Galerkin 正交性**：$a(u - u_h, v_h) = 0, \forall v_h \in V_h$。
- **Céa 引理 (Céa's Lemma)**：
  $$\alpha \|u - u_h\|_H^2 \le a(u - u_h, u - u_h) = a(u - u_h, u - v_h) \le M \|u - u_h\|_H \|u - v_h\|_H$$
  $$\|u - u_h\|_H \le \frac{M}{\alpha} \inf_{v_h \in V_h} \|u - v_h\|_H$$
  这证明了有限元数值解 $u_h$ 是全空间真解 $u$ 在有限维子空间 $V_h$ 上的**准最佳逼近**。

---

## 5. 常见误区与反例

- **误区 1：把对称双线性形式的 Riesz 定理与非对称的 Lax-Milgram 定理混同**。当 $a(u, v) = a(v, u)$ 对称时，可以通过能量泛函求极小值；若微分方程包含一阶对流项（非对称），能量泛函不存在，但只要满足强制性，Lax-Milgram 依然成立。
- **误区 2：在无零阶项且纯 Neumann 边界下盲目套用 Lax-Milgram**。若方程为 $-\Delta u = f$ 且 $\frac{\partial u}{\partial n}|_{\partial\Omega} = 0$，常数函数属于算子核空间（$a(1, 1) = 0$ 违背强制性）。此时解不唯一，必须在商空间 $H^1(\Omega) / \mathbb{R}$（即要求平均值 $\int_\Omega u dx = 0$）中才能恢复强制性。

---

## 6. 主动自测与闭卷检查

- [ ] 我能不看笔记默写出 Lax-Milgram 定理的连续性与强制性条件及其结论。
- [ ] 我能写出基于 Riesz 空间算子表示引理证明值域闭合与全满的关键步骤。
- [ ] 我能利用 Galerkin 正交性推导出有限元基础定理——Céa 引理。

---

## 7. 学完后可以完成（派生视图）

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
