---
title: "贝叶斯统计-题型-MCMC采样与贝叶斯分层模型阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "贝叶斯统计作业"
course: "33-贝叶斯统计"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["贝叶斯统计", "MCMC", "PyMC", "分层模型"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/22-概率论与数理统计/🗺️ 概率论与数理统计学习路径|概率统计]]"]
related: ["[[概率图模型-题型-变分推断与MCMC采样求解器阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/33-贝叶斯统计/🗺️ 贝叶斯统计学习路径|贝叶斯统计学习路径]]"]
downstream: []
tags: [学习, 33-贝叶斯统计, 作业, 实战, 阶梯作业]
aliases: ["Bayes-HW01-MCMC分层模型作业"]
---

# 贝叶斯统计 - HW01：MCMC 采样与贝叶斯分层模型阶梯作业

> 🎯 **作业目标**：推导 Beta-Binomial 共轭先验解析后验、手写 Metropolis-Hastings MCMC 采样器，并在 PyMC 中构建贝叶斯分层模型。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-bayes/hw01_mcmc_pymc.ipynb`
- **开源标杆仓库**：[Probabilistic Programming & Bayesian Methods for Hackers](https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers)
- **核心依赖**：`pymc`, `arviz`, `numpy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 解析后验计算正确 | 计算 Beta-Binomial / Normal-Normal 共轭先验后验分布参数并绘图。 |
| 🟡 **L2 - Medium Baseline** | 采样链收敛 $\hat{R} < 1.05$ | **手写 Metropolis-Hastings 采样器** 拟合双峰后验分布并计算 95% HDI 信用区间。 |
| 🔴 **L3 - Strong Baseline** | PyMC 分层模型求解 | **使用 PyMC / Stan 构建贝叶斯分层模型 (Hierarchical Model)**（如 Eight Schools 问题）。 |
| 👑 **L4 - Boss Baseline** | 变分后验求解收敛 | **手撕 Variational Inference (VI)** 变分后验推断算法，加速高维后验估计。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_metropolis_hastings_posterior_mean():
    from bayes_solvers import metropolis_hastings_normal
    # 数据来源于 N(2.0, 1.0)
    data = np.random.normal(2.0, 1.0, 200)
    
    samples = metropolis_hastings_normal(data, n_samples=5000)
    burn_in = samples[1000:]
    post_mean = np.mean(burn_in)
    
    assert np.isclose(post_mean, 2.0, atol=0.15), "MH MCMC 采样估算出的均值必须逼近真实均值 2.0"
```

---

## 🃏 Anki 卡片

- Q: 为什么在贝叶斯统计中用高度集成 (High-Density Interval, HDI) 取代传统频繁学派置信区间？
- A: 频繁学派置信区间指多次重复抽样中覆盖真值的概率；而贝叶斯 95% HDI 表示在后验概率密度最大的区间内，真实参数落在该区间内的后验概率为 95%，具有直接的概率解释。
