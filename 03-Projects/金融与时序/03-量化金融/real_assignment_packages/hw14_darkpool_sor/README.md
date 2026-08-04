# HW14 暗池与智能订单路由 Real Assignment Package

这是一份面向学生自做的 `HW14` 真实作业包，不再只是说明页。

## 布置时机

U13-U14 之间，学生已经知道执行不是单市场问题。

## 包内结构

- `starter/`：包含 `routing.py`、`run.py`、`check_data.py`，可以直接产出最小订单路由摘要
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `限价订单簿数据与 L1/L2/L3 盘口重建`
- `买卖价差及其微观结构拆解`
- `暗池交易与智能订单路由 SOR`

## 教学目标

- 会设计简单多市场路由规则
- 会把延迟和成交概率纳入执行分析
- 理解交易场所异质性

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw14_darkpool_sor`

真实数据到位后，至少应包含：

- `venue_quotes.csv`
- `latency_profile.csv`

可优先使用的数据来源：

- 多 venue 报价样例
- 模拟延迟剖面
- 自建 dark/lit 对照数据

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `venue_quotes.smoke.csv`
- `latency_profile.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw14_darkpool_sor\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw14_darkpool_sor" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw14_darkpool_sor\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw14_darkpool_sor\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw14_darkpool_sor"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw14_darkpool_sor\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`单市场执行 vs 多市场 SOR`

## 当前 starter 已支持

- 读取 `venue_quotes.smoke.csv` 与 `latency_profile.smoke.csv`
- 生成 `best_route` 与 `route_candidates`
- 输出 `routing_summary.json`

## 下一步建议

补充真实多 venue 数据或仿真数据，实现路由与延迟分析。
