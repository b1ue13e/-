---
type: project
topic: "红队、安全与可靠性"
created: 2026-08-05
status: active
progress: 0%
flow: project
kind: problem-type
tags: [项目, 45-生成式AI基础与Prompt工程, 作业映射, 安全]
source: "Original lab aligned with Berkeley LLM Agents MOOC Labs 2-3 and CMU 17-630 Week 8"
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

## 全面知识点
- [ ] jailbreak、数据投毒、sycophancy、PII、最小权限、审批和红队回归

## 验收
- 至少 30 条攻击与 20 条正常样本；报告防御前后攻击成功率、误报率和残余风险。
