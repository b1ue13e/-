---
title: "时间序列分析-题型-ARIMA与卡尔曼滤波去噪阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "时间序列分析作业"
course: "02-时间序列分析"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: intermediate
importance: A
concept: ["时间序列", "ARIMA", "卡尔曼滤波"]
prerequisites: ["[[ARIMA模型-量化应用]]"]
related: ["[[量化金融-题型-Alpha101因子与成本敏感回测阶梯作业]]"]
upstream: ["[[🗺️ 时间序列分析学习路径]]"]
downstream: []
tags: [学习, 02-时间序列分析, 作业, 实战, 阶梯作业]
aliases: ["TSA-HW01-ARIMA与Kalman作业"]
---

# 时间序列分析 - HW01：ARIMA 与卡尔曼滤波去噪阶梯作业

> 🎯 **作业目标**：手写单位根检验、ARIMA 模型自动定阶以及卡尔曼滤波 (Kalman Filter) 隐状态估计。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-tsa/hw01_arima_kalman.ipynb`
- **开源标杆仓库**：[robjhyndman/fpp3](https://github.com/robjhyndman/fpp3)
- **核心依赖**：`statsmodels`, `scipy`, `pandas`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 RMSE / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 平稳性检验正确 | 对非平稳时间序列进行 ADF 检验，差分平稳化后绘制 ACF / PACF 图。 |
| 🟡 **L2 - Medium Baseline** | AIC/BIC 最小值定阶 | 使用 `statsmodels.tsa.arima.model.ARIMA` 求解 $(p,d,q)$ 拟合与残差白噪声检验。 |
| 🔴 **L3 - Strong Baseline** | **手撕 Kalman Filter** | **从零手写卡尔曼滤波**：预测步 (Predict) 与更新步 (Update)，对含噪高频数据去噪。 |
| 👑 **L4 - Boss Baseline** | 深度时序 SOTA | 构建 Temporal Fusion Transformer (TFT) 或 N-BEATS 完成多变量时序预测。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_kalman_filter_denoising():
    from tsa_solvers import KalmanFilter1D
    kf = KalmanFilter1D(process_variance=1e-5, measurement_variance=1e-1)
    
    noisy_signal = np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.3, 100)
    filtered = [kf.update(z) for z in noisy_signal]
    
    rmse_raw = np.sqrt(np.mean((noisy_signal - np.sin(np.linspace(0, 10, 100)))**2))
    rmse_filtered = np.sqrt(np.mean((filtered - np.sin(np.linspace(0, 10, 100)))**2))
    
    assert rmse_filtered < rmse_raw, "卡尔曼滤波后 RMSE 必须显著低于原始噪音信号"
```

---

## 🃏 Anki 卡片

- Q: 卡尔曼滤波 (Kalman Filter) 中卡尔曼增益 $K_k$ 的物理含义与取值极端情况是什么？
- A: $K_k$ 决定了系统在“预测估计”与“测量观察”之间的信任权重。当测量噪声远小于预测方差时，$K_k \to 1$（信任测量）；反之当测量噪声极大时，$K_k \to 0$（信任预测）。
