---
type: project
topic: "推理与任务分解"
project_type: homework
course: "生成式AI基础与Prompt工程"
assignment_id: "生成式AI基础与Prompt工程-04"
assignment_level: lesson
assignment_format: lab
stage_id: "03"
requires: ["[[Prompt工程-推理-任务分解自一致性与验证]]", "[[Prompt评测-实验-指标数据集与误差分析]]"]
source_type: local_integration_task
created: 2026-08-05
status: planned
flow: project
tags: [作业, 45-生成式AI基础与Prompt工程, 推理]
source: "Original lab aligned with CMU 17-630 Weeks 3/6 and UC Berkeley LLM Reasoning lecture"
source_url: "https://www.cs.cmu.edu/~breaux/prompting/schedule.html"
accessed: 2026-08-09
license: "本地原创作业；公开课程页面仅作能力目标参考"
---

# 作业 04：推理与任务分解

## 可执行 starter Gate

在项目根目录运行 `python scripts/course_lab.py 04 --output artifacts/assignment04-offline.json`。固定 10 个结构化算术任务，每题必须产生 `parse → execute → verify` 三段 trace 且答案全对；CLI 失败返回 2。该夹具只验证分解协议，独立迁移仍需换成自然语言多步任务并加入工具失败。

| 策略 | 对应笔记 | 必交结果 |
| :--- | :--- | :--- |
| Direct | [[Prompt工程-需求-任务规格与结构化输出]] | 基线 |
| Few-shot | [[Prompt工程-上下文学习-示例选择与提示敏感性]] | 示例与顺序 |
| 分解 | [[Prompt工程-推理-任务分解自一致性与验证]] | 依赖图和中间状态 |
| 自一致性 | [[生成控制-解码-温度Top-k与Top-p]] | 一致率、成本 |
| 外部验证 | [[Prompt工程-推理-任务分解自一致性与验证]] | 代码/检索验证器 |

## 最小知识点集
- [ ] 步骤成功率、误差传播、重试与回退

## 学习目标

- 把复杂任务按信息依赖拆成可检查的状态转移，而不是按句子机械切分。
- 为每一步定义输入、输出、验证器、最大重试和失败回退。
- 比较 direct 与分解方案的端到端成功率、成本和延迟，并识别累计失败。

## 任务边界

离线算术夹具只验证 `parse → execute → verify` 协议，不证明自然语言推理能力。独立迁移必须换成至少一个自然语言多步任务，并故意注入一次解析或工具失败；不要求保存模型隐藏推理，只保留必要状态和证据。

## 提交产物

1. `artifacts/assignment04-offline.json` 和测试退出码。
2. 一张任务依赖图及各状态的 schema。
3. direct/分解对照表和一次失败后的重试或回退 trace。
4. 对分解是否值得保留的决策说明。

## 验收标准

运行 `python scripts/course_lab.py 04 --output artifacts/assignment04-offline.json` 返回 0；10 个固定任务全部产生三段 trace；验证失败不能被标记为成功；独立任务报告端到端成功率而非只报每步局部正确率。

## 引导自检

- [ ] 每一步是否有真实可执行或可人工复核的验证器？
- [ ] 同一模型“自我反思”是否被误写成独立验证？
- [ ] 分解增加的成本和新失败点是否被计入？
- [ ] 验证失败时流程是否停止、回退或升级，而非继续生成结论？

## 全面知识点
- [ ] least-to-most、plan-and-solve、step-back、chain-of-verification

## 验收
- 至少 40 个多步题；不得把更长答案自动视为更好；关键结论有独立验证器。
