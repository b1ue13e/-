---
type: index
topic: "CO₂ Capstone 运行报告"
course: "时间序列分析"
created: 2026-08-06
updated: 2026-08-07
status: active
flow: project
assessment_exempt: true
assessment_exempt_reason: "本页是脚本生成的参考运行证据，不是课程知识卡或学习者作业。"
generated_from: "scripts/run_capstone_co2.py"
tags: [项目, 时间序列分析, 运行证据]
---

# CO₂ Capstone 运行报告

- 数据来自 statsmodels 内置、标记为 public domain 的 CO₂ 数据，1965 年后按月聚合；原始数据中的早期缺失区间不进入实验。
- 验证窗口：1996-01 至 2000-01，每三个月一个滚动原点；最终测试原点：2001-01；horizon=12。
- 候选只有在完成全部验证原点和 horizon 且无拟合失败时才具备选择资格；优化未收敛按失败处理。
- 验证集按逐 horizon RMSE 的平均值选择模型：`ets`；选择完成后才运行最终测试。
- 验证平均 RMSE：ets=0.649、seasonal_naive=1.925、ml_lag=2.465、naive=3.171、arima=0.700（因失败/缺失不具备选择资格）；失败候选不会通过少算困难窗口获得不公平优势。
- 最终测试只运行冻结的模型集合：naive, seasonal_naive, ets。
- 点预测报告 MAE/RMSE；80%/95% 区间同时报告覆盖率和平均宽度。
- Naive、Seasonal Naive、ETS 与 ML 区间采用训练残差尺度的正态近似；ARIMA 使用模型预测分布。该近似是本次最小复现的限制，不视为已完成严格校准。
- `warnings.csv` 和 `failures.csv` 分别保留警告与失败；它们不会从选择证据中静默消失。
- 选中模型测试误差的 Ljung–Box 只作描述性诊断，不能反向调参；最差窗口和误差摘要见 `residual-diagnostics.csv`。
- 详细复算入口：`predictions.csv`、`metrics-by-horizon.csv`、`validation-model-selection.csv`、`residual-diagnostics.csv`、`warnings.csv`、`failures.csv`、`manifest.json`。

本报告不把运行结果解释为普遍模型优越性；它只证明本课程 Capstone 的最小可复现执行路径。
