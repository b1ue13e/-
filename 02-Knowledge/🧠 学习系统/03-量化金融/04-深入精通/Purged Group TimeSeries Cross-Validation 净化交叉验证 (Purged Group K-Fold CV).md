---
title: Purged Group TimeSeries Cross-Validation 净化交叉验证
type: concept
topic: Purged CV
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

# Purged Group TimeSeries Cross-Validation 净化交叉验证 (Purged Group K-Fold CV)

---

## 0. 先判断它值不值得深挖

**分类：A 类（核心概念，必须深挖）**

**理由：**
Purged Group TimeSeries Cross-Validation（净化与隔离交叉验证）是 Marcos López de Prado 专门针对金融时间序列机器学习提出的验证框架。传统的 $K$-Fold 随机交叉验证在金融领域是**致命毒药**，因为金融数据存在严重的时间重叠（Overlapping Labels）与序列相关性，直接使用标准 $K$-Fold 会造成严重的**样本泄漏（Data Leakage / Look-ahead Bias）**，导致模型回测效果极其优异、实盘瞬间爆仓。掌握 Purging（消除重叠）与 Embargoing（隔离带）是金融 ML 的生死红线。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**

假设你正在使用 500 天的数据训练一个预测股票未来 5 天收益率的机器学习模型。
你习惯性地使用了 Python `scikit-learn` 里的标准 `KFold(n_splits=5, shuffle=True)`：
把 500 天的数据打乱，随机抽取 80% 作为训练集，20% 作为测试集。

**以前的方法在哪里卡住：**
打乱数据（Shuffle）后，测试集中第 $t$ 天的预测目标 $Y_t$ 包含了从 $t$ 到 $t+5$ 天的持仓收益；而训练集中恰好随机抽中了第 $t+2$ 天的数据！
训练集在预测 $t+2$ 天时，已经使用了 $t+2$ 到 $t+7$ 天的价格。**模型偷看了测试集未发生的未来价格信息**！在交叉验证中，模型的 AUC 达到 0.95，回测曲线近乎直线；但一上实盘，表现惨不忍睹。

**为什么必须引入 Purged Group CV：**
1. **Purging（清除重叠）**：删除训练集中所有在时间上与测试集样本标签产生交集的样本。
2. **Embargoing（隔离带）**：在测试集之后强制插入一段“冷藏缓冲区”（如 5~10 天），消除高自相关性带来的信息滞后泄漏。

**它到底解决了哪类问题：**
解决了**金融重叠标签与时间序列自相关导致的严重样本泄漏、前视偏差及虚假高夏普比率**问题。

---

## 2. 为什么它重要？它有什么用？

- **体系与大图景**：金融机器学习（AFML）的模型评估基石，连接数据清洗（标签设计）与模型定型（特征重要性/Meta-labeling）。
- **量化与实战应用**：
  1. **防止策略虚假过拟合**：准确评估机器算法在样本外的真实预测能力，杜绝“回测是神、实盘是狗”的尴尬局面。
  2. **正确评估特征重要性 (MDI / MDA)**：只有在严格 Purged 的 CV 环境下，算出的特征重要性（Feature Importance）才是真实的。

---

## 3. 学它之前需要哪些前置知识？

1. **[[样本泄漏]]**：理解机器学习中训练集获取测试集未来信息的概念。
2. **[[Meta-labeling 二级标签与元标注 (Meta-labeling in Financial ML)|标签设计]]**：理解三重屏障法（Triple-Barrier Method）中每个样本点都有开始时间 $t_{1,i}$ 与结束到期时间 $t_{2,i}$。
3. **最小必要背景（标准 K-Fold CV）**：
   > **$K$-Fold**：将数据集分成 $K$ 份，依次取 1 份作为测试集，剩余 $K-1$ 份作为训练集。但在金融时间序列中不能打乱顺序。

---

## 4. 用直觉语言解释它

### 生活类比：防止考试泄题的“隔离考场与手机封存”

假设你要举办一场期末考试（测试集）：
- **传统 K-Fold 随机打乱** 就像：让参加考试的学生和刚刚考完拿到标准答案的学生混坐在一个考场里（训练集与测试集重叠），甚至允许他们交头接耳。考出来的成绩全都是满分（虚假的高准确率）。
- **Purging（清除重叠）** 就像：在考试开始前，把所有提前看过试卷或参与过命题的学生（时间重叠的样本）全部赶出考场。
- **Embargoing（隔离带）** 就像：考完试后，为了防止试题被传播给下一场考生，强制将考生在隔离室里关 2 个小时（在测试集结束后截断一段缓冲区）。

«“Purging 是把时间上有重叠的训练样本删掉；Embargoing 是在测试集后面画一条防泄漏的隔离带。”»

---

## 5. 正式定义、核心公式、符号解释

### 核心定义
**Purged & Embargoed Cross-Validation（净化与隔离交叉验证）**：一种专门针对时间序列与重叠标签数据的交叉验证方法。通过在划分训练集与测试集时，依据样本的时间区间 $[t_{1,i}, t_{2,i}]$ 剔除与测试集发生重叠的训练样本（Purging），并在测试集结束时间后插入固定窗口的隔离带（Embargoing），确保训练集与测试集在时间上的彻底独立。

### 核心逻辑与算子

#### 1. Purging 条件（训练样本 $i$ 被剔除的判定）
设测试集时间区间为 $[T^{test}_{start}, T^{test}_{end}]$。
对于训练集中的某个样本 $i$，其发起时间为 $t_{1,i}$，标签到期时间为 $t_{2,i}$。
若样本 $i$ 满足以下任一条件，必须从训练集中 **Purge (剔除)**：
1. $t_{1,i} \le T^{test}_{start} \le t_{2,i}$ （训练样本到期前测试集已开始）
2. $t_{1,i} \le T^{test}_{end} \le t_{2,i}$ （训练样本发起在测试集结束前）
3. $T^{test}_{start} \le t_{1,i} \le t_{2,i} \le T^{test}_{end}$ （训练样本完全落在测试集内部）

#### 2. Embargoing 条件（隔离带）
在测试集结束点 $T^{test}_{end}$ 之后，强制剔除训练集中所有发起时间 $t_{1,i} \in [T^{test}_{end}, T^{test}_{end} + h]$ 的样本，其中 $h$ 为 Embargo 窗口长度（通常取总样本量的 $1\% \sim 5\%$）。

### 符号解释表

| 符号 | 含义 | 维度/量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $t_{1,i}$ | 样本 $i$ 的特征产生/开仓时间 | 时间戳 | 样本起始点 |
| $t_{2,i}$ | 样本 $i$ 的止盈/止损/到期时间 | 时间戳 | 样本结束点 |
| $[T^{test}_{start}, T^{test}_{end}]$ | 测试集的时间区间 | 时间范围 | 当前 Fold 的评估区间 |
| $h$ | Embargo 隔离带长度 | 天数/百分比 | 防止测试集后方 AR(1) 记忆泄漏 |

---

## 6. 推导思路和思想来源

### 为什么 Purging 和 Embargoing 缺一不可？

```
时间轴 ─────────────────────────────────────────────────────────>
[ 训练集 A ] ── Purge ──> [ 测试集 Test ] ── Embargo ──> [ 训练集 B ]
```

1. **为什么需要 Purging？**
   在金融数据中，一个样本往往持续多天（比如 3 天持仓期）。如果测试集包含第 10 天，而训练集中有第 9 天开仓、第 12 天平仓的样本，该训练样本的最终标签包含了第 10、11 天的价格走势。模型在训练时就提前知道了测试集的走势，因此必须 **Purge**。

2. **为什么还需要 Embargoing？**
   即使删除了重叠样本，紧接着测试集结束点 $T^{test}_{end}$ 之后发起的训练样本（训练集 B），其特征 $X_{T_{end}+1}$ 与测试集末尾的特征 $X_{T_{end}}$ 存在极强的自相关性（如高动量/高波动率状态延续）。模型可以通过这种短期记忆“窥探”测试集刚发生的状态。因此必须插入 **Embargo** 隔离带。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算例题（判断样本是否需要 Purge）

**题目**：
某测试集包含的时间段为第 100 天到第 120 天（即 $T^{test} = [100, 120]$）。
训练集中有以下 3 个候选样本（时间区间为 $[t_1, t_2]$）：
- 样本 A：$[90, 105]$
- 样本 B：$[80, 95]$
- 样本 C：$[115, 130]$

请判断哪些样本需要被 Purge（剔除），哪些可以保留在训练集中？

**解答过程**：
1. **样本 A ($[90, 105]$)**：其结束时间 $t_2 = 105 \ge T^{test}_{start} = 100$，且 $t_1 = 90 \le 100$。该样本在第 100~105 天与测试集重叠，**必须 Purge**。
2. **样本 B ($[80, 95]$)**：其结束时间 $t_2 = 95 < 100$，完全在测试集开始前结束，且没有重叠。**保留**。
3. **样本 C ($[115, 130]$)**：其起始时间 $t_1 = 115 \le T^{test}_{end} = 120$。在第 115~120 天与测试集重叠，**必须 Purge**。

---

### 例子 2：中等例题（计算 Purging 与 Embargoing 后的样本保留比例）

**题目**：
共有 1000 个连续日度样本，每个样本持有期均为 5 天（$t_2 = t_1 + 5$）。
采用 5-Fold 划分测试集（每 Fold 200 天）。以第一个 Fold（测试集为第 1~200 天）为例，设置 Embargo 长度为 10 天（即第 201~210 天被 Embargo）。
计算在此 Fold 下，剩余可用于训练的样本数量。

**解答过程**：
1. 测试集区间：$[1, 200]$。
2. 训练集总空间：$[201, 1000]$（共 800 个样本）。
3. 检查重叠 Purge：由于测试集在第 200 天结束，之前在第 196~200 天开仓的样本已在测试集内；而第 201 天开仓的样本 $t_1 = 201 > 200$，无上前向重叠。
4. 检查 Embargo 隔离：第 201 天至第 210 天的 10 个样本被 Embargo 隔离带剔除。
5. 剩余有效训练样本：第 211 天到第 1000 天，共 $1000 - 211 + 1 = 790$ 个样本。

---

### 例子 3：实际应用（Python 实现 Purged Group K-Fold 算法逻辑）

```python
import numpy as np
import pandas as pd

def get_purged_train_indices(event_times, test_start, test_end, embargo_pct=0.01):
    """
    event_times: DataFrame 含 't1' (开仓时间) 和 't2' (平仓时间)
    test_start, test_end: 当前 Fold 测试集的起止时间
    """
    # 1. 初始训练集: 不在测试集时间内的样本
    train_mask = (event_times['t2'] < test_start) | (event_times['t1'] > test_end)
    
    # 2. Embargo: 测试集结束后的缓冲区
    embargo_offset = pd.Timedelta(days=int(len(event_times) * embargo_pct))
    embargo_limit = test_end + embargo_offset
    
    # 剔除在 Embargo 缓冲区内开仓的训练样本
    embargo_mask = (event_times['t1'] > test_end) & (event_times['t1'] <= embargo_limit)
    train_mask = train_mask & (~embargo_mask)
    
    return event_times[train_mask].index

# 示例数据
dates = pd.date_range("2025-01-01", periods=100)
events = pd.DataFrame({'t1': dates, 't2': dates + pd.Timedelta(days=3)})
valid_train_idx = get_purged_train_indices(events, dates[20], dates[40])
print("净化后有效训练集样本数量:", len(valid_train_idx))
```

---


## 7.5 💥 课本挂载与工业级实战模块 (Textbook Mapping & Production Lab)

### 7.5.5
> 🔓 **作业解锁前置条件**：学完 [[收益率与对数收益率]] + [[Purged Group TimeSeries Cross-Validation 净化交叉验证 (Purged Group K-Fold CV)|Purged CV]] 即可正式解锁本 Challenge 实战！
> 💡 **解锁指引**：理解 Purged CV 的核心定义与基本推导逻辑后即可解锁。

 🧪 拓展实验与李宏毅式实战 Challenge 题 (Lab Assignment: Purged CV 工业级实战 challenge)

本作业参考 **李宏毅 (Hung-yi Lee) 教授 ML 课程作业架构** 设计，设置四个渐进式难度基线 (Baselines)：

- 🟢 **简单基线 (Simple Baseline)**：
  - **任务要求**：理解 Purged CV 的核心数学定义，使用 Python 进行基础验证与数据提取。
  - **达标标准**：代码无 Error 跑通，输出基础结果。

- 🟡 **中等基线 (Medium Baseline)**：
  - **任务要求**：实现 Purged CV 的完整向量化代码框架，在历史数据上拟合参数并校验稳定度。
  - **达标标准**：完成核心算法的向量化与参数校准，模型表现达到基线水平。

- 🔴 **强基线 (Strong Baseline)**：
  - **任务要求**：引入严格的防前视偏差、手续费扣除与 Purged 交叉验证，使基于 Purged CV 的模块表现击败基线。
- **达标标准**：使用预先固定的数据、时间切分、基准与成本口径完成样本外比较；改进必须同时报告效应大小、风险变化和失败案例，不设跨数据集通用收益阈值。

- 🟣 **Boss 基线 (Kaggle / 实盘级基线)**：
  - **任务要求**：结合真实工业级实盘环境（如高频盘口/高维去噪/强化学习），达成实盘级夏普比率与风险控制指标。
- **达标标准**：完成预先注册的过拟合、样本外与压力测试；报告 PBO 的切分方案、不确定性和阈值敏感性，不把单一候选阈值当作跨市场通用上线标准。

## 8. 常见误区与易混概念

### 误区 1：只要使用了 TimeSeriesSplit（按时间顺序截断），就不会有样本泄漏

错误直觉：“我的训练集是第 1~100 天，测试集是第 101~120 天，按时间顺序排列，所以绝无泄漏。”  
为什么错：如果第 99 天开仓的训练样本，其持仓期是 5 天（到第 104 天平仓），那么第 99 天样本的收益标签包含了第 101~104 天的价格！由于第 101~104 天已经属于测试集，模型依然窥探了未来。  
正确理解：**即使按时间顺序切分，如果不进行 Purging，持仓期的重叠依然会导致严重的样本泄漏。**

### 概念对比：标准 K-Fold vs TimeSeriesSplit vs Purged Group CV

| 维度 | 标准 K-Fold CV | TimeSeriesSplit | Purged Group CV |
| :--- | :--- | :--- | :--- |
| **数据打乱 (Shuffle)** | 是（随机打乱） | 否（严格时间顺序） | 否（按时间切分） |
| **消除重叠 (Purging)** | 无 | 无 | **有（彻底剔除重叠持仓）** |
| **隔离带 (Embargo)** | 无 | 无 | **有（后置缓冲区）** |
| **应用于金融 ML** | 灾难级泄漏 (极其过拟合) | 依然存在边界泄漏 | **唯一严谨的金融 CV 标准** |

---

## 9. 相关知识点与 Obsidian 双链建议

请帮我建立知识网络。

注意：不要只列链接。每个链接后面必须用一句话说明“为什么要链接”。

上游依赖

- [[金融微观结构采样棒 (Financial Data Bars_ Volume, Dollar & Imbalance Bars in AFML)|金融微观结构采样棒]]：提供基础概念与理论推导支撑。
- [[Meta-labeling 二级标签与元标注 (Meta-labeling in Financial ML)|标签设计]]：提供基础概念与理论推导支撑。
- [[样本泄漏]]：提供基础概念与理论推导支撑。

下游延伸

- [[Meta-labeling 二级标签与元标注 (Meta-labeling in Financial ML)|Meta-labeling]]：进一步延伸拓展该知识点的应用场景与模型构建。
- [[PBO回测过拟合概率与Deflated Sharpe Ratio (Probability of Backtest Overfitting)|组合过拟合概率PBO]]：进一步延伸拓展该知识点的应用场景与模型构建。

横向关联

- [[收益率与对数收益率]]：衡量资产收益特性的基础量纲。
- [[实盘风控]]：风险控制与投资组合保护。

应用场景

- [[实盘风控]]：工业级量化策略风控与组合风险度量。


## 10. 闭卷复现任务

1. [ ] 默写 Purging（清除重叠）与 Embargoing（隔离带）各自的定义与作用。
2. [ ] 解释为什么传统的随机 $K$-Fold CV 在金融机器学习中会导致严重过拟合。
3. [ ] 画图说明测试集与训练集之间 Purge 和 Embargo 的时间轴分布。
4. [ ] 举例说明持仓重叠是如何造成跨边界信息泄漏的。
5. [ ] 说明 Embargo 隔离带长度 $h$ 的选择标准。

---

## 11. 自测题（5 道）

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | Purging 与 Embargoing 区别 |
| 2 | 公式运用 | 基础 | 判定样本重叠条件 |
| 3 | 条件判断 | 中等 | 高频Tick数据下的 Purging 必要性 |
| 4 | 变式/综合 | 中等 | 计算加加 Embargo 后的训练集有效样本数 |
| 5 | 开放/建模 | 较难 | 在 Combinatorial Purged Cross-Validation (CPCV) 中构建多路径回测 |

---

### 第 1 题：概念辨析（基础）
**题目**：在 Purged CV 架构中，“Embargoing（隔离带）”的核心目的是解决什么问题？

> [!question]- 答案解析
> **答案**：解决测试集结束点之后，训练样本由于序列自相关性（如高波动率或动量状态延续）产生的滞后信息泄漏问题。  
> **Obsidian 标签**：`#自测题/PurgedCV`

---

### 第 2 题：公式运用（基础）
**题目**：测试集时间为 3月1日 至 3月15日。某训练样本于 2月28日 开仓，3月3日 到期平仓。判断该样本是否需要被 Purge。

> [!question]- 答案解析
> **答案**：需要。该样本到期日 3月3日 落在了测试集（3月1日~3月15日）内部，存在 3 天的时间重叠，标签包含了测试集的价格变动，必须被 Purge。  
> **Obsidian 标签**：`#自测题/Purge判定`

---

### 第 3 题：条件判断（中等）
**题目**：判断：“若我们的交易策略是日内高频平仓（所有持仓在当天收盘前全部平仓，跨日无持仓），则完全不需要使用 Purging。”

> [!question]- 答案解析
> **答案**：正确。若所有样本在日内 $t_{2,i} = t_{1,i}$ 结束，跨日样本之间不存在任何持仓时间重叠（Label Overlap），此时重叠 Purging 自动失效，但依然需要保留 Embargo 防止特征自相关泄漏。  
> **Obsidian 标签**：`#自测题/高频Purging`

---

### 第 4 题：变式/综合（中等）
**题目**：简述为什么如果不使用 Purged CV，在金融数据集上计算出的特征重要性（Mean Decrease Impurity, MDI）会严重偏向于高频噪声特征？

> [!question]- 答案解析
> **答案**：因为在未 Purge 的重叠样本中，高频噪声特征可以通过记忆重复的未来价格，在训练集中虚假地降低决策树的基尼不纯度（Gini Impurity），使得模型误以为该噪声特征具有极高预测力。  
> **Obsidian 标签**：`#自测题/特征重要性泄漏`

---

### 第 5 题：开放/建模（较难）
**题目**：Marcos López de Prado 提出的组合净化交叉验证（Combinatorial Purged Cross-Validation, CPCV）相比于传统 Purged CV 有何突破？如何利用 CPCV 生成多条历史回测路径？

> [!question]- 答案解析
> **解析**：
> 1. **传统 Purged CV 局限**：只产生一条样本外测试路径，无法评估策略回测路径的分散性。
> 2. **CPCV 突破**：将 $N$ 个组中任意选择 $k$ 个组作为测试集（产生 $\binom{N}{k}$ 种组合），对每种组合实施 Purging 与 Embargoing。
> 3. **多路径生成**：这允许生成成百上千条相互独立且无泄漏的样本外回测 Equity Curves，从而可以精确计算策略“夏普比率概率分布”（Probabilistic Sharpe Ratio, PSR）与过拟合概率（PBO）。  
> **Obsidian 标签**：`#自测题/CPCV`

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
- **建议双链**：[[样本泄漏]]、[[Meta-labeling 二级标签与元标注 (Meta-labeling in Financial ML)|标签设计]]、[[Meta-labeli

---

<!-- quant-evidence-v3 -->
## 可定位依据与失效复核

本卡的复核对象是 **Purged CV**，而不是只复述一个公式。对 **Purged CV** 的独立验证重点是：按标签信息区间而非样本行号做 purge，并用 embargo 阻断相邻折的重叠信息。

### 权威来源与定位

1. scikit-learn 官方 Common pitfalls（数据泄漏与预处理边界）：https://scikit-learn.org/stable/common_pitfalls.html。用于复核“按标签信息区间而非样本行号做 purge，并用 embargo 阻断相邻折的重叠信息”。
2. scikit-learn `TimeSeriesSplit` 官方 API：https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html。用于复核“按标签信息区间而非样本行号做 purge，并用 embargo 阻断相邻折的重叠信息”。
3. Marcos López de Prado, *Advances in Financial Machine Learning*, Wiley, ISBN 9781119482086, Chapter 3、Chapter 7 与 Chapter 11。用于复核“按标签信息区间而非样本行号做 purge，并用 embargo 阻断相邻折的重叠信息”。

### 失效边界与验收协议

- **成立条件**：先写清数据时点、估计窗口、交易摩擦和分布/市场结构假设，再运行模型。
- **反例压力测试**：按标签信息区间而非样本行号做 purge，并用 embargo 阻断相邻折的重叠信息。
- **最小实验**：固定随机种子或冻结原始数据快照，同时保存基线、破坏条件后的对照组、关键中间量与失败日志。
- **通过标准**：结论必须在样本外仍保持方向一致；若成本、延迟、参数扰动或结构突变使结论反转，就把该情形登记为适用边界而不是删除失败结果。
