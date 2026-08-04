# HW04 Data Card

- title: `Beneish M-Score 与财报排雷`
- stage: `第一阶段：资产定价与财务量化`
- generated_at: `2026-07-31`

## 真实数据契约

数据目录建议固定为：

`f:\-\03-Projects\data\quant_finance\hw04_beneish_quality`

预期文件：

- `financial_statement.panel.csv`
- `filing_calendar.csv`

推荐来源：

- SEC/EDGAR
- 巨潮资讯/交易所公告
- Tushare 财务数据

## smoke 数据

这些数据只用于：

- 验证 starter 和 tests 跑通
- 验证文件路径、编码和基本接口
- 不用于真实研究结论

smoke 文件：

- `financial_statement.smoke.csv`
- `filing_calendar.smoke.csv`

## 硬约束

- 不得把 smoke 结果当成正式实验结论
- 必须在 README 中写清楚真实数据来源、时间区间和许可边界
- 必须说明是否存在未来信息、复权或对齐问题
