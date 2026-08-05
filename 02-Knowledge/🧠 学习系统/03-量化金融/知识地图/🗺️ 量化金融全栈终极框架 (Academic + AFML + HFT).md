---
type: index
topic: "量化金融全栈终极框架 (Academic + AFML + HFT)"
created: 2026-08-04
updated: 2026-08-05
status: active
difficulty: beginner
concept: ["数学金融", "金融机器学习", "微观结构", "高频交易"]
prerequisites: ["完成量化金融课程说明与先修诊断"]
related: ["量化金融课程说明与先修诊断", "Capstone-统一标的贯穿实战项目"]
tags: [索引, 量化金融, 终极框架, MOC, 渐进式学习]
flow: knowledge
kind: moc
---

# 🗺️ 量化金融全栈知识地图 (Academic + AFML + HFT)

> [!important] 本页职责：查阅地图
> 正式学习、当前位置和下一步统一返回 [[🗺️ 量化金融学习路径]]。本页只展示全量知识资产，不代表全部内容都是必修，也不用于替代 Week 0-9。

> **使用方式**：需要查找下游主题、作业或选修内容时再使用本页。随机控制、强化学习与 HFT 属于完成 Week 9 后的选修区。

---

## 🌳 量化学习技能树 (Dataview 自动化引擎)

> **🚀 提示**：下表由 Dataview 自动扫描全库生成。未来新增课程，只需在卡片头部加上 `nav_level: 11` 即可自动并入技能树！

```dataview
TABLE WITHOUT ID
  "Lv " + nav_level AS "Level",
  file.link AS "任务卡片",
  difficulty AS "难度"
FROM "02-Knowledge/🧠 学习系统/03-量化金融"
WHERE nav_level != null
SORT nav_level ASC
```

## Level 0：基础研究协议

> **本阶段目标**：依次通过 K01-K06，能用可运行断言说明收益口径、数据口径、时间协议、面板运算、滚动特征与样本泄漏边界。
> **验收标准**：完成 [[03-Projects/Capstone-AAPL/README|AAPL Phase 1 无泄漏基线]]，测试全绿，并解释为什么演示回测结果不能证明未来盈利。

### 0.1 认知建立：我们为什么坐在这里？
- [[量化金融-启蒙-主观交易与量化交易的本质区别]]
- 待创建：均线交叉在震荡市的 Whipsaw 效应（不计入当前必修清单）

### 0.2 实操初探：第一行代码与防坑指南
- [[最大回撤]]
- [[收益率与对数收益率]]
- [[时间索引与频率（量化）]]
- [[Pandas分组聚合与透视表]]
- [[回测框架与无泄漏实验]]
- [[策略评价指标]]
- [[样本泄漏]]
- [[夯实基础常见题型 (量化金融基石)]]
- [[做空生猪]]
- [[量化金融-实战起航-本地环境配置与依赖(requirements)]] (💻 必读：消灭 ModuleNotFoundError)
- [[数据排雷指南：复权、生存者偏差与未来函数]] (🛑 必读的救命稻草)
- [[手写第一个均线策略与回测评价指标]]
- [[不要骗自己：什么叫前视偏差 (Look-Ahead Bias)]]


### 0.3 避坑与错题集
- [[量化金融错题漏洞入口 (Quant Finance Pitfalls)]]
- [[量化金融-Level0-累计交错测验]]

---

## 🏆 贯穿全周期的主线战役 (The Capstone Thread)
- [[Capstone-统一标的贯穿实战项目]] (同一只苹果，从均线研究到期权定价)

## 🏛️ Pillar 1: 学术定价与经典量化基石 (Academic Foundations)
<details>
<summary>👉 点击展开 (难度：高中 - 大学本科) 🎖️ <code>[Lv.3 回测分析师]</code> -> <code>[Lv.4 风险观察员]</code></summary>
<br>

> **🎯 本阶段目标**：掌握量化世界里的经典物理定律（定价公式与风险模型）。
> **⚔️ 关底大作业**：完成 [[[支线任务] HW01-CAPM与Alpha检验]] 与 [[[支线任务] HW05-BSM期权定价与对冲]]。
> **🆘 补底捷径**：如果卡在线性代数，先前往 [[02-Knowledge/🧠 学习系统/09-高等代数/🗺️ 高等代数学习路径|高等代数学习路径]]；微积分补底尚未纳入本路径正式清单。

### 1.1 资产定价与因子投资 (为什么会有超额收益？)
- [[🧠 夏普比率 (Sharpe Ratio)]]
- [[🧠 无风险资产与资本市场线 (Risk-free Asset & Capital Market Line)]]
- [[马科维茨有效前沿]]
- [[相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)]]
- [[WACC加权平均资本成本]]
- [[ROE 拆解与杜邦分析 (DuPont Analysis)]]
- [[三大财务报表钩稽关系 (Interrelationship of Financial Statements)]]
- [[EBITDA 息税折旧摊销前利润 (Earnings Before Interest, Taxes, Depreciation, and Amortization)]]
- [[ABS 资产证券化 (Asset-Backed Securities)]]
- [[同业存单 (Negotiable Certificate of Deposit, NCD)]]
- [[国债逆回购 (Treasury Reverse Repo)]]
- [[CAPM 资本资产定价模型]]
- [[Fama-French三因子模型]]
- [[量化金融-资产定价-多因子模型]]
- [[Fama-MacBeth 两步回归法 (Fama-MacBeth Two-Step Regression)]]
- [[Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)]]
- [[质量因子与 QMJ 盈利能力溢价 (Quality Factor & QMJ - Quality Minus Junk)]]
- [[价值因子与 HML 账面市值比溢价 (Value Factor & HML)]]

### 1.2 时间序列与协整套利 (历史如何预测未来？)
- [[为什么可以避免伪回归]]
- [[Johansen检验]]
- [[协整关系与 Engle-Granger 两步法 (Cointegration & Engle-Granger Method)]]
- [[量化金融-平稳性与单位根检验实战]]
- [[ACF 自相关函数与 PACF 偏自相关函数 (Autocorrelation & Partial Autocorrelation Functions)]]
- [[单位根检验与 ADF 检验 (Unit Root & Augmented Dickey-Fuller Test)]]
- [[配对交易与统计套利 (Pairs Trading & Statistical Arbitrage)]]
- [[均值回归策略 (Mean-Reversion Trading Strategy)]]
- [[趋势跟踪策略框架与 CTA 交易哲学 (Trend-Following Framework & CTA Trading)]]

### 1.3 波动率、极值与风险管理
- [[非对称GARCH模型]]
- [[EVT极值理论与VaR-CVaR]]
- [[参数法VaR（方差-协方差法）]]
- [[历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)]]
- [[蒙特卡洛模拟法 VaR (Monte Carlo Simulation VaR)]]
- [[量化金融-波动率-GARCH家族模型]]
- [[非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)]]
- [[极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)]]
- [[量化金融-风险管理-期望损失分解与ES理论]]
- [[量化金融-风险管理-参数法与历史模拟法VaR]]

### 1.4 随机微积分与衍生品 (华尔街最艰深的数学底座)
- [[二叉树期权定价模型 (Binomial Option Pricing Model)]]
- [[期权希腊字母 (Option Greeks_ Delta, Gamma, Theta, Vega, Rho)]]
- [[利率期限结构与短利率单因子模型 (Yield Curve & Short Rate Models_ Vasicek & Hull-White)]]
- [[量化金融-随机过程-伊藤引理与随机微分方程]]
- [[Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)]]
- [[量化金融-期权定价-Greeks与动态对冲]]
- [[高阶希腊字母与衍生品风险对冲 (Higher-Order Greeks_ Vanna, Volga & Charm)]]
- [[隐含波动率与波动率微笑 (Implied Volatility & Volatility Smile)]]
- [[量化金融-衍生品-蒙特卡洛期权定价与方差缩减]]

</details>

---

## 🤖 Pillar 2: 现代金融机器学习 (Financial Machine Learning)
<details>
<summary>👉 点击展开 (难度：研究生 - Quant Researcher) 🎖️ <code>[Lv.5 组合分析师]</code> -> <code>[Lv.6 机器学习炼丹师]</code></summary>
<br>

> **🎯 本阶段目标**：在冻结数据和验证协议后建立非线性基线，并用严格的样本外评估区分信号、噪声与过拟合。
> **⚔️ 关底大作业**：完成 [[[支线任务] HW12-CPCV与PBO过拟合审计]]。
> **🆘 补底捷径**：如果你发现这部分概念难以理解，强烈建议先阅读 Lopez de Prado 的《Advances in Financial Machine Learning》。

### 2.1 现代采样与数据清洗 (把垃圾变废为宝)
- [[Volume Bars与Dollar Bars信息驱动采样 (Information-Driven Bars)]]
- [[金融微观结构采样棒 (Financial Data Bars_ Volume, Dollar & Imbalance Bars in AFML)]]
- [[OHLCV字段清洗与复权]]
- [[因子预处理：去极值、中性化与标准化 (Factor Preprocessing_ Winsorization, Neutralization & Z-Score)]]

### 2.2 特征工程与元标注 (主模型做预测，副模型定仓位)
- [[滚动窗口与波动率特征]]
- [[树模型基线]]
- [[Meta-labeling 二级标签与元标注 (Meta-labeling in Financial ML)]]

### 2.3 交叉验证与防过拟合 (不要骗自己系列进阶版)
- [[时间序列验证]]
- [[PBO回测过拟合概率与Deflated Sharpe Ratio (Probability of Backtest Overfitting)]]
- [[Purged Group TimeSeries Cross-Validation 净化交叉验证 (Purged Group K-Fold CV)]]
- [[策略回测前视偏差与生存者偏差防范审计 (Look-Ahead & Survivorship Bias Audit)]]

### 2.4 高阶组合优化
- [[HRP分层风险平价]]
- [[Marchenko-Pastur定理]]
- [[量化金融-资产定价-马科维茨组合与协方差矩阵正定化]]
- [[量化金融-投资组合-Black-Litterman模型推导]]
- [[协方差去噪与随机矩阵理论 RMT (Covariance Denoising & Marchenko-Pastur Law in AFML)]]
- [[分层风险平价组合 HRP (Hierarchical Risk Parity in AFML)]]
- [[动态止损机制与风险平价仓位管理 (Stop-Loss Mechanisms & Risk-Parity Position Sizing)]]
- [[动态下注规模与凯利公式 (Bet Sizing & Kelly Criterion in AFML)]]

</details>

---

## ⚡ Pillar 3: 市场微观结构与高频执行 (Microstructure & HFT)
<details>
<summary>👉 点击展开 (难度：核心机房工程师 - 算法交易员) 🎖️ <code>[Lv.7 极速算法师]</code></summary>
<br>

> **🎯 本阶段目标**：理解交易所撮合、订单簿、做市库存风险和大额执行的冲击成本；没有合法逐笔数据时只做机制学习，不声称存在可交易 Alpha。
> **⚔️ 关底大作业**：完成 [[[支线任务] HW15-盘口队列与挂单概率]] 与 [[[支线任务] HW13-AC最优拆单轨迹]]。
> **🆘 补底捷径**：卡在随机控制推导？退回到 [[量化金融-动态最优化-1-贝尔曼方程直觉与离散推导]] 看故事。

### 3.1 盘口重建与微观特征 (用放大镜看市场)
- [[盘口微观队列与L2数据]]
- [[盘口特征]]
- [[限价订单簿数据与 L1_L2_L3 盘口重建 (Limit Order Book Data & Reconstructing L1_L2_L3)]]
- [[买卖价差及其微观结构拆解 (Bid-Ask Spread & Microstructure Decomposition)]]
- [[订单流不平衡 (Order Flow Imbalance, OFI)]]
- [[高频 Alpha 信号工程与盘口特征构建 (High-Frequency Signals & Microstructure Features)]]

### 3.2 高频做市与信息模型 (如何安全地双向报价)
- [[订单类型与交易所连续竞价撮合机制 (Order Types & Continuous Double Auction)]]
- [[做市商库存模型与 Avellaneda-Stoikov 框架 (Inventory Models & Avellaneda-Stoikov Framework)]]
- [[信息交易模型推导 (Kyle 1985 经典单期模型)]]
- [[信息交易模型与 VPIN 毒性订单流度量 (Information-Based Models & VPIN)]]
- [[价格发现机制与 Hasbrouck 信息份额模型 (Price Discovery & Hasbrouck Information Share)]]

### 3.3 算法执行与智能路由 (大资金如何隐身)
- [[TWAP 时间加权平均价格 (Time-Weighted Average Price)]]
- [[VWAP 成交量加权平均价格 (Volume-Weighted Average Price)]]
- [[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型]]
- [[量化金融-执行策略-暗池撮合与SOR智能路由]]
- [[市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)]]
- [[跨市场排队优先权与挂单成交概率 (Queue Position & Fill Probability in High-Frequency Trading)]]

### 3.4 低延迟系统架构
- [[实盘风控]]
- [[高频交易系统架构与模块解耦设计 (High-Frequency Trading System Architecture)]]
- [[低延迟系统设计与 C++_FPGA 极致性能优化 (Low-Latency System Design & C++_FPGA Optimization)]]

### 3.5 动态最优化与强化学习
- [[金融MDP设计与奖励函数工程 (Financial MDP & Reward Engineering)]]
- [[RL 交易实验常见题型]]
- [[交易环境设计]]
- [[风险约束下的RL]]
- [[量化金融-动态最优化-1-贝尔曼方程直觉与离散推导]]
- [[量化金融-动态最优化-2-连续时间HJB方程推导]]
- [[量化金融-动态最优化-3-Merton最优消费问题应用]]
- [[强化学习金融交易环境与 MDP 状态-动作空间设计 (Gym-Finance & MDP in Financial RL)]]

- [[Qlib回测工作流(Qlib Workflow)]]
- [[ML 如何规范地进入金融建模常见题型]]
</details>

---

## 📜 赏金公会：全量支线副本集会所 (Quest Board)

> **🎯 提示**：想要一口气刷题？这里为您聚合了所有挂载在各主线任务底下的副本入口。无需跑图，直接接取悬赏！

```dataview
TABLE WITHOUT ID
  file.link AS "支线副本名称"
FROM "02-Knowledge/🧠 学习系统/03-量化金融"
WHERE startswith(file.name, "[支线任务]")
SORT file.name ASC
```
