---
type: study
course: "属性数据分析"
topic: "多项Logistic回归与基准类别模型"
stage_moc: "[[🧭 阶段4-多分类与顺序响应模型]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["多项Logistic回归", "基准类别模型", "Softmax", "相对风险比", "IIA假设"]
prerequisites: ["[[属性数据分析-二项Logistic回归模型与参数解释]]"]
upstream: ["[[属性数据分析-二项Logistic回归模型与参数解释]]"]
status: completed
tags: [学习, 属性数据分析, 多分类, Logistic回归, GLM]
created: 2026-08-09
---

# 属性数据分析-多项Logistic回归与基准类别模型

## 1. 名义多分类响应与基准类别模型

设响应变量 $Y \in \{1, 2, \dots, J\}$ 具有 $J$ 个无序分类类别（如交通方式：步行、公交、自驾）。

选择第 $J$ 类作为**基准类别（Baseline Category / Reference Class）**，构建 $J-1$ 个成对 Logit 方程：

$$
\ln\left( \frac{P(Y = j \mid \mathbf{x})}{P(Y = J \mid \mathbf{x})} \right) = \alpha_j + \mathbf{x}^T \boldsymbol{\beta}_j, \quad j = 1, 2, \dots, J-1
$$

### 各类别概率的闭式解 (Softmax)
利用概率归一化条件 $\sum_{j=1}^J P(Y = j) = 1$，推导出各类别概率：

$$
P(Y = j \mid \mathbf{x}) = \frac{\exp(\alpha_j + \mathbf{x}^T \boldsymbol{\beta}_j)}{1 + \sum_{k=1}^{J-1} \exp(\alpha_k + \mathbf{x}^T \boldsymbol{\beta}_k)}, \quad j = 1, \dots, J-1
$$

$$
P(Y = J \mid \mathbf{x}) = \frac{1}{1 + \sum_{k=1}^{J-1} \exp(\alpha_k + \mathbf{x}^T \boldsymbol{\beta}_k)}
$$

---

## 2. 系数解释：相对风险比 (Relative Risk Ratio, RRR)

对于第 $j$ 个类别方程中的系数 $\beta_{jk}$：
$$
\text{RRR}_{j} = \frac{P(Y = j \mid x_k + 1) / P(Y = J \mid x_k + 1)}{P(Y = j \mid x_k) / P(Y = J \mid x_k)} = \exp(\beta_{jk})
$$
* **解释口径**：在控制其他变量不变时，$x_k$ 每增加 1 个单位，**选择类别 $j$ 相对于基准类别 $J$ 的相对几率比（RRR）乘以 $\exp(\beta_{jk})$ 倍**。

---

## 3. 无关备选独立性 (IIA 假设与红蓝巴士悖论)

基准类别 Logit 隐含了**无关备选独立性公理（Independence of Irrelevant Alternatives, IIA）**：任意两个选项 $j$ 与 $k$ 的相对几率比 $\frac{P(Y=j)}{P(Y=k)}$ 仅取决于这两个选项本身的属性，与备选集中是否存在第三个选项完全无关。

> [!WARNING]
> **红蓝巴士悖论 (Red Bus / Blue Bus Paradox)**：若初始交通方式为汽车（50%）与红巴士（50%），引入蓝巴士后，由于蓝巴士与红巴士高度可替代，真实概率应为汽车（50%）、红巴士（25%）、蓝巴士（25%）。但多项 Logit 会错误预测为汽车（33%）、红巴士（33%）、蓝巴士（33%）。
> **对策**：当选项间存在高度相似性时，应使用**巢式 Logit（Nested Logit）**或**多项 Probit（Multinomial Probit）**。

---

## 4. Python statsmodels MNLogit 实战

```python
import statsmodels.api as sm
import pandas as pd
import numpy as np

# 模拟 3 分类名义响应数据 (例如车型选择: 0=轿车, 1=SUV, 2=卡车)
np.random.seed(42)
n = 300
income = np.random.normal(50, 15, n)
urban = np.random.binomial(1, 0.6, n)

X = sm.add_constant(pd.DataFrame({'income': income, 'urban': urban}))
# 生成真实 Softmax 概率
V0 = 0.0
V1 = -1.5 + 0.03 * income - 0.8 * urban
V2 = -2.5 + 0.05 * income + 0.5 * urban
denom = 1 + np.exp(V1) + np.exp(V2)
p0 = 1 / denom
p1 = np.exp(V1) / denom
p2 = np.exp(V2) / denom

probs = np.column_stack([p0, p1, p2])
y = [np.random.choice([0, 1, 2], p=p) for p in probs]

# 拟合多项 Logistic 模型 (以 0 为基准)
mn_model = sm.MNLogit(y, X).fit()
print(mn_model.summary())
print("\n相对风险比 (RRR):")
print(np.exp(mn_model.params))
```

---

## 5. 核心自测与检索练习

- [ ] 写出基准类别 Logit 模型的公式，并说明为什么只需要 $J-1$ 个方程。
- [ ] 解释 RRR（相对风险比）与二分类模型中 OR 的联系与区别。
- [ ] 什么是 IIA 假设？用红蓝巴士例子说明违反 IIA 假设时会带来什么偏差。

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
