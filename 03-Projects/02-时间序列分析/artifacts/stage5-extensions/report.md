---
type: index
topic: "阶段 5 扩展模型同协议运行报告"
course: "时间序列分析"
created: 2026-08-07
status: active
flow: project
kind: moc
assessment_exempt: true
assessment_exempt_reason: "本页是自动生成的运行证据报告，不承担知识点或作业验收。"
tags: [运行证据, 时间序列分析, 阶段5]
---

# 阶段 5 扩展模型同协议运行报告

## 协议

- 数据：statsmodels macrodata，公共领域，1959Q1–2009Q3。
- 目标：季度实际 GDP 年化对数增长率。
- 信息边界：所有滞后和外生变量最多使用预测季度前一季度已知值。
- 验证原点：2001Q4 至 2005Q3，共 16 个。
- 最终测试原点：2005Q4 至 2009Q3，共 16 个。
- 选择规则：候选必须完成全部验证原点且无失败，再按验证 RMSE 选择。
- 验证胜者：var，验证 RMSE=1.2751。
- 最终测试只运行：naive, var。

## 验证结果

| split | model | n_predictions | mae | rmse | mase |
| :--- | :--- | ---: | ---: | ---: | ---: |
| validation | var | 16 | 0.8883 | 1.2751 | 0.2838 |
| validation | state_space | 16 | 0.9978 | 1.3658 | 0.3193 |
| validation | ar | 16 | 1.0725 | 1.4089 | 0.3428 |
| validation | ml_lag | 16 | 1.3905 | 1.7263 | 0.4456 |
| validation | arimax | 16 | 1.5245 | 1.7352 | 0.4873 |
| validation | naive | 16 | 1.4391 | 1.7681 | 0.4602 |

## 最终测试结果

| split | model | n_predictions | mae | rmse | mase |
| :--- | :--- | ---: | ---: | ---: | ---: |
| test | var | 16 | 2.0656 | 2.6631 | 0.6895 |
| test | naive | 16 | 2.4995 | 2.8497 | 0.8343 |

## 失败与警告

- 失败记录：0。
- 警告记录：0。
- 失败不会从平均指标中静默删除；验证期缺少任一原点即失去选择资格。

## 解释边界

本报告只证明固定接口和同协议比较可以复算。它不证明扩展模型普遍优于经典基线，也不把预测关联解释为因果关系。若验证期胜者在最终测试不优于朴素基线，应保留负结果并降级。
