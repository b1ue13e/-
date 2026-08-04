---
title: "概率论与数理统计-题型-Bootstrap重抽样与ANOVA求解器阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "概率论与数理统计作业"
course: "22-概率论与数理统计"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: intermediate
importance: A
concept: ["数理统计", "MLE估计", "Bootstrap", "假设检验"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/22-概率论与数理统计/🗺️ 概率论与数理统计学习路径|概率统计学习路径]]"]
related: ["[[应用回归分析-题型-坐标下降Lasso与IRLS回归阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/22-概率论与数理统计/🗺️ 概率论与数理统计学习路径|概率统计学习路径]]"]
downstream: []
tags: [学习, 22-概率论与数理统计, 作业, 实战, 阶梯作业]
aliases: ["Stat-HW01-MLE与Bootstrap作业"]
---

# 概率论与数理统计 - HW01：Bootstrap 重抽样与 ANOVA 求解器阶梯作业

> 🎯 **作业目标**：验证中心极限定理 (CLT)、数值求解 MLE 估计、手写非参数 Bootstrap 置信区间计算与单/双因素方差分析 (ANOVA)。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-stats/hw01_mle_bootstrap.ipynb`
- **开源标杆仓库**：[Harvard Stat 110 (Joe Blitzstein)](https://github.com/mblondel/stat110) / UC Berkeley Data 8
- **核心依赖**：`scipy`, `numpy`, `matplotlib`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 模拟收敛于正态分布 | 蒙特卡洛模拟验证大数定律 (LLN) 与中心极限定理 (CLT) 样本均值分布。 |
| 🟡 **L2 - Medium Baseline** | 求解梯度 0 收敛 | **手写数值 MLE (极大似然估计)** 求解 Gamma / Weibull 双参数分布估计。 |
| 🔴 **L3 - Strong Baseline** | 置信覆盖率 ≥ 95% | **手写非参数 Bootstrap 重抽样算法**，计算任意非线性统计量 (如中位数比值) 的百分位置信区间。 |
| 👑 **L4 - Boss Baseline** | F 统计量与自由度无误 | **从零手撕单因素与双因素方差分析 (ANOVA) 计算引擎**，输出完整 SS, MS, F-value, p-value 表格。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_bootstrap_confidence_interval():
    from stat_solvers import bootstrap_ci
    data = np.random.exponential(scale=2.0, size=100)
    
    # 估计总体均值（真实为 2.0）
    ci_lower, ci_upper = bootstrap_ci(data, stat_func=np.mean, n_boot=2000, ci=95)
    assert ci_lower < 2.0 < ci_upper, "95% Bootstrap 置信区间必须覆盖真实真值 2.0"
```

---

## 🃏 Anki 卡片

- Q: 极大似然估计 (MLE) 的渐近正态性 (Asymptotic Normality) 定理指什么？
- A: 在正则条件下，当样本量 $n \to \infty$ 时，极大似然估计量 $\hat{\theta}_{MLE}$ 依分布收敛于均值为真实参数 $\theta_0$、方差为费雪信息量逆矩阵 $I^{-1}(\theta_0)/n$ 的正态分布：$\sqrt{n}(\hat{\theta} - \theta_0) \xrightarrow{d} \mathcal{N}(0, I^{-1}(\theta_0))$。
