---
type: study
topic: "分离变量法与Sturm-Liouville理论"
course: "偏微分方程"
created: 2026-08-08
status: completed
stage_moc: "[[🧭 阶段2-分离变量与积分变换]]"
flow: knowledge
kind: derivation
difficulty: intermediate
concept: ["分离变量法", "Sturm-Liouville理论", "特征值问题", "自伴算子", "正交基展开"]
upstream: ["[[偏微分方程-前置基础-常微分方程与线性代数]]", "[[偏微分方程-一维波动方程与达朗贝尔公式]]"]
tags: [学习, 偏微分方程, 分离变量, Sturm-Liouville, 正交展开]
---

# 分离变量法与 Sturm-Liouville 理论

> 所属阶段 MOC：[[02-分离变量与积分变换/🧭 阶段2-分离变量与积分变换|🧭 阶段 2：分离变量与积分变换]]  
> 学习定位：掌握线性偏微分方程在规则有界区域上的核心解析拆解技术，深入理解 Sturm-Liouville 微分算子的自伴性、实特征值谱系与广义 Fourier 级数完全性。

---

## 1. 核心问题与物理直觉

对于有界区域（如两端固定的弦、有限长绝热金属棒、矩形膜），波与热流会在边界处反复反射形成**驻波（Standing Waves）或本征衰减模态**。
分离变量法假设解可以写成时间函数与空间函数的乘积 $u(x, t) = X(x)T(t)$。将时空解耦后，空间方向退化为一个常微分方程特征值问题。这在无穷维函数空间中对应于寻找自伴微分算子的主轴基向量（特征基展开）。

---

## 2. 正式数学表述与 Sturm-Liouville 定理

### 2.1 正规 Sturm-Liouville 边值问题
设 $p(x) \in C^1[a, b], p(x) > 0, q(x) \in C[a, b], w(x) \in C[a, b], w(x) > 0$。在区间 $[a, b]$ 上考虑微分方程：
$$L[y] = -\frac{d}{dx}\left[ p(x)\frac{dy}{dx} \right] + q(x)y = \lambda w(x)y$$
满足自伴分立边界条件（Robin/Dirichlet/Neumann）：
$$\alpha_1 y(a) + \alpha_2 y'(a) = 0, \quad \beta_1 y(b) + \beta_2 y'(b) = 0$$

### 2.2 核心定理与谱性质
1. **微分算子的自伴性 (Self-Adjointness)**：
   在带权内积空间 $L_w^2(a, b)$ 中定义内积 $\langle u, v \rangle_w = \int_a^b u(x)v(x)w(x)dx$。利用两次分部积分：
   $$\int_a^b (u L[v] - v L[u]) \, dx = \left[ p(x)(v u' - u v') \right]_a^b = 0$$
   因此算子 $L$ 在满足边界条件的函数空间上是**自伴（对称）算子**。
2. **特征值的实数性与离散单调性**：
   所有特征值均为实数，且构成一个严格递增的无穷离散序列：
   $$\lambda_1 < \lambda_2 < \dots < \lambda_n \to +\infty$$
3. **特征函数的正交性与简单性 (Orthogonality & Simplicity)**：
   对应不同特征值的特征函数 $\phi_n(x)$ 关于权函数 $w(x)$ 严格正交：
   $$\int_a^b \phi_m(x)\phi_n(x)w(x) \, dx = 0 \quad (m \neq n)$$
   每个特征值 $\lambda_n$ 对应的特征子空间是一维的（单重根），第 $n$ 个特征函数 $\phi_n(x)$ 在开区间 $(a, b)$ 内恰好有 $n-1$ 个零点。
4. **完备性定理 (Completeness in $L_w^2$)**：
   正交特征函数系 $\{\phi_n\}_{n=1}^\infty$ 构成 $L_w^2(a, b)$ 的标准正交基。任意 $f \in L_w^2$ 均可唯一展开为广义傅里叶级数：
   $$f(x) = \sum_{n=1}^\infty c_n \phi_n(x), \quad c_n = \frac{\int_a^b f(x)\phi_n(x)w(x)dx}{\int_a^b \phi_n^2(x)w(x)dx}$$

---

## 3. 典型例题与推导演练

### 【例题】求解两端固定弦振动的分离变量级数解
考虑定解问题：
$$\begin{cases} u_{tt} = c^2 u_{xx}, & x \in (0, L), t > 0 \\ u(0, t) = 0, \quad u(L, t) = 0 \\ u(x, 0) = \phi(x), \quad u_t(x, 0) = \psi(x) \end{cases}$$

**完整推导步骤**：
1. **代入分离变量形式**：令 $u(x, t) = X(x)T(t)$，代入 PDE 得：
   $$\frac{T''(t)}{c^2 T(t)} = \frac{X''(x)}{X(x)} = -\lambda \quad (\text{分离常数})$$
2. **解空间方向 Sturm-Liouville 特征值问题**：
   $$X''(x) + \lambda X(x) = 0, \quad X(0) = 0, \, X(L) = 0$$
   求得非平凡解存在当且仅当 $\lambda_n = \left(\frac{n\pi}{L}\right)^2$，对应正交特征基为：
   $$X_n(x) = \sin\left(\frac{n\pi x}{L}\right), \quad n = 1, 2, 3, \dots$$
3. **求解时间常微分方程**：
   $$T_n''(t) + \left(\frac{n\pi c}{L}\right)^2 T_n(t) = 0 \implies T_n(t) = A_n \cos\left(\frac{n\pi c t}{L}\right) + B_n \sin\left(\frac{n\pi c t}{L}\right)$$
4. **线性叠加构造通解**：
   $$u(x, t) = \sum_{n=1}^\infty \left[ A_n \cos\left(\frac{n\pi c t}{L}\right) + B_n \sin\left(\frac{n\pi c t}{L}\right) \right] \sin\left(\frac{n\pi x}{L}\right)$$
5. **匹配初值 Fourier 系数**：
   - $u(x, 0) = \sum_{n=1}^\infty A_n \sin\left(\frac{n\pi x}{L}\right) = \phi(x) \implies A_n = \frac{2}{L}\int_0^L \phi(x)\sin\left(\frac{n\pi x}{L}\right)dx$
   - $u_t(x, 0) = \sum_{n=1}^\infty B_n \left(\frac{n\pi c}{L}\right)\sin\left(\frac{n\pi x}{L}\right) = \psi(x) \implies B_n = \frac{2}{n\pi c}\int_0^L \psi(x)\sin\left(\frac{n\pi x}{L}\right)dx$

---

## 4. 常见误区与反例

- **误区 1：认为所有边界条件都能直接套用正弦级数**。若边界为绝热 Neumann 条件 $u_x(0,t)=0, u_x(L,t)=0$，空间特征基必为**余弦基 $\cos(n\pi x/L)$** 且包含常数零模态 $\lambda_0 = 0$。盲目套用正弦会导致边界条件与函数展开矛盾。
- **误区 2：忽视齐次边界条件前提**。分离变量法要求空间边界条件**必须是齐次的**。若出现非齐次边界（如 $u(0,t) = T_1, u(L,t) = T_2$），必须先构造稳态线性背景解 $u_0(x) = T_1 + \frac{T_2-T_1}{L}x$ 予以平移消去，转化为关于扰动量 $v = u - u_0$ 的齐次边值问题后再分离变量。

---

## 5. 主动自测与闭卷检查

- [ ] 我能写出 Sturm-Liouville 算子的标准形式并利用分部积分证明其自伴对称性。
- [ ] 我能不看书完整推导两端固定弦振动的分离变量通解及 Fourier 展开系数。
- [ ] 我能说明非齐次边界条件如何通过稳态平移转化为齐次边值问题。

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
