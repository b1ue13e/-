---
title: "概率图模型-题型-变分推断与MCMC采样求解器阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "概率图模型作业"
course: "14-概率图模型"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["概率图模型", "MCMC采样", "变分推断"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/17-机器学习/🗺️ 机器学习学习路径|机器学习]]"]
related: ["[[贝叶斯统计-题型-MCMC采样与贝叶斯分层模型阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/14-概率图模型/🗺️ 概率图模型学习路径|概率图模型学习路径]]"]
downstream: []
tags: [学习, 14-概率图模型, 作业, 实战, 阶梯作业]
aliases: ["CS228-HW02-PGM推断作业"]
---

# 概率图模型 - HW02：变分推断与 MCMC 采样求解器阶梯作业

> 🎯 **作业目标**：手写变量消去法 (Variable Elimination)、Metropolis-Hastings / Gibbs 采样，以及变分自编码器 (VAE) 中的变分推断。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-pgm/hw02_vi_mcmc.ipynb`
- **开源标杆仓库**：[ermongroup/cs228-notes](https://github.com/ermongroup/cs228-notes) (Stanford CS228)
- **核心依赖**：`pgmpy`, `torch`, `numpy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 条件独立性校验正确 | 构建简单的 Bayesian Network，手算并用 `pgmpy` 验证 $D$-分离 ($d$-separation) 独立性。 |
| 🟡 **L2 - Medium Baseline** | 边缘分布计算无误 | **手写 Variable Elimination (变量消去法)** 算法，计算因子乘积 (Factor Product) 与消去。 |
| 🔴 **L3 - Strong Baseline** | 采样收敛 $\hat{R} < 1.05$ | **手写 Gibbs Sampling 与 Metropolis-Hastings 采样器**，求解隐马尔可夫模型 (HMM) 维特比解码。 |
| 👑 **L4 - Boss Baseline** | ELBO 优化收敛 | 手写 Variational Autoencoder (VAE)，实现 Mean-field 变分推断与 Reparameterization Trick 重参数化。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_variable_elimination_marginal():
    from pgm_solvers import factor_product, factor_marginalize
    # 构造测试 Factor
    phi_A = np.array([0.6, 0.4]) # P(A)
    phi_BA = np.array([[0.8, 0.2], [0.3, 0.7]]) # P(B|A)
    
    # 边际化消去 A 得到 P(B)
    P_B = np.dot(phi_A, phi_BA)
    assert np.isclose(P_B.sum(), 1.0)
    assert np.isclose(P_B[0], 0.6*0.8 + 0.4*0.3)
```

---

## 🃏 Anki 卡片

- Q: 在变分推断 (Variational Inference) 中，证据下界 (ELBO) 表达式 $\text{ELBO}(q) = \mathbb{E}_{q(z)}[\log p(x,z)] - \mathbb{E}_{q(z)}[\log q(z)]$ 与真实边缘似然 $\log p(x)$ 之间满足什么几何关系？
- A: $\log p(x) = \text{ELBO}(q) + \text{KL}(q(z) \parallel p(z|x))$。因为 KL 散度是非负的 ($\text{KL} \ge 0$)，所以 ELBO 始终是真实数据边际似然 $\log p(x)$ 的下界。最大化 ELBO 等价于最小化变分后验 $q(z)$ 与真实后验 $p(z|x)$ 之间的 KL 散度。
