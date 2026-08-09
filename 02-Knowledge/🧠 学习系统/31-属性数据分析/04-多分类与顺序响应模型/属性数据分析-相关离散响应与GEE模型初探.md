---
type: study
course: "属性数据分析"
topic: "相关离散响应与GEE模型初探"
stage_moc: "[[🧭 阶段4-多分类与顺序响应模型]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["GEE", "广义估计方程", "重复测量", "工作相关矩阵", "稳健三明治方差"]
prerequisites: ["[[属性数据分析-广义线性模型GLM框架与链接函数]]", "[[属性数据分析-二项Logistic回归模型与参数解释]]"]
upstream: ["[[属性数据分析-广义线性模型GLM框架与链接函数]]", "[[属性数据分析-二项Logistic回归模型与参数解释]]"]
status: completed
tags: [学习, 属性数据分析, GEE, 重复测量, 相关响应, 稳健统计]
created: 2026-08-09
---

# 属性数据分析-相关离散响应与GEE模型初探

## 1. 重复测量与整群分类数据挑战

当同一个体在不同时间点被多次测量（纵向数据 Longitudinal Data）或个体属于同一家庭/班级（整群数据 Clustered Data）时，同一集群内的观测值**不再相互独立**，存在显著正相关。

若直接套用标准 GLM：
- 参数估计 $\hat{\boldsymbol{\beta}}$ 依然是一致的；
- **标准误被严重低估**，导致虚假显著性。

---

## 2. 边际模型与广义估计方程 (GEE)

Liang 与 Zeger (1986) 提出了**广义估计方程（Generalized Estimating Equations, GEE）**，属于**边际模型（Marginal / Population-Averaged Model）**。

### 2.1 边际均值与工作相关矩阵
设集群 $i$ 有 $n_i$ 次测量，响应向量为 $\mathbf{Y}_i = (Y_{i1}, \dots, Y_{in_i})^T$：
1. **边际均值结构**：$g(\mu_{it}) = \mathbf{x}_{it}^T \boldsymbol{\beta}$；
2. **工作相关矩阵（Working Correlation Matrix, $R(\boldsymbol{\alpha})$）**：
   $$
   V_i = \text{Var}(\mathbf{Y}_i) = A_i^{1/2} R(\boldsymbol{\alpha}) A_i^{1/2}
   $$
   其中 $A_i = \text{diag}(V(\mu_{i1}), \dots, V(\mu_{in_i}))$。常见结构包括：独立（Independence）、可交换/等相关（Exchangeable）、自回归（AR(1)）、无约束（Unstructured）。

### 2.2 GEE 估计方程
$$
\sum_{i=1}^N D_i^T V_i^{-1} (\mathbf{Y}_i - \boldsymbol{\mu}_i) = \mathbf{0}
$$
其中 $D_i = \frac{\partial \boldsymbol{\mu}_i}{\partial \boldsymbol{\beta}}$。

---

## 3. 稳健三明治方差估计量 (Huber-White Sandwich Estimator)

> [!IMPORTANT]
> **GEE 最具威力的性质**：
> 即使我们**猜错了工作相关矩阵的结构**（例如真结构是 AR(1) 但我们假定了 Exchangeable），只要均值模型设定正确且集群数 $N \to \infty$，GEE 参数估计值 $\hat{\boldsymbol{\beta}}$ 依然强一致，且通过**经验三明治方差估计量（Empirical Sandwich Variance Estimator）**计算的标准误**依然无偏且渐近正确**！

$$
\widehat{\text{Var}}_{\text{sandwich}}(\hat{\boldsymbol{\beta}}) = M_0^{-1} \left( \sum_{i=1}^N D_i^T V_i^{-1} (\mathbf{Y}_i - \hat{\boldsymbol{\mu}}_i)(\mathbf{Y}_i - \hat{\boldsymbol{\mu}}_i)^T V_i^{-1} D_i \right) M_0^{-1}
$$
其中 $M_0 = \sum_{i=1}^N D_i^T V_i^{-1} D_i$。

---

## 4. Python statsmodels GEE 实战

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import numpy as np

# 模拟纵向重复测量二分类数据 (50 名患者, 每人 4 次随访)
np.random.seed(42)
n_patients = 50
n_visits = 4
patient_id = np.repeat(np.arange(n_patients), n_visits)
visit = np.tile(np.arange(n_visits), n_patients)
drug = np.repeat(np.random.binomial(1, 0.5, n_patients), n_visits)

# 考虑个体随机效应生成相关二分类数据
u_i = np.repeat(np.random.normal(0, 1.0, n_patients), n_visits)
eta = -1.0 + 0.8 * drug - 0.3 * visit + u_i
prob = 1 / (1 + np.exp(-eta))
y = np.random.binomial(1, prob)

df = pd.DataFrame({'patient': patient_id, 'visit': visit, 'drug': drug, 'y': y})

# 拟合 GEE 模型 (Exchangeable 相关结构)
gee_model = smf.gee('y ~ drug + visit',
                    groups='patient',
                    data=df,
                    family=sm.families.Binomial(),
                    cov_struct=sm.cov_struct.Exchangeable()).fit()

print(gee_model.summary())
print("\n稳健标准误 (Robust SE):", gee_model.bse)
```

---

## 🃏 Anki 卡片

### Card 1: GEE 估计方程与工作相关矩阵
- **Front**: 写出 GEE（广义估计方程）的准似然估计方程，并说明 $V_i$ 矩阵的构造。
- **Back**: 
  - 估计方程：$\sum_{i=1}^N D_i^T V_i^{-1} (\mathbf{Y}_i - \boldsymbol{\mu}_i) = \mathbf{0}$
  - 矩阵构造：$D_i = \frac{\partial \boldsymbol{\mu}_i}{\partial \boldsymbol{\beta}}$，$V_i = A_i^{1/2} R(\boldsymbol{\alpha}) A_i^{1/2}$。
  - 其中 $A_i = \text{diag}(V(\mu_{it}))$ 刻画边际方差，$R(\boldsymbol{\alpha})$ 为假设的工作相关矩阵（如 Exchangeable / AR(1)）。

### Card 2: 稳健三明治方差估计量 (Sandwich Estimator)
- **Front**: 为什么 GEE 模型的三明治方差估计量在工作相关矩阵 $R(\boldsymbol{\alpha})$ 误设时依然渐近无偏？
- **Back**: 
  - 三明治公式：$\text{Var}(\hat{\boldsymbol{\beta}}) = M_0^{-1} M_1 M_0^{-1}$，其中 $M_0 = \sum D_i^T V_i^{-1} D_i$，$M_1 = \sum D_i^T V_i^{-1} \mathbf{e}_i \mathbf{e}_i^T V_i^{-1} D_i$（$\mathbf{e}_i = \mathbf{Y}_i - \boldsymbol{\mu}_i$）。
  - 原因：中间项 $M_1$ 直接使用集群残差的外积 $\mathbf{e}_i \mathbf{e}_i^T$ 经验替换真协方差 $\text{Var}(\mathbf{Y}_i)$。由大数定律，当集群数 $N \to \infty$ 时，经验残差外积强一致收敛于真协方差，从而面包与肉的结构抵消了误设 $R(\boldsymbol{\alpha})$ 带来的偏差。

---

## 5. 核心自测与检索练习

- [ ] 什么是边际模型（GEE）与条件模型（GLMM / 随机效应模型）的区别？
- [ ] 为什么说 GEE 的稳健三明治方差估计量对工作相关矩阵的误设具有免疫力？
- [ ] 简述在临床试验纵向数据中，忽略重复测量的自相关性会导致什么统计推断风险。

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

