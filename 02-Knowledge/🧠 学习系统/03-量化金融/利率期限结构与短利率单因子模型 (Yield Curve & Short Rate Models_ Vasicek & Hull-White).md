---
title: '利率期限结构与短利率单因子模型 (Yield Curve & Short Rate Models: Vasicek & Hull-White)'
date: 2026-07-23
type: concept
course: 量化金融
importance: A
tags:
- 学习
- 量化金融
- 固收
- 利率期限结构
- 收益率曲线
- Vasicek
- HullWhite
- 短利率模型
- 均值回归
upstream:
- '[[国债逆回购 (Treasury Reverse Repo)|国债逆回购]]'
- '[[同业存单 (Negotiable Certificate of Deposit, NCD)|同业存单]]'
downstream:
- '[[Black-Scholes]]'
- '[[实盘风控]]'
status: learning
---
# 利率期限结构与短利率单因子模型 (Yield Curve & Short Rate Models: Vasicek & Hull-White)

---

## 0. 先判断它值不值得深挖

**分类：A 类（核心概念，必须深挖）**

**理由：**
利率期限结构与短利率模型（Yield Curve & Short Rate Models，以 Vasicek 1977 模型与 Hull-White 1990 无套利扩展模型为代表）是固定收益量化（Fixed Income Quant）、国债期货套利与利率衍生品（Swaps/Swaptions）定价的基石。不同于股票价格（随机游走发散），利率在宏观经济中受到中央银行（如美联储/央行）货币政策调控，具有极强的**均值回归（Mean Reversion）**特性。学会用随机微分方程 (SDE) 建模短利率 $r_t$ 并拟合整条收益率曲线（Yield Curve），是量化金融的核心功底。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**

假设你正在交易国债期货或利率互换（Interest Rate Swaps, IRS）。
如果直接使用股票的几何布朗运动（GBM $dS_t = \mu S_t dt + \sigma S_t dW_t$）建模利率：
1. GBM 假定利率会像股票一样无休止地指数拉升到正无穷，或者暴跌到零；
2. GBM 忽视了央行在利率过高时降息、过低时加息的**均值回归引力**；
3. 更致命的是，GBM 无法给不同到期期限（1年、5年、10年、30年）的国债算出一条符合市场真实平滑形状的收益率曲线（Yield Curve）。

**以前的方法在哪里卡住：**
无法在随机微分方程中引入**均值回归拉力 $\kappa (\theta - r_t)$**，且传统模型（Vasicek）无法完美拟合初始即期收益率曲线（Initial Yield Curve）。

**为什么必须引入短利率模型 (Vasicek / Hull-White)：**
设定瞬时短利率 $r_t$ 服从带均值回归的随机过程，并通过引入时间可变参数 $\theta(t)$（Hull-White），强制让模型算出的零息债券价格 $P(0, T)$ 100% 精确匹配今天市场上的真实国债收益率曲线。

**它到底解决了哪类问题：**
解决了**利率均值回归随机过程建模、国债收益率曲线全期限无套利定价以及利率衍生品风险对冲**的问题。

---

## 2. 为什么它重要？它有什么用？

- **体系与大图景**：固定收益与利率量化（第二阶段）的最核心框架，连接货币市场、国债期货与 Swap/Cap/Floor 定价。
- **量化与实战应用**：
  1. **国债收益率曲线形态套利 (Yield Curve Arbitrage)**：利用 Hull-White 模型评估 2 年期与 10 年期国债利差 (2Y-10Y Spread) 的陡峭化（Steepening）与平坦化（Flattening）。
  2. **房贷抵押证券 (MBS) 与 Swaption 风险对冲**：为带有提前还款期权（Prepayment Risk）的固收产品定价。

---

## 3. 学它之前需要哪些前置知识？

1. **[[国债逆回购 (Treasury Reverse Repo)|国债逆回购]]**、**[[同业存单 (Negotiable Certificate of Deposit, NCD)|同业存单]]**：理解货币市场短期利率与贴现债券定价。
2. **最小必要背景（零息债券价格与 Yield 转换关系）**：
   > $T$ 到期、面值 1 元的零息债券（Zero-Coupon Bond）在 $t$ 时刻的价格 $P(t, T)$：
   > $$P(t, T) = \exp\left( -Y(t, T) \cdot (T - t) \right) \implies Y(t, T) = -\frac{\ln P(t, T)}{T - t}$$
   > 其中 $Y(t, T)$ 即为 $T-t$ 期限的年化即期收益率 (Spot Rate)。

---

## 4. 用直觉语言解释它

### 生活类比：带有温控器的空调房间温度变化

- 假设房间的温度（短利率 $r_t$）：
  - 房间外面天气寒冷，但房间里装了一个**智能温控器（中央银行）**。
  - 温控器设定了目标舒适温度 $\theta = 24^\circ\text{C}$（目标基准利率）。
  - 当开窗突然涌入一阵冷空气使室温降到 $18^\circ\text{C}$ 时，温控器会以拉力 $\kappa$ 自动加大加热功率，把温度重新拉回 $24^\circ\text{C}$。
  - 外界随机的风吹（随机扰动 $\sigma dW_t$）会让温度产生小幅随机抖动，但温控器永远在做反向拉回。

**短利率模型的直觉本质**：
利率不会像股票一样无限暴涨或清零，它像被温控器控制的房间温度一样，时刻受到央行目标的“均值回归拉力”。

«“短利率模型就是把利率看成被央行‘温控器’控制的房间温度，在随机小抖动中永远向目标均值靠拢。”»

---

## 5. 正式定义、核心公式、符号解释

### 核心定义
1. **Vasicek 模型 (1977)**：假设短利率 $r_t$ 服从带常数均值回归速度与常数波动率的奥恩斯坦-乌伦贝克 (Ornstein-Uhlenbeck, OU) 过程。
2. **Hull-White 模型 (1990)**：对 Vasicek 模型的长期均值进行时间可变扩展 $\theta(t)$，使其能够 100% 完全精确拟合给定的初始收益率曲线。

### 核心公式

#### 1. Vasicek 短利率随机微分方程 (SDE)
$$dr_t = \kappa (\theta - r_t) dt + \sigma dW_t$$
- $\kappa > 0$：均值回归速度 (Speed of Mean Reversion)
- $\theta$：长期平均利率水平 (Long-term Mean Rate)
- $\sigma$：短利率波动率
- $dW_t$：标准布朗运动

#### 2. Vasicek 零息债券价格解析解 $P(t, T)$
$$P(t, T) = A(t, T) \exp\left( -B(t, T) r_t \right)$$
其中：
$$B(t, T) = \frac{1 - e^{-\kappa(T-t)}}{\kappa}$$
$$A(t, T) = \exp\left( \left( \theta - \frac{\sigma^2}{2\kappa^2} \right) \left[ B(t, T) - (T-t) \right] - \frac{\sigma^2}{4\kappa} B(t, T)^2 \right)$$

#### 3. Hull-White 单因子扩展 SDE (无套利扩展)
$$dr_t = [\theta(t) - a r_t] dt + \sigma dW_t$$
通过在每个时间点微调 $\theta(t)$，使导出的 $P(0, T)$ 完全等于市场观察到的即期贴现曲线 $f(0, T)$：
$$\theta(t) = \frac{\partial f(0, t)}{\partial t} + a f(0, t) + \frac{\sigma^2}{2a} (1 - e^{-2at})$$

### 符号解释表

| 符号 | 含义 | 维度/量纲 | 备注与要求 |
| :--- | :--- | :--- | :--- |
| $r_t$ | 瞬时短利率 (Short Rate) | 年化百分比 (如 2.5%) | 驱动整条收益率曲线的单因子 |
| $\kappa$ (或 $a$) | 均值回归速度 | 标量 (如 0.15) | 决定偏离后拉回的半衰期 |
| $\theta$ | 长期平均利率 | 年化百分比 | 央行中性利率 |
| $P(t, T)$ | $t$ 时刻 $T$ 到期的零息债券价格 | 货币单位 (如 0.95 元) | $P(T, T) = 1.0$ |
| $Y(t, T)$ | $T-t$ 期限的即期收益率 | 年化百分比 | $Y(t, T) = -\frac{\ln A(t, T) - B(t, T)r_t}{T-t}$ |

---

## 6. 推导思路和思想来源

### 为什么经典 Vasicek 模型在现代华尔街被 Hull-White 模型取代？
1. **Vasicek 的致命缺陷（无法无套利）**：
   在 Vasicek 模型中，$\theta$ 是常数。输入 $\kappa, \theta, \sigma$ 后，算出的 $P(0, T)$ 是一条固定形状的理论收益率曲线。但真实的市场收益率曲线包含复杂的扭曲（如倒挂、S 型），Vasicek 模型算出的价格与市场真实价格存在差价！交易员如果套用 Vasicek 定价，会被市场交易对手套利。
2. **转念（无套利校准 No-Arbitrage Fitting）**：
   Hull 和 White 提出：不要把 $\theta$ 设为死常数！让 $\theta(t)$ 成为时间的函数。
3. **结果**：通过对 $\theta(t)$ 进行时间曲线拟合，Hull-White 模型完美实现了“既保留均值回归性质，又能 100% 贴合今天市场上所有国债的价格（无套利校准）”！

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算例题（Vasicek 零息债券价格与 Yield 手算）

**题目**：
已知 Vasicek 模型参数：$\kappa = 0.5, \theta = 4.0\%, \sigma = 1.0\%$。
当前短利率 $r_0 = 2.0\%$。
求 2 年期零息债券（$T - t = 2$ 年）的 $B(0, 2)$ 辅助系数与即期收益率 $Y(0, 2)$ 的近似值。

**解答过程**：
1. 计算 $B(0, 2)$：
   $$B(0, 2) = \frac{1 - e^{-\kappa T}}{\kappa} = \frac{1 - e^{-0.5 \times 2}}{0.5} = \frac{1 - e^{-1.0}}{0.5} = \frac{1 - 0.3679}{0.5} = \frac{0.6321}{0.5} = 1.2642$$
2. 由于短利率 $r_0 = 2.0\%$ 低于长期均值 $\theta = 4.0\%$，均值回归拉力会推动未来的利率上升。
3. 计算 2 年期即期收益率 $Y(0, 2)$（在 $\sigma$ 较小时，近似为短利率与长期均值的加权）：
   $$Y(0, 2) \approx \frac{B(0, 2)}{T} r_0 + \left(1 - \frac{B(0, 2)}{T}\right) \theta = \frac{1.2642}{2} (2.0\%) + \left(1 - \frac{1.2642}{2}\right) (4.0\%)$$
   $$Y(0, 2) \approx 0.6321 \times 2.0\% + 0.3679 \times 4.0\% = 1.2642\% + 1.4716\% = 2.7358\%$$
4. **结论**：由于 $r_0 = 2.0\%$ 处于低位，2 年期收益率 $Y(0, 2) = 2.74\%$ 高于短利率（收益率曲线向上倾斜）。

---

### 例子 2：中等例题（根据 $\kappa$ 计算利率偏离的半衰期）

**题目**：
某国央行将基准利率大幅下调至 $1.0\%$，而 Vasicek 估计的长期均衡利率 $\theta = 3.0\%$，均值回归速度 $\kappa = 0.693$。
求市场短利率恢复回归到 $\theta$ 中间水平（即 2.0%）所需的半衰期天数/年数。

**解答过程**：
1. 均值回归的期望路径为：
   $$E[r_t] = \theta + (r_0 - \theta) e^{-\kappa t}$$
2. 当 $E[r_t] - \theta = \frac{1}{2} (r_0 - \theta)$ 时：
   $$e^{-\kappa t} = 0.5 \implies t_{half} = \frac{\ln 2}{\kappa}$$
3. 代入 $\kappa = 0.693$：
   $$t_{half} = \frac{0.69315}{0.693} \approx 1.0 \text{ 年}$$
4. **结论**：半衰期为 1.0 年，即市场利率预计在 1 年后回升到 2.0% 的中枢位置。

---

### 例子 3：实际应用（Python 矢量化构建 Vasicek 与 Hull-White 收益率曲线）

```python
import numpy as np
import matplotlib.pyplot as plt

def vasicek_yield_curve(r0, kappa, theta, sigma, maturities):
    """
    计算 Vasicek 模型下不同到期期限的即期收益率 Y(0, T)
    """
    yields = []
    for T in maturities:
        B = (1.0 - np.exp(-kappa * T)) / kappa
        A = np.exp((theta - 0.5 * (sigma**2) / (kappa**2)) * (B - T) - (sigma**2) * (B**2) / (4.0 * kappa))
        P = A * np.exp(-B * r0)
        Y = -np.log(P) / T
        yields.append(Y)
    return np.array(yields)

# 参数：短利率 2%，长期均值 4.5%，回归速度 0.3，波动率 1.5%
maturities = np.linspace(0.1, 10.0, 100) # 0.1 年到 10 年
yields = vasicek_yield_curve(r0=0.02, kappa=0.3, theta=0.045, sigma=0.015, maturities=maturities)

print("=== Vasicek 收益率曲线计算结果 ===")
print(f"1 年期即期收益率 Y(0, 1):  {yields[9]*100:.2f}%")
print(f"5 年期即期收益率 Y(0, 5):  {yields[49]*100:.2f}%")
print(f"10 年期即期收益率 Y(0, 10): {yields[-1]*100:.2f}%")
```

---

## 7.5 💥 课本挂载与工业级实战模块 (Textbook Mapping & Production Lab)

### 7.5.1 📚 经典课本章节锚定
- **教材挂载 1**：John C. Hull *《Options, Futures, and Other Derivatives》* 第 31 章 "Interest Rate Model" Section 31.3 "One-Factor Model (Vasicek, CIR, Hull-White)"。
  - **课本必读重点**：均值回归 SDE、A(t,T) 与 B(t,T) 的微分推导、Hull-White 树状图 (Trinomial Tree) 构建。
  - **推荐课后习题**：Hull Ch 31 Ex 31.10, 31.14（求解 3 年期 Caplet 定价与 Hull-White 树）。
- **教材挂载 2**：Bernt Øksendal *《Stochastic Differential Equations》* 第 5 章 "Financial Applications" - Term Structure of Interest Rates.
  - **实战挂载重点**：利用 Itô 引理与 Feynmann-Kac 公式推导零息债券偏微分方程 (PDE)。

### 7.5.2 ⚙️ 工业级 Python 最小可运行实战脚手架
（见上方 例子 3 完整代码）

### 7.5.3 ⚠️ 实盘落地“踩坑指南”与回测陷阱
1. **Vasicek 负利率许可陷阱 (Negative Interest Rates)**：
   Vasicek 模型假设短利率服从正态分布 $r_t \sim N(\cdot)$。在数学上，当波动率 $\sigma$ 较大且 $r_0$ 接近零时，模型算出的短利率 $r_t$ **有正概率变为负数**！在非负利率时代这被称为缺陷（CIR 模型通过 $\sigma \sqrt{r_t} dW_t$ 解决了负利率问题）。
2. **校准过拟合与“参数漂移 (Parameter Drift)”**：
   每天用市场贴现曲线反推校准 Hull-White 的 $\theta(t)$ 时，算出的参数会每日剧烈抖动。这会导致用 Hull-White 算的长期期权 Delta 对冲失效。

### 7.5.4 📊 实战性能评估指标体系
- **收益率曲线校准均方误差 (RMSE vs Market Yields)**：$\sqrt{\frac{1}{M}\sum (Y_{model}(T_i) - Y_{market}(T_i))^2}$。
- **久期与凸性 (Duration & Convexity)**：$D = -\frac{1}{P} \frac{\partial P}{\partial r} = B(t, T)$。
- **均值回归半衰期 $t_{half}$**：$\frac{\ln 2}{\kappa}$。

### 7.5.5
> 🔓 **作业解锁前置条件**：学完 [[收益率与对数收益率]] + [[利率期限结构与短利率单因子模型 (Yield Curve & Short Rate Models_ Vasicek & Hull-White)|利率期限结构与短利率模型]] 即可正式解锁本 Challenge 实战！
> 💡 **解锁指引**：理解 利率期限结构与短利率模型 的核心定义与基本推导逻辑后即可解锁。

 🧪 拓展实验与李宏毅式实战 Challenge 题 (Lab Assignment: 利率期限结构与短利率模型 工业级实战 challenge)

本作业参考 **李宏毅 (Hung-yi Lee) 教授 ML 课程作业架构** 设计，设置四个渐进式难度基线 (Baselines)：

- 🟢 **简单基线 (Simple Baseline)**：
  - **任务要求**：理解 利率期限结构与短利率模型 的核心数学定义，使用 Python 进行基础验证与数据提取。
  - **达标标准**：代码无 Error 跑通，输出基础结果。

- 🟡 **中等基线 (Medium Baseline)**：
  - **任务要求**：实现 利率期限结构与短利率模型 的完整向量化代码框架，在历史数据上拟合参数并校验稳定度。
  - **达标标准**：完成核心算法的向量化与参数校准，模型表现达到基线水平。

- 🔴 **强基线 (Strong Baseline)**：
  - **任务要求**：引入严格的防前视偏差、手续费扣除与 Purged 交叉验证，使基于 利率期限结构与短利率模型 的模块表现击败基线。
  - **达标标准**：扣除交易摩擦与滑点后，样本外 (OOS) 夏普比率 $> 1.8$ 或评估指标提升 20% 以上。

- 🟣 **Boss 基线 (Kaggle / 实盘级基线)**：
  - **任务要求**：结合真实工业级实盘环境（如高频盘口/高维去噪/强化学习），达成实盘级夏普比率与风险控制指标。
  - **达标标准**：代码具备极强泛化性与抗过拟合能力，通过 PBO 审计且过拟合概率 $\text{PBO} < 10\%$。


## 8. 常见误区和易混概念

### 误区 1：短利率模型算出的 $r_t$ 就是我们去银行存钱的 1 年期定期存款利率

错误直觉：“$r_t$ 等于 1 年期国债收益率。”  
为什么错：$r_t$ 是**瞬时短利率 (Instantaneous Short Rate)**，代表时间间隔 $\Delta t \to 0$ 极限下的无风险隔夜/极短借贷利率（类似隔夜 Shibor 或 SOFR）。1 年期收益率是 $r_t$ 在未来 1 年路径的积分平均值！  
正确理解：**$r_t$ 是驱动全期限收益率曲线的根源“种子变量”，而非长期利率本身。**

### 概念对比：Vasicek 模型 vs CIR 模型 vs Hull-White 模型

| 维度 | Vasicek 模型 (1977) | CIR 模型 (Cox-Ingersoll-Ross 1985) | Hull-White 单因子模型 (1990) |
| :--- | :--- | :--- | :--- |
| **SDE 项** | $dr_t = \kappa(\theta - r_t)dt + \sigma dW_t$ | $dr_t = \kappa(\theta - r_t)dt + \sigma \mathbf{\sqrt{r_t}} dW_t$ | $dr_t = [\mathbf{\theta(t)} - a r_t]dt + \sigma dW_t$ |
| **负利率许可** | **允许负利率** | **严格保证 $r_t > 0$**（若 $2\kappa\theta > \sigma^2$） | **允许负利率** |
| **市场曲线无套利校准** | 无法完美贴合市场曲线 | 无法完美贴合市场曲线 | **100% 精确贴合当前市场收益率曲线** |
| **解析解难度** | 闭式简单 | 闭式稍复杂 (含 Bessel 函数) | 闭式简单 |

---

## 9. 相关知识点与 Obsidian 双链建议

请帮我建立知识网络。

注意：不要只列链接。每个链接后面必须用一句话说明“为什么要链接”。

上游依赖

- [[国债逆回购 (Treasury Reverse Repo)|国债逆回购]]：提供基础概念与理论推导支撑。
- [[同业存单 (Negotiable Certificate of Deposit, NCD)|同业存单]]：提供基础概念与理论推导支撑。

下游延伸

- [[Black-Scholes]]：进一步延伸拓展该知识点的应用场景与模型构建。
- [[实盘风控]]：进一步延伸拓展该知识点的应用场景与模型构建。

横向关联

- [[收益率与对数收益率]]：衡量资产收益特性的基础量纲。
- [[实盘风控]]：风险控制与投资组合保护。

应用场景

- [[实盘风控]]：工业级量化策略风控与组合风险度量。


## 10. 闭卷复现任务

1. [ ] 默写 Vasicek 短利率随机微分方程 (SDE)。
2. [ ] 用“带有温控器的房间温度”解释均值回归短利率模型的直觉。
3. [ ] 默写 Vasicek 零息债券价格解析解中 $B(t, T)$ 的表达形式。
4. [ ] 解释为什么 Hull-White 模型要引入时间可变参数 $\theta(t)$（消除套利）。
5. [ ] 比较 Vasicek 模型与 CIR 模型在负利率上的区别。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 均值回归参数 $\kappa$ 的物理含义 |
| 2 | 公式运用 | 基础 | 利用 $\kappa = 0.4$ 计算 $B(0, 1)$ |
| 3 | 条件判断 | 中等 | 短利率 $r_0 > \theta$ 时的收益率曲线形状 |
| 4 | 变式/综合 | 中等 | CIR 模型中防止负利率的 Feller 条件 |
| 5 | 开放/证明 | 较难 | 利用伊藤引理推导零息债券 $P(t, T)$ 满足的偏微分方程 (PDE) |

---

### 第 1 题：概念辨析（基础）
**题目**：在 Vasicek 短利率模型 $dr_t = \kappa (\theta - r_t) dt + \sigma dW_t$ 中，当偏离值 $r_t - \theta > 0$ 时，漂移项 $(\theta - r_t)$ 的符号是什么？

> [!question]- 答案解析
> **答案**：符号为负。代表当短利率高于长期均值 $\theta$ 时，漂移项会产生向下拉拽的力量，拉动利率向下回调靠拢 $\theta$。  
> **Obsidian 标签**：`#自测题/Vasicek`

---

### 第 2 题：公式运用（基础）
**题目**：$\kappa = 1.0$。求 $T - t = 1$ 年期零息债券的 $B(0, 1)$ 值（已知 $e^{-1} \approx 0.3679$）。

> [!question]- 答案解析
> **答案**：
> $B(0, 1) = \frac{1 - e^{-1.0 \times 1}}{1.0} = 1 - 0.3679 = 0.6321$。  
> **Obsidian 标签**：`#自测题/B系数手算`

---

### 第 3 题：条件判断（中等）
**题目**：判断：“在倒挂的收益率曲线（Inverted Yield Curve）中，通常对应着当前短利率 $r_0$ 远高于长期均值 $\theta$ 的极端紧缩时期。”

> [!question]- 答案解析
> **答案**：正确。当央行大幅加息使短利率 $r_0$ 处于极高位置（$r_0 \gg \theta$）时，市场预期未来利率必然会均值回归向下回落，导致长期收益率低于短利率，产生收益率曲线倒挂。  
> **Obsidian 标签**：`#自测题/收益率倒挂`

---

### 第 4 题：变式/综合（中等）
**题目**：CIR 模型中防止短利率触及负数或零的“Feller 条件 (Feller Condition)”是什么？

> [!question]- 答案解析
> **答案**：
> 限制条件为：**$2 \kappa \theta \ge \sigma^2$**。
> 当均值回归拉力 $2 \kappa \theta$ 足够强大，足以克服随机波动率 $\sigma^2$ 的向下推力时，短利率 $r_t$ 严格大于 0（处处恒正）。  
> **Obsidian 标签**：`#自测题/Feller条件`

---

### 第 5 题：开放/证明（较难）
**题目**：根据无套利原理，利用伊藤引理推导零息债券价格 $P(t, r)$ 满足的衍生品基本偏微分方程 (PDE)。

> [!question]- 答案解析
> **解析**：
> 1. 根据 Itô 引理，债券价格 $P(t, r_t)$ 的微分为：
>    $$dP = \left( \frac{\partial P}{\partial t} + \kappa(\theta - r) \frac{\partial P}{\partial r} + \frac{1}{2} \sigma^2 \frac{\partial^2 P}{\partial r^2} \right) dt + \sigma \frac{\partial P}{\partial r} dW_t$$
> 2. 构造无套利组合，要求组合的期望收益率等于无风险短利率 $r_t$：
>    $$\frac{\partial P}{\partial t} + \kappa(\theta - r) \frac{\partial P}{\partial r} + \frac{1}{2} \sigma^2 \frac{\partial^2 P}{\partial r^2} - r P = 0$$
> 3. 带入边界条件 $P(T, T) = 1.0$，解此二阶线性 PDE 即可推导出解析解 $P(t, T) = A(t, T) e^{-B(t, T) r}$，证毕！  
> **Obsidian 标签**：`#自测题/债券PDE证明`

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
- **建议双链**：[[国债逆回购 (Treasury Reverse Repo)|国债逆回购]]、[[同业存单 (Negotiable Certificate of Deposit, NCD)|同业存单]]、[[Black-Scholes]]、[[实盘风控]]
- **标签**：`#学习` `#量化金融` `#固收` `#收益率曲线` `#Vasicek` `#HullWhite` `#短利率` `#均值回归`

---

<!-- quant-evidence-v3 -->
## 可定位依据与失效复核

本卡的复核对象是 **利率期限结构与短利率单因子模型 (Yield Curve & Short Rate Models: Vasicek & Hull-White)**，而不是只复述一个公式。对 **利率期限结构与短利率单因子模型 (Yield Curve & Short Rate Models: Vasicek & Hull-White)** 的独立验证重点是：先统一日计数与复利约定，再用零息债重定价误差检验曲线插值和短利率校准。

### 权威来源与定位

1. 美国财政部官方收益率曲线方法：https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics/treasury-yield-curve-methodology。用于复核“先统一日计数与复利约定，再用零息债重定价误差检验曲线插值和短利率校准”。
2. Basel Committee 证券化框架与 STC 标准：https://www.bis.org/bcbs/publ/d374.htm。用于复核“先统一日计数与复利约定，再用零息债重定价误差检验曲线插值和短利率校准”。
3. Frank J. Fabozzi、Steven V. Mann 与 Francesco Fabozzi, *The Handbook of Fixed Income Securities*, 9th ed., McGraw Hill, ISBN 9781260473896；按目录定位 yield curve、asset-backed securities 与 structured products 主题。用于复核“先统一日计数与复利约定，再用零息债重定价误差检验曲线插值和短利率校准”。

### 失效边界与验收协议

- **成立条件**：先写清数据时点、估计窗口、交易摩擦和分布/市场结构假设，再运行模型。
- **反例压力测试**：先统一日计数与复利约定，再用零息债重定价误差检验曲线插值和短利率校准。
- **最小实验**：固定随机种子或冻结原始数据快照，同时保存基线、破坏条件后的对照组、关键中间量与失败日志。
- **通过标准**：结论必须在样本外仍保持方向一致；若成本、延迟、参数扰动或结构突变使结论反转，就把该情形登记为适用边界而不是删除失败结果。
