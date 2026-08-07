# HW07 非对称 GARCH 与杠杆效应 Real Assignment Package

这是一份面向学生自做的 `HW07` 真实作业包，不再只是说明页。

## 布置时机

U08 前半段，学生已经做过一次标准 GARCH。

## 包内结构

- `starter/`：包含 `asymmetry.py`、`run.py`、`check_data.py`，可以直接产出最小非对称波动率摘要
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `GARCH 模型`
- `非对称 GARCH 模型与杠杆效应`

## 教学目标

- 理解 EGARCH/GJR-GARCH 非对称结构
- 会比较标准与非对称模型
- 会解释新闻响应曲线

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw07_asymmetric_garch`

真实数据到位后，至少应包含：

- `returns.daily.csv`

可优先使用的数据来源：

- 股票指数收益率
- 商品或汇率收益率

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `returns.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw07_asymmetric_garch\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw07_asymmetric_garch" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw07_asymmetric_garch\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw07_asymmetric_garch\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw07_asymmetric_garch"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw07_asymmetric_garch\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`GARCH vs EGARCH/GJR-GARCH`

## 当前 starter 已支持

- 读取 `returns.smoke.csv`
- 生成 `negative_volatility_proxy`、`positive_volatility_proxy`
- 输出 `asymmetry_summary.json`

## 下一步建议

在真实收益数据上补模型对照、参数解释和新闻响应曲线。
