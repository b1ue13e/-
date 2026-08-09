---
type: project
project_type: homework
course: "量化金融"
assignment_id: "QF-HW04"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)]]", "[[ROE 拆解与杜邦分析 (DuPont Analysis)]]"]
source_type: local_integration_task
source: "real_assignment_packages/hw04_beneish_quality"
source_url: "[[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw04_beneish_quality/README|HW04 可执行作业包]]"
license: "Repository-authored"
created: 2026-08-06
status: active
flow: project
tags: [作业, 量化金融]
---
# 量化金融-课后作业-04-Beneish-M-Score财报排雷

## 学习目标与任务

使用 [[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw04_beneish_quality/README|HW04 可执行作业包]] 复核财报字段口径，计算 Beneish 指标和 Sloan 应计项，输出异常样本解释；对缺失值、负分母、行业差异和公告日可得性进行审计。

## 环境与执行

- 运行数据检查、基线与测试，不得把报告期结束日误作可交易日期。
- 提交字段映射、信号表、异常案例、边界测试和风险说明。
- 评分：数据口径 25，公式实现 25，时点审计 20，解释 20，可复现性 10。

## 任务边界

- 只实现公开财报字段映射、Beneish 指标与 Sloan 应计项；不把异常分数直接当作欺诈结论或投资建议。
- 公告日、报告期和可交易日必须分开记录；缺失字段不得静默填充为零。

## 提交产物

- 字段映射表、计算结果、异常样本解释、公告日审计、边界测试和风险说明。
- 记录数据来源、版本、缺失处理、负分母策略和行业/公司口径差异。

## 验收标准

- 公式与参考实现一致，负分母、缺失值和极端值测试有明确结果。
- 每个异常案例都能追溯到数据时点和字段，不使用事后信息。

## 引导自检

- [ ] 先逐字段核对财报口径，再计算指标。
- [ ] 对缺失值、负分母和异常增长单独运行边界测试。
- [ ] 最后检查公告日是否早于信号生成日。

## 运行证据与失败判定

- 保存原始财报字段、单位换算、缺失值处理、逐家公司分项得分和公告日过滤日志。
- 负分母未标记、同比增长使用修订后数据或公告日晚于交易信号时，判定为失败。
- 提交至少一个正常样本、一个边界样本和一个不可判定样本，并说明停止交易规则。

## 最小复现工作流

1. 阅读作业包说明、数据卡和评分细则，冻结报表版本、币种/单位、财年、公告日和字段映射。
2. 运行数据检查，逐项记录缺失、负分母、零分母和修订数据；再运行 Starter Baseline 生成可复算样例。
3. 抽查至少一家公司，把原始字段、分项指标和总分连成审计链；不可计算样本必须显式输出原因。
4. 运行全部测试并保留命令、退出码与失败用例；不得用填零或删除异常行让测试表面通过。
5. 报告区分“异常筛查信号”和“财务造假结论”，保留假阳性/假阴性风险及数据可得性限制。

