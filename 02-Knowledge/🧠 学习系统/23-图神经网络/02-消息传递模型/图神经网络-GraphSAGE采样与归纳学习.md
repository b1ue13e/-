---
type: study
topic: "GraphSAGE采样与归纳学习"
course: "图神经网络"
created: 2026-08-08
status: planned
stage_moc: "[[🧭 阶段2-消息传递模型]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: [GraphSAGE, 邻域采样, 归纳学习]
upstream: ["[[图神经网络-消息传递统一框架]]", "[[图神经网络-图学习评估与无泄漏划分]]"]
related: [GCN, 邻域爆炸, mini-batch]
source: "Hamilton, Ying & Leskovec, Inductive Representation Learning on Large Graphs"
source_url: "https://arxiv.org/abs/1706.02216"
accessed: 2026-08-08
license: "论文链接；本卡为本地原创解释"
tags: [学习, 图神经网络, GraphSAGE]
---

# 图神经网络-GraphSAGE采样与归纳学习

## 1. 问题动机

固定节点 embedding lookup 对训练时未出现的新节点没有参数。GraphSAGE 学的是共享的聚合/更新函数，并在训练时只采样有限邻居，因而可以在有特征和邻接信息的新节点上计算表示。

## 2. 典型更新

对第 `k` 层：

$$h_{N(v)}^{(k)}=AGGREGATE_k\left(\{h_u^{(k-1)}:u∈N(v)\}\right)$$

$$h_v^{(k)}=σ\left(W_k\cdot CONCAT\left(h_v^{(k-1)},h_{N(v)}^{(k)}\right)\right)$$

完成后可选 `L2` 归一化。`AGGREGATE` 可以是 mean、pooling 或 LSTM，但必须保证邻居顺序不承担未声明语义；LSTM 版本需要额外的随机排列策略。

## 3. 采样与邻域爆炸

若每层采样 `s_k` 个邻居、目标 batch 有 `b` 个节点，最坏计算节点数近似为：

$$b\left(1+s_1+s_1s_2+…+\prod_{k=1}^{K}s_k\right)$$

增加深度不只是增加参数，也会指数扩大需要加载的计算子图。采样预算是工程协议的一部分，必须写入实验 manifest。

## 4. 归纳与 transductive 的边界

GraphSAGE 的函数可对新节点运行，不代表任何“新图”都能零成本泛化：新节点仍需可用特征、邻居和相同的预处理口径。若训练阶段使用了测试节点特征/边，仍需按任务定义声明 transductive；“模型结构支持 inductive”不等于实验协议已经 inductive。

## 5. 最小可运行采样聚合

```python
import torch

neighbors = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
features = torch.eye(4)
target = 2
sampled = neighbors[target][:1]
neighbor_mean = features[sampled].mean(dim=0)
input_vector = torch.cat([features[target], neighbor_mean])
layer = torch.nn.Linear(8, 3)
output = torch.relu(layer(input_vector))
assert output.shape == (3,)
print(sampled, output.shape)
```

这段代码只展示一个节点的一层采样；完整 mini-batch 需要去重节点、记录 parent-child 索引，并保证训练/验证/测试采样边界一致。

## 6. 与 GCN 的关键区别

| 维度 | GCN | GraphSAGE |
|:---|:---|:---|
| 聚合权重 | 全邻居的度归一化 | 可采样、可学习的聚合函数 |
| 归纳性 | 常见全图设置偏 transductive | 函数共享，天然支持新节点场景 |
| 计算 | 全图传播或稀疏乘法 | 受采样 fanout 控制的子图计算 |
| 风险 | 高度节点成本、过平滑 | 采样偏差、邻域重复和内存爆炸 |

## 7. 常见错误

1. 采样邻居后仍把采样均值当作全邻居均值，没有记录 fanout 和随机种子。
2. 训练和测试使用不同的特征标准化，导致“归纳能力”被预处理差异混淆。
3. 把每个节点的 embedding 直接存下来再分类，实际退化成 transductive lookup。
4. 只报告吞吐量，不报告采样后的性能、方差和未见节点协议。

## 8. 检索练习与通过标准

- 对 `K=2, fanout=[2,3]` 和 batch=4 估算最坏节点读取数。
- 写出新节点没有训练 ID 参数时，GraphSAGE 仍需要哪些输入。
- 设计一个采样偏差检查：全邻居 mean 与固定 seed 采样 mean 的误差如何报告。

通过标准：能写出更新公式；能解释 inductive 的必要条件；能计算 fanout 预算；代码形状和采样逻辑通过测试。

## 9. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

下一张：[[图神经网络-GAT图注意力与边特征]]。

