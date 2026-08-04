---
title: Black-Scholes 期权定价模型
date: 2026-07-23
type: concept
course: 量化金融
importance: A
tags:
- 学习
- 量化金融
- 衍生品
- Black-Scholes
- 期权定价
- 随机微积分
- 动态对冲
- 风险中性
upstream:
- '[[远期、期货与期权的区别]]'
- '[[二叉树定价]]'
downstream:
- '[[Greeks]]'
- '[[高阶希腊字母与衍生品风险对冲 (Higher-Order Greeks_ Vanna, Volga & Charm)|高阶希腊字母与对冲]]'
- '[[隐含波动率]]'
status: learning
---
# Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)

---

## 0. 先判断它值不值得深挖

**分类：A 类（核心概念，必须深挖）**

**理由：**
Black-Scholes-Merton (BSM) 模型是金融工程与量化金融史上最伟大的数学突破（获得 1997 年诺贝尔经济学奖）。它首次将随机微积分（伊藤清引理 Itô's Lemma）、热传导偏微分方程（PDE）与无套利连续动态对冲结合，给出了欧式期权的封闭解析解（Closed-form Solution）。它是期权做市、Delta 对冲、希腊字母（Greeks）与隐含波动率曲面（Volatility Smile）的数学根源。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**

在 1973 年之前，金融界对“期权（Option）到底值多少钱”一片茫然。
期权赋予持有者在未来以约定价格买卖股票的权利。股票未来可能暴涨 100%，也可能跌至 0。
传统投资者试图通过预测“股价未来会上涨还是下跌”来给期权定价（即加上主观概率与风险偏好）。

**以前的方法在哪里卡住：**
1. **风险偏好无法统一**：激进者觉得期权值 10 块，保守者觉得只值 2 块，无法形成市场统一均衡价格。
2. **风险无法被对冲**：持有期权就像买彩票，无法抹平随机波动带来的巨大风险。

**为什么必须引入 Black-Scholes 模型：**
Black 和 Scholes 提出了天才式的概念——**动态 Delta 对冲（Dynamic Delta Hedging）**。
在连续时间内，通过构造一个由“1 份期权”和“-$\Delta$ 份股票”组成的对冲组合，股票的随机布朗运动（Brownian Motion）被完全抵消，组合变成了**完全无风险的纯贴现组合**！

**它到底解决了哪类问题：**
解决了**无需知道股价未来期望涨幅（剔除主观风险偏好 $\mu$），仅依靠波动率 $\sigma$ 和无风险利率 $r$ 即可对欧式衍生品进行精确无套利解析定价**的问题。

---

## 2. 为什么它重要？它有什么用？

- **体系与大图景**：金融工程与连续时间金融（Continuous Time Finance）的最高皇冠，衍生品定价的绝对基石。
- **量化与实操应用**：
  1. **期权做市商动态对冲**：做市商实时计算衍生品的 $\Delta = \frac{\partial C}{\partial S}$，在标的资产上进行买卖对冲，锁定买卖价差（Bid-Ask Spread）利润。
  2. **反推隐含波动率 (IV)**：将市场实际交易的期权价格代入 BSM 逆向求解 $\sigma_{implied}$，用于预测市场恐慌指数（如 VIX）。
  3. **结构化衍生品定价**：雪球期权、障碍期权、可转债拆解的数学基准。

---

## 3. 学它之前需要哪些前置知识？

1. **[[二叉树定价]]**：理解离散时间下的无套利复制组合与风险中性定价（Risk-Neutral Valuation）。
2. **伊藤引理 (Itô's Lemma)**：连续时间随机微积分的核心链式法则：
   $$df(t, S_t) = \left( \frac{\partial f}{\partial t} + \mu S \frac{\partial f}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 f}{\partial S^2} \right) dt + \sigma S \frac{\partial f}{\partial S} dW_t$$
3. **最小必要背景（几何布朗运动 GBM）**：
   > 假定标的资产价格服从：$\frac{dS_t}{S_t} = \mu dt + \sigma dW_t$，其中 $dW_t \sim N(0, dt)$ 为维纳过程（Wiener Process）。

---

## 4. 用直觉语言解释它

### 生活类比：用买保险和对冲消灭随机性

假设你买了一辆价值 100 万元的跑车，担心今年出车祸降价。
如果你同时雇佣了一个精明的算命师（Delta 对冲），每次路况变差，他就立刻帮你卖空一部分车辆配件；路况变好，他就帮你补回配件。
通过**每一秒钟根据路况实时微调配件持仓**，你发现无论天气怎么变、车祸发不发生，你账户里的资产总价值变动都跟存银行拿固定利息完全一模一样！

**Black-Scholes 的直觉本质**：
期权的价格本质上就是**持续维护这个“无风险对冲复制组合”所必须花费的成本**。

«“B-S 公式证明了只要你每一秒都在做动态对冲，期权风险就能被完全抹平，其价格只取决于资产的波动剧烈程度，而与大家看涨还是看跌无关。”»

---

## 5. 正式定义、核心公式、符号解释

### 核心定义
**Black-Scholes 欧式看涨/看跌期权定价公式**：在无摩擦市场、几何布朗运动与无套利假设下，无红利支付的欧式看涨期权价格等于标的资产价格乘上第一概率因子，减去执行价格折现值乘上第二概率因子。

### 核心公式

#### 1. 欧式看涨期权 (Call Option) 定价公式
$$C(S_0, t) = S_0 N(d_1) - K e^{-r T} N(d_2)$$

#### 2. 欧式看跌期权 (Put Option) 定价公式
$$P(S_0, t) = K e^{-r T} N(-d_2) - S_0 N(-d_1)$$

#### 3. 参数 $d_1$ 与 $d_2$ 公式
$$d_1 = \frac{\ln(S_0 / K) + \left( r + \frac{\sigma^2}{2} \right) T}{\sigma \sqrt{T}}$$
$$d_2 = d_1 - \sigma \sqrt{T} = \frac{\ln(S_0 / K) + \left( r - \frac{\sigma^2}{2} \right) T}{\sigma \sqrt{T}}$$

#### 4. Black-Scholes 偏微分方程 (BS-PDE)
$$\frac{\partial V}{\partial t} + r S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - r V = 0$$

### 符号解释表

| 符号 | 含义 | 维度/量纲 | 备注与几何/概率意义 |
| :--- | :--- | :--- | :--- |
| $S_0$ | 标的资产当前现货价格 | 货币单位 | 即期价格 |
| $K$ | 期权履约/执行价格 (Strike) | 货币单位 | 未来买卖的约定价 |
| $r$ | 连续复利无风险利率 | 年化百分比 | 贴现基准 |
| $T$ | 到期剩余时间 | 年 (Years) | 如 6 个月取 $0.5$ |
| $\sigma$ | 标的资产年化波动率 | 年化百分比 | GBM 扩散项参数 |
| $N(\cdot)$ | 标准正态分布累积概率函数 (CDF) | $[0, 1]$ | $N(x) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^x e^{-\frac{u^2}{2}} du$ |
| $N(d_1)$ | 看涨期权 Delta ($\Delta$) | $[0, 1]$ | 复制组合中需持有的标的资产份数 |
| $N(d_2)$ | 风险中性世界中期权被行权的概率 | $[0, 1]$ | 期权最终实值 (ITM) 的概率 |

---

## 6. 推导思路和思想来源

### 动态 Delta 对冲与 PDE 导出主线

1. **构造无风险组合 $\Pi$**：
   考虑在 $t$ 时刻卖出 1 份期权 $V(S, t)$，同时买入 $\Delta$ 份股票 $S$：
   $$\Pi = -V + \Delta S$$
2. **计算组合的微元变化 $d\Pi$**：
   根据伊藤引理展开 $dV$：
   $$dV = \left( \frac{\partial V}{\partial t} + \mu S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} \right) dt + \sigma S \frac{\partial V}{\partial S} dW_t$$
   代入 $d\Pi = -dV + \Delta dS$：
   $$d\Pi = -\left( \frac{\partial V}{\partial t} + \mu S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} \right) dt - \sigma S \frac{\partial V}{\partial S} dW_t + \Delta (\mu S dt + \sigma S dW_t)$$
3. **消除随机项 $dW_t$（关键转念！）**：
   令 $dW_t$ 的系数等于 0：
   $$-\sigma S \frac{\partial V}{\partial S} + \Delta \sigma S = 0 \implies \Delta = \frac{\partial V}{\partial S}$$
   此时，组合成为**完全确定性的无风险资产**！
4. **无套利要求组合只能赚取无风险收益 $r$**：
   $$d\Pi = r \Pi dt \implies d\Pi = r (-V + \Delta S) dt$$
5. **化简即得 Black-Scholes PDE**：
   代入展开项并消除 $\mu$（真实期望收益率 $\mu$ 消失了！），整理得到著名的 BSM PDE：
   $$\frac{\partial V}{\partial t} + r S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - r V = 0$$
   结合终端条件 $C(S, T) = \max(S_T - K, 0)$，利用变量代换化为热传导方程求解，即得解析解公式。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算例题（计算 $d_1, d_2$ 与 Call 期权价格）

**题目**：
已知某股票当前价格 $S_0 = 100$ 元，执行价格 $K = 100$ 元（平值 Call）。
无风险利率 $r = 5\%$（连续复利），年化波动率 $\sigma = 20\%$，剩余到期时间 $T = 1$ 年。
已知标准正态分布表中：$N(0.425) \approx 0.6646$，$N(0.225) \approx 0.5890$。
求该看涨期权的理论价格 $C$。

**解答过程**：
1. 计算 $d_1$：
   $$d_1 = \frac{\ln(100/100) + (0.05 + 0.5 \times 0.20^2) \times 1}{0.20 \times \sqrt{1}} = \frac{0 + 0.05 + 0.02}{0.20} = \frac{0.07}{0.20} = 0.35$$
   （假设精确查表 $N(0.35) = 0.6368$）。
2. 计算 $d_2$：
   $$d_2 = d_1 - \sigma \sqrt{T} = 0.35 - 0.20 = 0.15$$
   （查表 $N(0.15) = 0.5596$）。
3. 代入 BSM 公式：
   $$C = 100 \times 0.6368 - 100 \times e^{-0.05 \times 1} \times 0.5596$$
   因为 $e^{-0.05} \approx 0.9512$：
   $$C = 63.68 - 100 \times 0.9512 \times 0.5596 = 63.68 - 53.23 = 10.45 \text{ 元}$$

---

### 例子 2：中等例题（看跌-看涨期权平价公式 Put-Call Parity 验证）

**题目**：
利用上一题条件，已知 $C = 10.45$ 元。使用看跌-看涨期权平价公式（Put-Call Parity）直接计算同等条件下的欧式看跌期权价格 $P$。

**解答过程**：
1. 看跌-看涨平价公式：
   $$C + K e^{-rT} = P + S_0$$
2. 移项求 $P$：
   $$P = C + K e^{-rT} - S_0 = 10.45 + 100 \times e^{-0.05} - 100$$
3. 代入计算：
   $$P = 10.45 + 95.12 - 100 = 5.57 \text{ 元}$$

---

### 例子 3：实际应用（Python 编写 BSM 衍生品定价与 Delta 对冲仿真）

```python
import numpy as np
from scipy.stats import norm

def bsm_call_price(S, K, r, T, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    delta = norm.cdf(d1)
    return price, delta

# 模拟当前标的 50 ETF 价格 2.80，行权价 2.80，r=2.5%, T=0.25(3个月), Vol=18%
price, delta = bsm_call_price(2.80, 2.80, 0.025, 0.25, 0.18)
print(f"50ETF 看涨期权理论单价: {price:.4f} 元, Delta 对冲比例: {delta:.4f}")
```

---

## 7.5 💥 课本挂载与工业级实战模块 (Textbook Mapping & Production Lab)

### 7.5.1 📚 经典课本章节锚定
- **教材挂载 1**：John C. Hull *《Options, Futures, and Other Derivatives (期权、期货及其他衍生产品)》* 第 15 章 "The Black-Scholes-Merton Model" 与 第 19 章 "The Greek Letters"。
  - **课本必读重点**：对数正态性质、Itô 引理证明 BSM-PDE、动态 Delta 对冲的无套利复制。
  - **推荐课后习题**：Hull Ch 15 Ex 15.11, 15.14（Call/Put 平价验证与异型股息支付调整）。
- **教材挂载 2**：Paul Wilmott *《Paul Wilmott on Quantitative Finance》* 第 6 章 "The Black-Scholes Header"。
  - **实战挂载重点**：热传导方程 (Heat Equation) 化简与离散化有限差分求解。

### 7.5.2 ⚙️ 工业级 Python 最小可运行实战脚手架
包含：BSM 闭式解定价、Delta 中性对冲模拟 (Delta-Neutral Hedging Simulation) 与每日对冲损益 PnL 归因追踪。

```python
import numpy as np
import pandas as pd
from scipy.stats import norm

def run_bsm_delta_hedging_lab():
    # 1. 拟合参数设置
    S0 = 100.0       # 初始标的价格
    K = 100.0        # 卖出 Call 的行权价
    r = 0.03         # 无风险利率 3%
    sigma = 0.20     # 真实波动率 20%
    T = 0.25         # 到期时间 3 个月 (63 个交易日)
    N_steps = 63
    dt = T / N_steps
    
    # 2. 模拟一条标的股价漫步轨迹 (GBM)
    np.random.seed(42)
    Z = np.random.normal(0, 1, N_steps)
    price_path = np.zeros(N_steps + 1)
    price_path[0] = S0
    for t in range(1, N_steps + 1):
        price_path[t] = price_path[t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[t-1])
        
    # 3. 动态 Delta 对冲模拟：期权空头 + 买入 Delta * S0 现货
    def bsm_delta(S, K, tau, r, sigma):
        if tau <= 1e-5: return 1.0 if S > K else 0.0
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * tau) / (sigma * np.sqrt(tau))
        return norm.cdf(d1)
    
    def bsm_call_price(S, K, tau, r, sigma):
        if tau <= 1e-5: return max(S - K, 0)
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * tau) / (sigma * np.sqrt(tau))
        d2 = d1 - sigma * np.sqrt(tau)
        return S * norm.cdf(d1) - K * np.exp(-r * tau) * norm.cdf(d2)

    # 第一天：卖出 1 份 Call 收到权利金，建立 Delta 现货多头
    init_call_price = bsm_call_price(S0, K, T, r, sigma)
    init_delta = bsm_delta(S0, K, T, r, sigma)
    
    cash_account = init_call_price - init_delta * S0 # 借入现金买现货
    stock_shares = init_delta
    
    # 每日重新调仓 Delta 对冲
    for step in range(1, N_steps):
        tau = T - step * dt
        S_t = price_path[step]
        
        # 现金账户生息
        cash_account *= np.exp(r * dt)
        
        # 重新计算新 Delta 并调整现货持仓
        new_delta = bsm_delta(S_t, K, tau, r, sigma)
        delta_shares = new_delta - stock_shares
        
        cash_account -= delta_shares * S_t
        stock_shares = new_delta

    # 到期日结算
    final_S = price_path[-1]
    final_call_payoff = max(final_S - K, 0)
    final_portfolio_value = stock_shares * final_S + cash_account * np.exp(r * dt) - final_call_payoff

    print("=== Black-Scholes 动态 Delta 对冲 Lab 结果 ===")
    print(f"初始收到期权金: {init_call_price:.4f} 元")
    print(f"标的到期价格: {final_S:.2f} 元 | 真实期权交割负债: {final_call_payoff:.2f} 元")
    print(f"Delta 动态对冲组合最终净残余 PnL: {final_portfolio_value:.4f} 元 (接近0，无套利成功)")

run_bsm_delta_hedging_lab()
```

### 7.5.3 ⚠️ 实盘落地“踩坑指南”与回测陷阱
1. **离散对冲滑点与 Gamma 风险 (Discrete Rebalancing Error)**：
   理论 BSM 假设“连续时刻对冲”。实盘中只能按分钟/日度离散对冲，若标的发生跳空剧烈波动（大 Gamma 区域），离散对冲会产生显著的 Gamma PnL 损耗。
2. **波动率偏斜与微笑 (Volatility Smile / Skew Violation)**：
   BSM 假设波动率 $\sigma$ 为常数。实盘市场中，不同行权价的期权存在显著的隐含波动率偏斜（Deep OTM Put IV 远高于 ITM Put），盲目套用单一定值 $\sigma$ 会导致虚假估值过高或过低。
3. **借贷利率非对称与融券成本**：
   BSM 假设无风险借款与贷款利率相同（$r_{borrow} = r_{lend}$）。实盘融券做空现货需要支付额外的融券利息（如 8%），会侵蚀对冲收益。

### 7.5.4 📊 实战性能评估指标体系
- **对冲跟踪误差 (Hedging Error Variance)**：$\text{Var}(\text{PnL}_{hedged})$。
- **Delta 中性度 (Delta Neutrality)**：$|\Delta_{portfolio}| \le 0.05$。
- **Gamma 风险暴露 (Gamma Exposure)**：$\Gamma = \frac{N'(d_1)}{S \sigma \sqrt{\tau}}$。

### 7.5.5
> 🔓 **作业解锁前置条件**：学完 [[远期、期货与期权的区别]] + [[二叉树定价]] + [[Black-Scholes]] + [[Greeks]] 即可正式解锁本 Challenge 实战！
> 💡 **解锁指引**：掌握 BSM 偏微分方程解与希腊字母 Delta 性质后即可解锁连续动态对冲。

 🧪 拓展实验与李宏毅式实战 Challenge 题 (HW05-Black-Scholes 期权定价与动态 Delta 中性对冲模拟)

本作业参考 **李宏毅 (Hung-yi Lee) 教授 ML 课程作业架构** 设计，设置四个渐进式难度基线 (Baselines)：

- 🟢 **简单基线 (Simple Baseline)**：
  - **任务要求**：使用 Python 实现 BSM 欧式看涨/看跌期权定价函数，验证 Put-Call Parity 理论无套利平价。
  - **达标标准**：代码无 Error 跑通，输出基础结果。

- 🟡 **中等基线 (Medium Baseline)**：
  - **任务要求**：模拟股价几何布朗运动 (GBM) 路径，每日根据 $\Delta_{BSM}$ 动态买卖标的股票，追踪连续 30 天对冲损益 PnL。
  - **达标标准**：完成核心算法的向量化与参数校准，模型表现达到基线水平。

- 🔴 **强基线 (Strong Baseline)**：
  - **任务要求**：加入真实离散对冲频率（如每小时对冲一次）产生的 Gamma 损耗，并结合实际买卖价差（Spread）计算对冲总滑点。
  - **达标标准**：扣除交易摩擦与滑点后，样本外 (OOS) 夏普比率 $> 1.8$ 或评估指标提升 20% 以上。

- 🟣 **Boss 基线 (Kaggle / 实盘级基线)**：
  - **任务要求**：构建结合波动率偏斜 (Volatility Skew) 的动态 Delta-Vega 联合对冲器，在 2008 年级历史大暴跌中保持期权组合 PnL 波动率 $< 3\%$。
  - **达标标准**：代码具备极强泛化性与抗过拟合能力，通过 PBO 审计且过拟合概率 $\text{PBO} < 10\%$。


## 8. 常见误区与易混概念

### 误区 1：股票看涨预期越强（$\mu$ 越高），Call 期权价格越贵

错误直觉：“大家都预测股价明年大涨 50%，看涨期权价格肯定要飙升。”  
为什么错：BSM 模型推导表明，通过连续动态 Delta 对冲消除了随机风险后，标的资产的预期收益率 $\mu$ **在 PDE 和定价公式中被完全消除**，取而代之的是无风险利率 $r$。  
正确理解：期权价格只与波动率 $\sigma$ 有关，与市场主观的预期涨幅 $\mu$ 无关（在风险中性世界中，所有资产以 $r$ 增长）。

### 概念对比：历史波动率 vs 隐含波动率 (IV)

| 维度 | 历史波动率 (Historical Volatility) | 隐含波动率 (Implied Volatility) |
| :--- | :--- | :--- |
| **数据来源** | 标的资产过去 N 天的历史对数收益率标准差 | 将当前市场期权报价反套入 BSM 公式逆向求解 |
| **时间视角** | 后视视角 (Backward-looking) | 前瞻视角 (Forward-looking)，反映市场未来恐慌度 |
| **主要应用** | 历史风险测算 | 期权做市、Volatility Smile 分析与套利 |

---

## 9. 相关知识点与 Obsidian 双链建议

请帮我建立知识网络。

注意：不要只列链接。每个链接后面必须用一句话说明“为什么要链接”。

上游依赖

- [[远期、期货与期权的区别]]：提供基础概念与理论推导支撑。
- [[二叉树定价]]：提供基础概念与理论推导支撑。

下游延伸

- [[Greeks]]：进一步延伸拓展该知识点的应用场景与模型构建。
- [[高阶希腊字母与衍生品风险对冲 (Higher-Order Greeks_ Vanna, Volga & Charm)|高阶希腊字母与对冲]]：进一步延伸拓展该知识点的应用场景与模型构建。
- [[隐含波动率]]：进一步延伸拓展该知识点的应用场景与模型构建。

横向关联

- [[收益率与对数收益率]]：衡量资产收益特性的基础量纲。
- [[实盘风控]]：风险控制与投资组合保护。

应用场景

- [[实盘风控]]：工业级量化策略风控与组合风险度量。


## 10. 闭卷复现任务

1. [ ] 默写 BSM 欧式看涨期权定价公式及其 $d_1, d_2$ 表达式。
2. [ ] 解释动态 Delta 对冲的物理含义（$\Delta = N(d_1)$）。
3. [ ] 说明为什么标的资产期望收益率 $\mu$ 不出现在 BSM 公式中。
4. [ ] 默写看跌-看涨期权平价公式 (Put-Call Parity)。
5. [ ] 列出 BSM 模型的核心假设与适用限制。

---

## 11. 自测题（5 道）

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | BSM 剔除的参数 |
| 2 | 公式运用 | 基础 | 利用 Put-Call Parity 计算 Put 价格 |
| 3 | 条件判断 | 中等 | 波动率 $\sigma$ 增大对 Call 和 Put 价格的影响 |
| 4 | 变式/综合 | 中等 | 到期时间 $T \to 0$ 时平值 Call 期权的极限价值 |
| 5 | 开放/证明 | 较难 | 利用伊藤引理推导无风险组合 $d\Pi$ 过程 |

---

### 第 1 题：概念辨析（基础）
**题目**：在 Black-Scholes 期权定价公式中，不包含下列哪一个变量？
A. 标的股价 $S_0$  B. 标的资产预期收益率 $\mu$  C. 波动率 $\sigma$  D. 无风险利率 $r$

> [!question]- 答案解析
> **答案**：B。通过动态 Delta 对冲，预期收益率 $\mu$ 被完全消除，定价处于风险中性世界。  
> **Obsidian 标签**：`#自测题/BSM假设`

---

### 第 2 题：公式运用（基础）
**题目**：某股票现价 50 元，6 个月期平值 Call 价格为 4.0 元。连续复利无风险利率 $r=4\%$。求同期限 50 元 Put 价格。（$e^{-0.02} \approx 0.9802$）

> [!question]- 答案解析
> **答案**：
> 由 $C + K e^{-rT} = P + S_0$：
> $4.0 + 50 \times 0.9802 = P + 50 \implies 4.0 + 49.01 = P + 50 \implies P = 3.01 \text{ 元}$。  
> **Obsidian 标签**：`#自测题/平价公式`

---

### 第 3 题：条件判断（中等）
**题目**：判断：“当标的资产的年化波动率 $\sigma$ 上升时，欧式看涨期权价格上升，而欧式看跌期权价格下降。”

> [!question]- 答案解析
> **答案**：错误。波动率增加增大了资产价格向上和向下的不确定性。由于期权具有“下行风险有限、上行收益无限”的非对称凸性（Convexity），无论是 Call 还是 Put，其价格都会随波动率 $\sigma$ 增加而上升（即 Vega $> 0$）。  
> **Obsidian 标签**：`#自测题/期权Vega`

---

### 第 4 题：变式/综合（中等）
**题目**：若某股票当前价格 $S_0 = 100$，执行价 $K = 100$。当到期剩余时间 $T \to 0$ 时，平值看涨期权价格 $C$ 趋向于多少？

> [!question]- 答案解析
> **答案**：当 $T \to 0$ 时，期权的时间价值（Time Value）衰减为 0。平值期权（$S_0 = K$）的内在价值为 $\max(100 - 100, 0) = 0$。因此 $C \to 0$。  
> **Obsidian 标签**：`#自测题/时间价值`

---

### 第 5 题：开放/证明（较难）
**题目**：简述为什么看涨期权价格对股价的偏导数 $\frac{\partial C}{\partial S}$（即 Delta）精确等于标准正态分布的累积概率 $N(d_1)$？

> [!question]- 答案解析
> **解析**：
> 对 BSM 公式 $C = S N(d_1) - K e^{-rT} N(d_2)$ 关于 $S$ 求全导数：
> $$\frac{\partial C}{\partial S} = N(d_1) + S N'(d_1) \frac{\partial d_1}{\partial S} - K e^{-rT} N'(d_2) \frac{\partial d_2}{\partial S}$$
> 利用等式 $S N'(d_1) = K e^{-rT} N'(d_2)$（可通过展开正态概率密度函数密度指数证明），后两项相互抵消，精准留下：
> $$\frac{\partial C}{\partial S} = N(d_1)$$  
> **Obsidian 标签**：`#自测题/Delta证明`

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
- **建议双链**：[[二叉树定价]]、[[Greeks]]、[[隐含波动率]]
- **标签**：`#学习` `#量化金融` `#期权定价` `#Black-Scholes` `#随机微积分` `#Greeks`

---

<!-- quant-evidence-v3 -->
## 可定位依据与失效复核

本卡的复核对象是 **Black-Scholes 期权定价模型**，而不是只复述一个公式。对 **Black-Scholes 期权定价模型** 的独立验证重点是：用 put-call parity、单调性和极限值三组性质测试，而不是只比对一个价格。

### 权威来源与定位

1. Black 与 Scholes (1973), *The Pricing of Options and Corporate Liabilities*, DOI: 10.1086/260062。用于复核“用 put-call parity、单调性和极限值三组性质测试，而不是只比对一个价格”。
2. Merton (1973), *Theory of Rational Option Pricing*, DOI: 10.2307/3003143。用于复核“用 put-call parity、单调性和极限值三组性质测试，而不是只比对一个价格”。
3. John C. Hull, *Options, Futures, and Other Derivatives*, Pearson, ISBN 9780134472089, Chapter 13–20（树模型、Black–Scholes、Greeks 与波动率微笑）。用于复核“用 put-call parity、单调性和极限值三组性质测试，而不是只比对一个价格”。

### 失效边界与验收协议

- **成立条件**：先写清数据时点、估计窗口、交易摩擦和分布/市场结构假设，再运行模型。
- **反例压力测试**：用 put-call parity、单调性和极限值三组性质测试，而不是只比对一个价格。
- **最小实验**：固定随机种子或冻结原始数据快照，同时保存基线、破坏条件后的对照组、关键中间量与失败日志。
- **通过标准**：结论必须在样本外仍保持方向一致；若成本、延迟、参数扰动或结构突变使结论反转，就把该情形登记为适用边界而不是删除失败结果。
