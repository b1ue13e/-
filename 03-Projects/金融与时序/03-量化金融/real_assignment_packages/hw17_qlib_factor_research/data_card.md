# HW17 Data Card

- title: `Qlib 因子研究与成本敏感回测`
- stage: `第五阶段：Capstone / 开源工作流`
- generated_at: `2026-07-31`

## 真实数据契约

数据目录建议固定为：

`f:\-\03-Projects\data\quant_finance\hw17_qlib_factor_research`

预期文件：

- `qlib_manifest.json`
- `workflow_config.yaml`
- `baseline_protocol.md`

推荐来源：

- microsoft/qlib
- investment_data 2026-07-27 release
- 本地 frozen config 与 lock file

## smoke 数据

这些数据只用于：

- 验证 starter 和 tests 跑通
- 验证文件路径、编码和基本接口
- 不用于真实研究结论

smoke 文件：

- `qlib_manifest.smoke.csv`
- `workflow_config.smoke.csv`
- `baseline_protocol.smoke.csv`

## 硬约束

- 不得把 smoke 结果当成正式实验结论
- 必须在 README 中写清楚真实数据来源、时间区间和许可边界
- 必须说明是否存在未来信息、复权或对齐问题
