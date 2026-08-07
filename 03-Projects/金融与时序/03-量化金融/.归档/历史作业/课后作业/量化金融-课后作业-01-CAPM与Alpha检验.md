---
type: project
project_type: homework
course: "量化金融"
assignment_id: "QF-HW01"
assignment_level: lesson
assignment_format: lab
stage_id: "01"
requires: ["[[收益率与对数收益率]]", "[[CAPM 资本资产定价模型]]"]
source_type: local_integration_task
source: "real_assignment_packages/hw01_capm_alpha_beta"
source_url: "[[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw01_capm_alpha_beta/README|HW01 可执行作业包]]"
license: "Repository-authored"
created: 2026-08-06
status: active
flow: project
tags: [作业, 量化金融]
---
# 量化金融-课后作业-01-CAPM与Alpha检验

## 学习目标

实现市场模型回归，区分总收益与超额收益，解释 Alpha、Beta、显著性和残差诊断。完整数据契约、Starter Code 与边界测试见 [[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw01_capm_alpha_beta/README|HW01 可执行作业包]]。

## 任务边界

1. 校验资产、市场与无风险利率的日期、频率和缺失值，生成数据审计摘要。
2. 计算对齐后的超额收益，估计 CAPM，并报告系数、置信区间、样本期和诊断图。
3. 改变频率或样本窗口做稳健性检验，解释 Alpha 是否仍有经济意义。

## 环境与执行

- 在作业包目录运行 `python starter/check_data.py`、`python starter/run.py` 和 `python -m pytest tests -q`。
- 提交代码、数据卡、结果表、诊断图、两页以内研究报告和命令日志；不得提交教师答案或密钥。
- 评分：数据与无泄漏 20，模型正确性 30，诊断与稳健性 20，解释 20，可复现性 10。提交前确认随机种子、时间边界和输出路径已记录。

## 提交产物

- `data_card.md`、运行日志、回归结果表、残差诊断图和研究报告。
- 报告必须同时写出样本期、收益口径、无风险利率口径和成交时点；只提交净值曲线不算完成。

## 验收标准

- 通过数据检查、Starter Code 和全部测试；Alpha/Beta 与参考实现误差在作业包规定容差内。
- 至少完成一个频率或样本窗口稳健性对照，并解释统计显著性与经济意义的差别。

## 引导自检

- [ ] 先确认资产、市场和无风险利率日期完全对齐。
- [ ] 再检查超额收益是否使用同一频率的无风险利率。
- [ ] 最后运行测试并核对报告中的样本期、随机种子和输出路径。

## 运行证据与失败判定

- 保存数据快照、回归表、残差诊断图和测试命令；结果文件名包含样本区间与随机种子。
- 若日期对齐、无风险利率频率或基准收益口径任一不一致，判定为失败，不解释 Alpha 经济含义。
- 更换一个样本窗口复跑；若 Alpha 符号、置信区间或样本量变化未记录，提交不完整。

## 最小复现工作流

1. 先阅读作业包 `README.md`、`data_card.md` 与 `rubric.md`，记录 Python/依赖版本、输入文件摘要、样本频率和起止日期；未冻结输入前不解释结果。
2. 原样运行 `python starter/check_data.py`，保存退出码、行数、缺失率和日期边界；数据检查未通过时停止，不跳过检查直接拟合。
3. 运行 `python starter/run.py` 生成朴素基线，再完成自己的实现；报告把基线、主结果和稳健性实验放在同一口径下比较。
4. 运行 `python -m pytest tests -q`，保存完整命令、退出码和失败用例。测试通过只证明接口与边界满足约定，不等同于结论成立。
5. 报告按“主张—证据—限制—下一步”组织；负结果、异常样本和未通过实验必须保留，不能只提交最终图。

