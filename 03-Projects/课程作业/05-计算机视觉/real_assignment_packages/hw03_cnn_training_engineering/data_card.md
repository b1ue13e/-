# HW03 Data Card

- title: `小型 CNN 与训练工程`
- stage: `第三阶段：CNN 训练闭环与日志`
- generated_at: `2026-08-01`

## 真实数据契约

数据目录建议固定为：

`F:\-\03-Projects\data\computer_vision\hw03_cnn_training_engineering`

预期文件：

- `cifar10_images.train.npz`
- `cifar10_images.val.npz`
- `label_map.json`

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
