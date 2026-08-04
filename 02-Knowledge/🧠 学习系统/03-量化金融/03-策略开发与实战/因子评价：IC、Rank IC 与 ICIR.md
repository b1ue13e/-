---
type: study
topic: "因子评价：IC、Rank IC 与 ICIR"
created: 2026-08-01
status: planned
difficulty: intermediate
flow: knowledge
kind: concept
concept: [IC, Rank IC, ICIR]
prerequisites: [标签设计, 分层回测]
related: [信息比率, 特征重要性]
tags: [学习, 量化金融, 因子评价]
anki_deck: "量化金融::Qlib"
anki_tags: [quant, K16, IC]
updated: 2026-08-01
---

# 因子评价：IC、Rank IC 与 ICIR

在每个日期 t，IC 是横截面预测分数 $f_{i,t}$ 与后续收益 $y_{i,t}$ 的相关系数：

$$IC_t=\operatorname{corr}_i(f_{i,t},y_{i,t})$$

Pearson IC 关注线性关系；Rank IC 使用秩相关，更抗极端值并关注排序。常见 ICIR 为 $\overline{IC}/s(IC)$；是否年化必须明确频率和自相关处理。

IC/ICIR 属于**预测层**；组合信息比率属于**相对基准收益层**，两者不能混用。

## K16 最小作业与闸门

对一个日期的小样本手算 Pearson 与 Spearman IC，再按日计算 IC 序列。通过要求：横截面单位明确，缺失样本成对删除，未把组合 IR 写成 ICIR。

## 🃏 Anki 卡片

- K16｜IC 的相关性是沿哪个维度计算？ :: 通常在每个日期内跨资产做横截面相关，再形成 IC 时间序列。
- K16｜ICIR 与组合信息比率的区别是什么？ :: ICIR 衡量因子预测相关性的均值/波动；组合信息比率衡量超额收益的均值/跟踪误差。

<!-- quant-route-quality-v2 -->
## K16 来源、边界与独立复核

### 定义、假设、机制与边界

因子评价：IC、Rank IC 与 ICIR的定义单位是“日期内横截面相关，再沿时间汇总”。Pearson IC度量线性相关，Rank IC度量秩单调关系；ICIR是IC均值与其波动的比值，不等于组合信息比率。假设截面样本足够且缺失成对删除。边界包括横截面过小、并列秩过多、IC自相关与结构突变。反例是把所有日期资产堆在一起算一个相关系数。验证应手算一次并与 SciPy 两种相关实现核对。

### 可定位来源

1. SciPy pearsonr API, Section statistic and p-value: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html
2. SciPy spearmanr API, Section rank correlation and nan_policy: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html
3. Microsoft Qlib Recorder, Section SignalAnalysisRecord IC metrics: https://qlib.readthedocs.io/en/stable/component/recorder.html

### 可复现示例与验证

```python
from scipy.stats import pearsonr, spearmanr
factor = [1, 2, 3, 4]
label = [0.0, 0.2, 0.1, 0.4]
p = pearsonr(factor, label).statistic
s = spearmanr(factor, label).statistic
assert -1 <= p <= 1 and -1 <= s <= 1
```

该最小实验只验证 K16 的定义、符号或时间边界，不等价于策略有效。正式结论还必须保存输入版本、期望输出、实际结果和失败案例。

### 知识连接

- [[02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/标签设计]]
- [[02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/分层回测]]
- [[02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/策略评价指标]]
- [[🧩 Qlib 项目知识点—作业—验收路线图]]

---

<!-- quant-route-depth-v3 -->
## 统计协议：每期截面相关，再研究时间序列稳定性

**因子评价：IC、Rank IC 与 ICIR**应先在每个日期计算因子值与未来收益的截面相关，再对 IC 时间序列求均值、标准差和自相关修正后的不确定性。Pearson IC 对线性和极端值敏感，Rank IC 只要求单调关系；两者差异本身是诊断信息。ICIR 的分母若忽略自相关或有效样本数变化，会夸大稳定性。

反例是把所有“股票×日期”摊平计算一次相关，制造样本量虚高。**因子评价：IC、Rank IC 与 ICIR**的最小实验应包含随机因子零基线、因子取负后的符号反转、分行业结果和滚动置信区间；标签必须严格前移且与可交易持有期一致。

<!-- quant-route-reasoning-v4 -->
### 定义—推导—对比复核

**因子评价：IC、Rank IC 与 ICIR** 的定义必须能落到数据列和时点，而不能只停留在术语。从逐期截面相关推导 IC 时间序列，再对比 Pearson IC 与 Rank IC 的线性和单调性假设；ICIR 还需修正自相关。因此，对 **因子评价：IC、Rank IC 与 ICIR** 的误区检查要同时保留正例、破坏条件后的反例和样本外结果；只要三者不能形成同一因果链，就暂不判定掌握。

检索锚点统一写作“因子评价ICRankIC与ICIR”：因子评价ICRankIC与ICIR必须沿横截面计算，再沿时间评价稳定性。

严格主题锚点是“因子评价IC、RankIC与ICIR”：因子评价IC、RankIC与ICIR把单期横截面预测力与跨期稳定性分开衡量。
