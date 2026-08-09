---
type: study
course: "属性数据分析"
topic: "分层列联表与CMH检验"
stage_moc: "[[🧭 阶段1-列联表与关联推断]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: ["Simpson悖论", "分层列联表", "CMH检验", "条件优势比", "混杂偏倚"]
prerequisites: ["[[属性数据分析-关联效应量-优势比与相对风险]]", "[[属性数据分析-独立性与拟合优度检验]]"]
upstream: ["[[属性数据分析-关联效应量-优势比与相对风险]]", "[[属性数据分析-独立性与拟合优度检验]]"]
status: completed
tags: [学习, 属性数据分析, 分层分析, CMH检验, 因果推断]
created: 2026-08-09
---

# 属性数据分析-分层列联表与CMH检验

## 1. 混杂因素与 Simpson 悖论

当引入第三个变量 $Z$（分层变量 / 混杂变量，水平 $k = 1, \dots, K$）时，我们得到 $I \times J \times K$ **三维分层列联表**。

### 1.1 条件关联 vs 边际关联
- **条件优势比（Conditional Odds Ratio, $\theta_{XY(k)}$）**：在第 $k$ 个层（$Z = k$）内，$X$ 与 $Y$ 的优势比。
- **边际优势比（Marginal Odds Ratio, $\theta_{XY}$）**：将所有层按频数直接合并为二维表后算出的优势比。

### 1.2 Simpson 悖论（Simpson's Paradox）
> [!WARNING]
> **现象**：边际表格中的关联方向，可能与**每一个子层内的条件关联方向完全相反**！
> 经典案例：UC Berkeley 录取数据中，总体上看男生的录取率显著高于女生（边际 $\text{OR} > 1$）；但在按报考院系 $Z$ 分层后，几乎每个系内女生的录取率均略高于或等于男生（条件 $\text{OR} \le 1$）。这是因为女生更倾向于申请录取率极低的竞争激烈院系。

---

## 2. 同质性关联假设 (Homogeneous Association)

若在所有层中，条件优势比均相等：
$$
H_0: \theta_{XY(1)} = \theta_{XY(2)} = \dots = \theta_{XY(K)} = \theta_{XY}
$$
则称 $X$ 与 $Y$ 存在**同质性关联（Homogeneous Association）**（即模型中无三阶交互效应 $X \times Y \times Z$）。可用 **Breslow-Day 检验** 或 **Tarone 修正检验** 来检验同质性。

---

## 3. Cochran-Mantel-Haenszel (CMH) 检验

在满足同质性关联前提下，若要检验在控制分层变量 $Z$ 后，$X$ 与 $Y$ 是否**条件独立**（$H_0: \theta_{XY(1)} = \dots = \theta_{XY(K)} = 1$），使用著名的 **CMH 检验**。

### 3.1 统计量推导
在第 $k$ 层 $2 \times 2$ 表中，固定边际下 $n_{11k}$ 服从超几何分布：
$$
\mathbb{E}[n_{11k} \mid H_0] = \frac{n_{1+k} n_{+1k}}{n_{++k}}
$$
$$
\text{Var}(n_{11k} \mid H_0) = \frac{n_{1+k} n_{2+k} n_{+1k} n_{+2k}}{n_{++k}^2 (n_{++k} - 1)}
$$

CMH 统计量汇总各层的超几何偏差：

$$
M^2 = \frac{\left( \left| \sum_{k=1}^K n_{11k} - \sum_{k=1}^K \mathbb{E}[n_{11k}] \right| - 0.5 \right)^2}{\sum_{k=1}^K \text{Var}(n_{11k})} \xrightarrow{d} \chi^2_1
$$

### 3.2 共同优势比的 Mantel-Haenszel 估计量 ($\hat{\theta}_{MH}$)
若拒绝条件独立，我们估计各层的共同综合优势比：

$$
\hat{\theta}_{MH} = \frac{\sum_{k=1}^K \frac{n_{11k} n_{22k}}{n_{++k}}}{\sum_{k=1}^K \frac{n_{12k} n_{21k}}{n_{++k}}}
$$

该估计量具有极优良的大样本性质，即使当层数 $K \to \infty$ 而每层样本量极小时（稀疏分层数据），$\hat{\theta}_{MH}$ 依然是一致估计量！

---

## 4. Python statsmodels CMH 实战

```python
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.contingency_tables import StratifiedTable

# 构造 2x2x2 分层列联表 (UCB 简化两院系数据)
# 维度: (Dept, Gender, Admit)
# Dept A: Male [512, 313], Female [89, 19]
# Dept B: Male [353, 207], Female [17, 8]
tables = np.array([
    [[512, 313],
     [89, 19]],
    [[353, 207],
     [17, 8]]
])

st = StratifiedTable(tables)

print("共同优势比 (MH OR):", st.oddsratio_pooled)
print("CMH 检验统计量与 p 值:", st.test_null_odds())
print("Breslow-Day 同质性检验 p 值:", st.test_equal_odds())
```

---

## 5. 核心自测与检索练习

- [ ] 什么是 Simpson 悖论？用直观语言解释它是如何产生的。
- [ ] 什么是同质性关联假设？若 Breslow-Day 检验 $p < 0.01$，我们还能直接汇报单一的 $\hat{\theta}_{MH}$ 吗？为什么？
- [ ] 为什么说 CMH 检验统计量是各层超几何分布偏差的加权组合？

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
