---
type: study
topic: "GAT图注意力与边特征"
course: "图神经网络"
created: 2026-08-08
status: planned
stage_moc: "[[🧭 阶段2-消息传递模型]]"
flow: knowledge
kind: derivation
difficulty: intermediate
concept: [GAT, 注意力, 多头注意力, 边特征]
upstream: ["[[图神经网络-消息传递统一框架]]", "[[图神经网络-GCN归一化传播与谱近似]]"]
related: [GraphSAGE, 图Transformer, 可解释性]
source: "Veličković et al., Graph Attention Networks"
source_url: "https://arxiv.org/abs/1710.10903"
accessed: 2026-08-08
license: "论文链接；本卡为本地原创解释"
tags: [学习, 图神经网络, GAT]
---

# 图神经网络-GAT图注意力与边特征

## 1. 问题动机

GCN 的邻居权重主要由度归一化决定，无法区分同一节点的不同邻居。GAT 让模型根据节点表示学习邻居权重，同时仍只在局部邻域上传播，避免把注意力误解成任意节点之间的全连接 Transformer。

## 2. 单头公式

先做线性投影 `z_v=W h_v`，对边 `(u,v)`：

$$e_{uv}=a^T[Wh_u\Vert Wh_v],\qquad α_{uv}=softmax_{u∈N(v)}(LeakyReLU(e_{uv}))$$

更新为：

$$h'_v=σ\left(\sum_{u∈N(v)}α_{uv}Wh_u\right)$$

邻域 softmax 的分母只在 `N(v)` 内，若加入自环则 `v` 自身也参与归一化。注意力系数是条件于当前特征和参数的权重，不是因果解释或稳定特征重要性。

## 3. 多头与边特征

多头注意力使用 `H` 组独立参数：中间层通常 concat，输出层常 mean；选择会改变隐藏维度。边特征可作为额外项 `b(e_{uv})` 加到 logits：

$$e_{uv}=a^T[Wh_u\Vert Wh_v]+b(e_{uv})$$

如果边类型/方向有不同语义，更稳妥的做法是显式区分 relation，而不是把离散类型直接当连续标量。

## 4. 最小数值检查

```python
import torch

scores = torch.tensor([1.0, 2.0, 0.0])
alpha = torch.softmax(scores, dim=0)
assert torch.isclose(alpha.sum(), torch.tensor(1.0))
values = torch.tensor([[1.0, 0.0], [0.0, 2.0], [1.0, 1.0]])
message = (alpha[:, None] * values).sum(dim=0)
assert message.shape == (2,)
print(alpha.tolist(), message.tolist())
```

这段只验证局部归一化和加权聚合；完整 GAT 还需为每个目标节点分别计算邻域分母，并在训练中优化 `W,a`。

## 5. 复杂度与边界

稀疏 GAT 的注意力分数通常按边计算，复杂度随 `|E|` 和隐藏维度增长；如果允许所有节点互相注意，复杂度转为 `O(n^2)`，那已经是另一种图 Transformer 设计。稀疏注意力不自动解决过压缩、过平滑或长程依赖。

## 6. 概念边界

- 注意力系数大不等于该邻居“因果重要”；它受参数、特征缩放和邻域归一化影响。
- GAT 与 GraphSAGE 都可归纳，但 GAT 的局部权重是数据驱动，GraphSAGE 的聚合函数可不含显式 attention。
- 边权和 attention weight 不同：前者是输入数据/领域定义，后者是模型中间状态；可以结合但不能互换。

## 7. 检索练习与通过标准

1. 对三个邻居给出 logits，手算 softmax 后的消息。
2. 说明多头 concat 后隐藏维度如何变化；输出层 mean 为什么常见。
3. 给出一个边特征让 attention 偏置合理、一个会造成误导的例子。

通过标准：能写出局部 softmax 分母；能检查多头形状；能解释稀疏/稠密复杂度；不把 attention 热图当作充分解释证据。

## 8. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

下一张：[[图神经网络-图级读出与任务头]]。

