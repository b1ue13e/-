---
title: "机器学习 - HW02：Classification 分类阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "机器学习作业"
course: "17-机器学习"
created: 2026-07-31
updated: 2026-08-01
status: learning
difficulty: intermediate
importance: A
concept: ["分类算法", "逻辑回归", "生成式模型"]
prerequisites: ["[[逻辑回归]]", "[[线性判别分析]]", "[[模型评估指标]]"]
tags: [学习, 17-机器学习, 作业, 分类]
aliases: ["ML-HW02-Classification"]
---

# 机器学习 - HW02：Classification 分类阶梯作业

> 这份作业是监督学习基本功的第二步。你已经做过回归，现在要真正建立“分类任务”的完整直觉，包括标签、交叉熵、类别边界、混淆矩阵和错误分析。

## 1. 布置时机

- 建议在学完以下内容后布置：
  - 逻辑回归
  - softmax 与交叉熵
  - 判别式与生成式分类
  - 基本评估指标
- 这份作业最好紧接 `HW01 Regression` 之后布置。
- 如果学生还不会切验证集、不会看混淆矩阵，就不适合直接往后推进。

## 2. 前置知识

开始前，学生应该已经会：

1. 理解分类与回归的差异。
2. 知道标签是离散类别，不是连续值。
3. 会用 PyTorch 或 sklearn 跑一个最简单的分类器。
4. 知道准确率、F1、confusion matrix 的基本含义。

## 3. 任务背景

你需要根据输入特征预测类别标签。  
官方常见题型可以类比为：`Phoneme Classification`。

这份作业训练的是：

- 分类任务的数据组织方式
- 类别边界和错分分析
- 简单模型到多层模型的过渡
- 从“能跑通”升级到“能解释为什么错”

## 4. 教学目标

完成后，应该能做到：

1. 独立完成一个基础分类任务。
2. 解释为什么某些类别容易混淆。
3. 理解判别式模型和生成式模型的差异。
4. 用验证集和混淆矩阵分析结果，而不是只看一个总分。

## 5. 老师提供的材料

### 必须提供

- `train_11.npy`
- `train_label_11.npy`
- `test_11.npy`
- 标签范围说明：39 类，编号 `0–38`
- 提交格式说明：`Id,Class`
- 可复现的本地 baseline 框架

### 最好额外提供

- `starter code`
- 最小运行命令
- 一个 baseline 精度区间
- confusion matrix 示例图

### 建议目录

- 数据：
  - `03-Projects/data/ml_hw02/timit_11/`
- 代码：
  - `03-Projects/projects-ml/hw02_classification/train.py`
  - `03-Projects/projects-ml/hw02_classification/dataset.py`
  - `03-Projects/projects-ml/hw02_classification/model.py`
  - `03-Projects/projects-ml/hw02_classification/infer.py`
  - `03-Projects/projects-ml/hw02_classification/report.md`

## 6. 数据说明

### 数据类型

- 输入：声学特征或结构化向量
- 输入维度：429，即 11 帧上下文 × 每帧 39 维
- 输出：39 个音素类别，标签为 `0–38`
- 任务类型：多分类

> [!warning] 文件名中的 `11` 不是类别数
> `train_11.npy` 的 `11` 表示上下文帧数量。官方任务是 **39 类**分类，模型输出层必须是 39 维。

### 你至少要先弄清楚

1. 输入维度是多少。
2. 一共有多少个类别。
3. 标签是否连续编号。
4. 是否存在类别不平衡。
5. 验证集如何切分。

## 7. 提交物

### 必交

1. `pred.csv`
2. `train.py`
3. `infer.py`
4. `report.md`

### 建议提交

1. `confusion_matrix.png`
2. `loss_curve.png`
3. `error_cases.md`

## 8. 评分标准

| 维度 | 占比 | 要求 |
|:---|:---:|:---|
| 基础完成度 | 25% | 能跑通训练、验证、推理 |
| 结果质量 | 35% | 验证指标稳定优于 baseline |
| 分析深度 | 25% | 能做混淆矩阵和错分类别分析 |
| 复现规范 | 15% | 路径、命令、标签映射清楚 |

### 合格线

- 跑通 baseline
- 有验证集精度
- 有提交文件
- 有最基本的分类结果说明

### 优秀线

- 有模型对照
- 有错分类别解释
- 有类别不平衡或错误分布分析

## 9. 分阶段完成要求

### 第一阶段：先跑通

- 读入数据
- 切验证集
- 跑通一个小型 MLP 或逻辑回归

### 第二阶段：再改进

- 标准化
- dropout / batch norm / scheduler
- 更深网络或更好的训练策略

### 第三阶段：最后解释

- 画 confusion matrix
- 分析 hardest classes
- 解释最终方案为什么更好

## 10. 建议实施步骤

1. 先检查输入维度和标签范围。
2. 用最小分类器跑出首个基线。
3. 固定随机种子并保留最优 checkpoint。
4. 一次只改一个训练因素。
5. 在验证集上做 confusion matrix。
6. 写下最容易错的类别对。

## 11. 常见坑

- 标签类型不是 `LongTensor`。
- 输出层类别数写错。
- 只看训练集准确率。
- 混淆矩阵标签顺序和真实标签顺序错位。
- 改了很多超参数但没记录。

## 12. 建议实验表

| 实验编号 | 模型 / 配置 | 正则化 / 技巧 | 验证指标 | 是否提交 | 备注 |
|:---:|:---|:---|:---|:---:|:---|
| E1 | Logistic / 小型 MLP baseline | 无 | 待填写 | 否 | 首个分类基线 |
| E2 | MLP + Dropout | dropout | 待填写 | 否 | 看泛化是否改善 |
| E3 | MLP + BN + Scheduler | batch norm + lr 调度 | 待填写 | 否 | 稳定训练 |
| E4 | Best checkpoint | 最优组合 | 待填写 | 是 | 最终提交版本 |

## 13. 复盘模板

### 本次最终采用

- 模型：
- 关键超参数：
- 最终验证指标：
- 是否提交：

### 本次最有效的改动

1.
2.
3.

### 主要错分类别

1.
2.
3.

### 当前判断

- 最大瓶颈在模型 / 特征 / 数据清洗 / 类别不平衡：
- 下次最值得优先尝试的方向：

## 14. 老师批改时最看重什么

1. 你有没有做干净的验证。
2. 你有没有分析错分类别。
3. 你是不是只会调分，还是能解释分类边界问题。
4. 你的提交和报告能不能复现。

## 15. 关联知识点

- [[逻辑回归]]
- [[线性判别分析]]
- [[类别不平衡问题]]
## 16. 真实作业包

- README：
  - [[03-Projects/projects-ml/hw02_classification/README.md|hw02_classification/README.md]]
- Starter：
  - `F:\\-\\03-Projects\\projects-ml\\hw02_classification\\starter\\`
- Data Card：
  - [[03-Projects/projects-ml/hw02_classification/data_card.md|data_card.md]]
- Baseline Tracker：
  - [[03-Projects/projects-ml/hw02_classification/baseline/README.md|baseline/README.md]]
- Report Template：
  - [[03-Projects/projects-ml/hw02_classification/reports/report_template.md|report_template.md]]
- Rubric：
  - [[03-Projects/projects-ml/hw02_classification/rubric.md|rubric.md]]

### 当前包定位

- 已升级为可运行的本地原创 baseline 包，覆盖数据校验、分层划分、标准化、MLP 训练、checkpoint、推理、混淆矩阵和 `Id,Class` 提交。
- 官方约 355 MB 压缩包保持 `link-only`；使用下载器获取后不进入 Git。
- 自动测试使用同样 `429` 维、`39` 类契约的合成 smoke 数据，不包含官方答案。
- 仍不预置教师答案、第三方权重或虚构成绩；真实 baseline 数字必须由本人运行后回填。
- 2026-08-01 本地验证：语法编译通过，自动测试 `3 passed`，官方远端文件大小核验通过；尚未下载和训练全量数据。

### 验证命令

```powershell
python -m pytest "03-Projects/projects-ml/hw02_classification/tests" -q
```
