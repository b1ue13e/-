---
type: study
topic: "Green函数与基本解积分表示"
course: "偏微分方程"
created: 2026-08-08
status: completed
stage_moc: "[[🧭 阶段3-调和函数与Green方法]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: ["基本解", "Green函数", "Green第二恒等式", "镜像法", "Poisson积分公式"]
upstream: ["[[偏微分方程-拉普拉斯方程与调和函数性质]]"]
tags: [学习, 偏微分方程, Green函数, 镜像法, Poisson核, 积分表示]
---

# Green 函数与基本解积分表示

> 所属阶段 MOC：[[03-调和函数与Green方法/🧭 阶段3-调和函数与Green方法|🧭 阶段 3：调和函数与Green方法]]  
> 学习定位：掌握 Laplace 算子基本解的构造性推导，运用 Green 恒等式建立非齐次 Poisson 边值问题的积分表示，通过上半平面与球域镜像法推导著名的 Poisson 积分公式。

---

## 1. 核心问题与物理直觉

对于代数方程 $A x = b$，求解是乘以逆矩阵 $x = A^{-1}b$。
对于偏微分方程 $-\Delta u = f$，微分算子 $-\Delta$ 在无穷维空间中的逆算子就是一个**积分核算子**：
$$u(x) = \int_\Omega G(x, y) f(y) \, dy + \text{边界修正项}$$
这个积分核 $G(x, y)$ 就是 **Green 函数**。它在物理上代表：在点 $y$ 处施加一个点电荷或集中点热源 $\delta(x - y)$ 时，在全场 $x$ 处产生的势响应，并且要求该响应在物理接地的导体边界 $\partial \Omega$ 上精准归零。

---

## 2. 正式数学表述与基本解

### 2.1 拉普拉斯算子的基本解 (Fundamental Solution)
寻找关于原点径向对称的解 $\Delta \Phi(x) = 0 \, (x \neq 0)$，令 $r = |x|$，方程化为：
$$\Phi''(r) + \frac{n-1}{r}\Phi'(r) = 0 \implies \Phi'(r) = \frac{C}{r^{n-1}}$$
积分并选取标准归一化常数（使 $-\Delta \Phi = \delta(0)$）：
$$\Phi(x) = \begin{cases} -\frac{1}{2\pi} \ln|x|, & n = 2 \\ \frac{1}{n(n-2)\alpha_n |x|^{n-2}} = \frac{1}{4\pi |x|}, & n = 3 \end{cases}$$

### 2.2 Green 函数的定义与边界修正
设 $\Omega \subset \mathbb{R}^n$ 为光滑有界区域。固定源点 $x \in \Omega$，$y \in \Omega$ 处的 Green 函数 $G(x, y)$ 定义为：
$$G(x, y) = \Phi(y - x) - \phi^x(y)$$
其中修正位势 $\phi^x(y)$ 是消除奇异项边界残差的正则调和函数：
$$\begin{cases} \Delta_y \phi^x(y) = 0, & y \in \Omega \\ \phi^x(y) = \Phi(y - x), & y \in \partial \Omega \end{cases}$$
显然在边界上，对任意 $y \in \partial \Omega$，满足 $G(x, y) = 0$。

### 2.3 Poisson-Dirichlet 边值问题的积分表示定理
若 $u \in C^2(\bar{\Omega})$ 满足 Dirichlet 边值问题：
$$\begin{cases} -\Delta u = f(x), & x \in \Omega \\ u(x) = g(x), & x \in \partial \Omega \end{cases}$$
则解可唯一显式表示为：
$$u(x) = \int_\Omega G(x, y) f(y) \, dy - \oint_{\partial \Omega} g(y) \frac{\partial G}{\partial n_y}(x, y) \, dS(y)$$

---

## 3. 经典镜像法 (Method of Images) 构造与 Poisson 积分公式

### 3.1 上半空间 $\mathbb{R}_+^n = \{ (x', x_n) : x_n > 0 \}$
- **构造镜像源**：设点 $x = (x', x_n)$，其关于边界平面 $x_n = 0$ 的镜像点为 $\tilde{x} = (x', -x_n)$。
- **Green 函数构造**：
  $$G(x, y) = \Phi(y - x) - \Phi(y - \tilde{x})$$
  当 $y \in \partial \mathbb{R}_+^n$（即 $y_n = 0$）时，$|y - x| = |y - \tilde{x}|$，故 $G(x, y) \equiv 0$。
- **法向导数（Poisson 核）**：
  $$K(x, y) = -\frac{\partial G}{\partial n_y}(x, y) = \left.\frac{\partial G}{\partial y_n}\right|_{y_n=0} = \frac{2 x_n}{n \alpha_n |x - y|^n}$$
- **二维上半平面 Poisson 积分公式** ($n = 2, \alpha_2 = \pi$)：
  $$u(x_1, x_2) = \frac{x_2}{\pi} \int_{-\infty}^\infty \frac{g(y_1)}{(x_1 - y_1)^2 + x_2^2} \, dy_1$$

### 3.2 单位球域 $B_1(0) = \{ x \in \mathbb{R}^n : |x| < 1 \}$
- **几何反演点 (Kelvin Inversion)**：对 $x \in B_1(0) \setminus \{0\}$，其关于单位球面的反演镜像点为 $x^* = \frac{x}{|x|^2}$。
- **球域 Green 函数**：
  $$G(x, y) = \Phi(y - x) - \Phi(|x|(y - x^*))$$
- **单位圆盘 Poisson 积分公式**（极坐标 $x = (r, \theta), y = (1, \phi)$）：
  $$u(r, \theta) = \frac{1 - r^2}{2\pi}\int_0^{2\pi} \frac{g(\phi)}{1 - 2r\cos(\theta - \phi) + r^2} \, d\phi$$

---

## 4. 常见误区与反例

- **误区 1：在 Green 恒等式中忽略外法向 $\mathbf{n}$ 与求导变量的关系**。泊松核定义中的法向导数是关于积分变量 $y$ 求外法向导数 $\frac{\partial G}{\partial n_y} = \nabla_y G \cdot \mathbf{n}_y$。若错对源点 $x$ 求导，会得到完全错误的核符号与维度。
- **误区 2：以为任意几何区域都能用初等镜像法构造 Green 函数**。镜像法要求区域边界具有高度几何对称性（半空间、全平面楔形角域、球域）。对于一般复杂多边形或非凸区域，Green 函数不存在初等解析表达式，必须依赖数值有限元或保角映射求解。

---

## 5. 主动自测与闭卷检查

- [ ] 我能从径向对称假设独立推导二维与三维 Laplace 算子基本解。
- [ ] 我能默写上半空间的 Green 函数并求导推导出上半平面的 Poisson 积分核。
- [ ] 我能说明 Green 函数的对称性 $G(x, y) = G(y, x)$ 其背后的物理互易定理依据。

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
