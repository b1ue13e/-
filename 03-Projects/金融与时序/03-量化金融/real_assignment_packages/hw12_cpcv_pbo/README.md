# HW12 CPCV 与 PBO 过拟合审计 Real Assignment Package

这是一份面向学生自做的 `HW12` 真实作业包，不再只是说明页。

## 布置时机

U11 结束后，作为第三阶段压舱石作业。

## 包内结构

- `starter/`：包含 `audit.py`、`run.py`、`check_data.py`，可以直接产出最小 CPCV/PBO 审计摘要
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `Purged Group TimeSeries Cross-Validation`
- `Meta-labeling`
- `组合过拟合概率 PBO`

## 教学目标

- 会做 purging/embargo
- 会做 CPCV 审计
- 形成先审计再汇报收益的纪律

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw12_cpcv_pbo`

真实数据到位后，至少应包含：

- `strategy_returns.daily.csv`
- `parameter_grid.csv`

可优先使用的数据来源：

- 既有策略回测结果
- 参数网格实验记录
- 自建研究日志导出

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `strategy_returns.smoke.csv`
- `parameter_grid.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw12_cpcv_pbo\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw12_cpcv_pbo" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw12_cpcv_pbo\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw12_cpcv_pbo\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw12_cpcv_pbo"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw12_cpcv_pbo\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`CPCV + PBO`

## 当前 starter 已支持

- 读取 `strategy_returns.smoke.csv` 与 `parameter_grid.smoke.csv`
- 生成最小 `cpcv_folds`
- 输出 `pbo_proxy` 与 `audit_summary.json`

## 下一步建议

接入真实策略结果，补时间块切分、purging/embargo 与 PBO 估计。
