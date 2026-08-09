---
type: project
project_type: homework
course: "量化金融"
assignment_id: "QF-HW05"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)]]", "[[高阶希腊字母与衍生品风险对冲 (Higher-Order Greeks_ Vanna, Volga & Charm)]]"]
source_type: local_integration_task
source: "real_assignment_packages/hw05_black_scholes_hedging"
source_url: "[[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw05_black_scholes_hedging/README|HW05 可执行作业包]]"
license: "Repository-authored"
created: 2026-08-06
status: active
flow: project
tags: [作业, 量化金融]
---
# 量化金融-课后作业-05-Black-Scholes定价与对冲

## 学习目标与任务

按 [[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw05_black_scholes_hedging/README|HW05 可执行作业包]] 实现欧式期权定价和 Delta，对极限情形做单元测试；模拟离散再平衡，对比不同频率、波动率偏误和交易成本下的对冲误差。

## 环境与执行

- 运行包内 smoke 数据、Starter Code 与测试，固定随机种子。
- 提交公式说明、测试、误差分布图、成本对照和两页报告。
- 评分：定价与 Greeks 30，对冲实验 25，边界测试 20，解释 15，可复现性 10。

## 任务边界

- 研究欧式期权闭式定价、Delta 与离散再平衡；不把 Black–Scholes 假设外推到美式期权或真实盘口报价。
- 必须明确无套利、连续交易、波动率和利率等假设，以及交易成本对对冲误差的影响。

## 提交产物

- 定价与 Greeks 计算、极限情形测试、对冲误差分布、频率/波动率/成本对照和报告。
- 报告列出随机种子、参数单位、年化约定和未覆盖的模型风险。

## 验收标准

- 价格单调性、边界行为和 Delta 范围测试通过；闭式结果与包内基准在容差内一致。
- 对冲实验至少比较两种再平衡频率，并解释误差来源而非只报告均值。

## 引导自检

- [ ] 先用极限参数检查公式方向，再运行基准案例。
- [ ] 抽查 Delta 与价格变化的符号关系。
- [ ] 最后加入成本并比较毛/净对冲误差。

## 运行证据与失败判定

- 提交基准参数、价格/Greeks 数值、极限参数检查、离散对冲路径和毛净误差表。
- 到期时间、波动率或无风险利率单位错误，Greeks 符号不符合单调性，或成本未计入时，判定为失败。
- 改变对冲频率与波动率后复跑，报告误差均值、分位数和尾部路径，而非只给一条曲线。

## 最小复现工作流

1. 阅读作业包说明、数据卡与 Rubric，冻结期权类型、到期单位、利率、波动率、对冲频率和成本假设。
2. 运行数据检查与 Starter Baseline，先用极限情形和单步手算验证价格、Delta 与现金账户方向。
3. 完成离散对冲后，在同一随机路径上比较频率与成本情景，保存路径级误差而非只保留均值。
4. 运行全部测试，记录命令、退出码和失败用例；不得放宽浮点容差掩盖单位或符号错误。
5. 报告逐项映射定价、Greeks、对冲、成本和复现证据，明确 Black-Scholes 假设破坏后的结论边界。

