---
type: reference
project_type: homework
course: "机器学习"
assignment_level: lesson
assignment_format: problem-set
topic: "GAN 生成对抗网络"
status: ongoing
created: 2026-08-06
updated: 2026-08-06
adapted_from: "李宏毅《Machine Learning》2021 Spring"
source_url: "https://speech.ee.ntu.edu.tw/~hylee/ml/2021-spring.php"
requires: ["[[机器学习-无监督学习]]", "[[机器学习-神经网络]]"]
license: "本地学习用途；外部教材仅 link-only，不复制教材答案"
source_license_status: "待验证"
tags: [作业, 机器学习, GAN 生成对抗网络]
flow: project
source_type: open_textbook_exercise
assignment_id: "机器学习-DL-04"
stage_id: "专题"
---


# 机器学习 · 深度学习专题（可选参考）：GAN 生成对抗网络

> 这份作业会让你第一次真正接触“模型不是在分类，而是在生成”。它的难点不是代码量，而是训练稳定性和你是否会判断模型到底学到了什么。

## 1. 布置时机

- 建议在学完以下内容后布置：
  - 深度生成模型基本概念
  - 对抗训练
  - 图像任务训练技巧
  - 训练不稳定现象
- 最好在完成 CNN 和基础训练调参之后布置。

## 2. 前置知识

开始前，学生应该已经会：

1. 训练一个基本图像模型。
2. 看懂训练曲线和样本网格图。
3. 理解生成器和判别器的角色。
4. 知道训练不稳定不是“代码错”这一种原因。

## 3. 任务背景

你需要用随机噪声生成目标风格的图像。  
官方常见题型可以类比为：`人脸图像生成`。

这份作业训练的是：

- 生成模型基本闭环
- 对抗训练稳定性
- 样本质量判断
- mode collapse 识别

## 4. 学习目标

完成后，应该能做到：

1. 跑通一个最小 GAN。
2. 通过样本而不是单一 loss 判断训练状态。
3. 识别 mode collapse、判别器过强和训练失衡。
4. 解释为什么某个稳定训练技巧有效。

## 5. 环境（材料与数据）
> ⚠️ **数据 / Starter 占位说明**：本仓库**未内置**任何数据集或 starter 代码。下方 `03-Projects/...` 路径是按李宏毅 ML2021 课程结构预留的**本地布局占位**，并非已就绪资源。实际数据、starter 与预训练权重请从课程主页（`source_url`）获取，并放入 `03-Projects/17-机器学习/data/<本作业>/` 与 `.../代码/<本作业>/`。未自行配置数据集与运行环境前，本作业骨架**不可直接运行**。


### 必须提供

- 训练图像集
- 图像尺寸说明
- `sample_submission` 或官方输出要求
- baseline 说明

### 最好额外提供

- `starter code`
- 训练样本网格图示例
- FID 或参考指标说明
- 常见 collapse 示例

### 建议目录

- 数据：
  - `03-Projects/data/ml_hw06/`
- 代码：
  - `03-Projects/projects-ml/hw06_gan/train.py`
  - `03-Projects/projects-ml/hw06_gan/dataset.py`
  - `03-Projects/projects-ml/hw06_gan/model.py`
  - `03-Projects/projects-ml/hw06_gan/infer.py`
  - `03-Projects/projects-ml/hw06_gan/report.md`

## 6. 数据说明

### 数据类型

- 输入：随机噪声 + 训练图像
- 输出：生成图像
- 任务类型：生成任务

### 你至少要先弄清楚

1. 图像分辨率是多少。
2. 输出图像归一化范围是什么。
3. 训练集规模是否足够。
4. 官方更看重视觉质量还是数值指标。
5. 如何保存不同 epoch 的样本进行比较。

## 7. 提交产物

### 必交

1. 官方要求的生成结果包
2. `train.py`
3. `infer.py`
4. `report.md`

### 建议提交

1. `sample_grid.png`
2. `training_log.csv`
3. `collapse_cases.md`

## 8. 验收标准与 Rubric
> **最低通过门槛**：满足 Rubric「基础完成度」全部要求且结果可复现（附环境 / 命令 / 随机种子），即视为通过；总分 ≥ 80/100 为良好。


| 维度 | 占比 | 要求 |
|:---|:---:|:---|
| 基础完成度 | 25% | 能稳定训练并生成样本 |
| 结果质量 | 35% | 样本质量明显优于最小 baseline |
| 分析深度 | 25% | 能分析 collapse 和稳定性问题 |
| 复现规范 | 15% | 配置、采样方式、checkpoint 清楚 |

## 9. 分阶段完成要求

### 第一阶段：先跑通

- 跑通最小 DCGAN
- 保存样本网格图
- 确认生成图像不是纯噪声

### 第二阶段：再改进

- 尝试稳定训练技巧
- 对比不同学习率和判别器步数
- 比较生成质量

### 第三阶段：最后解释

- 判断 collapse 与否
- 保存代表性 epoch 样本
- 总结最有效的稳定训练技巧

## 10. 建议实施步骤

1. 先跑通最小对抗训练。
2. 固定随机种子和采样噪声。
3. 每隔固定 epoch 保存样本。
4. 一次只改一项稳定训练技巧。
5. 选定最佳 checkpoint 再生成最终结果。

## 11. 引导与自检

- 图像归一化和输出激活不匹配。
- 判别器过强导致生成器学不动。
- 只看 loss，不看样本。
- collapse 出现后没有及时停下来分析。
- 没固定采样噪声，前后样本不可比。

## 12. 建议实验表

| 实验编号 | 模型 / 配置 | 稳定训练技巧 | 验证观察 | 是否提交 | 备注 |
|:---:|:---|:---|:---|:---:|:---|
| E1 | DCGAN baseline | 无 | 待填写 | 否 | 首个可运行生成基线 |
| E2 | DCGAN + SN / label smoothing | 轻量稳定技巧 | 待填写 | 否 | 看训练是否更稳 |
| E3 | WGAN-GP / EMA | 高级稳定技巧 | 待填写 | 否 | 比较生成质量 |
| E4 | Best model | 最优组合 | 待填写 | 是 | 最终提交版本 |

## 13. 复盘模板

### 本次最终采用

- 模型：
- 关键超参数：
- 最终观察结果：
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

- 更像 mode collapse / 判别器过强 / 生成器过强：
- 最有帮助的稳定训练技巧：
- 下次最值得优先尝试的方向：

## 14. 老师批改时最看重什么

1. 你会不会用样本判断训练状态。
2. 你有没有记录训练过程，而不是只给最后结果。
3. 你能不能解释为什么某个技巧有帮助。
4. 你的结果是否能重现。

## 15. 关联知识点

- [[机器学习-梯度下降]]
- [[机器学习-模型评估指标]]
- [[机器学习-过拟合与欠拟合|过拟合]]
## 16. 真实作业包

- README：
  - `hw06_gan/README.md`
- Starter：
  - `F:\\-\\03-Projects\\projects-ml\\hw06_gan\\starter\\`
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
