---
title: Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)
date: 2026-07-23
type: concept
course: 量化金融
importance: A
tags:
- 学习
- 量化金融
- 算法交易
- 最优执行
- AlmgrenChriss
- 变分法
- 市场冲击
- 持仓风险
- 冲击成本
upstream:
- '[[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型|Implementation Shortfall]]'
- '[[市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)|冲击成本模型]]'
downstream:
- '[[VWAP 成交量加权平均价格 (Volume-Weighted Average Price)|VWAP]]'
- '[[TWAP 时间加权平均价格 (Time-Weighted Average Price)|TWAP]]'
status: learning
---
# Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)

---

## 0. 先判断它值不值得深挖

**分类：A 类（核心概念，必须深挖）**

**理由：**
Almgren-Chriss 最优执行模型（由 Robert Almgren 与 Neil Chriss 于 2000 年发表在 *Journal of Risk* 上的开创性论文阐述）是现代算法交易（Algorithmic Trading）与 Implementation Shortfall (IS) 拆单算法的**最高数学基石**。在交易大单时，交易员面临着永恒的权衡：**卖得太快，临时市场冲击 (Temporary Impact) 太大砸塌股价；卖得太慢，持仓暴露在未知的市场波动风险 (Volatility Risk) 中**。Almgren-Chriss 模型利用变分法（Calculus of Variations）与欧拉-拉格朗日方程 (Euler-Lagrange Equation)，首次推导出了平衡市场冲击与波动率风险的最优指数衰减持仓轨迹 $x(t)$ 的闭式解析解。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**

假设你需要在一天的交易时间内清仓 100 万股某股票（初始持仓 $X_0 = 1,000,000$）。
- **极端策略 A（瞬间清仓）**：你在第 1 秒钟把 100 万股砸向盘口。市场被你瞬间砸塌，跌幅高达 5%，产生了极具毁灭性的**市场冲击成本 (Impact Cost)**；
- **极端策略 B（均速极慢清仓）**：你把 100 万股平均分摊到全天 6.5 小时里的每一秒卖出。虽然每秒砸盘很轻微，但盘中突发大盘大跌，你的剩余股票全被套死在半山腰，产生了巨大的**持仓市场风险 (Volatility Risk)**。

**以前的方法在哪里卡住：**
缺乏一个统一的效用函数（Utility Function）与数学工具，无法定量计算“究竟以怎样的速度卖出，才能使‘市场冲击损益 + 持仓方差风险’的总惩罚最小”。

**为什么必须引入 Almgren-Chriss 最优执行模型：**
构建显式包含**永久市场冲击 $\gamma$、临时市场冲击 $\eta$ 和风险厌恶系数 $\lambda$** 的均值-方差目标函数，导出最佳变分轨迹 $x_j$。

**它到底解决了哪类问题：**
解决了**如何科学推导大单拆分最佳执行速度 $v(t)$、在冲击成本与市场风险之间取得数学最优化平衡**的问题。

---

## 2. 为什么它重要？它有什么用？

- **体系与大图景**：算法交易与执行（第四阶段）的数学核心，直接为 Implementation Shortfall (IS) 算法、VWAP/TWAP 的偏离优化提供基准轨迹。
- **量化与实战应用**：
  1. **IS 拆单算法的执行发动机**：根据交易员的风险厌恶程度 $\lambda$，动态调整拆单是呈“前重后轻的指数衰减轨迹”还是“平缓匀速轨迹”。
  2. **评估大单清仓的最优持有期 $T^*$**：计算最佳清仓时间天数。

---

## 3. 学它之前需要哪些前置知识？

1. **[[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型|Implementation Shortfall]]**：理解执行缺失 (IS) 概念（决策价格与最终执行均价的差额）。
2. **[[市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)|冲击成本模型]]**：理解永久冲击（影响全市场均衡价）与临时冲击（当期盘口流动性消耗）。
3. **最小必要背景（二阶常系数齐次微分方程）**：
   > 形式：$x''(t) - \kappa^2 x(t) = 0$ 的通解为：
   > $$x(t) = C_1 \cosh(\kappa t) + C_2 \sinh(\kappa t) \quad \text{或} \quad C_1 e^{\kappa t} + C_2 e^{-\kappa t}$$

---

## 4. 用直觉语言解释它

### 生活类比：火灾逃生中的拥挤踩踏 vs 浓烟吸入

- 假设你所在的高楼发生火灾，有 1000 个人（100 万股）需要从安全通道撤离：
  - **撤离太急（瞬间砸盘）**：所有人同时挤向门口，产生严重的**踩踏事故（临时市场冲击 $\eta$）**；
  - **撤离太慢（慢吞吞卖）**：大家排队慢慢走，虽然不踩踏了，但后排的人会被**浓烟呛死（市场波动风险 $\lambda \sigma^2$）**。
- **Almgren-Chriss 模型** 就像：一位超级指挥官。
  - 他计算出了最完美的撤离速度曲线：**一开始趁火势刚起快速撤离大部分人（前期快速卖出），随后逐渐平缓（后期指数衰减）**。
  - 如果风大烟浓（波动率 $\sigma^2$ 大或风险厌恶 $\lambda$ 高），指挥官就命令一开始撤得更快一些！

**Almgren-Chriss 的直觉本质**：
在“快卖引发的踩踏成本”与“慢卖承受的火灾风险”之间，寻找一条让总伤害最小的指数衰减撤离轨迹。

«“Almgren-Chriss 模型就是推导出一条‘前快后慢’的指数曲线，让你在避免砸塌市场的同时，最快速度逃离股票下跌的火场。”»

---

## 5. 正式定义、核心公式、符号解释

### 核心定义
**Almgren-Chriss 最优执行模型**：在离散或连续时间框架下，假设股票价格服从包含线性永久冲击与线性临时冲击的算术布朗运动。交易员寻求一条持仓轨迹 $x(t)$（初始 $x(0) = X$，最终 $x(T) = 0$），以最小化期望执行缺失 $E[x]$ 与方差风险 $V[x]$ 的加权组合（目标函数 $U[x] = E[x] + \lambda V[x]$）。

### 核心公式与轨迹推导结果

#### 1. 价格演化与市场冲击假设 (Continuous Formulation)
在时间 $t \in [0, T]$，交易速度 $v(t) = -\frac{dx(t)}{t}$。
股票价格 $S(t)$ 演化为：
$$S(t) = S_0 + \sigma W(t) - \gamma (X - x(t))$$
实际卖出执行价格 $\tilde{S}(t)$ 包含临时冲击：
$$\tilde{S}(t) = S(t) - \eta v(t) = S(t) + \eta \frac{dx(t)}{dt}$$

#### 2. 目标函数 (Mean-Variance Utility)
期望执行缺失 $E[x]$ 与方差 $V[x]$ 为：
$$E[x] = \frac{1}{2} \gamma X^2 + \eta \int_0^T \left(\frac{dx}{dt}\right)^2 dt$$
$$V[x] = \sigma^2 \int_0^T x(t)^2 dt$$
最小化目标函数：
$$\min_{x(t)} U[x] = \int_0^T \left[ \eta \left(\frac{dx}{dt}\right)^2 + \lambda \sigma^2 x(t)^2 \right] dt + \frac{1}{2} \gamma X^2$$

#### 3. 欧拉-拉格朗日方程与最优持仓轨迹 $x(t)$ 闭式解
对泛函施加变分求导，导出二阶微分方程：
$$\eta \frac{d^2 x}{dt^2} - \lambda \sigma^2 x(t) = 0 \implies \frac{d^2 x}{dt^2} = \kappa^2 x(t)$$
其中**急迫度参数 (Urgency Parameter)**：
$$\kappa = \sqrt{\frac{\lambda \sigma^2}{\eta}}$$
结合边界条件 $x(0) = X, x(T) = 0$，解得**最优持仓轨迹**：

$$x(t) = X \cdot \frac{\sinh(\kappa (T - t))}{\sinh(\kappa T)}$$

### 符号解释表

| 符号 | 含义 | 维度/量纲 | 备注与要求 |
| :--- | :--- | :--- | :--- |
| $X$ | 初始待卖出总持仓 | 股数 (如 $1,000,000$) | $x(0) = X, x(T) = 0$ |
| $\eta$ | **临时市场冲击系数** | 元/(股/秒) | 交易速度越快，临时吃价越严重 |
| $\gamma$ | 永久市场冲击系数 | 元/股 | 永久改变均衡价格，与速度无关 |
| $\sigma$ | 标的资产波动率 | 元/$\sqrt{\text{秒}}$ | 波动率越大，越想快速卖出 |
| $\lambda$ | **风险厌恶系数 (Risk Aversion)** | 标量 | $\lambda \to \infty$ 变为瞬间清仓，$\lambda \to 0$ 变为 TWAP 匀速 |
| $\kappa$ | **急迫度系数 (Urgency)** | $1/\text{秒}$ | $\kappa = \sqrt{\frac{\lambda \sigma^2}{\eta}}$，决定曲线弯曲度 |

---

## 6. 推导思路和思想来源

### 为什么最优轨迹 $x(t)$ 是“前快后慢”的双曲正弦 $\sinh$ / 指数衰减曲线？
1. **初期阶段 ($t \to 0$)**：
   此时剩余持仓 $x(t)$ 非常大（接近 $X$）。根据 $V[x] = \sigma^2 \int x(t)^2 dt$，大持仓暴露在波动率下的方差风险极为恐怖！因此在初期必须**以极快的速度卖出（牺牲一部分临时冲击成本 $\eta$），迅速降低持仓头寸**。
2. **后期阶段 ($t \to T$)**：
   当持仓已经被砍到了很小的数量（如剩 5%），方差风险已经微乎其微。此时主导风险变成了临时冲击，因此可以**放慢速度平缓卖出**。
3. **极值边界**：
  - 当风险极度厌恶 ($\lambda \to \infty$ 或 $\kappa \to \infty$) 时：$\sinh$ 曲线弯曲到极致，表现为**开盘瞬间全部卖光**；
  - 当风险中性 ($\lambda \to 0$ 或 $\kappa \to 0$) 时：$\lim_{\kappa \to 0} \frac{\sinh(\kappa(T-t))}{\sinh(\kappa T)} = 1 - \frac{t}{T}$，**退化为完全平直的 TWAP 匀速卖出轨迹！**

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算例题（风险中性下的 TWAP 退化手算）

**题目**：
某交易员待卖出 $X = 100,000$ 股，交易总时间 $T = 5$ 小时。
假设该交易员是风险中性的（$\lambda = 0$，不介意市场波动风险）。
写出其 Almgren-Chriss 最优持仓轨迹 $x(t)$ 及每小时卖出股数。

**解答过程**：
1. 当 $\lambda = 0$ 时，急迫度 $\kappa = \sqrt{\frac{0 \cdot \sigma^2}{\eta}} = 0$。
2. 轨迹退化为线性 TWAP 方程：
   $$x(t) = X \left(1 - \frac{t}{T}\right) = 100,000 \left(1 - \frac{t}{5}\right)$$
3. 卖出速度 $v(t) = -\frac{dx}{dt} = \frac{X}{T} = \frac{100,000}{5} = 20,000 \text{ 股/小时}$。
4. **结论**：在风险中性（仅追求冲击成本最小化）时，Almgren-Chriss 的最优解答就是匀速 TWAP，每小时平稳卖出 20,000 股！

---

### 例子 2：中等例题（根据急迫度 $\kappa$ 计算中间时刻的持仓量）

**题目**：
初始持仓 $X = 1,000,000$ 股，交易时间 $T = 1$ 天。
由于市场波动剧烈，算得急迫度参数 $\kappa = 2.0$。
已知 $\sinh(2.0) \approx 3.6269$，$\sinh(1.0) \approx 1.1752$。
求交易进行到一半时间（$t = 0.5$ 天）时，剩余的最佳持仓 $x(0.5)$ 以及已经卖出的比例。

**解答过程**：
1. 代入 Almgren-Chriss 持仓公式：
   $$x(0.5) = X \cdot \frac{\sinh(\kappa (T - 0.5))}{\sinh(\kappa T)} = 1,000,000 \times \frac{\sinh(2.0 \times 0.5)}{\sinh(2.0 \times 1.0)}$$
   $$x(0.5) = 1,000,000 \times \frac{\sinh(1.0)}{\sinh(2.0)} = 1,000,000 \times \frac{1.1752}{3.6269} \approx 324,023 \text{ 股}$$
2. 计算已卖出比例：
   $$\text{已卖出比例} = 1 - \frac{324,023}{1,000,000} = 1 - 32.4\% = 67.6\%$$
3. **结论**：在时间仅过去了一半（50%）时，由于高急迫度 $\kappa = 2.0$，算法已经在前半程快速卖出了 **67.6% 的持仓**！

---

### 例子 3：实际应用（Python 绘制不同风险厌恶系数 $\lambda$ 下的 Almgren-Chriss 最优执行轨迹）

```python
import numpy as np
import matplotlib.pyplot as plt

def almgren_chriss_trajectory(X0, T, eta, sigma, risk_aversion_lambda, N_steps=100):
    t_grid = np.linspace(0, T, N_steps)
    if risk_aversion_lambda == 0:
        x_t = X0 * (1.0 - t_grid / T)
    else:
        kappa = np.sqrt(risk_aversion_lambda * (sigma**2) / eta)
        x_t = X0 * np.sinh(kappa * (T - t_grid)) / np.sinh(kappa * T)
    return t_grid, x_t

# 模拟卖出 1,000,000 股，时间 1 天，临时冲击 \eta=1e-6, 波动率 \sigma=0.02
X0, T, eta, sigma = 1000000, 1.0, 1e-6, 0.02

t_grid, x_risk_neutral = almgren_chriss_trajectory(X0, T, eta, sigma, risk_aversion_lambda=0)
t_grid, x_moderate     = almgren_chriss_trajectory(X0, T, eta, sigma, risk_aversion_lambda=1e-5)
t_grid, x_aggressive   = almgren_chriss_trajectory(X0, T, eta, sigma, risk_aversion_lambda=1e-4)

print("=== Almgren-Chriss 最优持仓轨迹计算 (t=0.5 时刻) ===")
print(f"风险中性 (\\lambda=0, TWAP匀速):    剩余持仓 {x_risk_neutral[50]:.0f} 股 (已卖出 50.0%)")
print(f"适度风险厌恶 (\\lambda=1e-5):       剩余持仓 {x_moderate[50]:.0f} 股 (已卖出 {(1-x_moderate[50]/X0)*100:.1f}%)")
print(f"极度风险厌恶 (\\lambda=1e-4, 前快): 剩余持仓 {x_aggressive[50]:.0f} 股 (已卖出 {(1-x_aggressive[50]/X0)*100:.1f}%)")
```

---

## 7.5 💥 课本挂载与工业级实战模块 (Textbook Mapping & Production Lab)

### 7.5.1 📚 经典课本章节锚定
- **教材挂载 1**：Barry Johnson *《Algorithmic Trading and DMA》* 第 10 章 "Optimal Execution Algorithms" Section 10.3 "Almgren-Chriss Framework"。
  - **课本必读重点**：离散时间与连续时间框架推导、Efficient Frontier of Execution（执行有效前沿）、临时与永久冲击分解。
  - **推荐课后计算**：Johnson Ch 10 Ex 10.4, 10.7（计算给定 $\lambda$ 下的绝对执行缺失期望 $E[x]$）。
- **教材挂载 2**：Robert Almgren & Neil Chriss (2000) 论文 *"Optimal Execution of Portfolio Transactions"* (Journal of Risk).
  - **实战挂载重点**：利用 Euler-Lagrange 方程从变分法导出微分方程 $\frac{d^2 x}{dt^2} = \kappa^2 x$。

### 7.5.2 ⚙️ 工业级 Python 最小可运行实战脚手架
（见上方 例子 3 完整代码）

### 7.5.3 ⚠️ 实盘落地“踩坑指南”与回测陷阱
1. **假设临时冲击为线性 ($\eta v$) 的局限**：
   Almgren-Chriss 假设临时冲击与交易速度 $v$ 成线性正比。但在实际盘口中，根据 Square-Root Law（平方根法则），**临时冲击通常是速度的方根函数 $\eta v^{0.5}$**。这会导致非线性 AC 模型需要改用数值迭代求解。
2. **日内成交量 U 型 Profile 忽略**：
   标准 AC 模型假设日内流动性 $\eta$ 是恒定的。工业界做法是结合 **日内 Volume Profile**（如早盘/尾盘流动性大，午间小），将时间 $t$ 转换为“流动性调整时间 (Liquidity-Adjusted Time)”。

### 7.5.4 📊 实战性能评估指标体系
- **执行有效前沿 (Execution Efficient Frontier)**：在 $E[IS] - V[IS]$ 坐标系中绘制不同 $\lambda$ 的前沿曲线。
- **急迫度参数 $\kappa$**：$\kappa = \sqrt{\frac{\lambda \sigma^2}{\eta}}$。
- **IS 相对 TWAP 改善幅度 (IS Improvement)**：$\frac{\text{IS}_{TWAP} - \text{IS}_{AC}}{\text{IS}_{TWAP}}$。

### 7.5.5
> 🔓 **作业解锁前置条件**：学完 [[买卖价差及其微观结构拆解 (Bid-Ask Spread & Microstructure Decomposition)|买卖价差]] + [[市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)|冲击成本模型]] + [[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型|Implementation Shortfall]] + [[Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)|Almgren-Chriss最优执行轨迹推导]] 即可正式解锁本 Challenge 实战！
> 💡 **解锁指引**：理解市场冲击与执行缺口 (IS) 后即可解锁变分法 Euler-Lagrange 方程求解。

 🧪 拓展实验与李宏毅式实战 Challenge 题 (HW13-变分法推导与 Almgren-Chriss 最优拆单轨迹)

本作业参考 **李宏毅 (Hung-yi Lee) 教授 ML 课程作业架构** 设计，设置四个渐进式难度基线 (Baselines)：

- 🟢 **简单基线 (Simple Baseline)**：
  - **任务要求**：手算急迫度参数 $\kappa = \sqrt{\frac{\lambda \sigma^2}{\eta}}$，求解风险中性 ($\lambda=0$) 下的 TWAP 匀速轨迹。
  - **达标标准**：代码无 Error 跑通，输出基础结果。

- 🟡 **中等基线 (Medium Baseline)**：
  - **任务要求**：使用 Python 实现 Almgren-Chriss 双曲正弦持仓轨迹 $x(t) = X \frac{\sinh(\kappa(T-t))}{\sinh(\kappa T)}$，绘制不同 $\lambda$ 下的持仓曲线。
  - **达标标准**：完成核心算法的向量化与参数校准，模型表现达到基线水平。

- 🔴 **强基线 (Strong Baseline)**：
  - **任务要求**：利用欧拉-拉格朗日变分方程完整推导 AC 二阶微分方程 $x''(t) = \kappa^2 x(t)$，并绘制执行有效前沿 (Execution Efficient Frontier)。
  - **达标标准**：扣除交易摩擦与滑点后，样本外 (OOS) 夏普比率 $> 1.8$ 或评估指标提升 20% 以上。

- 🟣 **Boss 基线 (Kaggle / 实盘级基线)**：
  - **任务要求**：结合真实日内成交量 U 型 Volume Profile，将 AC 模型扩展为连续非线性平方根冲击模型（Square-Root Law），实现百亿资金清仓滑点降低 15 BP。
  - **达标标准**：代码具备极强泛化性与抗过拟合能力，通过 PBO 审计且过拟合概率 $\text{PBO} < 10\%$。


## 8. 常见误区和易混概念

### 误区 1：Almgren-Chriss 导出的指数衰减轨迹在任何市场环境下都一定比匀速 TWAP 更好

错误直觉：“AC 模型是高级数学推导出来的，肯定全面碾压死板的 TWAP。”  
为什么错：如果市场波动率极低（$\sigma \to 0$）或者交易员完全不介意隔夜风险（$\lambda = 0$），AC 模型的解就会恰好退化为 TWAP！在低波动小单场景下，强行用 AC 前期暴砸反倒会产生过度的临时冲击。  
正确理解：**TWAP 是 AC 模型在风险中性（$\lambda = 0$）时的特例。**

### 概念对比：VWAP 算法 vs TWAP 算法 vs Almgren-Chriss (IS) 算法

| 维度 | VWAP 算法 | TWAP 算法 | Almgren-Chriss (IS) 算法 |
| :--- | :--- | :--- | :--- |
| **基准 Benchmark** | 全天成交量加权均价 | 全天算术时间均价 | **决策时刻价格 $S_0$ (Implementation Shortfall)** |
| **拆单轨迹依据** | 日内历史成交量 Profile | 时间均匀切分 ($\frac{dx}{dt} = C$) | **变分推导的最优指数衰减 $x(t) \propto \sinh$** |
| **核心驱动因子** | 预测日内成交量 U 型 | 纯时间计数 | **波动率 $\sigma$、冲击 $\eta$ 与风险厌恶 $\lambda$** |
| **适合场景** | 大单贴近全天均价 | 缺乏 Volume 数据时 | **高 Alpha 衰减、防范大跌风险的强目的性拆单** |

---

## 9. 相关知识点与 Obsidian 双链建议

请帮我建立知识网络。

注意：不要只列链接。每个链接后面必须用一句话说明“为什么要链接”。

上游依赖

- [[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型|Implementation Shortfall]]：提供基础概念与理论推导支撑。
- [[市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)|冲击成本模型]]：提供基础概念与理论推导支撑。

下游延伸

- [[VWAP 成交量加权平均价格 (Volume-Weighted Average Price)|VWAP]]：进一步延伸拓展该知识点的应用场景与模型构建。
- [[TWAP 时间加权平均价格 (Time-Weighted Average Price)|TWAP]]：进一步延伸拓展该知识点的应用场景与模型构建。

横向关联

- [[收益率与对数收益率]]：衡量资产收益特性的基础量纲。
- [[实盘风控]]：风险控制与投资组合保护。

应用场景

- [[实盘风控]]：工业级量化策略风控与组合风险度量。


## 10. 闭卷复现任务

1. [ ] 默写 Almgren-Chriss 最优持仓轨迹公式 $x(t) = X \frac{\sinh(\kappa(T-t))}{\sinh(\kappa T)}$。
2. [ ] 用“火灾逃生中的拥挤踩踏与浓烟吸入”解释 AC 模型的直觉。
3. [ ] 默写急迫度系数 $\kappa = \sqrt{\frac{\lambda \sigma^2}{\eta}}$ 的公式。
4. [ ] 解释当风险厌恶 $\lambda \to 0$ 时，AC 轨迹为何会退化为 TWAP 匀速轨迹。
5. [ ] 比较永久市场冲击 $\gamma$ 与临时市场冲击 $\eta$ 的本质区别。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 急迫度系数 $\kappa$ 与波动率 $\sigma$ 的关系 |
| 2 | 公式运用 | 基础 | 风险中性 $\lambda=0$ 下计算前 2 小时卖出比例 |
| 3 | 条件判断 | 中等 | 波动率 $\sigma$ 暴增时 AC 轨迹弯曲方向 |
| 4 | 变式/综合 | 中等 | 永久冲击 $\gamma$ 为什么不影响最佳拆单轨迹形状 |
| 5 | 开放/证明 | 较难 | 利用欧拉-拉格朗日方程从目标泛函 $\min \int [\eta (x')^2 + \lambda \sigma^2 x^2] dt$ 推导 $x'' = \kappa^2 x$ |

---

### 第 1 题：概念辨析（基础）
**题目**：在 Almgren-Chriss 模型中，急迫度系数 $\kappa = \sqrt{\frac{\lambda \sigma^2}{\eta}}$。当标的股票波动率 $\sigma$ 暴增时，$\kappa$ 会如何变化？持仓卖出轨迹会变得更前倾（卖更快）还是更平缓？

> [!question]- 答案解析
> **答案**：
> 1. $\sigma$ 增加会导致急迫度 $\kappa$ **增大**。
> 2. 轨迹会变得**更加前倾（前期卖出速度显著加快）**，因为高波动率意味着持仓风险暴露剧增，算法选择在前期忍受更大的冲击成本以尽快消灭持仓风险。  
> **Obsidian 标签**：`#自测题/AC急迫度`

---

### 第 2 题：公式运用（基础）
**题目**：待卖出 $X = 60,000$ 股，总时间 $T = 6$ 小时。若风险厌恶 $\lambda = 0$，求前 2 小时累积卖出股数。

> [!question]- 答案解析
> **答案**：
> 当 $\lambda = 0$ 时，轨迹为匀速 TWAP：
> 每小时卖出 $\frac{60,000}{6} = 10,000$ 股。
> 前 2 小时累积卖出 $10,000 \times 2 = 20,000$ 股。  
> **Obsidian 标签**：`#自测题/TWAP手算`

---

### 第 3 题：条件判断（中等）
**题目**：判断：“在 Almgren-Chriss 目标函数中，永久市场冲击系数 $\gamma$ 决定了持仓轨迹 $x(t)$ 的弯曲形状。”

> [!question]- 答案解析
> **答案**：错误。在 AC 模型中，永久市场冲击产生的期望总损失为 $\frac{1}{2} \gamma X^2$，这是一个只与初始持仓 $X$ 相关的**死常数**，其对 $x(t)$ 的求导变分为 0。决定轨迹弯曲形状的只有**临时冲击系数 $\eta$、波动率 $\sigma$ 与风险厌恶 $\lambda$**（即 $\kappa = \sqrt{\lambda \sigma^2 / \eta}$）。  
> **Obsidian 标签**：`#自测题/永久冲击独立性`

---

### 第 4 题：变式/综合（中等）
**题目**：简述什么是执行有效前沿 (Execution Efficient Frontier)。

> [!question]- 答案解析
> **答案**：
> 在以期望执行缺失 $E[IS]$ 为横轴、执行方差 $V[IS]$ 为纵轴的坐标系中，通过变动风险厌恶系数 $\lambda \in [0, \infty)$ 计算出的一系列最优轨迹所对应的 $(E[IS], V[IS])$ 闭合抛物线前沿。它代表在给定风险水平下所能达到的最小期望执行成本。  
> **Obsidian 标签**：`#自测题/执行有效前沿`

---

### 第 5 题：开放/证明（较难）
**题目**：利用变分法（Calculus of Variations）与欧拉-拉格朗日方程，推导 AC 模型的二阶微分方程 $\frac{d^2 x}{dt^2} = \kappa^2 x$。

> [!question]- 答案解析
> **解析**：
> 1. 设目标泛函 $J[x] = \int_0^T L(t, x, x') dt$，其中拉格朗日量 $L(t, x, x') = \eta (x')^2 + \lambda \sigma^2 x^2$（记 $x' = \frac{dx}{dt}$）。
> 2. 欧拉-拉格朗日极值条件方程为：
>    $$\frac{\partial L}{\partial x} - \frac{d}{dt} \left( \frac{\partial L}{\partial x'} \right) = 0$$
> 3. 分别计算偏导数：
>    $$\frac{\partial L}{\partial x} = 2 \lambda \sigma^2 x, \quad \frac{\partial L}{\partial x'} = 2 \eta x' \implies \frac{d}{dt}\left( \frac{\partial L}{\partial x'} \right) = 2 \eta x''$$
> 4. 代入方程：
>    $$2 \lambda \sigma^2 x - 2 \eta x'' = 0 \implies \eta x'' = \lambda \sigma^2 x \implies x'' = \left(\frac{\lambda \sigma^2}{\eta}\right) x$$
> 5. 令 $\kappa^2 = \frac{\lambda \sigma^2}{\eta}$，得 $x''(t) - \kappa^2 x(t) = 0$，证毕！  
> **Obsidian 标签**：`#自测题/AC变分推导`

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

- **适合文件夹**：`02-Knowledge/🧠 学习系统/03-量化金融/04-深入精通/`
- **建议双链**：[[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型|Implementation Shortfall]]、[[市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)|冲击成本模型]]、[[VWAP 成交量加权平均价格 (Volume-Weighted Average Price)|VWAP]]、[[TWAP 时间加权平均价格 (Time-Weighted Average Price)|TWAP]]
- **标签**：`#学习` `#量化金融` `#算法交易` `#最优执行` `#AlmgrenChriss` `#变分法` `#冲击成本` `#

---

<!-- quant-evidence-v3 -->
## 可定位依据与失效复核

本卡的复核对象是 **Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)**，而不是只复述一个公式。对 **Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)** 的独立验证重点是：区分永久冲击和临时冲击，并用参与率、波动率与风险厌恶系数做敏感性网格。

### 权威来源与定位

1. Almgren 与 Chriss (2001), *Optimal Execution of Portfolio Transactions*, DOI: 10.21314/JOR.2001.041。用于复核“区分永久冲击和临时冲击，并用参与率、波动率与风险厌恶系数做敏感性网格”。
2. Perold (1988), *The Implementation Shortfall: Paper versus Reality*, DOI: 10.3905/jpm.1988.409150。用于复核“区分永久冲击和临时冲击，并用参与率、波动率与风险厌恶系数做敏感性网格”。
3. Joel Hasbrouck, *Empirical Market Microstructure*, Oxford University Press, ISBN 9780195301649, Chapter 3 与 Chapter 5（价差、冲击和执行测量）。用于复核“区分永久冲击和临时冲击，并用参与率、波动率与风险厌恶系数做敏感性网格”。

### 失效边界与验收协议

- **成立条件**：先写清数据时点、估计窗口、交易摩擦和分布/市场结构假设，再运行模型。
- **反例压力测试**：区分永久冲击和临时冲击，并用参与率、波动率与风险厌恶系数做敏感性网格。
- **最小实验**：固定随机种子或冻结原始数据快照，同时保存基线、破坏条件后的对照组、关键中间量与失败日志。
- **通过标准**：结论必须在样本外仍保持方向一致；若成本、延迟、参数扰动或结构突变使结论反转，就把该情形登记为适用边界而不是删除失败结果。
