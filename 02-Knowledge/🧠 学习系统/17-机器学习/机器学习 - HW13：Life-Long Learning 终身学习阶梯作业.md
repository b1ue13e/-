---
title: "机器学习 - HW13：Life-Long Learning 终身学习阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "机器学习作业"
course: "17-机器学习"
created: 2026-07-31
updated: 2026-07-31
status: learning
difficulty: advanced
importance: A
concept: ["终身学习", "灾难性遗忘", "持续学习"]
prerequisites: ["[[多层神经网络]]", "[[模型评估指标]]", "[[过拟合专题]]"]
tags: [学习, 17-机器学习, 作业, Life-Long-Learning]
aliases: ["ML-HW13-Life-Long-Learning"]
---

# 机器学习 - HW13：Life-Long Learning 终身学习阶梯作业

> 这份作业的重点不是在单个任务上做到最好，而是观察模型在连续任务中为什么会忘、能不能少忘、什么方法更稳。

## 1. 布置时机

- 建议在学完以下内容后布置：
  - 多任务学习或连续任务设定
  - 基本深度学习训练
  - 泛化与过拟合概念
- 最好在学生已经有多次模型训练经验之后布置。

## 2. 前置知识

开始前，学生应该已经会：

1. 理解任务序列和单任务训练的区别。
2. 知道 catastrophic forgetting 是什么。
3. 会记录 task-by-task 结果。
4. 理解 replay 和 regularization 的大致思路。

## 3. 任务背景

你需要让模型连续学习多个任务，并尽量减少旧任务性能下降。

这份作业训练的是：

- 顺序任务训练
- 遗忘量化
- replay 与正则化比较
- 多任务表现记录

## 4. 教学目标

完成后，应该能做到：

1. 观察并量化遗忘现象。
2. 跑通一种缓解遗忘的方法。
3. 比较 replay 和 regularization。
4. 用 task-by-task 表说明问题。

## 5. 老师提供的材料

### 必须提供

- 任务拆分后的数据
- 任务顺序说明
- baseline 说明
- 输出要求

### 最好额外提供

- `starter code`
- forgetting curve 示例
- buffer / 正则化建议

### 建议目录

- 数据：
  - `03-Projects/data/ml_hw13/`
- 代码：
  - `03-Projects/projects-ml/hw13_life_long_learning/train.py`
  - `03-Projects/projects-ml/hw13_life_long_learning/dataset.py`
  - `03-Projects/projects-ml/hw13_life_long_learning/methods.py`
  - `03-Projects/projects-ml/hw13_life_long_learning/eval.py`
  - `03-Projects/projects-ml/hw13_life_long_learning/report.md`

## 6. 数据说明

### 数据类型

- 输入：按任务划分的数据
- 输出：各任务上的表现
- 任务类型：持续学习 / 多任务顺序训练

### 你至少要先弄清楚

1. 一共有多少个任务。
2. 任务顺序是否固定。
3. 每个阶段如何评估旧任务。
4. forgetting 指标如何定义。
5. buffer 或正则化需要什么额外信息。

## 7. 提交物

### 必交

1. `train.py`
2. `eval.py`
3. `report.md`

### 建议提交

1. `forgetting_curve.png`
2. `task_table.csv`
3. `method_comparison.md`

## 8. 评分标准

| 维度 | 占比 | 要求 |
|:---|:---:|:---|
| 基础完成度 | 25% | 跑通顺序训练与评估 |
| 结果质量 | 25% | 有可比较的防遗忘结果 |
| 分析深度 | 35% | 有 forgetting curve 和 task-by-task 分析 |
| 复现规范 | 15% | 任务顺序、buffer、评估口径清楚 |

## 9. 分阶段完成要求

### 第一阶段：先跑通

- 跑顺序训练 baseline
- 记录每个任务后的历史任务表现
- 看清遗忘现象

### 第二阶段：再改进

- 加 replay
- 加 EWC / LwF / SI
- 比较不同方法

### 第三阶段：最后解释

- 比较不同任务顺序
- 解释哪些任务最容易被忘
- 总结最稳方法

## 10. 建议实施步骤

1. 先建立无防遗忘 baseline。
2. 记录 task-by-task 表。
3. 再加入 replay。
4. 然后尝试正则化方法。
5. 最后比较顺序和 buffer 大小。

## 11. 常见坑

- 没记录 task-by-task 表。
- 任务顺序变了却没写清楚。
- replay buffer 太小没效果。
- 正则化方法实现错却没排查。
- 只看最终任务，不看历史任务回落。

## 12. 建议实验表

| 实验编号 | 模型 / 配置 | 防遗忘策略 | 验证观察 | 是否提交 | 备注 |
|:---:|:---|:---|:---|:---:|:---|
| E1 | Sequential baseline | 无 | 待填写 | 否 | 看清遗忘现象 |
| E2 | Replay baseline | buffer replay | 待填写 | 否 | 比较回放效果 |
| E3 | EWC / LwF / SI | 正则化方法 | 待填写 | 否 | 比较不同方法 |
| E4 | Best setup | 最优组合 | 待填写 | 是 | 最终提交版本 |

## 13. 复盘模板

### 本次最终采用

- 模型：
- 防遗忘策略：
- 最终验证观察：
- 是否提交：

### 本次最有效的改动

1.
2.
3.

### 主要失败现象

1.
2.
3.

### 当前判断

- 最容易遗忘的是哪类任务：
- replay 和 regularization 哪个更有效：
- 下次最值得优先尝试的方向：

## 14. 老师批改时最看重什么

1. 你有没有完整记录任务间性能变化。
2. 你有没有真正量化遗忘。
3. 你能不能比较不同防遗忘方法。
4. 你是否会分析哪些任务最容易掉。

## 15. 关联知识点

- [[多层神经网络]]
- [[模型评估指标]]
- [[过拟合专题]]
## 16. 真实作业包

- README：
  - [[03-Projects/projects-ml/hw13_life_long_learning/README.md|hw13_life_long_learning/README.md]]
- Starter：
  - `F:\\-\\03-Projects\\projects-ml\\hw13_life_long_learning\\starter\\`
- Data Card：
  - [[03-Projects/projects-ml/hw13_life_long_learning/data_card.md|data_card.md]]
- Baseline Tracker：
  - [[03-Projects/projects-ml/hw13_life_long_learning/baseline/README.md|baseline/README.md]]
- Report Template：
  - [[03-Projects/projects-ml/hw13_life_long_learning/reports/report_template.md|report_template.md]]
- Rubric：
  - [[03-Projects/projects-ml/hw13_life_long_learning/rubric.md|rubric.md]]

### 当前包定位

- 这是给学生自己完成作业用的 starter 包。
- 当前只提供目录、接口、报告模板和结果记录位。
- 不预置教师答案或可直接提交的 baseline 实现。
