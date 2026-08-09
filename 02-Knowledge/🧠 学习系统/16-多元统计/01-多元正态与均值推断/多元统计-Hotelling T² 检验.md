---
type: study
topic: "Hotelling T² 检验"
course: "16-多元统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段1-多元正态与均值推断]]"
upstream: ["[[多元统计-均值向量与协方差矩阵估计]]"]
flow: knowledge
kind: derivation
difficulty: intermediate
concept: ["Hotelling T²", "多元均值检验", "F分布转换", "仿射不变性", "置信椭球", "Wishart分布"]
tags: [学习, 多元统计, 假设检验, 均值推断, 矩阵推导]
---

# 多元统计-Hotelling T² 检验

## 1. 为什么不能对多个变量逐个做一元 t 检验？

在分析多指标数据（例如 6 项瑞士钞票尺寸指标或 13 项葡萄酒化学成分）时，如果对每个变量分别进行单变量 $t$ 检验：
1. **多重比较错误累积 (Type I Error Inflation)**：$p$ 个独立检验的总体假阳性率膨胀至 $1 - (1-\alpha)^p$（当 $p=6, \alpha=0.05$ 时，至少一次误报概率高达 $26.5\%$）；
2. **完全忽略变量间相关结构**：即使每个单独变量的均值差异都不显著，在多维联合空间中样本点可能已经显著偏离总体均值椭球；
3. **坐标轴依赖性（缺乏旋转不变性）**：单变量检验依赖变量选取方向，而真实空间中的均值差异往往出现在倾斜的对角轴方向上。

**Hotelling $T^2$ 检验**是一元 Student's $t$ 检验在高维向量空间的完美推广，具有严格的 **$GL(p)$ 仿射不变性**。

---

## 2. 单样本 Hotelling T² 检验理论与推导

### 2.1 假设设定与统计量构造

设 $\mathbf{X}_1, \dots, \mathbf{X}_n \overset{iid}{\sim} N_p(\boldsymbol{\mu}, \mathbf{\Sigma})$（$n > p$），检验假设：
$$H_0: \boldsymbol{\mu} = \boldsymbol{\mu}_0 \quad \text{vs} \quad H_1: \boldsymbol{\mu} \neq \boldsymbol{\mu}_0$$
定义 **Hotelling $T^2$ 统计量**：
$$T^2 = n (\bar{\mathbf{X}} - \boldsymbol{\mu}_0)^T \mathbf{S}^{-1} (\bar{\mathbf{X}} - \boldsymbol{\mu}_0)$$
其中样本协方差矩阵 $\mathbf{S} = \frac{1}{n-1}\sum_{i=1}^n (\mathbf{X}_i - \bar{\mathbf{X}})(\mathbf{X}_i - \bar{\mathbf{X}})^T$。

### 2.2 似然比检验 (LRT) 原理导引与 $T^2$ 的第一性原理导出

Hotelling $T^2$ 并非人为拼凑的二次型，而是从极大似然比检验 (Likelihood Ratio Test) 严格推导出的唯一统计量。
在原假设 $H_0: \boldsymbol{\mu} = \boldsymbol{\mu}_0$ 与全空间 $H_1$ 下，似然函数的最大值分别为 $L(\hat{\Omega}_0)$ 与 $L(\hat{\Omega})$。
似然比统计量：
$$\Lambda = \frac{\max_{H_0} L(\boldsymbol{\mu}_0, \mathbf{\Sigma})}{\max_{H_1} L(\boldsymbol{\mu}, \mathbf{\Sigma})} = \left( \frac{|\hat{\mathbf{\Sigma}}|}{|\hat{\mathbf{\Sigma}}_0|} \right)^{n/2}$$
利用行列式分块求逆展开（Schur 补）：
$$|\hat{\mathbf{\Sigma}}_0| = \left| \hat{\mathbf{\Sigma}} + (\bar{\mathbf{X}} - \boldsymbol{\mu}_0)(\bar{\mathbf{X}} - \boldsymbol{\mu}_0)^T \right| = |\hat{\mathbf{\Sigma}}| \cdot \left( 1 + (\bar{\mathbf{X}} - \boldsymbol{\mu}_0)^T \hat{\mathbf{\Sigma}}^{-1} (\bar{\mathbf{X}} - \boldsymbol{\mu}_0) \right)$$
代入可得似然比与 $T^2$ 的单调单射关系：
$$\Lambda = \left( 1 + \frac{T^2}{n-1} \right)^{-n/2} \iff T^2 = (n-1) \left( \Lambda^{-2/n} - 1 \right)$$
这证明了拒绝小 $\Lambda$ 完全等价于拒绝大 $T^2$，即 Hotelling $T^2$ 是多元正态均值检验的**一致最高功效无偏检验 (UMPU)**！

### 2.3 精确 F 分布转换定理与证明概要

> [!IMPORTANT]
> **定理 (Hotelling-Lawley 精确分布)**：
> 在原假设 $H_0$ 成立且总体服从多元正态分布的条件下：
> $$F = \frac{n - p}{(n - 1) p} T^2 \sim F(p, n - p)$$

**第一性原理证明思路**：
1. 样本均值 $\sqrt{n}(\bar{\mathbf{X}} - \boldsymbol{\mu}_0) \sim N_p(\mathbf{0}, \mathbf{\Sigma})$；
2. 样本离差阵 $\mathbf{A} = (n-1)\mathbf{S} \sim W_p(n-1, \mathbf{\Sigma})$ 服从自由度为 $n-1$ 的 Wishart 分布，且与 $\bar{\mathbf{X}}$ 统计独立；
3. 记向量 $\mathbf{Z} = \sqrt{n}\mathbf{\Sigma}^{-1/2}(\bar{\mathbf{X}} - \boldsymbol{\mu}_0) \sim N_p(\mathbf{0}, \mathbf{I})$，矩阵 $\mathbf{W} = \mathbf{\Sigma}^{-1/2}\mathbf{A}\mathbf{\Sigma}^{-1/2} \sim W_p(n-1, \mathbf{I})$；
4. 统计量转化为 $T^2 = (n-1) \mathbf{Z}^T \mathbf{W}^{-1} \mathbf{Z}$；
5. 给定 $\mathbf{Z}$，标量 $\frac{\mathbf{Z}^T \mathbf{Z}}{\mathbf{Z}^T \mathbf{W}^{-1} \mathbf{Z}} \sim \chi^2(n-p)$，而分子 $\|\mathbf{Z}\|^2 \sim \chi^2(p)$；
6. 两个独立卡方变量之比与自由度相除，精确诱导出 $F(p, n-p)$ 分布！

---

## 3. 两独立样本 Hotelling T² 检验

设两组样本分别来自 $N_p(\boldsymbol{\mu}_1, \mathbf{\Sigma})$ 和 $N_p(\boldsymbol{\mu}_2, \mathbf{\Sigma})$（假定协方差矩阵相等）：
$$H_0: \boldsymbol{\mu}_1 = \boldsymbol{\mu}_2 \quad \text{vs} \quad H_1: \boldsymbol{\mu}_1 \neq \boldsymbol{\mu}_2$$
合并样本协方差矩阵：
$$\mathbf{S}_{pooled} = \frac{(n_1 - 1)\mathbf{S}_1 + (n_2 - 1)\mathbf{S}_2}{n_1 + n_2 - 2}$$
两样本 $T^2$ 统计量：
$$T^2 = \frac{n_1 n_2}{n_1 + n_2} (\bar{\mathbf{X}}_1 - \bar{\mathbf{X}}_2)^T \mathbf{S}_{pooled}^{-1} (\bar{\mathbf{X}}_1 - \bar{\mathbf{X}}_2)$$
**精确 $F$ 分布转换**：
$$F = \frac{n_1 + n_2 - p - 1}{(n_1 + n_2 - 2) p} T^2 \sim F(p, n_1 + n_2 - p - 1)$$

---

## 4. 仿射不变性定理 (Affine Invariance)

设 $\mathbf{C} \in GL(p)$ 为任意 $p \times p$ 满秩可逆常数矩阵，$\mathbf{d} \in \mathbb{R}^p$ 为常数向量。
令数据变换为 $\mathbf{Y}_i = \mathbf{C}\mathbf{X}_i + \mathbf{d}$。
- $\bar{\mathbf{Y}} = \mathbf{C}\bar{\mathbf{X}} + \mathbf{d}$
- $\mathbf{S}_{\mathbf{Y}} = \mathbf{C} \mathbf{S}_{\mathbf{X}} \mathbf{C}^T \implies \mathbf{S}_{\mathbf{Y}}^{-1} = (\mathbf{C}^T)^{-1} \mathbf{S}_{\mathbf{X}}^{-1} \mathbf{C}^{-1}$
代入 $T^2$ 统计量：
$$T_{\mathbf{Y}}^2 = n (\mathbf{C}\bar{\mathbf{X}} - \mathbf{C}\boldsymbol{\mu}_0)^T (\mathbf{C} \mathbf{S}_{\mathbf{X}} \mathbf{C}^T)^{-1} (\mathbf{C}\bar{\mathbf{X}} - \mathbf{C}\boldsymbol{\mu}_0) = n (\bar{\mathbf{X}} - \boldsymbol{\mu}_0)^T \mathbf{C}^T (\mathbf{C}^T)^{-1} \mathbf{S}_{\mathbf{X}}^{-1} \mathbf{C}^{-1} \mathbf{C} (\bar{\mathbf{X}} - \boldsymbol{\mu}_0) = T_{\mathbf{X}}^2$$
> [!TIP]
> 这证明了 Hotelling $T^2$ **对任意线性坐标变换、缩放与正交旋转完全免疫**，是度量多元均值差异的本原几何统计量！

---

## 5. Python 实战代码：真实瑞士钞票真伪均值向量推断

```python
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, r"f:\-\03-Projects\16-多元统计\scripts")
from load_data import load_swiss_banknotes
from mva_toolkit import hotelling_t2_two_sample

# 1. 加载真实瑞士真伪钞票数据 (200 张 x 6 个测量指标)
df_bank = load_swiss_banknotes()
cols = ['Length', 'Left', 'Right', 'Bottom', 'Top', 'Diagonal']
X_genuine = df_bank[df_bank['Is_Counterfeit'] == 0][cols].values
X_counterfeit = df_bank[df_bank['Is_Counterfeit'] == 1][cols].values

# 2. 执行两样本 Hotelling T^2 检验
res = hotelling_t2_two_sample(X_genuine, X_counterfeit)

print("=== 瑞士真伪钞票均值向量差异两样本 Hotelling T^2 检验 ===")
print(f"Hotelling T^2 统计量: {res['T2']:.2f}")
print(f"转换后精确 F 统计量: {res['F_stat']:.2f} (df1={res['df1']}, df2={res['df2']})")
print(f"检验 p-value: {res['p_value']:.2e}")

assert res['p_value'] < 1e-10
print("✅ 结论：在 alpha=0.001 显著性水平下强烈拒绝原假设，真钞与伪钞在 6 维几何空间中均值向量差异极显著！")
```

---

## 6. 检索自测练习

1. 证明当维度 $p=1$ 时，单样本 Hotelling $T^2$ 统计量严格退化为 Student's $t$ 统计量的平方。
2. 解释若样本量 $n \le p$，样本协方差矩阵 $\mathbf{S}$ 会发生什么？此时如何修改检验方法？

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
