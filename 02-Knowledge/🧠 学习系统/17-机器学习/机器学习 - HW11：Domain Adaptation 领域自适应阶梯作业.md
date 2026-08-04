---
title: "机器学习 - HW11：Domain Adaptation 领域自适应阶梯作业"
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
concept: ["领域自适应", "分布偏移", "迁移学习"]
prerequisites: ["[[多层神经网络]]", "[[模型评估指标]]", "[[过拟合专题]]"]
tags: [学习, 17-机器学习, 作业, Domain-Adaptation]
aliases: ["ML-HW11-Domain-Adaptation"]
---

# 机器学习 - HW11：Domain Adaptation 领域自适应阶梯作业

> 这份作业的核心不是把 source 域分数做高，而是直面一个真实问题：训练分布和使用分布不一样时，模型到底还能不能工作。

## 1. 布置时机

- 建议在学完以下内容后布置：
  - 至少一个成熟分类模型
  - 分布偏移和泛化概念
  - 迁移学习基本直觉
- 最好在可信性和鲁棒性相关作业之后布置。

## 2. 前置知识

开始前，学生应该已经会：

1. 训练 source-only baseline。
2. 理解 domain gap。
3. 知道 target domain 可能没有标签。
4. 会做 source 和 target 的可视化或错误分析。

## 3. 任务背景

你需要把在 source 域训练好的模型迁移到 target 域，降低分布偏移带来的性能下滑。

这份作业训练的是：

- source-only baseline
- 特征对齐
- 伪标签与一致性策略
- target 域失败分析

## 4. 教学目标

完成后，应该能做到：

1. 量化 domain gap。
2. 跑通一种基础 adaptation 方法。
3. 比较 adaptation 前后 target 表现。
4. 解释 adaptation 为什么有效或为什么失败。

## 5. 老师提供的材料

### 必须提供

- source 数据
- target 数据
- target 测试集
- baseline 说明

### 最好额外提供

- `starter code`
- 一种基础 adaptation 方法参考
- domain gap 可视化示例

### 建议目录

- 数据：
  - `03-Projects/data/ml_hw11/`
- 代码：
  - `03-Projects/projects-ml/hw11_domain_adaptation/train.py`
  - `03-Projects/projects-ml/hw11_domain_adaptation/dataset.py`
  - `03-Projects/projects-ml/hw11_domain_adaptation/model.py`
  - `03-Projects/projects-ml/hw11_domain_adaptation/infer.py`
  - `03-Projects/projects-ml/hw11_domain_adaptation/report.md`

## 6. 数据说明

### 数据类型

- 输入：source / target 两域数据
- 输出：target 域预测
- 任务类型：跨域分类

### 你至少要先弄清楚

1. source 和 target 差异在哪里。
2. target 是否完全无标签。
3. 预处理是否在两域上一致。
4. target 评价指标是什么。
5. adaptation 是否会引入伪标签噪声。

## 7. 提交物

### 必交

1. `pred.csv`
2. `train.py`
3. `infer.py`
4. `report.md`

### 建议提交

1. `domain_gap_analysis.md`
2. `target_bad_cases.md`
3. `ablation.md`

## 8. 评分标准

| 维度 | 占比 | 要求 |
|:---|:---:|:---|
| 基础完成度 | 25% | 跑通 source-only 和 adaptation 版本 |
| 结果质量 | 30% | target 域结果优于 source-only |
| 分析深度 | 30% | 能分析 gap 来源和 hardest target cases |
| 复现规范 | 15% | 数据口径、预处理、配置清晰 |

## 9. 分阶段完成要求

### 第一阶段：先跑通

- 跑 source-only baseline
- 量化 target 掉分
- 保存首个 target 结果

### 第二阶段：再改进

- 加 feature alignment 或 DANN
- 尝试伪标签
- 观察 target 改善

### 第三阶段：最后解释

- 分析 hardest target cases
- 看 adaptation 前后差异
- 解释失败原因

## 10. 建议实施步骤

1. 先不要急着做 adaptation，先把 source-only 跑清楚。
2. 明确 source 和 target 的差异。
3. 跑一个最基础 adaptation 方法。
4. 如果有效，再尝试伪标签或一致性。
5. 选 target 失败样本做分析。

## 11. 常见坑

- 预处理在两域上不一致。
- 没先做 source-only baseline。
- 伪标签质量太差却直接强化训练。
- 只看平均分，不看 hardest target cases。
- 误把数据泄漏当 adaptation 提升。

## 12. 建议实验表

| 实验编号 | 模型 / 配置 | 对齐策略 | 验证指标 | 是否提交 | 备注 |
|:---:|:---|:---|:---|:---:|:---|
| E1 | Source-only baseline | 无 | 待填写 | 否 | 量化 domain gap |
| E2 | DANN / feature alignment | 基础对齐 | 待填写 | 否 | 看 adaptation 是否有效 |
| E3 | Pseudo label / consistency | 半监督增强 | 待填写 | 否 | 比较 target 域增益 |
| E4 | Best model | 最优组合 | 待填写 | 是 | 最终提交版本 |

## 13. 复盘模板

### 本次最终采用

- 模型：
- 对齐策略：
- 最终验证指标：
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

- domain gap 主要来自风格 / 噪声 / 标签边界：
- 最有帮助的 adaptation 技巧：
- 下次最值得优先尝试的方向：

## 14. 老师批改时最看重什么

1. 你有没有量化 domain gap。
2. 你有没有比较 adaptation 前后差异。
3. 你能不能分析 target 失败样本。
4. 你的提升是不是干净可信。

## 15. 关联知识点

- [[多层神经网络]]
- [[模型评估指标]]
- [[类别不平衡问题]]
## 16. 真实作业包

- README：
  - [[03-Projects/projects-ml/hw11_domain_adaptation/README.md|hw11_domain_adaptation/README.md]]
- Starter：
  - `F:\\-\\03-Projects\\projects-ml\\hw11_domain_adaptation\\starter\\`
- Data Card：
  - [[03-Projects/projects-ml/hw11_domain_adaptation/data_card.md|data_card.md]]
- Baseline Tracker：
  - [[03-Projects/projects-ml/hw11_domain_adaptation/baseline/README.md|baseline/README.md]]
- Report Template：
  - [[03-Projects/projects-ml/hw11_domain_adaptation/reports/report_template.md|report_template.md]]
- Rubric：
  - [[03-Projects/projects-ml/hw11_domain_adaptation/rubric.md|rubric.md]]

### 当前包定位

- 这是给学生自己完成作业用的 starter 包。
- 当前只提供目录、接口、报告模板和结果记录位。
- 不预置教师答案或可直接提交的 baseline 实现。
