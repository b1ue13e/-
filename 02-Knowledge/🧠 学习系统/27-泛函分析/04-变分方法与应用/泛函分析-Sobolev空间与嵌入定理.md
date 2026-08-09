---
type: study
topic: "Sobolev空间与嵌入定理"
course: "泛函分析"
created: 2026-08-09
updated: 2026-08-09
status: active
stage_moc: "[[🧭 阶段4-变分方法与应用]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: ["Sobolev空间", "弱导数", "Poincare不等式", "Sobolev嵌入", "Rellich-Kondrachov定理", "临界指数", "GNS不等式"]
prerequisites: ["弱收敛与Banach-Alaoglu定理", "实分析Lp空间与Holder不等式"]
upstream: ["[[泛函分析-弱收敛与Banach-Alaoglu定理]]", "[[泛函分析-前置-实分析Lp空间与Holder不等式]]"]
source: "Haim Brezis, Functional Analysis, Sobolev Spaces and PDEs, Chapter 8 & 9; MIT 18.102 Lec 16"
source_url: "https://link.springer.com/book/10.1007/978-0-387-70914-7"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0"
tags: [学习, 数学, 泛函分析, Sobolev空间, 弱导数, 紧嵌入, PDE, GNS不等式]
proof_mode: true
---

# 泛函分析-Sobolev空间与嵌入定理

> 所属阶段：[[🧭 阶段4-变分方法与应用|第四阶段：变分方法与应用]]
> 目标：掌握分部积分弱导数定义、Sobolev 空间 $H^1(\Omega)$ 与 $H_0^1(\Omega)$ 结构、一维 Poincaré 不等式无跳步推导、GNS 临界指数量纲缩放与 Rellich 紧嵌入定理。

---

## 0. 知识定位与不可微函数的微积分

### 1. 为什么经典导数无法满足现代偏微分方程？
经典微分方程要求解具有连续二阶导数（$u \in C^2$）。但在物理实际中，介质界面、点载荷、折角边界处函数的经典导数根本不存在（例如折线函数 $u(x) = 1 - |x|$ 在 $x=0$ 处不可微）。
然而从物理能量角度看，弹性形变能量 $\int_{-1}^1 |u^\prime|^2 dx = 2 < \infty$ 完全有限且守恒！
**Sobolev 空间通过“分部积分对偶测试”定义了弱导数**：
- 把处处可导的苛刻要求转化为加权测试函数积分；
- 赋予不可微但具有有限能量的函数完备的 Hilbert 空间结构（$H^1(\Omega)$）；
- 通过 **Sobolev 嵌入与 Rellich 紧嵌入**，把导数的可积性无损转化为函数的高阶连续性或强紧性。

---

## 1. 核心定义：弱导数与 Sobolev 空间

### 1. 弱导数 (Weak Derivative)
设 $\Omega \subset \mathbb{R}^d$ 为开集，$u \in L_{\text{loc}}^1(\Omega)$。
若存在局部可积函数 $v \in L_{\text{loc}}^1(\Omega)$，使得对**所有光滑紧支集测试函数 $\varphi \in C_c^\infty(\Omega)$**，均满足：
$$\int_\Omega u(x) \frac{\partial \varphi}{\partial x_i}(x) dx = - \int_\Omega v(x) \varphi(x) dx$$
则称 $v$ 为 $u$ 关于 $x_i$ 的**弱导数**，记作 $\partial_{x_i} u = v$。

### 2. Sobolev 空间 $H^1(\Omega)$ 与零迹空间 $H_0^1(\Omega)$
1. **$H^1(\Omega)$ 空间**：
   $$H^1(\Omega) = \left\{ u \in L^2(\Omega) \ \middle|\ \nabla u \in (L^2(\Omega))^d \right\}$$
   赋内积 $\langle u, v \rangle_{H^1} = \int_\Omega [uv + \nabla u \cdot \nabla v] dx$，构成**完备的 Hilbert 空间**。
2. **$H_0^1(\Omega)$ 空间 (零边界迹空间)**：
   $$H_0^1(\Omega) = \overline{C_c^\infty(\Omega)}^{\|\cdot\|_{H^1}} = \{ u \in H^1(\Omega) \mid \gamma(u) = 0 \text{ in } L^2(\partial\Omega) \}$$

---

## 2. 核心定理：Poincaré 不等式与 Sobolev 嵌入

### 1. Poincaré 不等式 (一维手把手推导)
**定理**：对任意 $u \in H_0^1(0, L)$，均有 $\|u\|_{L^2(0, L)} \le L \|u^\prime\|_{L^2(0, L)}$。
*推论*：在 $H_0^1(\Omega)$ 上，半范数 $\|u\|_{H_0^1} = \|\nabla u\|_{L^2}$ 与全范数 $\|u\|_{H^1}$ 是**等价范数**！

**推导过程**：
1. 对 $u \in C_c^\infty(0, L)$，由微积分基本定理：$u(x) = \int_0^x u^\prime(t) dt$。
2. 由 Cauchy-Schwarz 不等式：
   $$|u(x)|^2 = \left| \int_0^x 1 \cdot u^\prime(t) dt \right|^2 \le \left(\int_0^x 1^2 dt\right) \left(\int_0^x |u^\prime(t)|^2 dt\right) \le x \int_0^L |u^\prime(t)|^2 dt \le L \|u^\prime\|_{L^2}^2$$
3. 两边对 $x \in (0, L)$ 积分：$\int_0^L |u(x)|^2 dx \le L^2 \|u^\prime\|_{L^2}^2$。
4. 开平方即得 $\|u\|_{L^2} \le L \|u^\prime\|_{L^2}$。由稠密性直接延拓至全空间 $H_0^1(0, L)$。证毕！

---

### 2. GNS 临界指数的量纲缩放分析 (Dimensional Scaling)
为什么当 $d \ge 3$ 时临界指数恰为 $2^* = \frac{2d}{d-2}$？
- 考虑空间缩放变换 $u_\lambda(x) = u(\lambda x) \ (\lambda > 0)$。
- 计算左边：$\|u_\lambda\|_{L^q} = \lambda^{-d/q} \|u\|_{L^q}$；
- 计算右边：$\|\nabla u_\lambda\|_{L^p} = \lambda^{1 - d/p} \|\nabla u\|_{L^p}$；
- 要使不等式 $\|u_\lambda\|_{L^q} \le C \|\nabla u_\lambda\|_{L^p}$ 对所有尺度 $\lambda > 0$ 恒成立，幂次必须严格相等：
  $$-\frac{d}{q} = 1 - \frac{d}{p} \implies \frac{1}{q} = \frac{1}{p} - \frac{1}{d}$$
  当 $p = 2$ 时，代入即得：$\frac{1}{2^*} = \frac{1}{2} - \frac{1}{d} = \frac{d-2}{2d} \implies 2^* = \frac{2d}{d-2}$！

---

### 3. Rellich-Kondrachov 紧嵌入定理
**定理**：设 $\Omega \subset \mathbb{R}^d$ 是有界 Lipschitz 区域。对任意次临界指数 $1 \le q < 2^*$：
$$H^1(\Omega) \Subset L^q(\Omega)$$
即：$H^1(\Omega)$ 中的任意有界序列必定包含在 $L^q(\Omega)$ 中**强收敛的子序列**！

---

## 3. 经典反例与认知对抗

### 反例 1：跳跃阶梯函数无 $L_{\text{loc}}^1$ 弱导数（Dirac $\delta$ 危机）
- **函数**：Heaviside 阶梯函数 $H(x) = \mathbf{1}_{[0, 1]}(x)$ 在 $(-1, 1)$ 上。
- **失效分析**：若存在弱导数 $v \in L_{\text{loc}}^1$，分部积分导致要求 $\int_{-1}^1 v \varphi = \varphi(0)$。由 Lebesgue 积分绝对连续性在单点测度为 0 处积分必为 0，导致矛盾。
- **结论**：**跳跃间断点只能在广义函数/分布意义下求导为 $\delta(x)$，绝不属于任何 Sobolev 空间 $W^{1,p}$！**

---

## 4. 闭卷自测与练习

- [ ] 能一字不差默写弱导数的分部积分测试定义。
- [ ] 能在草稿纸上利用 Cauchy-Schwarz 独立推导一维 Poincaré 不等式。
- [ ] 能利用尺度伸缩变换 $\lambda$ 推导 GNS 临界指数公式 $\frac{1}{2^*} = \frac{1}{2} - \frac{1}{d}$。

---

## 🃏 Anki 卡片

TARGET DECK: 泛函分析::04-变分方法与应用

Q: 什么是函数的弱导数 (Weak Derivative)？
A: 
设 $u, v \in L_{\text{loc}}^1(\Omega)$。若对任意光滑紧支测试函数 $\varphi \in C_c^\infty(\Omega)$，均满足分部积分等式：
$$\int_\Omega u(x) \frac{\partial \varphi}{\partial x_i}(x) dx = - \int_\Omega v(x) \varphi(x) dx$$
则称 $v$ 为 $u$ 关于 $x_i$ 的**弱导数**。
<!--ID: 1723180000027-->

Q: 叙述 Rellich-Kondrachov 紧嵌入定理及其在偏微分方程中的核心作用。
A: 
设 $\Omega \subset \mathbb{R}^d$ 为有界光滑区域。对任意次临界指数 $1 \le q < 2^* = \frac{2d}{d-2}$，Sobolev 空间 $H^1(\Omega)$ **紧嵌入**到 $L^q(\Omega)$ 中（$H^1(\Omega) \Subset L^q(\Omega)$）。
作用：它能将弱解极小化序列在 $H^1$ 中的弱收敛性转化为在 $L^q$ 中的**强收敛性**，从而保证非线性项在极限下强连续过渡。
<!--ID: 1723180000028-->

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
