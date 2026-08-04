# HW10 HRP 分层风险平价 Real Assignment Package

这是一份面向学生自做的 `HW10` 真实作业包，不再只是说明页。

## 布置时机

U10 结束后，学生已感受到协方差不稳定。

## 包内结构

- `starter/`：包含 `hrp.py`、`run.py`、`check_data.py`，可以直接产出最小 HRP proxy 权重
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `马科维茨均值-方差模型`
- `相关系数、协方差与分散化`
- `分层风险平价组合 HRP`

## 教学目标

- 会实现 HRP 三步流程
- 会与 MPT、等权配置做公平对照
- 能解释稳健性差异

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw10_hrp_allocation`

真实数据到位后，至少应包含：

- `asset_returns.daily.csv`
- `asset_metadata.csv`

可优先使用的数据来源：

- 多资产 ETF 数据
- 行业指数或国家 ETF 池

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `asset_returns.smoke.csv`
- `asset_metadata.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw10_hrp_allocation\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw10_hrp_allocation" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw10_hrp_allocation\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw10_hrp_allocation\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw10_hrp_allocation"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw10_hrp_allocation\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`HRP vs MPT vs 1/N`

## 当前 starter 已支持

- 读取长表形式的 `asset_returns.smoke.csv`
- 给出一个最小 `cluster_order`
- 输出 `equal_weight` 与 `hrp_proxy_weight`

## 下一步建议

用真实多资产收益率补聚类、准对角化和样本外对照。
