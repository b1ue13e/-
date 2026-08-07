---
type: project
project_type: homework
course: "量化金融"
assignment_id: "MIT-18S096-PS02"
assignment_level: lesson
assignment_format: problem-set
stage_id: "01"
requires: ["[[CAPM 资本资产定价模型]]", "[[收益率与对数收益率]]"]
source_type: open_textbook_exercise
source: "MIT OCW 18.S096, adapted local problem set"
source_url: "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/pages/assignments/"
accessed: 2026-08-06
license: "MIT OCW Creative Commons; local adaptation marked as adapted"
adapted_from: "MIT OCW 18.S096 Problem Set 2"
translation_status: adapted_summary
solution_visibility: private
created: 2026-08-06
status: active
flow: project
tags: [作业, 量化金融, MIT-OCW]
---
# 量化金融-课后作业-02-回归与CAPM

## 学习目标与任务

1. 从价格构造同步的简单/对数收益和超额收益。
2. 推导并估计市场模型，解释 Alpha、Beta、残差风险和置信区间。
3. 对异方差、自相关、非同步交易和样本窗口变化进行诊断。

## 环境与执行

使用 Python 3.11、pandas、statsmodels；提交代码、回归表、诊断图、假设清单和结论。评分：数据 20，模型 30，诊断 25，解释 15，可复现性 10。

## 任务边界

- 只使用交易发生前已经可得的价格、市场和无风险利率；不得用未来修订值或测试期调参。
- 必须覆盖简单收益、对数收益和超额收益的口径选择，但不要求扩展到多因子模型。

## 提交产物

- 清洗后的数据字典、回归表、置信区间、残差诊断图、假设清单和结论备忘录。
- 运行日志应包含数据区间、频率、依赖版本和命令。

## 验收标准

- 回归系数、标准误和样本期可复算；至少一个诊断检验能改变或限制结论。
- 解释 Alpha/Beta 时同时说明统计不确定性、非同步交易或异方差的影响。

## 引导自检

- [ ] 先画价格和收益序列，确认没有日期错位。
- [ ] 再运行基线回归和残差诊断。
- [ ] 最后用另一窗口或频率复跑，记录结论是否稳定。

## 运行证据与失败判定

- 保存设计矩阵、系数与稳健标准误、残差图、样本外预测和复跑命令。
- 缺失值删除、日期错位、非交易日填充或把未来收益带入特征任一发生，判定为失败。
- 对窗口/频率变化报告 Alpha、Beta、R² 和区间估计的变化，而不是只保留最优结果。

## 最小执行协议

1. 选择一个资产、市场基准与匹配频率的无风险利率，记录下载时间、字段、复权口径和原始文件摘要；数据不可得时使用标明生成机制的合成数据。
2. 先以手工矩阵或简单 OLS 复算一个短样本，再运行完整 CAPM；总收益回归仅作错误对照，正式结论必须使用对齐后的超额收益。
3. 按时间划分基准窗口与复核窗口，分别保存系数、稳健标准误、残差诊断和影响点；禁止根据第二窗口结果回改第一窗口模型。
4. 明确 Alpha 不显著、残差自相关或 Beta 不稳定时的结论降级规则，不把统计结果改写为投资建议。
5. 提交数据卡、脚本、命令日志、两组回归表和失败案例；任一系数无法追溯到输入日期即不通过。

