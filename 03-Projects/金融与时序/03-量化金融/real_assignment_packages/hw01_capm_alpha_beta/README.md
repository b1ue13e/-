# HW01 CAPM 资产定价与单股 Alpha/Beta 归因 Real Assignment Package

这是一份面向学生自做的 `HW01` 真实作业包，不再只是说明页。

## 布置时机

U02 结束后，学生刚完成收益率、超额收益、基准与 CAPM 回归。

## 包内结构

- `starter/`：包含 `capm.py`、`run.py`、`check_data.py`，可以直接产出 CAPM smoke summary
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `收益率与对数收益率`
- `无风险资产与资本市场线`
- `CAPM 资本资产定价模型`

## 教学目标

- 会做单资产 CAPM 回归
- 会解释 alpha、beta 与基准
- 能做滚动 Beta 基础扩展

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw01_capm_alpha_beta`

真实数据到位后，至少应包含：

- `prices.daily.csv`
- `benchmark.daily.csv`
- `risk_free.daily.csv`

可优先使用的数据来源：

- Yahoo Finance 或 Stooq 日线价格
- FRED 无风险利率
- Tushare/AKShare 本地替代

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `prices.smoke.csv`
- `benchmark.smoke.csv`
- `risk_free.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw01_capm_alpha_beta\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw01_capm_alpha_beta" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw01_capm_alpha_beta\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw01_capm_alpha_beta\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw01_capm_alpha_beta"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw01_capm_alpha_beta\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`单资产 CAPM + 滚动 Beta`

## 当前 starter 已支持

- 从 `prices.smoke.csv` 自动计算最小收益率序列
- 读取 benchmark 与 risk-free
- 输出 `capm_summary.json`
- 给出一个最小滚动 beta proxy，方便学生继续扩展

## 下一步建议

把 smoke 数据替换成真实市场数据，再补 CAPM 回归和滚动窗口实现。
