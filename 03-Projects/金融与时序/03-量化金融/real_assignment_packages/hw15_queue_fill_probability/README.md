# HW15 挂单成交概率与队列位置 Real Assignment Package

这是一份面向学生自做的 `HW15` 真实作业包，不再只是说明页。

## 布置时机

U14 结束后，学生已经理解订单生命周期和价格优先时间优先。

## 包内结构

- `starter/`：包含 `queue_model.py`、`run.py`、`check_data.py`，可以直接产出最小队列成交摘要
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `限价订单簿数据与 L1/L2/L3 盘口重建`
- `买卖价差及其微观结构拆解`
- `跨市场排队优先权与挂单成交概率`

## 教学目标

- 会估计 fill probability
- 会解释队列位置与撤单影响
- 会比较挂单与吃单成本

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw15_queue_fill_probability`

真实数据到位后，至少应包含：

- `lob_events.csv`

可优先使用的数据来源：

- 订单簿事件流
- 盘口更新与成交消息
- 仿真撮合日志

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `lob_events.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw15_queue_fill_probability\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw15_queue_fill_probability" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw15_queue_fill_probability\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw15_queue_fill_probability\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw15_queue_fill_probability"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw15_queue_fill_probability\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`基础队列模型 + 成交概率估计`

## 当前 starter 已支持

- 读取 `lob_events.smoke.csv`
- 生成 `queue_depth_proxy` 与 `fill_probability_proxy`
- 输出 `queue_summary.json`

## 下一步建议

把 smoke 事件流替换成真实盘口事件，并补队列位置与 fill probability 估计器。
