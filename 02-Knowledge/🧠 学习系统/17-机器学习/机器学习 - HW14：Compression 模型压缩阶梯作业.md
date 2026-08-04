---
title: "机器学习 - HW14：Compression 模型压缩阶梯作业"
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
concept: ["模型压缩", "剪枝", "量化", "蒸馏"]
prerequisites: ["[[多层神经网络]]", "[[模型评估指标]]", "[[过拟合专题]]"]
tags: [学习, 17-机器学习, 作业, Compression]
aliases: ["ML-HW14-Compression"]
---

# 机器学习 - HW14：Compression 模型压缩阶梯作业

> 这份作业把你从“会训练模型”往“会交付模型”推一步。关键不是把模型压得最小，而是学会衡量精度、速度、体积三者之间的取舍。

## 1. 布置时机

- 建议在学完以下内容后布置：
  - 模型训练与评估
  - 蒸馏、剪枝、量化基本概念
  - 部署中的延迟和内存约束
- 最好在学生已经有一个成熟教师模型后布置。

## 2. 前置知识

开始前，学生应该已经会：

1. 保存和评估一个成熟模型。
2. 理解参数量、模型大小和延迟不是一回事。
3. 知道蒸馏、剪枝、量化的大致差异。
4. 会用统一脚本做评估。

## 3. 任务背景

你需要在尽量少损失性能的前提下，把模型变小、变快、变易部署。

这份作业训练的是：

- 小模型与原模型对照
- 蒸馏 / 剪枝 / 量化
- 精度-速度-大小权衡
- 工程口径的一致评估

## 4. 教学目标

完成后，应该能做到：

1. 跑通至少一种压缩方法。
2. 用统一口径比较压缩前后模型。
3. 解释哪种压缩最值当。
4. 理解“参数量减少”不一定等于“真实变快”。

## 5. 老师提供的材料

### 必须提供

- 原始教师模型或 baseline 模型
- 验证集
- 评估脚本
- baseline 说明

### 最好额外提供

- `starter code`
- latency 测量建议
- 量化 / 蒸馏示例

### 建议目录

- 数据：
  - `03-Projects/data/ml_hw14/`
- 代码：
  - `03-Projects/projects-ml/hw14_compression/train_teacher.py`
  - `03-Projects/projects-ml/hw14_compression/train_student.py`
  - `03-Projects/projects-ml/hw14_compression/compress.py`
  - `03-Projects/projects-ml/hw14_compression/eval.py`
  - `03-Projects/projects-ml/hw14_compression/report.md`

## 6. 数据说明

### 数据类型

- 输入：验证数据与原模型
- 输出：压缩后模型及评估结果
- 任务类型：模型工程优化任务

### 你至少要先弄清楚

1. 用什么硬件测速度。
2. batch size 是否固定。
3. 原模型的 baseline 是多少。
4. 量化或蒸馏后要不要再微调。
5. 真实部署更关心参数、体积还是延迟。

## 7. 提交物

### 必交

1. `compress.py`
2. `eval.py`
3. `report.md`

### 建议提交

1. `compression_table.csv`
2. `latency_benchmark.md`
3. `best.ckpt` 信息说明

## 8. 评分标准

| 维度 | 占比 | 要求 |
|:---|:---:|:---|
| 基础完成度 | 25% | 跑通至少一种压缩方法 |
| 结果质量 | 30% | 压缩收益和精度损失清楚可比 |
| 分析深度 | 30% | 能分析精度-速度-大小权衡 |
| 复现规范 | 15% | 评估硬件、batch、脚本清楚 |

## 9. 分阶段完成要求

### 第一阶段：先跑通

- 固定教师模型
- 做一种基础压缩
- 记录初步结果

### 第二阶段：再改进

- 尝试量化或蒸馏
- 比较不同方法
- 记录延迟和体积

### 第三阶段：最后解释

- 总结最值当方案
- 解释为什么某方案收益不明显
- 做三维权衡比较

## 10. 建议实施步骤

1. 先固定 baseline 模型和验证脚本。
2. 跑简单剪枝或小模型基线。
3. 再做蒸馏或量化。
4. 统一硬件和 batch 测速度。
5. 做压缩前后对照表。

## 11. 常见坑

- 不同实验用不同硬件测速度。
- 只看参数量，不看真实 latency。
- 量化后精度掉很多却没有再校准。
- 学生模型太小根本学不动。
- 前后评估脚本不一致。

## 12. 建议实验表

| 实验编号 | 模型 / 配置 | 压缩策略 | 验证观察 | 是否提交 | 备注 |
|:---:|:---|:---|:---|:---:|:---|
| E1 | Smaller model / pruning baseline | 简单压缩 | 待填写 | 否 | 首个压缩基线 |
| E2 | Quantization / KD | 单一压缩策略 | 待填写 | 否 | 比较精度损失 |
| E3 | Combined compression | 组合压缩 | 待填写 | 否 | 看收益是否叠加 |
| E4 | Best setup | 最优组合 | 待填写 | 是 | 最终提交版本 |

## 13. 复盘模板

### 本次最终采用

- 教师 / 原始模型：
- 压缩策略：
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

- 最值当的是参数压缩 / 延迟优化 / 精度保持：
- 哪种压缩方式最稳：
- 下次最值得优先尝试的方向：

## 14. 老师批改时最看重什么

1. 你有没有统一评估口径。
2. 你有没有比较真实延迟而不只看参数量。
3. 你能不能解释压缩收益和损失。
4. 你是否做了有意义的工程取舍。

## 15. 关联知识点

- [[多层神经网络]]
- [[模型评估指标]]
- [[深度学习优化器]]
## 16. 真实作业包

- README：
  - [[03-Projects/projects-ml/hw14_compression/README.md|hw14_compression/README.md]]
- Starter：
  - `F:\\-\\03-Projects\\projects-ml\\hw14_compression\\starter\\`
- Data Card：
  - [[03-Projects/projects-ml/hw14_compression/data_card.md|data_card.md]]
- Baseline Tracker：
  - [[03-Projects/projects-ml/hw14_compression/baseline/README.md|baseline/README.md]]
- Report Template：
  - [[03-Projects/projects-ml/hw14_compression/reports/report_template.md|report_template.md]]
- Rubric：
  - [[03-Projects/projects-ml/hw14_compression/rubric.md|rubric.md]]

### 当前包定位

- 这是给学生自己完成作业用的 starter 包。
- 当前只提供目录、接口、报告模板和结果记录位。
- 不预置教师答案或可直接提交的 baseline 实现。
