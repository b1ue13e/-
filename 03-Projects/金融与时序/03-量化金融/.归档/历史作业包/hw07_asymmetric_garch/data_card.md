# HW07 Data Card

- title: `非对称 GARCH 与杠杆效应`
- stage: `第二阶段：时间序列、期权与风控`
- generated_at: `2026-07-31`

## 真实数据契约

数据目录建议固定为：

`f:\-\03-Projects\data\quant_finance\hw07_asymmetric_garch`

预期文件：

- `returns.daily.csv`

推荐来源：

- 股票指数收益率
- 商品或汇率收益率

## smoke 数据

这些数据只用于：

- 验证 starter 和 tests 跑通
- 验证文件路径、编码和基本接口
- 不用于真实研究结论

smoke 文件：

- `returns.smoke.csv`

## 硬约束

- 不得把 smoke 结果当成正式实验结论
- 必须在 README 中写清楚真实数据来源、时间区间和许可边界
- 必须说明是否存在未来信息、复权或对齐问题
