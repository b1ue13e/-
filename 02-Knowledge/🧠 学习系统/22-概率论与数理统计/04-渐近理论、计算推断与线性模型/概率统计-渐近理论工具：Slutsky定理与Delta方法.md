---
type: study
topic: "概率统计-渐近理论工具：Slutsky定理与Delta方法"
course: "22-概率论与数理统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段4-渐近理论、计算推断与线性模型]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["渐近理论", "Slutsky定理", "连续映射定理", "Delta方法", "非线性变换渐近正态性"]
upstream: ["[[概率统计-极限定理与渐近收敛]]", "[[概率统计-估计量评价标准与Cramer-Rao下界]]"]
related: ["[[概率统计-非参数Bootstrap重抽样与置信区间]]", "[[概率统计-一元与多元线性回归的推断基础]]"]
tags: [学习, 概率论与数理统计, 渐近理论, Slutsky定理, Delta方法]
---

# 概率统计-渐近理论工具：Slutsky定理与Delta方法

---

## 1. 连续映射定理与斯卢茨基定理（Slutsky's Theorem）

### 1. 连续映射定理（Continuous Mapping Theorem, CMT）
若随机变量序列 $X_n \xrightarrow{d} X$（或 $X_n \xrightarrow{P} X$），且函数 $g: \mathbb{R} \to \mathbb{R}$ 在 $X$ 的所有可能取值点上连续，则：
$$g(X_n) \xrightarrow{d} g(X) \quad \left(\text{或 } g(X_n) \xrightarrow{P} g(X)\right)$$

### 2. 斯卢茨基定理（Slutsky's Theorem）
**定理**：设随机变量序列满足 $X_n \xrightarrow{d} X$，且 $Y_n \xrightarrow{P} c$（$c$ 为常数），则：
1. **加法性质**：$X_n + Y_n \xrightarrow{d} X + c$；
2. **乘法性质**：$X_n Y_n \xrightarrow{d} c X$；
3. **商性质**：若 $c \ne 0$，则 $\frac{X_n}{Y_n} \xrightarrow{d} \frac{X}{c}$。

**经典推论（未知标准差替换）**：
由 CLT，$Z_n = \frac{\sqrt{n}(\bar{X}_n - \mu)}{\sigma} \xrightarrow{d} \mathcal{N}(0, 1)$。
由辛钦大数定律，样本标准差 $S_n \xrightarrow{P} \sigma \implies \frac{\sigma}{S_n} \xrightarrow{P} 1$。
由 Slutsky 定理商性质：
$$t_n = \frac{\sqrt{n}(\bar{X}_n - \mu)}{S_n} = \left(\frac{\sqrt{n}(\bar{X}_n - \mu)}{\sigma}\right) \cdot \left(\frac{\sigma}{S_n}\right) \xrightarrow{d} \mathcal{N}(0, 1) \cdot 1 \sim \mathcal{N}(0, 1)$$
这就是**无论总体为何种分布（只要方差有限），大样本下 $t$ 统计量恒渐近标准正态分布**的数学根基！

---

## 2. 德尔塔方法（The Delta Method）

### 1. 一元 Delta 方法定理
**条件**：设随机变量序列满足 $\sqrt{n}(T_n - \theta) \xrightarrow{d} \mathcal{N}(0, \sigma^2)$。
若函数 $g(t)$ 在 $t = \theta$ 处连续可微且 $g'(\theta) \ne 0$。

**结论**：
$$\sqrt{n}\big(g(T_n) - g(\theta)\big) \xrightarrow{d} \mathcal{N}\left(0, \; \big[g'(\theta)\big]^2 \sigma^2\right)$$

### 2. 严格数学证明（泰勒展开与 Slutsky）
1. 在 $\theta$ 处对 $g(T_n)$ 作一阶泰勒展开：
   $$g(T_n) = g(\theta) + g'(\theta)(T_n - \theta) + R_n$$
   其中余项 $R_n = o(|T_n - \theta|)$。
2. 两端减去 $g(\theta)$ 并同乘 $\sqrt{n}$：
   $$\sqrt{n}\big(g(T_n) - g(\theta)\big) = g'(\theta) \cdot \sqrt{n}(T_n - \theta) + \sqrt{n} R_n$$
3. 因 $T_n \xrightarrow{P} \theta$，由微分余项性质 $\sqrt{n} R_n \xrightarrow{P} 0$。
4. 已知 $\sqrt{n}(T_n - \theta) \xrightarrow{d} Y \sim \mathcal{N}(0, \sigma^2)$。
   由 Slutsky 定理：
   $$\sqrt{n}\big(g(T_n) - g(\theta)\big) \xrightarrow{d} g'(\theta) Y + 0 \sim \mathcal{N}\left(0, [g'(\theta)]^2 \sigma^2\right) \quad \blacksquare$$

---

## 3. 经典案例推导：指数分布参数倒数 $\frac{1}{\bar{X}}$ 的渐近分布

设 $X_1, \dots, X_n \overset{\text{i.i.d.}}{\sim} \text{Exp}(\lambda)$，期望 $\mu = \frac{1}{\lambda}$，方差 $\sigma^2 = \frac{1}{\lambda^2}$。
欲求参数估计量 $\hat{\lambda} = g(\bar{X}) = \frac{1}{\bar{X}}$ 的渐近分布。
1. 由 CLT：$\sqrt{n}\left(\bar{X} - \frac{1}{\lambda}\right) \xrightarrow{d} \mathcal{N}\left(0, \frac{1}{\lambda^2}\right)$；
2. 定义变换函数 $g(t) = \frac{1}{t}$，求导 $g'(t) = -\frac{1}{t^2}$。在 $t = \mu = \frac{1}{\lambda}$ 处：
   $$g'(\mu) = -\frac{1}{(1/\lambda)^2} = -\lambda^2$$
3. 应用 Delta 方法：
   $$\sqrt{n}\left(\frac{1}{\bar{X}} - \lambda\right) \xrightarrow{d} \mathcal{N}\left(0, (-\lambda^2)^2 \cdot \frac{1}{\lambda^2}\right) \sim \mathcal{N}(0, \lambda^2)$$
- **结论**：在大样本下，$\hat{\lambda} \approx \mathcal{N}\left(\lambda, \frac{\lambda^2}{n}\right)$。

---

## 4. Python 验证 Delta 方法渐近方差

```python
import numpy as np
import scipy.stats as stats

np.random.seed(42)
lam_true = 2.0
n = 200
n_sim = 50_000

# 抽取指数分布并计算 1 / X_bar
samples = np.random.exponential(scale=1/lam_true, size=(n_sim, n))
x_bars = samples.mean(axis=1)
lam_hats = 1.0 / x_bars

# 计算标准化残差: sqrt(n) * (lam_hat - lam_true)
asymptotic_scaled = np.sqrt(n) * (lam_hats - lam_true)

sim_var = np.var(asymptotic_scaled)
theory_var = lam_true**2 # 4.0

print(f"Delta 方法模拟渐近方差: {sim_var:.4f}")
print(f"Delta 方法理论渐近方差: {theory_var:.4f}")
assert abs(sim_var - theory_var) < 0.1, "Delta 方法渐近方差检验未通过！"
```

---

## 5. 闭卷自测

- [ ] 默写 Slutsky 定理的三条代数性质；
- [ ] 给出一元 Delta 方法基于一阶泰勒展开与 Slutsky 定理的严谨证明；
- [ ] 若 $X_n \sim B(n, p)$，求对数发生比 $\ln\left(\frac{\hat{p}}{1-\hat{p}}\right)$ 的渐近正态方差。

---

## 6. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
