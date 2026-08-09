---
type: study
topic: "典型相关分析 CCA"
course: "16-多元统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段4-关联结构与对应分析]]"
upstream: ["[[多元统计-前置-正定矩阵与谱分解]]"]
flow: knowledge
kind: derivation
difficulty: advanced
concept: ["典型相关分析", "CCA", "广义特征值", "典型变量", "典型相关系数", "子空间关联"]
tags: [学习, 多元统计, 关联分析, 多变量系统, 广义特征值]
---

# 多元统计-典型相关分析CCA

## 1. 为什么两组多变量系统需要典型相关分析？

当我们需要衡量**两组多变量指标系统之间**（例如 10 个宏观经济变量组 $\mathbf{X}$ 与 6 个金融资产收益率组 $\mathbf{Y}$）的相关性时：
- 若对 $p \times q$ 个变量对逐一计算 Simple Correlation，会导致多达 60 个相互重叠的相关系数，无法洞察系统级的传导主线；
- 若只用简单多元回归，只能处理单个因变量 $Y_1$。

**典型相关分析 (Canonical Correlation Analysis, CCA)** 由 Hotelling (1936) 提出，其核心哲学：在 $\mathbf{X}$ 空间中寻找线性组合 $U = \mathbf{a}^T \mathbf{X}$，在 $\mathbf{Y}$ 空间中寻找线性组合 $V = \mathbf{b}^T \mathbf{Y}$，使新合成的**典型变量 $U$ 与 $V$ 之间的 Pearson 相关系数 $\rho = \operatorname{Corr}(U, V)$ 达到最大**。

---

## 2. 数学推导：广义特征值问题

### 2.1 优化目标与约束

设联合随机向量 $\begin{pmatrix} \mathbf{X} \\ \mathbf{Y} \end{pmatrix}$ 的协方差矩阵为分块矩阵：
$$\mathbf{\Sigma} = \begin{pmatrix} \mathbf{\Sigma}_{XX} & \mathbf{\Sigma}_{XY} \\ \mathbf{\Sigma}_{YX} & \mathbf{\Sigma}_{YY} \end{pmatrix}$$
寻找权重向量 $\mathbf{a} \in \mathbb{R}^p, \mathbf{b} \in \mathbb{R}^q$，最大化协方差 $\operatorname{Cov}(U, V) = \mathbf{a}^T \mathbf{\Sigma}_{XY} \mathbf{b}$，受单位方差约束：
$$\operatorname{Var}(U) = \mathbf{a}^T \mathbf{\Sigma}_{XX} \mathbf{a} = 1, \quad \operatorname{Var}(V) = \mathbf{b}^T \mathbf{\Sigma}_{YY} \mathbf{b} = 1$$

### 2.2 拉格朗日函数与广义特征值

构造拉格朗日函数：
$$L(\mathbf{a}, \mathbf{b}, \lambda, \mu) = \mathbf{a}^T \mathbf{\Sigma}_{XY} \mathbf{b} - \frac{\lambda}{2}(\mathbf{a}^T \mathbf{\Sigma}_{XX} \mathbf{a} - 1) - \frac{\mu}{2}(\mathbf{b}^T \mathbf{\Sigma}_{YY} \mathbf{b} - 1)$$
分别对 $\mathbf{a}, \mathbf{b}$ 求偏导并令为零：
1. $\mathbf{\Sigma}_{XY} \mathbf{b} - \lambda \mathbf{\Sigma}_{XX} \mathbf{a} = \mathbf{0} \implies \mathbf{\Sigma}_{XX}^{-1} \mathbf{\Sigma}_{XY} \mathbf{b} = \lambda \mathbf{a}$
2. $\mathbf{\Sigma}_{YX} \mathbf{a} - \mu \mathbf{\Sigma}_{YY} \mathbf{b} = \mathbf{0} \implies \mathbf{\Sigma}_{YY}^{-1} \mathbf{\Sigma}_{YX} \mathbf{a} = \mu \mathbf{b}$

易证 $\lambda = \mu = \rho$。将第二式代入第一式，消去 $\mathbf{b}$：
$$\mathbf{\Sigma}_{XX}^{-1} \mathbf{\Sigma}_{XY} \mathbf{\Sigma}_{YY}^{-1} \mathbf{\Sigma}_{YX} \mathbf{a} = \rho^2 \mathbf{a}$$
> [!IMPORTANT]
> **结论**：第 $k$ 对典型相关系数的平方 $\rho_k^2$ 即为矩阵 $\mathbf{M}_X = \mathbf{\Sigma}_{XX}^{-1} \mathbf{\Sigma}_{XY} \mathbf{\Sigma}_{YY}^{-1} \mathbf{\Sigma}_{YX}$ 的第 $k$ 大特征值，权重 $\mathbf{a}_k$ 为其特征向量！

---

## 3. Python 实战代码：真实宏观面板与资产收益率 CCA 建模

```python
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, r"f:\-\03-Projects\16-多元统计\scripts")
from load_data import load_macro_financial_panel
from mva_toolkit import cca_fit

# 1. 加载 15 年月度面板数据
df_macro = load_macro_financial_panel()
macro_cols = ['GDP_Growth', 'CPI', 'PPI', 'M2_Growth', 'PMI']
asset_cols = ['Stock_A_Return', 'Bond_10Y_Return', 'Commodity_Return', 'Gold_Return']

X = df_macro[macro_cols].values
Y = df_macro[asset_cols].values

# 2. 运行 CCA 拟合
res_cca = cca_fit(X, Y, n_components=2)

print("=== 宏观经济组 (5 特征) 与 金融资产组 (4 特征) 典型相关分析 ===")
print("典型相关系数 rho:", np.round(res_cca['correlations'], 4))
print("第一典型变量宏观权重 A[:, 0]:", np.round(res_cca['x_weights'][:, 0], 3))
print("第一典型变量资产权重 B[:, 0]:", np.round(res_cca['y_weights'][:, 0], 3))

assert res_cca['correlations'][0] > 0.8
print("✅ 宏观-资产典型相关分析 (CCA) 广义特征值求解成功！")
```

---

## 4. 检索自测练习

1. 证明前 $k$ 对典型变量满足正交无关约束：$\operatorname{Cov}(U_i, U_j) = 0, \operatorname{Cov}(V_i, V_j) = 0, \operatorname{Cov}(U_i, V_j) = 0 \, (i \neq j)$。
2. 解释典型相关分析 (CCA) 与多元双组回归在假设与降维效果上的本质区别。

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
