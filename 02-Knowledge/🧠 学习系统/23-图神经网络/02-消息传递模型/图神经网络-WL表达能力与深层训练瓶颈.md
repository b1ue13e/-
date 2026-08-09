---
type: study
topic: "WL表达能力与深层训练瓶颈"
course: "图神经网络"
created: 2026-08-08
status: planned
stage_moc: "[[🧭 阶段2-消息传递模型]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: [Weisfeiler-Lehman, over-smoothing, over-squashing]
upstream: ["[[图神经网络-消息传递统一框架]]", "[[图神经网络-GCN归一化传播与谱近似]]", "[[图神经网络-图级读出与任务头]]"]
related: [GIN, residual, Jumping Knowledge, graph rewiring]
source: "Hamilton, Graph Representation Learning, Ch.7; Stanford CS224W Homework 1"
source_url: "https://web.stanford.edu/class/cs224w/homework/CS224W_Aut2526_HW1.pdf"
accessed: 2026-08-08
license: "官方课程题目 link-only；本卡为本地原创解释"
tags: [学习, 图神经网络, 表达能力, 训练瓶颈]
---

# 图神经网络-WL表达能力与深层训练瓶颈

## 1. 两个不同问题

**表达能力**问：给定足够训练，模型能否区分两个结构不同的图；**训练瓶颈**问：层数加深后，梯度和信息是否还能有效到达目标。一个模型理论上可表达，不代表有限数据和深度下可训练。

## 2. 1-WL 直觉

1-WL（颜色细化）反复把节点自己的颜色与邻居颜色多重集哈希成新颜色。标准消息传递若使用共享参数和排列不变聚合，通常不超过 1-WL 的区分能力：如果 1-WL 无法区分两个图，某些 MPNN 也无法区分它们。这个结论是上界，不是说所有 GNN 都与 WL 完全等价。

GIN 使用近似 injective 的 sum 聚合和 MLP，旨在接近 1-WL；mean/max 可能丢失多重集计数。表达能力分析必须说明初始特征、聚合是否 injective、readout 和图类别。

## 3. Over-smoothing

重复乘以归一化传播算子会让连通区域节点表示趋同，节点间方差下降，分类边界消失。它是“表示变得太相似”的深度问题，不等同于欠拟合。

## 4. Over-squashing

远处指数增长的节点信息被压进固定宽度向量，导致长程依赖的梯度/信号被压缩。它是“信息通道太窄”，即使节点表示还没有完全相同也可能发生。增加层数可能同时加重邻域爆炸和过压缩。

## 5. 最小诊断代码

```python
import torch

H = torch.tensor([[1., 0.], [0.9, 0.1], [0.8, 0.2]])
variance_before = H.var(dim=0).mean()
S = torch.tensor([[0.5, 0.5, 0.0], [1/3, 1/3, 1/3], [0.0, 0.5, 0.5]])
H_next = S @ H
variance_after = H_next.var(dim=0).mean()
assert variance_after <= variance_before + 1e-6
print(float(variance_before), float(variance_after))
```

这只是平滑趋势检查，不是通用定理。真实实验还要看验证性能、梯度范数、不同深度和残差/跳层对照。

## 6. 解决策略与代价

- 残差/跳层：保留浅层信息，增加参数和调参负担；
- Jumping Knowledge：融合不同深度，需决定 concat/max/attention；
- 归一化、正则化、dropout：可能改善优化，但不自动恢复被压缩的远程信息；
- 采样/重连/位置编码：扩大有效感受野，可能改变任务协议或引入额外结构假设。

## 7. 常见错误

1. 把 over-smoothing 和 over-squashing 当同义词。
2. 用一张 attention 热图证明模型解决了长程依赖。
3. 看到深层模型分数下降就声称理论表达能力不足，而没有训练曲线和梯度证据。
4. 直接复制 WL 结论到有向、异质或带边特征图，忽略初始颜色和消息函数变化。

## 8. 检索练习与通过标准

- 构造两个 1-WL 难以区分的正则图，并说明初始特征改变后结论是否仍然成立。
- 设计实验分别测表示方差下降和长程节点标签的性能下降。
- 比较 2/4/8 层 GCN 与残差版本，报告参数、训练稳定性、验证指标和失败案例。

通过标准：能区分表达能力、过平滑、过压缩；能写出至少一个可测指标和一个不充分的“伪证据”；完成阶段 2 消融作业后再进入训练实验。

## 9. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

下一阶段：[[🧭 阶段3-训练与实验]]。

