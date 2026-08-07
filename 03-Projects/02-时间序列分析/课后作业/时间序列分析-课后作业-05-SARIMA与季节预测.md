---
type: project
project_type: homework
course: "时间序列分析"
assignment_id: "时间序列分析-05"
assignment_level: lesson
assignment_format: lab
stage_id: "03"
requires: ["[[L06-SARIMA与季节预测]]", "[[SARIMA模型]]", "[[季节性与STL分解]]"]
source_type: local_integration_task
source: "本地原创题目，知识顺序参考 FPP3 Section 9.9"
source_url: "https://otexts.com/fpp3/seasonal-arima.html"
source_version: "FPP3 3e online, accessed 2026-08-06"
license: "本地原创任务；外部教材仅 link-only。"
created: 2026-08-02
updated: 2026-08-06
status: planned
flow: project
tags: [作业, 时间序列分析, SARIMA, 季节预测]
---

# 时间序列分析｜课后作业 05：SARIMA 与季节预测

## 学习目标

手算普通/季节差分，展开乘法季节结构，以机制决定周期，并在滚动测试中公平比较 seasonal naïve 与 SARIMA。

## 任务边界与环境

- 自选公开月度或季度序列，至少 5 个完整候选周期；记录 URL、版本、频率和条款。
- Python 3、`pandas`、`statsmodels`、`matplotlib`；保存版本与运行命令。
- 测试至少覆盖一个完整季节；所有预处理在滚动窗口内部执行。
- 普通 CPU 预计少于 10 分钟，复杂候选不得超过 6 个。

## 题目

## 任务边界

本题只在一个冻结频率和季节周期上比较不超过六个简约候选。周期必须由数据频率、业务机制或图形证据共同支持；不得用最终测试段挑选周期、差分次数或模型。所有变换、异常处理和季节特征必须在每个滚动训练窗口内重新拟合，seasonal naïve 与 SARIMA 必须共享原点、horizon 和指标。

1. **差分手算（15 分）**：季度序列 `10,14,18,22,12,16,21,25` 做 $m=4$ 季节差分和再一次普通差分；展开 $(1-B)(1-B^4)y_t$。
2. **乘法结构（15 分）**：展开 ARIMA$(1,0,0)(1,0,0)_4$，圈出交叉滞后并解释其非独立参数性质。
3. **季节证据表（20 分）**：说明周期、变换、$d,D$、异常和结构变化的业务/图形证据。
4. **候选建模（20 分）**：3–6 个简约候选，含季节 AR 与季节 MA；记录 AICc、收敛、根和季节残差峰。
5. **滚动验收（20 分）**：按多个 horizon 报告 seasonal naïve 与最优 SARIMA 的 MAE/RMSE、区间覆盖率/宽度和季节位置失败。
6. **口试（10 分）**：解释四类差分/ARMA 项各解决什么，以及为何残差合格仍可能不值得部署。

## 提交产物与 Rubric

提交数据卡、手算、候选台账、可运行代码、滚动结果 CSV、图、200 字口试稿和环境文件。分值按六题分别为 15/15/20/20/20/10。

硬失败：周期无机制/频率证据、测试不足一个季节、无 seasonal naïve、只报覆盖率不报宽度、看测试集调参。通过线 80/100。完成后进入[[时间序列分析-课后作业-06-模型识别与残差诊断]]。

## 引导与自检

先写出季节周期和差分算子，再拟合候选；提交前检查季节朴素基线、多个 horizon、区间宽度、测试封存和窗口内预处理是否全部有证据。
