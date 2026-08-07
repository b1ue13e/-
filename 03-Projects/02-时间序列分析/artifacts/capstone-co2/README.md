---
type: index
topic: "CO₂ Capstone 运行证据入口"
course: "时间序列分析"
created: 2026-08-06
status: active
flow: project
assessment_exempt: true
assessment_exempt_reason: "本页只说明脚本生成的运行证据，不承担知识点或学习者作业验收。"
generated_from: "scripts/run_capstone_co2.py"
tags: [项目, 时间序列分析, 运行证据]
---

# CO₂ Capstone 运行证据

## 重跑命令

在仓库根目录执行：

```powershell
python 03-Projects/02-时间序列分析/scripts/run_capstone_co2.py
python -m unittest discover -s 03-Projects/02-时间序列分析/tests -v
```

脚本使用 `statsmodels.datasets.co2` 的内置公开数据，不下载或保存外部数据快照。它从 1965 年开始按月聚合，使用 1996–2000 年滚动验证原点选择模型，固定 2001 年测试原点，horizon 为 12。

## 产物

- `manifest.json`：数据、版本、边界、种子和测试政策。
- `environment.txt`：Python、NumPy、pandas、statsmodels 版本与命令。
- `predictions.csv`：1068 条逐预测记录（含 `ml_lag` 对照），包含 `train_end`、区间和覆盖标记。
- `metrics-by-horizon.csv`：按 split、模型和 horizon 的 MAE/RMSE、覆盖率和平均宽度。
- `validation-model-selection.csv`：仅由验证集选择模型；本次选择 ETS。
- 本次验证平均 RMSE 排名为 ETS、ARIMA、seasonal naive、`ml_lag`、naive；`ml_lag` 的负结果保留，用于检验复杂模型是否真的带来样本外增益。
- `residual-diagnostics.csv`：选中模型测试误差摘要和描述性 Ljung–Box 结果。
- `failures.csv`：保留一次 ARIMA `LU decomposition error`，不删除失败拟合。
- `run.log`：本次运行的行数、失败数和选择结果。
- `report.md`：不夸大结果的参考运行说明。

该目录是课程维护者的参考执行证据，不是学习者的大作业提交，也不能替代学习者自己的数据契约、模型台账和报告。
