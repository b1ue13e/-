---
type: study
topic: "组合过拟合概率PBO"
created: 2026-08-01
status: planned
difficulty: advanced
flow: knowledge
kind: concept
concept: [PBO, 多重尝试, 实验台账]
prerequisites: [Purged CV, 时间序列验证]
related: [回测偏差五层审计, 单变量消融]
tags: [学习, 量化金融, 过拟合审计]
anki_deck: "量化金融::Qlib"
anki_tags: [quant, K28, PBO]
updated: 2026-08-01
---

# 组合过拟合概率 PBO

PBO 试图估计：在多个候选策略中，样本内排名最好的候选在样本外落入较差一半的概率。它通常依赖组合对称交叉验证、足够多的候选和预先定义的评价指标。

少量手工配置、非独立重复试验或只保存最优结果时，无法诚实估计 PBO。此时更正确的做法是保留完整实验台账、失败配置和单变量消融，并明确“证据不足，未估计 PBO”。

PBO 没有跨市场、跨数据集通用的神奇阈值；结论依赖候选集合、切分、指标和数据生成过程。

## K28 最小作业与闸门

记录所有尝试、保留失败配置，并做一次只改变一个变量的消融。通过要求：不只保存最好结果；能解释为何当前样本不足以可靠估计 PBO；不使用通用 `PBO<10%` 作为无条件上线标准。

## 🃏 Anki 卡片

- K28｜PBO 想估计的事件是什么？ :: 样本内最优候选在样本外落入较差一半的概率。
- K28｜为什么少量配置不能诚实估计 PBO？ :: 候选和切分证据不足，排名分布不稳定，数值会制造虚假精确性。
- K28｜证据不足时应怎样替代 PBO 数字？ :: 保存完整尝试台账、失败配置、单变量消融，并明确未估计 PBO。

<!-- quant-route-quality-v2 -->
## K28 来源、边界与独立复核

### 定义、假设、机制与边界

组合过拟合概率PBO用于估计从多个候选策略中选出的样本内赢家在样本外退化的风险。机制需要足够多候选配置和可交换的时间分块，通过组合对称交叉验证比较样本内、外排名。它不是对少量手工实验随便输出的百分比。假设试验台账完整，否则选择偏差无法计入。反例是只保存最佳结果后声称 PBO 很低。验证应保存所有候选、失败配置、分块和排名映射。

### 可定位来源

1. Bailey et al., The Probability of Backtest Overfitting, Journal of Computational Finance 20(4), Section PBO: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253
2. Bailey and López de Prado, Deflated Sharpe Ratio, DOI 10.3905/jpm.2014.40.5.094, Section multiple testing: https://doi.org/10.3905/jpm.2014.40.5.094
3. López de Prado, Advances in Financial Machine Learning, Wiley, 2018, ISBN 9781119482086, Chapter 11.

### 可复现示例与验证

```python
trial_scores = {"cfg_a":0.2, "cfg_b":0.1, "cfg_c":-0.1, "cfg_d":0.05}
assert len(trial_scores) >= 4
winner = max(trial_scores, key=trial_scores.get)
assert winner == "cfg_a"
assert set(trial_scores) == {"cfg_a","cfg_b","cfg_c","cfg_d"}
```

该最小实验只验证 K28 的定义、符号或时间边界，不等价于策略有效。正式结论还必须保存输入版本、期望输出、实际结果和失败案例。

### 知识连接

- [[02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/Purged CV]]
- [[02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/回测偏差五层审计]]
- [[02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/策略评价指标]]
- [[🧩 Qlib 项目知识点—作业—验收路线图]]

---

<!-- quant-route-depth-v3 -->
## 推导直觉：PBO 衡量“样本内冠军”在样本外掉入后半区的频率

**组合过拟合概率 PBO**先把回测区间切成多个近似独立分块，在组合对称交叉验证的每个划分中选择样本内表现最好的候选，再记录它在互补样本外的相对排名。若样本外排名经 logit 变换后小于零，说明冠军落入后半区；这些失败事件的比例就是 PBO。它评估选择流程而非某条策略的显著性。

失效边界包括候选策略在看完整数据后才生成、分块过少、以及时间依赖跨块泄漏。**组合过拟合概率 PBO**的复现实验应加入大量纯噪声策略，验证候选数增加时 PBO 上升；同时报告分块方案敏感性和样本外性能分布，不能把低 PBO 单独当作可交易证明。
