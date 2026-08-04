# HW01 Data Card

- title: `CAPM 资产定价与单股 Alpha/Beta 归因`
- stage: `第一阶段：资产定价与财务量化`
- generated_at: `2026-07-31`

## 真实数据契约

数据目录建议固定为：

`f:\-\03-Projects\data\quant_finance\hw01_capm_alpha_beta`

预期文件：

- `prices.daily.csv`
- `benchmark.daily.csv`
- `risk_free.daily.csv`

推荐来源：

- Yahoo Finance 或 Stooq 日线价格
- FRED 无风险利率
- Tushare/AKShare 本地替代

## smoke 数据

这些数据只用于：

- 验证 starter 和 tests 跑通
- 验证文件路径、编码和基本接口
- 不用于真实研究结论

smoke 文件：

- `prices.smoke.csv`
- `benchmark.smoke.csv`
- `risk_free.smoke.csv`

## 硬约束

- 不得把 smoke 结果当成正式实验结论
- 必须在 README 中写清楚真实数据来源、时间区间和许可边界
- 必须说明是否存在未来信息、复权或对齐问题
