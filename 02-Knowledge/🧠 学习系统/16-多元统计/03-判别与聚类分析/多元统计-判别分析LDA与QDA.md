---
type: study
topic: "判别分析 LDA 与 QDA"
course: "16-多元统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段3-判别与聚类分析]]"
upstream: ["[[多元统计-前置-正定矩阵与谱分解]]"]
flow: knowledge
kind: derivation
difficulty: intermediate
concept: ["判别分析", "LDA", "QDA", "Fisher线性判别", "Rayleigh商", "贝叶斯决策面", "离散度矩阵"]
tags: [学习, 多元统计, 模式识别, 分类, 线性代数, 贝叶斯统计]
---

# 多元统计-判别分析LDA与QDA

## 1. 为什么分类需要专门的统计判别分析？

当数据包含明确的离散群体标签（如 0/1 瑞士真伪钞票，或 3 类葡萄酒品种），直接使用无监督 PCA 降维投影可能会遇到严重问题：**PCA 寻找的是总方差最大的方向，而总方差最大的方向未必是组间分离度最大的方向！**

**Fisher 线性判别分析 (LDA)** 与 **二次判别分析 (QDA)** 的核心哲学：
- **LDA**：在假设协方差齐性（$\mathbf{\Sigma}_1 = \mathbf{\Sigma}_2$）的前提下，寻找使**组间方差与组内方差之比（Rayleigh 商）最大化**的正交投影方向，形成线性决策面；
- **QDA**：放宽协方差齐性假设（$\mathbf{\Sigma}_k$ 各组异方差），推导出具有马氏距离特征的**二次曲面贝叶斯决策边界**。

---

## 2. Fisher LDA 严格数学推导：Rayleigh 商最大化

### 2.1 两类 Fisher 判别

设两组样本 $X_1, X_2$，均值分别为 $\boldsymbol{\mu}_1, \boldsymbol{\mu}_2$，类内离差阵为 $\mathbf{S}_W = (n_1-1)\mathbf{S}_1 + (n_2-1)\mathbf{S}_2$。
寻找一维投影方向 $\mathbf{w} \in \mathbb{R}^p$，使投影后的类间距离平方相对类内离散度最大化：
$$J(\mathbf{w}) = \frac{(\mathbf{w}^T (\boldsymbol{\mu}_1 - \boldsymbol{\mu}_2))^2}{\mathbf{w}^T \mathbf{S}_W \mathbf{w}} = \frac{\mathbf{w}^T \mathbf{S}_B \mathbf{w}}{\mathbf{w}^T \mathbf{S}_W \mathbf{w}}$$
其中类间离散度 $\mathbf{S}_B = (\boldsymbol{\mu}_1 - \boldsymbol{\mu}_2)(\boldsymbol{\mu}_1 - \boldsymbol{\mu}_2)^T$。

对 $J(\mathbf{w})$ 求导并令梯度为零：
$$\nabla_{\mathbf{w}} J(\mathbf{w}) = \frac{2 \mathbf{S}_B \mathbf{w} (\mathbf{w}^T \mathbf{S}_W \mathbf{w}) - 2 \mathbf{S}_W \mathbf{w} (\mathbf{w}^T \mathbf{S}_B \mathbf{w})}{(\mathbf{w}^T \mathbf{S}_W \mathbf{w})^2} = \mathbf{0}$$
由于 $\mathbf{S}_B \mathbf{w}$ 方向总是平行于 $(\boldsymbol{\mu}_1 - \boldsymbol{\mu}_2)$，因此最优投影向量解析解为：
$$\mathbf{w}^* = \mathbf{S}_W^{-1} (\boldsymbol{\mu}_1 - \boldsymbol{\mu}_2)$$

### 2.2 多类 LDA 广义特征值

对 $g > 2$ 多类问题，求解广义特征值问题：
$$\mathbf{S}_B \mathbf{w} = \lambda \mathbf{S}_W \mathbf{w} \iff \mathbf{S}_W^{-1} \mathbf{S}_B \mathbf{w} = \lambda \mathbf{w}$$
最多可提取 $m = \min(g-1, p)$ 个正交判别轴。

---

## 3. QDA 异方差贝叶斯二次决策边界

在多元正态分布假设下，类 $k$ 的后验概率为 $P(Y=k \mid \mathbf{x}) \propto f_k(\mathbf{x}) \pi_k$。
取对数定义判别函数：
$$\delta_k(\mathbf{x}) = \ln f_k(\mathbf{x}) + \ln \pi_k = -\frac{1}{2}\ln|\mathbf{\Sigma}_k| - \frac{1}{2}(\mathbf{x} - \boldsymbol{\mu}_k)^T \mathbf{\Sigma}_k^{-1} (\mathbf{x} - \boldsymbol{\mu}_k) + \ln \pi_k$$

- **当 $\mathbf{\Sigma}_k = \mathbf{\Sigma}$（同方差 LDA）**：展开二次项，$\mathbf{x}^T \mathbf{\Sigma}^{-1} \mathbf{x}$ 抵消，决策边界 $\delta_k(\mathbf{x}) = \delta_j(\mathbf{x})$ 是关于 $\mathbf{x}$ 的**超平面（线性边界）**；
- **当 $\mathbf{\Sigma}_k$ 不等（异方差 QDA）**：二次项无法抵消，决策边界是关于 $\mathbf{x}$ 的**二次超曲面（双曲/椭圆边界）**。

---

## 4. Python 实战代码：真实瑞士钞票 LDA 与 QDA 分类

```python
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, r"f:\-\03-Projects\16-多元统计\scripts")
from load_data import load_swiss_banknotes
from mva_toolkit import lda_fit, qda_fit

# 1. 加载瑞士钞票数据
df_bank = load_swiss_banknotes()
cols = ['Length', 'Left', 'Right', 'Bottom', 'Top', 'Diagonal']
X = df_bank[cols].values
y = df_bank['Is_Counterfeit'].values

# 2. 构建 Fisher LDA 与 QDA
res_lda = lda_fit(X, y)
res_qda = qda_fit(X, y)

# 3. 校验分类准确率
qda_preds = res_qda['predict'](X)
acc_qda = np.mean(qda_preds == y)

print("=== 瑞士钞票 Fisher LDA 与 QDA 模式识别 ===")
print("Fisher LDA 最优投影向量 w:\n", np.round(res_lda['W'][:, 0], 3))
print(f"QDA 拟合在 200 张钞票上的判别准确率: {acc_qda * 100:.2f}%")

assert acc_qda > 0.95
print("✅ Fisher LDA 与 QDA 模式识别构建成功！")
```

---

## 5. 检索自测练习

1. 证明若先对数据做白化变换（使类内协方差为 $\mathbf{I}$），则 Fisher LDA 最优投影向量方向即为两组均值连线向量 $\boldsymbol{\mu}_1 - \boldsymbol{\mu}_2$。
2. 解释为什么当特征维数 $p$ 很大、样本量 $n$ 较小时，QDA 因为要估计 $g \times \frac{p(p+1)}{2}$ 个协方差参数而极易发生严重过拟合？

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
