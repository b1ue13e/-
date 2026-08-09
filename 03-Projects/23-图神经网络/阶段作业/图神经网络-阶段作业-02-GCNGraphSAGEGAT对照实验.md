---
type: project
project_type: homework
course: "图神经网络"
assignment_id: "GNN-S02"
assignment_level: stage
assignment_format: lab
stage_id: "02"
requires: ["[[图神经网络-消息传递统一框架]]", "[[图神经网络-GCN归一化传播与谱近似]]", "[[图神经网络-GraphSAGE采样与归纳学习]]", "[[图神经网络-GAT图注意力与边特征]]", "[[图神经网络-图级读出与任务头]]", "[[图神经网络-WL表达能力与深层训练瓶颈]]", "[[图神经网络-图学习评估与无泄漏划分]]"]
source_type: local_integration_task
source: "本地原创阶段任务；CS224W Homework 1 仅作题型参照"
source_url: "https://web.stanford.edu/class/cs224w/homework/CS224W_Aut2526_HW1.pdf"
license: "本地原创；上游 link-only"
created: 2026-08-08
status: planned
starter_entrypoint: "python starter/run_assignment.py s02"
starter_status: verified_worked_example
flow: project
tags: [作业, 图神经网络, 阶段作业]
---

# 图神经网络-阶段作业-02-GCNGraphSAGEGAT对照实验

## 学习目标

在冻结的 toy 图节点分类协议上，公平比较 MLP、GCN、GraphSAGE、GAT，并用深度/邻接/注意力消融解释差异。Starter smoke 是协议样例，不是提交答案。

## 任务边界

本阶段只评价节点分类的离线 transductive 协议；不要把 toy 图结果外推成 inductive、OGB 或线上结论。所有模型必须共享特征、split、训练轮次、早停和 seed 集合；任何不同预算必须在配置和报告中显式说明。

## 任务与边界

1. 先运行 `python -m pytest -q` 和 starter baseline，检查 manifest、形状和训练更新。
2. 在 `submission/s02/` 独立实现或重构三模型；为归一化、邻居 mean、local softmax 写 oracle 测试。
3. 用 seeds `[7,42,2026]`，相同 split、隐藏维度预算、optimizer 和 epochs 比较四模型。
4. 至少做两项消融：去邻接/换深度/去自环/固定 attention/改变 fanout。
5. 报告参数量、train loss、val/test 指标、运行时间、表示方差和失败节点。

## 环境与提交

```powershell
python submission/s02/run.py --config submission/s02/config.json --output artifacts/s02
python -m pytest -q submission/s02/tests
```

先运行课程 worked example，确认四模型共享 split、seed 和输出字段后再创建自己的 `submission/s02/`：

```powershell
python starter/run_assignment.py s02 --output artifacts/s02-worked-example --epochs 40 --seeds 7 42 2026
```

该例子会写入 4 模型 × 3 seed 的 `runs.csv`、`summary.json` 与 `split_manifest.json`；GraphSAGE fanout 另有 capstone reference 的 batch 子图证据，不能把整图删边当作小批采样。

提交代码、配置、测试、`runs.csv`、`summary.json`、消融表、错误样本和复现 README。不得把 starter 的 `artifacts/starter-smoke` 当作自己的运行证据。

## 提交产物

`submission/s02/` 包含四个模型的实现或清晰改动、统一训练入口、形状/归一化/attention 测试、配置文件和数据协议；`artifacts/s02/` 包含所有 12 个模型×seed 运行、主表、消融表、表示方差、峰值节点/边数与失败样本。报告逐项回答“改变了什么、控制了什么、观察到什么、结论不能外推到哪里”。

## 常见失败

- GAT 的 attention 在全图而不是目标节点邻域内 softmax；
- GraphSAGE 采样了邻居却没有记录 fanout 和 seed；
- 只跑一个 seed，然后把偶然提升写成架构优势；
- 把测试指标用于早停或超参数选择。

## Rubric（100 分）

- 数据与泄漏 20；模型/形状正确 25；公平基线 20；消融与瓶颈诊断 20；复现与报告 15。
- 通过线 80；只有前向、测试标签参与训练、不同 split 或删除失败运行均为硬失败。

## 引导与自检

- GNN 异常高分先检查特征与 split；
- GAT 对每个目标节点单独做邻域 softmax；
- [ ] `S` 对称且加自环后重算度；
- [ ] permutation equivariance 测试通过；
- [ ] 复杂模型没有赢时如实保留。

## 阶段出口

通过后进入 [[🧭 阶段3-训练与实验]]。
