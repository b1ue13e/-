---
type: study
topic: "概率统计-估计量评价标准与Cramer-Rao下界"
course: "22-概率论与数理统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段2-抽样理论与参数估计]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["估计量评价标准", "无偏性", "有效性", "一致性", "均方误差", "MSE", "Fisher信息量", "Cramer-Rao下界", "UMVUE"]
upstream: ["[[概率统计-点估计方法：矩估计与极大似然估计]]"]
related: ["[[概率统计-参数区间估计与枢轴量法]]"]
tags: [学习, 概率论与数理统计, 参数估计, 无偏估计, 费雪信息量, CRLB]
---

# 概率统计-估计量评价标准与Cramer-Rao下界

---

## 1. 估计量四大评价标准

设 $\hat{\theta} = \hat{\theta}(X_1, \dots, X_n)$ 为参数 $\theta$ 的点估计量。

### 1. 无偏性（Unbiasedness）
若对参数空间内任意 $\theta \in \Theta$：
$$E[\hat{\theta}] = \theta$$
则称 $\hat{\theta}$ 为 $\theta$ 的**无偏估计量**。
- **偏差（Bias）**：$\text{Bias}(\hat{\theta}) = E[\hat{\theta}] - \theta$。

### 2. 均方误差（MSE, Mean Squared Error）
$$\text{MSE}(\hat{\theta}) = E\big[(\hat{\theta} - \theta)^2\big]$$
**偏差-方差分解定理（Bias-Variance Tradeoff）**：
$$\text{MSE}(\hat{\theta}) = \text{Var}(\hat{\theta}) + \big[\text{Bias}(\hat{\theta})\big]^2$$
- *推导*：展开 $E\big[(\hat{\theta} - E[\hat{\theta}] + E[\hat{\theta}] - \theta)^2\big]$，交叉项为 0。

### 3. 有效性（Efficiency / 相对效率）
若 $\hat{\theta}_1$ 与 $\hat{\theta}_2$ 均为 $\theta$ 的无偏估计量，若对所有 $\theta$ 均有 $\text{Var}(\hat{\theta}_1) \le \text{Var}(\hat{\theta}_2)$，且至少存在一个 $\theta$ 严格小于，则称 **$\hat{\theta}_1$ 比 $\hat{\theta}_2$ 更有效**。

### 4. 一致性 / 相合性（Consistency）
若随着样本容量 $n \to \infty$，估计量依概率收敛于真实参数：
$$\hat{\theta}_n \xrightarrow{P} \theta \quad (\forall \varepsilon > 0, \lim_{n\to\infty} P(|\hat{\theta}_n - \theta| \ge \varepsilon) = 0)$$
则称 $\hat{\theta}_n$ 为**一致估计量**。
- *判定定理*：若 $\lim_{n\to\infty} \text{Bias}(\hat{\theta}_n) = 0$ 且 $\lim_{n\to\infty} \text{Var}(\hat{\theta}_n) = 0$，则 $\hat{\theta}_n$ 必为一致估计量。

---

## 2. 费雪信息量（Fisher Information）的几何本质

设单观测值 $X \sim f(x; \theta)$。定义**得分函数（Score Function）** $S(\theta) = \frac{\partial \ln f(X; \theta)}{\partial \theta}$。
在正则条件下（积分与求导可交换），Score 函数的均值为 0：$E[S(\theta)] = 0$。

定义单样本的 **Fisher 信息量**：
$$I(\theta) = E\left[\left(\frac{\partial \ln f(X; \theta)}{\partial \theta}\right)^2\right] = \text{Var}(S(\theta)) = -E\left[\frac{\partial^2 \ln f(X; \theta)}{\partial \theta^2}\right]$$

> **第一性原理几何直觉**：
> 1. **对数似然曲率**：$-E\left[\frac{\partial^2 \ln f}{\partial \theta^2}\right]$ 是对数似然函数在真值处的**平均凸度/曲率（Curvature）**。似然曲面越陡峭（曲率越大），数据对参数 $\theta$ 的扰动越敏感，从数据中提取的信息量 $I(\theta)$ 就越大。
> 2. **样本加法性**：对 i.i.d. 样本 $X_1, \dots, X_n$，总信息量满足线性可加性：$I_n(\theta) = n I(\theta)$。

---

## 3. Cramér-Rao 不等式（CRLB）与几何证明

### 3.1 定理陈述
设 $X_1, \dots, X_n \overset{\text{i.i.d.}}{\sim} f(x; \theta)$，$\hat{\theta}(\mathbf{X})$ 为 $\theta$ 的任意无偏估计量（$E[\hat{\theta}] = \theta$）。在正则条件（支撑集与 $\theta$ 无关、积分与求导可交换）下，其方差存在下界：
$$\text{Var}(\hat{\theta}) \ge \frac{1}{I_n(\theta)} = \frac{1}{n I(\theta)}$$
若某个无偏估计量 $\hat{\theta}^*$ 的方差恰好达到该下界，则称 $\hat{\theta}^*$ 为**有效估计量（Efficient Estimator）**或 **UMVUE（一致最小方差无偏估计）**。

### 3.2 几何证明（基于 $L^2$ 希尔伯特空间上的柯西-施瓦茨不等式）
记总对数似然的导数（即**总 Score 函数**）$S_n(\theta) = \dfrac{\partial \ln L}{\partial \theta} = \sum_{i=1}^n \dfrac{\partial \ln f(X_i; \theta)}{\partial \theta}$；它与「总得分」的视角等价，只是把单个观测的 Score 在 $n$ 个样本上求和。
1. 由归一化 $\int f(\mathbf{x}; \theta) d\mathbf{x} = 1$ 对 $\theta$ 求导得 $E[S_n(\theta)] = 0$，且 $\text{Var}(S_n(\theta)) = I_n(\theta) = n I(\theta)$；
2. 由无偏性 $\int \hat{\theta}(\mathbf{x}) f(\mathbf{x}; \theta) d\mathbf{x} = \theta$ 对 $\theta$ 求导得：
   $$E\!\left[\hat{\theta}\, S_n(\theta)\right] = \frac{\partial}{\partial \theta} E[\hat{\theta}] = 1$$
3. 于是 $\text{Cov}\!\left(\hat{\theta}, S_n(\theta)\right) = E[\hat{\theta} S_n(\theta)] - E[\hat{\theta}]\,E[S_n(\theta)] = 1 - \theta \cdot 0 = 1$；
4. 在随机变量构成的 $L^2$ 内积空间中，对 $\hat{\theta}$ 与 $S_n(\theta)$ 应用柯西-施瓦茨不等式：
   $$\big[\text{Cov}(\hat{\theta}, S_n(\theta))\big]^2 \le \text{Var}(\hat{\theta}) \cdot \text{Var}(S_n(\theta)) \implies 1 \le \text{Var}(\hat{\theta}) \cdot n I(\theta)$$
   即 $\text{Var}(\hat{\theta}) \ge \dfrac{1}{n I(\theta)} \quad \blacksquare$
- **达界条件（等号成立）**：当且仅当 $\hat{\theta}(X) - \theta$ 与 Score 函数 $S_n(\theta)$ 线性相关，即分布族属于**指数族**。这正是「无偏估计达到 CRLB ⟺ 属于指数族」的几何判据。

---

## 4. 经典检验案例：正态均值 $\mu$ 的样本均值 $\bar{X}$

设 $X_1, \dots, X_n \overset{\text{i.i.d.}}{\sim} \mathcal{N}(\mu, \sigma^2)$（$\sigma^2$ 已知）。
1. 单样本对数密度：$\ln f(x; \mu) = -\frac{1}{2}\ln(2\pi\sigma^2) - \frac{(x-\mu)^2}{2\sigma^2}$；
2. 二阶导：$\frac{\partial^2 \ln f}{\partial \mu^2} = -\frac{1}{\sigma^2} \implies I(\mu) = -E\left[-\frac{1}{\sigma^2}\right] = \frac{1}{\sigma^2}$；
3. 总 Fisher 信息量：$I_n(\mu) = \frac{n}{\sigma^2}$；
4. CRLB 下界：$\text{CRLB} = \frac{1}{I_n(\mu)} = \frac{\sigma^2}{n}$；
5. 样本均值 $\bar{X}$ 的方差：$\text{Var}(\bar{X}) = \frac{\sigma^2}{n} \equiv \text{CRLB}$！
- **结论**：样本均值 $\bar{X}$ 是正态总体均值 $\mu$ 的**严格有效估计量与 UMVUE**。

---

## 5. Python 模拟验证估计量有效性

```python
import numpy as np

np.random.seed(42)
n_sim = 50_000
n = 20
mu, sigma = 0.0, 1.0

# 抽取正态样本
samples = np.random.normal(mu, sigma, size=(n_sim, n))

# 比较估计量 1 (样本均值) 与 估计量 2 (样本中位数)
est_mean = samples.mean(axis=1)
est_median = np.median(samples, axis=1)

var_mean = np.var(est_mean)
var_median = np.var(est_median)
crlb = sigma**2 / n # 1.0 / 20 = 0.05

print(f"理论 CRLB 方差下界: {crlb:.5f}")
print(f"样本均值方差 (有效估计量): {var_mean:.5f}")
print(f"样本中位数方差: {var_median:.5f}")
print(f"样本均值相对中位数效率比: {var_median / var_mean:.4f} (理论 pi/2 ≈ 1.5708)")

assert abs(var_mean - crlb) < 0.002, "样本均值未能达到 CRLB！"
assert var_mean < var_median, "样本均值方差必须严格小于中位数！"
```

---

## 6. 闭卷自测

- [ ] 给出均方误差 MSE 偏差-方差分解的完整推导；
- [ ] 写出 Fisher 信息量的两种等价计算公式；
- [ ] 默写利用柯西-施瓦茨不等式证明 Cramér-Rao 不等式的主线。

---

## 7. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
