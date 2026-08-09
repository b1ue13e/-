---
type: study
topic: "多元方差分析 MANOVA"
course: "16-多元统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段1-多元正态与均值推断]]"
upstream: ["[[多元统计-Hotelling T² 检验]]"]
flow: knowledge
kind: derivation
difficulty: advanced
concept: ["多元方差分析", "MANOVA", "Wilks Lambda", "Pillai 迹", "Hotelling-Lawley 迹", "Roy 最大根", "广义特征值"]
tags: [学习, 多元统计, 假设检验, 方差分析, 矩阵推导]
---

# 多元统计-多元方差分析MANOVA

## 1. 为什么有了单变量 ANOVA 还需要 MANOVA？

在多组（$g \ge 3$）多变量（$p \ge 2$）实验设计中（例如比较 3 种不同产区葡萄酒的 13 种化学成分，或 4 种教学方法对学生数学、物理、化学 3 科成绩的综合影响）：
1. **多重检验假阳性率严重累积**；
2. **完全忽略响应变量之间的协方差相关结构**：组间差异可能不在任何单一变量轴上，而是体现在响应变量的联合子空间上；
3. **ANOVA 无法控制多维效应量**。

**多元方差分析 (Multivariate Analysis of Variance, MANOVA)** 是单因素/多因素方差分析在向量响应变量空间的严格推广。

---

## 2. 矩阵离差平方和分解与广义特征值主线

### 2.1 假设设定与矩阵分解

设共有 $g$ 个独立处理组，第 $i$ 组有 $n_i$ 个 $p$ 维观测样本 $\mathbf{X}_{ij} \sim N_p(\boldsymbol{\mu}_i, \mathbf{\Sigma})$，总样本量 $N = \sum_{i=1}^g n_i$。
检验原假设：
$$H_0: \boldsymbol{\mu}_1 = \boldsymbol{\mu}_2 = \dots = \boldsymbol{\mu}_g \quad \text{vs} \quad H_1: \text{至少存在两个组的均值向量不等}$$

定义总离差阵 $\mathbf{T}$、组间假设离差阵 $\mathbf{H}$（Hypothesis SSP）与组内误差离差阵 $\mathbf{E}$（Error SSP）：
$$\mathbf{T} = \sum_{i=1}^g \sum_{j=1}^{n_i} (\mathbf{X}_{ij} - \bar{\mathbf{X}})(\mathbf{X}_{ij} - \bar{\mathbf{X}})^T$$
$$\mathbf{H} = \sum_{i=1}^g n_i (\bar{\mathbf{X}}_i - \bar{\mathbf{X}})(\bar{\mathbf{X}}_i - \bar{\mathbf{X}})^T \quad (df_H = g - 1)$$
$$\mathbf{E} = \sum_{i=1}^g \sum_{j=1}^{n_i} (\mathbf{X}_{ij} - \bar{\mathbf{X}}_i)(\mathbf{X}_{ij} - \bar{\mathbf{X}}_i)^T \quad (df_E = N - g)$$
严格满足矩阵恒等式：
$$\mathbf{T} = \mathbf{H} + \mathbf{E}$$

### 2.2 广义特征值：MANOVA 的第一性原理

求解广义特征值问题：
$$\mathbf{H}\mathbf{v} = \lambda \mathbf{E}\mathbf{v} \iff \mathbf{E}^{-1}\mathbf{H}\mathbf{v} = \lambda \mathbf{v}$$
设非零特征值为 $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_s > 0$，其中非零特征值个数 $s = \min(p, g - 1)$。
$\lambda_k$ 度量了组间离散度相对组内离散度在第 $k$ 个正交判别方向上的最大分离比例。

---

## 3. MANOVA 四大多元检验统计量

所有四大经典多元检验统计量均是这组广义特征值 $\lambda_k$ 的直接显式函数：

| 统计量名称 | 数学定义 (基于广义特征值 $\lambda_k$) | 矩阵形式表达 | 稳健性与统计功效特征 |
| :--- | :--- | :--- | :--- |
| **Wilks' $\Lambda$** | $\Lambda = \prod_{k=1}^s \frac{1}{1 + \lambda_k}$ | $\frac{|\mathbf{E}|}{|\mathbf{H} + \mathbf{E}|} = \frac{|\mathbf{E}|}{|\mathbf{T}|}$ | 最经典的广义似然比统计量，似然解释性强 |
| **Pillai's Trace** | $V = \sum_{k=1}^s \frac{\lambda_k}{1 + \lambda_k}$ | $\operatorname{tr}(\mathbf{H}(\mathbf{H}+\mathbf{E})^{-1})$ | **对协方差非齐性与非正态偏离最稳健（推荐首选）** |
| **Hotelling-Lawley Trace** | $U = \sum_{k=1}^s \lambda_k$ | $\operatorname{tr}(\mathbf{H}\mathbf{E}^{-1})$ | 与 Hotelling $T^2$ 直接推广对应 |
| **Roy's Largest Root** | $\theta = \frac{\lambda_1}{1 + \lambda_1}$ | $\lambda_{\max}(\mathbf{H}(\mathbf{H}+\mathbf{E})^{-1})$ | 当组间差异集中在单一主方向时功效最大 |

---

## 4. Python 实战代码：真实 UCI Wine 数据集产区 MANOVA 检验

```python
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, r"f:\-\03-Projects\16-多元统计\scripts")
from load_data import load_wine_data
from mva_toolkit import manova_fit

# 1. 加载 3 个葡萄酒品种 (Cultivar 0, 1, 2) 的 13 项化学指标
df_wine = load_wine_data()
features = [c for c in df_wine.columns if c != 'Cultivar']
X = df_wine[features].values
y = df_wine['Cultivar'].values

# 2. 运行 MANOVA 拟合
manova_res = manova_fit(X, y)

print("=== UCI 葡萄酒数据集产区多元方差分析 (MANOVA) ===")
print(f"Wilks' Lambda 统计量: {manova_res['wilks_lambda']:.6f}")
print(f"Rao's F 近似统计量: {manova_res['wilks_F']:.2f} (p-value = {manova_res['wilks_p_value']:.2e})")
print(f"Pillai's Trace 迹统计量: {manova_res['pillai_trace']:.4f}")
print(f"Hotelling-Lawley 迹统计量: {manova_res['hotelling_lawley']:.4f}")
print(f"Roy's 最大根: {manova_res['roys_largest_root']:.4f}")

assert manova_res['wilks_p_value'] < 1e-15
print("✅ 结论：3 个葡萄酒品种在 13 维化学指标综合空间中均值向量差异高度显著！")
```

---

## 5. 检索自测练习

1. 当组数 $g=2$ 时，证明 Wilks' $\Lambda$ 与两样本 Hotelling $T^2$ 统计量之间满足单调等价关系 $\Lambda = \frac{1}{1 + \frac{T^2}{N-2}}$。
2. 解释若各组协方差矩阵不相等（Box's M 检验被拒绝），为什么应优先报告 Pillai's Trace 而非 Wilks' Lambda？

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
