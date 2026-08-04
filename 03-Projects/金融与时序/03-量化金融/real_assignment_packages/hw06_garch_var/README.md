# HW06 GARCH(1,1) 动态波动率与动态 VaR Real Assignment Package

这是一份面向学生自做的 `HW06` 真实作业包，不再只是说明页。

## 布置时机

U07 结束后，作为第二阶段压舱石作业。

## 包内结构

- `starter/`：包含 `volatility.py`、`run.py`、`check_data.py`，可以直接产出最小动态波动率与 VaR 摘要
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `收益率序列的风格化事实`
- `波动率聚集`
- `ARCH 效应`
- `GARCH 模型`

## 教学目标

- 会拟合 GARCH
- 会构造动态 VaR
- 会做风险覆盖检验

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw06_garch_var`

真实数据到位后，至少应包含：

- `returns.daily.csv`

可优先使用的数据来源：

- FRED、Yahoo Finance 或本地指数日线
- 交易所指数收益序列

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `returns.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw06_garch_var\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw06_garch_var" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw06_garch_var\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw06_garch_var\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw06_garch_var"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw06_garch_var\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`GARCH 条件波动率 + VaR 覆盖检验`

## 当前 starter 已支持

- 读取 `returns.smoke.csv`
- 生成 `conditional_volatility_proxy`
- 输出 `var95_proxy` 与 `volatility_summary.json`

## 下一步建议

在真实收益序列上补充 GARCH 拟合、VaR 回测和覆盖检验。
