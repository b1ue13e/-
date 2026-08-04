# HW16 Gymnasium 金融交易环境与 PPO Real Assignment Package

这是一份面向学生自做的 `HW16` 真实作业包，不再只是说明页。

## 布置时机

U15 或 RL 专题启动单元，学生已经建立成本和风险意识。

## 包内结构

- `starter/`：包含 `env_spec.py`、`run.py`、`check_data.py`，可以直接产出最小环境规格摘要
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `动态下注规模与凯利公式`
- `动态止损机制与风险平价仓位管理`
- `强化学习金融交易环境与 MDP 状态-动作空间设计`

## 教学目标

- 会封装交易环境
- 会设计状态、动作、奖励
- 会把成本和风险写进环境

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw16_finrl_gymnasium`

真实数据到位后，至少应包含：

- `market_state.daily.csv`

可优先使用的数据来源：

- 标的历史行情
- 自定义技术指标面板
- 仓位和成本设定

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `market_state.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw16_finrl_gymnasium\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw16_finrl_gymnasium" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw16_finrl_gymnasium\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw16_finrl_gymnasium\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw16_finrl_gymnasium"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw16_finrl_gymnasium\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`最小 Gymnasium 环境 + PPO 接口占位`

## 当前 starter 已支持

- 读取 `market_state.smoke.csv`
- 抽取 `feature_columns`、`position_column` 与 `action_space`
- 输出 `env_summary.json`

## 下一步建议

先把环境接口做成最小可运行版本，再逐步加入奖励塑形和评估协议。
