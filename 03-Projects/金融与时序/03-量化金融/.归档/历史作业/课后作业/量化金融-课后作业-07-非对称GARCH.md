---
type: project
project_type: homework
course: "量化金融"
assignment_id: "QF-HW07"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[量化金融-波动率-GARCH家族模型]]"]
source_type: local_integration_task
source: "real_assignment_packages/hw07_asymmetric_garch"
source_url: "[[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw07_asymmetric_garch/README|HW07 可执行作业包]]"
license: "Repository-authored"
created: 2026-08-06
status: active
flow: project
tags: [作业, 量化金融]
---
# 量化金融-课后作业-07-非对称GARCH

## 学习目标与任务

在 [[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw07_asymmetric_garch/README|HW07 可执行作业包]] 中实现或调用 EGARCH/GJR-GARCH，比较正负冲击新闻响应曲线、样本外预测和残差诊断，并说明参数约束与不可识别情形。

## 环境与执行

- 运行 smoke 数据和测试，记录优化器、初值与收敛状态。
- 提交模型对照表、新闻响应图、诊断、失败样本和复现日志。
- 评分：实现 25，非对称解释 25，诊断与样本外 25，失败分析 15，可复现性 10。

## 任务边界

- 比较 EGARCH/GJR-GARCH 对正负冲击的响应；不把杠杆效应解释为所有市场或所有频率都成立。
- 参数约束、收敛状态和分布假设必须显式记录；不以优化器“返回成功”替代诊断。

## 提交产物

- 模型对照表、新闻响应曲线、残差诊断、样本外预测、失败样本和复现日志。
- 报告记录初值、优化器、收敛警告和参数稳定性。

## 验收标准

- 正负冲击响应方向可由参数和图形互相验证；样本外结果与对称基线可比。
- 任一收敛失败或参数越界必须被报告并触发限制说明。

## 引导自检

- [ ] 先用对称 GARCH 建立基线。
- [ ] 再分别改变冲击符号，检查响应函数。
- [ ] 最后检查收敛、残差和时间外预测。

## 运行证据与失败判定

- 提交对称基线、非对称项估计、正负冲击响应图、收敛日志和时间外预测。
- 非对称系数符号未解释、模型未收敛、标准化残差仍有显著 ARCH 效应时，判定为失败。
- 在相同数据切分下比较预测损失和 VaR 违约，不得用样本外表现反向调参。

## 最小复现工作流

1. 阅读作业包说明、数据卡与 Rubric，冻结收益口径、模型方程、分布、初值、估计窗口和测试区间。
2. 运行数据检查与对称 GARCH 基线，再运行非对称模型；在同一参数网格和数据切分下比较。
3. 保存收敛状态、参数约束、新闻冲击响应、标准化残差和时间外预测；不可识别模型必须列入失败结果。
4. 运行全部测试并保存命令、退出码和失败用例；不得删除负冲击或改变样本区间制造杠杆效应。
5. 报告分开陈述统计证据、预测增益和经济解释，并说明模型复杂度增加是否得到样本外证据支持。


