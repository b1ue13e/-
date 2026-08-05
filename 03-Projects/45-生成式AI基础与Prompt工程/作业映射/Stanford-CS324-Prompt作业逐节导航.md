---
type: project
topic: "Stanford CS324 Prompt 作业逐节导航"
created: 2026-08-05
status: active
progress: 0%
tags: [项目, 45-生成式AI基础与Prompt工程, Stanford-CS324, Prompt]
flow: project
kind: moc
source: "Stanford CS324 Winter 2023 Intro Assignment and Winter 2022 Project 1 public pages; link-only use"
---

# Stanford CS324 Prompt 作业逐节导航

> [!warning] 授权边界
> CS324 作业公开可访问，但未见统一开放许可。本页只按公开章节标题导航，不复制题面、数据或答案。入口：[2023 Intro Assignment](https://stanford-cs324.github.io/winter2023/assignment/)；[2022 Project 1 PDF](https://stanford-cs324.github.io/winter2022/assignments/project1.pdf)。

## Intro Assignment 逐部分映射

| 官方部分 | 完成所需知识 | 对应笔记 | 自建验收（非官方题面） |
| :--- | :--- | :--- | :--- |
| Part 1: Understanding foundation models | 模型能力、适配、局限 | [[生成式AI-基础-概率生成Token与能力边界]]、[[模型适配-对齐-SFT-RLHF与DPO]] | 能区分模型、方法、任务与指标 |
| Part 2: Using foundation models | Prompt 基线、API/界面、模型差异 | [[Prompt工程-需求-任务规格与结构化输出]]、[[Prompt工程-上下文学习-示例选择与提示敏感性]] | 固定 20 条开发集比较两个方案 |
| Part 3: Foundation models in the news | 主张、证据、风险与利益相关者 | [[生成式AI-可靠性-幻觉校准与事实核验]]、[[Prompt工程-安全-提示注入与分层防护]] | 对一则报道做证据—主张表 |

## Project 1 逐节映射

| 官方章节 | 交付关注 | 对应笔记 | 本课检查点 |
| :--- | :--- | :--- | :--- |
| §1 Overview | 项目目标与两条主线 | [[Prompt工程-需求-任务规格与结构化输出]] | 一页任务规格 |
| §2 Capabilities | 能力研究问题与实验 | [[Prompt工程-上下文学习-示例选择与提示敏感性]]、[[Prompt评测-实验-指标数据集与误差分析]] | 开发/测试隔离 |
| §2.1 Task | 任务、数据、指标 | [[Prompt工程-需求-任务规格与结构化输出]] | 输入/输出/边界完整 |
| §2.2 Approach | 方法、基线、比较 | [[Prompt工程-方法-指令示例推理与约束]] | 只改一个变量 |
| §2.3 Deliverables | 结果、分析与可复现材料 | [[课程前置-Python-JSON测试与实验复现]] | 配置、逐样本结果、失败分类 |
| §3 Risks | 风险研究与缓解 | [[生成式AI-可靠性-幻觉校准与事实核验]]、[[Prompt工程-安全-提示注入与分层防护]] | 威胁模型与对照测试 |
| §4 Focal Property | 选定属性的深入分析 | [[Prompt评测-LLMJudge-偏置校准与人工复核]] | 属性定义、量规、人工复核 |

## 与本课程原创作业的关系

- [[生成式AI与Prompt工程-作业02-Prompt基线与模型比较]] 是 Intro 的本地教学化练习，不是 Stanford 原题。
- [[生成式AI与Prompt工程-作业03-Prompt受控实验]] 借鉴 P1 的交付结构，但数据、问题和验收均为本课原创。
- 官方作业与本地作业分开归档，报告中不得把本地结果写成 Stanford 课程成绩或官方复现。

