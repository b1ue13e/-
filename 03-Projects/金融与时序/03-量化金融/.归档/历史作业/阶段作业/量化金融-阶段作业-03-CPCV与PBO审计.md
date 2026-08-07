---
type: project
project_type: homework
course: "量化金融"
assignment_id: "QF-ST03-04"
assignment_level: stage
assignment_format: lab
stage_id: "03"
requires: ["[[Purged Group TimeSeries Cross-Validation 净化交叉验证 (Purged Group K-Fold CV)]]", "[[PBO回测过拟合概率与Deflated Sharpe Ratio (Probability of Backtest Overfitting)]]"]
source_type: local_integration_task
source: "real_assignment_packages/hw12_cpcv_pbo"
source_url: "[[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw12_cpcv_pbo/README|HW12 可执行作业包]]"
license: "Repository-authored"
created: 2026-08-06
status: active
flow: project
tags: [作业, 量化金融]
---
# 量化金融-阶段作业-03-CPCV与PBO审计

## 学习目标

用 [[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw12_cpcv_pbo/README|HW12 可执行作业包]] 构造带 purge 与 embargo 的组合时间路径，审计候选策略的泄漏、选择偏差、PBO 和去偏 Sharpe；与随机切分的乐观结果对照。

## 任务边界

- 只审计时间切分、purge、embargo、PBO 与 DSR；不把一次策略收益排名当作泛化证明。
- 组合路径必须在研究协议中预先固定，测试集只做最终审计。

## 提交产物

- 明确标签区间、持有期和 embargo；运行全部测试。
- 提交切分可视化、审计表、PBO/DSR 结果、失败策略和停止规则。评分：切分 30，过拟合审计 30，对照 15，解释 15，可复现性 10。

## 验收标准

- purge/embargo 测试通过；随机切分与净化切分差异可解释。
- 报告列出停止规则、失败策略和 PBO/DSR 的不确定性，不以单一阈值宣称有效。

## 引导自检

- [ ] 先画时间块和标签持有区间。
- [ ] 再检查 purge/embargo 是否覆盖重叠样本。
- [ ] 最后运行 PBO/DSR 并保留失败策略。

## 运行证据与失败判定

- 提交时间块图、每折训练/验证索引、purge/embargo 区间、策略排名矩阵和 PBO/DSR 计算表。
- 标签持有期与验证集重叠、组合路径重复、失败策略被删除或只报告最佳 Sharpe 时，判定为失败。
- 保存一组故意泄漏的负例测试，证明审计能捕获时间边界错误，而不是只运行正常路径。

## 最小复现工作流

1. 阅读作业包说明、数据卡与 Rubric，冻结标签持有期、时间块数、测试块组合、purge、embargo 和候选策略集。
2. 运行数据检查并画出每条路径的训练/验证边界；先运行无保护负例，再启用 CPCV 比较乐观偏差。
3. 保存每条路径的策略排名、相对表现、PBO 输入和 DSR 中间量；失败策略不得从矩阵中删除。
4. 运行全部测试并记录命令、退出码和失败用例；组合路径缺失或时间重叠未清除时停止评分。
5. 报告区分回测流程通过与策略有效性，说明 PBO/DSR 的样本不确定性和拒绝上线条件。
