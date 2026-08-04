# HW17 Qlib 因子研究与成本敏感回测 Real Assignment Package

这是一份面向学生自做的 `HW17` 真实作业包，不再只是说明页。

## 布置时机

U15 之后，作为 Capstone 启动包。

## 包内结构

- `starter/`：包含 `protocol.py`、`run.py`、`check_data.py`，可以直接审计 Qlib smoke 协议
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `收益率与对数收益率`
- `时间序列数据处理`
- `策略评价指标`
- `Qlib 工作流与无泄漏审计`

## 教学目标

- 会冻结 commit、环境和数据 release
- 会搭建朴素 baseline 与 Qlib baseline
- 会做含成本样本外回测

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw17_qlib_factor_research`

真实数据到位后，至少应包含：

- `qlib_manifest.json`
- `workflow_config.yaml`
- `baseline_protocol.md`

可优先使用的数据来源：

- microsoft/qlib
- investment_data 2026-07-27 release
- 本地 frozen config 与 lock file

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `qlib_manifest.smoke.csv`
- `workflow_config.smoke.csv`
- `baseline_protocol.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw17_qlib_factor_research\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw17_qlib_factor_research" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw17_qlib_factor_research\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw17_qlib_factor_research\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw17_qlib_factor_research"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw17_qlib_factor_research\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`等权/朴素信号 vs Qlib LightGBM Alpha158`

## 当前 starter 已支持

- 检查 `qlib_manifest / workflow_config / baseline_protocol`
- 验证 `LightGBM + Alpha158 + E0/E1/E2` 最小协议是否齐全
- 输出 `protocol_summary.json`

## 下一步建议

将 smoke 协议替换成真实 commit、manifest 与配置文件，再跑官方 smoke workflow。
