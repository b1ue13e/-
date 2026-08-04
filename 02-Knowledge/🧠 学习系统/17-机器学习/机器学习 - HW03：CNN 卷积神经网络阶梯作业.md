---
title: "机器学习 - HW03：CNN 卷积神经网络阶梯作业"
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
concept: ["卷积神经网络", "图像分类", "数据增强"]
prerequisites: ["[[多层神经网络]]", "[[深度学习优化器]]", "[[过拟合专题]]"]
tags: [学习, 17-机器学习, 作业, CNN]
aliases: ["ML-HW03-CNN"]
---

# 机器学习 - HW03：CNN 卷积神经网络阶梯作业

> 这份作业是视觉任务的正式起点。重点不是会背 CNN 名词，而是第一次把图像数据、卷积结构、数据增强和失败样本分析放到一个完整作业里。

## 1. 布置时机

- 建议在学完以下内容后布置：
  - 多层感知机
  - 卷积与池化
  - dropout / batch norm
  - 图像分类基本评估
- 最好在完成 `HW02 Classification` 后布置。

## 2. 前置知识

开始前，学生应该已经会：

1. 理解图像分类和表格分类的差异。
2. 会用 DataLoader 读取图像。
3. 知道 train transform 和 valid transform 不能混用。
4. 会看基本训练曲线。

## 3. 任务背景

你需要对图像做多分类识别。  
官方常见题型可以类比为：`Food-11`。

这份作业训练的是：

- 图像读取和预处理
- CNN 结构搭建
- 数据增强
- 可视化失败样本和类别混淆

## 4. 教学目标

完成后，应该能做到：

1. 用 CNN 跑通图像分类任务。
2. 区分模型结构问题和数据增强问题。
3. 知道 augmentation 为什么有时有帮助、有时会伤害结果。
4. 能通过失败样本做基本诊断。

## 5. 老师提供的材料

### 必须提供

- `training/`
- `validation/`
- `testing/`
- `sample_submission.csv`
- 类别说明
- baseline 说明

### 最好额外提供

- `starter code`
- transform 示例
- 标签映射说明
- baseline 准确率区间

### 建议目录

- 数据：
  - `03-Projects/data/ml_hw03/food-11/`
- 代码：
  - `03-Projects/projects-ml/hw03_cnn/train.py`
  - `03-Projects/projects-ml/hw03_cnn/dataset.py`
  - `03-Projects/projects-ml/hw03_cnn/model.py`
  - `03-Projects/projects-ml/hw03_cnn/infer.py`
  - `03-Projects/projects-ml/hw03_cnn/report.md`

## 6. 数据说明

### 数据类型

- 输入：图像
- 输出：类别标签
- 任务类型：图像分类

### 你至少要先弄清楚

1. 图像尺寸是否统一。
2. 类别数是多少。
3. 是否有类别不平衡。
4. 验证集是否固定。
5. 是否有未标注数据。

## 7. 提交物

### 必交

1. `pred.csv`
2. `train.py`
3. `infer.py`
4. `report.md`

### 建议提交

1. `aug_examples.png`
2. `confusion_matrix.png`
3. `bad_cases.md`

## 8. 评分标准

| 维度 | 占比 | 要求 |
|:---|:---:|:---|
| 基础完成度 | 25% | 能稳定读取图像并跑通 CNN |
| 结果质量 | 35% | 验证集结果优于基础 CNN baseline |
| 分析深度 | 25% | 有 augmentation 对照和失败样本分析 |
| 复现规范 | 15% | 标签映射、路径、命令、配置清晰 |

## 9. 分阶段完成要求

### 第一阶段：先跑通

- 读入数据
- 跑通最小 CNN
- 输出首个 baseline

### 第二阶段：再改进

- 加 augmentation
- 调整 backbone 或训练策略
- 稳定训练曲线

### 第三阶段：最后解释

- 看 confusion matrix
- 看 hardest classes
- 保存失败样本

## 10. 建议实施步骤

1. 先确认目录和标签映射。
2. 跑通最小 CNN，不急着上复杂 backbone。
3. 分开写 train 和 valid transform。
4. 一次只改一组 augmentation。
5. 保存 best checkpoint。
6. 挑 10 个失败样本做说明。

## 11. 常见坑

- train / valid transform 混用。
- resize 和 normalize 顺序不清。
- 类别映射保存不一致。
- augmentation 太重，反而破坏语义。
- 只看总分，不看混淆类别。

## 12. 建议实验表

| 实验编号 | 模型 / 配置 | 数据增强 | 验证指标 | 是否提交 | 备注 |
|:---:|:---|:---|:---|:---:|:---|
| E1 | Simple CNN baseline | resize + toTensor | 待填写 | 否 | 首个图像基线 |
| E2 | CNN + 基础增强 | flip / crop / normalize | 待填写 | 否 | 观察增强收益 |
| E3 | Better backbone | 更深网络 + scheduler | 待填写 | 否 | 比较 backbone 差异 |
| E4 | Best model | 最优增强与结构 | 待填写 | 是 | 最终提交版本 |

## 13. 复盘模板

### 本次最终采用

- 模型：
- 输入尺寸：
- 数据增强组合：
- 最终验证指标：
- 是否提交：

### 本次最有效的改动

1.
2.
3.

### 主要失败样本

1.
2.
3.

### 当前判断

- 最容易混淆的类别：
- augmentation 是否真的有帮助：
- 下次最值得优先尝试的方向：

## 14. 老师批改时最看重什么

1. 你有没有真正做 augmentation 对照。
2. 你有没有分析 hardest classes。
3. 你是否理解图像任务中的泛化问题。
4. 你的结果能否复现。

## 15. 关联知识点

- [[多层神经网络]]
- [[深度学习优化器]]
- [[模型评估指标]]
## 16. 真实作业包

- README：
  - [[03-Projects/projects-ml/hw03_cnn/README.md|hw03_cnn/README.md]]
- Starter：
  - `F:\\-\\03-Projects\\projects-ml\\hw03_cnn\\starter\\`
- Data Card：
  - [[03-Projects/projects-ml/hw03_cnn/data_card.md|data_card.md]]
- Baseline Tracker：
  - [[03-Projects/projects-ml/hw03_cnn/baseline/README.md|baseline/README.md]]
- Report Template：
  - [[03-Projects/projects-ml/hw03_cnn/reports/report_template.md|report_template.md]]
- Rubric：
  - [[03-Projects/projects-ml/hw03_cnn/rubric.md|rubric.md]]

### 当前包定位

- 这是给学生自己完成作业用的 starter 包。
- 当前只提供目录、接口、报告模板和结果记录位。
- 不预置教师答案或可直接提交的 baseline 实现。
