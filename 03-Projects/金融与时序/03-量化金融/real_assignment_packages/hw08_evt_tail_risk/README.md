# HW08 EVT 与尾部风险外推 Real Assignment Package

这是一份面向学生自做的 `HW08` 真实作业包，不再只是说明页。

## 布置时机

U08 后半段，学生已经体验过常规 VaR 的不足。

## 包内结构

- `starter/`：包含 `tail_risk.py`、`run.py`、`check_data.py`，可以直接产出最小尾部风险摘要
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `历史模拟 VaR`
- `参数法 VaR`
- `尾部风险`
- `极值理论 EVT 与 POT 模型`

## 教学目标

- 会做 POT/GPD 拟合
- 会估计极端 VaR/ES
- 会报告门槛敏感性

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw08_evt_tail_risk`

真实数据到位后，至少应包含：

- `returns.daily.csv`

可优先使用的数据来源：

- 指数收益序列
- 外汇或商品日频收益

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `returns.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw08_evt_tail_risk\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw08_evt_tail_risk" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw08_evt_tail_risk\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw08_evt_tail_risk\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw08_evt_tail_risk"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw08_evt_tail_risk\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`POT 阈值法 + 极端 VaR/ES`

## 当前 starter 已支持

- 读取 `returns.smoke.csv`
- 生成最小 `threshold_proxy` 与 `exceedances`
- 输出 `tail_risk_summary.json`

## 下一步建议

在真实收益序列上补阈值选择、GPD 拟合与敏感性分析。
