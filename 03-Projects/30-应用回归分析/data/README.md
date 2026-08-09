---
type: index
topic: "应用回归分析项目数据说明"
created: 2026-08-09
status: active
flow: project
tags: [数据, 应用回归分析]
---

# 数据说明

默认 Capstone 使用 scikit-learn 内置 diabetes 数据集，由 load_diabetes(as_frame=True) 在本地读取，不需要网络下载，也不在本目录复制数据。

- 数据入口：https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_diabetes.html
- 本地包版本：scikit-learn 1.8.0
- 数据集原始来源与再分发许可：[待验证]
- 默认分析单位：一个基线受试者记录
- 默认目标：一年后疾病进展的连续量化指标

更换数据时，必须记录来源 URL、版本、许可证、访问日期、校验值、字段语义和隐私限制。

