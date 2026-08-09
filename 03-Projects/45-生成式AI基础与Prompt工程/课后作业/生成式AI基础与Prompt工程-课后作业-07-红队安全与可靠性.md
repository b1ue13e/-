---
type: project
topic: "红队、安全与可靠性"
project_type: homework
course: "生成式AI基础与Prompt工程"
assignment_id: "生成式AI基础与Prompt工程-07"
assignment_level: lesson
assignment_format: lab
stage_id: "04"
requires: ["[[Prompt工程-安全-提示注入与分层防护]]", "[[生成式AI-可靠性-幻觉校准与事实核验]]", "[[Prompt评测-LLMJudge-偏置校准与人工复核]]"]
source_type: local_integration_task
created: 2026-08-05
status: planned
flow: project
tags: [作业, 45-生成式AI基础与Prompt工程, 安全]
source: "Original lab aligned with Berkeley LLM Agents MOOC Labs 2-3 and CMU 17-630 Week 8"
source_url: "https://www.cs.cmu.edu/~breaux/prompting/schedule.html"
accessed: 2026-08-09
license: "本地原创作业；公开课程页面仅作能力目标参考"
---

# 作业 07：红队、安全与可靠性

## 可执行 starter Gate

运行 `python course_lab.py 07 --output assignment07-offline.json`。固定矩阵按 typed `source/action` 决策，高风险动作暂停、外部数据不能授予非只读能力；按实际 `allow_action` 计算 ASR，同时报告 TSR/FRR，要求 `0/1/0`。该策略回归不含可复用攻击载荷，也不构成真实模型生产安全证明。

| 威胁 | 对应笔记 | 防护验收 |
| :--- | :--- | :--- |
| 直接注入 | [[Prompt工程-安全-提示注入与分层防护]] | 规则不被覆盖 |
| 间接注入 | [[Prompt工程-安全-提示注入与分层防护]] | 文档不触发动作 |
| 事实幻觉 | [[生成式AI-可靠性-幻觉校准与事实核验]] | 支持率/拒答率 |
| 隐私泄漏 | [[Prompt工程-安全-提示注入与分层防护]] | 敏感字段不输出 |
| Judge 欺骗 | [[Prompt评测-LLMJudge-偏置校准与人工复核]] | 人工抽查发现率 |

## 最小知识点集
- [ ] 资产、攻击者、入口、权限、影响、检测与恢复

## 学习目标

- 画出资产、攻击者、入口、信任边界、权限和副作用的最小威胁模型。
- 为直接/间接注入、越权、泄漏和事实失败建立可重复的红队矩阵。
- 同时报告攻击成功率、正常任务成功率和误拒率，避免“全拒答即安全”。

## 任务边界

本作业只使用课程内无害攻击样本与假 canary，不测试真实账号、密钥、内网或第三方系统。任何写操作均由类型化策略暂停并要求人工确认；离线策略通过不等于生产系统安全。

## 提交产物

1. `artifacts/assignment07-offline.json` 与策略测试日志。
2. 威胁模型、资产/入口表和至少 20 条回归样本。
3. ASR、TSR、FRR 及每个失败样本的处置记录。
4. 最小权限、审批摘要、日志和恢复方案。

## 验收标准

运行 `python scripts/course_lab.py 07 --output artifacts/assignment07-offline.json` 返回 0；固定矩阵达到 ASR=0、TSR=1、FRR=0；外部数据不能授予权限；高风险动作必须暂停；报告同时说明未覆盖攻击面。

## 引导自检

- [ ] 策略是否基于来源和动作类型，而非脆弱关键词列表？
- [ ] 正常只读请求是否仍可完成？
- [ ] 人工确认前是否展示目标、参数和副作用摘要？
- [ ] 日志是否足以复盘攻击入口、决策和恢复动作？

## 全面知识点
- [ ] jailbreak、数据投毒、sycophancy、PII、最小权限、审批和红队回归

## 验收
- 至少 30 条攻击与 20 条正常样本；报告防御前后攻击成功率、误报率和残余风险。
