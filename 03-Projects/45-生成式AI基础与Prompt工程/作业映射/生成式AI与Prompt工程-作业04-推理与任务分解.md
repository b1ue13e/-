---
type: project
topic: "推理与任务分解"
created: 2026-08-05
status: active
progress: 0%
flow: project
kind: problem-type
tags: [项目, 45-生成式AI基础与Prompt工程, 作业映射, 推理]
source: "Original lab aligned with CMU 17-630 Weeks 3/6 and UC Berkeley LLM Reasoning lecture"
---

# 作业 04：推理与任务分解

## 可执行 starter Gate

在 `03-Projects/45-生成式AI基础与Prompt工程/starter/` 运行 `python course_lab.py 04 --output assignment04-offline.json`。固定 10 个结构化算术任务，每题必须产生 `parse → execute → verify` 三段 trace 且答案全对；CLI 失败返回 2。该夹具只验证分解协议，独立迁移仍需换成自然语言多步任务并加入工具失败。

| 策略 | 对应笔记 | 必交结果 |
| :--- | :--- | :--- |
| Direct | [[Prompt工程-需求-任务规格与结构化输出]] | 基线 |
| Few-shot | [[Prompt工程-上下文学习-示例选择与提示敏感性]] | 示例与顺序 |
| 分解 | [[Prompt工程-推理-任务分解自一致性与验证]] | 依赖图和中间状态 |
| 自一致性 | [[生成控制-解码-温度Top-k与Top-p]] | 一致率、成本 |
| 外部验证 | [[Prompt工程-推理-任务分解自一致性与验证]] | 代码/检索验证器 |

## 最小知识点集
- [ ] 步骤成功率、误差传播、重试与回退

## 全面知识点
- [ ] least-to-most、plan-and-solve、step-back、chain-of-verification

## 验收
- 至少 40 个多步题；不得把更长答案自动视为更好；关键结论有独立验证器。
