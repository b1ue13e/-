---
type: alias
topic: "Transformer 时序导航"
canonical: "[[Transformer 时序预测]]"
created: 2026-04-16
updated: 2026-08-05
status: active
flow: knowledge
kind: moc
tags: [索引, 时间序列, Transformer]
---

# Transformer 时序｜导航别名

> 权威主题卡为[[Transformer 时序预测]]。本页不复制注意力公式与模型边界。

## 最小判断

- 位置/时间编码负责顺序，注意力权重不等于因果解释。
- 自回归解码需要因果掩码；只编码预测原点前历史的直接多步模型不一定在编码器内使用因果掩码。
- 标准注意力成本随窗口长度约为 $O(L^2)$，但是否使用 patch、局部或稀疏注意力取决于任务。
- RevIN、差分、分解都是候选，不是普遍硬要求。
- 必须与线性、ETS/ARIMA、树模型和朴素基线进行公平滚动比较。

**学习顺序**：[[Transformer 时序预测]] → [[N-BEATS与N-HiTS]] → [[滚动回测与预测区间]]。

**出口题**：什么情况下编码器内允许历史位置双向注意，而仍不构成未来泄漏？

