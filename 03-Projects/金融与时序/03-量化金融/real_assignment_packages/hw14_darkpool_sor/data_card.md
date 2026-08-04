# HW14 Data Card

- title: `暗池与智能订单路由`
- stage: `第四阶段：高频交易与强化学习`
- generated_at: `2026-07-31`

## 真实数据契约

数据目录建议固定为：

`f:\-\03-Projects\data\quant_finance\hw14_darkpool_sor`

预期文件：

- `venue_quotes.csv`
- `latency_profile.csv`

推荐来源：

- 多 venue 报价样例
- 模拟延迟剖面
- 自建 dark/lit 对照数据

## smoke 数据

这些数据只用于：

- 验证 starter 和 tests 跑通
- 验证文件路径、编码和基本接口
- 不用于真实研究结论

smoke 文件：

- `venue_quotes.smoke.csv`
- `latency_profile.smoke.csv`

## 硬约束

- 不得把 smoke 结果当成正式实验结论
- 必须在 README 中写清楚真实数据来源、时间区间和许可边界
- 必须说明是否存在未来信息、复权或对齐问题
