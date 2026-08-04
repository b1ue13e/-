---
type: project
topic: "A04 E2 Qlib LightGBM"
created: 2026-08-01
status: planned
progress: 0%
flow: project
kind: project
prerequisites: [A03, K18, K19, K20, K21, K22, K23]
tags: [项目, 量化金融, Qlib, LightGBM, Alpha158]
---

# A04 E2 Qlib LightGBM

> 目标：判断 Alpha158/LightGBM 相对 E0/E1 是否带来同口径、样本外、含成本的稳定增量。

## 必交物

- 冻结的 Qlib 配置与三段时间切分
- Dataset、Model、Recorder、预测和组合产物索引
- E0/E1/E2 同协议对照表
- 验证集早停证据；测试集未用于选择轮数
- 前 20 特征重要性与一次单变量消融
- 预测分数、排序规则和交易规则分离说明

## 硬验收

- 相同股票池、测试区间、成本和组合规则。
- 同时报告 gross/net 和失败案例。
- 不把 feature importance 解释为因果效应。
- 官方 smoke 结果不能替代自己的公平对照。
