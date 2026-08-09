---
type: study
course: "属性数据分析"
topic: "Logistic模型拟合优度与完全分离诊断"
stage_moc: "[[🧭 阶段2-二项响应与Logistic回归]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: ["偏差检验", "Hosmer-Lemeshow检验", "完全分离", "准完全分离", "Firth惩罚似然"]
prerequisites: ["[[属性数据分析-Logistic模型参数估计与Fisher得分算法]]"]
upstream: ["[[属性数据分析-Logistic模型参数估计与Fisher得分算法]]"]
status: completed
tags: [学习, 属性数据分析, 模型诊断, 完全分离, 拟合优度]
created: 2026-08-09
---

# 属性数据分析-Logistic模型拟合优度与完全分离诊断

## 1. 拟合优度与模型偏差 (Deviance)

### 1.1 偏差 (Deviance) 的定义
偏差衡量当前拟合模型与具有完美拟合能力的**饱和模型（Saturated Model，为每个唯一样本点分配独立参数 $\hat{\pi}_i = y_i$）**的对数似然差距：

$$
D = 2 \left[ \ell(\text{饱和模型}) - \ell(\text{当前模型}) \right] = 2 \sum_{i=1}^n \left[ y_i \ln\left(\frac{y_i}{\hat{\mu}_i}\right) + (n_i - y_i) \ln\left(\frac{n_i - y_i}{n_i - \hat{\mu}_i}\right) \right]
$$

### 1.2 分组成组数据 (Grouped Data) vs 未分组二元数据 (Ungrouped Data)
> [!WARNING]
> **常见陷阱**：
> - **对于成组数据（每个自变量配置下试验次数 $n_i \ge 5$）**：$D \xrightarrow{d} \chi^2_{N - p}$，可直接作为拟合优度绝对检验统计量。
> - **对于未分组数据（每个样本 $n_i = 1, y_i \in \{0, 1\}$）**：随着样本量 $n \to \infty$，饱和模型的参数个数也趋于无穷大，导致 $D$ **不再服从卡方分布**！此时不可直接用 $D$ 的 $p$ 值检验模型拟合优度。

---

## 2. Hosmer-Lemeshow (HL) 拟合优度检验

针对连续协变量未分组二元数据，Hosmer 与 Lemeshow (1980) 提出了分组检验：
1. 按模型预测概率 $\hat{\pi}_i$ 从小到大排序，等分成 $G$ 组（通常 $G = 10$，即十分位数组）。
2. 计算每组内的实际观测事件数 $O_{1g} = \sum_{i \in g} y_i$ 与模型期望事件数 $E_{1g} = \sum_{i \in g} \hat{\pi}_i$。
3. 构建类似 Pearson 卡方的检验统计量：
   $$
   H = \sum_{g=1}^G \frac{(O_{1g} - E_{1g})^2}{E_{1g}} + \sum_{g=1}^G \frac{(O_{0g} - E_{0g})^2}{E_{0g}} \xrightarrow{d} \chi^2_{G - 2}
   $$
* **判定规则**：$p > 0.05$ 表示未发现显著失拟（模型拟合可接受）；$p < 0.05$ 表示模型存在显著失拟（缺少重要非线性项或交互项）。

---

## 3. 完全分离 (Complete Separation) 与准完全分离

### 3.1 现象与数学成因 (Albert & Anderson, 1984)
* **完全分离（Complete Separation）**：存在一个超平面，能将 $y=1$ 与 $y=0$ 的样本点** 100% 完美分开**（如 $x > 5 \implies y=1$；$x \le 5 \implies y=0$）。
* **准完全分离（Quasi-complete Separation）**：超平面能完美分割两类，但在分割面上恰好存在若干样本点。

```
完全分离示意:
y=0:  o   o   o   o
--------------------| (超平面 x = c)
y=1:                  *   *   *   *
```

### 3.2 算法发散表现
在分离存在时，为了使交叉熵损失达到 0，MLE 的参数估计值会向无穷大发散：
$$
\hat{\beta} \to \pm \infty, \quad \text{SE}(\hat{\beta}) \to \infty
$$
统计软件常报错：*“Algorithm did not converge”* 或输出荒谬的 $\hat{\beta} = 18.5, \text{SE} = 4582.1, p = 0.998$。

---

## 4. 解决方案：Firth 惩罚似然估计 (Firth's Penalized Likelihood)

David Firth (1993) 提出在对数似然函数中引入 Jeffreys 先验作为惩罚项：

$$
\ell_{\text{Firth}}(\boldsymbol{\beta}) = \ell(\boldsymbol{\beta}) + \frac{1}{2} \ln |\mathcal{I}(\boldsymbol{\beta})|
$$

* **优异性质**：
  1. 惩罚项在参数趋向无穷时提供向原点的拉力，在数学上严格保证了即便在完全分离下，参数估计值也**处处有限且唯一存在**；
  2. 将小样本下 MLE 的 $O(n^{-1})$ 阶一阶渐近偏倚完全消除，得到更精确的无偏估计。

---

## 5. Python 实战代码（HL 检验与分离诊断）

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import scipy.stats as stats

def hosmer_lemeshow_test(y_true, y_pred, g=10):
    # Hosmer-Lemeshow 拟合优度检验
    df = pd.DataFrame({'y': y_true, 'pred': y_pred})
    df['group'] = pd.qcut(df['pred'], q=g, duplicates='drop')
    
    hl_table = df.groupby('group', observed=False).agg(
        obs=('y', 'sum'),
        total=('y', 'count'),
        exp=('pred', 'sum')
    )
    hl_table['obs_0'] = hl_table['total'] - hl_table['obs']
    hl_table['exp_0'] = hl_table['total'] - hl_table['exp']
    
    # 统计量
    h_stat = np.sum(
        (hl_table['obs'] - hl_table['exp'])**2 / hl_table['exp'] +
        (hl_table['obs_0'] - hl_table['exp_0'])**2 / hl_table['exp_0']
    )
    dof = len(hl_table) - 2
    p_val = 1 - stats.chi2.cdf(h_stat, df=dof)
    return h_stat, dof, p_val

# 模拟数据
np.random.seed(42)
x = np.random.normal(size=200)
y = np.random.binomial(1, 1 / (1 + np.exp(-(-0.2 + 1.1*x))))
model = sm.Logit(y, sm.add_constant(x)).fit(disp=False)

h_stat, dof, p_val = hosmer_lemeshow_test(y, model.predict())
print(f"HL 统计量: {h_stat:.4f}, df: {dof}, p-value: {p_val:.4f}")
```

---

## 6. 核心自测与检索练习

- [ ] 为什么在未分组二分类数据下，不能直接查卡方分布表用残差偏差 $D$ 来判断模型拟合是否良好？
- [ ] 简述 Hosmer-Lemeshow 检验的构建流程与自由度计算规则。
- [ ] 解释完全分离的几何直观，并说明 Firth 惩罚极大似然法是如何从数学上解决估计值发散问题的。

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
