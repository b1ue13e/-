---
title: Meta-labeling 二级标签与元标注 (Meta-labeling in Financial ML)
type: concept
topic: Meta-labeling
created: '{date}'
status: ongoing
difficulty: advanced
course: 量化金融
importance: A
tags: 
concept: []
prerequisites: []
related: []
upstream: 
downstream: 
date: 2026-07-23
---

# Meta-labeling 二级标签与元标注 (Meta-labeling in Financial ML)

---

## 0. 先判断它值不值得深挖

**分类：A 类（核心概念，必须深挖）**

**理由：**
Meta-labeling（元标注）是由 Marcos López de Prado 在《Advances in Financial Machine Learning (AFML)》中提出的颠覆性机器学习量化框架。它解决了金融领域直接用机器学习预测价格方向（看涨/看跌）效果极差的难题。通过将“预测方向（Side）”与“预测胜率/下注规模（Size）”解耦，用基础模型（如均线/突破/RSI）决定买卖方向，而用二次机器学习模型（Meta-model）决定“要不要下单以及下单多大”，大幅提高了夏普比率并降低了假阳性（False Positives）交易。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**

假设你训练了一个随机森林（Random Forest）模型去直接预测明天的股票是涨还是跌（分类 1 或 -1）。
在金融高噪声数据上，这个分类器的准确率（Accuracy）通常只有可怜的 $51\% \sim 53\%$。
由于交易手续费和滑点的存在，直投这个模型会导致回测曲线一路向下溃败。

**以前的方法在哪里卡住：**
1. **强行要求 ML 解决所有问题**：让分类器同时决定“什么时候买、买什么方向、能赚多少钱”，模型复杂度极高，极易在金融低信噪比数据上**严重的过拟合 (Overfitting)**。
2. **忽视假阳性（False Positive）成本**：传统指标 Recall（召回率）较高，但 Precision（精准率）低，导致触发了大量微弱且不赚钱的频繁交易，手续费吞噬了所有利润。

**为什么必须引入 Meta-labeling：**
将任务一分为二：
- **主模型（Primary Model）**：专注高召回率（High Recall）。使用经典量化规则（如均线交叉、突破、基本面规则）生成交易信号方向 $Side \in \{-1, 1\}$。
- **元模型（Meta-Model）**：专注高精准率（High Precision）。只预测主模型给出的信号**到底是真盈利（1）还是假信号（0）**。

**它到底解决了哪类问题：**
解决了**金融机器学习中直接分类准确率低、过拟合严重，以及传统策略假阳性交易过多吞噬利润**的问题。

---

## 2. 为什么它重要？它有什么用？

- **体系与大图景**：金融机器学习（AFML 框架）的核心算力分配枢纽，连接传统规则策略与现代化 ML 下注引擎。
- **量化与实操应用**：
  1. **过滤假突破（Filter False Breakouts）**：当传统动量突破策略发出买入信号时，元模型结合当前波动率、订单流不平衡（OFI）与微观结构特征，判断这次突破是真突破还是假突破。
  2. **决定下注规模（Bet Sizing）**：元模型输出的概率 $P(y=1)$ 直接作为 Sigmoid 函数的输入，用于计算最佳仓位权重 $Size = 2 P(y=1) - 1$。

---

## 3. 学它之前需要哪些前置知识？

1. **[[Purged CV]]**：理解金融时间序列交叉验证中的重叠消除（Purging）与净化（Embargoing）。
2. **[[标签设计]]**：理解三重屏障法（Triple-Barrier Method）生成止盈、止损与到期标签。
3. **最小必要背景（混淆矩阵 Confusion Matrix）**：
   > - **Precision (精准率)**：TP / (TP + FP)，预测为真里实际真的比例。
   > - **Recall (召回率)**：TP / (TP + FN)，实际为真里被找出来的比例。

---

## 4. 用直觉语言解释它

### 生活类比：主裁判与视频助理裁判 (VAR)

- **主模型（主裁判）**：眼神好，看球场上任何疑似犯规就立刻吹哨（高 Recall，宁可错吹，绝不漏吹）。
- **元模型（VAR 视频助理裁判）**：在主裁判吹哨后，慢动作放大了看这一脚**到底是真犯规（1）还是假摔（0）**。如果判断是假摔，取消罚球！

**Meta-labeling 的直觉本质**：
主模型负责“寻找所有潜在的机会”，元模型负责“对这些机会进行打分过滤”，剔除里面的渣滓和假信号。

«“Meta-labeling 不是让 AI 猜涨跌，而是让 AI 帮传统策略剔除假信号，只在胜率极高时才下注。”»

---

## 5. 正式定义、核心公式、符号解释

### 核心定义
**Meta-labeling（元标注）**：指在主模型生成方向信号 $S_t \in \{-1, 0, 1\}$ 的基础上，重新构造二分类目标变量 $Y_t \in \{0, 1\}$（若主信号最终盈利则 $Y_t=1$，亏损则 $Y_t=0$），并训练二次机器学习模型对主信号进行二阶段真实性预测与仓位调控的方法。

### 核心公式

#### 1. 二级标签定义 ($Y_t^{meta}$)
已知主模型给出的方向为 $\hat{y}_t \in \{-1, 1\}$，资产实际收益率为 $r_t$：
$$Y_t^{meta} = \begin{cases} 1, & \text{if } r_t \cdot \hat{y}_t > 0 \quad (\text{主模型方向正确，盈利}) \\ 0, & \text{if } r_t \cdot \hat{y}_t \le 0 \quad (\text{主模型方向错误，亏损}) \end{cases}$$

#### 2. 最终复合交易指令与下注规模
$$\text{Final Signal}_t = \hat{y}_t \cdot I\left( P(Y_t^{meta} = 1 \mid X_t) > p^*$ \right)$$
$$\text{Bet Size}_t = \text{sign}(\hat{y}_t) \times \max\left(0, \frac{P(Y_t^{meta}=1) - \frac{1}{2}}{\frac{1}{2}}\right)$$

### 符号解释表

| 符号 | 含义 | 维度/量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\hat{y}_t$ | 主模型生成的原始方向信号 | $\{-1, 1\}$ | 来自均线/布林带/突破规则 |
| $Y_t^{meta}$ | 元模型的训练二分类目标 | $\{0, 1\}$ | 1 代表主信号盈利，0 代表亏损 |
| $X_t$ | 传递给元模型的特有特征集 | 多维向量 | 如波动率、流动性、订单流等 |
| $P(Y_t^{meta}=1)$ | 元模型估计的成功概率 | $[0, 1]$ | 由 XGBoost / Random Forest 输出 |
| $p^*$ | 下注门槛概率阈值 | $[0.5, 1.0]$ | 常用 $0.6 \sim 0.7$ |

---

## 6. 推导思路和思想来源

### 为什么 Meta-labeling 能大幅提升夏普比率？
1. **防止特征滥用与过拟合**：如果把技术指标、宏观数据、微观结构全部塞进一个决策树去预测涨跌，树的深度会极深，导致严重过拟合。
2. **转念（分工明确）**：
   - 规则模型已经包含了人对市场宏观经济逻辑的先验理解（例如：均线向上金叉大概率趋势向上）。
   - 机器学习模型（Meta-model）只需要学习“在何种波动率和微观结构下，这个金叉容易失效”。模型只需要做简单的二分类（0/1 过滤），复杂度大幅降低！
3. **提高了 F1-Score / Precision**：大大减少了在震荡市里被频繁频繁止损（False Positive）导致的佣金消耗。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算例题（Meta-labeling 标签生成）

**题目**：
主模型（双均线交叉）在连续 4 天给出了如下买卖方向 $\hat{y}_t$。股票未来真实收益率 $r_t$ 如下：
- $t=1$: 主模型给出 $\hat{y}_1 = +1$ (做多)，实际收益率 $r_1 = +2.5\%$
- $t=2$: 主模型给出 $\hat{y}_2 = +1$ (做多)，实际收益率 $r_2 = -1.2\%$
- $t=3$: 主模型给出 $\hat{y}_3 = -1$ (做空)，实际收益率 $r_3 = -3.0\%$
- $t=4$: 主模型给出 $\hat{y}_4 = -1$ (做空)，实际收益率 $r_4 = +1.5\%$

计算元模型训练需要的二级标签序列 $Y^{meta}$。

**解答过程**：
1. $t=1$: $r_1 \cdot \hat{y}_1 = (+2.5\%) \times (+1) = +2.5\% > 0 \implies Y_1^{meta} = 1$
2. $t=2$: $r_2 \cdot \hat{y}_2 = (-1.2\%) \times (+1) = -1.2\% \le 0 \implies Y_2^{meta} = 0$
3. $t=3$: $r_3 \cdot \hat{y}_3 = (-3.0\%) \times (-1) = +3.0\% > 0 \implies Y_3^{meta} = 1$
4. $t=4$: $r_4 \cdot \hat{y}_4 = (+1.5\%) \times (-1) = -1.5\% \le 0 \implies Y_4^{meta} = 0$
5. 结果：二级标签为 $[1, 0, 1, 0]$。

---

### 例子 2：中等例题（根据元模型概率确定下注仓位）

**题目**：
设元模型输出了某次做多信号的成功概率 $P(Y^{meta}=1) = 0.80$。
主模型方向 $\hat{y} = +1$。
按照公式 $\text{Bet Size} = 2 P - 1$ 计算建议建仓规模比例（假设全仓为 1.0）。若成功概率降至 $0.45$，下注规模是多少？

**解答过程**：
1. 当 $P = 0.80$ 时：
   $$\text{Bet Size} = 2 \times 0.80 - 1 = 1.6 - 1.0 = +0.60 \quad (60\% \text{ 仓位做多})$$
2. 当 $P = 0.45 < 0.50$ 时：
   由于概率低于 $0.50$，元模型认为主信号大概率是假信号，
   $$\text{Bet Size} = \max(0, 2 \times 0.45 - 1) = \max(0, -0.1) = 0.0 \quad (0\% \text{ 仓位，直接放弃交易})$$

---

### 例子 3：实际应用（Python 搭建 Meta-labeling 训练流水线）

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# 假设主模型生成了原始信号 primary_signal (1, -1, 0)
np.random.seed(42)
N = 1000
primary_signal = np.random.choice([1, -1], size=N)
market_returns = np.random.normal(0.0002, 0.01, size=N)

# 1. 构造 Meta-label
meta_labels = ((primary_signal * market_returns) > 0).astype(int)

# 2. 构造特征矩阵 (如过去波动率、RSI)
X_features = np.random.normal(0, 1, (N, 5))

# 3. 训练 Meta-Model (随机森林)
meta_model = RandomForestClassifier(n_estimators=50, max_depth=3)
meta_model.fit(X_features[:800], meta_labels[:800])

# 4. 预测样本外概率并下注
pred_probs = meta_model.predict_proba(X_features[800:])[:, 1]
final_positions = primary_signal[800:] * (pred_probs > 0.6)

print("被过滤掉的非高胜率交易比例:", np.mean(final_positions == 0))
```

---

## 7.5 💥 课本挂载与工业级实战模块 (Textbook Mapping & Production Lab)

### 7.5.1 📚 经典课本章节锚定
- **教材挂载 1**：Marcos López de Prado *《Advances in Financial Machine Learning (金融机器学习精要)》* 第 3 章 "Financial Labels" 与 第 10 章 "Bet Sizing"。
  - **课本必读重点**：Triple-Barrier 法生成主事件、Secondary Classification (Meta-labeling) 二级标签定义。
  - **推荐课后代码 Lab**：AFML Chapter 3 Snippet 3.1 ~ 3.4（Python Triple-Barrier & Meta-label Generator）。
- **教材挂载 2**：Stefan Jansen *《Machine Learning for Algorithmic Trading》* 第 7 章 "Linear Models" - Meta-labeling Strategies.
  - **实战挂载重点**：利用 Random Forest 作为 Meta-Classifier 过滤布林带均值回归假突破。

### 7.5.2 ⚙️ 工业级 Python 最小可运行实战脚手架
包含：唐奇安通道主模型信号生成、Triple-Barrier 收益回溯、Meta-label 二级标签合成与 Random Forest 元分类器评估。

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

def run_metalabeling_production_lab():
    # 1. 模拟行情数据 (5000 个时点)
    np.random.seed(42)
    close = 100.0 + np.cumsum(np.random.normal(0.02, 1.0, 5000))
    df = pd.DataFrame({'close': close})
    
    # 2. 传统主模型：20 日唐奇安通道突破策略 (Primary Model)
    df['upper'] = df['close'].rolling(20).max().shift(1)
    df['lower'] = df['close'].rolling(20).min().shift(1)
    
    df['primary_signal'] = 0
    df.loc[df['close'] > df['upper'], 'primary_signal'] = 1   # 看涨突破
    df.loc[df['close'] < df['lower'], 'primary_signal'] = -1  # 看跌突破
    
    # 筛选出主模型触发信号的事件点
    events = df[df['primary_signal'] != 0].copy()
    if len(events) < 50:
        print("信号事件不足，无法训练 Meta-model")
        return
        
    # 3. 构造 5 日后的真实收益与 Meta-label 二级标签 (Secondary Labeling)
    # 收益率 r_t = (close_{t+5} - close_t) / close_t
    events['future_return'] = (df['close'].shift(-5) - df['close']) / df['close']
    events.dropna(inplace=True)
    
    # 元标签：主模型预测方向与真实收益方向一致，则 Meta-label = 1，否则 = 0
    events['meta_label'] = (events['primary_signal'] * events['future_return'] > 0).astype(int)
    
    # 4. 构建特征工程 (用于元分类器的特征)
    events['volatility_20'] = df['close'].pct_change().rolling(20).std()
    events['rsi_14'] = 50.0 + 10.0 * np.random.randn(len(events)) # 简化的微观特征
    events.dropna(inplace=True)
    
    features = ['volatility_20', 'rsi_14']
    X = events[features]
    y = events['meta_label']
    
    # 5. 训练二次分类器 (Random Forest Meta-Classifier)
    split = int(len(X) * 0.7)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    
    meta_clf = RandomForestClassifier(n_estimators=50, max_depth=3, random_state=42)
    meta_clf.fit(X_train, y_train)
    
    y_pred_prob = meta_clf.predict_proba(X_test)[:, 1]
    
    print("=== Meta-labeling 工业级实战 Lab 结果 ===")
    print(f"训练集样本数: {len(X_train)} | 测试集样本数: {len(X_test)}")
    print(f"元模型 AUC ROC 得分: {roc_auc_score(y_test, y_pred_prob):.4f}")
    print(f"主模型基础胜率: {y_test.mean():.2%}")
    print(f"通过 Meta-labeling (概率 > 0.6) 过滤后的优化胜率: {y_test[y_pred_prob > 0.6].mean():.2%}")

run_metalabeling_production_lab()
```

### 7.5.3 ⚠️ 实盘落地“踩坑指南”与回测陷阱
1. **未处理持仓重叠引发的信息泄漏 (Overlapping Sample Bias)**：
   若主模型持仓 5 天，那么 $t$ 时刻与 $t+1$ 时刻的 Meta-label 包含了高度重叠的未来价格走势。直接放入标准 CV 会导致极严重的过拟合。必须使用 **Purged CV 与 Embargoing 隔离**。
2. **类别极度不平衡 (Class Imbalance)**：
   如果主模型本身质量极差，胜率只有 10%，则 Meta-label 中 1 的比例极低。此时分类器可能简单倾向于全预测为 0。必须使用 **Balanced Random Forest 或 Class Weight 补偿**。
3. **特征污染 (Feature Contamination)**：
   元模型使用的特征（如 Volatility, RSI）必须是在主模型触发信号的 $t$ 时刻完全可获得的实时特征，绝不能包含 $t+1$ 之后的未来的统计量。

### 7.5.4 📊 实战性能评估指标体系
- **假阳性过滤率 (False Positive Reduction Rate)**：被元模型成功拦截的亏损交易占比。
- **精确度-召回率曲线 AUC (PR-AUC)**：评估元模型在类别不平衡下的真实辨识力。
- **过滤后夏普比率提升度 (Sharpe Improvement)**：$\Delta Sharpe = Sharpe_{meta} - Sharpe_{primary}$。

### 7.5.5
> 🔓 **作业解锁前置条件**：学完 [[收益率与对数收益率]] + [[Meta-labeling]] 即可正式解锁本 Challenge 实战！
> 💡 **解锁指引**：理解 Meta-labeling 的核心定义与基本推导逻辑后即可解锁。

 🧪 拓展实验与李宏毅式实战 Challenge 题 (Lab Assignment: Meta-labeling 工业级实战 challenge)

本作业参考 **李宏毅 (Hung-yi Lee) 教授 ML 课程作业架构** 设计，设置四个渐进式难度基线 (Baselines)：

- 🟢 **简单基线 (Simple Baseline)**：
  - **任务要求**：理解 Meta-labeling 的核心数学定义，使用 Python 进行基础验证与数据提取。
  - **达标标准**：代码无 Error 跑通，输出基础结果。

- 🟡 **中等基线 (Medium Baseline)**：
  - **任务要求**：实现 Meta-labeling 的完整向量化代码框架，在历史数据上拟合参数并校验稳定度。
  - **达标标准**：完成核心算法的向量化与参数校准，模型表现达到基线水平。

- 🔴 **强基线 (Strong Baseline)**：
  - **任务要求**：引入严格的防前视偏差、手续费扣除与 Purged 交叉验证，使基于 Meta-labeling 的模块表现击败基线。
- **达标标准**：使用预先固定的数据、时间切分、基准与成本口径完成样本外比较；改进必须同时报告效应大小、风险变化和失败案例，不设跨数据集通用收益阈值。

- 🟣 **Boss 基线 (Kaggle / 实盘级基线)**：
  - **任务要求**：结合真实工业级实盘环境（如高频盘口/高维去噪/强化学习），达成实盘级夏普比率与风险控制指标。
- **达标标准**：完成预先注册的过拟合、样本外与压力测试；报告 PBO 的切分方案、不确定性和阈值敏感性，不把单一候选阈值当作跨市场通用上线标准。


## 8. 常见误区与易混概念

### 误区 1：Meta-labeling 可以独立使用，不需要主模型

错误直觉：“既然 Meta-labeling 这么强大，我可以不用任何均线规则，直接用 Meta-labeling 算出一切。”  
为什么错：Meta-labeling 必须依赖主模型给出的 $Side \in \{-1, 1\}$ 才能构建二分类目标 $Y = \text{sign}(r \cdot Side)$。没有主模型，就没有元模型。  
正确理解：**Meta-labeling 是一种“附属于传统/规则策略”的二阶段优化滤镜。**

### 概念对比：直接 ML 分类 vs Meta-labeling 架构

| 维度 | 直接 ML 分类 (Direct Classification) | Meta-labeling 二阶段架构 |
| :--- | :--- | :--- |
| **预测目标** | 预测价格涨跌 $\{-1, 1\}$ | 预测主模型信号**是否会盈利** $\{0, 1\}$ |
| **主模型角色** | 无（全由 ML 替代） | 由领域知识/传统量化规则担任 |
| **过拟合倾向** | 极高（在低信噪比金融数据上崩塌） | 低（降低了 ML 模型的任务维度） |
| **交易频率与费率** | 高频随机触发，被手续费吞噬 | 低频高质量触发，仅在概率高时下注 |

---

## 9. 相关知识点与 Obsidian 双链建议

请帮我建立知识网络。

注意：不要只列链接。每个链接后面必须用一句话说明“为什么要链接”。

上游依赖

- [[Purged CV]]：提供基础概念与理论推导支撑。
- [[标签设计]]：提供基础概念与理论推导支撑。
- [[树模型基线]]：提供基础概念与理论推导支撑。

下游延伸

- [[下注规模]]：进一步延伸拓展该知识点的应用场景与模型构建。
- [[止损与仓位]]：进一步延伸拓展该知识点的应用场景与模型构建。

横向关联

- [[收益率与对数收益率]]：衡量资产收益特性的基础量纲。
- [[实盘风控]]：风险控制与投资组合保护。

应用场景

- [[实盘风控]]：工业级量化策略风控与组合风险度量。


## 10. 闭卷复现任务

1. [ ] 默写 Meta-labeling 的二级标签 $Y^{meta}$ 的数学定义。
2. [ ] 用“主裁判与 VAR”解释 Meta-labeling 的直觉分工。
3. [ ] 说明为什么 Meta-labeling 能有效减少假阳性（False Positive）交易。
4. [ ] 写出利用元模型概率映射到下注规模（Bet Size）的公式。
5. [ ] 列出直接 ML 分类与 Meta-labeling 架构的 2 个核心区别。

---

## 11. 自测题（5 道）

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | Meta-label 标签的取值范围 |
| 2 | 公式运用 | 基础 | 手算二级标签 $Y^{meta}$ |
| 3 | 条件判断 | 中等 | 主模型只给 0 信号时元模型的处理 |
| 4 | 变式/综合 | 中等 | 基于概率 $P$ 进行仓位 Scale 映射 |
| 5 | 开放/建模 | 较难 | 在 Meta-labeling 中处理类不平衡（Class Imbalance）的采样技巧 |

---

### 第 1 题：概念辨析（基础）
**题目**：在 Meta-labeling 架构中，元模型（Meta-model）的输出变量类型是什么？

> [!question]- 答案解析
> **答案**：二分类变量（0 或 1），代表主模型给出的信号在扣除或考虑收益后是否盈利（1 代表正确/盈利，0 代表错误/亏损）。  
> **Obsidian 标签**：`#自测题/MetaLabeling`

---

### 第 2 题：公式运用（基础）
**题目**：主模型建议做空某股票（$\hat{y} = -1$），扣除费用后该股票实际价格下跌了 $3.0\%$（$r = -3.0\%$）。求对应的元标签 $Y^{meta}$。

> [!question]- 答案解析
> **答案**：
> $r \cdot \hat{y} = (-3.0\%) \times (-1) = +3.0\% > 0$。
> 因为做空盈利，所以 $Y^{meta} = 1$。  
> **Obsidian 标签**：`#自测题/元标签计算`

---

### 第 3 题：条件判断（中等）
**题目**：判断：“在训练元模型时，我们可以把全样本中所有未触发主模型信号（$\hat{y}_t = 0$）的时间点也加入训练集。”

> [!question]- 答案解析
> **答案**：错误。元模型的目标是评估“已经发出的信号的质量”。当主模型未发出信号（$\hat{y}_t = 0$）时，不存在需要过滤的信号。因此，训练集必须**严格筛选为主模型发出非零信号的时间节点**。  
> **Obsidian 标签**：`#自测题/元模型训练集`

---

### 第 4 题：变式/综合（中等）
**题目**：假设元模型预测某买入信号盈利的概率 $P=0.75$。如果使用分段下注策略：当 $P < 0.60$ 时不下注，当 $P \ge 0.60$ 时按线性调整比例 $\text{Size} = \frac{P - 0.60}{0.40}$ 下单。求此时的下注仓位比例。

> [!question]- 答案解析
> **答案**：
> 因为 $P = 0.75 \ge 0.60$：
> $\text{Size} = \frac{0.75 - 0.60}{0.40} = \frac{0.15}{0.40} = 0.375$ （即使用 $37.5\%$ 仓位下单）。  
> **Obsidian 标签**：`#自测题/下注映射`

---

### 第 5 题：开放/建模（较难）
**题目**：为什么在金融市场中，主模型发出的信号通常存在严重的“盈利/亏损类不平衡”（比如只有 20% 的信号盈利）？元模型如何通过 Adjusting Class Weights 或 SMOTE 应对这一问题？

> [!question]- 答案解析
> **解析**：
> 1. **类不平衡根源**：金融数据信噪比极低，绝大部分交易信号会被震荡噪声磨损，导致 $Y^{meta}=1$ 的样本比例显著低于 $Y^{meta}=0$。
> 2. **后果**：直接训练的机器学习模型会偏向预测全为 0，失去过滤能力。
> 3. **解决方案**：在元模型（如 XGBoost）中设置 `scale_pos_weight`（将少数类 $Y=1$ 的权重调高），或者在样本空间对 $Y^{meta}=1$ 实施 SMOTE 过采样，提高模型对高胜率特征的敏感度。  
> **Obsidian 标签**：`#自测题/类不平衡处理`

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

- **适合文件夹**：`02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/`
- **建议双链**：[[Purged CV]]、[[下注规模]]、[[标签设计]]
- **标签**：`#学习` `#量化金融` `#金融机器学习` `#MetaLabeling` `#AFML` `#下注规模`

---

<!-- quant-evidence-v3 -->
## 可定位依据与失效复核

本卡的复核对象是 **Meta-labeling**，而不是只复述一个公式。对 **Meta-labeling** 的独立验证重点是：主模型只决定方向，二级模型只决定是否下注；用 out-of-fold 概率避免标签回灌。

### 权威来源与定位

1. scikit-learn 官方 Common pitfalls（数据泄漏与预处理边界）：https://scikit-learn.org/stable/common_pitfalls.html。用于复核“主模型只决定方向，二级模型只决定是否下注；用 out-of-fold 概率避免标签回灌”。
2. scikit-learn `TimeSeriesSplit` 官方 API：https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html。用于复核“主模型只决定方向，二级模型只决定是否下注；用 out-of-fold 概率避免标签回灌”。
3. Marcos López de Prado, *Advances in Financial Machine Learning*, Wiley, ISBN 9781119482086, Chapter 3、Chapter 7 与 Chapter 11。用于复核“主模型只决定方向，二级模型只决定是否下注；用 out-of-fold 概率避免标签回灌”。

### 失效边界与验收协议

- **成立条件**：先写清数据时点、估计窗口、交易摩擦和分布/市场结构假设，再运行模型。
- **反例压力测试**：主模型只决定方向，二级模型只决定是否下注；用 out-of-fold 概率避免标签回灌。
- **最小实验**：固定随机种子或冻结原始数据快照，同时保存基线、破坏条件后的对照组、关键中间量与失败日志。
- **通过标准**：结论必须在样本外仍保持方向一致；若成本、延迟、参数扰动或结构突变使结论反转，就把该情形登记为适用边界而不是删除失败结果。
