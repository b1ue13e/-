---
title: VWAP 成交量加权平均价格 (Volume-Weighted Average Price)
date: 2026-07-23
type: study
course: 量化金融
importance: A
tags:
- 学习
- 量化金融
- 算法交易
- 最优执行
- VWAP
- 市场微观结构
- 冲击成本
upstream:
- '[[市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)|冲击成本模型]]'
- '[[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型|Implementation Shortfall]]'
downstream:
- '[[TWAP 时间加权平均价格 (Time-Weighted Average Price)|TWAP]]'
- '[[Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)|Almgren-Chriss最优执行轨迹推导]]'
status: planned
kind: concept
flow: knowledge
topic: VWAP 成交量加权平均价格 (Volume-Weighted Average Price)
created: '2026-08-06'
difficulty: intermediate
concept: []
prerequisites: []
related: []
source: 本课程历史知识卡；原始来源 [待验证]
source_url: '[待验证]'
accessed: '2026-08-06'
license: link-only；正文为本地学习整理
assessment_exempt: false
---

# VWAP 成交量加权平均价格 (Volume-Weighted Average Price)

---

## 0. 先判断它值不值得深挖

**分类：A 类（核心概念，必须深挖）**

**理由：**
VWAP（成交量加权平均价格）是机构算法交易（Algorithmic Trading）和高频执行中出镜率最高的核心执行基准（Execution Benchmark）。公募基金、私募基金向券商 Algorithmic Desk 下大单时，90% 的考核标准就是“实际成交均价是否优于市场全天的 VWAP”。掌握 VWAP 的预测、历史成交量 U 型曲线与拆单算法，是量化交易与最优执行（Execution Optimization）的核心功底。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**

假设你是一家大型公募基金的交易员，今天必须在开盘到收盘期间，在市场买入 500 万股贵州茅台（价值约 75 亿元）。
如果你一下子把 500 万股挂在盘口，巨大的买盘会立刻把股价拉抬暴涨 5%（即产生巨大的冲击成本 Market Impact Cost），导致后半段买入价格极贵。

**以前的方法在哪里卡住：**
1. **简单均匀切分拆单 (TWAP)**：按时间每分钟切成固定的股数卖出。但股市存在“开盘与收盘成交活跃、午间成交清淡”的 U 型流动性分布。在午间成交量极低时强行均匀拆单，同样会把薄弱的盘口砸穿。
2. **人工凭感觉手动下单**：容易产生主观心理偏误，且无法向出资人（LP/基金经理）证明自己的交易没有买贵。

**为什么必须引入 VWAP 算法交易：**
根据全天历史**成交量分布曲线（Volume Profile）**，将大单切分为与全天成交量节奏高度拟合的小单切片。在市场成交活跃时多买，在交投清淡时少买。

**它到底解决了哪类问题：**
解决了**大额订单拆拆细化执行时，如何将市场冲击成本降至最低，并以不劣于全天市场成交量加权均价的水平完成建仓/平仓**的问题。

---

## 2. 为什么它重要？它有什么用？

- **体系与大图景**：最优执行（第四阶段）的骨架指标，连接交易信号与实际订单流落地。
- **量化与实操应用**：
  1. **大单拆拆执行算法（VWAP Algo）**：交易柜台（EMS）利用历史 20 天的日内 U 型成交量曲线预测今天的成交量分布，动态调整拆单比例。
  2. **交易执行绩效评估 (TCA)**：计算执行滑点 $Slippage = P_{trade} - VWAP_{market}$，作为考核交易员和券商算法质量的 KPI。

---

## 3. 学它之前需要哪些前置知识？

1. **[[TWAP 时间加权平均价格 (Time-Weighted Average Price)|TWAP]]**：时间加权平均价格（均分时间拆单法）。
2. **[[限价订单簿数据与 L1_L2_L3 盘口重建 (Limit Order Book Data & Reconstructing L1_L2_L3)|订单簿数据]]**：理解盘口深度（Order Book Depth）与买卖挂单撮合机制。
3. **最小必要背景（日内 U 型成交量分布）**：
   > 股票市场在开盘后 30 分钟（09:30-10:00）和收盘前 30 分钟（14:30-15:00）成交最为活跃，呈 U 型或 Smile 型曲线。

---

## 4. 用直觉语言解释它

### 生活类比：批发商按“菜市场人流高峰”采购

假设你是一家饭店采购员，今天要去农贸市场采购 500 斤大白菜。
- 如果你在中午 12 点（市场空无一人）强行要买 300 斤，摊主会趁机抬价。
- 正确做法是：早上 8 点人流最高峰、货源最充足时，你顺手买走 200 斤（占比小不引起注意）；中午人少时，你只买 50 斤；下午 4 点下班高峰货源又多时，你再买走 250 斤。

**VWAP 的直觉本质**：
顺着市场的“水流”（成交量潮汐）去买卖。市场水流大时你多舀水，水流小时你少舀水，让自己的买入节奏完全融进全市场的交易节奏里。

«“VWAP 就是按照全天成交量的潮汐分布切分大单，让自己的平均买价贴近全市场的加权平均价。”»

---

## 5. 正式定义、核心公式、符号解释

### 核心定义
**VWAP（成交量加权平均价格）**：指在特定时间窗口内，某资产的总成交金额除以总成交股数的加权平均值。

### 核心公式

#### 1. 全天静态 VWAP 离散公式
$$VWAP = \frac{\sum_{i=1}^N P_i \times V_i}{\sum_{i=1}^N V_i}$$

#### 2. VWAP 拆单算法子目标（$t$ 拆单量预测）
假设总订单量为 $V_{total}$，第 $t$ 步的计划下单量为 $v_t$：
$$v_t = V_{total} \times \frac{\hat{V}_t}{\sum_{\tau=1}^M \hat{V}_\tau}$$
其中 $\hat{V}_t$ 为模型预测的第 $t$ 个时间片全市场发生的成交量。

### 符号解释表

| 符号 | 含义 | 维度/量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $P_i$ | 第 $i$ 笔逐笔成交（或第 $i$ 个 K 线）的成交价格 | 货币单位 | 价格要素 |
| $V_i$ | 第 $i$ 笔逐笔成交（或第 $i$ 个 K 线）的成交量 | 股数/手 | 加权权重 |
| $V_{total}$ | 机构需要执行的大单总量 | 股数/手 | 目标执行量 |
| $\hat{V}_t$ | 预估的第 $t$ 时间片全市场成交量 | 股数/手 | 通常取历史同期中位数/均值 |
| $M$ | 全天拆分的时间片总数 | 整数 | 如 240 分钟划分 240 个片 |

---

## 6. 推导思路和思想来源

### 为什么 VWAP 优于 TWAP？
1. **TWAP 的局限**：假设每个时间片的市场深度一致。在成交量低谷期（如 11:00-11:30），TWAP 下单量占全市场比例（Participation Rate）急剧飙升，从而引发不成比例的巨大冲击成本（Impact Cost 具有平方根或非线性特征：$Impact \propto \sqrt{\frac{v_t}{V_t}}$）。
2. **转念（使得 Participation Rate 恒定）**：
   令自己在每个时间片的参与率 $\frac{v_t}{V_t} = c$ 为常数。
   则 $v_t = c \times V_t$。
   由于 $\sum v_t = V_{total} \implies c = \frac{V_{total}}{\sum V_t}$。
   这样即可保证自己的下单量完全追踪市场的流动性分布，将市场冲击降至最低！

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算例题（VWAP 与算术平均价 TWAP 对比）

**题目**：
某股票全天仅有 3 笔成交：
- 9:30 时：价格 $10.0$ 元，成交量 $1000$ 股。
- 11:00 时：价格 $11.0$ 元，成交量 $100$ 股。
- 14:30 时：价格 $10.5$ 元，成交量 $900$ 股。

求全天的 Simple Average（简单算术平均价）与全天 VWAP。

**解答过程**：
1. 简单算术平均价：
   $$P_{simple} = \frac{10.0 + 11.0 + 10.5}{3} = \frac{31.5}{3} = 10.50 \text{ 元}$$
2. VWAP 加权计算：
   - 总成交金额 $= 10.0 \times 1000 + 11.0 \times 100 + 10.5 \times 900 = 10000 + 1100 + 9450 = 20550 \text{ 元}$
   - 总成交股数 $= 1000 + 100 + 900 = 2000 \text{ 股}$
   - $$VWAP = \frac{20550}{2000} = 10.275 \text{ 元}$$
3. **结论**：因为大成交量发生在低价区（10.0 元与 10.5 元），VWAP（10.275 元）显著低于算术平均价（10.50 元），更真实反映资金的真实买入成本。

---

### 例子 2：中等例题（VWAP 拆单计划生成）

**题目**：
某基金计划在 1 小时内买入 10,000 股某股票。已知根据历史预测，这 1 小时划分为 3 个区间，全市场预测成交量为：
- 区间 1：$20,000$ 股
- 区间 2：$10,000$ 股
- 区间 3：$20,000$ 股

计算该 VWAP 算法在 3 个区间应分别下单买入多少股？

**解答过程**：
1. 全市场预测总成交量 $= 20,000 + 10,000 + 20,000 = 50,000$ 股。
2. 目标参与率 $c = \frac{10,000}{50,000} = 20\%$。
3. 计算各区间下单量：
   - 区间 1：$20,000 \times 20\% = 4,000$ 股
   - 区间 2：$10,000 \times 20\% = 2,000$ 股
   - 区间 3：$20,000 \times 20\% = 4,000$ 股

---

### 例子 3：实际应用（Python 算法交易 VWAP 拆单模拟）

```python
import numpy as np
import pandas as pd

## 假定历史 5 分钟成交量 Profile (24 个区间)
np.random.seed(42)
volume_profile = np.array([5, 4, 3, 2, 2, 1, 1, 1, 2, 2, 3, 4] * 2) # U 型
volume_profile_pct = volume_profile / np.sum(volume_profile)

## 目标买入 100,000 股
total_order_size = 100000
sliced_orders = total_order_size * volume_profile_pct

print("开盘前 5 分钟计划下单股数:", int(sliced_orders[0]))
print("午间清淡期 5 分钟计划下单股数:", int(sliced_orders[5]))
```

---

## 7.5 💥 课本挂载与工业级实战模块 (Textbook Mapping & Production Lab)

### 7.5.1 📚 经典课本章节锚定
- **教材挂载 1**：Barry Johnson *《Algorithmic Trading and DMA (算法交易与直接市场接入)》* 第 6 章 "Optimal Execution Algorithms" - VWAP Execution.
  - **课本必读重点**：Historical Volume Profile 预测模型、Participation Rate 设定与成交量偏差（Volume Mis-estimation）修正。
  - **推荐课后计算 Lab**：Johnson Ch 6.4（日内 U 型成交量曲线拟合与多频段拆单分配）。
- **教材挂载 2**：Rishi Narang *《Inside the Black Box (黑盒内的交易)》* 第 7 章 "Execution Systems"。
  - **实战挂载重点**：暗池 (Dark Pool) 匹配、智能订单路由 (SOR) 与防止高频被动吃单滑点。

### 7.5.2 ⚙️ 工业级 Python 最小可运行实战脚手架
包含：日内 5 分钟线 Volume Profile 预测、VWAP 拆单执行计划推导、与交易绩效 TCA (Transaction Cost Analysis) 评估。

```python
import numpy as np
import pandas as pd

def run_vwap_production_lab():
    # 1. 模拟过去 20 天 5 分钟 K 线历史成交量 Profile (48 个 5 分钟 Bars/天)
    np.random.seed(42)
    bars_per_day = 48
    days = 20
    
    # 构造典型的 U 型日内成交量曲线
    u_shape = np.exp(np.linspace(1.5, 0, 24)).tolist() + np.exp(np.linspace(0, 1.5, 24)).tolist()
    u_shape = np.array(u_shape) / np.sum(u_shape)
    
    historical_volume = np.zeros((days, bars_per_day))
    for d in range(days):
        total_daily_vol = np.random.uniform(800000, 1200000)
        historical_volume[d] = total_daily_vol * u_shape * np.random.uniform(0.8, 1.2, bars_per_day)
        
    # 2. 计算预测的 Volume Profile 权重 (各时段期望比例)
    predicted_profile = historical_volume.mean(axis=0)
    predicted_profile /= predicted_profile.sum()
    
    # 3. 客户发下单指令：今日需买入总量 V_target = 100,000 股
    V_target = 100000
    scheduled_orders = np.round(V_target * predicted_profile).astype(int)
    
    # 4. 模拟今日实盘执行：模拟价格和真实发生的成交量
    todays_actual_volume = 1100000 * u_shape * np.random.uniform(0.85, 1.15, bars_per_day)
    todays_prices = 50.0 + np.cumsum(np.random.normal(0.01, 0.1, bars_per_day))
    
    # 计算全天真实市场 VWAP
    market_vwap = np.sum(todays_prices * todays_actual_volume) / np.sum(todays_actual_volume)
    
    # 计算算法执行均价 (Algo Execution VWAP)
    algo_executed_price = np.sum(todays_prices * scheduled_orders) / np.sum(scheduled_orders)
    
    # 5. TCA 绩效分析 (Slippage vs Market VWAP)
    slippage_bp = (algo_executed_price - market_vwap) / market_vwap * 10000
    
    print("=== VWAP 最优拆单算法 Lab 结果 ===")
    print(f"拟拆单目标股数: {V_target} 股 | 实际拆单总额: {scheduled_orders.sum()} 股")
    print(f"早盘第 1 个 5 分钟派单量: {scheduled_orders[0]} 股 ({predicted_profile[0]:.2%})")
    print(f"午间第 24 个 5 分钟派单量: {scheduled_orders[23]} 股 ({predicted_profile[23]:.2%})")
    print(f"全天市场加权均价 (Market VWAP): {market_vwap:.4f} 元")
    print(f"算法实际成交均价 (Algo VWAP):   {algo_executed_price:.4f} 元")
    print(f"TCA 执行滑点: {slippage_bp:+.2f} BP ({'超越市场' if slippage_bp < 0 else '落后市场'})")

run_vwap_production_lab()
```

### 7.5.3 ⚠️ 实盘落地“踩坑指南”与回测陷阱
1. **静态 Volume Profile 的“失真塌陷”**：
   在突发重大宏观利好/利空日，午间原本冷清的时段会突然爆出天量成交。若算法傻傻按历史静态 Profile 发单，会导致午间派单量过小、尾盘追赶大单触发极高市场冲击成本。必须引入 **动态实时成交量更新 (Dynamic Profile Adjustment)**。
2. **参与率过高暴露痕迹 (Participation Rate Limit)**：
   若该算法在单一个 5 分钟 Bin 内的派单量达到了市场当前总成交量的 30% 以上（$\text{POV} > 30\%$），会暴露高频机构的吸筹意图，被高频 HFT 捕获并实施盘口抬价抢跑。工业界强制设定 **$\text{POV} \le 15\%$ 上限**。
3. **收盘集合竞价 (Auction Spillover)**：
   若全天未按计划完成拆单，剩余的大量未成交股票被迫拖延到收盘集合竞价 (3:00 PM Close)，会承受极大的尾盘集合竞价滑点。

### 7.5.4 📊 实战性能评估指标体系
- **VWAP 滑点 (VWAP Slippage in BPs)**：$\frac{P_{algo} - P_{market\_vwap}}{P_{market\_vwap}} \times 10,000$。
- **拆单跟踪偏离度 (Tracking Variance)**：$\sum (v_{algo, t} - v_{target, t})^2$。
- **市场参与率上限 (Max Participation Rate)**：$\max_t \left( \frac{v_{algo, t}}{V_{market, t}} \right) \le 15\%$。

### 7.5.5
> 🔓 **作业解锁前置条件**：学完 [[收益率与对数收益率]] + [[VWAP 成交量加权平均价格 (Volume-Weighted Average Price)|VWAP]] 即可正式解锁本 Challenge 实战！
> 💡 **解锁指引**：理解 VWAP 的核心定义与基本推导逻辑后即可解锁。

 🧪 拓展实验与李宏毅式实战 Challenge 题 (Lab Assignment: VWAP 工业级实战 challenge)

本作业参考 **李宏毅 (Hung-yi Lee) 教授 ML 课程作业架构** 设计，设置四个渐进式难度基线 (Baselines)：

- 🟢 **简单基线 (Simple Baseline)**：
  - **任务要求**：理解 VWAP 的核心数学定义，使用 Python 进行基础验证与数据提取。
  - **达标标准**：代码无 Error 跑通，输出基础结果。

- 🟡 **中等基线 (Medium Baseline)**：
  - **任务要求**：实现 VWAP 的完整向量化代码框架，在历史数据上拟合参数并校验稳定度。
  - **达标标准**：完成核心算法的向量化与参数校准，模型表现达到基线水平。

- 🔴 **强基线 (Strong Baseline)**：
  - **任务要求**：引入严格的防前视偏差、手续费扣除与 Purged 交叉验证，使基于 VWAP 的模块表现击败基线。
  - **达标标准**：扣除交易摩擦与滑点后，样本外 (OOS) 夏普比率 $> 1.8$ 或评估指标提升 20% 以上。

- 🟣 **Boss 基线 (Kaggle / 实盘级基线)**：
  - **任务要求**：结合真实工业级实盘环境（如高频盘口/高维去噪/强化学习），达成实盘级夏普比率与风险控制指标。
  - **达标标准**：代码具备极强泛化性与抗过拟合能力，通过 PBO 审计且过拟合概率 $\text{PBO} < 10\%$。


## 8. 常见误区与易混概念

### 误区 1：VWAP 算法的目标是超越市场、创造阿尔法 (Alpha)

错误直觉：“VWAP 算法能帮我买在全天的最低价。”  
为什么错：VWAP 是一种**执行追踪算法（Benchmark Tracking Algo）**，其目标是尽可能**贴近**全天的 VWAP 均价，减少滑点与冲击，而非预测高低点做 Alpha 择时。  
正确理解：VWAP 是测量和优化“交易质量”的尺子，不是预测股价的方向信号。

### 概念对比：VWAP vs TWAP

| 维度 | VWAP (成交量加权) | TWAP (时间加权) |
| :--- | :--- | :--- |
| **权重依据** | 预测的市场成交量（Volume Profile） | 时间区间均匀切分 |
| **最佳适用场景** | 大盘股、流动性高且成交量 U 型明显的股票 | 小盘股、缺乏成交量历史分布或交投极清淡股票 |
| **主要风险** | 若突发事件导致当日成交量严重偏离历史预测，算法会失真 | 在成交量低谷期可能造成过大冲击 |

---

## 9. 相关知识点与 Obsidian 双链建议

请帮我建立知识网络。

注意：不要只列链接。每个链接后面必须用一句话说明“为什么要链接”。

上游依赖

- [[市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)|冲击成本模型]]：提供基础概念与理论推导支撑。
- [[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型|Implementation Shortfall]]：提供基础概念与理论推导支撑。

下游延伸

- [[TWAP 时间加权平均价格 (Time-Weighted Average Price)|TWAP]]：进一步延伸拓展该知识点的应用场景与模型构建。
- [[Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)|Almgren-Chriss最优执行轨迹推导]]：进一步延伸拓展该知识点的应用场景与模型构建。

横向关联

- [[收益率与对数收益率]]：衡量资产收益特性的基础量纲。
- [[实盘风控]]：风险控制与投资组合保护。

应用场景

- [[实盘风控]]：工业级量化策略风控与组合风险度量。


## 10. 闭卷复现任务

1. [ ] 默写全天静态 VWAP 的计算公式。
2. [ ] 用“农贸市场采购白菜”解释 VWAP 算法的直觉。
3. [ ] 说明为什么直接使用 TWAP 会在成交量低谷期造成较大冲击成本。
4. [ ] 写出基于成交量 Profile 预测的 VWAP 拆单比例公式。
5. [ ] 列出 VWAP 与 TWAP 的 2 个核心区别。

---

## 11. 自测题（5 道）

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | VWAP 交易基准的定义 |
| 2 | 公式运用 | 基础 | 手算两笔成交的 VWAP |
| 3 | 条件判断 | 中等 | 市场突发消息导致成交量放大大时 VWAP 算法的调整 |
| 4 | 变式/综合 | 中等 | 计算实际成交价格相对于 VWAP 的滑点 (Slippage) |
| 5 | 开放/建模 | 较难 | 引入动态卡尔曼滤波改进日内 Volume Profile 实时预测 |

---

### 第 1 题：概念辨析（基础）
**题目**：在交易绩效评估（TCA）中，若买入大单的实际平均成交价低于全天 VWAP，这代表什么？

> [!question]- 答案解析
> **答案**：代表执行绩效优异（Positive Slippage / Outperformance），说明交易员或算法以优于全天加权均价的更低成本完成了买入建仓。  
> **Obsidian 标签**：`#自测题/VWAP`

---

### 第 2 题：公式运用（基础）
**题目**：某股票某日仅有两笔交易：以 20 元成交 4000 股，以 25 元成交 1000 股。求全天的 VWAP。

> [!question]- 答案解析
> **答案**：
> $\text{总金额} = 20 \times 4000 + 25 \times 1000 = 80,000 + 25,000 = 105,000 \text{ 元}$。
> $\text{总股数} = 4000 + 1000 = 5000 \text{ 股}$。
> $VWAP = \frac{105,000}{5000} = 21.0 \text{ 元}$。  
> **Obsidian 标签**：`#自测题/VWAP计算`

---

### 第 3 题：条件判断（中等）
**题目**：判断：“VWAP 算法要求在全天每一个时间段的参与率（Participation Rate）尽可能保持恒定。”

> [!question]- 答案解析
> **答案**：正确。VWAP 的核心逻辑就是让自己的下单量按固定比例 $c$ 匹配全市场的成交量 $V_t$，从而保持参与率恒定，最小化单时段冲击。  
> **Obsidian 标签**：`#自测题/参与率`

---

### 第 4 题：变式/综合（中等）
**题目**：某机构委托买入 100 万股，市场全天 VWAP 为 10.00 元。该机构算法实际买入均价为 10.05 元。求买入执行滑点（bp，基点）。

> [!question]- 答案解析
> **答案**：
> $\text{滑点} = \frac{P_{actual} - VWAP}{VWAP} = \frac{10.05 - 10.00}{10.00} = \frac{0.05}{10.00} = 0.0050 = 0.50\% = 50 \text{ bp}$（多付出了 50 个基点的成本）。  
> **Obsidian 标签**：`#自测题/执行滑点`

---

### 第 5 题：开放/建模（较难）
**题目**：传统的 VWAP 算法只依赖历史静态 Volume Profile，在遇到“突发利好放量暴涨”时会有什么致命缺陷？如何改进？

> [!question]- 答案解析
> **解析**：
> 1. **缺陷**：静态 Profile 无法预测突发放量。当市场因利好暴涨放量时，静态 VWAP 算法依然在按原计划低速下单，导致参与率过低、订单严重滞后，被迫在尾盘追高买入。
> 2. **改进**：使用**动态 VWAP (Dynamic Volume Profile)**，结合实时 Order Book 的 Order Flow Imbalance (OFI) 和即期成交量，运用 EWMA 或 Kalman Filter 实时更新后半天的 $\hat{V}_t$ 预测。  
> **Obsidian 标签**：`#自测题/动态VWAP`

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
- **建议双链**：[[TWAP 时间加权平均价格 (Time-Weighted Average Price)|TWAP]]、[[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型|Implementation Shortfall]]、[[市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)|冲击成本模型]]
- **标签**：`#学习` `#量化金融` `#算法交易` `#VWAP` `#最优执行` `#冲击成本`

---

<!-- quant-evidence-v3 -->
## 可定位依据与失效复核

本卡的复核对象是 **VWAP 成交量加权平均价格 (Volume-Weighted Average Price)**，而不是只复述一个公式。对 **VWAP 成交量加权平均价格 (Volume-Weighted Average Price)** 的独立验证重点是：先用只含当时可见数据的成交量曲线预测，再比较计划 VWAP 与实际市场 VWAP。

### 权威来源与定位

1. Almgren 与 Chriss (2001), *Optimal Execution of Portfolio Transactions*, DOI: 10.21314/JOR.2001.041。用于复核“先用只含当时可见数据的成交量曲线预测，再比较计划 VWAP 与实际市场 VWAP”。
2. Perold (1988), *The Implementation Shortfall: Paper versus Reality*, DOI: 10.3905/jpm.1988.409150。用于复核“先用只含当时可见数据的成交量曲线预测，再比较计划 VWAP 与实际市场 VWAP”。
3. Joel Hasbrouck, *Empirical Market Microstructure*, Oxford University Press, ISBN 9780195301649, Chapter 3 与 Chapter 5（价差、冲击和执行测量）。用于复核“先用只含当时可见数据的成交量曲线预测，再比较计划 VWAP 与实际市场 VWAP”。

### 失效边界与验收协议

- **成立条件**：先写清数据时点、估计窗口、交易摩擦和分布/市场结构假设，再运行模型。
- **反例压力测试**：先用只含当时可见数据的成交量曲线预测，再比较计划 VWAP 与实际市场 VWAP。
- **最小实验**：固定随机种子或冻结原始数据快照，同时保存基线、破坏条件后的对照组、关键中间量与失败日志。
- **通过标准**：结论必须在样本外仍保持方向一致；若成本、延迟、参数扰动或结构突变使结论反转，就把该情形登记为适用边界而不是删除失败结果。

## 🧪 学完本节后可完成的作业

- **可完成**：[[03-Projects/金融与时序/03-量化金融/阶段作业/量化金融-阶段作业-04-Almgren-Chriss最优执行|Almgren-Chriss最优执行]]。
- **为什么现在能做**：本卡已经提供该任务需要的定义、公式、条件或实现边界；若任务还依赖后续知识，先完成对应阶段 MOC 中排在本卡之后的知识卡。
- **提交产物**：闭卷定义/推导、一个可复查计算或代码结果、一个失败案例，以及对适用边界的说明。
