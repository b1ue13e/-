---
type: index
topic: "量化金融全栈终极框架 (Academic + AFML + HFT)"
created: 2026-08-04
status: active
difficulty: beginner
concept: ["数学金融", "金融机器学习", "微观结构", "高频交易"]
prerequisites: ["无要求（包含新手村引导）"]
related: []
tags: [索引, 量化金融, 终极框架, MOC, 渐进式学习]
flow: knowledge
kind: moc
---

# 🗺️ 量化金融全栈终极框架 (Academic + AFML + HFT)

> **导读**：欢迎来到量化金融的终极武库。
> 为了防止信息过载，本指南采用了**“任务驱动”**与**“渐进式展开”**设计。每一个折叠面板后，不再是冰冷的知识点列表，而是明确的“通关目标”、“实战大作业”和“知识救生圈”。
>
> 🧗‍♂️ **如果是零基础小白，请只在 【Level 0】 停留，直到你完成第一次回测再往下走！**

---

## 🌳 量化通关技能树 (Dataview 自动化引擎)

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

## 🐣 Level 0: 新手启蒙村 (小白从这里开始) 🎖️ `[Lv.1 量化探索者]` -> `[Lv.2 策略设计师]`

> **🎯 本阶段目标**：建立量化的基本信仰，感受数据律动，获得第一口“赚钱幻觉”的多巴胺，不要一上来就推微积分！
> **⚔️ 验收标准**：写出不到 20 行代码的均线回测，并明白为什么回测赚钱实盘会亏。

### 0.1 认知建立：我们为什么坐在这里？
- [[量化金融-启蒙-主观交易与量化交易的本质区别]]
- [[为什么均线交叉在震荡市会被来回打脸 (Whipsaw Effect)]] (待补)

### 0.2 实操初探：第一行代码与防坑指南
- [[量化金融-实战起航-本地环境配置与依赖(requirements)]] (💻 必读：消灭 ModuleNotFoundError)
- [[数据排雷指南：复权、生存者偏差与未来函数]] (🛑 必读的救命稻草)
- [[手写第一个均线策略与回测评价指标]]
- [[不要骗自己：什么叫前视偏差 (Look-Ahead Bias)]]

---

## 🏆 贯穿全周期的主线战役 (The Capstone Thread)
- [[Capstone-统一标的贯穿实战项目]] (同一只苹果，从均线研究到期权定价)

## 🏛️ Pillar 1: 学术定价与经典量化基石 (Academic Foundations)
<details>
<summary>👉 点击展开 (难度：高中 - 大学本科) 🎖️ <code>[Lv.3 回测分析师]</code> -> <code>[Lv.4 风险观察员]</code></summary>
<br>

> **🎯 本阶段目标**：掌握量化世界里的经典物理定律（定价公式与风险模型）。
> **⚔️ 关底大作业**：完成 [[[支线任务] HW01-CAPM与Alpha检验]] 与 [[[支线任务] HW05-BSM期权定价与对冲]]。
> **🆘 补底捷径**：如果卡在微积分和线性代数，请暂时退出，前往 `[[09-高等代数]]` 的【矩阵基本运算】补课。

### 1.1 资产定价与因子投资 (为什么会有超额收益？)
- [[CAPM 资本资产定价模型]]
- [[Fama-French三因子模型]]
- [[量化金融-资产定价-多因子模型]]
- [[Fama-MacBeth 两步回归法 (Fama-MacBeth Two-Step Regression)]]
- [[Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)]]
- [[质量因子与 QMJ 盈利能力溢价 (Quality Factor & QMJ - Quality Minus Junk)]]
- [[价值因子与 HML 账面市值比溢价 (Value Factor & HML)]]

### 1.2 时间序列与协整套利 (历史如何预测未来？)
- [[ACF 自相关函数与 PACF 偏自相关函数 (Autocorrelation & Partial Autocorrelation Functions)]]
- [[单位根检验与 ADF 检验 (Unit Root & Augmented Dickey-Fuller Test)]]
- [[量化金融-时间序列-协整检验与统计套利]]
- [[配对交易与统计套利 (Pairs Trading & Statistical Arbitrage)]]
- [[均值回归策略 (Mean-Reversion Trading Strategy)]]
- [[趋势跟踪策略框架与 CTA 交易哲学 (Trend-Following Framework & CTA Trading)]]

### 1.3 波动率、极值与风险管理 (如何测量深渊的深度？)
- [[量化金融-波动率-GARCH家族模型]]
- [[非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)]]
- [[极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)]]
- [[量化金融-风险管理-期望损失分解与ES理论]]
- [[量化金融-风险管理-参数法与历史模拟法VaR]]

### 1.4 随机微积分与衍生品 (华尔街最艰深的数学底座)
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

> **🎯 本阶段目标**：抛弃学术界天真的假设，用现代机器学习手段榨取数据里的非线性 Alpha，同时极力避免把噪声当成信号（过拟合）。
> **⚔️ 关底大作业**：完成 [[[支线任务] HW12-CPCV与PBO过拟合审计]]。
> **🆘 补底捷径**：如果你发现这部分概念难以理解，强烈建议先阅读 Lopez de Prado 的《Advances in Financial Machine Learning》。

### 2.1 现代采样与数据清洗 (把垃圾变废为宝)
- [[金融微观结构采样棒 (Financial Data Bars_ Volume, Dollar & Imbalance Bars in AFML)]]
- [[OHLCV字段清洗与复权]]
- [[因子预处理：去极值、中性化与标准化 (Factor Preprocessing_ Winsorization, Neutralization & Z-Score)]]

### 2.2 特征工程与元标注 (主模型做预测，副模型定仓位)
- [[Meta-labeling 二级标签与元标注 (Meta-labeling in Financial ML)]]

### 2.3 交叉验证与防过拟合 (不要骗自己系列进阶版)
- [[Purged Group TimeSeries Cross-Validation 净化交叉验证 (Purged Group K-Fold CV)]]
- [[策略回测前视偏差与生存者偏差防范审计 (Look-Ahead & Survivorship Bias Audit)]]

### 2.4 高阶组合优化 (别再全仓梭哈了)
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

> **🎯 本阶段目标**：进入毫秒级的微观战场，研究交易所的匹配引擎，像做市商一样双向报价薅羊毛，或者大单建仓时不被别人发现（冲击成本）。
> **⚔️ 关底大作业**：完成 [[[支线任务] HW15-盘口队列与挂单概率]] 与 [[[支线任务] HW13-AC最优拆单轨迹]]。
> **🆘 补底捷径**：卡在随机控制推导？退回到 [[量化金融-动态最优化-1-贝尔曼方程直觉与离散推导]] 看故事。

### 3.1 盘口重建与微观特征 (用放大镜看市场)
- [[限价订单簿数据与 L1_L2_L3 盘口重建 (Limit Order Book Data & Reconstructing L1_L2_L3)]]
- [[买卖价差及其微观结构拆解 (Bid-Ask Spread & Microstructure Decomposition)]]
- [[订单流不平衡 (Order Flow Imbalance, OFI)]]
- [[高频 Alpha 信号工程与盘口特征构建 (High-Frequency Signals & Microstructure Features)]]

### 3.2 高频做市与信息模型 (如何安全地双向报价)
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

### 3.4 极速系统架构 (天下武功唯快不破)
- [[高频交易系统架构与模块解耦设计 (High-Frequency Trading System Architecture)]]
- [[低延迟系统设计与 C++_FPGA 极致性能优化 (Low-Latency System Design & C++_FPGA Optimization)]]

### 3.5 动态最优化与强化学习 (让机器自动进化)
- [[量化金融-动态最优化-1-贝尔曼方程直觉与离散推导]]
- [[量化金融-动态最优化-2-连续时间HJB方程推导]]
- [[量化金融-动态最优化-3-Merton最优消费问题应用]]
- [[强化学习金融交易环境与 MDP 状态-动作空间设计 (Gym-Finance & MDP in Financial RL)]]

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
