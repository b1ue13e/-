# HW03 Data Card

- title: `Fama-MacBeth 跨期横截面风险溢价估计`
- stage: `第一阶段：资产定价与财务量化`
- generated_at: `2026-07-31`

## 真实数据契约

数据目录建议固定为：

`f:\-\03-Projects\data\quant_finance\hw03_fama_macbeth`

预期文件：

- `asset_panel.monthly.csv`
- `factor_panel.monthly.csv`

推荐来源：

- Ken French Data Library
- WRDS/CRSP 资产截面数据
- 本地股票池月频收益面板

## smoke 数据

这些数据只用于：

- 验证 starter 和 tests 跑通
- 验证文件路径、编码和基本接口
- 不用于真实研究结论

smoke 文件：

- `asset_panel.smoke.csv`
- `factor_panel.smoke.csv`

## 硬约束

- 不得把 smoke 结果当成正式实验结论
- 必须在 README 中写清楚真实数据来源、时间区间和许可边界
- 必须说明是否存在未来信息、复权或对齐问题
