# HW04 Data Card

- title: `迁移学习与误差分析`
- stage: `第四阶段：冻结、微调与误差审计`
- generated_at: `2026-08-01`

## 真实数据契约

数据目录建议固定为：

`F:\-\03-Projects\data\computer_vision\hw04_transfer_learning_error_analysis`

预期文件：

- `cifar10_transfer.train.npz`
- `cifar10_transfer.val.npz`
- `label_map.json`
- `transfer_config.json`

## smoke 数据

这些数据只用于：

- 验证 starter 和 tests 跑通
- 验证文件路径、编码和基本接口
- 不用于真实研究结论

smoke 文件：

- `train.smoke.csv`
- `val.smoke.csv`

## 硬约束

- 不得把 smoke 结果当成正式实验结论
- 必须在 README 中写清楚真实数据来源、时间区间和许可边界
- 必须说明是否存在切分污染、标签泄漏或预处理边界问题
