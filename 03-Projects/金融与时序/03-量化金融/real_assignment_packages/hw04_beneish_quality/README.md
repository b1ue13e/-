# HW04 Beneish M-Score 与财报排雷 Real Assignment Package

这是一份面向学生自做的 `HW04` 真实作业包，不再只是说明页。

## 布置时机

U05 结束后，学生已经完成财务报表关系、利润质量和应计项直觉。

## 包内结构

- `starter/`：包含 `quality_signal.py`、`run.py`、`check_data.py`，可以直接产出最小财报质量信号摘要
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `三大财务报表关系`
- `ROE 拆解与杜邦分析`
- `利润表与利润质量`
- `Beneish M-Score 与 Sloan 应计项因子`

## 教学目标

- 会从财报字段构造风险信号
- 理解财报发布日期滞后
- 能解释误判案例

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw04_beneish_quality`

真实数据到位后，至少应包含：

- `financial_statement.panel.csv`
- `filing_calendar.csv`

可优先使用的数据来源：

- SEC/EDGAR
- 巨潮资讯/交易所公告
- Tushare 财务数据

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `financial_statement.smoke.csv`
- `filing_calendar.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw04_beneish_quality\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw04_beneish_quality" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw04_beneish_quality\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw04_beneish_quality\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw04_beneish_quality"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw04_beneish_quality\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`Beneish M-Score + 简单质量分层`

## 当前 starter 已支持

- 读取 `financial_statement.smoke.csv` 与 `filing_calendar.smoke.csv`
- 生成最小 `accrual_ratio`
- 输出 `quality_summary.json`

## 下一步建议

把 starter 扩成真实财报字段映射，并加入发布日期过滤逻辑。
