---
type: reference
project_type: homework
course: "机器学习"
assignment_level: lesson
assignment_format: problem-set
topic: "BERT 自监督表征"
status: ongoing
created: 2026-08-06
updated: 2026-08-06
adapted_from: "李宏毅《Machine Learning》2021 Spring"
source_url: "https://speech.ee.ntu.edu.tw/~hylee/ml/2021-spring.php"
requires: ["[[机器学习-无监督学习]]"]
license: "本地学习用途；外部教材仅 link-only，不复制教材答案"
source_license_status: "待验证"
tags: [作业, 机器学习, BERT 自监督表征]
flow: project
source_type: open_textbook_exercise
assignment_id: "机器学习-DL-05"
stage_id: "专题"
---


# 机器学习 · 深度学习专题（可选参考）：BERT 自监督表征

> 这份作业的重点不是“再训练一个更大的模型”，而是理解预训练表示为什么强、什么时候有用、什么时候会被数据清洗和截断策略拖后腿。

## 1. 布置时机

- 建议在学完以下内容后布置：
  - Transformer 基础
  - 预训练与微调
  - 文本表示与 tokenizer
  - 序列长度和显存管理
- 最好在 `HW05 Transformer` 之后布置。

## 2. 前置知识

开始前，学生应该已经会：

1. 理解 tokenization 的基本过程。
2. 会跑一个基础 transformer 任务。
3. 知道 fine-tuning 和从头训练的区别。
4. 会分析长度截断对结果的影响。

## 3. 任务背景

你需要把预训练语言模型迁移到具体下游任务。  
常见题型可以是：文本分类、问答、序列标注。

这份作业训练的是：

- tokenizer 和文本清洗
- 预训练模型微调
- 截断策略与 batch 设计
- 错例分析和迁移收益判断

## 4. 学习目标

完成后，应该能做到：

1. 正确微调一个预训练语言模型。
2. 对比不同 `max_length` 和学习率设置。
3. 说明预训练带来的收益。
4. 解释为什么某些错例和文本长度、领域偏差有关。

## 5. 环境（材料与数据）
> ⚠️ **数据 / Starter 占位说明**：本仓库**未内置**任何数据集或 starter 代码。下方 `03-Projects/...` 路径是按李宏毅 ML2021 课程结构预留的**本地布局占位**，并非已就绪资源。实际数据、starter 与预训练权重请从课程主页（`source_url`）获取，并放入 `03-Projects/17-机器学习/data/<本作业>/` 与 `.../代码/<本作业>/`。未自行配置数据集与运行环境前，本作业骨架**不可直接运行**。


### 必须提供

- 训练 / 验证 / 测试文本
- 标签说明
- tokenizer 版本
- baseline 说明

### 最好额外提供

- `starter code`
- 预训练权重来源说明
- 参考 `max_length`
- 显存预算建议

### 建议目录

- 数据：
  - `03-Projects/data/ml_hw07/`
- 代码：
  - `03-Projects/projects-ml/hw07_bert/train.py`
  - `03-Projects/projects-ml/hw07_bert/dataset.py`
  - `03-Projects/projects-ml/hw07_bert/model.py`
  - `03-Projects/projects-ml/hw07_bert/infer.py`
  - `03-Projects/projects-ml/hw07_bert/report.md`

## 6. 数据说明

### 数据类型

- 输入：文本
- 输出：标签或 span / token 结果
- 任务类型：NLP 下游任务

### 你至少要先弄清楚

1. tokenizer 版本是否固定。
2. 文本长度分布如何。
3. 标签映射如何保存。
4. 输入格式是单句、句对还是段落。
5. 哪些样本容易被截断。

## 7. 提交产物

### 必交

1. `pred.csv`
2. `train.py`
3. `infer.py`
4. `report.md`

### 建议提交

1. `ablation.md`
2. `bad_cases.md`
3. `best.ckpt` 信息说明

## 8. 验收标准与 Rubric
> **最低通过门槛**：满足 Rubric「基础完成度」全部要求且结果可复现（附环境 / 命令 / 随机种子），即视为通过；总分 ≥ 80/100 为良好。


| 维度 | 占比 | 要求 |
|:---|:---:|:---|
| 基础完成度 | 25% | 能完成微调与推理 |
| 结果质量 | 35% | 优于简单 baseline |
| 分析深度 | 25% | 能分析 tokenizer、长度和错例 |
| 复现规范 | 15% | tokenizer、label map、配置清晰 |

## 9. 分阶段完成要求

### 第一阶段：先跑通

- 跑通标准 fine-tuning
- 固定 tokenizer 和标签映射
- 生成首个 baseline

### 第二阶段：再改进

- 对比 `max_length`
- 调整 batch 和 learning rate
- 尝试冻结层或分层 lr

### 第三阶段：最后解释

- 看长文本错例
- 看领域偏差样本
- 总结预训练收益

## 10. 建议实施步骤

1. 先固定 tokenizer 版本。
2. 用默认微调参数跑一个基线。
3. 调 `max_length` 和 learning rate。
4. 再尝试冻结底层或分层学习率。
5. 挑错例分析截断和词义偏差。

## 11. 引导与自检

- tokenizer 版本不一致。
- label map 没固定。
- `max_length` 太短导致信息丢失。
- OOM 后盲目降 batch 却忘了梯度累积。
- 只看总分，不看错例。

## 12. 建议实验表

| 实验编号 | 模型 / 配置 | tokenizer / 截断策略 | 验证指标 | 是否提交 | 备注 |
|:---:|:---|:---|:---|:---:|:---|
| E1 | BERT baseline | 默认 tokenizer + 默认长度 | 待填写 | 否 | 首个 fine-tuning 基线 |
| E2 | BERT + max length 调整 | 长度 / batch size 调整 | 待填写 | 否 | 看截断影响 |
| E3 | 冻结层 / 分层 lr | 冻结底层或分组学习率 | 待填写 | 否 | 看稳定性与泛化 |
| E4 | Best model | 最优组合 | 待填写 | 是 | 最终提交版本 |

## 13. 复盘模板

### 本次最终采用

- 模型：
- tokenizer / 词表版本：
- max length：
- 最终验证指标：
- 是否提交：

### 本次最有效的改动

1.
2.
3.

### 主要错误类型

1.
2.
3.

### 当前判断

- 主要瓶颈在 tokenization / 截断 / 数据清洗 / 微调策略：
- 预训练带来的最大增益体现在哪：
- 下次最值得优先尝试的方向：

## 14. 老师批改时最看重什么

1. 你有没有把 tokenizer 和标签体系讲清楚。
2. 你有没有比较长度和微调策略。
3. 你是否能解释预训练为什么有帮助。
4. 你是否会看错例，而不只看一个分数。

## 15. 关联知识点

- [[机器学习-神经网络]]
- [[机器学习-梯度下降]]
- [[机器学习-模型评估指标]]
## 16. 真实作业包

- README：
  - `hw07_bert/README.md`
- Starter：
  - `F:\\-\\03-Projects\\projects-ml\\hw07_bert\\starter\\`
- Data Card：
  - `data_card.md`
- Baseline Tracker：
  - `baseline/README.md`
- Report Template：
  - `report_template.md`
- Rubric：
  - `rubric.md`

### 当前包定位

- 这是给学生自己完成作业用的 starter 包。
- 当前只提供目录、接口、报告模板和结果记录位。
- 不预置教师答案或可直接提交的 baseline 实现。
