---
type: study
topic: "Fourier与Laplace积分变换求解"
course: "偏微分方程"
created: 2026-08-08
status: completed
stage_moc: "[[🧭 阶段2-分离变量与积分变换]]"
flow: knowledge
kind: derivation
difficulty: intermediate
concept: ["Fourier变换", "Laplace变换", "卷积定理", "频域解法"]
upstream: ["[[偏微分方程-一维波动方程与达朗贝尔公式]]", "[[偏微分方程-热传导方程与极值原理]]"]
tags: [学习, 偏微分方程, 积分变换, 傅里叶变换, 拉普拉斯变换, 频域]
---

# Fourier 与 Laplace 积分变换求解

> 所属阶段 MOC：[[02-分离变量与积分变换/🧭 阶段2-分离变量与积分变换|🧭 阶段 2：分离变量与积分变换]]  
> 学习定位：掌握全空间连续频谱分析方法，熟练运用 Fourier 变换与 Laplace 变换将时空偏微分算子转化为频域代数或常微分方程，并通过卷积定理实现解析逆变换。

---

## 1. 核心问题与物理直觉

当空间区域从有界区间拓展至全空间 $\mathbb{R}$ 或时间轴半无界 $[0, \infty)$ 时，离散的傅里叶级数谱线无限密集，演化为**连续傅里叶积分变换与 Laplace 变换**。
微分算子在时域是复杂的差分比较，但在频域乘上因式 $i\xi$ 或复频率 $s$，将原本耦合的多维微分方程直接降阶为关于频域变量的简单代数方程。

---

## 2. 正式数学表述与变换法则

### 2.1 傅里叶变换 (Fourier Transform) 及其基本性质
对 $u(x) \in L^1(\mathbb{R})$，定义傅里叶变换及其逆变换：
$$\hat{u}(\xi) = \mathcal{F}[u](\xi) = \int_{-\infty}^\infty u(x) e^{-i\xi x} \, dx, \quad u(x) = \mathcal{F}^{-1}[\hat{u}](x) = \frac{1}{2\pi}\int_{-\infty}^\infty \hat{u}(\xi) e^{i\xi x} \, d\xi$$
- **导数性质**：$\mathcal{F}\left[ \frac{\partial u}{\partial x} \right] = i\xi \hat{u}(\xi), \quad \mathcal{F}\left[ \frac{\partial^2 u}{\partial x^2} \right] = -\xi^2 \hat{u}(\xi)$
- **空间卷积定理**：若 $h(x) = (f * g)(x) = \int_{-\infty}^\infty f(x - y)g(y)dy$，则 $\mathcal{F}[f * g](\xi) = \hat{f}(\xi) \cdot \hat{g}(\xi)$。

### 2.2 拉普拉斯变换 (Laplace Transform)
对时间变量 $t \ge 0$，定义拉普拉斯变换：
$$U(x, s) = \mathcal{L}[u](x, s) = \int_0^\infty u(x, t) e^{-st} \, dt \quad (\text{Re}(s) > s_0)$$
- **时间导数性质**：$\mathcal{L}\left[ \frac{\partial u}{\partial t} \right] = s U(x, s) - u(x, 0)$，直接内嵌了初始条件。
- $\mathcal{L}\left[ \frac{\partial^2 u}{\partial t^2} \right] = s^2 U(x, s) - s u(x, 0) - u_t(x, 0)$。

---

## 3. 典型例题与推导演练

### 【例题】利用 Fourier 变换严格推导全空间热传导方程解
考虑定解问题：
$$u_t = k u_{xx}, \quad x \in \mathbb{R}, t > 0; \quad u(x, 0) = g(x)$$

**推导步骤**：
1. **对空间变量 $x$ 施加傅里叶变换**：
   $$\mathcal{F}[u_t] = k \mathcal{F}[u_{xx}] \implies \frac{d\hat{u}}{dt}(\xi, t) = -k \xi^2 \hat{u}(\xi, t)$$
2. **求解一阶常微分方程**：
   $$\hat{u}(\xi, t) = \hat{u}(\xi, 0) \exp(-k \xi^2 t) = \hat{g}(\xi) \exp(-k \xi^2 t)$$
3. **识别频域乘积项与逆变换**：
   已知高斯函数逆傅里叶变换：
   $$\mathcal{F}^{-1}\left[ \exp(-k \xi^2 t) \right] = \frac{1}{\sqrt{4\pi k t}} \exp\left( -\frac{x^2}{4kt} \right) = \Phi(x, t)$$
4. **应用卷积定理**：
   $$u(x, t) = \mathcal{F}^{-1}[\hat{g}(\xi) \cdot \hat{\Phi}(\xi, t)] = (g * \Phi)(x, t) = \frac{1}{\sqrt{4\pi k t}}\int_{-\infty}^\infty \exp\left( -\frac{(x - y)^2}{4kt} \right) g(y) \, dy$$
   推导出的公式与经典高斯热核完全一致。

---

## 4. 常见误区与反例

- **误区 1：在有限有界区间上滥用连续傅里叶变换**。连续 Fourier 变换积分区间为 $(-\infty, \infty)$。有界区间上的函数若直接做连续 Fourier 变换，无法自然满足边界条件；有界区间应使用离散 Fourier 级数或有限积分变换。
- **误区 2：忽略 Laplace 变换的收敛半平面**。若解随时间增长超过指数阶（如 $e^{t^2}$），Laplace 积分发散，无法应用。必须确保原函数满足 $|u(x,t)| \le M e^{s_0 t}$。

---

## 5. 主动自测与闭卷检查

- [ ] 我能不看笔记熟练写出空间二阶导数的 Fourier 变换公式 $\mathcal{F}[u_{xx}] = -\xi^2 \hat{u}$。
- [ ] 我能利用 Fourier 变换与卷积定理独立推导出一维热传导方程高斯卷积解。
- [ ] 我能说明 Laplace 变换如何自动吸纳初始条件 $u(x, 0)$。

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
