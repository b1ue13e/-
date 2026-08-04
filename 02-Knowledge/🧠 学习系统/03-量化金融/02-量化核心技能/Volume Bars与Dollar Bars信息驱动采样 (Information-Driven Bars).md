---
type: study
topic: "信息驱动采样 (Information-Driven Bars)"
created: 2026-08-04
status: ongoing
difficulty: intermediate
course: "03-量化金融"
importance: "A"
stage: "📗 第二阶段：量化核心技能"
tags: [学习, 量化金融, 数据工程, 采样, 市场微观结构]
concept: ["信息驱动采样", "Volume Bars", "Dollar Bars", "Tick Imbalance Bars"]
prerequisites: ["OHLCV字段清洗与复权", "订单类型与交易所连续竞价撮合机制"]
related: ["协方差去噪与随机矩阵理论 RMT", "分层风险平价组合 HRP", "Almgren-Chriss 最优算法执行轨迹推导"]
upstream: ["[[OHLCV字段清洗与复权]]", "[[订单类型与交易所连续竞价撮合机制 (Order Types & Continuous Double Auction)]]"]
downstream: ["[[协方差去噪与随机矩阵理论 RMT (Covariance Denoising & Marchenko-Pastur Law in AFML)]]", "[[分层风险平价组合 HRP (Hierarchical Risk Parity in AFML)]]"]
flow: knowledge
kind: concept
source: "López de Prado, Advances in Financial Machine Learning (AFML), Chapter 2"
anki_deck: "量化金融::核心技能"
anki_tags: ["量化金融", "数据工程", "信息驱动采样"]
---

# Volume Bars 与 Dollar Bars：信息驱动采样 (Information-Driven Bars)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：传统时间柱（Time Bars）是所有量化策略的基础，但它有一个致命缺陷——在市场冷清时段（如午间休市），时间柱采集的信息量极少，而在开盘/收盘或重大新闻发布时信息爆发，却被同等频率的采样粗暴均摊。信息驱动采样（Information-Driven Bars）解决了这个问题，它让采样频率跟随市场信息流动的节奏自适应变化，是 Marcos López de Prado 在 AFML 中提出的"现代量化数据工程第一课"。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 传统时间柱（1 分钟 K 线、5 分钟 K 线、日线）以固定时钟频率采样。但在真实市场中，信息的到达不是均匀的——开盘前 5 分钟可能发生 30% 的日成交量，而午间 30 分钟只有 2%。用固定时间窗口采样，意味着我们**在信息密度最高的时段欠采样，在信息密度最低的时段过采样**，这会导致：
> 1. **统计量失真**：波动率、相关性、自相关等统计量被时间柱的节奏绑架
> 2. **机器学习失效**：模型学习到的模式是"时钟模式"而非"市场模式"
> 3. **回测偏差**：时间柱的回测结果无法反映真实的逐笔成交微观结构

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：不掌握信息驱动采样，后续所有基于协方差矩阵（MPT、HRP、MP 去噪）、波动率建模（GARCH）、以及回测框架的统计推断都会在采样层就引入不可消除的偏差。它是 AFML 全书数据工程的基石。
- **实际应用场景**：
  - **高频策略回测**：用 Dollar Bars 替代 1 分钟 K 线，消除成交量日内 U 型模式的干扰
  - **协方差矩阵估计**：用 Volume Bars 让每个观测包含等量的市场参与信息
  - **机器学习特征工程**：Tick Imbalance Bars 直接量化买卖压力的不对称性
  - **跨市场比较**：不同活跃度的股票用 Dollar Bars 统一采样后，统计量才可比较
- **高频题型/任务**：AFML 第二章 Snip 2.1-2.4 的代码 Lab；HW09 采样引擎实战

---

## 3. 学它之前需要哪些前置知识？

最小必要背景（各 200 字以内）：

1. **[[OHLCV字段清洗与复权]]**：理解 OHLCV 字段含义、时间戳处理、前/后复权概念。Volume Bars 需要用到成交量（V）字段的清洗和异常值检测。
2. **[[订单类型与交易所连续竞价撮合机制 (Order Types & Continuous Double Auction)]]**：理解逐笔成交（Tick）数据的结构——每笔 Tick 包含价格、成交量、买卖方向（买方主动/卖方主动）。这是 Tick Imbalance Bars 的信息源头。

---

## 4. 用直觉语言解释它

> «"这东西其实就像——你不按日历过生日，而是按开心的事过生日"»

- **直觉类比/几何图像**：时间柱像「每隔固定时间拍一张照片」，不管照片里有没有内容。Volume Bars 像「每吃掉固定数量的饺子拍一张照片」——吃得快时（成交活跃）照片密集，吃得慢时（成交冷清）照片稀疏。Dollar Bars 更进一步：不同"饺子"大小不同（股票价格差异大），所以用「每吃掉固定金额的饺子」来消除价格水平的影响。
- **为什么很自然**：信息流入市场的物理载体是**成交**（Tick），不是时钟指针。每一笔成交都携带了新信息（价格变化、成交量、方向）。采样应该跟随这个物理过程，而不是人为强加的时钟。
- **一句话直觉本质**：**让采样频率与市场信息流入速度同步，而非与墙上时钟同步。**

---

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义

**信息驱动柱（Information-Driven Bar）** 是一类不再以固定时间间隔，而是以**固定成交量的累积阈值**来切分 OHLCV 柱的采样方法。

### 2. 四类 Bars 的定义

#### (a) Volume Bars（成交量柱）

采样规则：每当**累计成交量** $V_{\text{cum}}$ 达到预设阈值 $V_{\text{threshold}}$，就切出一根新 Bar。

$$V_{\text{cum}} = \sum_{i=1}^{T} v_i \geq V_{\text{threshold}} \quad \Rightarrow \quad \text{New Bar}$$

- $v_i$：第 $i$ 笔 Tick 的成交量（股数）
- 典型阈值：日均成交量的 1/50（约产生 50 根 Bar/天）

#### (b) Dollar Bars（美元成交额柱）

采样规则：每当**累计成交额** $D_{\text{cum}}$ 达到预设阈值 $D_{\text{threshold}}$，就切出一根新 Bar。

$$D_{\text{cum}} = \sum_{i=1}^{T} p_i \cdot v_i \geq D_{\text{threshold}} \quad \Rightarrow \quad \text{New Bar}$$

- $p_i$：第 $i$ 笔 Tick 的成交价格
- Dollar Bars 自动适应股票拆分和价格变动，优于 Volume Bars

#### (c) Tick Imbalance Bars（买卖不平衡柱）

采样规则：当 Tick 的**买卖方向不平衡度**的累计绝对值达到阈值时切 Bar。

定义 Tick 方向：
$$b_t = \begin{cases} 1 & \text{买方主动（价格 ≥ 卖一价）} \\ -1 & \text{卖方主动（价格 ≤ 买一价）} \\ 0 & \text{无法判断} \end{cases}$$

Tick 不平衡度：
$$\theta_T = \frac{\sum_{t=1}^{T} b_t}{\sum_{t=1}^{T} |b_t|}$$

当 $|\sum b_t| \geq E_0[|\sum b_t|]$（期望阈值）时切 Bar。期望阈值由指数加权移动平均动态更新。

#### (d) Volume/Dollar Imbalance Bars

结合 Volume Bars 和 Tick Imbalance：当**成交量加权的不平衡度**达到阈值时切 Bar。

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $v_i$ | 第 $i$ 笔 Tick 成交量 | 正整数（股） | 异常值需 Winsorize |
| $p_i$ | 第 $i$ 笔 Tick 成交价 | $\mathbb{R}^+$（元） | 注意除权除息日 |
| $V_{\text{threshold}}$ | Volume Bar 阈值 | 正整数 | 通常 = ADV / N（如 N=50） |
| $D_{\text{threshold}}$ | Dollar Bar 阈值 | $\mathbb{R}^+$ | 通常 = ADVR / N |
| $b_t$ | Tick 方向签名 | $\{-1,0,1\}$ | 基于 Lee-Ready 算法或 BVC |
| $\theta_T$ | 不平衡度 | $[-1,1]$ | 0 = 完全平衡 |
| $\text{ADV}$ | 日均成交量 | 股 | 滚动窗口估计 |

### 4. 常见变体与适用条件

- **适用条件**：有逐笔 Tick 数据或至少 Level-1 快照数据；标的流动性足够（日均成交 ≥ 10 万股）
- **限制条件**：极端低流动性标的可能导致 Bar 生成极慢；不同股票的阈值需要分别校准；Dollar Bars 在不同市场（A 股 vs 美股）因价格量级差异需要调整阈值

---

## 6. 推导思路和思想来源

- **最初困难**：时间柱假设信息均匀到达，但市场微观结构证明信息到达是高度聚集的（波动率聚类、成交量日内 U 型模式）
- **直接方法局限**：用更高的时间频率（如 Tick 级）采样可以缓解，但引入噪声放大和计算爆炸
- **关键"转念"**：**信息不是时间驱动，是成交驱动。** 每一笔成交都是市场参与者"用钱投票"的信息载体。我们应该让采样阈值定义为一个**恒定的信息量**（固定成交量/成交额），而不是固定的时间长度。
- **推导主线与动机**：从"信息=时钟"到"信息=成交"的范式转换 → Volume Bars（等量信息） → Dollar Bars（等金额信息，消除价格效应） → Imbalance Bars（等方向信息，捕获买卖压力不对称）
- **为什么自然得到此结论**：物理世界中的采样（如地震仪、心电图）早已使用「事件驱动」而非「时钟驱动」——因为有意义的事件才是信息载体，而不是均匀的时间间隔。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

- **题目**：某股票 5 笔逐笔成交数据如下。设 Volume Bar 阈值 $V_{\text{threshold}} = 500$ 股。求出生成的 Volume Bars。

| Tick | 价格 | 成交量 |
|:---|:---:|:---:|
| 1 | 10.00 | 200 |
| 2 | 10.02 | 150 |
| 3 | 10.01 | 300 |
| 4 | 10.03 | 100 |
| 5 | 10.04 | 400 |

- **解题思路与关键步骤**：
  1. 累积成交量：Tick 1→200, Tick 2→350, Tick 3→650 ≥ 500 → **切 Bar 1**（OHLC: 10.00/10.02/10.00/10.01, V=500, 剩余150滚动到下一Bar）
  2. 继续：Tick 3 剩余 150 → Tick 4→250, Tick 5→650 ≥ 500 → **切 Bar 2**（OHLC: 10.01/10.04/10.01/10.04, V=500, 剩余150）

- **最终答案**：2 根 Volume Bars；Bar 1: O=10.00, H=10.02, L=10.00, C=10.01, V=500；Bar 2: O=10.01, H=10.04, L=10.01, C=10.04, V=500
- **易错点**：跨 Tick 切 Bar 时，剩余成交量必须**滚动到下根 Bar**，不能丢弃
- **🤔 追问**：如果这里换成 Dollar Bar 阈值 $D_{\text{threshold}} = 5000$ 元，结果会怎样？

### 例子 2：中等例子（Dollar Bars 消除价格效应）

- **题目与完整解答**：
  股票 A（价格 ~10 元）和股票 B（价格 ~1000 元）都用 Volume Bars（阈值=日均成交量/50），为什么股票 A 每天产生约 50 根 Bar，股票 B 可能只有 20 根？
  
  **解答**：Volume Bars 的阈值以「股数」为单位。股票 B 单价高，同样的「股数」阈值对应于更大的「金额」阈值。如果股票 B 的日均成交金额与 A 相同，但单价高 100 倍，则 B 的日均成交股数是 A 的 1/100，以同样的股数阈值采样，B 的 Bar 数量会远少于 A。
  
  **解决方案**：用 Dollar Bars 替代 Volume Bars。阈值设定为日均成交金额的 1/50，这样无论股票单价高低，每天生成的 Bar 数量大致相同（约 50 根），实现跨资产的统计可比性。

### 例子 3：实际应用例子（Python 实现）

- **实际价值与转化**：

```python
import numpy as np
import pandas as pd

def dollar_bars(tick_df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """
    从 Tick 数据生成 Dollar Bars
    
    Parameters
    ----------
    tick_df : pd.DataFrame
        columns: ['price', 'volume']
    threshold : float
        Dollar Bar 阈值（元）
    
    Returns
    -------
    pd.DataFrame with OHLCV columns
    """
    bars = []
    cum_dollar = 0.0
    o = h = l = c = v = None
    
    for _, row in tick_df.iterrows():
        price, vol = row['price'], row['volume']
        dollar = price * vol
        
        if cum_dollar == 0:
            o = price
            h = price
            l = price
        
        cum_dollar += dollar
        v = (v or 0) + vol
        h = max(h, price)
        l = min(l, price)
        c = price
        
        if cum_dollar >= threshold:
            bars.append({'open': o, 'high': h, 'low': l, 
                        'close': c, 'volume': v, 
                        'cum_dollar': cum_dollar})
            cum_dollar = 0.0
            o = h = l = c = v = None
    
    return pd.DataFrame(bars)

# 示例：用日均成交金额的 1/50 作为阈值
# advr = tick_df['price'].mul(tick_df['volume']).resample('D').sum().mean()
# threshold = advr / 50
# dollar_bars_df = dollar_bars(tick_df, threshold)
```

---

## 8. 常见误区和易混概念

### 误区 1：「Volume Bars 和 Time Bars 只是采样频率不同，统计性质差不多」

- **错误直觉**：以为只是把 1 分钟 K 线换成"每 1000 股 K 线"，统计量应该差不多
- **为什么错**：Time Bars 的收益率序列有显著的**日内季节性自相关**（开盘高波动、午间低波动），Volume Bars 的收益率序列更接近独立同分布（i.i.d.），因为每个 Bar 包含的信息量更均匀
- **正确理解**：Volume Bars 和 Dollar Bars 的收益率序列的**正态性显著优于** Time Bars，自相关性显著低于 Time Bars。这对于后续的协方差矩阵估计和统计检验至关重要。

### 误区 2：「Dollar Bars 和 Volume Bars 区别不大」

- **错误直觉**：成交额 = 价格 × 成交量，二者只是差一个价格因子，差不多
- **为什么错**：如果不做拆股/分红调整，股票价格从 10 元涨到 100 元后，同样的 Volume Bar 阈值（如 10000 股）对应的 Dollar 金额从 10 万变成 100 万，Bar 的生成频率会剧变
- **正确理解**：Dollar Bars 天然对价格变动和公司行为（拆股/分红）具有鲁棒性，是更优的采样选择。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| Time Bars (时间柱) | 固定时间间隔 | 信息量不均匀，有日内季节性 | 传统技术分析、简单回测 |
| Volume Bars (成交量柱) | 固定股数成交量 | 等量信息，消除成交量聚集 | 单品种日内策略 |
| Dollar Bars (金额柱) | 固定成交金额 | 等金额信息，跨品种可比 | 多品种组合策略、协方差估计 |
| Tick Imbalance Bars | 固定买卖不平衡度 | 等方向信息，捕获信息不对称 | 市场微观结构研究、毒性订单流检测 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[OHLCV字段清洗与复权]]：采样前必须确保 Tick 数据的清洗（异常成交量、负价格、时间戳乱序）
- [[订单类型与交易所连续竞价撮合机制 (Order Types & Continuous Double Auction)]]：理解 Tick 方向签名 $b_t$ 的判断依据（Lee-Ready 算法）

### 下游延伸
- [[协方差去噪与随机矩阵理论 RMT (Covariance Denoising & Marchenko-Pastur Law in AFML)]]：Dollar Bars 是生成稳定协方差矩阵的第一步；如果输入数据就有采样偏差，去噪也无济于事
- [[分层风险平价组合 HRP (Hierarchical Risk Parity in AFML)]]：HRP 依赖相关矩阵，Dollar Bars 让不同资产的相关矩阵估计更可靠

### 横向关联
- [[Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)]] ↔ 本概念：最优执行需要精确估计市场冲击，Volume Bars 提供更准确的成交量到达过程建模

### 应用场景
- [[量化金融-GARCH波动率策略]]：用 Dollar Bars 替代 Time Bars 作为 GARCH 输入，消除时间柱的波动率聚类伪影

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
- [ ] 1. 用一句话说清楚信息驱动采样解决什么问题。
- [ ] 2. 用直觉语言解释它（«"这东西其实就像……"»）。
- [ ] 3. 写出 Volume Bar 和 Dollar Bar 的切 Bar 条件公式。
- [ ] 4. 解释 Tick Imbalance Bar 中 $b_t$ 和 $\theta_T$ 的含义。
- [ ] 5. 解释为什么 Dollar Bars 比 Volume Bars 更优。
- [ ] 6. 讲出"信息=成交"范式转换的推导主线。
- [ ] 7. 手算做出例子 1 的跨 Tick 切 Bar 过程。
- [ ] 8. 说出 Time Bars 和 Volume Bars 在自相关性上的关键区别。
- [ ] 9. 说出它和协方差矩阵估计、HRP 的关系。
- [ ] 10. 说出一个实际策略中替换 Time Bars 为 Dollar Bars 的场景。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 四种 Bar 的定义与区别 |
| 2 | 公式运用 | 基础 | Volume Bar 阈值计算 |
| 3 | 条件判断 | 中等 | 何时用 Dollar Bars vs Volume Bars |
| 4 | 变式/综合 | 中等 | 跨 Tick 切 Bar 的边界处理 |
| 5 | 开放/证明/建模 | 较难 | 设计 Tick Imbalance Bar 并验证统计性质 |

### 题目与解析

#### 1. 四种信息驱动 Bars 的核心区别
> [!question]- 答案解析
> - **答案**：Volume Bars 固定成交量（股）；Dollar Bars 固定成交金额（元）；Tick Imbalance Bars 固定买卖方向不平衡度；Volume Imbalance Bars 固定成交量加权的不平衡度。
> - **解析**：核心差异在于"固定的量"不同。Volume/Dollar Bars 关注信息量，Imbalance Bars 关注信息方向。
> - **易错原因**：混淆 Imbalance Bars 的阈值定义——不是固定 Tick 数量，而是固定不平衡度的累积。
> - **对应误区**：误区 1（以为只是采样频率不同）
> - **Obsidian 标签建议**：`#自测题/基础`

#### 2. Volume Bar 阈值计算
> [!question]- 答案解析
> - **答案**：$V_{\text{threshold}} = \text{ADV} / N$，其中 ADV = 近 20 日日均成交量，N = 期望每日 Bar 数（如 50）。
> - **解析**：阈值需要滚动更新以避免前瞻偏差。典型 N=50 意味着每天大约产生 50 根 Bar。

#### 3. Dollar Bars vs Volume Bars 选择
> [!question]- 答案解析
> - **答案**：多品种组合策略（跨价格量级）→ Dollar Bars；单品种日内策略 → Volume Bars 可接受；需要跨时间比较（有拆股历史）→ Dollar Bars。
> - **解析**：Dollar Bars 对价格水平变化具有天然鲁棒性，Volume Bars 在价格变动后需要重新校准阈值。

#### 4. 跨 Bar 剩余成交量的滚动处理
> [!question]- 答案解析
> - **答案**：当累积量超过阈值时，超出的部分必须**滚动到下一根 Bar**，作为下一根 Bar 的第一笔成交。
> - **解析**：$v_{\text{remain}} = V_{\text{cum}} - V_{\text{threshold}}$，下一根 Bar 的 OHLC 以该 Tick 的价格同时作为开盘价。

#### 5. 开放题：设计 Tick Imbalance Bar 阈值
> [!question]- 答案解析
> - **答案**：使用指数加权移动平均（EWMA）动态更新期望不平衡度 $E_0[|\sum b_t|]$：
>   $$E_{T+1}[|\sum b|] = (1 - \alpha) \cdot E_T[|\sum b|] + \alpha \cdot |\sum_{t=1}^{T} b_t|$$
>   当 $|\sum b_t| \geq E_T[|\sum b|]$ 时切 Bar。$\alpha$ 典型值 0.01-0.05。
> - **解析**：EWMA 让阈值自适应市场状态的变化（如波动率上升时信息流入加速）。

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

### 我的推导复现
> 不看上文，尝试写出核心公式或推导主线：

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/`
- **关联已有笔记**：`[[OHLCV字段清洗与复权]]` `[[订单类型与交易所连续竞价撮合机制 (Order Types & Continuous Double Auction)]]` `[[协方差去噪与随机矩阵理论 RMT (Covariance Denoising & Marchenko-Pastur Law in AFML)]]` `[[分层风险平价组合 HRP (Hierarchical Risk Parity in AFML)]]`
- **建议标签**：`#学习` `#量化金融` `#数据工程` `#采样`
- **拆分建议**：Tick Imbalance Bars 可在积累 5+ 个实际案例后拆出独立卡，当前先放在本卡作为变体

## 🃏 Anki 卡片

- 信息驱动采样的核心范式转换是什么？ :: 从"信息=时钟"到"信息=成交"的范式转换——采样频率与市场信息流入速度同步，而非与墙上时钟同步。
- Volume Bars 的切 Bar 条件是什么？ :: 累计成交量 $V_{\text{cum}} = \sum v_i \geq V_{\text{threshold}}$ 时切 Bar，阈值通常 = ADV/N。
- Dollar Bars 比 Volume Bars 的核心优势是什么？ :: Dollar Bars 自动适应股票价格变动和公司行为（拆股/分红），跨品种、跨时段统计可比。
\n\n> ⚔️ **支线实战任务 (Side Quest)**：👉 点击进入 [[[支线任务] HW09-DollarBars采样引擎]] 刷怪通关！\n