---
title: "随机过程-题型-布朗运动模拟与SDE数值解阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "随机过程作业"
course: "24-随机过程"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: intermediate
importance: A
concept: ["随机过程", "布朗运动", "SDE求解", "伊藤引理"]
prerequisites: ["[[🗺️ 概率论与数理统计学习路径|概率统计]]"]
related: ["[[量化金融-题型-Alpha101因子与成本敏感回测阶梯作业]]"]
upstream: ["[[🗺️ 随机过程学习路径|随机过程学习路径]]"]
downstream: []
tags: [学习, 24-随机过程, 作业, 实战, 阶梯作业]
aliases: ["Stoch-HW01-布朗运动与SDE作业"]
---

# 随机过程 - HW01：布朗运动模拟与 SDE 数值解阶梯作业

> 🎯 **作业目标**：计算马尔可夫链稳态分布、模拟布朗运动 (Brownian Motion) 二次变差，并手写 Euler-Maruyama Scheme 求解随机微分方程 (SDE)。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-stoch/hw01_brownian_sde.ipynb`
- **开源标杆仓库**：[MIT 6.041 Probabilistic Systems Analysis](https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/) / Stanford CME 308
- **核心依赖**：`numpy`, `scipy`, `matplotlib`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 稳态概率求解无误 | 构造马尔可夫链转移概率矩阵 $P$，计算 10 步转移概率与平稳分布 $\pi P = \pi$。 |
| 🟡 **L2 - Medium Baseline** | 模拟到达时间间隔 | 模拟齐次与非齐次泊松过程 (Poisson Process)，验证事件到达间隔为指数分布。 |
| 🔴 **L3 - Strong Baseline** | 二次变差收敛于时间 $T$ | **模拟标准布朗运动 $B(t)$**，计算并验证分割细度趋于 0 时，二次变差 $\sum (B(t_i) - B(t_{i-1}))^2 \to T$。 |
| 👑 **L4 - Boss Baseline** | SDE 数值收敛阶 $O(\sqrt{\Delta t})$ | **手写 Euler-Maruyama 与 Milstein 格式** 数值求解几何布朗运动 (GBM) 与 Ornstein-Uhlenbeck (OU) 过程 SDE。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_brownian_motion_quadratic_variation():
    from stoch_solvers import simulate_brownian_motion
    N = 10000
    T = 1.0
    t, B = simulate_brownian_motion(T=T, N=N)
    
    # 二次变差应该非常接近时间 T=1.0
    quad_var = np.sum(np.diff(B)**2)
    assert np.isclose(quad_var, T, atol=0.05), f"二次变差 {quad_var} 必须逼近 T=1.0"
```

---

## 🃏 Anki 卡片

- Q: 简述伊藤清引理 (Itô's Lemma) 对于微元 $(dB_t)^2$ 的核心替换规则及其在随机微积分中的物理含义。
- A: 伊藤引理规定在二阶泰勒展开中，$(dB_t)^2 = dt$，而 $dt \cdot dB_t = 0$ 且 $(dt)^2 = 0$。这是因为布朗运动具有无限可微性与非零的二阶变差，使得二阶项在极限下产生常数项 $dt$ 的确定性漂移。
