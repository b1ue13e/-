---
title: "机器学习 - HW15：Meta Learning 元学习阶梯作业"
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
concept: ["元学习", "few-shot", "快速适应"]
prerequisites: ["[[多层神经网络]]", "[[模型评估指标]]", "[[梯度下降法]]"]
tags: [学习, 17-机器学习, 作业, Meta-Learning]
aliases: ["ML-HW15-Meta-Learning"]
---

# 机器学习 - HW15：Meta Learning 元学习阶梯作业

> 这份作业是整门课的高阶收束。它不再要求模型在一个固定任务上越训越强，而是要求模型学会“更快适应新任务”，这和前面所有作业都不完全一样。

## 1. 布置时机

- 建议在学完以下内容后布置：
  - few-shot 学习基本概念
  - episodic training
  - 表征学习与泛化
  - 基本优化直觉
- 最好放在整门课最后。

## 2. 前置知识

开始前，学生应该已经会：

1. 理解 support / query 的区别。
2. 知道 few-shot baseline 是什么。
3. 了解 ProtoNet 或 MAML 的基本思路。
4. 会比较不同 `N-way K-shot` 设定。

## 3. 任务背景

你需要让模型在很少样本的新任务上快速适应。

这份作业训练的是：

- few-shot 任务组织
- episodic training
- baseline 与 meta 方法比较
- 不同 way / shot 下的泛化分析

## 4. 教学目标

完成后，应该能做到：

1. 跑通一个 few-shot baseline。
2. 跑通一种 meta learning 方法。
3. 比较不同 way / shot 设定。
4. 解释 meta 方法为什么更快适应。

## 5. 老师提供的材料

### 必须提供

- few-shot 数据划分
- episode 采样规则
- baseline 说明
- 输出要求

### 最好额外提供

- `starter code`
- ProtoNet / MAML 示例
- 任务采样器说明

### 建议目录

- 数据：
  - `03-Projects/data/ml_hw15/`
- 代码：
  - `03-Projects/projects-ml/hw15_meta_learning/train.py`
  - `03-Projects/projects-ml/hw15_meta_learning/dataset.py`
  - `03-Projects/projects-ml/hw15_meta_learning/sampler.py`
  - `03-Projects/projects-ml/hw15_meta_learning/eval.py`
  - `03-Projects/projects-ml/hw15_meta_learning/report.md`

## 6. 数据说明

### 数据类型

- 输入：episode 形式的任务样本
- 输出：few-shot 分类结果
- 任务类型：元学习 / few-shot 泛化

### 你至少要先弄清楚

1. `N-way K-shot` 是如何定义的。
2. support / query 如何划分。
3. 训练和验证 episode 是否同口径。
4. baseline 和 meta 方法是否公平比较。
5. unseen classes 是否单独测试。

## 7. 提交物

### 必交

1. `train.py`
2. `eval.py`
3. `report.md`

### 建议提交

1. `fewshot_table.csv`
2. `episode_analysis.md`
3. `best.ckpt` 信息说明

## 8. 评分标准

| 维度 | 占比 | 要求 |
|:---|:---:|:---|
| 基础完成度 | 25% | 跑通 few-shot baseline 和一种 meta 方法 |
| 结果质量 | 30% | 不同设置下有稳定结果 |
| 分析深度 | 30% | 能分析 way / shot 和适应速度 |
| 复现规范 | 15% | 采样逻辑、配置、评估清楚 |

## 9. 分阶段完成要求

### 第一阶段：先跑通

- 跑一个 few-shot baseline
- 固定 episode 采样规则
- 生成首个结果表

### 第二阶段：再改进

- 跑 ProtoNet 或 MAML
- 比较不同 way / shot
- 比较 unseen classes 表现

### 第三阶段：最后解释

- 分析失败 episode
- 总结 meta 增益来自哪里
- 解释哪个设定最难

## 10. 建议实施步骤

1. 先写清 support / query 采样逻辑。
2. 先跑一个简单 baseline。
3. 再跑一种 meta 方法。
4. 对比多个 `way-shot` 设定。
5. 挑失败 episode 做分析。

## 11. 常见坑

- 训练和验证 episode 口径不一致。
- support / query 划分写错。
- few-shot baseline 太弱，比较不公平。
- 只记一个 `way-shot` 设定。
- 中间最好模型没保存。

## 12. 建议实验表

| 实验编号 | 模型 / 配置 | way-shot 设置 | 验证观察 | 是否提交 | 备注 |
|:---:|:---|:---|:---|:---:|:---|
| E1 | Few-shot baseline | 5-way 1-shot | 待填写 | 否 | 首个可比较基线 |
| E2 | ProtoNet / MAML | 5-way 1-shot | 待填写 | 否 | 对比 meta 增益 |
| E3 | Same model | 5-way 5-shot / 10-way | 待填写 | 否 | 看设定变化影响 |
| E4 | Best setup | 最优组合 | 待填写 | 是 | 最终提交版本 |

## 13. 复盘模板

### 本次最终采用

- 模型：
- way / shot 设置：
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

- 主要瓶颈在特征表示 / episode 采样 / 优化：
- meta 方法的主要收益体现在哪：
- 下次最值得优先尝试的方向：

## 14. 老师批改时最看重什么

1. 你有没有公平比较 baseline 和 meta 方法。
2. 你有没有做不同 way / shot 设定。
3. 你能不能解释 meta 方法为何有增益。
4. 你的 episode 采样规则是否清楚可复现。

## 15. 关联知识点

- [[多层神经网络]]
- [[梯度下降法]]
- [[模型评估指标]]
## 16. 真实作业包

- README：
  - [[03-Projects/projects-ml/hw15_meta_learning/README.md|hw15_meta_learning/README.md]]
- Starter：
  - `F:\\-\\03-Projects\\projects-ml\\hw15_meta_learning\\starter\\`
- Data Card：
  - [[03-Projects/projects-ml/hw15_meta_learning/data_card.md|data_card.md]]
- Baseline Tracker：
  - [[03-Projects/projects-ml/hw15_meta_learning/baseline/README.md|baseline/README.md]]
- Report Template：
  - [[03-Projects/projects-ml/hw15_meta_learning/reports/report_template.md|report_template.md]]
- Rubric：
  - [[03-Projects/projects-ml/hw15_meta_learning/rubric.md|rubric.md]]

### 当前包定位

- 这是给学生自己完成作业用的 starter 包。
- 当前只提供目录、接口、报告模板和结果记录位。
- 不预置教师答案或可直接提交的 baseline 实现。
