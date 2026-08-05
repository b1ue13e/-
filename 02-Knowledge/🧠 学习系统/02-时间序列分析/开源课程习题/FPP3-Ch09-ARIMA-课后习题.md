---
type: project
topic: "FPP3 Ch.9 ARIMA 课后习题"
created: 2026-08-06
status: planned
progress: 0%
flow: project
kind: problem-type
course: "时间序列分析"
source: "FPP3 Section 9.11 Exercises"
source_url: "https://otexts.com/fpp3/arima-exercises.html"
tags: [项目, 课后习题, 时间序列分析, FPP3, 自测题/困难]
---

# FPP3 Ch.9 ARIMA 课后习题

> 题型标签：#自测题/困难。每个模型必须留下差分依据、候选阶数、残差诊断和样本外结果。

| 题号 | 任务转述 | 交付物 | 对应笔记 |
|:---|:---|:---|:---|
| 1 | 比较长度 36、360、1000 的白噪声 ACF，解释置信带和样本波动。 | 三图 + 解释 | [[自相关函数ACF]] |
| 2 | 对 Amazon 股价绘制价格、ACF、PACF，说明非平稳性及差分必要性。 | 三图 + 判断 | [[平稳性]] |
| 3 | 为 Turkish GDP、Tasmania accommodation、souvenirs 选择 Box-Cox 与差分阶数。 | 变换/差分表 | [[单位根检验]] |
| 4 | 用滞后算子写出 souvenirs 的差分。 | 手算公式 | [[滞后算子]] |
| 5 | 为个人零售序列选择使其平稳的差分阶数。 | ADF/KPSS + 图 | [[单位根检验-ADF-KPSS]] |
| 6 | 模拟 AR(1)、MA(1)、ARMA(1,1)、AR(2)，改变参数并比较图形与稳定性。 | Python/R 脚本 + 解释 | [[AR模型]]、[[MA模型]] |
| 7 | 对澳洲航空旅客序列自动选 ARIMA，写滞后算子模型，比较带漂移/高阶候选。 | 模型表 + 预测 | [[ARIMA建模流程-识别-估计-诊断]] |
| 8 | 对美国 GDP 变换后拟合多个 ARIMA，诊断并和 ETS 比较。 | 模型选择报告 | [[ARIMA模型与差分平稳性]] |
| 9 | 对 `aus_arrivals` 选一个国家，用差分、ACF/PACF 识别模型并与自动 ARIMA 比较。 | 识别表 + 预测 | [[平稳性与ACF-PACF]] |
| 10 | 对 US employment 选行业做 STL、变换、差分、ARIMA 候选、诊断和三年预测。 | 完整建模报告 | [[ARIMA建模流程-识别-估计-诊断]] |
| 11 | 对 electricity/cement/gas 季节序列做季节 ARIMA，并与 ETS 预测比较。 | 24 期预测 + 对比 | [[SARIMA模型]] |
| 12 | 对同一序列用 STL 季调后拟合非季节模型，与上一题比较。 | 两方案评估 | [[季节性与STL分解]] |
| 13 | 对 tourism 各序列拟合 ARIMA，重点检查 Snowy Mountains 与 Melbourne 预测是否合理。 | 预测图 + 异常说明 | [[ARIMA模型与差分平稳性]] |
| 14 | 对零售序列开发季节 ARIMA，和前章结果及最新实际数据比较。 | 预测回顾 | [[滚动回测与预测区间]] |
| 15 | 对 hare 序列识别 AR(4)，手算未来三期并与软件预测解释差异。 | 手算 + 软件对照 | [[AR模型平稳性与等比数列求和]] |
| 16 | 对 Switzerland population 识别带一阶差分的 ARIMA，手算未来三期并与软件对照。 | 手算 + 软件对照 | [[差分运算]] |

## 我的作答

| 题号 | 状态 | 证据链接 | 错误类型 |
|:---|:---:|:---|:---|
| 1–4 | ☐ |  |  |
| 5–8 | ☐ |  |  |
| 9–12 | ☐ |  |  |
| 13–16 | ☐ |  |  |
