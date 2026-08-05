---
type: project
topic: "结构化输出与LLM Judge"
created: 2026-08-05
status: active
progress: 0%
flow: project
kind: problem-type
tags: [项目, 45-生成式AI基础与Prompt工程, 作业映射, LLMJudge]
source: "Original lab aligned with Stanford CS224N 2026 benchmarking materials and public Assignment 4 reference"
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

## 全面知识点
- [ ] 置信区间、双人标注一致性、分歧样本路由

## 验收
- 100 条样本、20 条双人金标准、位置与长度偏置报告；Judge 不得替代确定性真值。
