---
type: index
topic: "CO₂ Capstone 运行报告"
course: "时间序列分析"
created: 2026-08-06
status: active
flow: project
assessment_exempt: true
assessment_exempt_reason: "本页是脚本生成的参考运行证据，不是课程知识卡或学习者作业。"
generated_from: "scripts/run_capstone_co2.py"
tags: [项目, 时间序列分析, 运行证据]
---

# CO₂ Capstone 运行报告

- 数据来自 statsmodels 内置 CO₂ 数据，1965 年后按月聚合；原始数据中的早期缺失区间不进入实验。
- 验证窗口：1996-01 至 2000-01，每三个月一个滚动原点；最终测试原点：2001-01；horizon=12。
- 验证集按逐 horizon RMSE 的平均值选择模型：`ets`。
- 验证平均 RMSE 排名：ets=0.649、arima=0.685、seasonal_naive=1.925、ml_lag=2.465、naive=3.171；`ml_lag` 未优于 ETS，负结果保留用于复杂度与样本外增益审计。
- 点预测报告 MAE/RMSE；80%/95% 区间同时报告覆盖率和平均宽度。
- Naive、Seasonal Naive、ETS 与 ML 区间采用训练残差尺度的正态近似；ARIMA 使用模型预测分布。该近似是本次最小复现的限制，不视为已完成严格校准。
- 测试集只在选择冻结后运行一次；所有模型和失败拟合均保留在 CSV。
- 选中模型测试误差的 Ljung–Box lag 12 仅作描述性诊断，不能反向调参；最差窗口和误差摘要见 `residual-diagnostics.csv`。
- 详细复算入口：`predictions.csv`、`metrics-by-horizon.csv`、`residual-diagnostics.csv`、`failures.csv`、`manifest.json`。

本报告不把运行结果解释为普遍模型优越性；它只证明本课程 Capstone 的最小可复现执行路径。
