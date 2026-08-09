---
type: study
topic: "有限差分法相容性稳定性与Lax等价定理"
course: "偏微分方程"
created: 2026-08-08
status: completed
stage_moc: "[[🧭 阶段4-现代变分弱解与数值计算]]"
flow: knowledge
kind: derivation
difficulty: intermediate
concept: ["有限差分法", "截断误差", "相容性", "von Neumann稳定性", "Lax等价定理", "制造解方法"]
upstream: ["[[偏微分方程-二阶线性PDE分类与标准型]]", "[[偏微分方程-Lax-Milgram定理与椭圆弱解存在性]]"]
tags: [学习, 偏微分方程, 数值计算, 有限差分, 稳定性, 收敛性, MMS]
---

# 有限差分法相容性稳定性与 Lax 等价定理

> 所属阶段 MOC：[[04-现代变分弱解与数值计算/🧭 阶段4-现代变分弱解与数值计算|🧭 阶段 4：现代变分弱解与数值计算]]  
> 学习定位：掌握偏微分方程经典离散算法——有限差分法 (FDM)，掌握局部截断误差推导、von Neumann Fourier 谱稳定性分析、Lax 等价定理以及制造解方法 (MMS) 验证收敛阶的代码工程闭环。

---

## 1. 核心问题与物理直觉

对于无法获得初等解析解的真实工程偏微分方程，计算机通过在时空网格上对微分算子进行离散代数逼近。
数值计算面临的核心灵魂三问是：
1. **相容性 (Consistency)**：网格尺寸 $h, \Delta t \to 0$ 时，差分方程是否逼近原微分方程？
2. **稳定性 (Stability)**：计算机浮点舍入误差在时间步进中是否会被指数级放大而溢出？
3. **收敛性 (Convergence)**：数值解是否真正逼近原方程的真解？
**Lax 等价定理 (Lax Equivalence Theorem)** 将三者严格统一：**对于适定的线性初值问题，在相容的前提下，稳定性是收敛性的充要条件！**

---

## 2. 二维 Poisson 方程标准 5 点中心差分格式

考虑单位正方形 $\Omega = (0, 1)^2$ 上的 Poisson 方程：
$$-\left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right) = f(x, y)$$
取等距网格步长 $h = \Delta x = \Delta y = \frac{1}{N}$，网格节点 $(x_i, y_j) = (ih, jh)$。

### 2.1 5 点差分星形模板 (5-Point Stencil)
利用 Taylor 展开：
$$u(x+h, y) = u + h u_x + \frac{h^2}{2}u_{xx} + \frac{h^3}{6}u_{xxx} + \frac{h^4}{24}u_{xxxx} + O(h^5)$$
$$u(x-h, y) = u - h u_x + \frac{h^2}{2}u_{xx} - \frac{h^3}{6}u_{xxx} + \frac{h^4}{24}u_{xxxx} + O(h^5)$$
相加得二阶导数中心差分近似：
$$\frac{\partial^2 u}{\partial x^2}(x_i, y_j) = \frac{u_{i+1,j} - 2u_{i,j} + u_{i-1,j}}{h^2} - \frac{h^2}{12}\frac{\partial^4 u}{\partial x^4}(\xi_i, y_j)$$
将 $x$ 与 $y$ 方向代入 Poisson 方程，得到经典的 **5 点离散代数方程**：
$$-\Delta_h U_{i,j} = \frac{4U_{i,j} - U_{i+1,j} - U_{i-1,j} - U_{i,j+1} - U_{i,j-1}}{h^2} = f_{i,j}$$

### 2.2 局部截断误差与相容性 (Local Truncation Error)
将真解代入差分格式算子中，定义局部截断误差 $\tau_{i,j}$：
$$\tau_{i,j} = -\Delta_h u(x_i, y_j) - f(x_i, y_j) = -\frac{h^2}{12}\left( \frac{\partial^4 u}{\partial x^4} + \frac{\partial^4 u}{\partial y^4} \right) + O(h^4)$$
当 $h \to 0$ 时，$\tau_{i,j} = O(h^2) \to 0$。故 5 点中心差分格式是 **二阶相容的 ($O(h^2)$)**。

---

## 3. 一维热传导方程与 von Neumann 稳定性谱分析

考虑热方程 $u_t = \alpha u_{xx}$，网格比 $r = \frac{\alpha \Delta t}{h^2}$。

### 3.1 前向时间中心空间格式 (FTCS - 显式格式)
$$\frac{U_j^{n+1} - U_j^n}{\Delta t} = \alpha \frac{U_{j+1}^n - 2U_j^n + U_{j-1}^n}{h^2} \implies U_j^{n+1} = (1 - 2r)U_j^n + r(U_{j+1}^n + U_{j-1}^n)$$

### 3.2 von Neumann 谱稳定性分析推导
设误差的单模态 Fourier 展开为 $U_j^n = \xi^n e^{i k (jh)}$，代入格式中消去公共项：
$$\xi = 1 - 2r + r(e^{i k h} + e^{-i k h}) = 1 - 2r + 2r\cos(kh) = 1 - 4r\sin^2\left(\frac{kh}{2}\right)$$
- **稳定性充要条件**：对所有波数 $k$，放大因子模长必须满足 $|\xi(k)| \le 1$。
  $$-1 \le 1 - 4r\sin^2\left(\frac{kh}{2}\right) \le 1$$
- 右半部分 $1 - 4r\sin^2 \le 1$ 恒成立。
- 左半部分要求 $4r\sin^2\left(\frac{kh}{2}\right) \le 2 \implies r \le \frac{1}{2}$。
- **结论**：FTCS 显式格式是**条件稳定的**，时间步长必须受严格的 CFL 扩散约束限制：
  $$\Delta t \le \frac{h^2}{2\alpha}$$

### 3.3 后向时间隐式格式 (BTCS - 无条件稳定)
$$\frac{U_j^{n+1} - U_j^n}{\Delta t} = \alpha \frac{U_{j+1}^{n+1} - 2U_j^{n+1} + U_{j-1}^{n+1}}{h^2} \implies \xi = \frac{1}{1 + 4r\sin^2(kh/2)}$$
显然对任意 $r > 0$，$0 < \xi \le 1$，因此 BTCS 格式是 **无条件稳定的 (Unconditionally Stable)**。

---

## 4. 制造解方法 (MMS) 收敛阶实测验证技术

在工业科学计算中，如何验证代码实现没有隐藏 Bug 且确实达到了理论 $O(h^2)$ 收敛阶？核心方法就是 **制造解方法 (Method of Manufactured Solutions - MMS)**。

### MMS 算法四步曲：
1. **人为构造具有高阶连续性的解析解**：
   $$u_{exact}(x, y) = \sin(\pi x) \sin(\pi y)$$
2. **反向精确代入 PDE 算子求解源项 $f(x, y)$**：
   $$f(x, y) = -\Delta u_{exact} = -\left( -\pi^2 \sin(\pi x)\sin(\pi y) - \pi^2 \sin(\pi x)\sin(\pi y) \right) = 2\pi^2 \sin(\pi x)\sin(\pi y)$$
   精确计算边界条件 $g(x, y) = u_{exact}|_{\partial\Omega} = 0$。
3. **在多重细化网格 $N \in \{10, 20, 40, 80\}$ 上运行差分求解器得到数值解 $U_h$**。
4. **计算离散误差范数并计算实测收敛阶**：
   $$E_h = \|U_h - u_{exact}\|_{L_2}, \quad \text{Order} = \frac{\ln(E_{h_1} / E_{h_2})}{\ln(h_1 / h_2)}$$
   若实测阶稳定逼近 $2.00$，即证实算法实现与二阶理论完全一致。

---

## 5. 常见误区与反例

- **误区 1：认为只要截断误差 $O(h^2)$，数值解就一定收敛**。若计算格式不稳定（例如显式波动或热传导步长过大破坏了 CFL 条件），截断误差虽小，但浮点舍入误差会在几十步内放大 $10^{30}$ 倍导致数值溢出，完全无法收敛。
- **误区 2：在测试收敛阶时使用包含奇点或间断的初值**。若初值或解自身不属于 $C^4$（例如含有角点奇异性），高阶导数项有界性失效，差分格式的理论二阶收敛阶会退化为 $O(h^{0.5})$ 或更低。做 MMS 验证时必须选用充分光滑的制造解。

---

## 6. 主动自测与闭卷检查

- [ ] 我能用 Taylor 展开推导出 5 点 Laplace 差分模板的二阶局部截断误差。
- [ ] 我能利用 Fourier 放大因子独立推导出热传导显式格式的稳定性条件 $r \le 1/2$。
- [ ] 我能清晰阐述制造解方法 (MMS) 的 4 步验证逻辑与收敛阶对数公式。

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
