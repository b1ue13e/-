---
type: concept
topic: BeneishMScore与Sloan应计项因子
created: '{date}'
status: learning
difficulty: intermediate
concept: []
prerequisites: []
related: []
tags:
- 学习
- 量化金融
- 财报分析
- BeneishMScore
- Sloan应计项
- 财务造假
- 财报排雷
- 质量因子
title: Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)
date: 2026-07-23
course: 量化金融
importance: A
upstream:
- '[[三大报表关系]]'
- '[[ROE拆解与杜邦分析]]'
downstream:
- '[[质量因子]]'
- '[[策略回测前视偏差与生存者偏差防范审计 (Look-Ahead & Survivorship Bias Audit)|策略回测前视偏差与生存者偏差审计]]'
---

# Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)

---

## 0. 先判断它值不值得深挖

**分类：A 类（核心概念，必须深挖）**

**理由：**
Beneish M-Score 模型（Messod Beneish 1999 年提出）与 Sloan 应计项因子（Richard Sloan 1996 年提出）是基本面量化选股（Quantitative Value / Quality）中防范“业绩爆雷与财务造假”最著名的量化黑科技。著名案例：Beneish M-Score 曾在安然（Enron）破产前数月精准识别出其财报严重造假。在量化实盘中，即使一个股票按 PE/PB 极其便宜，如果其 M-Score 高于警戒线或应计项过度偏高，系统会将其强制列入“黑名单（Blacklist）”剔除，避免回测陷阱与实盘穿仓。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**

假设你运行一个基于“高 ROE + 低 PE”的价值量化选股策略。
你选出了一家叫“康美药业”或“安然”的股票：账面净利润同比飙升 100%，ROE 高达 30%，PE 却只有 8 倍，看似完美的“超级价值股”！
你重仓买入后不久，该公司突发暴雷：审计师出具拒绝表示意见，监管立案调查造假，股价连续 20 个跌停板甚至退市。**你数年的 Alpha 收益在一个月内全被清零。**

**以前的方法在哪里卡住：**
1. **只看净利润（Net Income）**：忽视了会计准则（权责发生制 Accrual Accounting）允许管理层通过虚构应收账款（AR）和提前确认收入来伪造利润。
2. **缺乏量化评分系统**：人工看财报效率低且容易被粉饰手法蒙蔽，缺乏能批量对 4000 只股票进行自动审计扫描的数学模型。

**为什么必须引入 Beneish M-Score 与 Sloan 应计项因子：**
利用资产负债表与利润表多维度勾稽关系，计算**应计项 (Accruals) 占总资产比例**，并使用 8 维概率Probit/Logit 模型导出 **M-Score 财务操纵得分**。

**它到底解决了哪类问题：**
解决了**量化策略如何在买入前自动扫描防范财务造假、剥离无现金支撑的纸面虚高利润**的问题。

---

## 2. 为什么它重要？它有什么用？

- **体系与大图景**：第一阶段（财务量化）与第三阶段（基本面选股）的避险安全网，直接为[[质量因子]]与[[价值因子]]策略提供硬核排雷过滤器。
- **量化与实战应用**：
  1. **做多/做空黑名单过滤**：当 $M\text{-Score} > -1.78$ 时，判定该股票具有极高财报操纵概率，从多头股票池强制剥离。
  2. **Alpha 空头策略 (Short-side Alpha)**：做空高应计项（High Accruals）且高 M-Score 的垃圾操纵股，获取反转向下溢价。

---

## 3. 学它之前需要哪些前置知识？

1. **[[三大报表关系]]**：理解净利润（Net Income）与经营现金流（CFO）的差额即为应计项（Accruals）。
2. **最小必要背景（权责发生制 Accrual Accounting）**：
   > 权责发生制下：销售商品即使没收到现金，只要开了发票就能记为“收入”（增加应收账款 AR）。
   > $\text{净利润 (Net Income)} = \text{经营现金流 (CFO)} + \text{应计项 (Accruals)}$。
   > 若应计项占净利润比例过高，说明利润全是在账面纸上，真金白银现金为零！

---

## 4. 用直觉语言解释它

### 生活类比：看奶茶店的“记账白条”与“收银机现金”

- 假设你准备收购两家年账面利润都是 100 万元的奶茶店：
  - **A 店**：收银机里实打实收到了 95 万元现金，剩下的 5 万元是企业客户下个月结账的白条。（**低应计项，高现金含金量**）
  - **B 店**：收银机里只有 10 万元现金，剩下的 90 万元全是隔壁狐朋狗友欠下的记账白条（应收账款 AR）！而且 B 店今年的折旧提得极低、存货堆满仓库。（**高应计项，极高造假概率**）
- **Sloan 应计项** 就像：拿秤称一称那 90 万元白条占总资产的重量。
- **Beneish M-Score** 就像：老牌会计师发明的“8 维度探照灯”，专门去打量那些白条突然猛增、折旧突然变慢、销售费用突然被塞进资产里的可疑迹象。

**直觉本质**：
用现金流检验账面利润，用资产负债表的异常膨胀揭穿利润表的美化假象。

«“Sloan 应计项就是看利润里有多少是没收回的白条；Beneish M-Score 就是一套综合排雷仪表盘，专门识别假账。”»

---

## 5. 正式定义、核心公式、符号解释

### 核心定义
1. **Sloan 应计项因子 (Sloan Balance Sheet Accruals)**：指利用资产负债表非现金流动资产与非利息流动负债的变化量，衡量企业会计利润中未由真实现金流支撑的比例。
2. **Beneish M-Score 模型**：由 8 个财务比率构成的复合得分，用于估算企业操纵财务报表收益（Earnings Manipulation）概率的计量模型。

### 核心公式

#### 1. Sloan 资产负债表应计项公式 (Balance Sheet Accruals)
$$\text{Accruals}_t = (\Delta \text{NOA}_t) = (\Delta \text{Current Assets}_t - \Delta \text{Cash}_t) - (\Delta \text{Current Liabilities}_t - \Delta \text{ST Debt}_t - \Delta \text{Tax Payables}_t) - \text{Depreciation}_t$$
标准化应计项率：
$$\text{Sloan\_Accrual\_Ratio}_t = \frac{\text{Accruals}_t}{\text{Average Total Assets}_t}$$

#### 2. Beneish M-Score 八因素模型公式
$$M\text{-Score} = -4.84 + 0.920 \cdot \text{DSRI} + 0.528 \cdot \text{GMI} + 0.404 \cdot \text{AQI} + 0.892 \cdot \text{SGI} + 0.115 \cdot \text{DEPI} - 0.172 \cdot \text{SGAI} + 4.679 \cdot \text{TATA} - 0.327 \cdot \text{LVGI}$$

判定临界点：**当 $M\text{-Score} > -1.78$ 时（如 $-1.20$），模型发出财务操纵报警！**

### M-Score 8 大子比率含义表

| 比率名称 | 全称与计算公式 | 捕捉的操纵痕迹/意图 |
| :--- | :--- | :--- |
| **DSRI** | 预收账款周转天数指数 $\frac{\text{DSR}_t}{\text{DSR}_{t-1}}$ | 捕捉虚构收入与放宽信用赊销加速记账 |
| **GMI** | 毛利率指数 $\frac{\text{Margin}_{t-1}}{\text{Margin}_t}$ | 毛利率恶化时公司更有动机造假（$GMI > 1$ 发出警报） |
| **AQI** | 资产质量指数 $\frac{1 - (\text{PPE}_t + \text{Cash}_t)/\text{Assets}_t}{1 - (\text{PPE}_{t-1} + \text{Cash}_{t-1})/\text{Assets}_{t-1}}$ | 捕捉将费用化支出错误资本化（塞入其他资产） |
| **SGI** | 营业收入增长指数 $\frac{\text{Sales}_t}{\text{Sales}_{t-1}}$ | 高增长公司增长停滞时造假动机极高 |
| **DEPI** | 折旧率指数 $\frac{\text{Depr\_Rate}_{t-1}}{\text{Depr\_Rate}_t}$ | 捕捉延长资产折旧年限以虚增当期利润（$DEPI > 1$ 警报） |
| **SGAI** | 销售管理费用指数 $\frac{\text{SGA\_Ratio}_t}{\text{SGA\_Ratio}_{t-1}}$ | 销售费用率上升反映经营效率下降 |
| **LVGI** | 财务杠杆指数 $\frac{\text{Leverage}_t}{\text{Leverage}_{t-1}}$ | 债务负担加重触发债务契约违约风险 |
| **TATA** | 资产总应计项率 $\frac{\text{Net Income}_t - \text{CFO}_t}{\text{Total Assets}_t}$ | **最重要的权重！** 利润与现金流的直接脱节程度 |

---

## 6. 推导思路和思想来源

### 为什么 Beneish 给 TATA（总应计项率）赋予了高达 $+4.679$ 的正系数？
1. **造假的物理极限**：公司可以虚构销售合同、可以变更折旧年限，但它**无法伪造银行账户里的现金余额**。
2. **脱节显形**：如果 $\text{Net Income}$ 很高而经营现金流 $\text{CFO}$ 很低，说明多出来的所有利润全是靠财务手法捏造出来的。
3. **转念**：把净利润与现金流的背离度 $\frac{\text{Net Income} - \text{CFO}}{\text{Assets}}$ 乘以极大的惩罚权重 $+4.679$，能一枪命中所有虚增利润公司的要害！

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算例题（Sloan 应计项占比计算）

**题目**：
某上市公司财务数据如下（单位：亿元）：
- 2025 年净利润 $\text{Net Income} = 10.0$ 亿元；
- 2025 年经营活动现金流净额 $\text{CFO} = 2.0$ 亿元；
- 平均总资产 $\text{Total Assets} = 50.0$ 亿元。

求该公司的总应计项 $\text{Accruals}$ 以及 Sloan 应计项率 $\text{Sloan\_Ratio}$，并判断其现金流含金量。

**解答过程**：
1. 计算总应计项：
   $$\text{Accruals} = \text{Net Income} - \text{CFO} = 10.0 - 2.0 = 8.0 \text{ 亿元}$$
2. 计算 Sloan 应计项率：
   $$\text{Sloan\_Ratio} = \frac{8.0}{50.0} = 0.16 \quad (16\%)$$
3. **结论**：该公司 80% 的账面利润（8 亿/10 亿）没有现金支撑，应计项率高达 16%，属于高风险虚高利润股票！

---

### 例子 2：中等例题（DSRI 应收账款天数指数预警）

**题目**：
某公司 2024 年营业收入 10 亿，应收账款 1 亿（$\text{DSR}_{2024} = 0.10$）。
2025 年营业收入 12 亿（增长 20%），应收账款暴增至 3 亿（$\text{DSR}_{2025} = 0.25$）。
计算其 DSRI 指数，并分析其财务含义。

**解答过程**：
1. 计算 DSRI 指数：
   $$\text{DSRI} = \frac{\text{DSR}_{2025}}{\text{DSR}_{2024}} = \frac{0.25}{0.10} = 2.50$$
2. **分析**：DSRI 为 2.50（远大于 1.0）。说明在收入仅增长 20% 的情况下，应收账款占收入比率翻了 2.5 倍！
3. **结论**：该公司极有可能在年末通过向经销商大量塞货、开具无法收回的白条（或虚构发票）来硬塞 2025 年的业绩。

---

### 例子 3：实际应用（Python 计算 Beneish M-Score 与全市场黑名单排雷）

```python
import numpy as np
import pandas as pd

def calculate_beneish_m_score(dsri, gmi, aqi, sgi, depi, sgai, tata, lvgi):
    """
    计算 Beneish M-Score 得分
    """
    m_score = (-4.84 + 
               0.920 * dsri + 
               0.528 * gmi + 
               0.404 * aqi + 
               0.892 * sgi + 
               0.115 * depi - 
               0.172 * sgai + 
               4.679 * tata - 
               0.327 * lvgi)
    return m_score

# 模拟 3 只股票的财务比率
stocks_data = pd.DataFrame({
    'ticker': ['A_Normal', 'B_Warning', 'C_Fraud_Enron'],
    'DSRI': [1.02, 1.30, 2.10],
    'GMI':  [0.98, 1.15, 1.45],
    'AQI':  [1.01, 1.20, 1.85],
    'SGI':  [1.05, 1.25, 1.60],
    'DEPI': [1.00, 1.10, 1.40],
    'SGAI': [1.02, 1.05, 0.95],
    'TATA': [0.02, 0.08, 0.22],
    'LVGI': [1.01, 1.15, 1.50]
})

stocks_data['M_Score'] = calculate_beneish_m_score(
    stocks_data['DSRI'], stocks_data['GMI'], stocks_data['AQI'], stocks_data['SGI'],
    stocks_data['DEPI'], stocks_data['SGAI'], stocks_data['TATA'], stocks_data['LVGI']
)

stocks_data['Is_Manipulator'] = stocks_data['M_Score'] > -1.78

print("=== Beneish M-Score 财报排雷结果 ===")
for idx, row in stocks_data.iterrows():
    print(f"股票: {row['ticker']:15s} | M-Score: {row['M_Score']:+.4f} | 状态: {'⚠️ 拦截! (财报操纵概率高)' if row['Is_Manipulator'] else '✅ 安全'}")
```

---

## 7.5 💥 课本挂载与工业级实战模块 (Textbook Mapping & Production Lab)

### 7.5.1 📚 经典课本章节锚定
- **教材挂载 1**：Tobias Carlisle & Wesley Gray *《Quantitative Value》* 第 3 章 "Eliminating Earnings Manipulators (Beneish M-Score)" 与 第 4 章 "Eliminating Fraud"。
  - **课本必读重点**：M-Score 八因素构建逻辑、Sloan 应计项二分法与做空低质量股票。
  - **推荐课后计算**：算出安然 1999 年与 2000 年财报的 M-Score（分别为 -1.88 与 -1.31）。
- **教材挂载 2**：马丁·弗里德森 *《财务报表分析 (Financial Statement Analysis)》* 第 11 章 "Forecasting Financial Distress"。
  - **实战挂载重点**：现金流与利润背离的警示信号与审计调整。

### 7.5.2 ⚙️ 工业级 Python 最小可运行实战脚手架
（见上方 例子 3 完整代码）

### 7.5.3 ⚠️ 实盘落地“踩坑指南”与回测陷阱
1. **金融股与重资产科技股不适用**：
   Beneish M-Score 是为**制造/零售等非金融企业**设计的。银行与保险公司的资产负债表结构天然包含极高杠杆与应收账款，直接套用 M-Score 会导致 100% 误杀。
2. **高增长初创公司 (High Growth Startups) 误伤**：
   快速扩张的高科技公司（SGI 极高）可能因正常的业务扩张导致应收账款增加。必须结合行业中位数进行中性化调整。

### 7.5.4 📊 实战性能评估指标体系
- **M-Score 警戒线**：$-1.78$（高于该值剔除）。
- **Sloan 应计项五分位数 (Sloan Quintiles)**：做多 Q1 (最低应计项)，做空 Q5 (最高应计项)。
- **爆雷率降低幅度 (Blowup Reduction Rate)**：引入排雷过滤器后组合成分股暴跌事件降低比例。

### 7.5.5
> 🔓 **作业解锁前置条件**：学完 [[三大报表关系]] + [[ROE拆解与杜邦分析]] + [[利润表与利润质量]] + [[Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)|BeneishMScore与Sloan应计项因子]] 即可正式解锁本 Challenge 实战！
> 💡 **解锁指引**：掌握三大财务报表交叉校验与现金流背离识别后即可解锁全市场财报排雷。

 🧪 拓展实验与李宏毅式实战 Challenge 题 (HW04-Beneish M-Score 八因素财报排雷与做空垃圾股)

本作业参考 **李宏毅 (Hung-yi Lee) 教授 ML 课程作业架构** 设计，设置四个渐进式难度基线 (Baselines)：

- 🟢 **简单基线 (Simple Baseline)**：
  - **任务要求**：手算单家上市公司 2024 年与 2025 年的 DSRI、TATA 指数及 Beneish M-Score，判定其造假风险。
  - **达标标准**：代码无 Error 跑通，输出基础结果。

- 🟡 **中等基线 (Medium Baseline)**：
  - **任务要求**：编写 Python 自动化排雷脚本，批量计算沪深全市场 4000 只股票的 8 维比率，生成 $M\text{-Score} > -1.78$ 警报黑名单。
  - **达标标准**：完成核心算法的向量化与参数校准，模型表现达到基线水平。

- 🔴 **强基线 (Strong Baseline)**：
  - **任务要求**：结合 Sloan 应计项因子（Sloan Accruals），构建五分位组合 (Quintile Portfolios)，验证买入最低应计项 (Q1)、卖出最高应计项 (Q5) 的对冲 Alpha。
- **达标标准**：使用预先固定的数据、时间切分、基准与成本口径完成样本外比较；改进必须同时报告效应大小、风险变化和失败案例，不设跨数据集通用收益阈值。

- 🟣 **Boss 基线 (Kaggle / 实盘级基线)**：
  - **任务要求**：构建基本面 Quality-Junk 复合做空研究，结合 M-Score 与 Altman Z-Score 识别高风险股票；预先声明财报可得时间、退市样本、借券约束和成本，报告净 Alpha、误报、样本外衰减与失败案例，不设置通用收益门槛。
- **达标标准**：完成预先注册的过拟合、样本外与压力测试；报告 PBO 的切分方案、不确定性和阈值敏感性，不把单一候选阈值当作跨市场通用上线标准。


## 8. 常见误区和易混概念

### 误区 1：只要净利润在增长，公司经营状况就一定越来越好

错误直觉：“公司利润今年增长了 50%，赶紧加仓。”  
为什么错：如果利润增长 50% 主要是靠延伸折旧年限、把费用资本化和向关联方赊销拉起来的（CFO 现金流为负），这是崩盘前的虚假繁荣。  
正确理解：**必须结合 Sloan 应计项和 M-Score 确认利润是否有真实现金支持。**

### 概念对比：Sloan 应计项 vs Beneish M-Score vs Altman Z-Score

| 维度 | Sloan 应计项因子 | Beneish M-Score | Altman Z-Score |
| :--- | :--- | :--- | :--- |
| **侧重点** | 专门量化**现金流与利润的背离度** | 专门识别**主观财务报表操纵/造假** | 专门预测**企业破产与违约风险** |
| **指标数量** | 1 个复合应计项率 | 8 个财务比率 | 5 个财务比率 |
| **警示方向** | 应计项越高，未来收益越差 | 得分大于 -1.78 代表高造假风险 | 得分小于 1.81 代表高破产风险 |

---

## 9. 相关知识点与 Obsidian 双链建议

请帮我建立知识网络。

注意：不要只列链接。每个链接后面必须用一句话说明“为什么要链接”。

上游依赖

- [[三大报表关系]]：提供基础概念与理论推导支撑。
- [[ROE拆解与杜邦分析]]：提供基础概念与理论推导支撑。

下游延伸

- [[质量因子]]：进一步延伸拓展该知识点的应用场景与模型构建。
- [[策略回测前视偏差与生存者偏差防范审计 (Look-Ahead & Survivorship Bias Audit)|策略回测前视偏差与生存者偏差审计]]：进一步延伸拓展该知识点的应用场景与模型构建。

横向关联

- [[收益率与对数收益率]]：衡量资产收益特性的基础量纲。
- [[实盘风控]]：风险控制与投资组合保护。

应用场景

- [[实盘风控]]：工业级量化策略风控与组合风险度量。


## 10. 闭卷复现任务

1. [ ] 默写 Sloan 应计项的直觉定义与公式 $\text{Accruals} = \text{Net Income} - \text{CFO}$。
2. [ ] 用“奶茶店记账白条与收银机现金”解释应计项的直觉。
3. [ ] 默写 Beneish M-Score 报警临界点（$-1.78$）。
4. [ ] 列出 M-Score 8 个子比率中最重要的 3 个（TATA, DSRI, AQI）。
5. [ ] 区分 M-Score（防造假）与 Altman Z-Score（防破产）的侧重点。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | M-Score 触发报警阀值 |
| 2 | 公式运用 | 基础 | 净利润 5 亿，CFO 1 亿，求 Sloan 应计项 |
| 3 | 条件判断 | 中等 | M-Score 在金融银行股上的适用性 |
| 4 | 变式/综合 | 中等 | DSRI 指数异常飙高背后的会计含义 |
| 5 | 开放/建模 | 较难 | 利用应计项异象（Accrual Anomaly）设计多空对冲 Alpha 策略 |

---

### 第 1 题：概念辨析（基础）
**题目**：计算出某非金融上市公司的 Beneish M-Score 为 $-1.25$。根据模型规则，该公司的财报状态如何？

> [!question]- 答案解析
> **答案**：因为 $-1.25 > -1.78$（高于临界警戒线），模型发出财务操纵/造假高风险预警。  
> **Obsidian 标签**：`#自测题/BeneishMScore`

---

### 第 2 题：公式运用（基础）
**题目**：某公司净利润 4.0 亿元，经营现金流 CFO 为 $-1.0$ 亿元，总资产 20.0 亿元。求 Sloan 应计项率。

> [!question]- 答案解析
> **答案**：
> $\text{Accruals} = \text{Net Income} - \text{CFO} = 4.0 - (-1.0) = 5.0 \text{ 亿元}$。
> $\text{Sloan\_Ratio} = \frac{5.0}{20.0} = 25\%$。（极度危险的高应计项）。  
> **Obsidian 标签**：`#自测题/Sloan计算`

---

### 第 3 题：条件判断（中等）
**题目**：判断：“因为 Beneish M-Score 表现优异，我们可以直接将其套用到招商银行的财报上进行造假扫描。”

> [!question]- 答案解析
> **答案**：错误。银行与保险等金融机构的业务本身就是经营货币与信用，其资产负债表充满应收/应付款与高杠杆，直接套用非金融业的 M-Score 公式会导致 100% 误报。  
> **Obsidian 标签**：`#自测题/MScore适用边界`

---

### 第 4 题：变式/综合（中等）
**题目**：如果一家公司的 AQI（资产质量指数）从 1.0 突然飙升到 2.5，这暗示了管理层可能在实施什么财务手法？

> [!question]- 答案解析
> **答案**：
> 资产质量指数 $\text{AQI} = \frac{1 - (\text{现金}+\text{固定资产})/\text{总资产}_{t}}{1 - (\text{现金}+\text{固定资产})/\text{总资产}_{t-1}}$。
> AQI 飙升暗示公司把本应记入当期损益的费用/成本（如研发开支、广告费、咨询费），通过错误手段**资本化塞进了无形资产、商誉或其他流动/非流动资产中**，以虚增当期利润。  
> **Obsidian 标签**：`#自测题/AQI分析`

---

### 第 5 题：开放/建模（较难）
**题目**：Sloan (1996) 提出了著名的“应计项异象 (Accrual Anomaly)”：即高应计项股票未来收益率显著低于低应计项股票。为什么市场投资者长期无法消除这一异象？

> [!question]- 答案解析
> **解析**：
> 1. **功能性文盲假设 (Functional Fixation)**：大部分普通投资者和传统分析师过于关注净利润这个单一指标，无法区分利润中“现金分量”与“应计分量”的持久性差异（现金流比应计项更持久）。
> 2. **做空套利限制 (Short-Sale Constraints)**：高应计项股票往往是小盘暴雷股，在实盘中存在融券困难、做空成本高昂与借券中断风险，导致套利力量无法完全抹平该异象。  
> **Obsidian 标签**：`#自测题/应计项异象`

---

## 12. 我的主动回忆区

## 我的闭卷复述

> 不看上文，用自己的话解释这个知识点：

## 我的推导复现

> 不看上文，尝试写出核心公式或推导主线：

## 我的错误与卡点

- 

## 下次复习日期

- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/03-量化金融/01-夯实基础/`
- **建议双链**：[[三大报表关系]]、[[ROE拆解与杜邦分析]]、[[质量因子]]、[[价值因子]]
- **标签**：`#学习` `#量化金融` `#财报分析` `#BeneishMScore` `#Sloan应计项` `#财务造假` `#排雷`

---

<!-- quant-evidence-v3 -->
## 可定位依据与失效复核

本卡的复核对象是 **BeneishMScore与Sloan应计项因子**，而不是只复述一个公式。对 **BeneishMScore与Sloan应计项因子** 的独立验证重点是：逐项追溯 M-Score 输入到原始报表，防止会计口径、重述和行业差异制造误报。

### 权威来源与定位

1. U.S. SEC, *Beginner's Guide to Financial Statements*：https://www.sec.gov/about/reports-publications/beginners-guide-financial-statements。用于复核“逐项追溯 M-Score 输入到原始报表，防止会计口径、重述和行业差异制造误报”。
2. Beneish (1999), *The Detection of Earnings Manipulation*, DOI: 10.1111/0022-1082.00102。用于复核“逐项追溯 M-Score 输入到原始报表，防止会计口径、重述和行业差异制造误报”。
3. Sloan (1996), *Do Stock Prices Fully Reflect Information in Accruals and Cash Flows?*, *The Accounting Review*, DOI: 10.2307/2491392。用于复核“逐项追溯 M-Score 输入到原始报表，防止会计口径、重述和行业差异制造误报”。

### 失效边界与验收协议

- **成立条件**：先写清数据时点、估计窗口、交易摩擦和分布/市场结构假设，再运行模型。
- **反例压力测试**：逐项追溯 M-Score 输入到原始报表，防止会计口径、重述和行业差异制造误报。
- **最小实验**：固定随机种子或冻结原始数据快照，同时保存基线、破坏条件后的对照组、关键中间量与失败日志。
- **通过标准**：结论必须在样本外仍保持方向一致；若成本、延迟、参数扰动或结构突变使结论反转，就把该情形登记为适用边界而不是删除失败结果。
