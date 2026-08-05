---
title: "PyG Data"
date: 2026-07-31
type: concept
kind: concept
flow: knowledge
course: "01-社交网络挖掘"
importance: "A"
tags: [学习, 核心概念, 图表示学习与GNN]
upstream: ["[[02-Knowledge/🧠 学习系统/01-社交网络挖掘/01-图与网络基础/图论基础]]]", "[[[PyTorch张量基础]]]"]
downstream: ["[[PyG Dataset.md]]]", "[[[Message Passing机制]]]"]
status: learning
---

> [!NOTE] 核心直觉：标准化图数据的“快递盒”
> **类比**：就像是一个标准化的快递盒（Box），里面分门别类装好了节点属性（说明书）、边索引（连线图）、边属性（特殊标签）和整图属性（发货单）。所有千奇百怪的图结构，在进入神经网络之前，都被强行折叠并打包成了这几个标准抽屉里的张量。

## 1. 为什么需要这个知识点？
- **背景**：在深度学习（如PyTorch）中，所有输入数据都需要表示为张量（Tensor）。但图数据高度不规则，节点度数不同，没有像图像那样的固定网格或矩阵形状。
- **痛点**：手动将图结构（节点、边）转换为适合GPU加速训练的稀疏表示非常繁琐，且极其容易在批处理（Batching）时打乱原本的连接关系。
- **意义**：PyTorch Geometric (PyG) 提供了 `torch_geometric.data.Data` 类，作为表示同构图（Homogeneous Graph）的绝对基础数据结构。它标准化了图的张量表示，利用COO格式极大地节省了内存，并无缝集成了后续所有的GNN层和高效的批处理机制。

## 2. 核心定义与公式/代码
`Data` 对象是一个扁平的数据容器，可以通过键值对的方式访问各种属性。

```python
import torch
from torch_geometric.data import Data

# 1. 节点特征矩阵 x: [num_nodes, num_node_features]
# 假设有3个节点，每个节点有1维特征
x = torch.tensor([[-1], [0], [1]], dtype=torch.float)

# 2. 边索引 edge_index: [2, num_edges] (COO格式，必须是长整型)
# 表示有向边: 0->1, 1->2
edge_index = torch.tensor([[0, 1],
                           [1, 2]], dtype=torch.long)

# 3. 创建Data对象
data = Data(x=x, edge_index=edge_index)

print(data.num_nodes)     # 3
print(data.num_edges)     # 2
print(data.is_directed()) # True
print(data.has_isolated_nodes()) # False
```

**核心属性规范**：
- `data.x`: 节点特征张量，形状为 `[num_nodes, num_node_features]`。
- `data.edge_index`: 图的拓扑结构（COO稀疏矩阵格式），形状为 `[2, num_edges]`，类型为 `torch.long`。第一行是Source节点，第二行是Target节点。
- `data.edge_attr`: 边特征张量，形状为 `[num_edges, num_edge_features]`。
- `data.y`: 训练标签（既可以是节点级 `[num_nodes, *]`，也可以是图级 `[1, *]`）。

## 3. 具体应用案例
**场景**：社交网络用户关系建模。
假设我们在构建一个微型社交网络，有3个用户（节点），每个用户有2个特征（年龄，注册时长），用户之间存在2条关注关系（边），并且我们希望通过图神经网络去预测这些用户是否为虚假机器人账号。
我们可以用 `Data` 对象将这个微型网络装载进内存中。`Data` 对象的字典式访问 (`data['x']`)、自动推断节点数量以及与 GPU 设备的无缝转移 (`data.to('cuda')`)，让处理图数据变得和处理普通的图片分类数据流一样顺畅。在图层内部传播时，GNN只看 `x` 和 `edge_index` 就可以完成特征聚合。

## 4. 常见误区与陷阱 (Pitfalls)
> [!WARNING] 踩坑预警
> - **Edge Index 形状错误**: `edge_index` 必须是 `[2, num_edges]` 而不是 `[num_edges, 2]`。新手常把边的列表 `[(0,1), (1,2)]` 直接转张量，导致后续 GNN 层报错。如果拿到的是 `[num_edges, 2]`，必须调用 `.t().contiguous()` 转置。
> - **无向图的隐式表示**: PyG 的 `Data` 底层没有专门的“无向图”开关。无向图必须通过**双向有向边**来表示（例如，如果有0-1的边，`edge_index` 中必须同时包含列 `[0, 1]` 和列 `[1, 0]`）。建议直接使用 `torch_geometric.utils.to_undirected` 工具函数来处理原始边数据。
> - **数据类型不匹配**: `edge_index` 必须是 `torch.long` (即 `int64`)，而特征 `x` 通常是 `torch.float` (即 `float32`)。如果不小心将边索引转成了浮点数，会导致底层 C++/CUDA 代码在提取索引时直接抛出类型异常。

## 5. 跨学科链接与双链
- **上游知识**：[[02-Knowledge/🧠 学习系统/01-社交网络挖掘/01-图与网络基础/图论基础]]]（邻接矩阵、图论基本定义）, [[[PyTorch张量基础]]]
- **下游知识**：[[PyG Dataset.md]]]（管理多个Data对象的集合）, [[[Message Passing机制]]]（利用Data对象进行消息传递计算）
- **跨领域关联**：稀疏矩阵存储结构 (计算机科学：Sparse Matrix Storage - Coordinate list COO，这是 `edge_index` 设计的底层依据)。

## 6. 费曼自测清单 (Active Recall)
- [ ] PyG的Data对象中，表示图拓扑结构的核心属性是什么？它的形状有什么强制要求？
- [ ] 为什么 PyG 采用 COO 格式（边索引）而不是 N×N 的稠密邻接矩阵来存储图结构？
- [ ] 如何在一个 Data 对象中表示一个包含5个节点、4条边的无向图？`edge_index` 张量需要包含多少列？
- [ ] 如果我要给每条边添加一个距离权重值，应该存储在 Data 对象的哪个属性里？它的形状应该是什么？
