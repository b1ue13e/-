---
type: project
topic: "FPP3 Ch.5 预测工具箱课后习题"
created: 2026-08-06
status: planned
progress: 0%
flow: project
kind: problem-type
course: "时间序列分析"
source: "FPP3 Section 5.11 Exercises"
source_url: "https://otexts.com/fpp3/toolbox-exercises.html"
tags: [项目, 课后习题, 时间序列分析, FPP3, 自测题/中等]
---

# FPP3 Ch.5 预测工具箱课后习题

> 题型标签：#自测题/中等。所有模型比较必须使用同一测试集和同一误差指标。

| 题号 | 任务转述 | 交付物 | 对应笔记 |
|:---|:---|:---|:---|
| 1 | 为澳大利亚人口、Bricks、NSW Lambs、Household wealth、takeaway turnover 选择 Naive/SNaive/Drift 基线并解释选择。 | 基线表 + 预测图 | [[03-经典模型层/预测与评估]] |
| 2 | 对 Facebook 股价使用 drift，证明其预测等价于连接首末观测的直线，并与其他基线比较。 | 推导 + 比较表 | [[滚动回测与预测区间]] |
| 3 | 对 1992 年后澳大利亚啤酒产量做季节朴素预测，检查残差是否白噪声。 | 残差图 + 检验 | [[残差诊断与白噪声检验]] |
| 4 | 对 Australian Exports 与 Bricks 重复基线比较，分别选择合适的 Naive/SNaive。 | 测试集指标 | [[预测与评估]] |
| 5 | 对 `aus_livestock` 七条序列使用 SNaive，讨论是否是合理基线。 | 七序列预测图 + 结论 | [[时间序列结构-趋势季节噪声与ETS分解]] |
| 6 | 判断五个预测论断（正态残差、小残差、MAPE、复杂度、测试集最优）并给出理由。 | 真伪表 + 反例 | [[残差诊断与白噪声检验]] |
| 7 | 对个人零售序列按 2011 年切分训练/测试，做 SNaive，检查残差、预测和准确率，并测试训练长度敏感性。 | 切分图 + 指标表 | [[滚动回测与预测区间]] |
| 8 | 对 NSW pigs 保留最后 72 个观测为测试集，比较多种基线并诊断首选模型。 | 6 年测试报告 | [[滚动回测与预测区间]] |
| 9 | 对 Household wealth 留出最后四年，比较所有合适基线及残差。 | 模型排名 + 诊断 | [[预测与评估]] |
| 10 | 对 takeaway turnover 留出最后四年，比较基线及残差。 | 模型排名 + 诊断 | [[滚动回测与预测区间]] |
| 11 | 对 Bricks 做 STL + 季调朴素预测，比较固定/变化季节、稳健 STL 与 SNaive。 | 两年测试集比较 | [[季节性与STL分解]] |
| 12 | 汇总 Gold Coast tourism，建立排除 1/2/3 年的训练集，做一年 SNaive 并用 MAPE 比较。 | 三组切分 + MAPE | [[滚动回测与预测区间]] |

## 我的作答

| 题号 | 状态 | 测试集切分 | 最终模型/理由 |
|:---|:---:|:---|:---|
| 1–4 | ☐ |  |  |
| 5–8 | ☐ |  |  |
| 9–12 | ☐ |  |  |
