# HW03 Fama-MacBeth 跨期横截面风险溢价估计 Real Assignment Package

这是一份面向学生自做的 `HW03` 真实作业包，不再只是说明页。

## 布置时机

U04 结束后，学生已经理解时间序列回归与横截面回归的差别。

## 包内结构

- `starter/`：包含 `fama_macbeth.py`、`run.py`、`check_data.py`，可以直接产出最小两步回归摘要
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `CAPM 资本资产定价模型`
- `APT 套利定价理论`
- `Fama-French 三因子模型`
- `Fama-MacBeth 两步回归法`

## 教学目标

- 会做两步回归
- 会估计风险溢价
- 能谨慎解释统计显著性

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw03_fama_macbeth`

真实数据到位后，至少应包含：

- `asset_panel.monthly.csv`
- `factor_panel.monthly.csv`

可优先使用的数据来源：

- Ken French Data Library
- WRDS/CRSP 资产截面数据
- 本地股票池月频收益面板

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `asset_panel.smoke.csv`
- `factor_panel.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw03_fama_macbeth\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw03_fama_macbeth" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw03_fama_macbeth\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw03_fama_macbeth\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw03_fama_macbeth"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw03_fama_macbeth\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`两步回归 + 风险溢价显著性`

## 当前 starter 已支持

- 读取 `asset_panel.smoke.csv` 与 `factor_panel.smoke.csv`
- 生成 `exposure_summary`
- 输出 `risk_premium_proxy` 与 `fama_macbeth_summary.json`

## 下一步建议

用真实月频面板替换 smoke 数据，并补足两步回归循环与稳健标准误。
