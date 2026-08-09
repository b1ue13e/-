---
type: study
topic: "一阶拟线性PDE与特征线法"
course: "偏微分方程"
created: 2026-08-08
status: completed
stage_moc: "[[🧭 阶段1-经典方程与特征线法]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["一阶拟线性方程", "特征线法", "Cauchy问题", "激波"]
upstream: ["[[偏微分方程-前置基础-常微分方程与线性代数]]"]
tags: [学习, 偏微分方程, 特征线, 一阶PDE, 激波]
---

# 一阶拟线性 PDE 与特征线法

> 所属阶段 MOC：[[01-经典方程与特征线法/🧭 阶段1-经典方程与特征线法|🧭 阶段 1：经典方程与特征线法]]  
> 学习定位：掌握一阶偏微分方程沿特征方向降维为 ODE 的核心解析技术，建立波的传播与激波非线性奇点直觉。

---

## 1. 核心问题与物理直觉

一阶偏微分方程（如连续性方程、流体输运方程、交通流模型）描述的是某种物理量（密度、浓度、速度）在空间流场中的对流输运。
对于偏微分方程 $a u_x + b u_y = c$，我们发现左侧正是解曲面 $z = u(x,y)$ 上的方向导数。只要我们沿着切向量为 $(a, b, c)$ 的空间特征曲线运动，偏微分方程就退化为一个纯粹的**常微分方程组（特征线 ODE）**。

---

## 2. 正式数学表述与特征线定理

### 2.1 一阶拟线性 PDE 与 Cauchy 问题
考虑一般二维一阶拟线性 PDE：
$$a(x, y, u)\frac{\partial u}{\partial x} + b(x, y, u)\frac{\partial u}{\partial y} = c(x, y, u)$$
给定初始 Cauchy 数据曲线 $\Gamma$:
$$x = x_0(s), \quad y = y_0(s), \quad u = u_0(s), \quad s \in I$$

### 2.2 特征方程组 (Characteristic ODEs)
定义参数 $t$ 为沿特征线的传播时间，特征方程组为：
$$\frac{dx}{dt} = a(x, y, u), \quad \frac{dy}{dt} = b(x, y, u), \quad \frac{du}{dt} = c(x, y, u)$$
其初始条件为：$x(s, 0) = x_0(s), \, y(s, 0) = y_0(s), \, u(s, 0) = u_0(s)$。

### 2.3 局部唯一解存在定理与非退化条件 (Jacobian Transversality)
设 $a, b, c$ 在初值曲线附近连续可微。若初始曲线与特征方向在 $t=0$ 处处不相切，即满足**横截条件（Transversality Condition）**：
$$J = \det \left.\begin{pmatrix} \frac{\partial x}{\partial s} & \frac{\partial y}{\partial s} \\ \frac{\partial x}{\partial t} & \frac{\partial y}{\partial t} \end{pmatrix}\right|_{t=0} = x_0'(s)b(x_0(s), y_0(s), u_0(s)) - y_0'(s)a(x_0(s), y_0(s), u_0(s)) \neq 0$$
则由隐函数定理，映射 $(s, t) \mapsto (x, y)$ 在 $\Gamma$ 邻域内可逆，存在唯一的局部严格经典解 $u(x, y) = u(s(x,y), t(x,y))$。

---

## 3. 经典非线性输运：无粘 Burgers 方程与激波

考虑模型方程：
$$u_t + u u_x = 0, \quad u(x, 0) = u_0(x)$$
- 特征方程为：$\frac{dt}{d\tau} = 1, \, \frac{du}{d\tau} = 0, \, \frac{dx}{d\tau} = u$。
- 解得：$u(x, t) = u_0(s)$ 沿直线 $x = s + u_0(s)t$ 保持为常数。
- **梯度突变与激波形成时间**：对解求导得 $u_x(x,t) = \frac{u_0'(s)}{1 + t u_0'(s)}$。
  若初始剖面存在压缩区（即存在 $s$ 使得 $u_0'(s) < 0$），则特征线必将在有限时间相交，首次破裂时间（Gradient Catastrophe Time）为：
  $$T_b = \frac{1}{\max(-u_0'(s))}$$
  破裂后经典导数不复存在，必须引入弱解并满足 **Rankine-Hugoniot 跳跃条件**：激波传播速度为 $s = \frac{u_L + u_R}{2}$。

---

## 4. 典型例题与推导演练

### 【例题】求解线性变系数 Cauchy 问题
求解方程：$x u_x + y u_y = 2u$，初值条件为 $u(x, 1) = x^3$ ($x > 0$)。

**求解步骤**：
1. **参数化初值曲线**：设 $s \in (0, \infty)$，初值为 $x_0(s) = s, \, y_0(s) = 1, \, u_0(s) = s^3$。
2. **写出特征方程组并求解**：
   - $\frac{dx}{dt} = x \implies x(s, t) = s e^t$
   - $\frac{dy}{dt} = y \implies y(s, t) = 1 \cdot e^t = e^t$
   - $\frac{du}{dt} = 2u \implies u(s, t) = s^3 e^{2t}$
3. **检验横截条件**：
   $$J = x_0'(s)b - y_0'(s)a = 1 \cdot y_0(s) - 0 \cdot x_0(s) = 1 \neq 0$$
   处处非退化，全局可逆。
4. **反解参数 $(s, t)$**：
   由 $y = e^t \implies e^t = y$，代入 $x = s y \implies s = \frac{x}{y}$。
5. **写出最终解析解**：
   $$u(x, y) = \left(\frac{x}{y}\right)^3 \cdot y^2 = \frac{x^3}{y}$$
6. **验算**：$x u_x + y u_y = x\left(\frac{3x^2}{y}\right) + y\left(-\frac{x^3}{y^2}\right) = \frac{3x^3}{y} - \frac{x^3}{y} = \frac{2x^3}{y} = 2u$。且 $u(x, 1) = x^3$。完全正确。

---

## 5. 常见误区与反例

- **误区 1：忽略横截性条件导致解不存在或不唯一**。若特征线恰好与初始曲线相切（$J = 0$），初值不能任意给定；若初值不满足特征相容性，方程在该点无解；若满足相容性，则存在无穷多解。
- **误区 2：以为线性方程也会产生激波**。激波是**非线性效应**（如对流速度 $u$ 自身依赖于振幅，导致大振幅波速更快追上小振幅）。常系数或仅依赖于 $(x,y)$ 的线性方程特征线永不相交，不会出现激波破裂。

---

## 6. 主动自测与闭卷检查

- [ ] 我能不看书写出一阶拟线性特征线 ODE 方程组及其横截条件。
- [ ] 我能根据初值导数的负极大值计算无粘 Burgers 方程的激波形成时间 $T_b$。
- [ ] 我能独立完成变系数 Cauchy 问题从参数化到隐式反解的全过程。

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
