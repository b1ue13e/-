# HW09 Data Card

- title: `Volume Bars 与 Dollar Bars 采样`
- stage: `第三阶段：金融 ML、因子与回测`
- generated_at: `2026-07-31`

## 真实数据契约

数据目录建议固定为：

`f:\-\03-Projects\data\quant_finance\hw09_volume_dollar_bars`

预期文件：

- `ticks.csv`

推荐来源：

- Crypto 逐笔成交
- 交易所逐笔样例
- 自采 tick 数据

## smoke 数据

这些数据只用于：

- 验证 starter 和 tests 跑通
- 验证文件路径、编码和基本接口
- 不用于真实研究结论

smoke 文件：

- `ticks.smoke.csv`

## 硬约束

- 不得把 smoke 结果当成正式实验结论
- 必须在 README 中写清楚真实数据来源、时间区间和许可边界
- 必须说明是否存在未来信息、复权或对齐问题
