# HW15 Data Card

- title: `挂单成交概率与队列位置`
- stage: `第四阶段：高频交易与强化学习`
- generated_at: `2026-07-31`

## 真实数据契约

数据目录建议固定为：

`f:\-\03-Projects\data\quant_finance\hw15_queue_fill_probability`

预期文件：

- `lob_events.csv`

推荐来源：

- 订单簿事件流
- 盘口更新与成交消息
- 仿真撮合日志

## smoke 数据

这些数据只用于：

- 验证 starter 和 tests 跑通
- 验证文件路径、编码和基本接口
- 不用于真实研究结论

smoke 文件：

- `lob_events.smoke.csv`

## 硬约束

- 不得把 smoke 结果当成正式实验结论
- 必须在 README 中写清楚真实数据来源、时间区间和许可边界
- 必须说明是否存在未来信息、复权或对齐问题
