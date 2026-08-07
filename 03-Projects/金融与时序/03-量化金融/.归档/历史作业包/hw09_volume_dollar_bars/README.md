# HW09 Volume Bars 与 Dollar Bars 采样 Real Assignment Package

这是一份面向学生自做的 `HW09` 真实作业包，不再只是说明页。

## 布置时机

U09 结束后，作为进入研究工程层的第一份作业。

## 包内结构

- `starter/`：包含 `bars.py`、`run.py`、`check_data.py`，可以直接产出最小 bar 采样摘要
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `OHLCV 字段清洗与复权`
- `订单簿数据`
- `金融微观结构采样棒`

## 教学目标

- 会从 tick/成交数据构造 bars
- 能比较不同采样方式下的统计性质
- 建立数据采样意识

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw09_volume_dollar_bars`

真实数据到位后，至少应包含：

- `ticks.csv`

可优先使用的数据来源：

- Crypto 逐笔成交
- 交易所逐笔样例
- 自采 tick 数据

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `ticks.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw09_volume_dollar_bars\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw09_volume_dollar_bars" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw09_volume_dollar_bars\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw09_volume_dollar_bars\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw09_volume_dollar_bars"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw09_volume_dollar_bars\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`Volume Bars + Dollar Bars 对照`

## 当前 starter 已支持

- 读取 `ticks.smoke.csv`
- 生成 `volume_bar_count` 与 `dollar_bar_count`
- 输出 `bar_summary.json`

## 下一步建议

将 smoke tick 替换成真实逐笔数据，并补充 bars 构建与统计对照。
