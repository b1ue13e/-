---
title: 非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)
type: concept
topic: "非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)"
created: 2026-07-23
status: ongoing
difficulty: intermediate
course: 量化金融
importance: A
tags: 
concept: []
prerequisites: []
related: []
upstream: 
downstream: 
---
# 非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)

---

## 0. 先判断它值不值得深挖

**分类：A 类（核心概念，必须深挖）**

**理由：**
非对称 GARCH 模型（由 Nelson 1991 提出的指数 GARCH - EGARCH 与 Glosten, Jagannathan and Runkle 1993 提出的 GJR-GARCH 为代表）是解决传统对称 GARCH(1,1) 模型最大缺陷的计量武器。在真实股票与加密货币市场中，存在极强的**杠杆效应（Leverage Effect）**——即利空/坏消息（负收益冲击 $\varepsilon_{t-1} < 0$）引发的波动率飙升，远大于相同同等幅度的利好/好消息（正收益冲击 $\varepsilon_{t-1} > 0$）。若忽视非对称性，风控系统会在市场暴跌时严重低估下一期的真实 VaR 风险！

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**

假设你正在使用标准对称 GARCH(1,1) 模型估算某指数的波动率：
$$\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$
昨天股市发生了大震荡，涨跌幅绝对值都是 3%：
- 情况 A：股市暴涨了 3%（$+3\%$），方程算出的明天波动率预测是 $\sigma_t^2$；
- 情况 B：股市暴跌了 3%（$-3\%$），由于 $(-3\%)^2 = (+3\%)^2 = 9\%^2$，标准 GARCH 模型给出的明天波动率预测**完全一模一样**！
但在真实市场中，大跌 3% 引发的市场恐慌和抛售会让明天的波动率飙升到 35%，而大涨 3% 后的波动率只有 22%。**标准 GARCH 在大跌时严重漏报了风险。**

**以前的方法在哪里卡住：**
残差是以平方项 $\varepsilon_{t-1}^2$ 形式进入条件方差方程的，强行将负冲击与正冲击等同看待。

**为什么必须引入非对称 GARCH (EGARCH / GJR-GARCH)：**
在条件方差方程中引入**方向指示函数 (Indicator Function $I(\varepsilon_{t-1} < 0)$)** 或 **对数杠杆响应项**，给予负冲击额外的非对称惩罚权重 $\gamma$。

**它到底解决了哪类问题：**
解决了**准确捕捉股市坏消息引发的非对称波动率剧增、消除参数非负性约束限制**的问题。

---

## 2. 为什么它重要？它有什么用？

- **体系与大图景**：时间序列与波动率建模（第二阶段）的硬核模型，连接 GARCH 模型与高阶风险度量（GARCH-VaR / 动态风险头寸）。
- **量化与实战应用**：
  1. **股市崩盘前夕的风控预警**：在暴跌发生后，EGARCH 能够瞬间抬高后续数日的波动率预测，触发做市商关停挂单。
  2. **波动率期权 (VIX Options) 定价**：准确拟合标的价格下跌时 VIX 暴涨的死穴。

---

## 3. 学它之前需要哪些前置知识？

1. **[[02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/GARCH模型]]**：熟练掌握标准 GARCH(1,1) 方程。
2. **[[非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)|收益率序列的风格化事实]]**：理解波动率聚集（Volatility Clustering）与非对称杠杆效应（Leverage Effect）。

---

## 4. 用直觉语言解释它

### 生活类比：踩脚与送礼的不对称情绪反应

- 假设你和朋友相处（市场波动）：
  - 如果你给朋友送了一份 100 元的礼品（好消息 $+100$），朋友的心情波动提升了 10 分。
  - 如果你踩了朋友脚一脚并让他损失了 100 元（坏消息 $-100$），朋友会暴怒跳脚，心情愤怒波动直接飙升了 50 分！
- **标准 GARCH** 就像：一个情商极低的机器人，认为“送 100 元”和“踩一脚”带来的情绪波动完全一样。
- **GJR-GARCH / EGARCH** 就像：一个精明的情商高手，专门给“踩一脚（坏消息）”加上了 5 倍的额外情绪放大系数（非对称杠杆项）。

**非对称 GARCH 的直觉本质**：
认清人类对亏损的恐惧远大于对盈利的喜悦，在价格下跌时给予波动率额外的负面加倍系数。

«“非对称 GARCH 就是给坏消息加装了‘放大镜’，让暴跌引发的波动率飙升远大于大涨带来的波动。”»

---

## 5. 正式定义、核心公式、符号解释

### 核心定义
1. **GJR-GARCH(1,1) 模型**：在标准 GARCH 条件方差方程中加入指示变量 $I_{t-1} = \mathbb{I}(\varepsilon_{t-1} < 0)$，使得负残差获得额外的杠杆系数 $\gamma$。
2. **EGARCH(1,1) 模型 (Exponential GARCH)**：对条件方差取自然对数 $\ln(\sigma_t^2)$ 进行建模，同时包含残差大小与残差符号的标准化项。

### 核心公式

#### 1. GJR-GARCH(1,1) 条件方差方程
$$\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \gamma \varepsilon_{t-1}^2 I_{t-1} + \beta \sigma_{t-1}^2$$
其中：
$$I_{t-1} = \begin{cases} 1, & \text{若 } \varepsilon_{t-1} < 0 \quad (\text{坏消息}) \\ 0, & \text{若 } \varepsilon_{t-1} \ge 0 \quad (\text{好消息}) \end{cases}$$
- 好消息的波动率冲击系数：$\alpha$
- 坏消息的波动率冲击系数：$\alpha + \gamma$（当 $\gamma > 0$ 时，存在非对称杠杆效应！）

#### 2. EGARCH(1,1) 条件对数方差方程 (Nelson 1991)
$$\ln(\sigma_t^2) = \omega + \beta \ln(\sigma_{t-1}^2) + \alpha \left( \left|\frac{\varepsilon_{t-1}}{\sigma_{t-1}}\right| - \sqrt{\frac{2}{\pi}} \right) + \gamma \frac{\varepsilon_{t-1}}{\sigma_{t-1}}$$
- 由于左侧是 $\ln(\sigma_t^2)$，参数 $\omega, \alpha, \beta, \gamma$ **无须任何非负性约束**，取任意实数均能确保导出 $\sigma_t^2 > 0$！
- 当 $\gamma < 0$ 时，负残差使得 $\gamma \frac{\varepsilon_{t-1}}{\sigma_{t-1}} > 0$，代表坏消息会额外拉高对数波动率。

### 符号解释表

| 符号 | 含义 | 维度/量纲 | 备注与要求 |
| :--- | :--- | :--- | :--- |
| $\sigma_t^2$ | $t$ 时刻条件方差 | 收益率平方 $(r^2)$ | 必须为正 |
| $I_{t-1}$ | 坏消息哑变量 (Dummy) | $\{0, 1\}$ | $\varepsilon_{t-1} < 0$ 时置为 1 |
| $\gamma$ | **非对称杠杆效应系数** | 标量 | GJR 中 $\gamma > 0$ 表示坏消息冲击更大；EGARCH 中 $\gamma < 0$ 表示坏消息冲击更大 |
| $\alpha + \beta + \frac{1}{2}\gamma$ | GJR-GARCH 波动率持久度 | 标量 $< 1$ | 必须小于 1 确保平稳性 |

---

## 6. 推导思路和思想来源

### 为什么 EGARCH 要对对数波动率 $\ln(\sigma_t^2)$ 建模？
1. **困境**：在标准 GARCH 中，必须硬性限制 $\omega > 0, \alpha \ge 0, \beta \ge 0$。如果估计出的参数为负数，可能会算处极具荒谬的“负波动率 $\sigma_t^2 < 0$”，导致程序崩溃。
2. **转念**：指数函数 $\exp(x)$ 永远大于 0！如果对 $\ln(\sigma_t^2)$ 进行线性方程建模，再取 $\exp(\cdot)$，无论右侧算出的值是多大的负数，最终导出的 $\sigma_t^2 = \exp(\text{右侧}) > 0$ 始终恒正！
3. **结果**：彻底解除了回归参数的符号约束，极大地便利了最大似然估计 (MLE)。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算例题（GJR-GARCH 波动率响应手算）

**题目**：
已知 GJR-GARCH(1,1) 模型参数为：
$\omega = 0.1$, $\alpha = 0.05$, $\gamma = 0.10$, $\beta = 0.80$。上一期波动率 $\sigma_{t-1} = 2.0\%$（$\sigma_{t-1}^2 = 4.0$）。
分析以下两种不同情况下的本期波动率 $\sigma_t^2$：
- **场景 A**：昨天股票大涨，产生正残差 $\varepsilon_{t-1} = +2.0$（好消息）；
- **场景 B**：昨天股票暴跌，产生负残差 $\varepsilon_{t-1} = -2.0$（坏消息）。

**解答过程**：
1. **场景 A (好消息 $\varepsilon_{t-1} = +2.0 > 0$)**：
   哑变量 $I_{t-1} = 0$。
   $$\sigma_t^2 = 0.1 + 0.05 \times (+2.0)^2 + 0.10 \times (2.0)^2 \times 0 + 0.80 \times 4.0$$
   $$\sigma_t^2 = 0.1 + 0.05 \times 4.0 + 0 + 3.2 = 0.1 + 0.2 + 3.2 = 3.50$$
2. **场景 B (坏消息 $\varepsilon_{t-1} = -2.0 < 0$)**：
   哑变量 $I_{t-1} = 1$。
   $$\sigma_t^2 = 0.1 + 0.05 \times (-2.0)^2 + 0.10 \times (-2.0)^2 \times 1 + 0.80 \times 4.0$$
   $$\sigma_t^2 = 0.1 + 0.20 + 0.40 + 3.2 = 3.90$$
3. **结论**：虽然涨跌绝对值均为 2.0，但在坏消息冲击下，本期条件方差高达 3.90（比好消息场景高出 11.4%），成功捕获了杠杆效应！

---

### 例子 2：中等例题（评估 EGARCH 的新闻响应曲线 News Impact Curve）

**题目**：
对比标准 GARCH 与 EGARCH 的新闻响应曲线 (News Impact Curve, NIC)。
解释为什么标准 GARCH 的 NIC 关于 $\varepsilon_{t-1} = 0$ 对称，而 EGARCH 的 NIC 呈现非对称开口。

**解答过程**：
1. **新闻响应曲线 (NIC)**：保持 $\sigma_{t-1}^2$ 不变，画出 $\sigma_t^2$ 随上期残差 $\varepsilon_{t-1}$ 变化的函数图像。
2. **标准 GARCH**：$\sigma_t^2 = C + \alpha \varepsilon_{t-1}^2$ 是以 $\varepsilon_{t-1} = 0$ 为对称轴开口向上的**抛物线**。无论 $\varepsilon_{t-1} = +5$ 还是 $-5$，产生的 $\sigma_t^2$ 完全一致。
3. **EGARCH**：当 $\gamma < 0$ 时，$\varepsilon_{t-1} < 0$ 区域的斜率拉陡，$\varepsilon_{t-1} > 0$ 区域斜率较平缓，图像呈现左高右低的非对称倾斜 V 型。

---

### 例子 3：实际应用（Python 使用 `arch` 库拟合 EGARCH 模型与动态 VaR 预测）

```python
import numpy as np
import pandas as pd
from arch import arch_model

# 模拟 1000 天带有杠杆效应的日收益率数据
np.random.seed(42)
N = 1000
returns = np.zeros(N)
sigma = np.zeros(N)
sigma[0] = 0.015

for t in range(1, N):
    # 模拟杠杆效应：前一天跌了，今天波动率大幅增加
    gamma_effect = 0.0005 if returns[t-1] < 0 else 0.0
    sigma[t] = np.sqrt(0.00001 + 0.05 * returns[t-1]**2 + gamma_effect + 0.85 * sigma[t-1]**2)
    returns[t] = np.random.normal(0, sigma[t])

returns_series = pd.Series(returns * 100) # 转为百分比

# 1. 拟合 EGARCH(1,1) 模型 (o=1, p=1, q=1)
egarch = arch_model(returns_series, vol='EGARCH', p=1, o=1, q=1, dist='Normal')
res = egarch.fit(disp='off')

print("=== EGARCH(1,1) 模型拟合结果 ===")
print(res.summary().tables[1])

# 2. 预测下一日 95% EGARCH-VaR
next_vol = np.sqrt(res.forecast(horizon=1).variance.iloc[-1, 0]) / 100.0
var_95 = 1.645 * next_vol
print(f"\n预测明日波动率: {next_vol*100:.2f}% | 明日 95% EGARCH-VaR: {var_95*100:.2f}%")
```

---

## 7.5 💥 课本挂载与工业级实战模块 (Textbook Mapping & Production Lab)

### 7.5.1 📚 经典课本章节锚定
- **教材挂载 1**：Ruey S. Tsay *《Analysis of Financial Time Series》* 第 3 章 "Conditional Heteroscedastic Models" Section 3.8 "The EGARCH Model" & Section 3.9 "The GJR-GARCH Model"。
  - **课本必读重点**：Nelson(1991) 论文推导、News Impact Curve 定义、MLE 极大似然对数估计。
  - **推荐课后习题**：Tsay Ch 3 Ex 3.5, 3.8（利用 S-P 500 日收益率拟合 EGARCH 并检验 $\gamma < 0$ 显著性）。
- **教材挂载 2**：Philippe Jorion *《Value at Risk》* 第 9 章 "Forecasting Risks and Correlations"。
  - **实战挂载重点**：非对称 GARCH 预测在巴塞尔协议极端 VaR 计提中的应用。

### 7.5.2 ⚙️ 工业级 Python 最小可运行实战脚手架
（见上方 例子 3 完整代码）

### 7.5.3 ⚠️ 实盘落地“踩坑指南”与回测陷阱
1. **商品与外汇市场的“反向杠杆效应”**：
   在股票市场中，坏消息引发高波动（$\gamma < 0$）；但在**商品市场（如原油、农产品）**中，往往是利好暴涨（供应中断）引发极高波动（$\gamma > 0$）。不能机械假设所有市场都具有相同的非对称符号。
2. **对数转换的极小值数值爆裂**：
   EGARCH 计算 $\ln(\sigma_t^2)$ 时，若某一期残差极小靠近零，$\frac{\varepsilon_{t-1}}{\sigma_{t-1}}$ 的标准化项可能导致数值微小的溢出。必须限制对数上限与下限。

### 7.5.4 📊 实战性能评估指标体系
- **杠杆系数显著性 $t$-值**：测试 $\gamma$ 是否显著非零 ($|t| > 2.0$)。
- **似然比检验 (Likelihood Ratio Test - LR Test)**：比较 GJR-GARCH 相比标准 GARCH 的对数似然提升度。
- **Kupiec 检验 (VaR Backtesting)**：评估基于 EGARCH 的 VaR 穿透率是否精确等于 5%。

### 7.5.5
> 🔓 **作业解锁前置条件**：学完 [[02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/GARCH模型]] + [[非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)|非对称GARCH模型]] 即可正式解锁本 Challenge 实战！
> 💡 **解锁指引**：掌握标准 GARCH 模型后，进一步解锁股市坏消息引发的非对称杠杆效应拟合。

 🧪 拓展实验与李宏毅式实战 Challenge 题 (HW07-EGARCH & GJR-GARCH 杠杆效应与新闻响应曲线)

本作业参考 **李宏毅 (Hung-yi Lee) 教授 ML 课程作业架构** 设计，设置四个渐进式难度基线 (Baselines)：

- 🟢 **简单基线 (Simple Baseline)**：
  - **任务要求**：手算 GJR-GARCH 在好消息（正残差）与坏消息（负残差）下的不同条件方差 $\sigma_t^2$。
  - **达标标准**：代码无 Error 跑通，输出基础结果。

- 🟡 **中等基线 (Medium Baseline)**：
  - **任务要求**：使用 `arch` 库分别拟合 EGARCH(1,1) 与 GJR-GARCH(1,1)，绘制新闻响应曲线 (News Impact Curve, NIC) 验证非对称杠杆效应 $\gamma$。
  - **达标标准**：完成核心算法的向量化与参数校准，模型表现达到基线水平。

- 🔴 **强基线 (Strong Baseline)**：
  - **任务要求**：对比正态分布假设与 Student-t 肥尾分布假设下的 EGARCH 预测效果，估计极端下行 VaR 的准确率。
  - **达标标准**：扣除交易摩擦与滑点后，样本外 (OOS) 夏普比率 $> 1.8$ 或评估指标提升 20% 以上。

- 🟣 **Boss 基线 (Kaggle / 实盘级基线)**：
  - **任务要求**：基于 EGARCH 预测的非对称波动率飙升信号，构建高频做市商“波动率跳空 (Vol-Crash)”自动关停保护系统，防范单日最大撤回。
  - **达标标准**：代码具备极强泛化性与抗过拟合能力，通过 PBO 审计且过拟合概率 $\text{PBO} < 10\%$。


## 8. 常见误区和易混概念

### 误区 1：在所有金融市场中，坏消息引发的波动率都一定大于好消息

错误直觉：“所有资产大跌时的波动率都比大涨时高。”  
为什么错：这是股票市场的特征（源于企业财务杠杆率上升）。在天然气、原油或黄金等商品市场，供需短缺引发的**暴涨（好消息/看涨冲击）**往往伴随着更剧烈的波动率飙升。  
正确理解：**非对称参数 $\gamma$ 的符号必须根据具体资产属性通过数据拟合确定！**

### 概念对比：标准 GARCH vs GJR-GARCH vs EGARCH

| 维度 | 标准 GARCH(1,1) | GJR-GARCH(1,1) | EGARCH(1,1) |
| :--- | :--- | :--- | :--- |
| **非对称性** | 否（对称抛物线） | **是（加入哑变量 $I_{t-1}$）** | **是（包含标准化符号项）** |
| **方差表达形式** | $\sigma_t^2$ | $\sigma_t^2$ | **$\ln(\sigma_t^2)$** |
| **参数非负限制** | 严格限制 $\alpha, \beta, \omega \ge 0$ | 严格限制 $\alpha, \beta, \gamma \ge 0$ | **无任何非负限制（自由估计）** |
| **对数似然估计** | 容易陷入边界约束 | 容易陷入边界约束 | **最稳定、无收敛障碍** |

---

## 9. 相关知识点与 Obsidian 双链建议

请帮我建立知识网络。

注意：不要只列链接。每个链接后面必须用一句话说明“为什么要链接”。

上游依赖

- [[02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/GARCH模型]]：提供基础概念与理论推导支撑。
- [[非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)|收益率序列的风格化事实]]：提供基础概念与理论推导支撑。

下游延伸

- [[极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)|尾部风险]]：进一步延伸拓展该知识点的应用场景与模型构建。
- [[历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)|历史模拟VaR]]：进一步延伸拓展该知识点的应用场景与模型构建。

横向关联

- [[收益率与对数收益率]]：衡量资产收益特性的基础量纲。
- [[实盘风控]]：风险控制与投资组合保护。

应用场景

- [[实盘风控]]：工业级量化策略风控与组合风险度量。


## 10. 闭卷复现任务

1. [ ] 默写 GJR-GARCH(1,1) 的条件方差方程并解释哑变量 $I_{t-1}$。
2. [ ] 用“踩脚与送礼的情绪反应”解释非对称 GARCH 的直觉。
3. [ ] 默写 EGARCH(1,1) 的对数方差方程，并说明为什么它不需要参数非负限制。
4. [ ] 解释什么是股票市场的“杠杆效应 (Leverage Effect)”。
5. [ ] 画出标准 GARCH 与 EGARCH 的新闻响应曲线 (NIC) 的形状差异。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 杠杆效应定义 |
| 2 | 公式运用 | 基础 | GJR-GARCH 条件方差手算 |
| 3 | 条件判断 | 中等 | EGARCH 参数允许为负的原理 |
| 4 | 变式/综合 | 中等 | GJR-GARCH 波动率持久度计算 |
| 5 | 开放/建模 | 较难 | 推导 EGARCH(1,1) 的无条件方差期望值 |

---

### 第 1 题：概念辨析（基础）
**题目**：在 GJR-GARCH(1,1) 方程 $\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \gamma \varepsilon_{t-1}^2 I_{t-1} + \beta \sigma_{t-1}^2$ 中，当杠杆系数 $\gamma > 0$ 时，代表什么？

> [!question]- 答案解析
> **答案**：代表存在非对称杠杆效应，即上一期的负残差（坏消息 $\varepsilon_{t-1} < 0$）引发的当期波动率增加量为 $(\alpha + \gamma) \varepsilon_{t-1}^2$，大于同等幅度正残差的 $\alpha \varepsilon_{t-1}^2$。  
> **Obsidian 标签**：`#自测题/GJRGARCH`

---

### 第 2 题：公式运用（基础）
**题目**：$\omega = 0.05, \alpha = 0.04, \gamma = 0.08, \beta = 0.85$。若 $\sigma_{t-1}^2 = 2.0$，上一期残差 $\varepsilon_{t-1} = -1.0$。求 $\sigma_t^2$。

> [!question]- 答案解析
> **答案**：
> 因为 $\varepsilon_{t-1} = -1.0 < 0$，故 $I_{t-1} = 1$。
> $\sigma_t^2 = 0.05 + 0.04 \times (-1.0)^2 + 0.08 \times (-1.0)^2 \times 1 + 0.85 \times 2.0$
> $\sigma_t^2 = 0.05 + 0.04 + 0.08 + 1.70 = 1.87$。  
> **Obsidian 标签**：`#自测题/GJR计算`

---

### 第 3 题：条件判断（中等）
**题目**：判断：“在估计 EGARCH(1,1) 模型时，如果优化算法求得 $\omega = -0.5$，这代表模型错误，因为方差参数不能为负。”

> [!question]- 答案解析
> **答案**：错误。EGARCH 建模的对象是自然对数 $\ln(\sigma_t^2)$，其常数项 $\omega$ 可以取任意负实数，通过指数映射后 $\sigma_t^2 = \exp(\dots)$ 依然恒为正数。  
> **Obsidian 标签**：`#自测题/EGARCH参数`

---

### 第 4 题：变式/综合（中等）
**题目**：在 GJR-GARCH(1,1) 中，假设正负残差发生的概率各为 50%。该模型的波动率平稳持久度 (Persistence) 如何计算？

> [!question]- 答案解析
> **答案**：
> 由于 $E[I_{t-1}] = 0.5$，条件方差对上一期滞后项的期望响应系数为 $\alpha + \frac{1}{2}\gamma + \beta$。
> 因此，GJR-GARCH 的持久度为：**$\text{Persistence} = \alpha + \frac{1}{2}\gamma + \beta$**。必须满足 $\alpha + \frac{1}{2}\gamma + \beta < 1$ 模型才平稳。  
> **Obsidian 标签**：`#自测题/GJR持久度`

---

### 第 5 题：开放/建模（较难）
**题目**：如何结合 EGARCH 模型的非对称波动率预测 $\hat{\sigma}_{t+1}$，改进配对交易（Pairs Trading）的动态 Z-Score 触发行权阈值？

> [!question]- 答案解析
> **解析**：
> 1. **静态阈值弊端**：传统配对交易使用固定 $Z = \pm 2.0$ 止损。但是在高波动（市场大跌）时，价差本身就会自然拉宽，固定阈值会导致频繁误触发。
> 2. **EGARCH 动态调增**：利用 EGARCH 预测下一期价差的非对称条件标准差 $\hat{\sigma}_{t+1}$，将开仓门槛动态调整为 $\text{Threshold}_{t+1} = \text{Mean} \pm K \cdot \hat{\sigma}_{t+1}$。
> 3. **效果**：在下跌暴跌时自动放宽开仓门槛防踩坑，在平稳期收紧门槛抓小获利，显著提升策略夏普比率。  
> **Obsidian 标签**：`#自测题/EGARCH动态配对`

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

- **适合文件夹**：`02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/`
- **建议双链**：[[02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/GARCH模型]]、[[非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)|收益率序列的风格化事实]]、[[历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)|历史模拟VaR]]
- **标签**：`#学习` `#量化金融` `#时间序列` `#GARCH` `#EGARCH` `#GJRGARCH` `#杠杆效应` `#非对

---

<!-- quant-evidence-v3 -->
## 可定位依据与失效复核

本卡的复核对象是 **非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)**，而不是只复述一个公式。对 **非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)** 的独立验证重点是：比较正负冲击的新闻冲击曲线，并检验标准化残差是否仍有 ARCH 效应。

### 权威来源与定位

1. Bollerslev (1986), *Generalized Autoregressive Conditional Heteroskedasticity*, DOI: 10.1016/0304-4076(86)90063-1。用于复核“比较正负冲击的新闻冲击曲线，并检验标准化残差是否仍有 ARCH 效应”。
2. Nelson (1991), *Conditional Heteroskedasticity in Asset Returns: A New Approach*, DOI: 10.2307/2938260。用于复核“比较正负冲击的新闻冲击曲线，并检验标准化残差是否仍有 ARCH 效应”。
3. Kevin Sheppard 的 `arch` 官方波动率建模文档：https://arch.readthedocs.io/en/latest/univariate/univariate_volatility_modeling.html；参见 Chapter 1 示例。用于复核“比较正负冲击的新闻冲击曲线，并检验标准化残差是否仍有 ARCH 效应”。

### 失效边界与验收协议

- **成立条件**：先写清数据时点、估计窗口、交易摩擦和分布/市场结构假设，再运行模型。
- **反例压力测试**：比较正负冲击的新闻冲击曲线，并检验标准化残差是否仍有 ARCH 效应。
- **最小实验**：固定随机种子或冻结原始数据快照，同时保存基线、破坏条件后的对照组、关键中间量与失败日志。
- **通过标准**：结论必须在样本外仍保持方向一致；若成本、延迟、参数扰动或结构突变使结论反转，就把该情形登记为适用边界而不是删除失败结果。
