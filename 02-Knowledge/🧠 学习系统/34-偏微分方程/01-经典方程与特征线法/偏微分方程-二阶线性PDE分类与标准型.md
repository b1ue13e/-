---
type: study
topic: "二阶线性PDE分类与标准型"
course: "偏微分方程"
created: 2026-08-08
status: completed
stage_moc: "[[🧭 阶段1-经典方程与特征线法]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["二阶PDE分类", "判别式", "标准型", "Hadamard适定性"]
upstream: ["[[偏微分方程-一阶拟线性PDE与特征线法]]"]
tags: [学习, 偏微分方程, 分类, 标准型, 适定性, 判别式]
---

# 二阶线性 PDE 分类与标准型

> 所属阶段 MOC：[[01-经典方程与特征线法/🧭 阶段1-经典方程与特征线法|🧭 阶段 1：经典方程与特征线法]]  
> 学习定位：建立二阶偏微分方程的主部分类体系（双曲/抛物/椭圆），掌握坐标变换化为标准型的通用代数算法，理解 Hadamard 适定性三要素。

---

## 1. 核心问题与物理直觉

二阶偏微分方程是物理世界中最常见的动力学与稳态场方程（波动方程、热传导方程、引力与静电位势方程）。
为什么波动方程 $u_{tt} - c^2 u_{xx} = 0$ 表现出局域波包的以固定速度传播，热方程 $u_t - k u_{xx} = 0$ 表现出无穷速度的平滑耗散，而 Laplace 方程 $u_{xx} + u_{yy} = 0$ 表现出边界决定的内部无限光滑平衡态？
根本原因在于方程**二阶最高阶导数主部（Principal Part）的代数判别式几何符号**。

---

## 2. 正式数学表述与分类定理

### 2.1 二维一般二阶线性偏微分方程
考虑方程：
$$A(x,y)u_{xx} + 2B(x,y)u_{xy} + C(x,y)u_{yy} + D(x,y)u_x + E(x,y)u_y + F(x,y)u = G(x,y)$$
其特征二次型矩阵为 $M = \begin{pmatrix} A & B \\ B & C \end{pmatrix}$，定义判别式：
$$\Delta(x,y) = B^2(x,y) - A(x,y)C(x,y) = -\det(M)$$

### 2.2 经典三类方程严格判定与标准型

| 类型 | 判别式条件 | 特征方程特征根 $\frac{dy}{dx} = \frac{B \pm \sqrt{\Delta}}{A}$ | 物理原型 | 典型标准型（规范形式） | 定解性质 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **双曲型 (Hyperbolic)** | $\Delta > 0$ | 存在 2 条互异实特征线族 $\xi(x,y)=C_1, \eta(x,y)=C_2$ | 波动方程 $u_{tt} - c^2 u_{xx} = 0$ | $u_{\xi\eta} = \dots$ 或 $u_{\alpha\alpha} - u_{\beta\beta} = \dots$ | 具有因果性，有限传播速度，允许弱奇异性沿特征线传播 |
| **抛物型 (Parabolic)** | $\Delta = 0$ | 仅有 1 条实特征线族 $\xi(x,y)=C$ | 热传导方程 $u_t - k u_{xx} = 0$ | $u_{\eta\eta} = \dots$ | 单向时间演化，耗散性，瞬时无限平滑，不可时间逆推 |
| **椭圆型 (Elliptic)** | $\Delta < 0$ | 无实特征根（共轭复特征线） | 拉普拉斯方程 $u_{xx} + u_{yy} = 0$ | $u_{\alpha\alpha} + u_{\beta\beta} = \dots$ | 空间各向同性，无特征传播，极值原理与内部解析性 |

### 2.3 特征坐标变换算法
引入非退化坐标变换 $\xi = \xi(x,y), \eta = \eta(x,y)$，利用链式法则展开：
- $u_{xx} = u_{\xi\xi}\xi_x^2 + 2u_{\xi\eta}\xi_x\eta_x + u_{\eta\eta}\eta_x^2 + \dots$
- 代入原方程，二阶主部变为：
  $$\tilde{A} u_{\xi\xi} + 2\tilde{B} u_{\xi\eta} + \tilde{C} u_{\eta\eta} + \text{低阶项} = G$$
  其中：
  $$\tilde{A} = A\xi_x^2 + 2B\xi_x\xi_y + C\xi_y^2, \quad \tilde{C} = A\eta_x^2 + 2B\eta_x\eta_y + C\eta_y^2$$
  令 $\tilde{A} = 0, \tilde{C} = 0$ 即可解出特征线常微分方程 $\frac{dy}{dx} = \frac{B \pm \sqrt{B^2-AC}}{A}$。

### 2.4 Hadamard 适定性定义 (Well-Posedness)
一个偏微分方程定解问题（初值或边值）若在某函数空间中被称为 **Hadamard 适定的**，必须同时满足：
1. **存在性 (Existence)**：至少存在一个满足条件的解。
2. **唯一性 (Uniqueness)**：解是唯一的。
3. **连续依赖性 (Stability / Continuous Dependence)**：解连续依赖于初始/边界数据（初值微小扰动 $\epsilon \to 0$ 导致解的扰动在适当范数下亦趋于 $0$）。

---

## 3. 经典反例：Laplace 方程 Cauchy 问题的 Hadamard 病态性

### 【反例构造】证明椭圆方程 Cauchy 问题非适定
考虑上半平面 Laplace 方程的初值问题：
$$\begin{cases} u_{xx} + u_{yy} = 0, & x \in \mathbb{R}, y > 0 \\ u(x, 0) = 0 \\ u_y(x, 0) = \frac{1}{n} \sin(nx) \end{cases}$$
1. **求解解表达式**：
   使用分离变量法易得该问题的精确解为：
   $$u_n(x, y) = \frac{1}{n^2} \sin(nx) \sinh(ny)$$
2. **考察初值扰动**：
   当 $n \to \infty$ 时，初值及其导数在一致模下满足：
   $$\|u_n(x, 0)\|_{L^\infty} = 0, \quad \left\|\frac{\partial u_n}{\partial y}(x, 0)\right\|_{L^\infty} = \frac{1}{n} \to 0$$
   即初值与 0 解极其接近。
3. **考察解的爆炸**：
   对任意固定的 $y > 0$，当 $n \to \infty$ 时：
   $$|u_n(x, y)| = \frac{1}{n^2} |\sin(nx)| \frac{e^{ny} - e^{-ny}}{2} \approx \frac{e^{ny}}{2n^2} \to +\infty$$
4. **结论**：初值无穷小扰动引起了解在任意正时间 $y>0$ 处的指数级爆炸，不满足稳定性。因此**椭圆方程的 Cauchy 问题在 Hadamard 意义下严重病态（Ill-posed）**。椭圆方程必须配以闭合边界上的 Dirichlet/Neumann 边界条件才是适定的。

---

## 4. 典型例题与化简演练

### 【例题】将方程 $u_{xx} - 4u_{xy} - 5u_{yy} = 0$ 化为标准型并求通解
**求解步骤**：
1. **计算判别式**：$A = 1, B = -2, C = -5$。
   $$\Delta = B^2 - AC = (-2)^2 - 1 \cdot (-5) = 4 + 5 = 9 > 0 \implies \text{严格双曲型}$$
2. **求特征线方程**：
   $$\frac{dy}{dx} = \frac{B \pm \sqrt{\Delta}}{A} = \frac{-2 \pm 3}{1} \implies \frac{dy}{dx} = 1 \quad \text{或} \quad \frac{dy}{dx} = -5$$
3. **解特征积分曲线**：
   $$y - x = C_1 \implies \xi = y - x; \quad y + 5x = C_2 \implies \eta = y + 5x$$
4. **标准型化简**：
   经此变换，主部交叉项化简为：
   $$u_{\xi\eta} = 0$$
5. **积分求通解**：
   对 $\xi, \eta$ 依次积分得：
   $$u(\xi, \eta) = f(\xi) + g(\eta) \implies u(x, y) = f(y - x) + g(y + 5x)$$
   其中 $f, g$ 为任意二次可微函数。

---

## 5. 常见误区与反例

- **误区 1：认为变系数方程在全平面属于同一种类型**。例如著名的 Tricomi 方程 $y u_{xx} + u_{yy} = 0$，当 $y > 0$ 时为椭圆型，当 $y < 0$ 时为双曲型，在 $y = 0$ 退化线上为抛物型（跨音速流动的数学模型）。必须局部逐点判断。
- **误区 2：在数值计算中对椭圆方程施加显式时间步进**。由 Hadamard 反例可知，椭圆方程没有时间因果性，不能作为初值问题从一端往前推演，否则数值舍入误差会立即指数爆炸导致溢出 NaN。

---

## 6. 主动自测与闭卷检查

- [ ] 我能准确写出二阶方程判别式公式并独立推导特征线斜率方程。
- [ ] 我能不看笔记复述 Hadamard 适定性三要素。
- [ ] 我能手写推导 Laplace 方程 Cauchy 初值问题的病态解爆炸过程。

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
