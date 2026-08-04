---
title: "量化金融-题型-Alpha101因子与成本敏感回测阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "量化金融作业"
course: "03-量化金融"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["因子投资", "Alpha101", "回测引擎"]
prerequisites: ["[[ARIMA模型-量化应用]]", "[[交叉验证]]"]
related: ["[[机器学习-题型-李宏毅式分类与深层模型阶梯作业]]"]
upstream: ["[[🗺️ 量化金融学习路径]]"]
downstream: []
tags: [学习, 03-量化金融, 作业, 实战, 阶梯作业]
aliases: ["Quant-HW17-因子回测作业"]
---

# 量化金融 - HW17：Alpha101 因子与成本敏感回测阶梯作业

> 🎯 **作业目标**：手写 WorldQuant Alpha101 经典因子，基于 Qlib / Backtrader 框架构建支持双边千分之一印花税与滑点的交易回测引擎。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-quant/hw17_factor_backtest.ipynb`
- **开源标杆仓库**：[microsoft/qlib](https://github.com/microsoft/qlib)
- **核心依赖**：`qlib`, `pandas`, `numpy`, `backtrader`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 Sharpe Ratio | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | Sharpe ≥ 0.8 | 使用 `pandas` 实现双均线 (MA5/MA20) 策略，计算无摩擦 Sharpe 比率与最大回撤。 |
| 🟡 **L2 - Medium Baseline** | Sharpe ≥ 1.3 | **手撕 Alpha101 核心因子**（如 Alpha006、Alpha012），计算 IC / Rank IC 与 IC 换手率。 |
| 🔴 **L3 - Strong Baseline** | Sharpe ≥ 1.8 | **构建成本敏感回测引擎**：加入 0.1% 交易印花税 + 0.03% 滑点，实现 Top-K 截面市值中性化因子选股。 |
| 👑 **L4 - Boss Baseline** | Sharpe ≥ 2.5 | 使用 `Qlib` 线性/树模型进行多因子动态组合优化，并通过 LightGBM 消除行业风格暴露。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

自测校验脚本 `03-Projects/projects-quant/tests/test_hw17.py`：

```python
import pytest
import pandas as pd
import numpy as np

def test_alpha006_calculation():
    # 测试手写 Alpha006 (-1 * correlation(open, volume, 10)) 逻辑
    df = pd.DataFrame({
        'open': np.random.randn(100),
        'volume': np.random.randn(100)
    })
    
    from factor_lib import alpha006
    factor_val = alpha006(df['open'], df['volume'], window=10)
    
    assert not factor_val.isna().all(), "Alpha 因子输出不得全部为 NaN"
    assert factor_val.shape[0] == 100, "因子数据长度必须与输入数据一致"
```

---

## 🃏 Anki 卡片

- Q: 为什么在量化回测中如果不进行“行业与市值中性化”处理，高 IC 因子可能只是表达了特定风格暴露？
- A: 未中性化的因子可能只是暴露在小市值风格或特定大盘行业（如白酒/新能源）上，其收益源于风格β而非阿尔法Alpha。中性化通过回归剔除市值和行业影响，提取纯净 Alpha。
