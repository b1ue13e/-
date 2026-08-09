---
type: study
course: "属性数据分析"
topic: "Poisson回归模型与暴露量率模型"
stage_moc: "[[🧭 阶段3-计数数据与对数线性模型]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["Poisson回归", "对数链接", "暴露量", "Offset", "发生率比"]
prerequisites: ["[[属性数据分析-广义线性模型GLM框架与链接函数]]"]
upstream: ["[[属性数据分析-广义线性模型GLM框架与链接函数]]"]
status: completed
tags: [学习, 属性数据分析, 计数数据, Poisson回归, GLM]
created: 2026-08-09
---

# 属性数据分析-Poisson回归模型与暴露量率模型

## 1. 计数数据与 Poisson 回归基础

设响应变量 $Y_i \in \{0, 1, 2, \dots\}$ 为非负整数计数，服从泊松分布：
$$
P(Y_i = y_i \mid \mathbf{x}_i) = \frac{\exp(-\mu_i) \mu_i^{y_i}}{y_i!}, \quad \mu_i = \mathbb{E}[Y_i]
$$

### 1.1 模型形式
采用典则链接对数函数（Log-link）：
$$
\ln(\mu_i) = \mathbf{x}_i^T \boldsymbol{\beta} = \beta_0 + \beta_1 x_{i1} + \dots + \beta_p x_{ip} \implies \mu_i = \exp(\mathbf{x}_i^T \boldsymbol{\beta})
$$

### 1.2 参数解释：发生率比 (Incidence Rate Ratio, IRR)
若自变量 $x_1$ 增加 1 个单位，保持其余变量不变：
$$
\frac{\mu(x_1 + 1)}{\mu(x_1)} = \frac{\exp(\beta_0 + \beta_1(x_1 + 1) + \dots)}{\exp(\beta_0 + \beta_1 x_1 + \dots)} = \exp(\beta_1)
$$
* **解释口径**：在控制其他变量不变时，**$x_1$ 每增加 1 个单位，期望事件计数的发生率乘以 $\exp(\beta_1)$ 倍（$\text{IRR} = \exp(\beta_1)$）**。

---

## 2. 暴露量与率模型 (Rate Models with Offset)

在很多场景下，观测个体暴露于不同大小的时间、面积或人口规模（称为**暴露量 Exposure / 风险人年 Time-at-risk**，记为 $t_i$）。例如：
- 某城市发生交通事故数，暴露量为总人口规模或机动车登记量；
- 某患者疾病复发次数，暴露量为随访随访月数 $t_i$。

我们关注的是**发生率（Rate）** $\lambda_i = \frac{\mu_i}{t_i}$：
$$
\ln\left( \frac{\mu_i}{t_i} \right) = \mathbf{x}_i^T \boldsymbol{\beta} \implies \ln(\mu_i) - \ln(t_i) = \mathbf{x}_i^T \boldsymbol{\beta} \implies \ln(\mu_i) = \ln(t_i) + \mathbf{x}_i^T \boldsymbol{\beta}
$$

> [!IMPORTANT]
> **偏置项 (Offset)**：$\ln(t_i)$ 作为一个**回归系数固定为 1 的特殊自变量**引入模型，称为 Offset。它完美地将不同暴露基数标准化，使得回归系数 $\boldsymbol{\beta}$ 直接刻画发生率 $\lambda_i$ 的对数效应。

---

## 3. 对数似然与参数估计

独立样本对数似然函数为：
$$
\ell(\boldsymbol{\beta}) = \sum_{i=1}^n \left[ y_i \ln(\mu_i) - \mu_i - \ln(y_i!) \right] = \sum_{i=1}^n \left[ y_i (\ln t_i + \mathbf{x}_i^T \boldsymbol{\beta}) - t_i e^{\mathbf{x}_i^T \boldsymbol{\beta}} - \ln(y_i!) \right]
$$

梯度向量（Score 向量）：
$$
U(\boldsymbol{\beta}) = \sum_{i=1}^n (y_i - \mu_i) \mathbf{x}_i = X^T (\mathbf{y} - \boldsymbol{\mu})
$$
Hessian 矩阵为负定矩阵 $H(\boldsymbol{\beta}) = -X^T W X$，其中 $W = \text{diag}(\mu_1, \dots, \mu_n)$。

---

## 4. Python statsmodels Rate Model 实战

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import numpy as np

# 构造模拟数据: 工厂事故数
np.random.seed(42)
n = 100
workers = np.random.uniform(50, 500, n)  # 暴露量: 工人数量
exposure_time = workers / 100.0          # 单位: 百人-年
safety_training = np.random.binomial(1, 0.5, n) # 1=有安全培训, 0=无

# 真发生率: lambda = exp(0.8 - 0.6 * safety_training)
lambda_true = np.exp(0.8 - 0.6 * safety_training)
mu = lambda_true * exposure_time
accidents = np.random.poisson(mu)

df = pd.DataFrame({'accidents': accidents, 'training': safety_training, 'exposure': exposure_time})

# 拟合带 offset 的 Poisson 回归
model = smf.glm('accidents ~ training', data=df,
                offset=np.log(df['exposure']),
                family=sm.families.Poisson()).fit()

print(model.summary())
print("\n发生率比 (IRR):", np.exp(model.params['training']))
```

---

## 5. 核心自测与检索练习

- [ ] 为什么在泊松回归中，系数 $\beta_j$ 的指数变换 $\exp(\beta_j)$ 称为发生率比（IRR）？
- [ ] 解释 Offset 偏置项的数学作用，为什么它的回归系数必须固定为 1？
- [ ] 若某药使癫痫发作频数的 Poisson 回归系数为 $\hat{\beta} = -0.405$，服药者的发作率是对照组的多少百分比？

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
