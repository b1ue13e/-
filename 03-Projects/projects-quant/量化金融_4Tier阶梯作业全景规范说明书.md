---
title: "量化金融 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "量化金融 4-Tier 阶梯作业规范"
course: "量化金融"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [量化金融, 4Tier作业, 阶梯作业, 编程实战, PyTest]
---

# 📈 量化金融 4-Tier 阶梯作业全景规范说明书

> 本说明书为 **03-量化金融** 路径下所有 17 项阶梯作业 (HW01 ~ HW17) 提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ API/数据获取 / 算例验证 / 基础公式手算
🟡 L2 - Medium Baseline   │ 因子清洗 / 中性化 / Fama-MacBeth 回归 / 组合优化
🔴 L3 - Strong Baseline   │ [核心] 从零手撕无泄漏因子引擎 / GARCH(1,1) MLE / HRP 聚类 / 撮合引擎
👑 L4 - Boss Baseline     │ 高频 L3 盘口队列模拟 / 极低延迟优化 / FinRL 交易强化学习
```

---

## 🎯 17 门量化阶梯作业 4-Tier 细化规格

### 1. HW01 - CAPM 资本资产定价模型与 Alpha 检验
- 🟢 **L1**: 使用 yfinance/akshare 调取单股与指数数据，计算 Log Return 并通过 OLS 拟合 CAPM Beta。
- 🟡 **L2**: 计算 Jensen's Alpha 与 Tracking Error，完成 Rolling 36 个月 Beta 动态稳定性检验。
- 🔴 **L3 (手撕核心)**：**从零手撕轻量化无前视偏差因子提取器**，手写 OLS 矩阵求解器 $\hat{\beta} = (X^T X)^{-1} X^T Y$，不依赖 `statsmodels`。
- 👑 **L4**: 引入高频 1 分钟数据下的 Realized Beta 计算与微观结构噪音剔除。

### 2. HW02 - 马科维茨有效前沿与 HRP 分层风险平价
- 🟢 **L1**: 给定 5 只资产的均值与协方差矩阵，使用 SciPy `minimize` 求解最小方差组合。
- 🟡 **L2**: 绘制带无风险资产的资本市场线 (CML)，计算最大夏普比率 (Tangency Portfolio)。
- 🔴 **L3 (手撕核心)**：**从零手撕 HRP (Hierarchical Risk Parity) 算法**：
  1. 计算相关系数相关距离 $d_{ij} = \sqrt{2(1-\rho_{ij})}$；
  2. 手写单联动 (Single Linkage) 层次聚类；
  3. 按照树状图进行递归二分法 (Recursive Bisection) 资金分配。
- 👑 **L4**: 结合 Black-Litterman 模型，将主观观点 (Views) 与市场均衡通过贝叶斯推断融合。

### 3. HW03 - Fama-MacBeth 两步回归与因子溢价检验
- 🟢 **L1**: 读取美股/A股全市场股票月度收益率与市值、账面市值比 (HML) 特征。
- 🟡 **L2**: 第一步对每只股票做时序回归得到 Factor Loadings $\hat{\beta}_i$；第二步截面回归得到风险溢价 $\hat{\gamma}_t$。
- 🔴 **L3 (手撕核心)**：**手写 Shanken (1992) 变量误差修正 (Errors-in-Variables Correction)**，计算修正后的 Fama-MacBeth $t$ 统计量，严防数据泄漏。
- 👑 **L4**: 引入 GMM (广义矩估计) 统一估计因子载荷与风险溢价。

### 4. HW04 - Beneish M-Score 财报排雷与 Sloan 应计项因子
- 🟢 **L1**: 从财报数据提取 DSRI, GMI, AQI, SGI, DEPI, SGAI, LVGI, TATA 8 个财务指标。
- 🟡 **L2**: 计算 Beneish M-Score 指标，设定 $M > -1.78$ 阈值进行财务造假预警分类。
- 🔴 **L3 (手撕核心)**：**手写 Sloan (1996) 应计项 (Accruals) 拆解引擎**，分离现金流收益与应计收益，验证应计异象 (Accruals Anomaly)。
- 👑 **L4**: 结合 XGBoost 建立多表钩稽特征树模型，预测上市公司未来审计意见下调概率。

### 5. HW05 - Black-Scholes 期权定价与动态 Delta 对冲
- 🟢 **L1**: 输入 $S, K, T, r, \sigma$，使用 BSM 封闭解求 Call/Put 期权价格与 Delta。
- 🟡 **L2**: 实现二叉树期权定价模型 (CRR)，支持美式期权早提前行权 (Early Exercise) 评估。
- 🔴 **L3 (手撕核心)**：**手撕 Monte Carlo 欧式/亚式期权定价器**：
  1. 采用 Geometric Brownian Motion (GBM) 离散采样 $S_{t+\Delta t} = S_t \exp((r-\frac{\sigma^2}{2})\Delta t + \sigma \sqrt{\Delta t} Z)$；
  2. 实现对偶变量 (Antithetic Variates) 蒙特卡洛方差缩减；
  3. 手写动态 Delta 复制对冲实验，记录对冲误差分布。
- 👑 **L4**: 手撕 Newton-Raphson 求解隐含波动率 (Implied Volatility)，画出 Volatility Smile。

### 6. HW06 - GARCH(1,1) 动态波动率拟合与动态 VaR
- 🟢 **L1**: 使用 `arch` 包拟合股票收益率 GARCH(1,1) 模型，提取条件方差 $\sigma_t^2$。
- 🟡 **L2**: 计算 95% 和 99% 参数法与历史模拟法 Value at Risk (VaR)。
- 🔴 **L3 (手撕核心)**：**手撕 GARCH(1,1) 极大似然估计 (MLE)**：
  $$ \ln L(\theta) = -\frac{1}{2} \sum_{t=1}^T \left( \ln(2\pi) + \ln(\sigma_t^2) + \frac{\epsilon_t^2}{\sigma_t^2} \right) $$
  手写递归迭代公式 $\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$，用 `scipy.optimize` 优化约束 $\alpha + \beta < 1$。
- 👑 **L4**: 使用 Extreme Value Theory (EVT) Peaks-Over-Threshold (POT) 模型对其尾部超过门槛部分做广义帕累托分布 (GPD) 拟合。

### 7. HW07 - EGARCH & GJR-GARCH 杠杆效应与新闻响应曲线
- 🟢 **L1**: 比较标准化残差在负冲击与正冲击下的条件方差差异。
- 🟡 **L2**: 拟合 GJR-GARCH 与 EGARCH 模型，绘制新闻响应曲线 (News Impact Curve)。
- 🔴 **L3 (手撕核心)**：**手写 EGARCH 对数条件方差递推器**，推导杠杆系数 $\gamma$ 的统计显著性。
- 👑 **L4**: 多变量 DCC-GARCH (Dynamic Conditional Correlation) 手撕实现。

### 8. HW08 - 极值理论 EVT 黑天鹅外推
- 🟢 **L1**: 计算 99.9% 极端 quantile VaR。
- 🟡 **L2**: 使用 Hill 估计量计算尾部指数 (Tail Index)。
- 🔴 **L3 (手撕核心)**：**手撕 Generalized Pareto Distribution (GPD) MLE 参数估计器**，计算 99.99% 极值 VaR 与 Expected Shortfall (ES)。
- 👑 **L4**: 结合 Copula 函数建立高维资产尾部依赖 (Tail Dependence) 结构。

### 9. HW09 - Tick 级数据转 Volume Bars & Dollar Bars 采样引擎
- 🟢 **L1**: 将逐笔成交 Tick 数据按固定时间 1 分钟/5 分钟重采样为 Time Bars。
- 🟡 **L2**: 按累积成交量采样为 Volume Bars，按成交额采样为 Dollar Bars。
- 🔴 **L3 (手撕核心)**：**手写高性能 Dollar Imbalance Bars (DIB) 采样引擎**：
  1. 手写 Tick Rule 标记买卖方向 $b_t = \text{sign}(\Delta P_t)$；
  2. 动态估计期望 Bar 长度指数移动平均 $E_0[T]$ 与失衡期望；
  3. 离散事件驱动输出，消除 Time Bars 产生的异方差性。
- 👑 **L4**: C++ / PyBind11 实现百万级 Tick/秒的高效采样。

### 10. HW10 - HRP 分层风险平价与单联动聚类
- 🟢 **L1**: 计算 20 只股票历史收益率的协方差矩阵。
- 🟡 **L2**: 使用 SciPy 聚类包生成 Dendrogram 树状图。
- 🔴 **L3 (手撕核心)**：**独立手写准对角化 (Quasi-Diagonalization) 重新排列算法**。
- 👑 **L4**: 因子空间分层风险平价 (Factor-Space HRP)。

### 11. HW11 - RMT 协方差矩阵去噪与 Marchenko-Pastur 检验
- 🟢 **L1**: 计算资产协方差矩阵的特征值谱 (Eigenvalue Spectrum)。
- 🟡 **L2**: 拟合 Marchenko-Pastur 分布理论概率密度函数。
- 🔴 **L3 (手撕核心)**：**手写 RMT 噪声剪裁 (Clipping) 与收缩 (Shrinkage) 去噪器**，重新构建可逆且正定的去噪协方差矩阵。
- 👑 **L4**: Random Matrix Theory 下的动量/均值回归信号筛选。

### 12. HW12 - CPCV 组合净化交叉验证与 PBO 过拟合审计
- 🟢 **L1**: 使用标准 K-Fold CV 评估 ML 策略。
- 🟡 **L2**: 分析 K-Fold 在金融时序中的重叠标签样本泄漏 (Overlapping Labels Leakage)。
- 🔴 **L3 (手撕核心)**：**手撕 Purged Group TimeSeries Cross-Validation (Purging & Embargo)**：
  1. 根据事件开盘到平仓的事件区间 $[t_{i,start}, t_{i,end}]$；
  2. 剔除训练集中与验证集时间重叠的样本 (Purging)；
  3. 在验证集后增加 Embargo 隔离带，严防自相关泄漏。
- 👑 **L4**: 计算 Probability of Backtest Overfitting (PBO)，评估拟合过度风险。

### 13. HW13 - Almgren-Chriss 最优拆单轨迹与冲击成本
- 🟢 **L1**: 计算 VWAP 与 TWAP 均匀拆单执行轨迹。
- 🟡 **L2**: 拟合平方根市场冲击成本模型 (Square-Root Market Impact Model)。
- 🔴 **L3 (手撕核心)**：**手写 Almgren-Chriss 闭式解与动态规划求解器**：
  $$ x_j = \frac{\sinh(\kappa (T - t_j))}{\sinh(\kappa T)} X $$
  平衡永久冲击 (Permanent Impact) 与暂态冲击 (Temporary Impact) 及持仓风险。
- 👑 **L4**: 结合微观盘口深度，实现自适应限价单/市价单路由。

### 14. HW14 - 暗池与 SOR 智能订单路由
- 🟢 **L1**: 模拟多交易所连续竞价撮合盘口。
- 🟡 **L2**: 评估订单在暗池 (Dark Pool) 中的隐蔽成交概率。
- 🔴 **L3 (手撕核心)**：**手写 Smart Order Router (SOR) 整数线性规划/贪心分配算法**。
- 👑 **L4**: 高频低延迟消息队列模拟。

### 15. HW15 - 盘口队列与挂单成交概率
- 🟢 **L1**: 读取 L2 盘口买一卖一 Depth 数据。
- 🟡 **L2**: 计算 Order Flow Imbalance (OFI) 订单流不平衡指标。
- 🔴 **L3 (手撕核心)**：**手写 L3 限价订单簿 (Limit Order Book) 挂单队列位置 (Queue Position) 模拟器**。
- 👑 **L4**: Hawkes Process 点过程拟合挂单与撤单冲击。

### 16. HW16 - Gymnasium 金融 RL 交易环境设计
- 🟢 **L1**: 创建 OpenAIGym 基础交易环境 Wrapper。
- 🟡 **L2**: 设计状态空间 (State: 过去 30 天 K 线 + 仓位)、动作空间 (Action: 买/卖/持有)。
- 🔴 **L3 (手撕核心)**：**手写扣除滑点与手续费的夏普比率/回撤敏感奖励函数 (Reward Function)**，防止 agent 陷入过度交易陷阱。
- 👑 **L4**: 使用 Stable-Baselines3 训练 PPO/DQN Agent 并做 Out-of-Sample 验证。

### 17. HW17 - Qlib 因子研究与成本敏感回测 (Capstone)
- 🟢 **L1**: 在 Qlib / pandas 中构建 Alpha101 基础因子（如 Alpha006, Alpha012）。
- 🟡 **L2**: 计算 Rank IC, ICIR, 因子 Turnover，并做分组回测 (Decile Backtest)。
- 🔴 **L3 (手撕核心)**：**手写事件驱动成本敏感回测引擎**：
  1. 考虑买卖印花税、双边佣金与滑点；
  2. 计算 Turnover-Adjusted Sharpe Ratio；
  3. 输出完整的无前视偏差审计报告。
- 👑 **L4**: 结合 LightGBM + Meta-labeling 进行二级过滤，实盘仿真跑通全流程。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-quant/tests/` 目录下为上述作业运行单元测试：

```bash
pytest 03-Projects/projects-quant/tests/test_hw01_capm.py
pytest 03-Projects/projects-quant/tests/test_hw06_garch.py
pytest 03-Projects/projects-quant/tests/test_hw12_cpcv.py
```
