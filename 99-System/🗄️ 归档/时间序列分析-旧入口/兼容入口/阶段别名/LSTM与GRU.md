---
type: alias
topic: "LSTM 与 GRU 导航"
canonical: "[[LSTM与GRU在时序中的应用]]"
created: 2026-04-16
updated: 2026-08-05
status: active
flow: knowledge
kind: moc
tags: [索引, 时间序列, LSTM, GRU]
---

# LSTM 与 GRU｜导航别名

> 权威主题卡统一为[[LSTM与GRU在时序中的应用]]；普通循环机制先读[[RNN时序建模]]。

## 选择边界

- GRU 在相同输入/隐藏宽度下标准参数量通常约比 LSTM 少 25%，但效果不能预先保证。
- 门控缓解而非彻底消除梯度问题。
- 缩放通常有助于优化，但必须在训练窗口拟合。
- 水平、差分或收益率由任务决定，不能一律差分。
- 只有在同一滚动协议下稳定胜过朴素、统计和树模型基线，复杂度才有依据。

**学习顺序**：[[RNN时序建模]] → [[LSTM与GRU在时序中的应用]] → [[Transformer 时序预测]]。

**出口题**：门控为何只能缓解而不能保证消除长序列梯度衰减？

