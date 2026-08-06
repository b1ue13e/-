# HW05 Data Card

- title: `Pascal VOC 最小目标检测工程包`
- stage: `第五阶段：检测工程闭环`
- generated_at: `2026-08-01`

## 真实数据契约

数据目录建议固定为：

`F:\-\03-Projects\data\computer_vision\hw05_pascal_voc_detection_pkg`

预期文件：

- `voc_annotations.train.json`
- `voc_annotations.val.json`
- `detection_config.json`
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
