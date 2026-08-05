---
title: "时间序列分析 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "时间序列分析 4-Tier 阶梯作业规范"
course: "时间序列分析"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [时间序列分析, 4Tier作业, 阶梯作业, 编程实战, PyTest, STAT510, Tsay]
---

# 📈 时间序列分析 4-Tier 阶梯作业全景规范说明书 (Penn State STAT 510 & Tsay 范式)

> 本说明书为 **02-时间序列分析** 路径（基于 Penn State STAT 510 与 Ruey S. Tsay《金融时间序列分析》）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ Statsmodels 调包 / ACF与PACF绘图 / 基础 ARIMA 拟合
🟡 L2 - Medium Baseline   │ 残差白噪声检验 (Ljung-Box) / 滚动交叉验证 (Rolling CV)
🔴 L3 - Strong Baseline   │ [核心] 不调用高级时序库，从零手撕 卡尔曼滤波 (Kalman Filter) / GARCH MLE 求解 / 协整检验
👑 L4 - Boss Baseline     │ 高频微观结构模型 (Hawkes Process) / 贝叶斯结构时间序列 (BSTS) / 深度时序 (Informer/N-BEATS)
```

---

## 🎯 时间序列分析阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 平稳性检验与自回归模型 (Stationarity & ARMA)
- **开源溯源**：STAT 510 Lesson 1-3 / Tsay Ch 2
- 🟢 **L1**: 使用 `statsmodels` 进行 ADF (Augmented Dickey-Fuller) 单位根检验。
- 🟡 **L2**: 计算并绘制样本 ACF 与 PACF 确定 AR(p) 与 MA(q) 的截尾/拖尾阶数。
- 🔴 **L3 (手撕核心)**：**从零手撕 Yule-Walker 方程求解 AR(p) 系数，以及实现 Durbin-Levinson 递推算法**。
- 👑 **L4**: 实现 ARMA 模型的最大似然估计 (MLE) 优化求解过程。

### 2. HW02 - 波动率建模 (Volatility Modeling: ARCH/GARCH)
- **开源溯源**：Tsay Ch 3
- 🟢 **L1**: 调用 `arch` 包拟合 GARCH(1,1) 模型并预测条件方差。
- 🟡 **L2**: 检验残差的 ARCH 效应 (Engle's LM Test)。
- 🔴 **L3 (手撕核心)**：**手撕 GARCH(1,1) 条件方差递推方程 $\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$，并使用 SciPy Optimize 手动最大化对数似然函数**。
- 👑 **L4**: 实现带偏态 t 分布误差的 EGARCH (指数 GARCH) 模型 MLE 求解。

### 3. HW03 - 多变量时间序列与协整 (Multivariate Time Series & Cointegration)
- **开源溯源**：Tsay Ch 8 / STAT 510 Lesson 11
- 🟢 **L1**: 运行 Johansen 协整检验与 VAR 模型拟合。
- 🟡 **L2**: 计算并绘制正交化脉冲响应函数 (Orthogonalized Impulse Response Function, OIRF)。
- 🔴 **L3 (手撕核心)**：**手撕 Engle-Granger 两步法协整检验与误差修正模型 (ECM) 构建**。
- 👑 **L4**: 实现结构向量自回归模型 (SVAR) 的短期与长期约束参数识别。

### 4. HW04 - 状态空间模型与卡尔曼滤波 (State Space Models & Kalman Filter)
- **开源溯源**：STAT 510 Lesson 12
- 🟢 **L1**: 调用 `pykalman` 或 `statsmodels.tsa.statespace` 提取不可观测成分 (如 Local Level Model)。
- 🟡 **L2**: 实现结构时间序列 (Structural Time Series) 的趋势与季节性分解。
- 🔴 **L3 (手撕核心)**：**手撕线性高斯卡尔曼滤波 (Kalman Filter) 的预测步 (Prediction Step) 与更新步 (Update Step) 方程组**。
- 👑 **L4**: 实现扩展卡尔曼滤波 (EKF) 或粒子滤波 (Particle Filter) 处理非线性非高斯状态空间。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-ts/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-ts/tests/test_hw01_yule_walker.py
pytest 03-Projects/projects-ts/tests/test_hw02_garch_mle.py
pytest 03-Projects/projects-ts/tests/test_hw04_kalman_filter.py
```
