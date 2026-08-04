---
title: "机器学习 - HW05：Transformer 阶梯作业"
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
concept: ["Transformer", "序列到序列", "注意力机制"]
prerequisites: ["[[多层神经网络]]", "[[深度学习优化器]]", "[[模型评估指标]]"]
tags: [学习, 17-机器学习, 作业, Transformer]
aliases: ["ML-HW05-Transformer"]
---

# 机器学习 - HW05：Transformer 阶梯作业

> 这份作业是整门课里第一个真正的序列生成作业。它要求你不只是会分类，而是要学会把输入序列翻译成输出序列，并且能评估生成结果到底好不好。

## 1. 布置时机

- 建议在学完以下内容后布置：
  - self-attention
  - encoder / decoder 基本结构
  - 序列到序列任务
  - teacher forcing 与解码
- 最好在 `HW04 Self-Attention` 后布置。

## 2. 前置知识

开始前，学生应该已经会：

1. 理解 token、词表、padding、mask。
2. 知道 encoder 和 decoder 的分工。
3. 理解 greedy decode 和 beam search 的区别。
4. 知道序列任务不能只看 loss，也要看样例输出。

## 3. 任务背景

你需要把输入序列转换成输出序列。  
官方常见题型可以类比为：`Machine Translation`。

这份作业训练的是：

- tokenizer 和词表
- seq2seq 训练
- 解码策略
- 生成样例与失败分析

## 4. 教学目标

完成后，应该能做到：

1. 跑通一个标准 transformer seq2seq 模型。
2. 区分训练 loss 和生成质量。
3. 比较不同解码策略的效果。
4. 通过样例输出分析模型错误。

## 5. 老师提供的材料

### 必须提供

- `train.en / train.zh`
- `valid.en / valid.zh`
- `test.en`
- tokenizer 或 subword 模型
- `sample_submission`

### 最好额外提供

- `starter code`
- tokenizer 构建说明
- baseline 参考结果
- 后处理规则说明

### 建议目录

- 数据：
  - `03-Projects/data/ml_hw05/`
- 代码：
  - `03-Projects/projects-ml/hw05_transformer/train.py`
  - `03-Projects/projects-ml/hw05_transformer/dataset.py`
  - `03-Projects/projects-ml/hw05_transformer/model.py`
  - `03-Projects/projects-ml/hw05_transformer/decode.py`
  - `03-Projects/projects-ml/hw05_transformer/report.md`

## 6. 数据说明

### 数据类型

- 输入：源语言序列
- 输出：目标语言序列
- 任务类型：序列生成 / 机器翻译

### 你至少要先弄清楚

1. tokenizer 是如何构造的。
2. special tokens 有哪些。
3. source / target 词表是否分开。
4. 长句如何截断或分桶。
5. 验证时用什么指标和样例来判断效果。

## 7. 提交物

### 必交

1. `pred.txt` 或 `pred.csv`
2. `train.py`
3. `decode.py`
4. `report.md`

### 建议提交

1. `samples.md`
2. `beam_vs_greedy.md`
3. `loss_curve.png`

## 8. 评分标准

| 维度 | 占比 | 要求 |
|:---|:---:|:---|
| 基础完成度 | 25% | 能跑通训练与解码 |
| 结果质量 | 35% | 验证结果和样例输出达到 baseline 以上 |
| 分析深度 | 25% | 有解码策略和失败样例分析 |
| 复现规范 | 15% | tokenizer、词表、后处理清楚 |

## 9. 分阶段完成要求

### 第一阶段：先跑通

- 数据和 tokenizer 跑通
- transformer baseline 跑通
- 能输出可读结果

### 第二阶段：再改进

- warmup / label smoothing
- beam search
- 更合理的 batch 和长度策略

### 第三阶段：最后解释

- 对比 greedy 与 beam
- 看失败翻译样例
- 解释最终设置的取舍

## 10. 建议实施步骤

1. 先固定 tokenizer 和词表版本。
2. 用最小模型跑通基线。
3. 先看几条样例输出，不急着调大模型。
4. 再加 warmup、label smoothing、beam search。
5. 保存 best checkpoint 和解码配置。

## 11. 常见坑

- source / target tokenizer 混乱。
- decoder causal mask 写错。
- special tokens 没处理干净。
- 只看指标，不看生成样例。
- beam size 一味增大却没有收益。

## 12. 建议实验表

| 实验编号 | 模型 / 配置 | 解码策略 | 验证指标 | 是否提交 | 备注 |
|:---:|:---|:---|:---|:---:|:---|
| E1 | Small transformer baseline | greedy | 待填写 | 否 | 首个 seq2seq 基线 |
| E2 | + warmup / label smoothing | greedy | 待填写 | 否 | 看训练稳定性 |
| E3 | Best checkpoint + beam search | beam search | 待填写 | 否 | 比较解码收益 |
| E4 | Final submission | 最优组合 | 待填写 | 是 | 最终提交版本 |

## 13. 复盘模板

### 本次最终采用

- 模型：
- tokenizer / 词表版本：
- 解码策略：
- 最终验证指标：
- 是否提交：

### 本次最有效的改动

1.
2.
3.

### 主要翻译错误

1.
2.
3.

### 当前判断

- 主要瓶颈在数据清洗 / tokenization / 模型容量 / 解码策略：
- greedy 与 beam 的主要差异：
- 下次最值得优先尝试的方向：

## 14. 老师批改时最看重什么

1. 你有没有把 tokenizer 和解码流程讲清楚。
2. 你有没有分析生成样例，而不是只报分数。
3. 你有没有比较不同解码策略。
4. 你的结果能不能被别人重跑出来。

## 15. 关联知识点

- [[深度学习优化器]]
- [[过拟合专题]]
- [[模型评估指标]]
## 16. 真实作业包

- README：
  - [[03-Projects/projects-ml/hw05_transformer/README.md|hw05_transformer/README.md]]
- Starter：
  - `F:\\-\\03-Projects\\projects-ml\\hw05_transformer\\starter\\`
- Data Card：
  - [[03-Projects/projects-ml/hw05_transformer/data_card.md|data_card.md]]
- Baseline Tracker：
  - [[03-Projects/projects-ml/hw05_transformer/baseline/README.md|baseline/README.md]]
- Report Template：
  - [[03-Projects/projects-ml/hw05_transformer/reports/report_template.md|report_template.md]]
- Rubric：
  - [[03-Projects/projects-ml/hw05_transformer/rubric.md|rubric.md]]

### 当前包定位

- 这是给学生自己完成作业用的 starter 包。
- 当前只提供目录、接口、报告模板和结果记录位。
- 不预置教师答案或可直接提交的 baseline 实现。
