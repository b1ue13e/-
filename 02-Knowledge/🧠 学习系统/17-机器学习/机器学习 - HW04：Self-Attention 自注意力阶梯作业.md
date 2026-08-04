---
title: "机器学习 - HW04：Self-Attention 自注意力阶梯作业"
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
concept: ["自注意力", "序列建模", "位置编码"]
prerequisites: ["[[多层神经网络]]", "[[梯度下降法]]", "[[模型评估指标]]"]
tags: [学习, 17-机器学习, 作业, Self-Attention]
aliases: ["ML-HW04-Self-Attention"]
---

# 机器学习 - HW04：Self-Attention 自注意力阶梯作业

> 这份作业不是让你记住 attention 公式，而是让你第一次真正感受到“序列中的每个位置都可以和别的位置交互”会带来什么表达能力。

## 1. 布置时机

- 建议在学完以下内容后布置：
  - RNN 的局限
  - Q / K / V 的基本含义
  - multi-head attention
  - 残差与 layer norm
- 最好在 CNN 作业之后、Transformer 作业之前布置。

## 2. 前置知识

开始前，学生应该已经会：

1. 理解序列数据和图像数据的区别。
2. 知道 mask 在序列任务中的作用。
3. 会用 batch 组织不等长序列。
4. 会看训练和验证曲线。

## 3. 任务背景

你需要对序列进行分类或表征。  
官方常见题型可以类比为：`Speaker Classification`。

这份作业训练的是：

- 序列输入组织
- attention block 的搭建
- pooling / 长度策略选择
- attention 模型与传统结构的比较

## 4. 教学目标

完成后，应该能做到：

1. 跑通基本 attention encoder。
2. 理解 sequence length、head 数、hidden size 会如何影响训练。
3. 看懂 padding mask 为什么必要。
4. 用简单消融说明模型结构选择。

## 5. 老师提供的材料

### 必须提供

- 训练特征文件
- 测试特征文件
- 标签文件
- `speaker2id.json`
- `sample_submission.csv`

### 最好额外提供

- `starter code`
- 处理变长序列的示例
- 一个 baseline 结果

### 建议目录

- 数据：
  - `03-Projects/data/ml_hw04/`
- 代码：
  - `03-Projects/projects-ml/hw04_self_attention/train.py`
  - `03-Projects/projects-ml/hw04_self_attention/dataset.py`
  - `03-Projects/projects-ml/hw04_self_attention/model.py`
  - `03-Projects/projects-ml/hw04_self_attention/infer.py`
  - `03-Projects/projects-ml/hw04_self_attention/report.md`

## 6. 数据说明

### 数据类型

- 输入：序列特征
- 输出：类别标签
- 任务类型：序列分类

### 你至少要先弄清楚

1. 序列长度是否固定。
2. padding 规则是什么。
3. mask 是如何构造的。
4. 类别数和标签映射是否固定。
5. 训练和推理的切块规则是否一致。

## 7. 提交物

### 必交

1. `pred.csv`
2. `train.py`
3. `infer.py`
4. `report.md`

### 建议提交

1. `ablation.md`
2. `length_analysis.md`
3. `bad_cases.md`

## 8. 评分标准

| 维度 | 占比 | 要求 |
|:---|:---:|:---|
| 基础完成度 | 25% | 跑通 attention 模型与推理 |
| 结果质量 | 35% | 指标优于简单 baseline |
| 分析深度 | 25% | 有结构消融或长度策略分析 |
| 复现规范 | 15% | mask、标签映射、推理流程清楚 |

## 9. 分阶段完成要求

### 第一阶段：先跑通

- 正确读取变长序列
- 跑通最小 attention 模型
- 生成首个验证结果

### 第二阶段：再改进

- 比较 pooling
- 调整 head / hidden size
- 稳定训练

### 第三阶段：最后解释

- 做简单消融
- 记录 hardest sequences
- 写出结构选择理由

## 10. 建议实施步骤

1. 先确保 padding 和 mask 正确。
2. 先用单层模型跑通。
3. 再增加 heads、残差、layer norm。
4. 控制变量做 pooling 对照。
5. 保存最佳结果和配置。

## 11. 常见坑

- 忘记处理 padding mask。
- 训练和推理切块方式不一致。
- 标签映射没固定。
- hidden size 一味增大导致显存爆掉。
- 只会调分，不做结构对照。

## 12. 建议实验表

| 实验编号 | 模型 / 配置 | 序列策略 | 验证指标 | 是否提交 | 备注 |
|:---:|:---|:---|:---|:---:|:---|
| E1 | Single-layer attention baseline | 固定长度切块 | 待填写 | 否 | 跑通 Q/K/V 流程 |
| E2 | Multi-head attention | 多头 + residual | 待填写 | 否 | 比较 heads 数 |
| E3 | Attention vs pooling | 不同 pooling 方式 | 待填写 | 否 | 做结构消融 |
| E4 | Best model | 最优 head / hidden / length | 待填写 | 是 | 最终提交版本 |

## 13. 复盘模板

### 本次最终采用

- 模型：
- heads / hidden size：
- 序列长度策略：
- 最终验证指标：
- 是否提交：

### 本次最有效的改动

1.
2.
3.

### 主要错误类型

1.
2.

### 当前判断

- 主要瓶颈在序列长度 / pooling / 模型容量 / 数据噪声：
- attention 权重是否提供了可解释信息：
- 下次最值得优先尝试的方向：

## 14. 老师批改时最看重什么

1. 你有没有真正处理好变长序列。
2. 你有没有做结构消融。
3. 你能不能说明 attention 相比简单聚合的价值。
4. 你的推理流程是否可复现。

## 15. 关联知识点

- [[多层神经网络]]
- [[深度学习优化器]]
- [[过拟合专题]]
## 16. 真实作业包

- README：
  - [[03-Projects/projects-ml/hw04_self_attention/README.md|hw04_self_attention/README.md]]
- Starter：
  - `F:\\-\\03-Projects\\projects-ml\\hw04_self_attention\\starter\\`
- Data Card：
  - [[03-Projects/projects-ml/hw04_self_attention/data_card.md|data_card.md]]
- Baseline Tracker：
  - [[03-Projects/projects-ml/hw04_self_attention/baseline/README.md|baseline/README.md]]
- Report Template：
  - [[03-Projects/projects-ml/hw04_self_attention/reports/report_template.md|report_template.md]]
- Rubric：
  - [[03-Projects/projects-ml/hw04_self_attention/rubric.md|rubric.md]]

### 当前包定位

- 这是给学生自己完成作业用的 starter 包。
- 当前只提供目录、接口、报告模板和结果记录位。
- 不预置教师答案或可直接提交的 baseline 实现。
