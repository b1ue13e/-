---
type: project
topic: "结构化输出与LLM Judge"
project_type: homework
course: "生成式AI基础与Prompt工程"
assignment_id: "生成式AI基础与Prompt工程-05"
assignment_level: lesson
assignment_format: lab
stage_id: "04"
requires: ["[[Prompt工程-需求-任务规格与结构化输出]]", "[[Prompt评测-实验-指标数据集与误差分析]]", "[[Prompt评测-LLMJudge-偏置校准与人工复核]]"]
source_type: local_integration_task
created: 2026-08-05
status: planned
flow: project
tags: [作业, 45-生成式AI基础与Prompt工程, LLMJudge]
source: "Original lab aligned with Stanford CS324 evaluation structure"
source_url: "https://stanford-cs324.github.io/winter2022/"
accessed: 2026-08-09
license: "本地原创作业；公开课程页面仅作评测结构参考"
---

# 作业 05：结构化输出与 LLM Judge

## 可执行 starter Gate

运行 `python course_lab.py 05 --output assignment05-offline.json`。starter 含 8 个 JSON 正反例，严格校验字段集合、类别、priority 类型/范围和非空 evidence；pairwise Judge 对同一候选交换 A/B 位置再评分，要求 schema accuracy 与 swap consistency 均为 1.0。独立迁移必须接真实模型输出并加入盲化人工复核。

| 子任务 | 对应笔记 | 指标 |
| :--- | :--- | :--- |
| JSON Schema | [[Prompt工程-需求-任务规格与结构化输出]] | 解析率、字段正确率 |
| 确定性校验 | [[Prompt评测-实验-指标数据集与误差分析]] | 准确率/F1/单测通过率 |
| Judge Rubric | [[Prompt评测-LLMJudge-偏置校准与人工复核]] | 与人工一致率 |
| A/B 位置交换 | [[Prompt评测-LLMJudge-偏置校准与人工复核]] | 翻转率 |
| 长度对照 | [[Prompt评测-LLMJudge-偏置校准与人工复核]] | 长度偏置 |

## 最小知识点集
- [ ] Schema、解析异常、Rubric、人工金标准

## 学习目标

- 为结构化输出定义字段集合、类型、范围和失败关闭策略，并用正反例测试。
- 将确定性校验与开放式 Judge 分工：能由 schema、真值或单测判定的部分不交给模型评审。
- 用位置交换、盲化和人工金标准量化 Judge 偏置与一致性。

## 任务边界

离线 pairwise fixture 只验证交换协议，不代表真实 Judge 的可靠性。真实 Judge 必须记录模型 ID、Rubric、候选随机化和人工复核样本；高风险或低一致率样本必须路由人工。

## 提交产物

1. `artifacts/assignment05-offline.json` 与 schema 测试结果。
2. 至少 8 个正反例，覆盖缺字段、额外字段、类型错误和越界值。
3. 位置交换前后结果、翻转率、与人工一致率及分歧样本。
4. Judge 适用/禁用边界和人工接管规则。

## 验收标准

运行 `python scripts/course_lab.py 05 --output artifacts/assignment05-offline.json` 返回 0；schema accuracy 和 swap consistency 均为 1.0；真实 Judge 结论必须给出人工校准证据，不能把模型评分当真值。

## 引导自检

- [ ] parser 是否拒绝额外字段和错误类型？
- [ ] 候选 A/B 是否只交换位置，没有改文本？
- [ ] 是否检查长度、风格和自偏好，而不只检查位置偏置？
- [ ] Judge 与人工分歧时是否保留原始输入和复核结论？

## 全面知识点
- [ ] 置信区间、双人标注一致性、分歧样本路由

## 验收
- 100 条样本、20 条双人金标准、位置与长度偏置报告；Judge 不得替代确定性真值。
