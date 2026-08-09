---
type: study
course: "属性数据分析"
topic: "广义线性模型GLM框架与链接函数"
stage_moc: "[[🧭 阶段0-前置知识]]"
flow: knowledge
kind: derivation
difficulty: intermediate
concept: ["广义线性模型", "链接函数", "典则链接", "线性预测器"]
prerequisites: ["[[属性数据分析-离散概率分布与指数族]]", "[[属性数据分析-极大似然估计与渐近推断三大检验]]"]
upstream: ["[[属性数据分析-离散概率分布与指数族]]", "[[属性数据分析-极大似然估计与渐近推断三大检验]]"]
status: completed
tags: [学习, 属性数据分析, GLM, 广义线性模型]
created: 2026-08-09
---

# 属性数据分析-广义线性模型GLM框架与链接函数

## 1. 广义线性模型（GLM）统一框架

由 Nelder 与 Wedderburn (1972) 提出的**广义线性模型（Generalized Linear Models, GLM）**将经典高斯回归、Logistic 回归、Poisson 回归、对数线性模型等纳入统一的理论与算法框架。

一个 GLM 由以下三大核心构件（Triad）唯一定义：

1. **随机成分（Random Component）**：
   响应变量 $Y_1, \dots, Y_n$ 独立，服从某一属于自然指数族的分布：
   $$
   f(y_i; \theta_i, \phi) = \exp\left\{ \frac{y_i \theta_i - b(\theta_i)}{a(\phi)} + c(y_i, \phi) \right\}
   $$
   期望为 $\mu_i = \mathbb{E}[Y_i] = b'(\theta_i)$，方差为 $\text{Var}(Y_i) = b''(\theta_i) a(\phi) = V(\mu_i) a(\phi)$。

2. **系统成分（Systematic Component）**：
   引入自变量矩阵 $X$（包含常数项），构建**线性预测器（Linear Predictor）**：
   $$
   \eta_i = \mathbf{x}_i^T \boldsymbol{\beta} = \beta_0 + \beta_1 x_{i1} + \dots + \beta_p x_{ip}
   $$

3. **链接函数（Link Function）**：
   可微单调函数 $g(\cdot)$，将受约束的均值空间 $\mu_i$ 映射至无约束的实数轴 $\mathbb{R}$：
   $$
   \eta_i = g(\mu_i) \iff \mu_i = g^{-1}(\mathbf{x}_i^T \boldsymbol{\beta})
   $$

---

## 2. 典则链接函数 (Canonical Link Function)

### 2.1 定义与推导
如果链接函数 $g(\cdot)$ 直接将期望值 $\mu_i$ 映射为指数族的**自然参数 $\theta_i$**，即：
$$
g(\mu_i) = \theta_i
$$
则称 $g$ 为该分布的**典则链接函数（Canonical Link Function）**。

由于 $\mu_i = b'(\theta_i)$，因此其反函数直接给出典则链接：
$$
g_{\text{canonical}}(\mu) = (b')^{-1}(\mu)
$$

### 2.2 常见分布的典则链接对照表

| 分布族 | 常用应用场景 | 自然参数 $\theta(\mu)$ | 典则链接函数 $g(\mu)$ | 均值逆映射 $\mu = g^{-1}(\eta)$ |
| :--- | :--- | :--- | :--- | :--- |
| **正态 (Normal)** | 经典连续测量值 | $\mu$ | **恒等链接 (Identity)**: $g(\mu) = \mu$ | $\mu = \eta$ |
| **伯努利 / 二项** | 成功/失败二分类 | $\ln\left(\frac{\mu}{1-\mu}\right)$ | **Logit**: $g(\mu) = \ln\left(\frac{\mu}{1-\mu}\right)$ | $\mu = \frac{1}{1 + e^{-\eta}}$ |
| **泊松 (Poisson)** | 事件发生频数 | $\ln\mu$ | **对数链接 (Log)**: $g(\mu) = \ln\mu$ | $\mu = e^{\eta}$ |
| **Gamma** | 正偏态持续时间 | $-1/\mu$ | **倒数链接 (Inverse)**: $g(\mu) = 1/\mu$ | $\mu = 1/\eta$ |

---

## 3. 典则链接的优良数学性质

使用典则链接带来极大理论与计算优势：
1. **充分统计量（Sufficient Statistics）**：对数似然关于参数 $\boldsymbol{\beta}$ 的充分统计量就是 $X^T \mathbf{y}$，即无信息损失。
2. **Score 方程形式极度优美**：
   $$
   U(\boldsymbol{\beta}) = \frac{\partial \ell}{\partial \boldsymbol{\beta}} = \frac{1}{a(\phi)} X^T (\mathbf{y} - \boldsymbol{\mu}) = \mathbf{0} \implies X^T \mathbf{y} = X^T \hat{\boldsymbol{\mu}}
   $$
   这意味着在样本上，自变量加权的观测值总和与模型拟合值总和严格相等！
3. **Hessian 矩阵独立于观测数据 $Y$**：Fisher 信息矩阵与负 Hessian 矩阵严格重合（Observed Information = Expected Fisher Information），保证了优化算法（Newton-Raphson）在凹似然曲面上的超线性收敛。

---

## 4. Python statsmodels GLM 拟合对比

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import numpy as np

# 构造模拟二分类数据
np.random.seed(42)
x = np.random.normal(size=100)
eta = 0.5 + 1.2 * x
pi = 1 / (1 + np.exp(-eta))
y = np.random.binomial(n=1, p=pi)

df = pd.DataFrame({'x': x, 'y': y})

# 1. 使用 GLM 拟合二项 Logit 模型
model_glm = smf.glm('y ~ x', data=df, family=sm.families.Binomial(link=sm.families.links.Logit())).fit()

# 2. 输出参数与置信区间
print(model_glm.summary())
```

---

## 5. 核心自测与检索练习

- [ ] 说明 GLM 三大构件（随机成分、系统成分、链接函数）在 Logistic 回归中分别对应什么。
- [ ] 推导 Poisson 分布的典则链接是 $\ln\mu$ 的数学步骤。
- [ ] 为什么在非典则链接（如 Probit 模型）下，Score 方程形式比 Logit 模型更复杂？

---

## 6. 学完后可以完成

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/31-属性数据分析"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

```dataview
LIST
FROM "03-Projects/31-属性数据分析"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
