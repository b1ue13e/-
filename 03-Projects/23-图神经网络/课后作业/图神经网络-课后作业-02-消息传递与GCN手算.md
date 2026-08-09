---
type: project
project_type: homework
course: "图神经网络"
assignment_id: "GNN-L02"
assignment_level: lesson
assignment_format: problem-set
stage_id: "02"
requires: ["[[图神经网络-消息传递统一框架]]", "[[图神经网络-GCN归一化传播与谱近似]]", "[[图神经网络-图学习评估与无泄漏划分]]"]
source_type: local_integration_task
source: "本地原创任务；参考 CS224W Homework 1"
source_url: "https://web.stanford.edu/class/cs224w/homework/CS224W_Aut2526_HW1.pdf"
license: "本地原创；上游题目 link-only"
created: 2026-08-08
status: planned
flow: project
tags: [作业, 图神经网络, GCN]
---

# 图神经网络-课后作业-02-消息传递与GCN手算

## 学习目标与任务边界

本作业验证 message/aggregate/update、邻居排列不变性、GCN 归一化和训练/评估职责。只做小图手算与最小前向，不要求 PyG 或 GPU。

## 任务

### L02-1 统一框架

对一个带边特征的小图写出 `M,U,⊕,R` 的一组定义，说明 `⊕` 为什么必须对邻居排列不变。给出一个依赖输入顺序的错误 aggregator。

### L02-2 GCN 归一化

对路径 `0—1—2` 加自环，写出 `\tilde A`、`\tilde D` 和 `S`；计算一列 one-hot 特征传播后的结果，解释中心节点和边界节点的权重。

### L02-3 前向与训练边界

实现一层 GCN 前向，加入线性任务头和交叉熵；只在 `train_mask` 上反向传播。提交初始/最终 train loss 和验证指标，不计算调参用 test 指标。

### L02-4 泄漏审计

给出一个链路预测中测试边仍在邻接矩阵的反例；说明它在什么 transductive 定义下可能合理、在什么 inductive 定义下必然泄漏。

## 检查里程碑

1. `oracle.md` 先保存手算的 `\tilde A/\tilde D/S`，再允许写实现；代码输出与手算逐元素比较，容差不超过 `1e-6`。
2. `test_shapes.py` 检查节点维、输入维、隐藏维和类别维；错误信息要指出预期与实际形状。
3. `train.py` 日志至少包含 epoch、train loss、val accuracy；只保留最后一次 test 评价，不能每轮读取 test。
4. `leakage.md` 画出训练消息传递图和被隐藏测试边；分别写 transductive/inductive 下的合法性判断。

允许使用课程 starter 验证接口，但提交代码必须能解释每次矩阵乘法，并在新输出目录产生独立日志。若最终 loss 没下降，保留日志并从梯度、mask、学习率、归一化顺序依次诊断。

## 环境与运行

```powershell
python -m pytest -q
python your_solution.py --model gcn --epochs 60 --seed 7 --output artifacts/l02
```

## 提交产物

- `submission/l02/gcn.py` 与形状/归一化测试；
- 手算 PDF/Markdown；
- `artifacts/l02/metrics.json`、训练日志和 split manifest；
- 泄漏审计说明与一个失败案例。

## Rubric（100 分）

- MPNN 形式与不变性 25 分；
- GCN 归一化手算 30 分；
- 可学习训练闭环 25 分；
- split/泄漏与报告边界 20 分。

通过线：75 分；只有前向没有参数更新、或测试标签进入 loss 为硬失败。

## 引导与自检

- 先写 `S` 再写代码；
- 检查 `S == S.T` 和输出形状；
- 在日志中区分 train loss、val metric 和一次性 test metric；
- [ ] 自环后的度矩阵重新计算；
- [ ] 没有把“代码能运行”写成“模型已泛化”。

## 常见失败模式

- `train_mask` 只用于算 accuracy，却用全节点标签计算 loss；
- `S @ X @ W` 和 `X @ W @ S` 形状偶然可乘但语义错误；
- 加自环后仍使用原度矩阵；
- 为了让 test 更高而重复改变 split；
- 把一次 toy 运行的高分写成 GCN 一定优于 MLP。

## 后续入口

进入 [[🧭 阶段2-消息传递模型]]，阶段综合作业为 [[图神经网络-阶段作业-02-GCNGraphSAGEGAT对照实验]]。
