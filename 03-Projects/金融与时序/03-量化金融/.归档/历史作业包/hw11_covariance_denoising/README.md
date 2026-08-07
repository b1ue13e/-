# HW11 协方差去噪与随机矩阵理论 Real Assignment Package

这是一份面向学生自做的 `HW11` 真实作业包，不再只是说明页。

## 布置时机

U10-U11 之间，学生已经感受到高维噪声问题。

## 包内结构

- `starter/`：包含 `denoise.py`、`run.py`、`check_data.py`，可以直接产出最小协方差去噪摘要
- `baseline/`：baseline 结果记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `相关系数、协方差与分散化`
- `协方差去噪与随机矩阵理论 RMT`

## 教学目标

- 理解 MP 法则
- 会做基础协方差去噪
- 能比较去噪前后的配置差异

## 真实数据契约

预期真实数据目录：

`f:\-\03-Projects\data\quant_finance\hw11_covariance_denoising`

真实数据到位后，至少应包含：

- `asset_returns.daily.csv`

可优先使用的数据来源：

- 多股票横截面日频收益
- ETF/行业收益矩阵

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `asset_returns.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw11_covariance_denoising\starter\run.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw11_covariance_denoising" --output-dir "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw11_covariance_denoising\your_outputs"
python "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw11_covariance_denoising\starter\check_data.py" --input-dir "f:\-\03-Projects\data\quant_finance\hw11_covariance_denoising"
pytest "f:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw11_covariance_denoising\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`原始协方差 vs 去噪协方差`

## 当前 starter 已支持

- 读取 `asset_returns.smoke.csv`
- 生成 `raw_variance` 与 `denoised_variance`
- 输出 `denoise_summary.json`

## 下一步建议

把 smoke 矩阵替换成真实高维收益矩阵，并补谱分析与去噪流程。
