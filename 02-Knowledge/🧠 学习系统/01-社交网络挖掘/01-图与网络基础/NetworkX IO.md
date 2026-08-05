---
title: "NetworkX IO"
date: 2026-07-31
type: concept
kind: concept
flow: knowledge
course: "01-社交网络挖掘"
importance: "A"
tags: [学习, 核心概念, NetworkX, IO, 图数据存储]
upstream: ["[[NetworkX入门]]"]
downstream: ["[[真实图数据分析]]", "[[图可视化]]"]
status: learning
---

> [!NOTE] 核心直觉：翻译官与档案管理员
> **类比**：NetworkX的IO模块就像是一个精通多国语言的“翻译官”兼“档案管理员”。它能够将NetworkX在内存中抽象的“图结构”（节点、边、属性）翻译成各种外部存储格式（如GML, GraphML, 边表等），以便长期保存或与其他软件（如Gephi, Pajek）共享；同时也能将外部格式“翻译”回Python内存中的图对象。

## 1. 为什么需要这个知识点？
- **背景**：在真实的社交网络挖掘任务中，图数据通常非常庞大且存储在文件系统中。同时，我们通过计算得出的网络特征（如中心性指标、社区划分结果）也需要被持久化保存。
- **痛点**：手动解析不同格式的图数据（特别是包含复杂节点和边属性的数据）非常繁琐且容易出错。而且不同的图分析和可视化工具支持的数据格式往往各不相同。
- **意义**：掌握NetworkX的IO操作，打通了图数据从“硬盘”到“内存”，再从“内存”到“硬盘”的闭环，是进行任何实际社交网络挖掘项目不可或缺的数据工程基础。

## 2. 核心定义与公式/代码
NetworkX 提供了一系列 `read_*` 和 `write_*` 方法来处理不同格式的图文件。

**1. Edge List (边列表)**
最常见、最简单的格式，适合存储带有简单权重或属性的边。
```python
import networkx as nx

G = nx.path_graph(4)
# 写入 (默认使用空格分隔)
nx.write_edgelist(G, "test.edgelist", data=False)
# 读取
G_read = nx.read_edgelist("test.edgelist")
```

**2. Adjacency List (邻接表)**
适合存储没有复杂属性的简单图。
```python
# 写入
nx.write_adjlist(G, "test.adjlist")
# 读取
G_read = nx.read_adjlist("test.adjlist")
```

**3. GML (Graph Modelling Language)**
支持丰富的节点和边属性，是一种通用的纯文本图格式。
```python
# 写入
nx.write_gml(G, "test.gml")
# 读取
G_read = nx.read_gml("test.gml")
```

**4. GraphML**
基于XML的图格式，高度结构化，被许多图处理软件（如Gephi）广泛支持。
```python
# 写入
nx.write_graphml(G, "test.graphml")
# 读取
G_read = nx.read_graphml("test.graphml")
```

## 3. 具体应用案例
**场景**：将处理好的推特(Twitter)用户关系网络导出，以便使用Gephi进行高级可视化渲染。

假设你在Python中使用NetworkX分析了一个Twitter网络，计算了每个用户的PageRank，并将其作为节点属性保存在了图中。现在你想用Gephi来绘制这个网络，让高权重的节点显得更大。

**操作步骤**：
1. 计算属性并赋值：
```python
pageranks = nx.pagerank(G)
nx.set_node_attributes(G, pageranks, 'pagerank')
```
2. 导出为GraphML格式（不要用Edge List，因为它不能保存节点属性）：
```python
nx.write_graphml(G, "twitter_network_with_pr.graphml")
```
3. 随后，你可以直接在Gephi中导入 `twitter_network_with_pr.graphml` 文件。Gephi会自动识别出节点、边，以及你刚刚计算的 `pagerank` 属性，并将其用于调整节点的大小或颜色映射。

## 4. 常见误区与陷阱 (Pitfalls)
> [!WARNING] 踩坑预警
> - **[属性丢失陷阱]**: 很多初学者使用 `write_edgelist` 导出带有多维节点属性的图，导致再读入时节点属性全部丢失。Edge list 只能保存边的拓扑和边上的属性。如果图包含丰富的节点属性，必须使用 `GML`、`GraphML` 或 `Node/Link JSON` 格式。
> - **[节点类型限制错误]**: 在写入 GML 等格式时，NetworkX 通常要求节点的标签必须是字符串或整数。如果你的节点名称是复杂的 Python 对象（如元组 `(1, 2)` 或类的实例），直接写入会抛出错误，需要先进行类型转换或使用 `nx.relabel_nodes` 映射为字符串。
> - **[超大规模图的内存爆炸]**: 基于 XML 的 GraphML 文件不仅体积大，而且在解析时会消耗大量内存。对于边数达到数千万量级的图，使用普通的 NetworkX IO 函数不仅极慢，还容易 OOM (Out Of Memory)。此时应当考虑分块读取、使用稀疏矩阵，或者直接连接图数据库（如 Neo4j）。

## 5. 跨学科链接与双链
- **上游知识**：[[NetworkX入门]], [[数据序列化]]
- **下游知识**：[[复杂网络可视化]], [[Gephi基础]], [[大图数据处理]]
- **跨领域关联**：文件解析技术 (XML/JSON Parsing)、持久化存储系统 (Persistence Storage)。

## 6. 费曼自测清单 (Active Recall)
- [ ] 为什么要使用 GraphML 或 GML 格式而不是简单的 Edge list 格式？它们在存储能力上的核心区别是什么？
- [ ] 如果我的图中节点ID是一个 Python 字典对象，直接导出为 GML 会发生什么？应该如何安全地导出？
- [ ] 用 Python 默写：将一个图对象 `G` 保存为 `network.graphml` 文件，并再次读取为对象 `H` 的两行核心代码。
- [ ] NetworkX的内置IO模块在处理亿级节点的大规模图时会遇到什么性能瓶颈？如何缓解？
