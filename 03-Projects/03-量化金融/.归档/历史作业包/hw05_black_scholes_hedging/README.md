# HW05 Black-Scholes 定价与动态 Delta 对冲 Real Assignment Package

这是一份面向学生自做的 `HW05` 真实作业包，不再只是说明页。

## 布置时机

U06 结束后，学生已学完期权 payoff、BSM 与 Greeks。

## 包内结构

- `starter/`：包含 `hedging.py`、`run.py`、`check_data.py`，可以直接产出最小期权对冲摘要
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `远期、期货与期权的区别`
- `二叉树期权定价模型`
- `Black-Scholes 期权定价模型`
- `期权 Greeks`

## 教学目标

- 会实现 BSM 定价
- 会做离散 Delta 对冲
- 能解释对冲误差

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw05_black_scholes_hedging`

真实数据到位后，至少应包含：

- `underlying.daily.csv`
- `option_quotes.daily.csv`
- `risk_free.daily.csv`

可优先使用的数据来源：

- OptionMetrics 或交易所期权数据
- Yahoo Finance 期权链
- 国债收益率曲线

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `underlying.smoke.csv`
- `option_quotes.smoke.csv`
- `risk_free.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw05_black_scholes_hedging\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw05_black_scholes_hedging" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw05_black_scholes_hedging\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw05_black_scholes_hedging\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw05_black_scholes_hedging"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw05_black_scholes_hedging\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`BSM 闭式 + 离散 Delta 对冲`

## 当前 starter 已支持

- 读取 `underlying.smoke.csv`、`option_quotes.smoke.csv`、`risk_free.smoke.csv`
- 生成最小 `delta_proxy_path`
- 输出 `hedging_summary.json`

## 下一步建议

先把 smoke 路径替换成真实期权与标的行情，再补 Greeks 与对冲模块。
