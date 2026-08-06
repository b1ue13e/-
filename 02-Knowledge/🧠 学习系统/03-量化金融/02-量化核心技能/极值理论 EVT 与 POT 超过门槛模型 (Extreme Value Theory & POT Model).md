---
title: 极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)
type: study
topic: 极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)
created: '2026-07-23'
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
kind: concept
flow: knowledge
source: 本课程历史知识卡；原始来源 [待验证]
source_url: https://www.bis.org/basel_framework/chapter/MAR/33.htm。用于复核“用阈值稳定图与参数稳定性选
accessed: '2026-08-06'
license: link-only；正文为本地学习整理
assessment_exempt: false
---

# 极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)

---

## 0. 先判断它值不值得深挖

**分类：A 类（核心概念，必须深挖）**

**理由：**
极值理论（Extreme Value Theory, EVT，特别是基于 Balkema-De Haan-Pickands 定理的 POT 超额门槛模型 Peak-Over-Threshold）被称为风控数学中的“极值统计学皇冠”。在金融危机、黑色星期一或流动性枯竭等极端时刻，中心极限定理（CLT）失效，正态分布和标准 GARCH 无法对 99.9% 概率下的极小概率巨额亏损进行准确估算。极值理论证明了**无论原始收益率服从什么分布，只要损失超过足够高的门槛 $u$，其超额损失（Exceedance Loss）一定渐进收敛于广义帕累托分布 (Generalized Pareto Distribution, GPD)**。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**

假设你正在为一家管理百亿资产的对冲基金计算 99.9% 置信度下的尾部风险（Expected Shortfall / CVaR）。
在过去的 1000 天历史数据中，99.9% 置信度意味着你要找倒数第 1 绝的大暴跌。
但是历史数据里最惨的一天也仅仅跌了 8%。
如果你用参数法（正态分布），它告诉你绝不可能跌超过 10%；如果你用历史模拟法，它因为没有历史更惨的数据而完全无法外推。**当现实中爆发了 20% 的断崖大暴跌时，你的风控系统由于无法对历史数据之外的“极端尾部”进行外推估算而瞬间穿仓破产！**

**以前的方法在哪里卡住：**
1. **中心极限定理 (CLT)**：关心的是样本均值的分布（正态分布），对尾部极值完全无能为力。
2. **历史模拟法**：无法外推（Cannot extrapolate）历史样本之外未曾发生过的极端巨额损失。

**为什么必须引入极值理论 (EVT - POT 模型)：**
让数据集中在损失超过门槛 $u$ 的那些“极值残差”上，拟合具有厚尾参数 $\xi$ 的广义帕累托分布 (GPD)，实现对 99.9% 甚至 99.99% 尾部极值的**精准数学外推**。

**它到底解决了哪类问题：**
解决了**如何对历史未曾发生的极端黑天鹅损失进行科学数学外推、精确计算 99.9% 高置信度下 VaR 与 CVaR/Expected Shortfall** 的问题。

---

## 2. 为什么它重要？它有什么用？

- **体系与大图景**：尾部风险与极端风控（第二阶段）的终极工具，连接历史模拟 VaR、GARCH 动态模型与巴塞尔协议 III 条件 VaR 监管要求。
- **量化与实战应用**：
  1. **巨灾与极端黑天鹅风险尾部外推**：为 Tail-Risk Hedge（尾部对冲基金，如黑天鹅基金）精确计算极端做空 Put 的期望收益。
  2. **条件 VaR (CVaR / Expected Shortfall) 解析求解**：利用 GPD 分布参数导出尾部期望损失的闭式解析解。

---

## 3. 学它之前需要哪些前置知识？

1. **[[极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)|尾部风险]]**：理解条件 VaR (CVaR / ES) 的积分定义。
2. **[[历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)|历史模拟VaR]]**：理解传统经验分位数的缺陷。
3. **最小必要背景（广义帕累托分布 GPD）**：
   > 累积分布函数：$G_{\xi, \beta}(y) = 1 - \left(1 + \frac{\xi y}{\beta}\right)^{-1/\xi}$。
   > 其中 $y = x - u > 0$ 为超过门槛 $u$ 的超额损失，$\xi$ 为形状参数（Shape Parameter / 尾部指数），$\beta$ 为尺度参数 (Scale Parameter)。

---

## 4. 用直觉语言解释它

### 生活类比：百年一遇特大洪水水坝设计

- 假设你是一名水利工程师，要建造一座能防范“百年一遇（99.9%）”甚至“千年一遇”特大洪水的超级大坝。
  - 你手头只有气象局过去 30 年的降雨记录，历史最高水位是 5 米。
  - **正态分布法**：拿圆规画抛物线，说“5.5 米水坝就绝对安全，千年一遇也不可能超过 5.5 米”。（结果特大洪水来了，水位达到 10 米，大坝溃堤！）
  - **历史模拟法**：说“过去最高 5 米，那我造 5.01 米就好了”。（完全没有外推能力）。
  - **极值理论 POT 模型**：
    1. 先划定一条防汛警戒线（门槛 $u = 3$ 米）。
    2. 把历史上所有超过 3 米的 20 次大暴雨拿出来，专门分析水流超额增量（$y = \text{水位} - 3$）。
    3. 数学证明了这些超额水流遵循“帕累托厚尾规律”，据此精确外推出“百年一遇水位是 9.2 米，千年一遇是 14.5 米”！

**极值理论 POT 的直觉本质**：
忽略平淡无奇的日常微小波动，把所有聚光灯打在“超过警戒线”的极端灾难数据上，用帕累托厚尾公式外推出未来的极限破坏力。

«“极值理论 POT 模型就是只看那些‘越过警戒线’的暴雨数据，用专门的厚尾公式外推出百年一遇的洪水有多高。”»

---

## 5. 正式定义、核心公式、符号解释

### 核心定义
**POT 超过门槛模型 (Peak-Over-Threshold Model)**：极值理论（EVT）中处理连续时间序列极值的方法。设定一个足够高的门槛 $u$，对于所有超过门槛的超额损失 $Y = X - u \mid X > u$，利用 Balkema-De Haan-Pickands 极限定理，使用广义帕累托分布（GPD）进行拟合，并导出极端 VaR 与 ES 的封闭解析解。

### 核心公式

#### 1. 广义帕累托分布 (GPD) 尾部条件概率公式
对于超过门槛 $u$ 的超额损失 $y = x - u > 0$：
$$F_u(y) = P(X - u \le y \mid X > u) = \frac{F(u + y) - F(u)}{1 - F(u)}$$
当 $u \to \infty$ 时，该条件分布收敛于 GPD：
$$G_{\xi, \beta}(y) = \begin{cases} 1 - \left(1 + \frac{\xi y}{\beta}\right)^{-1/\xi}, & \xi \neq 0 \\ 1 - \exp\left(-\frac{y}{\beta}\right), & \xi = 0 \end{cases}$$
- $\xi > 0$：**肥尾分布（Fat-Tailed / Heavy-Tailed）**，代表金融收益率极值的真实状态（帕累托尾）。

#### 2. POT 估算的极端 VaR 解析解公式
设总样本数 $N$，超过门槛 $u$ 的样本数 $N_u$（先验尾部概率 $\phi_u = \frac{N_u}{N}$）。
在极高置信度 $1 - \alpha$ 下（如 $99.9\%, \alpha = 0.001$）：

$$\text{VaR}_{1-\alpha} = u + \frac{\beta}{\xi} \left[ \left( \frac{N}{N_u} \alpha \right)^{-\xi} - 1 \right]$$

#### 3. POT 估算的条件 VaR (Expected Shortfall / ES) 解析解公式
$$\text{ES}_{1-\alpha} = E[X \mid X > \text{VaR}_{1-\alpha}] = \frac{\text{VaR}_{1-\alpha} + \beta - \xi u}{1 - \xi}$$

### 符号解释表

| 符号 | 含义 | 维度/量纲 | 备注与要求 |
| :--- | :--- | :--- | :--- |
| $u$ | 预设极端门槛 (Threshold) | 货币单位 / % | 常用前 5% 或 10% 经验分位数 |
| $N_u$ | 超过门槛 $u$ 的极端样本数量 | 数量 | $N_u$ 需足够大（通常 $N_u \ge 50$） |
| $\xi$ | **形状参数 (Shape Parameter)** | 标量 | **$\xi > 0$ 决定尾部的肥厚程度！$\xi$ 越大，黑天鹅威力越大** |
| $\beta$ | 尺度参数 (Scale Parameter) | 货币单位 | 衡量极端超额损失的波动分散度 |
| $\text{ES}_{1-\alpha}$ | 期望损失 (Expected Shortfall) | 货币单位 | **要求 $\xi < 1$，否则 ES 为无穷大！** |

---

## 6. 推导思路和思想来源

### 为什么说 Balkema-De Haan-Pickands 定理是“极值领域的中心极限定理”？
1. **中心极限定理 (CLT) 的局限**：
   CLT 证明了求和/求均值 $\frac{1}{N}\sum X_i$ 无论原始分布如何，最终收敛于**正态分布**。但 CLT 彻底磨平了尾部极值信息。
2. **极值理论 (EVT) 的突破**：
   Pickands (1975) 证明了：无论原始分布 $F(x)$ 是学生 $t$ 分布、正态分布还是柯西分布，只要研究对象是“超过高门槛 $u$ 的条件超额损失 $X - u \mid X > u$”，当 $u \to \infty$ 时，其极限分布**必然且只能**收敛于广义帕累托分布 (GPD)！
3. **转念**：风控专家不需要去猜整条曲线的全貌，只需要专注于估计 GPD 的两个参数 $(\xi, \beta)$，就能完美导出 99.9% 甚至 99.99% 的未见过的尾部极限！

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算例题（利用 POT 公式外推 99.9% 极端 VaR）

**题目**：
某基金分析了过去 $N = 1000$ 天的日损失。
设定门槛 $u = 3.0\%$，共有 $N_u = 50$ 天损失超过了 3.0%（即 $N_u / N = 5\%$）。
利用极大似然估计对这 50 个超额损失拟合 GPD，求得形状参数 $\xi = 0.20$，尺度参数 $\beta = 1.0\%$。
求该基金在 $99.9\%$ 置信度下（$\alpha = 0.001$）的 POT 极端 VaR。

**解答过程**：
1. 计算先验比例 $\frac{N}{N_u} \alpha$：
   $$\frac{N}{N_u} \alpha = \frac{1000}{50} \times 0.001 = 20 \times 0.001 = 0.02$$
2. 计算幂次项 $(0.02)^{-\xi} = (0.02)^{-0.20}$：
   $$(0.02)^{-0.20} = (50)^{0.20} = 50^{1/5} \approx 2.1867$$
3. 代入 POT VaR 公式：
   $$\text{VaR}_{99.9\%} = u + \frac{\beta}{\xi} \left[ (0.02)^{-\xi} - 1 \right] = 3.0\% + \frac{1.0\%}{0.20} [2.1867 - 1]$$
   $$\text{VaR}_{99.9\%} = 3.0\% + 5.0\% \times 1.1867 = 3.0\% + 5.9335\% = 8.9335\%$$
4. **结论**：在 99.9% 置信度下（千年一遇级别），该基金的 1 日最大可能损失为 8.93%（成功实现了超越历史最大损失 6% 的科学外推！）。

---

### 例子 2：中等例题（根据 POT VaR 解析求解 Expected Shortfall CVaR）

**题目**：
接上述计算结果，已知 $\text{VaR}_{99.9\%} = 8.9335\%$，$\xi = 0.20$, $\beta = 1.0\%$, $u = 3.0\%$。
求解超越 99.9% 门槛后的 Expected Shortfall ($\text{ES}_{99.9\%}$)。

**解答过程**：
1. 代入 POT ES 闭式解析解公式：
   $$\text{ES}_{99.9\%} = \frac{\text{VaR}_{99.9\%} + \beta - \xi u}{1 - \xi}$$
2. 计算分子：
   $$\text{分子} = 8.9335\% + 1.0\% - (0.20 \times 3.0\%) = 9.9335\% - 0.60\% = 9.3335\%$$
3. 计算分母：
   $$\text{分母} = 1 - 0.20 = 0.80$$
4. 求解 ES：
   $$\text{ES}_{99.9\%} = \frac{9.3335\%}{0.80} \approx 11.6669\%$$
5. **结论**：在最惨的 0.1% 极端黑天鹅状况下，一旦发生暴跌，平均损失将高达 11.67%！

---

### 例子 3：实际应用（Python 使用 `scipy.stats.genpareto` 拟合 POT 模型与尾部曲线）

```python
import numpy as np
import pandas as pd
from scipy.stats import genpareto

def run_evt_pot_lab():
    # 1. 模拟生成 2000 天带有极度厚尾 (t 分布 df=3) 的股票损失数据
    np.random.seed(42)
    losses = - (np.random.standard_t(df=3, size=2000) * 0.02)
    losses = losses[losses > 0] # 只保留正损失
    
    # 2. 设定 95% 分位数作为门槛 u (Peak-Over-Threshold)
    u = np.percentile(losses, 95)
    exceedances = losses[losses > u] - u
    
    N = len(losses)
    N_u = len(exceedances)
    
    # 3. 使用 GPD (广义帕累托分布) 拟合超额损失
    # scipy.stats.genpareto 的参数定义：c=\xi, scale=\beta
    xi_fit, loc_fit, beta_fit = genpareto.fit(exceedances, flock=0)
    
    # 4. 外推 99.9% 极端 VaR 与 ES (\alpha = 0.001)
    alpha = 0.001
    var_999 = u + (beta_fit / xi_fit) * (((N / N_u) * alpha) ** (-xi_fit) - 1.0)
    es_999 = (var_999 + beta_fit - xi_fit * u) / (1.0 - xi_fit)
    
    print("=== EVT-POT 极值理论实战结果 ===")
    print(f"设定门槛 u (95% 分位数): {u*100:.2f}% | 超过门槛的极端样本数 N_u: {N_u}")
    print(f"拟合 GPD 形状参数 \\xi (厚尾指数): {xi_fit:.4f} ({'典型肥尾' if xi_fit > 0 else '薄尾'})")
    print(f"拟合 GPD 尺度参数 \\beta: {beta_fit*100:.4f}%")
    print(f"外推 99.9% POT-VaR: {var_999*100:.2f}%")
    print(f"外推 99.9% POT-ES (CVaR): {es_999*100:.2f}%")

run_evt_pot_lab()
```

---

## 7.5 💥 课本挂载与工业级实战模块 (Textbook Mapping & Production Lab)

### 7.5.1 📚 经典课本章节锚定
- **教材挂载 1**：Philippe Jorion *《Value at Risk》* 第 14 章 "Stress Testing and Extreme Value Theory" Section 14.3 "Extreme Value Theory"。
  - **课本必读重点**：Balkema-De Haan-Pickands 定理、Hill 估计量、POT 门槛选择。
  - **推荐课后计算**：Jorion Ch 14 Ex 14.5, 14.8（利用 GPD 公式求解 99.9% VaR）。
- **教材挂载 2**：Ruey S. Tsay *《Analysis of Financial Time Series》* 第 7 章 "Extreme Value Theory, Quantile Estimation, and Value at Risk"。
  - **实战挂载重点**：Mean Excess Plot (均值超额图) 选择最佳门槛 $u$。

### 7.5.2 ⚙️ 工业级 Python 最小可运行实战脚手架
（见上方 例子 3 完整代码）

### 7.5.3 ⚠️ 实盘落地“踩坑指南”与回测陷阱
1. **门槛 $u$ 选择的“方差-偏差权衡 (Bias-Variance Tradeoff)”**：
   - 门槛 $u$ 设得太高 $\to$ 样本数 $N_u$ 太少，GPD 参数估计方差极巨大；
   - 门槛 $u$ 设得太低 $\to$ 不满足 $u \to \infty$ 的定理条件，引入巨大的模型偏差。工业界通过 **Mean Excess Plot（均值超额图）** 寻找线性平坦起点选择 $u$。
2. **假设超额残差独立同分布 (IID)**：
   如果市场处于波动率聚集期，连续几天大跌的超额残差存在自相关。必须先用 **GARCH 模型过滤出独立标准化残差**，再对残差应用 EVT-POT（即 GARCH-EVT 组合模型）。

### 7.5.4 📊 实战性能评估指标体系
- **GPD 形状参数 $\xi$**：$\xi > 0$（通常金融资产 $\xi \in [0.1, 0.4]$）。
- **99.9% ES 相对 VaR 放大倍数**：$\frac{\text{ES}_{99.9\%}}{\text{VaR}_{99.9\%}}$（评估尾部绝壁风险）。
- **超越门槛率检验**：$\frac{N_u}{N}$ 稳定保持在预设分位数周围。

### 7.5.5
> 🔓 **作业解锁前置条件**：学完 [[历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)|历史模拟VaR]] + [[参数法VaR（方差-协方差法）|参数法VaR]] + [[极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)|尾部风险]] + [[极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)|极值理论与POT模型]] 即可正式解锁本 Challenge 实战！
> 💡 **解锁指引**：理解分位数 VaR 的缺陷与肥尾损失分布后即可解锁 POT 极值外推。

 🧪 拓展实验与专题实战练习 (HW08-EVT 广义帕累托分布 (GPD) 极端黑天鹅尾部外推)

本作业参考 **李宏毅 (Hung-yi Lee) 教授 ML 课程作业架构** 设计，设置四个渐进式难度基线 (Baselines)：

- 🟢 **简单基线 (Simple Baseline)**：
  - **任务要求**：设定 95% 经验分位数门槛 $u$，筛选出超越门槛的超额损失样本 $y = x - u$。
  - **达标标准**：代码无 Error 跑通，输出基础结果。

- 🟡 **中等基线 (Medium Baseline)**：
  - **任务要求**：使用 `scipy.stats.genpareto` 对超额损失拟合 GPD 形状参数 $\xi$ 与尺度参数 $\beta$，手算 99.9% 极端 POT-VaR。
  - **达标标准**：完成核心算法的向量化与参数校准，模型表现达到基线水平。

- 🔴 **强基线 (Strong Baseline)**：
  - **任务要求**：利用 Mean Excess Plot（均值超额图）自动化选择最佳门槛 $u^*$，并推导出 99.9% 条件 Expected Shortfall (CVaR) 解析解。
  - **达标标准**：扣除交易摩擦与滑点后，样本外 (OOS) 夏普比率 $> 1.8$ 或评估指标提升 20% 以上。

- 🟣 **Boss 基线 (Kaggle / 实盘级基线)**：
  - **任务要求**：构建 GARCH-EVT 复合尾部风险防护网：先用 GARCH 提取独立标准化残差，再对残差进行 POT 极值外推，在黑天鹅暴跌中精准买入 Tail Put 对冲。
  - **达标标准**：代码具备极强泛化性与抗过拟合能力，通过 PBO 审计且过拟合概率 $\text{PBO} < 10\%$。


## 8. 常见误区和易混概念

### 误区 1：极值理论 (EVT) 是用来预测黑天鹅具体将在哪一天发生的

错误直觉：“有了 EVT 模型，我就能准确算出下周三会不会发生崩盘。”  
为什么错：EVT 是**概率条件分布模型**，它计算的是“在极小概率下，如果暴跌发生，其损失幅度的概率外推分布”，绝非时间序列预测模型。  
正确理解：**EVT 解决的是“跌有多深”的尾部幅度估算，而不是“哪天会跌”的择时预测。**

### 概念对比：Block Maxima (GEV 模型) vs Peak-Over-Threshold (POT 模型)

| 维度 | Block Maxima 块极值模型 | Peak-Over-Threshold (POT) 门槛模型 |
| :--- | :--- | :--- |
| **数据切片方式** | 将时间划分为固定块（如每年），只取**每年最大值** | 设定固定门槛 $u$，取**所有超过 $u$ 的点** |
| **极限分布** | 广义极值分布 (GEV: Gumbel, Fréchet, Weibull) | **广义帕累托分布 (GPD)** |
| **数据利用效率** | 极低（一年几十个 Bar 只保留 1 个点） | **极高（保留了所有极端灾难数据，工业界首选）** |

---

## 9. 相关知识点与 Obsidian 双链建议

请帮我建立知识网络。

注意：不要只列链接。每个链接后面必须用一句话说明“为什么要链接”。

上游依赖

- [[历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)|历史模拟VaR]]：提供基础概念与理论推导支撑。
- [[极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)|尾部风险]]：提供基础概念与理论推导支撑。

下游延伸

- [[量化金融-风险管理-期望损失分解与ES理论|压力测试]]：进一步延伸拓展该知识点的应用场景与模型构建。
- [[实盘风控]]：进一步延伸拓展该知识点的应用场景与模型构建。

横向关联

- [[收益率与对数收益率]]：衡量资产收益特性的基础量纲。
- [[实盘风控]]：风险控制与投资组合保护。

应用场景

- [[实盘风控]]：工业级量化策略风控与组合风险度量。


## 10. 闭卷复现任务

1. [ ] 默写 POT 超过门槛模型中 GPD 分布的条件概率定义。
2. [ ] 用“百年一遇特大洪水水坝设计”解释 EVT-POT 的直觉。
3. [ ] 默写 POT 估算的 99.9% 极端 VaR 与 ES 解析解公式。
4. [ ] 解释为什么形状参数 $\xi > 0$ 代表金融资产的“肥尾特征”。
5. [ ] 比较 Block Maxima (GEV) 与 POT (GPD) 的数据利用效率差异。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | GPD 分布中 $\xi > 0$ 的物理含义 |
| 2 | 公式运用 | 基础 | 利用 POT 闭式解手算 99.9% VaR |
| 3 | 条件判断 | 中等 | $\xi \ge 1$ 时 Expected Shortfall 的收敛性 |
| 4 | 变式/综合 | 中等 | 门槛 $u$ 选择过高或过低的影响 |
| 5 | 开放/建模 | 较难 | 在 GARCH-EVT 框架下利用标准化残差估计动态极值 VaR |

---

### 第 1 题：概念辨析（基础）
**题目**：在极值理论的广义帕累托分布 (GPD) 中，形状参数 $\xi$ (Shape Parameter) 决定了尾部的什么性质？当 $\xi > 0$ 时代表什么？

> [!question]- 答案解析
> **答案**：
> 1. $\xi$ 决定了尾部衰减的厚薄程度（尾部指数）。
> 2. 当 $\xi > 0$ 时，代表分布具有**帕累托重尾/肥尾 (Fat-Tailed / Heavy-Tailed)** 特征，尾部以幂律 (Power-law) 衰减，极易出现超大黑天鹅。  
> **Obsidian 标签**：`#自测题/GPD形状参数`

---

### 第 2 题：公式运用（基础）
**题目**：$u = 5\%$, $\beta = 2\%$, $\xi = 0.5$。若算得 $\frac{N}{N_u} \alpha = 0.01$。求 POT $\text{VaR}_{1-\alpha}$。

> [!question]- 答案解析
> **答案**：
> 1. 幂次项 $(0.01)^{-0.5} = (100)^{0.5} = 10$。
> 2. $\text{VaR} = u + \frac{\beta}{\xi} [10 - 1] = 5\% + \frac{2\%}{0.5} \times 9 = 5\% + 4\% \times 9 = 5\% + 36\% = 41\%$。  
> **Obsidian 标签**：`#自测题/POT计算`

---

### 第 3 题：条件判断（中等）
**题目**：判断：“如果在拟合 GPD 时，算得形状参数 $\xi = 1.2$，我们依然可以套用公式精确计算出 Expected Shortfall (ES)。”

> [!question]- 答案解析
> **答案**：错误。在 GPD 分布中，计算 Expected Shortfall 的分母为 $1 - \xi$。当 $\xi \ge 1$ 时，分布的期望/均值趋近于无穷大（无界），ES 无法收敛（无穷大）。模型要求必须满足 $\xi < 1$。  
> **Obsidian 标签**：`#自测题/ES发散`

---

### 第 4 题：变式/综合（中等）
**题目**：为什么在实践中，做市商通常使用 GARCH-EVT 两步法（先用 GARCH 过滤残差，再对残差跑 EVT），而不是直接对原始收益率跑 EVT？

> [!question]- 答案解析
> **答案**：
> 1. **满足 IID 假设**：EVT 理论要求样本独立同分布 (IID)。原始收益率存在显著的“波动率聚集”，直接跑 EVT 会违反 IID 假设。
> 2. **GARCH 滤波**：先用 GARCH 模型剥离出条件波动率，提取出独立同分布的标准化残差 $\hat{e}_t = \varepsilon_t / \sigma_t$，再对残差跑 EVT，能完美兼顾“动态波动率”与“极值厚尾外推”。  
> **Obsidian 标签**：`#自测题/GARCHEVT`

---

### 第 5 题：开放/建模（较难）
**题目**：设计一个利用 Mean Excess Plot（均值超额图）自动确定最佳门槛 $u^*$ 的算法思路。

> [!question]- 答案解析
> **解析**：
> 1. **均值超额函数定义**：对任意门槛 $u$，计算超过 $u$ 的样本的平均超额值 $e(u) = E[X - u \mid X > u]$。
> 2. **GPD 线性定理**：若超过 $u^*$ 的尾部服从 GPD，则对于所有 $u > u^*$，均值超额函数 $e(u)$ 是关于 $u$ 的**线性函数**：
>    $$e(u) = \frac{\beta + \xi u}{1 - \xi}$$
> 3. **算法设计**：从低到高遍历不同的 $u$，拟合 $e(u)$ 与 $u$ 的回归方程，选择 **$R^2$ 最接近 1 且残差开始呈现稳定线性直线的那个最小 $u^*$** 作为最佳门槛。  
> **Obsidian 标签**：`#自测题/MeanExcessPlot`

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
- **建议双链**：[[历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)|历史模拟VaR]]、[[极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)|尾部风险]]、[[实盘风控]]、[[量化金融-风险管理-期望损失分解与ES理论|压力测试]]
- **标签**：`#学习` `#量化金融` `#风控` `#极值理论` `#EVT` `#POT模型` `#广义帕累托` `#GPD` `#黑天鹅`

---

<!-- quant-evidence-v3 -->
## 可定位依据与失效复核

本卡的复核对象是 **极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)**，而不是只复述一个公式。对 **极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)** 的独立验证重点是：用阈值稳定图与参数稳定性选 POT 阈值，并在滚动窗口外检查尾部覆盖率。

### 权威来源与定位

1. Rockafellar 与 Uryasev (2000), *Optimization of Conditional Value-at-Risk*, DOI: 10.21314/JOR.2000.038。用于复核“用阈值稳定图与参数稳定性选 POT 阈值，并在滚动窗口外检查尾部覆盖率”。
2. Basel Framework MAR33（内部模型法与 Expected Shortfall）：https://www.bis.org/basel_framework/chapter/MAR/33.htm。用于复核“用阈值稳定图与参数稳定性选 POT 阈值，并在滚动窗口外检查尾部覆盖率”。
3. McNeil、Frey 与 Embrechts, *Quantitative Risk Management*, Princeton University Press, ISBN 9780691166278, Chapter 2 与 Chapter 7。用于复核“用阈值稳定图与参数稳定性选 POT 阈值，并在滚动窗口外检查尾部覆盖率”。

### 失效边界与验收协议

- **成立条件**：先写清数据时点、估计窗口、交易摩擦和分布/市场结构假设，再运行模型。
- **反例压力测试**：用阈值稳定图与参数稳定性选 POT 阈值，并在滚动窗口外检查尾部覆盖率。
- **最小实验**：固定随机种子或冻结原始数据快照，同时保存基线、破坏条件后的对照组、关键中间量与失败日志。
- **通过标准**：结论必须在样本外仍保持方向一致；若成本、延迟、参数扰动或结构突变使结论反转，就把该情形登记为适用边界而不是删除失败结果。


---

## 🖼️ 量化名人堂 (Hall of Fame)

> 在这冰冷的公式背后，是这些天才数学家用一生在华尔街厮杀出来的智慧结晶：

**分形几何之父：Benoit Mandelbrot**
![Benoit Mandelbrot](https://raw.githubusercontent.com/datawhalechina/quant-for-beginners/main/notebooks/phase2_intro/Benoit%20Mandelbrot.jpg)

## 🧪 学完本节后可完成的作业

- **可完成**：[[03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-08-EVT尾部风险|EVT尾部风险]]。
- **为什么现在能做**：本卡已经提供该任务需要的定义、公式、条件或实现边界；若任务还依赖后续知识，先完成对应阶段 MOC 中排在本卡之后的知识卡。
- **提交产物**：闭卷定义/推导、一个可复查计算或代码结果、一个失败案例，以及对适用边界的说明。
