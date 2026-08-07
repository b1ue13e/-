---
type: project
project_type: homework
course: "量化金融"
assignment_id: "QF-HW06"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[量化金融-波动率-GARCH家族模型]]", "[[策略评价指标]]"]
source_type: local_integration_task
source: "real_assignment_packages/hw06_garch_var"
source_url: "[[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw06_garch_var/README|HW06 可执行作业包]]"
license: "Repository-authored"
created: 2026-08-06
status: active
flow: project
tags: [作业, 量化金融]
---
# 量化金融-课后作业-06-GARCH波动率与动态VaR

## 学习目标与任务

使用 [[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw06_garch_var/README|HW06 可执行作业包]] 识别 ARCH 效应，估计 GARCH(1,1)，滚动生成一步波动率和 VaR；与常数波动率基线比较，并做覆盖率与独立性诊断。

## 环境与执行

- 严格按时间顺序拟合与预测，运行数据检查、基线和测试。
- 提交参数表、诊断图、VaR 违约序列、基线对照和失败条件。
- 评分：时间边界 20，模型与预测 30，回测诊断 25，解释 15，可复现性 10。

## 任务边界

- 估计 GARCH(1,1) 并生成一步预测和动态 VaR；不把模型结果当作无条件风险保证。
- 训练、预测和回测按时间顺序分离；常数波动率作为必需基线。

## 提交产物

- 参数表、条件波动率图、VaR 序列、违约统计、基线对照、失败条件和命令日志。
- 报告注明尾部概率、收益/损失符号、窗口和分布假设。

## 验收标准

- 时间边界、成本/符号和测试通过；覆盖率与独立性诊断结果可复算。
- 若 GARCH 未优于基线，必须保留该失败结果并解释可能原因。

## 引导自检

- [ ] 先检查收益率和损失符号。
- [ ] 再运行常数波动率基线，最后拟合 GARCH。
- [ ] 用时间外窗口检查 VaR 违约，而不是只看拟合优度。

## 运行证据与失败判定

- 保存条件方差路径、参数估计、收敛信息、VaR 阈值、违约日期和基线比较表。
- 直接用全样本波动率、损失方向反转、滚动窗口泄漏或忽略估计失败时，判定为失败。
- 报告不同置信水平下的违约率、连续违约聚集和成本/持仓限制下的风险变化。

## 最小复现工作流

1. 阅读作业包说明、数据卡与 Rubric，冻结收益频率、损失符号、估计窗口、分布假设和 VaR 置信水平。
2. 运行数据检查与 Starter Baseline，先生成常数波动率结果，再拟合 GARCH；每个预测只能使用当时可得数据。
3. 保存每次滚动估计的收敛状态、条件方差和 VaR，估计失败必须显式标记，不能沿用未来参数。
4. 运行全部测试，记录命令、退出码和失败用例；随后执行覆盖率、独立性与连续违约诊断。
5. 报告把拟合优度、预测质量和风险覆盖分开，逐项对应数据、模型、回测和复现评分证据。

