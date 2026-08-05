---
title: "NetworkX创建图"
date: 2026-07-31
type: concept
kind: concept
flow: knowledge
course: "01-社交网络挖掘"
importance: "A"
tags: [学习, 核心概念, NetworkX]
upstream: ["[[图与网络基础]]", "[[NetworkX入门]]"]
downstream: ["[[图论算法]]", "[[节点中心性计算]]"]
status: learning
---

> [!NOTE] 核心直觉：搭积木建城市
> **类比**：使用 NetworkX 创建图就像是玩乐高搭城市。首先，你需要铺开一张空白的地图（创建一个空图对象），然后你可以一个个放置建筑物（添加节点 Node），接着你用道路把这些建筑物连接起来（添加边 Edge）。你可以随时在建筑物上贴标签（节点属性），或者说明道路的长度、是否单行（边属性）。

## 1. 为什么需要这个知识点？
- **背景**：在进行社交网络挖掘或任何基于图的数据分析时，我们首先需要将现实世界的数据（如社交关系、交通路线）转化为计算机可以理解的图数据结构。
- **痛点**：自己手写图数据结构（如邻接矩阵或邻接表）容易出错且缺乏高级操作，难以处理带有复杂属性的大规模网络。
- **意义**：NetworkX 提供了极度灵活且直观的 API，使得在 Python 中从零开始构建、修改、丰富网络结构变得极其简单，是后续所有复杂网络分析的基础。

## 2. 核心定义与公式/代码

NetworkX 的图对象主要包含四种：无向图 (`Graph`)、有向图 (`DiGraph`)、多重无向图 (`MultiGraph`) 和多重有向图 (`MultiDiGraph`)。

```python
import networkx as nx

# 1. 创建空图（以无向图为例）
G = nx.Graph()

# 2. 添加节点 (Nodes)
G.add_node(1) # 添加单个节点
G.add_nodes_from([2, 3]) # 批量添加节点
G.add_nodes_from([
    (4, {"color": "red"}),
    (5, {"color": "green"}),
]) # 批量添加带属性的节点

# 3. 添加边 (Edges)
G.add_edge(1, 2) # 添加单条边
G.add_edges_from([(1, 3), (2, 3)]) # 批量添加边
G.add_edges_from([
    (1, 4, {"weight": 2.5}),
    (2, 5, {"weight": 1.0}),
]) # 批量添加带属性的边

# 4. 获取图的基本信息
print(G.nodes()) # 输出: [1, 2, 3, 4, 5]
print(G.edges()) # 输出: [(1, 2), (1, 3), (1, 4), (2, 3), (2, 5)]
```

## 3. 具体应用案例
**场景**：构建一个微型的好友关系网络，并计算共同好友。
假设有 Alice, Bob, Charlie, David 四人，Alice 和 Bob、Charlie 认识，Bob 和 Charlie 也认识，Charlie 还认识 David。我们需要将其建成网络，并记录他们相识的年份。

```python
import networkx as nx

G = nx.Graph()
# 批量添加边及属性（相识年份）
relations = [
    ("Alice", "Bob", {"since": 2015}),
    ("Alice", "Charlie", {"since": 2018}),
    ("Bob", "Charlie", {"since": 2016}),
    ("Charlie", "David", {"since": 2020})
]
G.add_edges_from(relations)

# 查看Alice和Charlie之间边的属性
print(G["Alice"]["Charlie"]) # 输出: {'since': 2018}

# Alice和Bob的共同好友（即他们共同的邻居）
common_friends = list(nx.common_neighbors(G, "Alice", "Bob"))
print(common_friends) # 输出: ['Charlie']
```

## 4. 常见误区与陷阱 (Pitfalls)
> [!WARNING] 踩坑预警
> - **[重复添加节点/边不会报错]**: 如果你向图中添加已经存在的节点或边，NetworkX 不会抛出异常，而是静默地更新属性。这可能会掩盖数据清洗过程中的重复数据问题。
> - **[无向图 vs 有向图的边遍历]**: 在有向图中添加边 `G.add_edge('A', 'B')` 只意味着 `A -> B`，此时 `B` 的邻居不包含 `A`。如果在无向图中添加，则是双向的。初学者常因为选错图类型导致入度出度计算错误。
> - **[节点类型]**: 任何可哈希（Hashable）的 Python 对象都可以作为节点（例如字符串、整数、元组），但列表（List）或字典（Dict）不可哈希，不能作为节点，否则会引发 `TypeError`。

## 5. 跨学科链接与双链
- **上游知识**：[[Python基础]]，[[数据结构（邻接表/邻接矩阵）]]
- **下游知识**：[[NetworkX图可视化]]，[[度分布分析]]，[[最短路径算法]]
- **跨领域关联**：数据库原理（属性图数据库如 Neo4j 的基本数据模型与 NetworkX 高度一致）。

## 6. 费曼自测清单 (Active Recall)
- [ ] 如何创建一个有向图，而不是无向图？
- [ ] 如何一次性向图中添加带权重的多条边？
- [ ] 如果试图把一个 Python 字典 `{"id": 1}` 作为一个节点添加到 NetworkX 图中，会发生什么？
- [ ] 当向 `Graph` 中重复添加边 `(A, B)` 且赋予不同的权重时，NetworkX 的默认行为是什么？
