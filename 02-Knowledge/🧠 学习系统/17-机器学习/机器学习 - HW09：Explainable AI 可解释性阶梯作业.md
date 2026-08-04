---
title: "机器学习 - HW09：Explainable AI 可解释性阶梯作业"
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
concept: ["可解释性", "Saliency", "Feature Attribution"]
prerequisites: ["[[多层神经网络]]", "[[模型评估指标]]", "[[过拟合专题]]"]
tags: [学习, 17-机器学习, 作业, Explainable-AI]
aliases: ["ML-HW09-Explainable-AI"]
---

# 机器学习 - HW09：Explainable AI 可解释性阶梯作业

> 这份作业的重点不是再把分类分数提高一点，而是开始认真回答一个更难的问题：模型到底在看什么，它给出这个判断到底有没有道理。

## 1. 布置时机

- 建议在学完以下内容后布置：
  - 至少一个成熟分类模型
  - 梯度和反向传播
  - 视觉模型基础
  - 误差分析基本方法
- 不建议在学生还没有成熟模型时布置。

## 2. 前置知识

开始前，学生应该已经会：

1. 训练并保存一个分类模型。
2. 理解梯度和中间特征。
3. 知道 heatmap 不是“真相”，只是解释候选。
4. 会挑样本做人工分析。

## 3. 任务背景

你需要对已训练模型进行解释，分析模型关注的区域或特征是否合理。

这份作业训练的是：

- saliency / attribution
- 多种解释方法对照
- 模型偏见与伪特征判断
- 用解释结果反向改模型

## 4. 教学目标

完成后，应该能做到：

1. 跑通一种解释方法。
2. 比较两种以上解释方法。
3. 指出哪些解释结果不可靠。
4. 通过解释结果发现模型偏差。

## 5. 老师提供的材料

### 必须提供

- 已训练模型
- 验证样本
- 标签说明
- 解释输出要求

### 最好额外提供

- `starter code`
- saliency / grad-cam 示例
- 典型成功 / 失败案例

### 建议目录

- 数据：
  - `03-Projects/data/ml_hw09/`
- 代码：
  - `03-Projects/projects-ml/hw09_explainable_ai/run_explain.py`
  - `03-Projects/projects-ml/hw09_explainable_ai/model.py`
  - `03-Projects/projects-ml/hw09_explainable_ai/utils.py`
  - `03-Projects/projects-ml/hw09_explainable_ai/report.md`

## 6. 数据说明

### 数据类型

- 输入：验证样本
- 输出：解释可视化
- 任务类型：模型分析任务

### 你至少要先弄清楚

1. 要解释的是哪个模型。
2. 解释样本怎么选。
3. 解释图是否和原图同尺度。
4. 不同解释方法的输出是否可直接比较。
5. 失败样本是否要单独记录。

## 7. 提交物

### 必交

1. `run_explain.py`
2. `report.md`
3. `visualizations.zip`

### 建议提交

1. `comparison.md`
2. `bad_cases.md`
3. `bias_notes.md`

## 8. 评分标准

| 维度 | 占比 | 要求 |
|:---|:---:|:---|
| 基础完成度 | 20% | 跑通至少一种解释方法 |
| 结果质量 | 25% | 解释图清晰且可复查 |
| 分析深度 | 40% | 多方法对照、失败解释和偏见分析 |
| 复现规范 | 15% | 模型、样本、可视化流程清楚 |

## 9. 分阶段完成要求

### 第一阶段：先跑通

- 跑通一种解释方法
- 输出第一批解释图
- 检查 pipeline 是否正确

### 第二阶段：再改进

- 增加第二种方法
- 对比不同方法结果
- 做稳定性测试

### 第三阶段：最后解释

- 选成功与失败样本
- 分析背景偏见或伪特征
- 提出改进建议

## 10. 建议实施步骤

1. 先锁定一个成熟模型。
2. 选一小批样本先跑可视化。
3. 再加第二种解释方法。
4. 挑典型样本做对照。
5. 记录看起来合理但其实可能不可靠的解释。

## 11. 常见坑

- 模型没有切到 `eval()`。
- 预处理和训练时不一致。
- 直接肉眼比较不同方法的热力图强度。
- 只挑好看样例，不记失败样例。
- 把“可视化漂亮”误当成“解释可靠”。

## 12. 建议实验表

| 实验编号 | 方法 / 配置 | 样本范围 | 主要观察 | 是否提交 | 备注 |
|:---:|:---|:---|:---|:---:|:---|
| E1 | Saliency baseline | 少量验证样本 | 待填写 | 否 | 首个解释基线 |
| E2 | Grad-CAM / IG | 同一批样本对照 | 待填写 | 否 | 比较解释差异 |
| E3 | 稳定性测试 | 加噪或重参数化 | 待填写 | 否 | 看解释是否稳 |
| E4 | Final analysis | 最终样本集合 | 待填写 | 是 | 最终提交版本 |

## 13. 复盘模板

### 本次最终采用

- 主要解释方法：
- 对照方法：
- 样本范围：
- 是否提交：

### 本次最有效的发现

1.
2.
3.

### 主要失败解释

1.
2.

### 当前判断

- 模型更像在看主体 / 背景 / 局部纹理：
- 哪种解释方法最稳定：
- 下次最值得优先尝试的方向：

## 14. 老师批改时最看重什么

1. 你有没有对比不同解释方法。
2. 你有没有记录失败解释。
3. 你能不能指出模型是不是学歪了。
4. 你的分析是否有证据，不是主观想象。

## 15. 关联知识点

- [[模型评估指标]]
- [[过拟合专题]]
- [[多层神经网络]]
## 16. 真实作业包

- README：
  - [[03-Projects/projects-ml/hw09_explainable_ai/README.md|hw09_explainable_ai/README.md]]
- Starter：
  - `F:\\-\\03-Projects\\projects-ml\\hw09_explainable_ai\\starter\\`
- Data Card：
  - [[03-Projects/projects-ml/hw09_explainable_ai/data_card.md|data_card.md]]
- Baseline Tracker：
  - [[03-Projects/projects-ml/hw09_explainable_ai/baseline/README.md|baseline/README.md]]
- Report Template：
  - [[03-Projects/projects-ml/hw09_explainable_ai/reports/report_template.md|report_template.md]]
- Rubric：
  - [[03-Projects/projects-ml/hw09_explainable_ai/rubric.md|rubric.md]]

### 当前包定位

- 这是给学生自己完成作业用的 starter 包。
- 当前只提供目录、接口、报告模板和结果记录位。
- 不预置教师答案或可直接提交的 baseline 实现。
