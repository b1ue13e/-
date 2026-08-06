---
type: study
topic: Pandas分组聚合与透视表
created: '2026-04-18'
updated: 2026-08-01
status: planned
difficulty: intermediate
course: 量化金融
note_role: concept
flow: sprint
kind: concept
prerequisites:
- 时间索引与频率（量化）
- Pandas 基础
related:
- 滚动窗口与波动率特征
- 因子预处理
assessment_exempt: false
source: pandas GroupBy 与 Reshaping 文档
source_url: https://pandas.pydata.org/docs/user_guide/groupby.html
accessed: '2026-08-06'
license: link-only
sprint_id: 2026-S01-quant
concept:
- Pandas分组聚合与透视表
tags:
- 学习
- 量化金融
anki_deck: 量化金融::Qlib
anki_tags:
- quant
- K04
- verified_route
---

# Pandas分组聚合与透视表

> [!info] 主线导航
> [[🗺️ 量化金融学习路径|返回路径]] · **Week 2 / K04** · 上一张 [[时间索引与频率（量化）]] · 下一张 [[滚动窗口与波动率特征]]

> **K04 目标**：不靠阅读完成度，而是通过定义、边界、反例和可运行断言证明掌握。

## 0. 先测再学

闭卷写出 Pandas分组聚合与透视表 的输入、输出、成立条件和一个失败案例。若无法写清，先完成本页示例，不并行开启下一个 K 点。

## 1. 定义、机制、假设与边界

Pandas分组聚合与透视表在量化面板中的定义必须区分资产内时间运算与同日截面运算。groupby 的 split-apply-combine 机制只在分组键正确、索引对齐稳定时成立；直接对全表 shift 会越过资产边界。适用边界是 pivot 要求行列键唯一，而 pivot_table 会执行聚合，不能拿它掩盖重复行情。反例测试应让 A 的末行紧邻 B 的首行，并确认 B 的首个滞后值仍为空。

## 2. Worked example

```python
import pandas as pd
s = pd.Series([10, 11, 20, 18], index=["A", "A", "B", "B"])
lag = s.groupby(level=0).shift(1)
assert pd.isna(lag.iloc[0]) and pd.isna(lag.iloc[2])
assert lag.iloc[3] == 20
```

运行后必须保存输入、期望输出和实际输出。代码可执行只证明局部定义一致，不证明策略在样本外有效。

## 3. K04 最小作业

1. 用自己的数据重新构造上述最小示例，不直接复制数值。
2. 增加一个由本主题边界产生的失败案例，并确认断言确实失败。
3. 闭卷解释公式或机制，再与权威来源逐项核对。
4. 把代码、输出、失败日志和一句结论登记到 [[A01-数据协议与无泄漏审计]]。

## 4. 闭卷闸门

- [ ] 能用自己的话定义 Pandas分组聚合与透视表
- [ ] 能说明至少一个成立条件和一个失效边界
- [ ] 手算或人工推演与代码结果一致
- [ ] 失败案例能够被测试捕获
- [ ] 没有把局部代码通过夸大为策略有效

## 🃏 Anki 卡片

- K04｜Pandas分组聚合与透视表的核心判断是什么？ :: Pandas分组聚合与透视表在量化面板中的定义必须区分资产内时间运算与同日截面运算。
- K04｜Pandas分组聚合与透视表最需要防范的反例是什么？ :: 反例测试应让 A 的末行紧邻 B 的首行，并确认 B 的首个滞后值仍为空。

<!-- quant-route-quality-v2 -->
## 5. 可定位来源

1. pandas Group by: split-apply-combine, Section Window and resample operations: https://pandas.pydata.org/docs/user_guide/groupby.html
2. pandas Reshaping and pivot tables, Section pivot versus pivot_table: https://pandas.pydata.org/docs/user_guide/reshaping.html
3. pandas MultiIndex/advanced indexing, Section Basic indexing: https://pandas.pydata.org/docs/user_guide/advanced.html

## 6. 知识连接

- [[02-Knowledge/🧠 学习系统/03-量化金融/01-夯实基础/时间索引与频率（量化）]]
- [[02-Knowledge/🧠 学习系统/03-量化金融/01-夯实基础/滚动窗口与波动率特征]]
- [[因子预处理：去极值、中性化与标准化 (Factor Preprocessing_ Winsorization, Neutralization & Z-Score)]]
- [[02-Knowledge/🧠 学习系统/03-量化金融/00-前置知识/🧭 阶段0-先修诊断与研究协议]]

---

<!-- quant-route-depth-v3 -->
## 决策规则：分组键定义经济对象，聚合函数决定统计含义

**Pandas 分组聚合与透视表**必须先写明一行代表“证券×日期”还是“订单×事件”，再决定 `groupby` 的键。机制上，`transform` 返回与原表等长的组内统计量，适合中性化和标准化；`agg` 改变粒度，适合生成截面或月度面板；`pivot_table` 会聚合重复键，不能当作无损 reshape。最小复现实验要刻意放入重复证券日、缺失行业和两种排序，断言聚合前后金额或成交量守恒。

失效边界包括把未来行业分类回填到历史、用默认均值吞掉重复键、以及在分组后丢失时间排序。**Pandas 分组聚合与透视表**只有在键唯一性、空值策略、排序和输出粒度均被断言时才通过；否则即使表格形状正确，也可能已经发生样本泄漏或重复计数。

## 适用条件与边界

- `transform` 保持原行数，`agg` 改变粒度，`pivot_table` 会聚合重复键；选择 API 前必须先声明行粒度和键的唯一性。
- 缺失分组键、排序不稳定或把未来分类回填到历史都会改变统计含义，不能仅凭输出形状正确判定通过。

## 公式与符号

对分组 $g$ 的均值为 $\bar{x}_g=|g|^{-1}\sum_{i\in g}x_i$；`groupby(keys)` 中 `keys` 定义经济对象，`transform` 返回与输入同长的组内统计量，`agg` 返回每组一行的汇总表。

## 🧪 学完本节后可完成的作业

- **可立即完成**：[[03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-01-线性代数与概率基础#题 4|PS01 题 4]]，用分组聚合验证协方差与权重汇总不发生跨资产污染。
- **需结合后续知识**：[[03-Projects/金融与时序/03-量化金融/大作业/量化金融-大作业-AAPL贯穿式量化研究|Capstone-AAPL Phase 1]]，在多资产面板上通过分组与时间排序测试。
- **提交产物**：输入/输出粒度说明、最小样例、重复键和缺失键失败案例。

<!-- quant-route-reasoning-v4 -->
### 定义—推导—对比复核

**Pandas分组聚合与透视表** 的定义必须能落到数据列和时点，而不能只停留在术语。`transform` 保持行粒度而 `agg` 改变粒度；从键的函数依赖推导输出行数，并与 `pivot` 不允许重复键的定义对比。因此，对 **Pandas分组聚合与透视表** 的误区检查要同时保留正例、破坏条件后的反例和样本外结果；只要三者不能形成同一因果链，就暂不判定掌握。
