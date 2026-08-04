---
title: "机器学习 - HW08：Autoencoder 自编码器阶梯作业"
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
concept: ["自编码器", "表示学习", "异常检测"]
prerequisites: ["[[多层神经网络]]", "[[主成分分析]]", "[[模型评估指标]]"]
tags: [学习, 17-机器学习, 作业, Autoencoder]
aliases: ["ML-HW08-Autoencoder"]
---

# 机器学习 - HW08：Autoencoder 自编码器阶梯作业

> 这份作业会把“会做监督学习”往前推一步，进入表示学习和异常检测。重点不是把重建损失降到最低，而是理解 latent 表示到底学到了什么。

## 1. 布置时机

- 建议在学完以下内容后布置：
  - 表示学习基本概念
  - 降维与重建
  - PCA 直觉
  - 异常检测基本思路
- 最好在学生已经做过至少一个图像或特征任务之后布置。

## 2. 前置知识

开始前，学生应该已经会：

1. 理解输入和重建目标的关系。
2. 理解 latent representation 的基本直觉。
3. 知道 reconstruction error 可以用来做什么。
4. 会看输入 / 重建对照图。

## 3. 任务背景

你需要通过压缩再重建来学习表示，并把重建误差用于异常检测或表示分析。

这份作业训练的是：

- 无监督表示学习
- latent 维度设计
- 重建质量判断
- 阈值选择与异常检测

## 4. 教学目标

完成后，应该能做到：

1. 跑通基础 autoencoder。
2. 解释 latent dim 改变的影响。
3. 比较普通 AE 和变体 AE。
4. 用 reconstruction error 做基本异常检测。

## 5. 老师提供的材料

### 必须提供

- 训练数据
- 测试数据
- 基础数据说明
- baseline 要求

### 最好额外提供

- `starter code`
- 重建图示例
- 阈值选择思路
- 变体模型建议

### 建议目录

- 数据：
  - `03-Projects/data/ml_hw08/`
- 代码：
  - `03-Projects/projects-ml/hw08_autoencoder/train.py`
  - `03-Projects/projects-ml/hw08_autoencoder/dataset.py`
  - `03-Projects/projects-ml/hw08_autoencoder/model.py`
  - `03-Projects/projects-ml/hw08_autoencoder/infer.py`
  - `03-Projects/projects-ml/hw08_autoencoder/report.md`

## 6. 数据说明

### 数据类型

- 输入：图像或特征向量
- 输出：重建后的同形输入
- 任务类型：无监督表示学习 / 异常检测

### 你至少要先弄清楚

1. 输入范围是否归一化。
2. latent dim 应该多大。
3. 用什么损失重建。
4. 阈值如何设定。
5. 是否需要可视化 latent space。

## 7. 提交物

### 必交

1. `pred.csv` 或异常分数输出
2. `train.py`
3. `infer.py`
4. `report.md`

### 建议提交

1. `reconstruction_examples.png`
2. `error_distribution.png`
3. `latent_visualization.png`

## 8. 评分标准

| 维度 | 占比 | 要求 |
|:---|:---:|:---|
| 基础完成度 | 25% | 跑通训练和重建 |
| 结果质量 | 30% | 重建和异常检测效果达到 baseline |
| 分析深度 | 30% | 能解释 latent、误差分布和阈值选择 |
| 复现规范 | 15% | 路径、损失、阈值规则清楚 |

## 9. 分阶段完成要求

### 第一阶段：先跑通

- 跑通基础 AE
- 保存输入 / 重建图
- 生成初始异常分数

### 第二阶段：再改进

- 调 latent dim
- 比较 AE 变体
- 改善重建效果

### 第三阶段：最后解释

- 看 error distribution
- 分析异常样本
- 解释 latent 学到的结构

## 10. 建议实施步骤

1. 先固定输入预处理方式。
2. 跑通一个最小 AE。
3. 保存重建样本，不只看 loss。
4. 调 latent dim 和模型深度。
5. 最后再尝试 VAE、denoising AE 或 sparse AE。

## 11. 常见坑

- 输入没归一化。
- 只看 loss，不看重建图。
- latent dim 过大导致模型只是记忆。
- 阈值凭感觉设定。
- 不同变体损失定义混用。

## 12. 建议实验表

| 实验编号 | 模型 / 配置 | latent / 损失设定 | 验证观察 | 是否提交 | 备注 |
|:---:|:---|:---|:---|:---:|:---|
| E1 | AE baseline | 基础 MSE | 待填写 | 否 | 首个重建基线 |
| E2 | Deep AE / Denoising AE | 更深结构或加噪训练 | 待填写 | 否 | 比较重建质量 |
| E3 | VAE / Sparse AE | 变体比较 | 待填写 | 否 | 看表示学习差异 |
| E4 | Best model | 最优组合 | 待填写 | 是 | 最终提交版本 |

## 13. 复盘模板

### 本次最终采用

- 模型：
- latent dim：
- 损失函数：
- 最终验证指标：
- 是否提交：

### 本次最有效的改动

1.
2.
3.

### 主要失败现象

1.
2.

### 当前判断

- 主要瓶颈在表示能力 / 阈值选择 / 预处理：
- latent 是否学到了可解释结构：
- 下次最值得优先尝试的方向：

## 14. 老师批改时最看重什么

1. 你有没有真正看重建结果。
2. 你有没有解释 latent 表示。
3. 你是否理解异常检测里的阈值问题。
4. 你是否做了结构对照而不是只报一个结果。

## 15. 关联知识点

- [[主成分分析]]
- [[多层神经网络]]
- [[模型评估指标]]
## 16. 真实作业包

- README：
  - [[03-Projects/projects-ml/hw08_autoencoder/README.md|hw08_autoencoder/README.md]]
- Starter：
  - `F:\\-\\03-Projects\\projects-ml\\hw08_autoencoder\\starter\\`
- Data Card：
  - [[03-Projects/projects-ml/hw08_autoencoder/data_card.md|data_card.md]]
- Baseline Tracker：
  - [[03-Projects/projects-ml/hw08_autoencoder/baseline/README.md|baseline/README.md]]
- Report Template：
  - [[03-Projects/projects-ml/hw08_autoencoder/reports/report_template.md|report_template.md]]
- Rubric：
  - [[03-Projects/projects-ml/hw08_autoencoder/rubric.md|rubric.md]]

### 当前包定位

- 这是给学生自己完成作业用的 starter 包。
- 当前只提供目录、接口、报告模板和结果记录位。
- 不预置教师答案或可直接提交的 baseline 实现。
