---
type: study
course: "属性数据分析"
topic: "二项Logistic回归模型与参数解释"
stage_moc: "[[🧭 阶段2-二项响应与Logistic回归]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["Logistic回归", "Logit变换", "几率比解释", "交互效应"]
prerequisites: ["[[属性数据分析-广义线性模型GLM框架与链接函数]]", "[[属性数据分析-关联效应量-优势比与相对风险]]"]
upstream: ["[[属性数据分析-广义线性模型GLM框架与链接函数]]", "[[属性数据分析-关联效应量-优势比与相对风险]]"]
status: completed
tags: [学习, 属性数据分析, Logistic回归, GLM, 参数解释]
created: 2026-08-09
---

# 属性数据分析-二项Logistic回归模型与参数解释

## 1. 模型形式与概率映射

设响应变量 $Y_i \in \{0, 1\}$，成功概率 $\pi(\mathbf{x}_i) = P(Y_i = 1 \mid \mathbf{x}_i)$。

### 1.1 Logit 形式
二项 Logistic 回归采用 Logit 典则链接，将概率比值映射到无约束实数空间：

$$
\text{logit}(\pi(\mathbf{x})) = \ln\left( \frac{\pi(\mathbf{x})}{1 - \pi(\mathbf{x})} \right) = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_p x_p = \mathbf{x}^T \boldsymbol{\beta}
$$

### 1.2 概率形式（Sigmoid 函数）
两端取反解，得到 S 型预测概率函数：

$$
\pi(\mathbf{x}) = \frac{\exp(\mathbf{x}^T \boldsymbol{\beta})}{1 + \exp(\mathbf{x}^T \boldsymbol{\beta})} = \frac{1}{1 + \exp(-\mathbf{x}^T \boldsymbol{\beta})}
$$

其导数满足优美的对称递减性质：$\frac{\partial \pi}{\partial x_j} = \beta_j \pi(\mathbf{x}) (1 - \pi(\mathbf{x}))$。当 $\pi = 0.5$（即线性预测器为 0）时，斜率达到最大值 $\frac{\beta_j}{4}$（称为 **Divide-by-4 经验法则**）。

---

## 2. 回归系数 $\beta_j$ 的核心统计学解释

### 2.1 连续协变量的解释
设连续自变量 $x_1$ 增加 1 个单位（由 $x_1$ 变为 $x_1 + 1$），保持其他变量 $\mathbf{x}_{-1}$ 不变：

$$
\text{logit}(\pi(x_1 + 1, \mathbf{x}_{-1})) - \text{logit}(\pi(x_1, \mathbf{x}_{-1})) = \beta_1
$$

对两边取指数：
$$
\frac{\text{Odds}(x_1 + 1)}{\text{Odds}(x_1)} = \exp(\beta_1)
$$
* **解释口径**：在控制其他所有协变量不变的前提下，**$x_1$ 每增加 1 个单位，事件发生的几率（Odds）乘以 $\exp(\beta_1)$ 倍（即增加 $(\exp(\beta_1) - 1) \times 100\%$）**。
* 若 $x_1$ 增加 $c$ 个单位，则比值比为 $\exp(c \beta_1)$。

### 2.2 二分类协变量的解释（虚拟变量）
设 $x_2 \in \{0, 1\}$（如 $1=\text{处理组}, 0=\text{对照组}$）：
$$
\text{Odds Ratio (处理组 vs 对照组)} = \frac{\text{Odds}(x_2 = 1)}{\text{Odds}(x_2 = 0)} = \exp(\beta_2)
$$
此时 $\exp(\beta_2)$ 就是控制其他协变量后的**调整优势比（Adjusted Odds Ratio, aOR）**。

### 2.3 交互效应（效应修饰 Effect Modification）
若包含交互项 $\beta_3 (x_1 \times x_2)$：
$$
\text{logit}(\pi) = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \beta_3 x_1 x_2
$$
则 $x_1$ 增加 1 单位对 Log-odds 的效应变为 $\beta_1 + \beta_3 x_2$。这意味着 $x_1$ 的效应大小依赖于 $x_2$ 的水平。

---

## 3. Python 建模与参数解释范例

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import numpy as np

# 模拟数据
np.random.seed(123)
n = 300
age = np.random.normal(50, 10, n)
treatment = np.random.binomial(1, 0.5, n)
# 真模型: logit(pi) = -2 + 0.04*age + 1.2*treatment
eta = -2.0 + 0.04 * age + 1.2 * treatment
pi = 1 / (1 + np.exp(-eta))
y = np.random.binomial(1, pi)

df = pd.DataFrame({'age': age, 'treatment': treatment, 'y': y})

# 拟合 Logistic 回归
model = smf.logit('y ~ age + treatment', data=df).fit()
print(model.summary())

# 输出系数的 OR 及其 95% 置信区间
params = model.params
conf = model.conf_int()
conf['OR'] = params
conf.columns = ['2.5%', '97.5%', 'OR']
print("\n优势比 (OR) 与 95% CI:")
print(np.exp(conf))
```

---

## 4. 核心自测与检索练习

- [ ] 为什么 Logistic 回归不能像线性回归那样直接说“$x_1$ 每增加 1 单位，$Y$ 增加 $\beta_1$”？
- [ ] 什么是 Divide-by-4 经验法则？若某个自变量的系数 $\hat{\beta}_1 = 0.8$，该变量对发生概率 $\pi$ 的最大可能增量是多少？
- [ ] 若 $\hat{\beta}_{\text{smoke}} = 0.693$，吸烟者的患病优势是非吸烟者的多少倍？

---

## 5. 学完后可以完成

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
