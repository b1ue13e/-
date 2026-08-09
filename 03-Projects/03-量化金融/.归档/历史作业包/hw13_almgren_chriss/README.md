# HW13 Almgren-Chriss 最优执行 Real Assignment Package

这是一份面向学生自做的 `HW13` 真实作业包，不再只是说明页。

## 布置时机

U13 开始，课程从做策略转向如何下单。

## 包内结构

- `starter/`：包含 `execution.py`、`run.py`、`check_data.py`，可以直接产出最小执行轨迹摘要
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `买卖价差及其微观结构拆解`
- `市场冲击成本模型与平方根法则`
- `Implementation Shortfall`
- `Almgren-Chriss 最优执行轨迹推导`

## 教学目标

- 理解成本-风险权衡
- 会实现最优拆单轨迹
- 能比较匀速执行与最优执行

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw13_almgren_chriss`

真实数据到位后，至少应包含：

- `parent_order.csv`
- `liquidity_profile.csv`

可优先使用的数据来源：

- 自定义 parent order 设定
- 日内成交量曲线
- 简化订单簿流动性数据

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `parent_order.smoke.csv`
- `liquidity_profile.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw13_almgren_chriss\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw13_almgren_chriss" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw13_almgren_chriss\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw13_almgren_chriss\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw13_almgren_chriss"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw13_almgren_chriss\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`TWAP vs Almgren-Chriss`

## 当前 starter 已支持

- 读取 `parent_order.smoke.csv` 与 `liquidity_profile.smoke.csv`
- 生成 `twap_schedule_proxy` 与 `risk_averse_schedule_proxy`
- 输出 `execution_summary.json`

## 下一步建议

把 smoke 设定替换成真实流动性曲线，补执行成本与轨迹求解器。
