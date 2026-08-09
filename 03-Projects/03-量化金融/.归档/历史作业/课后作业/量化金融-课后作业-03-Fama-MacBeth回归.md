---
type: project
project_type: homework
course: "量化金融"
assignment_id: "QF-HW03"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[CAPM 资本资产定价模型]]", "[[Fama-MacBeth 两步回归法 (Fama-MacBeth Two-Step Regression)]]"]
source_type: local_integration_task
source: "real_assignment_packages/hw03_fama_macbeth"
source_url: "[[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw03_fama_macbeth/README|HW03 可执行作业包]]"
license: "Repository-authored"
created: 2026-08-06
status: active
flow: project
tags: [作业, 量化金融]
---
# 量化金融-课后作业-03-Fama-MacBeth回归

## 学习目标与任务

按 [[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw03_fama_macbeth/README|HW03 可执行作业包]] 完成滚动 Beta 估计、逐期横截面回归与风险溢价聚合；比较普通、Newey-West 或分组稳健标准误，并解释“统计显著”与“可交易”的差别。

## 环境与执行

- 先执行数据检查，再运行 baseline 和测试；时间序列估计窗口不得使用当期以后数据。
- 提交中间 Beta 面板、逐期系数、汇总表、稳健性对照和研究备忘录。
- 评分：时间边界 20，两步实现 30，推断 20，经济解释 20，可复现性 10。

## 任务边界

- 第一阶段只估计历史窗口 Beta，第二阶段只用当期可得特征做横截面回归；不得把未来收益或测试集信息带入特征选择。
- 必须比较至少一种稳健标准误，但不要求扩展到高频微观结构模型。

## 提交产物

- Beta 面板、逐期风险溢价、聚合表、标准误对照、时间边界审计和研究备忘录。
- 备忘录须区分统计显著、经济显著和可交易性，并记录失败样本。

## 验收标准

- 时间切分测试通过，逐期回归和聚合结果可由日志复算。
- 稳健标准误、窗口长度或资产筛选变化后，结论边界有明确说明。

## 引导自检

- [ ] 先检查每个资产的 Beta 窗口是否只使用历史数据。
- [ ] 再抽查单个日期的横截面回归输入。
- [ ] 最后比较普通与稳健标准误，并写出不确定性来源。

## 运行证据与失败判定

- 保存每期横截面样本量、Beta 估计窗口、风险溢价序列、两类标准误和缺失处理日志。
- 若 Beta 窗口使用未来信息、横截面样本为空、聚类维度未说明或只报告显著系数，判定为失败。
- 对资产数量和时间窗口做一次敏感性复跑，并保留不显著或方向相反的结果。

## 最小复现工作流

1. 阅读作业包说明、数据卡与 Rubric，冻结资产池、第一步窗口、第二步频率、缺失规则和标准误方案。
2. 运行数据检查并保存每期样本量；先运行 Starter Baseline，再完成滚动 Beta 和横截面回归。
3. 抽取一个日期手工复算横截面输入与系数，确认代码没有跨期读取；随后运行全样本与敏感性实验。
4. 运行全部测试，保存命令、退出码、运行时和失败用例；禁止删除无显著结果来换取更好图表。
5. 报告把估计误差、经济量级和可交易性分开讨论，并逐项对应 Rubric 的数据、模型、诊断与复现证据。

