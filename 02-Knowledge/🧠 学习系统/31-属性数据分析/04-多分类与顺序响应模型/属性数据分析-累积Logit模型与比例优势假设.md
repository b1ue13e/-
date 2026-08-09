---
type: study
course: "属性数据分析"
topic: "累积Logit模型与比例优势假设"
stage_moc: "[[🧭 阶段4-多分类与顺序响应模型]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: ["有序Logit", "累积Logit", "比例优势模型", "潜变量截断", "Brant检验"]
prerequisites: ["[[属性数据分析-二项Logistic回归模型与参数解释]]", "[[属性数据分析-多项Logistic回归与基准类别模型]]"]
upstream: ["[[属性数据分析-二项Logistic回归模型与参数解释]]", "[[属性数据分析-多项Logistic回归与基准类别模型]]"]
status: completed
tags: [学习, 属性数据分析, 有序数据, 累积Logit, 比例优势]
created: 2026-08-09
---

# 属性数据分析-累积Logit模型与比例优势假设

## 1. 有序分类数据与累积概率

当响应变量 $Y$ 的类别具有天然顺序（例如治疗改善程度：$1=\text{无改善} < 2=\text{部分改善} < 3=\text{显著改善}$）时，若当作名义变量会损失顺序信息，当作连续数值又强加了等间距假设。

定义**累积概率（Cumulative Probability）**：
$$
P(Y \le j \mid \mathbf{x}) = \pi_1(\mathbf{x}) + \pi_2(\mathbf{x}) + \dots + \pi_j(\mathbf{x}), \quad j = 1, 2, \dots, J-1
$$

---

## 2. 累积 Logit 模型与比例优势假设 (Proportional Odds)

累积 Logit 模型（Cumulative Logit Model）定义为：

$$
\text{logit}(P(Y \le j \mid \mathbf{x})) = \ln\left( \frac{P(Y \le j \mid \mathbf{x})}{1 - P(Y \le j \mid \mathbf{x})} \right) = \alpha_j - \mathbf{x}^T \boldsymbol{\beta}, \quad j = 1, 2, \dots, J-1
$$

其中：
- $\alpha_1 \le \alpha_2 \le \dots \le \alpha_{J-1}$ 为单调递增的**截断阈值（Cutpoints / Intercepts）**；
- $\boldsymbol{\beta}$ 为**公共斜率向量（Common Slope Vector）**，对所有分割点 $j$ 保持恒定。这被称为**比例优势假设（Proportional Odds Assumption）**。

### 2.1 优势比与参数解释
比较两个协变量向量 $\mathbf{x}_1$ 与 $\mathbf{x}_2$：
$$
\frac{\text{Odds}(Y \le j \mid \mathbf{x}_1)}{\text{Odds}(Y \le j \mid \mathbf{x}_2)} = \exp\left\{ -(\mathbf{x}_1 - \mathbf{x}_2)^T \boldsymbol{\beta} \right\} \implies \frac{\text{Odds}(Y > j \mid \mathbf{x}_1)}{\text{Odds}(Y > j \mid \mathbf{x}_2)} = \exp\left\{ (\mathbf{x}_1 - \mathbf{x}_2)^T \boldsymbol{\beta} \right\}
$$
* **解释口径**：$x_k$ 每增加 1 个单位，在任何分割点上，**处于更高评级类别（$Y > j$）的几率乘以 $\exp(\beta_k)$ 倍**。

---

## 3. 连续潜变量截断机制推导 (Latent Variable Formulation)

设存在不可直接观测的连续潜变量 $Y^* = \mathbf{x}^T \boldsymbol{\beta} + \varepsilon$，其中误差项 $\varepsilon \sim \text{Logistic}(0, 1)$，其累积分布函数为 $F(z) = \frac{1}{1 + e^{-z}}$。

观测分类 $Y$ 由阈值截断生成：
$$
Y = j \iff \alpha_{j-1} < Y^* \le \alpha_j
$$
则：
$$
P(Y \le j \mid \mathbf{x}) = P(Y^* \le \alpha_j \mid \mathbf{x}) = P(\varepsilon \le \alpha_j - \mathbf{x}^T \boldsymbol{\beta}) = \frac{1}{1 + \exp(-(\alpha_j - \mathbf{x}^T \boldsymbol{\beta}))}
$$
两端取 Logit 变换，立即得到累积 Logit 模型！这从底层证明了有序模型的严谨物理意义。

---

## 4. 比例优势假设的检验与诊断 (Brant Test)

比例优势假设要求 $\boldsymbol{\beta}_1 = \boldsymbol{\beta}_2 = \dots = \boldsymbol{\beta}_{J-1}$。
* **检验方法**：使用 **Brant 检验**（Wald 型检验）或 **似然比检验（LRT）**，将比例优势模型与无约束的非比例模型（Partial Proportional Odds）进行 Deviance 比较。
* 若假设被拒绝，应转向广义有序 Logit 模型（Generalized Ordered Logit）或相邻类别模型（Adjacent-Category Logit）。

---

## 5. Python 拟合累积 Logit 模型实战

```python
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel
import pandas as pd
import numpy as np

# 加载关节炎治疗真实数据 (Arthritis)
# Treatment: Treated vs Placebo; Improved: None < Some < Marked
df_arthritis = pd.read_csv("f:/03-Projects/31-属性数据分析/data/arthritis.csv")

# 拟合有序累积 Logit 模型 (distr='logit')
ord_model = OrderedModel(
    df_arthritis['Improved'],
    df_arthritis[['Treatment', 'Age']],
    distr='logit'
).fit(method='bfgs', disp=False)

print(ord_model.summary())
print("\n优势比 (OR):", np.exp(ord_model.params['Treatment[T.Treated]']))
```

---

## 6. 核心自测与检索练习

- [ ] 为什么有序数据不能直接当连续数字做线性回归？
- [ ] 解释比例优势假设的含义，若该假设不成立会对结论产生什么影响？
- [ ] 从潜变量截断模型出发，推导累积 Logit 公式的数学步骤。

---

## 7. 学完后可以完成

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
