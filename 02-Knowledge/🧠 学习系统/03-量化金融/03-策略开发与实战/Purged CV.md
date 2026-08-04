---
type: study
topic: "Purged CV"
created: 2026-04-18
updated: 2026-08-01
status: planned
difficulty: intermediate
course: 量化金融
note_role: concept
flow: knowledge
kind: concept
sprint_id: 2026-S01-quant
concept: ["Purged CV"]
tags: [学习, 量化金融]
anki_deck: "量化金融::Qlib"
anki_tags: [quant, K26, verified_route]
---
# Purged CV

> **K26 目标**：不靠阅读完成度，而是通过定义、边界、反例和可运行断言证明掌握。

## 0. 先测再学

闭卷写出 Purged CV 的输入、输出、成立条件和一个失败案例。若无法写清，先完成本页示例，不并行开启下一个 K 点。

## 1. 定义、机制、假设与边界

Purged CV 的定义是在标签跨越多个时点时，从训练折删除与测试标签区间重叠的样本；embargo 则在边界后追加缓冲。两者机制基于标签区间，而不是随意删几天。假设仅使用 TimeSeriesSplit gap 并不总等价于 purge，因为每个样本的标签终点可能不同。反例是标签持有十天却只隔一天。验证应构造明确区间并断言训练标签与测试区间无交集。

## 2. Worked example

```python
train_intervals = [(1,3), (4,6)]
test_interval = (7,10)
overlap = lambda a,b: max(a[0],b[0]) <= min(a[1],b[1])
assert not any(overlap(x, test_interval) for x in train_intervals)
embargo_end = test_interval[1] + 2
assert embargo_end == 12
```

运行后必须保存输入、期望输出和实际输出。代码可执行只证明局部定义一致，不证明策略在样本外有效。

## 3. K26 最小作业

1. 用自己的数据重新构造上述最小示例，不直接复制数值。
2. 增加一个由本主题边界产生的失败案例，并确认断言确实失败。
3. 闭卷解释公式或机制，再与权威来源逐项核对。
4. 把代码、输出、失败日志和一句结论登记到 [[A05-成本与稳健性审计]]。

## 4. 闭卷闸门

- [ ] 能用自己的话定义 Purged CV
- [ ] 能说明至少一个成立条件和一个失效边界
- [ ] 手算或人工推演与代码结果一致
- [ ] 失败案例能够被测试捕获
- [ ] 没有把局部代码通过夸大为策略有效

## 🃏 Anki 卡片

- K26｜Purged CV的核心判断是什么？ :: Purged CV 的定义是在标签跨越多个时点时，从训练折删除与测试标签区间重叠的样本；embargo 则在边界后追加缓冲。
- K26｜Purged CV最需要防范的反例是什么？ :: 反例是标签持有十天却只隔一天。

<!-- quant-route-quality-v2 -->
## 5. 可定位来源

1. scikit-learn TimeSeriesSplit, Section gap parameter: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
2. López de Prado, Advances in Financial Machine Learning, Wiley, 2018, ISBN 9781119482086, Chapter 7.
3. Bailey et al., The Probability of Backtest Overfitting, Journal of Computational Finance 20(4), Section combinatorial validation: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

## 6. 知识连接

- [[02-Knowledge/🧠 学习系统/03-量化金融/02-量化核心技能/时间序列验证]]
- [[02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/标签设计]]
- [[02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/组合过拟合概率PBO]]
- [[🧩 Qlib 项目知识点—作业—验收路线图]]
