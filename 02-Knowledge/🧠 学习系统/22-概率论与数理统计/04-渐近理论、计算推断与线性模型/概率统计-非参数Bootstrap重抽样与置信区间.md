---
type: study
topic: "概率统计-非参数Bootstrap重抽样与置信区间"
course: "22-概率论与数理统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段4-渐近理论、计算推断与线性模型]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["非参数统计", "Bootstrap", "经验分布函数", "eCDF", "重抽样", "百分位置信区间", "BCa区间"]
upstream: ["[[概率统计-渐近理论工具：Slutsky定理与Delta方法]]", "[[概率统计-参数区间估计与枢轴量法]]"]
related: ["[[概率统计-一元与多元线性回归的推断基础]]"]
tags: [学习, 概率论与数理统计, 计算统计, Bootstrap, 重抽样, 非参数推断]
---

# 概率统计-非参数Bootstrap重抽样与置信区间

---

## 1. 经验分布函数（eCDF）与代换原则（Plug-in Principle）

### 1. 经验分布函数（Empirical CDF）
设 $X_1, \dots, X_n \overset{\text{i.i.d.}}{\sim} F(x)$。定义样本的经验分布函数为：
$$\hat{F}_n(x) = \frac{1}{n}\sum_{i=1}^n I(X_i \le x)$$
- **格里文科-坎泰利定理（Glivenko-Cantelli Theorem / 统计学基本定理）**：
  经验分布函数是一致收敛于真实总体分布函数的：
  $$\sup_{x \in \mathbb{R}} |\hat{F}_n(x) - F(x)| \xrightarrow{\text{a.s.}} 0 \quad (\text{当 } n \to \infty)$$

### 2. 统计泛函与代换原则
若参数可表示为真实分布的泛函 $\theta = T(F)$（如总体均值 $\mu = \int x dF(x)$，总体中位数 $M = F^{-1}(0.5)$），则代换估计量定义为：
$$\hat{\theta} = T(\hat{F}_n)$$

---

## 2. 非参数 Bootstrap 算法流程

```
真实总体 F  ---(未知抽样)--->  原始样本 X = (X_1, ..., X_n)  [估计量: θ_hat]
                                    |
                            (以 1/n 概率有放回抽样 n 次)
                                    v
                              Bootstrap 样本 X* = (X*_1, ..., X*_n)
                                    |
                              (计算统计量)
                                    v
                              θ*_b = T(X*_b)   (重复 B 次, 通常 B=2000)
```

### 标准执行步骤：
1. 从原始样本 $\mathbf{x} = (x_1, \dots, x_n)$ 中**有放回均匀抽取容量为 $n$ 的新样本** $\mathbf{x}^* = (x_1^*, \dots, x_n^*)$；
2. 在重抽样样本 $\mathbf{x}^*$ 上计算目标统计量 $\hat{\theta}^* = T(\mathbf{x}^*)$；
3. 独立重复上述过程 $B$ 次（通常 $B = 2000 \sim 10000$），获得 Bootstrap 统计量序列 $\{\hat{\theta}^*_1, \hat{\theta}^*_2, \dots, \hat{\theta}^*_B\}$；
4. **Bootstrap 标准误估计**：
   $$\widehat{\text{SE}}_{\text{boot}}(\hat{\theta}) = \sqrt{\frac{1}{B-1}\sum_{b=1}^B (\hat{\theta}^*_b - \bar{\theta}^*)^2}$$

---

## 3. Bootstrap 置信区间的构造方法

### 1. 标准误差区间法（Normal Bootstrap Interval）
若 $\hat{\theta}$ 的分布近似对称且无偏：
$$CI_{1-\alpha} = \left[\hat{\theta} - z_{\alpha/2} \cdot \widehat{\text{SE}}_{\text{boot}}, \quad \hat{\theta} + z_{\alpha/2} \cdot \widehat{\text{SE}}_{\text{boot}}\right]$$

### 2. 百分位数置信区间（Percentile Bootstrap Interval）
直接利用重抽样经验分布的分位数：
将 $B$ 个重抽样估计量从小到大排序 $\hat{\theta}^*_{(1)} \le \hat{\theta}^*_{(2)} \le \dots \le \hat{\theta}^*_{(B)}$。
$$CI_{1-\alpha} = \left[\hat{\theta}^*_{(\lfloor B \cdot \frac{\alpha}{2}\rfloor)}, \quad \hat{\theta}^*_{(\lfloor B \cdot (1 - \frac{\alpha}{2})\rfloor)}\right]$$
- **优点**：无需假设分布对称，具有单调变换不变性。

---

## 4. Python 实现非参数 Bootstrap（以样本中位数为例）

```python
import numpy as np
import scipy.stats as stats

np.random.seed(42)
# 从高度偏态的对数正态分布抽样
true_data = np.random.lognormal(mean=0.0, sigma=1.0, size=100)
true_median = np.exp(0.0) # 1.0

# 1. 原始样本估计
hat_median = np.median(true_data)

# 2. Bootstrap 重抽样 (B=5000)
B = 5000
n = len(true_data)
boot_estimates = np.empty(B)

for b in range(B):
    boot_sample = np.random.choice(true_data, size=n, replace=True)
    boot_estimates[b] = np.median(boot_sample)

# 3. 计算标准误与 95% 百分位区间
boot_se = np.std(boot_estimates, ddof=1)
ci_lower = np.percentile(boot_estimates, 2.5)
ci_upper = np.percentile(boot_estimates, 97.5)

print(f"样本中位数估计: {hat_median:.4f}")
print(f"Bootstrap 估计标准误 SE: {boot_se:.4f}")
print(f"95% 百分位 Bootstrap 置信区间: [{ci_lower:.4f}, {ci_upper:.4f}]")
assert ci_lower < true_median < ci_upper, "Bootstrap 置信区间未能覆盖真实中位数！"
```

---

## 5. 闭卷自测

- [ ] 阐述非参数 Bootstrap 的核心哲学与代换原则（Plug-in Principle）；
- [ ] 写出百分位数 Bootstrap 置信区间的四步算法；
- [ ] 说明为什么 Bootstrap 必须使用**有放回抽样（with replacement）**而不是无放回抽样。

---

## 6. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
