---
title: "机器学习 - HW01：Regression 回归阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "机器学习作业"
course: "17-机器学习"
created: 2026-07-31
updated: 2026-07-31
status: learning
difficulty: intermediate
importance: A
concept: ["线性回归", "特征工程", "泛化误差"]
prerequisites: ["[[线性回归]]", "[[数据集划分与交叉验证]]", "[[模型评估指标]]"]
tags: [学习, 17-机器学习, 作业, 回归]
aliases: ["ML-HW01-Regression"]
---

# 机器学习 - HW01：Regression 回归阶梯作业

> 这是一份真正意义上的第一份机器学习作业。重点不是追求最花哨的模型，而是让你第一次完整经历 `读数据 -> 切验证 -> 建模 -> 调参 -> 提交 -> 解释结果` 的闭环。

## 1. 布置时机

- 建议在学完以下内容后布置：
  - 线性回归
  - 损失函数
  - 梯度下降
  - 训练集 / 验证集 / 测试集
  - 基本评价指标
- 不建议在还没讲清 `validation` 和 `overfitting` 之前布置。
- 这是整门课第一份作业，目的是建立完整实验流程，不是上来就卷复杂模型。

## 2. 前置知识

开始这份作业前，学生应该已经会：

1. 理解输入特征和标签的区别。
2. 理解回归任务输出的是连续值。
3. 知道什么是训练误差、验证误差、测试提交。
4. 会用 Python / PyTorch 或 sklearn 跑一个最基础模型。

## 3. 任务背景

你需要根据给定的结构化特征，预测连续值目标。  
官方常见题型可以类比为：`COVID-19 Cases Prediction`。

这份作业训练的不是“套一个最强模型”，而是下面几件更基础也更重要的能力：

- 会读表格数据
- 会做基础预处理
- 会建立 baseline
- 会区分训练效果和泛化效果
- 会用实验记录说明自己为什么选这个版本

## 4. 教学目标

完成这份作业后，应该能做到：

1. 独立完成一个标准监督学习回归任务。
2. 写出最小可复现实验脚本。
3. 知道该如何判断欠拟合和过拟合。
4. 知道特征处理为什么会改变结果。
5. 能对自己的最终模型做基本解释。

## 5. 老师提供的材料

### 必须提供

- `covid.train.csv`
- `covid.test.csv`
- `sample_submission.csv`
- 字段说明或 `data_card.md`
- baseline 说明
- 建议目录结构

### 最好额外提供

- `starter code`
- 最小运行命令
- 一个 baseline 分数或参考误差区间
- 常见错误提示

### 建议目录

- 数据：
  - `03-Projects/data/ml_hw01/`
- 代码：
  - `03-Projects/projects-ml/hw01_regression/train.py`
  - `03-Projects/projects-ml/hw01_regression/dataset.py`
  - `03-Projects/projects-ml/hw01_regression/model.py`
  - `03-Projects/projects-ml/hw01_regression/infer.py`
  - `03-Projects/projects-ml/hw01_regression/report.md`

## 6. 数据说明

### 数据类型

- 输入：结构化数值特征
- 输出：连续值
- 任务类型：监督学习中的回归

### 你至少要先弄清楚

1. 一共有多少个特征。
2. 有没有缺失值。
3. 标签分布是否偏斜。
4. 是否需要标准化。
5. 验证集如何切分。

### 建议先做的数据检查

- 看列数和样本数
- 看是否有空值
- 看标签均值、方差、极值
- 看训练集与测试集字段是否一致

## 7. 提交物

### 必交

1. `pred.csv`
2. `train.py`
3. `infer.py`
4. `report.md`

### 建议提交

1. `loss_curve.png`
2. `feature_notes.md`
3. `error_analysis.md`

## 8. 评分标准

| 维度 | 占比 | 要求 |
|:---|:---:|:---|
| 基础完成度 | 30% | 能正常读取数据、训练模型、导出提交文件 |
| 结果质量 | 30% | 验证集指标优于 baseline，结果稳定 |
| 分析深度 | 25% | 能解释特征处理、模型选择、误差来源 |
| 复现规范 | 15% | 目录清楚、命令可运行、记录完整 |

### 合格线

- 跑通 baseline
- 有验证集结果
- 有可提交文件
- 有最基本的实验说明

### 优秀线

- 有明确的特征处理和模型对照
- 有残差分析或错误分布分析
- 能说明为什么最终方案更好

## 9. 分阶段完成要求

### 第一阶段：先跑通

- 完成数据读取
- 完成 train / valid 切分
- 跑通一个线性回归或浅层 MLP

### 第二阶段：再改进

- 标准化
- 特征筛选
- 正则化或更合适模型

### 第三阶段：最后解释

- 画训练曲线
- 记录最佳实验
- 分析误差来源

## 10. 建议实施步骤

1. 先写最小 `dataset` 和 `train` 流程。
2. 固定随机种子，切出验证集。
3. 跑通 baseline，并记录首个分数。
4. 一次只改一个因素，例如标准化、特征数、模型结构。
5. 保存最佳模型并生成提交文件。
6. 写复盘，不要只留下一个最终数字。

## 11. 常见坑

- 训练集和验证集切分不固定，结果每次都不一样。
- 标准化时偷看了测试集统计量。
- 只看训练误差，不看验证误差。
- 输出层维度写错，回归却输出成多分类形式。
- 最佳 checkpoint 没保存，最后只剩一个过拟合模型。
- 改了很多东西却没记录，最后不知道哪一步真的有效。

## 12. 建议实验表

| 实验编号 | 模型 / 配置 | 特征处理 | 验证指标 | 是否提交 | 备注 |
|:---:|:---|:---|:---|:---:|:---|
| E1 | Linear Regression baseline | 原始特征 | 待填写 | 否 | 首个可跑通基线 |
| E2 | Linear + 标准化 | 标准化 | 待填写 | 否 | 看标准化是否有效 |
| E3 | MLP baseline | 标准化 + 简单特征筛选 | 待填写 | 否 | 对比线性与非线性 |
| E4 | Best model | 最优组合 | 待填写 | 是 | 记录最终提交版本 |

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

### 主要失败实验

1.
2.

### 当前判断

- 更像欠拟合 / 过拟合：
- 误差主要来自：
- 下次最值得优先尝试的方向：

## 14. 老师批改时最看重什么

1. 你有没有建立 baseline。
2. 你有没有做干净的验证。
3. 你有没有清楚记录实验变化。
4. 你能不能解释为什么这个结果成立。

## 15. 关联知识点

- [[线性回归]]
- [[偏差与方差]]
- [[过拟合专题]]

## 16. 真实作业包

- README：
  - [[03-Projects/projects-ml/hw01_regression/README.md|hw01_regression/README.md]]
- Starter：
  - `F:\\-\\03-Projects\\projects-ml\\hw01_regression\\starter\\`
- Data Card：
  - [[03-Projects/projects-ml/hw01_regression/data_card.md|data_card.md]]
- Baseline Tracker：
  - [[03-Projects/projects-ml/hw01_regression/baseline/README.md|baseline/README.md]]
- Report Template：
  - [[03-Projects/projects-ml/hw01_regression/reports/report_template.md|report_template.md]]
- Rubric：
  - [[03-Projects/projects-ml/hw01_regression/rubric.md|rubric.md]]

### 当前包定位

- 这是给学生自己完成作业用的 starter 包。
- 当前只提供目录、接口、报告模板和结果记录位。
- 不预置教师答案或可直接提交的 baseline 实现。
