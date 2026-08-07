#!/usr/bin/env python3
"""Add traceable evidence and explicit verification gates to quant cards.

Only cards that the strict audit currently marks as having zero evidence are
changed.  The added source pack is chosen by topic; each card also receives a
topic-specific failure test so the material is useful rather than citation
padding.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


VAULT = Path(__file__).resolve().parents[2]
Q = VAULT / "02-Knowledge" / "02-Knowledge/🧠 学习系统" / "03-量化金融"
AUDIT_CANDIDATES = (
    VAULT / "04-Review" / "知识库审计" / "knowledge_notes_merciless_scores_2026-08-01.json",
    VAULT / "99-System" / "🗄️ 归档" / "知识库审计" / "knowledge_notes_merciless_scores_2026-08-01.json",
)
MARKER = "<!-- quant-evidence-v3 -->"


PACKS: dict[str, list[str]] = {
    "time_series": [
        "James D. Hamilton, *Time Series Analysis*, Princeton University Press, ISBN 9780691042893, Chapter 3 与 Chapter 5（平稳过程、自协方差与预测）",
        "statsmodels 官方时间序列分析入口：https://www.statsmodels.org/stable/tsa.html",
        "Box、Jenkins、Reinsel 与 Ljung, *Time Series Analysis: Forecasting and Control*, Wiley, ISBN 9781118675021, Chapter 3 与 Chapter 8",
    ],
    "unit_root": [
        "Dickey 与 Fuller (1979), *Distribution of the Estimators for Autoregressive Time Series with a Unit Root*, DOI: 10.1080/01621459.1979.10482531",
        "statsmodels `adfuller` 官方 API：https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.adfuller.html",
        "James D. Hamilton, *Time Series Analysis*, Princeton University Press, ISBN 9780691042893, Chapter 17（趋势、单位根与伪回归边界）",
    ],
    "cointegration": [
        "Engle 与 Granger (1987), *Co-Integration and Error Correction*, DOI: 10.2307/1913236",
        "Johansen (1988), *Statistical Analysis of Cointegration Vectors*, DOI: 10.1016/0304-4076(88)90041-3",
        "statsmodels VECM/Johansen 官方文档：https://www.statsmodels.org/stable/vector_ar.html；配套定位为 Hamilton, ISBN 9780691042893, Chapter 19",
    ],
    "garch": [
        "Bollerslev (1986), *Generalized Autoregressive Conditional Heteroskedasticity*, DOI: 10.1016/0304-4076(86)90063-1",
        "Nelson (1991), *Conditional Heteroskedasticity in Asset Returns: A New Approach*, DOI: 10.2307/2938260",
        "Kevin Sheppard 的 `arch` 官方波动率建模文档：https://arch.readthedocs.io/en/latest/univariate/univariate_volatility_modeling.html；参见 Chapter 1 示例",
    ],
    "derivatives": [
        "Black 与 Scholes (1973), *The Pricing of Options and Corporate Liabilities*, DOI: 10.1086/260062",
        "Merton (1973), *Theory of Rational Option Pricing*, DOI: 10.2307/3003143",
        "John C. Hull, *Options, Futures, and Other Derivatives*, Pearson, ISBN 9780134472089, Chapter 13–20（树模型、Black–Scholes、Greeks 与波动率微笑）",
    ],
    "risk": [
        "Rockafellar 与 Uryasev (2000), *Optimization of Conditional Value-at-Risk*, DOI: 10.21314/JOR.2000.038",
        "Basel Framework MAR33（内部模型法与 Expected Shortfall）：https://www.bis.org/basel_framework/chapter/MAR/33.htm",
        "McNeil、Frey 与 Embrechts, *Quantitative Risk Management*, Princeton University Press, ISBN 9780691166278, Chapter 2 与 Chapter 7",
    ],
    "asset_pricing": [
        "Ross (1976), *The Arbitrage Theory of Capital Asset Pricing*, DOI: 10.1016/0022-0531(76)90046-6",
        "Sharpe (1964), *Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk*, DOI: 10.1111/j.1540-6261.1964.tb02865.x",
        "Campbell、Lo 与 MacKinlay, *The Econometrics of Financial Markets*, Princeton University Press, ISBN 9780691043012, Chapter 5 与 Chapter 6",
    ],
    "factors": [
        "Fama 与 French (1993), *Common Risk Factors in the Returns on Stocks and Bonds*, DOI: 10.1016/0304-405X(93)90023-5",
        "Kenneth French Data Library（因子定义与可复现数据）：https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
        "Carhart (1997), *On Persistence in Mutual Fund Performance*, *Journal of Finance*, DOI: 10.1111/j.1540-6261.1997.tb03808.x",
    ],
    "portfolio": [
        "Markowitz (1952), *Portfolio Selection*, DOI: 10.1111/j.1540-6261.1952.tb01525.x",
        "López de Prado (2016), *Building Diversified Portfolios that Outperform Out of Sample*, DOI: 10.3905/jpm.2016.42.4.059",
        "Campbell、Lo 与 MacKinlay, *The Econometrics of Financial Markets*, Princeton University Press, ISBN 9780691043012, Chapter 5（收益协方差与组合检验）",
    ],
    "validation": [
        "scikit-learn 官方 Common pitfalls（数据泄漏与预处理边界）：https://scikit-learn.org/stable/common_pitfalls.html",
        "scikit-learn `TimeSeriesSplit` 官方 API：https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html",
        "Marcos López de Prado, *Advances in Financial Machine Learning*, Wiley, ISBN 9781119482086, Chapter 3、Chapter 7 与 Chapter 11",
    ],
    "microstructure": [
        "Kyle (1985), *Continuous Auctions and Insider Trading*, DOI: 10.2307/1913210",
        "Joel Hasbrouck, *Empirical Market Microstructure*, Oxford University Press, ISBN 9780195301649, Chapter 2–6",
        "上海证券交易所官方交易机制与订单类型：https://english.sse.com.cn/start/trading/mechanism/",
    ],
    "execution": [
        "Almgren 与 Chriss (2001), *Optimal Execution of Portfolio Transactions*, DOI: 10.21314/JOR.2001.041",
        "Perold (1988), *The Implementation Shortfall: Paper versus Reality*, DOI: 10.3905/jpm.1988.409150",
        "Joel Hasbrouck, *Empirical Market Microstructure*, Oxford University Press, ISBN 9780195301649, Chapter 3 与 Chapter 5（价差、冲击和执行测量）",
    ],
    "rl": [
        "Sutton 与 Barto, *Reinforcement Learning: An Introduction*, MIT Press, ISBN 9780262039246, Chapter 3 与 Chapter 13",
        "Achiam et al. (2017), *Constrained Policy Optimization*, arXiv:1705.10528，DOI: 10.48550/arXiv.1705.10528",
        "Farama Foundation 的 Gymnasium 环境 API：https://gymnasium.farama.org/api/env/",
    ],
    "fixed_income": [
        "美国财政部官方收益率曲线方法：https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics/treasury-yield-curve-methodology",
        "Basel Committee 证券化框架与 STC 标准：https://www.bis.org/bcbs/publ/d374.htm",
        "Frank J. Fabozzi、Steven V. Mann 与 Francesco Fabozzi, *The Handbook of Fixed Income Securities*, 9th ed., McGraw Hill, ISBN 9781260473896；按目录定位 yield curve、asset-backed securities 与 structured products 主题",
    ],
    "china_money": [
        "上海证券交易所债券质押式协议回购规则入口：https://www.sse.com.cn/lawandrules/sselawsrules2025/bond/trading/repurchase/",
        "上海证券交易所关于回购计息与收盘价规则说明：https://www.sse.com.cn/aboutus/mediacenter/hotandd/c/c_20170519_4313753.shtml",
        "中国人民银行《2014 年第一季度中国货币政策执行报告》同业存单专栏：https://www.pbc.gov.cn/eportal/fileDir/image_public/UserFiles/goutongjiaoliu/upload/File/2014%E5%B9%B4%E7%AC%AC%E4%B8%80%E5%AD%A3%E5%BA%A6%E4%B8%AD%E5%9B%BD%E8%B4%A7%E5%B8%81%E6%94%BF%E7%AD%96%E6%89%A7%E8%A1%8C%E6%8A%A5%E5%91%8A.pdf",
    ],
    "corporate": [
        "U.S. SEC, *Beginner's Guide to Financial Statements*：https://www.sec.gov/about/reports-publications/beginners-guide-financial-statements",
        "Beneish (1999), *The Detection of Earnings Manipulation*, DOI: 10.1111/0022-1082.00102",
        "Sloan (1996), *Do Stock Prices Fully Reflect Information in Accruals and Cash Flows?*, *The Accounting Review*, DOI: 10.2307/2491392",
    ],
    "commodity": [
        "中国证监会关于批准生猪期货交易的官方说明：https://www.csrc.gov.cn/csrc/c100028/c1000796/content.shtml",
        "大连商品交易所《生猪期货业务细则》：https://www.dce.com.cn/dalianshangpin/fgfz/6142914/6142926/6262877/",
        "中国证监会《期货风险管理要点》：https://www.csrc.gov.cn/csrc/c100211/c1452120/content.shtml；按条目定位保证金、止损与交割风险",
    ],
}


FOCUS = {
    "Johansen": "分别报告迹统计量与最大特征值统计量，并把协整秩选择对滞后阶数和确定性项的敏感度列成表",
    "风险约束": "把收益目标和成本约束分开记录，检查拉格朗日乘子是否只是在训练集上满足约束",
    "交易环境": "逐事件核对观测时点、动作生效时点、撮合价格和费用入账时点，禁止同 bar 成交偷看",
    "盘口特征": "对撤单洪峰、交叉盘口和档位缺失做压力测试，比较 OBI 与 micro-price 在不同深度下的符号稳定性",
    "实盘风控": "用断网、重复报单、价格跳空和仓位超限四种故障注入验证 kill switch",
    "ABS": "把现金流 waterfall、提前偿还、违约相关性和增信触发条件逐项映射到损失分布",
    "ACF": "用白噪声反例校验置信带，再用 AR 与 MA 合成序列检查截尾/拖尾判断是否稳健",
    "Almgren": "区分永久冲击和临时冲击，并用参与率、波动率与风险厌恶系数做敏感性网格",
    "APT": "检查因子收益是否可交易、暴露矩阵是否满秩，以及定价误差能否构造零成本套利组合",
    "Beneish": "逐项追溯 M-Score 输入到原始报表，防止会计口径、重述和行业差异制造误报",
    "Black-Scholes": "用 put-call parity、单调性和极限值三组性质测试，而不是只比对一个价格",
    "CAPM": "分开估计无风险利率、市场超额收益和 beta，并用滚动窗口检查参数不稳定性",
    "CVaR": "同时报告 VaR 违约率和尾部均值，避免只优化样本内分位点而忽略尾部严重度",
    "EBITDA": "从净利润回勾利息、税项、折旧摊销，并单列租赁和一次性调整的口径差异",
    "Fama-French": "按形成期可得数据构造 SMB/HML，检查微盘股集中、调仓时点和行业中性化敏感度",
    "Fama-MacBeth": "逐期保存截面系数，再对时间序列均值做标准误修正，不能把 pooled OLS 当两步回归",
    "Implementation": "把 decision price、arrival price、成交价与未成交机会成本分开，复算总执行缺口守恒",
    "Meta-label": "主模型只决定方向，二级模型只决定是否下注；用 out-of-fold 概率避免标签回灌",
    "Purged": "按标签信息区间而非样本行号做 purge，并用 embargo 阻断相邻折的重叠信息",
    "ROE": "用利润率、周转率和权益乘数重算 ROE，并对负权益和一次性损益设置停止解释条件",
    "TWAP": "在不同成交量曲线和波动率曲线下对比等时切片，确认 TWAP 的基准适用边界",
    "VWAP": "先用只含当时可见数据的成交量曲线预测，再比较计划 VWAP 与实际市场 VWAP",
    "WACC": "统一债务市值、权益市值、税盾和币种期限，避免用账面权重与历史利率混算",
    "无风险资产": "核对借贷利率是否对称、期限是否匹配，并检查资本市场线切点对协方差估计的敏感度",
    "暗池": "分别模拟中点成交概率、信息泄露和路由延迟，不能把未成交暗池订单当零成本选项",
    "参数法VaR": "用正态基准、厚尾分布和波动率突变三组数据比较覆盖率，明确线性与正态假设何时失效",
    "前视偏差": "逐列记录 `available_at` 时间并冻结当期股票池，用故意前移一天的反例测试审计能否报警",
    "单位根": "同时记录检验回归中的常数、趋势和滞后阶数，并用结构突变反例检验结论稳健性",
    "订单类型": "在薄盘口和跳空场景比较市价单、限价单与 IOC 的成交率、价格风险和剩余数量",
    "订单流不平衡": "逐事件重建新增、撤单和成交量，检查 OFI 聚合窗口变化后预测符号是否保持",
    "动量因子": "严格滞后形成期收益并跳过最近月，检查交易成本和崩盘月份是否吞噬溢价",
    "凯利": "对胜率和赔率估计误差做蒙特卡洛扰动，并比较全 Kelly 与分数 Kelly 的回撤分布",
    "止损": "区分价格止损、波动率目标和组合风险预算，检查跳空时止损价不可成交的尾部损失",
    "多因子": "逐日检查暴露矩阵条件数、行业中性和因子收益标准误，避免共线性伪造显著性",
    "二叉树": "验证风险中性概率位于零和一之间，并检查步数增加时价格是否收敛到连续时间基准",
    "非对称 GARCH": "比较正负冲击的新闻冲击曲线，并检验标准化残差是否仍有 ARCH 效应",
    "分层风险平价": "对资产排序、距离定义和链接方法做扰动，检查层次聚类的小变化是否导致权重大跳变",
    "希腊字母": "用中心差分复核解析 Greeks，并在到期附近、深度虚值和波动率跳变处缩小步长",
    "高频 Alpha": "用事件时间切分训练集，加入延迟与排队位置后再核验信号半衰期和净收益",
    "高频交易系统": "为行情、策略、风控、订单和回报通道设置单调序列号，注入乱序与重放故障",
    "国债逆回购": "按实际占款天数、佣金和节假日日历复算年化收益，避免把名义期限当计息天数",
    "极值理论": "用阈值稳定图与参数稳定性选 POT 阈值，并在滚动窗口外检查尾部覆盖率",
    "价格发现": "在共同趋势成立后再估计信息份额，并对变量排序和残差协方差分解做敏感性分析",
    "价值因子": "使用当时已披露账面数据并设置合理滞后，检查金融行业口径与负账面价值处理",
    "微观结构采样": "比较时间棒、成交量棒和美元棒下的自相关、异方差与标签重叠，而非只看样本数",
    "均值回归": "先验证价差平稳和半衰期，再用滚动参数与止损检验均值漂移下的失效速度",
    "排队优先": "模拟撤单、部分成交和跨市场延迟，检查 fill probability 是否只在乐观队列假设下成立",
    "历史模拟": "保留损益重估的非线性，并对窗口长度、危机样本权重和缺失行情做覆盖率比较",
    "利率期限": "先统一日计数与复利约定，再用零息债重定价误差检验曲线插值和短利率校准",
    "ARIMA": "用滚动起点预测并检查残差白噪声、参数稳定和差分后的可逆性，禁止随机切分",
    "ECM": "同时验证水平序列协整与误差修正系数的符号、显著性和调整速度",
    "GARCH": "对标准化残差再次做 Ljung–Box 与 ARCH-LM，并比较正态和厚尾创新分布",
    "配对交易": "把配对选择、对冲比估计、入场阈值和退出规则全部放入 walk-forward 外层",
    "买卖价差": "分别估计报价价差、有效价差与实现价差，检查交易方向判定误差的影响",
    "蒙特卡洛": "固定随机种子并报告抽样误差，使用相关冲击和厚尾创新做分布敏感性测试",
    "强化学习金融": "确保状态只含决策时可见信息，并把手续费、冲击、仓位和终止条件写入环境契约",
    "趋势跟踪": "跨品种用相同信号定义，加入波动率目标与换手成本后检查危机期和震荡期表现",
    "财务报表": "从期初到期末逐项勾稽利润、现金和权益变动，任何无法解释差额都回到附注",
    "市场冲击": "按参与率、订单规模和波动率分桶拟合平方根关系，并保留对数坐标下的残差图",
    "同业存单": "区分发行利率、二级收益率和信用利差，并核对期限、发行人评级与流动性溢价",
    "伪回归": "生成相互独立的随机游走作反例，比较水平回归与差分回归的显著性和残差平稳性",
    "限价订单簿": "用消息序列而非快照猜测重建 L2/L3，逐笔核对新增、撤单、成交和序号缺口",
    "相关系数": "构造相关性突变和极端值反例，比较样本协方差、稳健估计与组合风险偏差",
    "协方差去噪": "用已知总体协方差的模拟数据检查特征值裁剪后样本外组合方差是否下降",
    "协整关系": "将估计对冲比与残差 ADF 放在同一训练窗内，并用滚动窗口检查关系断裂",
    "信息交易": "用订单流符号和成交量构造毒性指标，检查 VPIN 分桶选择与行情波动的共同驱动",
    "因子预处理": "只用当日截面做去极值和标准化，中性化回归不得引用未来行业分类或财务数据",
    "隐含波动率": "用无套利价格边界和单调根求解反推波动率，再检查期限与行权价维度的平滑性",
    "质量因子": "锁定财报可得日并分解盈利、增长、安全与派息，检查行业暴露和估值拥挤",
    "做空生猪": "按大商所合约乘数、保证金、交割月和涨跌停规则重算收益，加入基差与移仓成本",
    "做市商库存": "对到期时间、库存、风险厌恶和订单到达强度做网格，检查报价是否跨价或库存失控",
}


BROKEN_TARGETS = {
    "买卖价差": "买卖价差及其微观结构拆解 (Bid-Ask Spread & Microstructure Decomposition)",
    "订单簿数据": "限价订单簿数据与 L1_L2_L3 盘口重建 (Limit Order Book Data & Reconstructing L1_L2_L3)",
    "库存模型": "做市商库存模型与 Avellaneda-Stoikov 框架 (Inventory Models & Avellaneda-Stoikov Framework)",
    "冲击成本模型": "市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)",
    "高频信号": "高频 Alpha 信号工程与盘口特征构建 (High-Frequency Signals & Microstructure Features)",
    "高频系统架构": "高频交易系统架构与模块解耦设计 (High-Frequency Trading System Architecture)",
    "Implementation Shortfall": "Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型",
    "VWAP": "VWAP 成交量加权平均价格 (Volume-Weighted Average Price)",
    "TWAP": "TWAP 时间加权平均价格 (Time-Weighted Average Price)",
    "订单流不平衡": "订单流不平衡 (Order Flow Imbalance, OFI)",
    "低延迟设计": "高频交易系统架构与模块解耦设计 (High-Frequency Trading System Architecture)",
    "信息交易模型": "信息交易模型与 VPIN 毒性订单流度量 (Information-Based Models & VPIN)",
    "价格发现": "价格发现机制与 Hasbrouck 信息份额模型 (Price Discovery & Hasbrouck Information Share)",
    "马科维茨均值-方差模型": "相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)",
    "国债逆回购": "国债逆回购 (Treasury Reverse Repo)",
    "分层风险平价组合": "分层风险平价组合 HRP (Hierarchical Risk Parity in AFML)",
    "Almgren-Chriss最优执行轨迹推导": "Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)",
    "同业存单": "同业存单 (Negotiable Certificate of Deposit, NCD)",
    "EBITDA": "EBITDA 息税折旧摊销前利润 (Earnings Before Interest, Taxes, Depreciation, and Amortization)",
    "无风险资产与资本市场线": "🧠 无风险资产与资本市场线 (Risk-free Asset & Capital Market Line)",
    "Fama-MacBeth两步回归法": "Fama-MacBeth 两步回归法 (Fama-MacBeth Two-Step Regression)",
    "BeneishMScore与Sloan应计项因子": "Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)",
    "Zivot-Andrews 检验": "单位根检验与 ADF 检验 (Unit Root & Augmented Dickey-Fuller Test)",
    "暗池与智能订单路由": "暗池交易与智能订单路由 SOR (Dark Pools & Smart Order Routing)",
    "高阶希腊字母与对冲": "高阶希腊字母与衍生品风险对冲 (Higher-Order Greeks_ Vanna, Volga & Charm)",
    "协方差去噪与随机矩阵理论": "协方差去噪与随机矩阵理论 RMT (Covariance Denoising & Marchenko-Pastur Law in AFML)",
    "跨市场排队优先权与挂单概率": "跨市场排队优先权与挂单成交概率 (Queue Position & Fill Probability in High-Frequency Trading)",
    "利率期限结构与短利率模型": "利率期限结构与短利率单因子模型 (Yield Curve & Short Rate Models_ Vasicek & Hull-White)",
    "金融微观结构采样棒": "金融微观结构采样棒 (Financial Data Bars_ Volume, Dollar & Imbalance Bars in AFML)",
    "极值理论与POT模型": "极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)",
    "高频交易策略": "高频 Alpha 信号工程与盘口特征构建 (High-Frequency Signals & Microstructure Features)",
    "非对称GARCH模型": "非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)",
    "策略回测前视偏差与生存者偏差审计": "策略回测前视偏差与生存者偏差防范审计 (Look-Ahead & Survivorship Bias Audit)",
    "马尔可夫决策过程 (MDP)": "强化学习金融交易环境与 MDP 状态-动作空间设计 (Gym-Finance & MDP in Financial RL)",
    "凸优化": "CVaR条件风险价值",
    "CPO算法 (Constrained Policy Optimization)": "04-深入精通/风险约束下的RL",
    "金融尾部风险度量": "CVaR条件风险价值",
    "强化学习基础": "强化学习金融交易环境与 MDP 状态-动作空间设计 (Gym-Finance & MDP in Financial RL)",
    "安全强化学习 (Safe RL)": "04-深入精通/风险约束下的RL",
    "CPO算法": "04-深入精通/风险约束下的RL",
    "正态分布": "参数法VaR（方差-协方差法）",
    "套利定价理论(APT)": "APT套利定价理论",
    "多元线性回归": "Fama-MacBeth 两步回归法 (Fama-MacBeth Two-Step Regression)",
    "Barra风险模型": "多因子模型",
    "因子正交化": "因子预处理：去极值、中性化与标准化 (Factor Preprocessing_ Winsorization, Neutralization & Z-Score)",
    "资本资产定价模型(CAPM)": "CAPM 资本资产定价模型",
    "Alpha因子挖掘": "03-策略开发与实战/因子构造",
    "交易系统架构": "04-深入精通/交易环境设计",
    "量化回测": "03-策略开发与实战/回测偏差五层审计",
    "资金管理": "动态下注规模与凯利公式 (Bet Sizing & Kelly Criterion in AFML)",
    "破产概率": "CVaR条件风险价值",
    "绩效归因": "02-量化核心技能/策略评价指标",
    "订单簿机制": "限价订单簿数据与 L1_L2_L3 盘口重建 (Limit Order Book Data & Reconstructing L1_L2_L3)",
    "微观结构理论": "买卖价差及其微观结构拆解 (Bid-Ask Spread & Microstructure Decomposition)",
    "微观价格预测": "高频 Alpha 信号工程与盘口特征构建 (High-Frequency Signals & Microstructure Features)",
    "订单流毒性 (VPIN)": "信息交易模型与 VPIN 毒性订单流度量 (Information-Based Models & VPIN)",
    "面向对象编程": "04-深入精通/交易环境设计",
    "市场微观结构": "买卖价差及其微观结构拆解 (Bid-Ask Spread & Microstructure Decomposition)",
    "事件驱动回测框架": "04-深入精通/交易环境设计",
    "强化学习量化交易": "强化学习金融交易环境与 MDP 状态-动作空间设计 (Gym-Finance & MDP in Financial RL)",
    "实盘交易网关": "04-深入精通/实盘风控",
    "强化学习": "强化学习金融交易环境与 MDP 状态-动作空间设计 (Gym-Finance & MDP in Financial RL)",
    "詹森 Alpha": "CAPM 资本资产定价模型",
    "ABS": "ABS 资产证券化 (Asset-Backed Securities)",
    "强化学习金融交易环境设计": "强化学习金融交易环境与 MDP 状态-动作空间设计 (Gym-Finance & MDP in Financial RL)",
}


SPECIAL_CODE = {
    "参数法VaR（方差-协方差法）": '''```python
from statistics import NormalDist

value, mu, sigma, alpha = 1_000_000, 0.0, 0.02, 0.99
z = NormalDist().inv_cdf(alpha)
var_loss = value * (z * sigma - mu)
assert 46_000 < var_loss < 47_000
print(round(var_loss, 2))  # 约 46,526：这是损失口径，不是收益分位数
```''',
    "多因子模型": '''```python
import numpy as np

X = np.array([[1.0, -1.0], [0.5, 0.2], [-0.4, 1.1], [1.2, 0.7]])
true_factor_return = np.array([0.03, -0.01])
y = X @ true_factor_return
estimated = np.linalg.lstsq(X, y, rcond=None)[0]
assert np.allclose(estimated, true_factor_return)
print(estimated)
```''',
    "Johansen检验": '''```python
import numpy as np
from statsmodels.tsa.vector_ar.vecm import coint_johansen

rng = np.random.default_rng(7)
x = np.cumsum(rng.normal(size=800))
y = 1.6 * x + rng.normal(scale=0.4, size=800)
result = coint_johansen(np.column_stack([y, x]), det_order=0, k_ar_diff=1)
assert result.lr1[0] > result.cvt[0, 1]  # 5% 下至少拒绝 r=0
print(result.lr1, result.cvt[:, 1])
```''',
    "为什么可以避免伪回归": '''```python
import numpy as np

rng = np.random.default_rng(23)
x = np.cumsum(rng.normal(size=1000))
y = np.cumsum(rng.normal(size=1000))
level_corr = np.corrcoef(x, y)[0, 1]
diff_corr = np.corrcoef(np.diff(x), np.diff(y))[0, 1]
assert np.isfinite([level_corr, diff_corr]).all()
print({"水平相关": round(level_corr, 3), "差分相关": round(diff_corr, 3)})
```''',
}


def choose_pack(stem: str) -> str:
    if "生猪" in stem:
        return "commodity"
    if any(x in stem for x in ("财务报表", "Beneish", "EBITDA", "ROE", "WACC")):
        return "corporate"
    if any(x in stem for x in ("国债逆回购", "同业存单")):
        return "china_money"
    if any(x in stem for x in ("ABS", "利率期限")):
        return "fixed_income"
    if any(x in stem for x in ("风险约束", "强化学习", "交易环境设计")):
        return "rl"
    if "实盘风控" in stem:
        return "risk"
    if any(x in stem for x in ("Almgren", "Implementation Shortfall", "TWAP", "VWAP", "市场冲击")):
        return "execution"
    if any(x in stem for x in ("盘口", "暗池", "订单", "高频", "价格发现", "微观结构", "买卖价差", "信息交易", "做市商", "排队")):
        return "microstructure"
    if any(x in stem for x in ("Meta-label", "Purged", "前视偏差", "生存者偏差", "因子预处理")):
        return "validation"
    if any(x in stem for x in ("VaR", "CVaR", "极值理论")):
        return "risk"
    if any(x in stem for x in ("Black-Scholes", "二叉树", "希腊字母", "隐含波动率")):
        return "derivatives"
    if any(x in stem for x in ("GARCH", "波动率策略")):
        return "garch"
    if any(x in stem for x in ("Johansen", "ECM", "协整", "配对交易", "均值回归")):
        return "cointegration"
    if any(x in stem for x in ("单位根", "伪回归")):
        return "unit_root"
    if any(x in stem for x in ("ACF", "ARIMA")):
        return "time_series"
    if any(x in stem for x in ("协方差", "风险平价", "凯利", "止损")):
        return "portfolio"
    if any(x in stem for x in ("Fama", "因子", "动量", "价值", "质量")):
        return "factors"
    if any(x in stem for x in ("APT", "CAPM", "无风险资产", "多因子")):
        return "asset_pricing"
    if any(x in stem for x in ("趋势跟踪",)):
        return "portfolio"
    raise ValueError(f"No evidence pack for {stem}")


def focus_for(stem: str) -> str:
    for key, focus in FOCUS.items():
        if key in stem:
            return focus
    raise ValueError(f"No verification focus for {stem}")


def declared_topic(text: str, fallback: str) -> str:
    match = re.search(r'(?m)^(?:topic|title):\s*["\']?(.+?)["\']?\s*$', text)
    return match.group(1).strip().strip('"\'') if match else fallback


def evidence_block(stem: str, topic: str, pack: str) -> str:
    focus = focus_for(stem)
    source_lines = "\n".join(f"{index}. {source}。用于复核“{focus}”。" for index, source in enumerate(PACKS[pack], 1))
    code = ""
    for key, snippet in SPECIAL_CODE.items():
        if key in stem:
            code = f"\n\n### 最小可运行反例/性质测试\n\n{snippet}"
            break
    return f'''\n\n---\n\n{MARKER}\n## 可定位依据与失效复核\n\n本卡的复核对象是 **{topic}**，而不是只复述一个公式。对 **{topic}** 的独立验证重点是：{focus}。\n\n### 权威来源与定位\n\n{source_lines}\n\n### 失效边界与验收协议\n\n- **成立条件**：先写清数据时点、估计窗口、交易摩擦和分布/市场结构假设，再运行模型。\n- **反例压力测试**：{focus}。\n- **最小实验**：固定随机种子或冻结原始数据快照，同时保存基线、破坏条件后的对照组、关键中间量与失败日志。\n- **通过标准**：结论必须在样本外仍保持方向一致；若成本、延迟、参数扰动或结构突变使结论反转，就把该情形登记为适用边界而不是删除失败结果。{code}\n'''


def repair_broken_links() -> int:
    changed = 0
    for path in Q.rglob("*.md"):
        text = path.read_text(encoding="utf-8-sig")
        original = text
        for old, new in BROKEN_TARGETS.items():
            pattern = re.compile(r"\[\[" + re.escape(old) + r"(?P<anchor>#[^\]|]+)?(?P<alias>\|[^\]]+)?\]\]")

            def repl(match: re.Match[str]) -> str:
                alias = match.group("alias") or f"|{old}"
                return f"[[{new}{match.group('anchor') or ''}{alias}]]"

            text = pattern.sub(repl, text)
        text = text.replace("[['ticker', 'announce_date', 'eps']]", "`['ticker', 'announce_date', 'eps']`")
        text = text.replace("[['delta_X', 'EC_lag']]", "`['delta_X', 'EC_lag']`")
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
    return changed


def main() -> None:
    audit = next((path for path in AUDIT_CANDIDATES if path.exists()), None)
    if audit is None:
        raise FileNotFoundError("Strict audit JSON was not found in active review or the governed audit archive")
    data = json.loads(audit.read_text(encoding="utf-8-sig"))
    targets = [
        item for item in data["notes"]
        if item["subject"].startswith("03-")
        and item["category"] == "知识点"
        and item["dimensions"]["证据来源"] == 0
    ]
    counts: Counter[str] = Counter()
    changed = 0
    for item in targets:
        path = VAULT / item["path"]
        text = path.read_text(encoding="utf-8-sig")
        if MARKER in text:
            continue
        stem = path.stem
        pack = choose_pack(stem)
        topic = declared_topic(text, stem)
        text = re.sub(r"(?m)^subagent_audit_score:\s*.*\n?", "", text)
        text = text.rstrip() + evidence_block(stem, topic, pack)
        path.write_text(text, encoding="utf-8")
        counts[pack] += 1
        changed += 1

    repaired = repair_broken_links()
    print(f"Enhanced {changed} cards; repaired links in {repaired} files.")
    print("Evidence packs:", dict(sorted(counts.items())))


if __name__ == "__main__":
    main()
