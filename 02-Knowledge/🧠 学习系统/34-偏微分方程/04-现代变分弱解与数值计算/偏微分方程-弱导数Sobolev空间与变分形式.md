---
type: study
topic: "弱导数Sobolev空间与变分形式"
course: "偏微分方程"
created: 2026-08-08
status: completed
stage_moc: "[[🧭 阶段4-现代变分弱解与数值计算]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["弱导数", "Sobolev空间", "Poincare不等式", "变分形式", "检验函数"]
upstream: ["[[偏微分方程-拉普拉斯方程与调和函数性质]]"]
tags: [学习, 偏微分方程, 弱导数, Sobolev空间, 泛函分析, 变分法]
---

# 弱导数 Sobolev 空间与变分形式

> 所属阶段 MOC：[[04-现代变分弱解与数值计算/🧭 阶段4-现代变分弱解与数值计算|🧭 阶段 4：现代变分弱解与数值计算]]  
> 学习定位：从经典逐点微分跨入现代泛函分析视角，掌握检验函数分部积分定义的弱导数、Sobolev 希尔伯特空间 $H^1(\Omega)$、$H_0^1(\Omega)$、Poincaré 不等式与弱变分形式。

---

## 1. 核心问题与物理直觉

经典微积分要求微分方程中所有导数逐点存在且连续（$u \in C^2$）。但在物理实际中：
- 复合材料截面上的热导率是间断跳跃的；
- 集中点力作用下的弹性膜在受力点导数不连续；
- 流体激波前后速度场存在跳变。
在这些情况下，$u \notin C^2$ 并不意味着物理定律失效。现代偏微分方程通过引入光滑紧支集**检验函数 $\phi \in C_c^\infty(\Omega)$**，利用分部积分将导数从未知解“转移”到极其光滑的检验函数上，从而定义了**弱导数 (Weak Derivative)**。

---

## 2. 正式数学表述与 Sobolev 空间理论

### 2.1 弱导数严格定义 (Weak Derivative)
设 $u, v \in L_{loc}^1(\Omega)$，$\alpha = (\alpha_1, \dots, \alpha_n)$ 为多重指标，$|\alpha| = \sum \alpha_i$。
若对任意光滑紧支集测试函数 $\phi \in C_c^\infty(\Omega)$，均满足：
$$\int_\Omega u D^\alpha \phi \, dx = (-1)^{|\alpha|} \int_\Omega v \phi \, dx$$
则称 $v$ 为 $u$ 的 **$\alpha$ 阶弱偏导数**，记作 $D^\alpha u = v$。
*唯一性*：若弱导数存在，则在几乎处处（$L^1$ 空间）意义下唯一。

### 2.2 Sobolev 空间 $H^1(\Omega)$ 与 $H_0^1(\Omega)$
1. **$H^1(\Omega)$ 空间**：定义为平方可积且一阶弱偏导数亦平方可积的实 Hilbert 空间：
   $$H^1(\Omega) = W^{1,2}(\Omega) = \left\{ u \in L^2(\Omega) : \frac{\partial u}{\partial x_i} \in L^2(\Omega), \, i = 1, \dots, n \right\}$$
   内积与诱导范数定义为：
   $$\langle u, v \rangle_{H^1} = \int_\Omega (u v + \nabla u \cdot \nabla v) \, dx, \quad \|u\|_{H^1} = \sqrt{\|u\|_{L^2}^2 + \|\nabla u\|_{L^2}^2}$$
2. **$H_0^1(\Omega)$ 空间（零边界迹空间）**：
   $$H_0^1(\Omega) = \overline{C_c^\infty(\Omega)}^{\|\cdot\|_{H^1}}$$
   代表在边界 $\partial \Omega$ 上具有零 Dirichlet 迹值的 Sobolev 函数空间。

### 2.3 庞加莱不等式 (Poincaré Inequality)
设 $\Omega \subset \mathbb{R}^n$ 为有界开区域。则存在仅依赖于 $\Omega$ 的正常数 $C_\Omega > 0$，使得对任意 $u \in H_0^1(\Omega)$ 均成立：
$$\|u\|_{L^2(\Omega)} \le C_\Omega \|\nabla u\|_{L^2(\Omega)}$$
*重要结论*：在 $H_0^1(\Omega)$ 空间上，半范数 $|u|_{H^1} = \|\nabla u\|_{L^2}$ 与全范数 $\|u\|_{H^1}$ **严格等价**。

### 2.4 Poisson 方程的弱变分形式推导
考虑经典 Dirichlet 问题：$-\Delta u = f \text{ in } \Omega, \, u|_{\partial \Omega} = 0$。
1. 任取测试函数 $v \in H_0^1(\Omega)$，两端同乘 $v$ 并在 $\Omega$ 上积分：
   $$\int_\Omega (-\Delta u) v \, dx = \int_\Omega f v \, dx$$
2. 应用 Green 第一恒等式（分部积分）：
   $$\int_\Omega \nabla u \cdot \nabla v \, dx - \oint_{\partial \Omega} \frac{\partial u}{\partial n} v \, dS = \int_\Omega f v \, dx$$
3. 因 $v \in H_0^1(\Omega)$，边界项 $\oint_{\partial \Omega} = 0$。
4. **弱变分问题**：求 $u \in H_0^1(\Omega)$，使得对所有 $v \in H_0^1(\Omega)$ 均满足：
   $$a(u, v) = \ell(v), \quad \text{其中 } a(u, v) = \int_\Omega \nabla u \cdot \nabla v \, dx, \quad \ell(v) = \int_\Omega f v \, dx$$

---

## 3. 典型例题与经典反例

### 【例 1：经典有弱导数案例】
考察一维折线函数 $u(x) = 1 - |x|, x \in (-1, 1)$。
- 经典导数在 $x = 0$ 处不存在。
- 检验弱导数候选 $v(x) = -\text{sgn}(x) = \begin{cases} 1, & x < 0 \\ -1, & x > 0 \end{cases}$。
- 对任意 $\phi \in C_c^\infty(-1, 1)$：
  $$\int_{-1}^1 u \phi' dx = \int_{-1}^0 (1+x)\phi' dx + \int_0^1 (1-x)\phi' dx = [(1+x)\phi]_{-1}^0 - \int_{-1}^0 \phi dx + [(1-x)\phi]_0^1 + \int_0^1 \phi dx$$
  $= \phi(0) - \int_{-1}^0 \phi dx - \phi(0) + \int_0^1 \phi dx = -\int_{-1}^1 v \phi dx$。
- 因此 $u$ 的一阶弱导数存在且为 $v(x) \in L^2(-1, 1)$，故 $u \in H^1(-1, 1)$。

### 【例 2：无弱导数反例】
考察阶跃函数（Heaviside）$u(x) = H(x) = \begin{cases} 0, & x < 0 \\ 1, & x > 0 \end{cases}$。
- 若存在弱导数 $v \in L_{loc}^1(-1, 1)$，则需满足 $\int_{-1}^1 H \phi' dx = -\int_{-1}^1 v \phi dx$。
- 左侧 $\int_0^1 \phi' dx = \phi(1) - \phi(0) = -\phi(0)$。
- 这要求对任意 $\phi$ 成立 $\int_{-1}^1 v(x) \phi(x) dx = \phi(0)$。
- 众所周知，Dirac $\delta$ 广义函数无法由任何实可积函数 $v \in L_{loc}^1$ 生成。因此阶跃函数在常规 Sobolev 空间 $H^1$ 中**不存在弱导数**。

---

## 4. 常见误区与反例

- **误区 1：认为只要几乎处处有导数就存在弱导数**。著名的 Cantor 阶梯函数几乎处处导数为 0，但如果对其求分布导数，会得到集中在 Cantor 集合上的奇异测度，并不满足弱导数定义。
- **误区 2：在非零边界问题中误用 $H_0^1(\Omega)$**。若边界为非齐次 Dirichlet 条件 $u|_{\partial\Omega} = g \neq 0$，解所在的空间是仿射子空间 $u \in g_0 + H_0^1(\Omega)$，其中 $g_0 \in H^1(\Omega)$ 为边界数据的 $H^1$ 延拓，而测试函数空间 $v$ 仍必须属于齐次的 $H_0^1(\Omega)$。

---

## 5. 主动自测与闭卷检查

- [ ] 我能准确写出弱导数的多重指标检验积分定义。
- [ ] 我能利用微积分基本定理证明一维有界区间上的 Poincaré 不等式 $\|u\|_{L^2} \le L \|u'\|_{L^2}$。
- [ ] 我能不看书完整推导出 Poisson 方程的双线性形式 $a(u, v) = \ell(v)$。

---

## 6. 学完后可以完成（派生视图）

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
