---
title: "属性数据分析-题型-Softmax回归与对数线性模型阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "属性数据分析作业"
course: "31-属性数据分析"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: intermediate
importance: A
concept: ["分类数据", "列联表", "Logistic回归", "对数线性模型"]
prerequisites: ["[[🗺️ 应用回归分析学习路径|应用回归分析]]"]
related: ["[[应用回归分析-题型-坐标下降Lasso与IRLS回归阶梯作业]]"]
upstream: ["[[🗺️ 属性数据分析学习路径|属性数据分析学习路径]]"]
downstream: []
tags: [学习, 31-属性数据分析, 作业, 实战, 阶梯作业]
aliases: ["CDA-HW01-Softmax与对数线性作业"]
---

# 属性数据分析 - HW01：Softmax 回归与对数线性模型阶梯作业

> 🎯 **作业目标**：计算 $2\times 2$ 列联表 Odds Ratio、手写 Multinomial Logistic Regression (Softmax)，并拟合多维列联表对数线性模型 (Log-Linear Models)。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-cda/hw01_softmax_loglinear.ipynb`
- **开源标杆仓库**：[Agresti Categorical Data Analysis Companion](https://github.com/michaeleby/Agresti-CDA)
- **核心依赖**：`statsmodels`, `scikit-learn`, `numpy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 卡方检验 p-value 无误 | 计算 $2\times 2$ 列联表 Pearson 卡方检验、Fisher 精确检验与优势比 (Odds Ratio)。 |
| 🟡 **L2 - Medium Baseline** | ROC AUC ≥ 0.85 | 拟合二项 Logistic 回归，绘制 ROC 曲线与计算 AUC 置信区间。 |
| 🔴 **L3 - Strong Baseline** | 交叉熵 Loss 收敛 | **手撕 Multinomial Logistic Regression (Softmax Regression)** 迭代更新算法。 |
| 👑 **L4 - Boss Baseline** | 交互效应判定 | **拟合多维列联表对数线性模型 (Log-linear Model)**，评估三阶及高阶因子交互效应。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_odds_ratio_calculation():
    from cda_solvers import odds_ratio
    # 2x2 列联表 [[a, b], [c, d]] => OR = (a*d) / (b*c)
    table = np.array([[50, 10], [20, 40]])
    or_val = odds_ratio(table)
    
    expected = (50 * 40) / (10 * 20) # 2000 / 200 = 10.0
    assert np.isclose(or_val, expected, atol=1e-5)
```

---

## 🃏 Anki 卡片

- Q: 在属性数据分析中，优势比 (Odds Ratio, OR) 与相对危险度 (Relative Risk, RR) 有何区别？
- A: RR 为两组患病概率之比 $\frac{p_1}{p_2}$；OR 为两组优势之比 $\frac{p_1/(1-p_1)}{p_2/(1-p_2)}$。在发病率极低的稀有疾病假设下 ($p_1, p_2 \ll 1$)，优势比近似等于相对危险度 ($OR \approx RR$)。
