---
title: 蒙特卡洛模拟法 VaR (Monte Carlo Simulation VaR)
type: study
topic: Monte Carlo VaR
created: '2026-08-06'
status: ongoing
difficulty: intermediate
course: 量化金融
importance: A
tags:
- 学习
- 量化金融
concept: []
prerequisites: []
related: []
upstream: null
downstream: null
date: 2026-07-23
kind: concept
flow: knowledge
source: 本课程历史知识卡；原始来源 [待验证]
source_url: https://www.bis.org/basel_framework/chapter/MAR/33.htm。用于复核“固定随机种子并报告抽样误差，使用相关冲击和厚尾创新做分布敏感性测试”。
accessed: '2026-08-06'
license: link-only；正文为本地学习整理
assessment_exempt: false
---

# Monte Carlo VaR

---

## 0. 先判断它值不值得深挖

**分类：A 类（核心概念，必须深挖）**

**理由：**
蒙特卡洛模拟法 VaR（Monte Carlo Simulation VaR）被称为风险管理的“终极武器”。当投资组合中包含了具有强路径依赖性（Path-dependent）的奇异期权（如障碍期权 Barrier Option、亚式期权 Asian Option）、或者资产收益率呈现极其复杂的随机跳跃（Jump-Diffusion）与随机波动率（Heston Model）时，参数法和历史模拟法均告失效。蒙特卡洛模拟通过计算机生成数万甚至数百万条未来可能的随机资产价格演化路径，为任意复杂金融工程组合提供绝对精准的数值 VaR 解。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**

假设你的对冲基金持有一个复杂的雪球结构衍生品（Snowball Option）或障碍看跌期权组合。
该期权规定：在未来 1 年内，只要标的价格跌破 80 元（敲入障碍 Knock-in），期权的收益模式会瞬间从固定年化 15% 变成全额承担股票下跌亏损！
如果你用参数法（Greeks 线性近似），或者用历史模拟法（过去数据没发生过敲入），你的风控系统会给出“风险极低”的假象。**一旦标的跌破 80 元，组合会发生非线性的灾难性断崖爆仓。**

**以前的方法在哪里卡住：**
1. **参数法 (Delta-Normal)**：假设期权损益与标的价格呈线性关系，在障碍敲入/敲出这类非连续断崖处完全失效。
2. **历史模拟法**：受限于过去的死数据，无法推演历史上未曾发生过、但理论上可能发生的未来复杂路径组合。

**为什么必须引入蒙特卡洛 VaR：**
设定随机过程（如带跳跃的随机微分方程 SDE），用伪随机数生成器在计算机中模拟 $M = 100,000$ 种未来平行宇宙中资产价格的完整演化轨迹，对每条轨迹精确重新定价，得出未来的概率分布。

**它到底解决了哪类问题：**
解决了**包含复杂路径依赖衍生品、非线性凸性头寸以及自定义复杂随机过程组合的无死角风险度量**问题。

---

## 2. 为什么它重要？它有什么用？

- **体系与大图景**：风控三大 VaR 方法（参数法、历史模拟法、蒙特卡洛法）中理论上限最高、适用面最广的框架。
- **量化与实战应用**：
  1. **复杂场外衍生品 (OTC Derivatives) 风险管理**：为结构化票据（Autocallable / Snowball）、奇异期权库计算全生命周期 VaR。
  2. **多因子随机波动率 (Stochastic Volatility) 建模**：支持结合 Heston 模型的波动率随机漂移计算极端风控限额。

---

## 3. 学它之前需要哪些前置知识？

1. **[[Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)|Black-Scholes]]**：理解标的资产价格服从几何布朗运动 (Geometric Brownian Motion, GBM)。
2. **[[历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)|历史模拟VaR]]**：理解 VaR 分位数提取与模拟损益排序。
3. **最小必要背景（几何布朗运动离散化）**：
   $$S_{t+\Delta t} = S_t \exp\left( (r - \frac{1}{2}\sigma^2)\Delta t + \sigma \sqrt{\Delta t} Z_t \right)$$
   其中 $Z_t \sim N(0, 1)$ 为标准正态伪随机数。

---

## 4. 用直觉语言解释它

### 生活类比：平行宇宙模拟器与沙盘推演

- 假设你是一名军事指挥官，准备部署一场复杂的战役（建立衍生品组合）。
- 你有一台**超级计算机平行宇宙模拟器（蒙特卡洛引擎）**：
  - 你按下按钮，模拟器瞬间在计算机里推演了 **100,000 场平行战役**。
  - 在第 1 场，天气晴朗（股价大涨），你赢了；
  - 在第 8,500 场，突然刮起暴风雪且遭遇桥梁断裂（触发障碍敲入），你损失惨重。
- 模拟结束后，你把这 100,000 场战役的最终输赢结果从最惨到最好排个序。
  看最惨的那 5,000 场（5% 最坏结局）里，最轻的那个损失是多少——这就是你的蒙特卡洛 VaR！

**蒙特卡洛 VaR 的直觉本质**：
用计算机掷数十万次硬币，在虚拟世界里穷尽未来所有可能的平行宇宙结局，从倒数分位数中抓出最大风险。

«“蒙特卡洛 VaR 就是用电脑在虚拟世界里运行 10 万个平行宇宙，直接在结局库里按概率抓出最惨的亏损。”»

---

## 5. 正式定义、核心公式、符号解释

### 核心定义
**蒙特卡洛模拟法 VaR (Monte Carlo VaR)**：指显式假定标的资产价格服从特定的连续时间随机过程，利用伪随机数生成器产生大量（如 $M = 100,000$）标的资产未来价格的演化路径，计算资产组合在每条路径末端的期权与现货价值，进而构建理论损益分布，并提取指定置信水平 $(1-\alpha)$ 对应的 VaR 的数值模拟方法。

### 核心公式

#### 1. 几何布朗运动 (GBM) 路径生成递推公式
对每条模拟路径 $m \in \{1, 2, \dots, M\}$，在时间步 $k \in \{1, 2, \dots, N\}$：
$$S_{k, m} = S_{k-1, m} \cdot \exp\left( (\mu - \frac{1}{2} \sigma^2) \Delta t + \sigma \sqrt{\Delta t} \epsilon_{k, m} \right)$$
其中 $\epsilon_{k, m} \sim N(0, 1)$ 为独立同分布的标准正态伪随机数。

#### 2. 多资产相关性 Cholesky 分解 (处理资产间相关性)
若 $K$ 个资产间存在相关系数矩阵 $\mathbf{R}$，先求 Cholesky 下三角分解 $\mathbf{R} = \mathbf{L} \mathbf{L}^T$。
将独立随机数向量 $\mathbf{Z} \sim N(\mathbf{0}, \mathbf{I})$ 转换为**相关随机数向量 $\mathbf{E}$**：
$$\mathbf{E} = \mathbf{L} \mathbf{Z}$$

#### 3. 组合末期重新定价与 VaR 提取
对第 $m$ 条路径的末期组合价值 $V_T^{(m)} = f(S_{N, m}^{(1)}, S_{N, m}^{(2)}, \dots)$ 重新定价：
$$\Delta V^{(m)} = V_T^{(m)} - V_0$$
对 $M$ 个损益 $\Delta V^{(m)}$ 升序排列，取第 $\lfloor M \cdot \alpha \rfloor$ 个位置对应的负损益：
$$\mathbf{\text{VaR}_{1-\alpha} = - \Delta V_{(\lfloor M \cdot \alpha \rfloor)}}$$

### 符号解释表

| 符号 | 含义 | 维度/量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $M$ | 蒙特卡洛模拟的路径总条数 | 标量 (如 100,000) | $M$ 越大，数值误差越小，但计算越慢 |
| $N$ | 每条路径的离散时间步数 | 步数 | 路径依赖型期权需要大 $N$ |
| $\mathbf{L}$ | 协方差/相关系数矩阵的 Cholesky 分解 | $K \times K$ 下三角矩阵 | $\mathbf{R} = \mathbf{L} \mathbf{L}^T$ 用于生成相关随机数 |
| $f(S_T)$ | 衍生品定价函数 (Pricing Engine) | 货币单位 | 可以是 B-S 公式、二叉树或有限差分 |

---

## 6. 推导思路和思想来源

### 为什么在蒙特卡洛模拟中，对数收益率漂移项是 $(\mu - \frac{1}{2} \sigma^2) \Delta t$，而不是 $\mu \Delta t$？
1. **Itô 引理与 Jensen 不等式**：
   假定股票价格 $S_t$ 服从随机微分方程 $dS_t = \mu S_t dt + \sigma S_t dW_t$。
   根据 Itô 引理，对数价格 $x_t = \ln S_t$ 的微分为：
   $$d(\ln S_t) = \frac{1}{S_t} dS_t - \frac{1}{2 S_t^2} (dS_t)^2 = \left(\mu - \frac{1}{2} \sigma^2\right) dt + \sigma dW_t$$
2. **转念（几何平均与算术平均）**：
   必须减去凸性项 $-\frac{1}{2}\sigma^2$，才能确保指数映射后 $E[S_t] = S_0 e^{\mu t}$ 保持期望值无偏！若漏掉 $-\frac{1}{2}\sigma^2$，模拟出的未来价格会向上严重向上漂移偏高。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算例题（利用 Cholesky 分解生成相关正态随机数）

**题目**：
资产 1 与 资产 2 的相关系数 $\rho = 0.6$。
计算机生成了两个独立的标准正态随机数 $Z_1 = 1.0, Z_2 = 0.0$。
使用 Cholesky 分解生成满足相关系数 $\rho = 0.6$ 的相关随机数 $E_1, E_2$。

**解答过程**：
1. 构建相关系数矩阵 $\mathbf{R}$ 并求 Cholesky 分解 $\mathbf{R} = \mathbf{L} \mathbf{L}^T$：
   $$\mathbf{R} = \begin{bmatrix} 1.0 & 0.6 \\ 0.6 & 1.0 \end{bmatrix} \implies \mathbf{L} = \begin{bmatrix} 1.0 & 0.0 \\ 0.6 & 0.8 \end{bmatrix}$$
   验证：$L_{21}^2 + L_{22}^2 = 0.6^2 + 0.8^2 = 0.36 + 0.64 = 1.0$。
2. 计算相关随机数向量 $\mathbf{E} = \mathbf{L} \mathbf{Z}$：
   $$E_1 = 1.0 \times Z_1 + 0.0 \times Z_2 = 1.0 \times 1.0 = 1.0$$
   $$E_2 = 0.6 \times Z_1 + 0.8 \times Z_2 = 0.6 \times 1.0 + 0.8 \times 0.0 = 0.6$$
3. **结论**：转换后的随机数为 $E_1 = 1.0, E_2 = 0.6$，完美继承了 0.6 的正相关关系。

---

### 例子 2：中等例题（对陷落障碍期权 Barrier Option 进行蒙特卡洛路径评估）

**题目**：
某投资者持有 1 年期向下敲出看涨期权（Down-and-Out Call），敲出障碍价格 $B = 80$ 元，执行价 $K = 100$ 元。
在模拟的第 $m$ 条路径中，股价走势为：$S_0=100 \to S_1=90 \to S_2=78 \to S_3=105 \to S_T=120$。
计算该条路径末期的期权损益。

**解答过程**：
1. 检查整条路径是否触及敲出障碍 $B = 80$ 元：
   在 $t=2$ 时刻，股价 $S_2 = 78 < 80$ 元，**触发了 Knock-Out 障碍**。
2. **结论**：该期权在 $t=2$ 时已作废消失。虽然到期日股价高达 120 元，但该路径的最终期权收益强行为 **0 元**！
3. **对比**：只有蒙特卡洛模拟能逐步记录 $S_2 = 78$ 这种路径依赖过程，其他模型全会误判。

---

### 例子 3：实际应用（Python 矢量化蒙特卡洛 VaR 引擎）

```python
import numpy as np

def monte_carlo_var_option(S0, K, T, r, sigma, option_type='call', M_paths=100000, alpha=0.05):
    # 1. 矢量化生成 M 条路径的末期股价 (GBM)
    Z = np.random.normal(0, 1, M_paths)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    
    # 2. 定价引擎
    if option_type == 'call':
        payoff = np.maximum(ST - K, 0)
    else:
        payoff = np.maximum(K - ST, 0)
        
    discounted_payoff = np.exp(-r * T) * payoff
    
    # 初始购买成本 (B-S 期望值)
    initial_cost = np.mean(discounted_payoff)
    
    # 计算损益 \Delta V
    pnl = discounted_payoff - initial_cost
    
    # 3. 提取 VaR
    var_val = -np.percentile(pnl, alpha * 100)
    return var_val

print("10 万条路径蒙特卡洛 95% Option VaR:", monte_carlo_var_option(100, 100, 1.0, 0.05, 0.2, M_paths=100000))
```

---


## 7.5 💥 课本挂载与工业级实战模块 (Textbook Mapping & Production Lab)

### 7.5.5
> 🔓 **作业解锁前置条件**：学完 [[收益率与对数收益率]] + [[蒙特卡洛模拟法 VaR (Monte Carlo Simulation VaR)|Monte Carlo VaR]] 即可正式解锁本 Challenge 实战！
> 💡 **解锁指引**：理解 Monte Carlo VaR 的核心定义与基本推导逻辑后即可解锁。

 🧪 拓展实验与李宏毅式实战 Challenge 题 (Lab Assignment: Monte Carlo VaR 工业级实战 challenge)

本作业参考 **李宏毅 (Hung-yi Lee) 教授 ML 课程作业架构** 设计，设置四个渐进式难度基线 (Baselines)：

- 🟢 **简单基线 (Simple Baseline)**：
  - **任务要求**：理解 Monte Carlo VaR 的核心数学定义，使用 Python 进行基础验证与数据提取。
  - **达标标准**：代码无 Error 跑通，输出基础结果。

- 🟡 **中等基线 (Medium Baseline)**：
  - **任务要求**：实现 Monte Carlo VaR 的完整向量化代码框架，在历史数据上拟合参数并校验稳定度。
  - **达标标准**：完成核心算法的向量化与参数校准，模型表现达到基线水平。

- 🔴 **强基线 (Strong Baseline)**：
  - **任务要求**：引入严格的防前视偏差、手续费扣除与 Purged 交叉验证，使基于 Monte Carlo VaR 的模块表现击败基线。
- **达标标准**：使用预先固定的数据、时间切分、基准与成本口径完成样本外比较；改进必须同时报告效应大小、风险变化和失败案例，不设跨数据集通用收益阈值。

- 🟣 **Boss 基线 (Kaggle / 实盘级基线)**：
  - **任务要求**：结合真实工业级实盘环境（如高频盘口/高维去噪/强化学习），达成实盘级夏普比率与风险控制指标。
- **达标标准**：完成预先注册的过拟合、样本外与压力测试；报告 PBO 的切分方案、不确定性和阈值敏感性，不把单一候选阈值当作跨市场通用上线标准。

## 8. 常见误区与易混概念

### 误区 1：蒙特卡洛模拟法不需要任何数学假设，结果绝对 100% 正确

错误直觉：“蒙特卡洛模拟了 10 万次，算出来的 VaR 肯定不会错。”  
为什么错：蒙特卡洛模拟的准确性完全取决于你输入的**随机过程假设 (Stochastic Process Assumption)**。如果你输入的仍然是 GBM（正态分布 increment），你模拟出的平行宇宙里依然没有肥尾和随机跳跃（模型风险）。  
正确理解：**蒙特卡洛是优秀的“求解器”，但“输入的随机方程”决定了结果的生死。**

### 概念对比：伪随机数 (Pseudo-random) vs 准随机数 (Quasi-random / Sobol Sequence)

| 维度 | 伪随机数 (Pseudo-random Numbers) | 准随机数 (Quasi-random / Sobol 序列) |
| :--- | :--- | :--- |
| **分布均匀度** | 会产生聚类 (Clustering) 与随机空隙 | **高维空间极度均匀填充 (Low Discrepancy)** |
| **收敛速度** | $O(1 / \sqrt{M})$（需 100,000 次模拟） | **$O(1 / M)$（仅需 5,000 次模拟，快 20 倍！）** |
| **应用场景** | 标准随机测试 | **工业级蒙特卡洛 VaR 高速引擎** |

---

## 9. 相关知识点与 Obsidian 双链建议

请帮我建立知识网络。

注意：不要只列链接。每个链接后面必须用一句话说明“为什么要链接”。

上游依赖

- [[历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)|历史模拟VaR]]：提供基础概念与理论推导支撑。
- [[Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)|Black-Scholes]]：提供基础概念与理论推导支撑。

下游延伸

- [[参数法VaR（方差-协方差法）|参数法VaR]]：进一步延伸拓展该知识点的应用场景与模型构建。
- [[极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)|尾部风险]]：进一步延伸拓展该知识点的应用场景与模型构建。
- [[极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)|极值理论与POT模型]]：进一步延伸拓展该知识点的应用场景与模型构建。

横向关联

- [[收益率与对数收益率]]：衡量资产收益特性的基础量纲。
- [[实盘风控]]：风险控制与投资组合保护。

应用场景

- [[实盘风控]]：工业级量化策略风控与组合风险度量。


## 10. 闭卷复现任务

1. [ ] 默写 GBM 模拟路径递推公式，并解释 $-\frac{1}{2}\sigma^2$ 项的作用。
2. [ ] 用“平行宇宙模拟器”解释蒙特卡洛 VaR 的直觉。
3. [ ] 默写多资产相关随机数 Cholesky 分解公式 $\mathbf{E} = \mathbf{L} \mathbf{Z}$。
4. [ ] 解释为什么路径依赖型奇异期权（如障碍期权）必须使用蒙特卡洛 VaR。
5. [ ] 比较伪随机数与 Sobol 准随机数在蒙特卡洛收敛速度上的差异。

---

## 11. 自测题（5 道）

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 蒙特卡洛模拟适用场景 |
| 2 | 公式运用 | 基础 | 利用标准正态随机数手算末期股价 $S_T$ |
| 3 | 条件判断 | 中等 | 增加模拟路径数 $M$ 对标准误（Standard Error）的影响 |
| 4 | 变式/综合 | 中等 | 对偶变量法 (Antithetic Variates) 方差缩减技术 |
| 5 | 开放/建模 | 较难 | 在 GPU (CUDA/PyTorch) 上加速 100 万条路径蒙特卡洛 VaR 计算 |

---

### 第 1 题：概念辨析（基础）
**题目**：当投资组合中含有复杂的亚式期权（Asian Option，收益取决于全期平均股价）时，三大 VaR 方法中哪一种最适用？

> [!question]- 答案解析
> **答案**：蒙特卡洛模拟法 VaR（Monte Carlo VaR）。亚式期权的收益依赖于整条连续价格路径的平均值，只有蒙特卡洛法能逐步模拟完整的价格路径。  
> **Obsidian 标签**：`#自测题/蒙特卡洛适用性`

---

### 第 2 题：公式运用（基础）
**题目**：$S_0 = 100, r = 0, \sigma = 0.2, T = 1$。生成的正态随机数 $Z = 1.0$。求 GBM 模拟出的末期股价 $S_T$（取 $e^{0.18} \approx 1.1972$）。

> [!question]- 答案解析
> **答案**：
> 1. 漂移项 $- \frac{1}{2}\sigma^2 = - \frac{1}{2} (0.2)^2 = -0.02$。
> 2. 指数项 $= (-0.02) \times 1 + 0.2 \times \sqrt{1} \times 1.0 = -0.02 + 0.20 = 0.18$。
> 3. $S_T = 100 \times e^{0.18} = 100 \times 1.1972 = 119.72 \text{ 元}$。  
> **Obsidian 标签**：`#自测题/GBM路径手算`

---

### 第 3 题：条件判断（中等）
**题目**：判断：“在蒙特卡洛模拟中，如果想将估算的数值误差降低到原来的 $\frac{1}{10}$，必须将模拟路径数 $M$ 增加到原来的 100 倍。”

> [!question]- 答案解析
> **答案**：正确。根据中心极限定理，伪随机数蒙特卡洛的标准误与 $\frac{1}{\sqrt{M}}$ 成正比。要将误差缩小 10 倍，路径数 $M$ 必须增加到 $10^2 = 100$ 倍。  
> **Obsidian 标签**：`#自测题/蒙特卡洛收敛阶`

---

### 第 4 题：变式/综合（中等）
**题目**：简述“对偶变量法 (Antithetic Variates)”是如何在不增加 CPU 计算量的代价下，大幅降低蒙特卡洛模拟的方差的？

> [!question]- 答案解析
> **答案**：
> 1. **对偶生成**：每当生成一个随机数 $Z \sim N(0, 1)$ 并计算一条路径 $S_T(Z)$ 时，强行同时生成一条使用 $-Z$ 的对偶路径 $S_T(-Z)$。
> 2. **消除方差**：由于 $Z$ 与 $-Z$ 负相关，两条路径组合收益的协方差为负，求平均后大幅抵消了随机模拟的方差，显著加快了收敛速度。  
> **Obsidian 标签**：`#自测题/对偶变量法`

---

### 第 5 题：开放/建模（较难）
**题目**：如何将跳跃-扩散模型 (Merton Jump-Diffusion Model) 引入蒙特卡洛 VaR 引擎，以模拟股市黑天鹅跳空暴跌？

> [!question]- 答案解析
> **解析**：
> 1. **修改 SDE 驱动**：在 GBM 基础上增加泊松跳跃项：
>    $$\frac{dS_t}{S_{t-}} = (\mu - \lambda k) dt + \sigma dW_t + (Y_t - 1) dN_t$$
> 2. **模拟步骤**：
>    - 每一步先按泊松分布 $N_t \sim \text{Poisson}(\lambda \Delta t)$ 判断是否发生跳跃。
>    - 若 $N_t > 0$，从对数正态分布 $\ln Y_t \sim N(\mu_J, \sigma_J^2)$ 中抽取跳跃幅度 $Y_t$（设 $\mu_J < 0$ 代表暴跌跳空）。
> 3. **结果**：模拟路径中会出现断崖式连续跳空跌停，精准捕捉了金融市场的尾部跳跃风险。  
> **Obsidian 标签**：`#自测题/跳跃扩散蒙特卡洛`

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
- **建议双链**：[[历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)|历史模拟VaR]]、[[Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)|Black-Scholes]]、[[极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)|尾部风险]]
- **标签**：`#

---

<!-- quant-evidence-v3 -->
## 可定位依据与失效复核

本卡的复核对象是 **Monte Carlo VaR**，而不是只复述一个公式。对 **Monte Carlo VaR** 的独立验证重点是：固定随机种子并报告抽样误差，使用相关冲击和厚尾创新做分布敏感性测试。

### 权威来源与定位

1. Rockafellar 与 Uryasev (2000), *Optimization of Conditional Value-at-Risk*, DOI: 10.21314/JOR.2000.038。用于复核“固定随机种子并报告抽样误差，使用相关冲击和厚尾创新做分布敏感性测试”。
2. Basel Framework MAR33（内部模型法与 Expected Shortfall）：https://www.bis.org/basel_framework/chapter/MAR/33.htm。用于复核“固定随机种子并报告抽样误差，使用相关冲击和厚尾创新做分布敏感性测试”。
3. McNeil、Frey 与 Embrechts, *Quantitative Risk Management*, Princeton University Press, ISBN 9780691166278, Chapter 2 与 Chapter 7。用于复核“固定随机种子并报告抽样误差，使用相关冲击和厚尾创新做分布敏感性测试”。

### 失效边界与验收协议

- **成立条件**：先写清数据时点、估计窗口、交易摩擦和分布/市场结构假设，再运行模型。
- **反例压力测试**：固定随机种子并报告抽样误差，使用相关冲击和厚尾创新做分布敏感性测试。
- **最小实验**：固定随机种子或冻结原始数据快照，同时保存基线、破坏条件后的对照组、关键中间量与失败日志。
- **通过标准**：结论必须在样本外仍保持方向一致；若成本、延迟、参数扰动或结构突变使结论反转，就把该情形登记为适用边界而不是删除失败结果。

## 🧪 学完本节后可完成的作业

- **可完成**：[[03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-05-Black-Scholes定价与对冲|Black-Scholes定价与对冲]]。
- **为什么现在能做**：本卡已经提供该任务需要的定义、公式、条件或实现边界；若任务还依赖后续知识，先完成对应阶段 MOC 中排在本卡之后的知识卡。
- **提交产物**：闭卷定义/推导、一个可复查计算或代码结果、一个失败案例，以及对适用边界的说明。
