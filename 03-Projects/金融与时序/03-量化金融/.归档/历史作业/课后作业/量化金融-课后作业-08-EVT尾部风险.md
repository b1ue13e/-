---
type: project
project_type: homework
course: "量化金融"
assignment_id: "QF-HW08"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[EVT极值理论与VaR-CVaR]]"]
source_type: local_integration_task
source: "real_assignment_packages/hw08_evt_tail_risk"
source_url: "[[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw08_evt_tail_risk/README|HW08 可执行作业包]]"
license: "Repository-authored"
created: 2026-08-06
status: active
flow: project
tags: [作业, 量化金融]
---
# 量化金融-课后作业-08-EVT尾部风险

## 学习目标与任务

按 [[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw08_evt_tail_risk/README|HW08 可执行作业包]] 选择 POT 阈值、拟合 GPD、估计高分位 VaR/ES；与历史模拟比较，并用阈值稳定图、超越数和时间外验证解释不确定性。

## 环境与执行

- 固定尾部方向与损失符号，运行数据检查、基线和测试。
- 提交阈值诊断、参数和区间、风险对照、边界测试与模型限制。
- 评分：数据与符号 15，POT/GPD 30，诊断 25，风险解释 20，可复现性 10。

## 任务边界

- 只研究超过阈值的尾部损失、GPD 拟合、VaR/ES 与历史模拟对照；不把极值拟合外推为完整收益分布。
- 阈值选择、尾部方向、独立性和样本外验证必须预先声明。

## 提交产物

- 阈值稳定图、超越数、GPD 参数与区间、VaR/ES 对照、边界测试、限制说明和日志。
- 报告注明尾部样本量、阈值敏感性、时间外区间和数据许可。

## 验收标准

- 损失符号、阈值和 GPD 参数计算通过；风险估计能由输入和日志复算。
- 至少比较两个阈值或一个历史模拟基线，并保留不稳定结果。

## 引导自检

- [ ] 先固定损失方向和收益频率。
- [ ] 再绘制阈值诊断，最后拟合 GPD。
- [ ] 用时间外样本检查 VaR/ES，明确样本不足的影响。

## 运行证据与失败判定

- 保存阈值扫描、超额样本量、GPD 参数、尾指数、VaR/ES 和置信区间。
- 阈值选择无诊断、损失方向混淆、超额样本过少或把全样本信息带入阈值时，判定为失败。
- 用独立时间外窗口回测违约次数，明确小样本下不确定性和停止使用条件。

## 最小复现工作流

1. 阅读作业包说明、数据卡与 Rubric，冻结损失方向、阈值候选、最小超额数、拟合区间和时间外区间。
2. 运行数据检查与历史模拟基线，再执行阈值扫描；每个阈值都记录样本数、参数、诊断和不确定性。
3. 选定阈值后才计算 VaR/ES，测试集不参与阈值选择；保存参数失败、区间过宽和超额不足情形。
4. 运行全部测试并保存命令、退出码和失败用例；随后在独立区间报告违约日期与覆盖结果。
5. 报告区分模型尾部外推与可观测证据，逐项对应数据、拟合、稳定性、回测和复现评分项。


