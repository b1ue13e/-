# HW02 马科维茨均值-方差有效前沿 Real Assignment Package

这是一份面向学生自做的 `HW02` 真实作业包，不再只是说明页。

## 布置时机

U03 结束后，作为第一阶段压舱石作业。

## 包内结构

- `starter/`：包含 `frontier.py`、`run.py`、`check_data.py`，可以直接产出最小配置对照
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `收益率与对数收益率`
- `相关系数、协方差与分散化`
- `马科维茨均值-方差模型`

## 教学目标

- 会估计收益与协方差
- 会画有效前沿
- 能比较等权、最小方差与切线组合

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw02_markowitz_frontier`

真实数据到位后，至少应包含：

- `asset_returns.daily.csv`
- `asset_metadata.csv`

可优先使用的数据来源：

- Yahoo Finance 多资产日线
- Fama-French 行业组合或 ETF 数据
- Wind/Tushare 本地替代

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `asset_returns.smoke.csv`
- `asset_metadata.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw02_markowitz_frontier\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw02_markowitz_frontier" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw02_markowitz_frontier\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw02_markowitz_frontier\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw02_markowitz_frontier"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw02_markowitz_frontier\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`等权 vs 最小方差 vs 切线组合`

## 当前 starter 已支持

- 读取长表形式的 `asset_returns.smoke.csv`
- 输出 `equal_weight`、`inverse_vol_weight` 和 `tangency_proxy`
- 生成 `frontier_summary.json`

## 下一步建议

把 starter 扩展成真实优化器，并补充权重约束和样本外比较。
