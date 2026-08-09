---
type: study
topic: "Python 图数据处理基础"
course: "社交网络挖掘"
created: 2026-08-07
status: planned
difficulty: beginner
concept: [Python容器, 边表, 数据不变量]
prerequisites: [Python基础语法]
flow: knowledge
kind: concept
stage_moc: "[[🧭 社交网络挖掘-前置知识]]"
upstream: ["[[数学与Python前置诊断]]"]
source: "Python 3 documentation; NetworkX stable documentation"
source_url: "https://networkx.org/documentation/stable/tutorial.html"
accessed: 2026-08-07
license: "本地原创桥接卡；官方文档仅作 API 定位，link-only"
tags: [学习, 社交网络挖掘, Python, 前置知识]
---

# 社交网络挖掘：Python 图数据处理基础

## 要解决的问题

网络算法接收的不是“一个图”的抽象概念，而是边表、节点属性和清洗规则。只要把字符串、方向或重复边处理错，后续所有中心性、社区和传播结果都会建立在错误输入上。

本卡只要求掌握课程会反复使用的四件事：容器选择、边表解析、不变量检查和 NetworkX 图类型。文件操作、面向对象和高阶 Python 语法不在本卡范围内。

## 最小数据契约

一条有向边写成有序对 $(u,v)$，表示从 $u$ 指向 $v$。读取边表前必须决定：

1. 节点标识是字符串还是整数，是否允许自动转换。
2. 空行和注释行如何处理。
3. 自环 $(u,u)$ 是否保留。
4. 重复边是去重、计数为权重，还是使用 `MultiDiGraph` 保留。
5. 有向边是否允许被错误地排序成无向对。

集合适合去重，字典适合保存节点到属性的映射，列表适合保留事件顺序。不要因为列表最熟悉就用它承担所有职责。

## 可运行最小例

```python
from io import StringIO
import networkx as nx

raw = StringIO("1 2\n2 1\n2 3\n2 3\n3 3\n")
edges = []
for line_no, line in enumerate(raw, start=1):
    parts = line.split()
    if len(parts) != 2:
        raise ValueError(f"line {line_no}: expected two columns")
    source, target = map(int, parts)
    edges.append((source, target))

unique_edges = set(edges)
graph = nx.DiGraph()
graph.add_edges_from(unique_edges)

assert len(edges) == 5
assert len(unique_edges) == 4
assert graph.number_of_nodes() == 3
assert graph.number_of_edges() == 4
assert graph.has_edge(1, 2) and graph.has_edge(2, 1)
assert list(nx.selfloop_edges(graph)) == [(3, 3)]
print(sorted(graph.in_degree()), sorted(graph.out_degree()))
```

预期输出中的节点顺序可以排序固定；入度和出度必须分别计算，不能用一个无向度数替代。

## 从容器到图对象

| 需求 | 合适结构 | 失败方式 |
| :--- | :--- | :--- |
| 去重后的简单边集 | `set[tuple]` | 丢失事件次数与时间顺序 |
| 保留事件流 | `list[tuple]` | 重复事件不能直接当简单边 |
| 简单有向网络 | `nx.DiGraph` | 平行边会被合并 |
| 保留平行边 | `nx.MultiDiGraph` | 多数统计量需先声明聚合口径 |
| 节点属性 | `dict[node, value]` | 缺失键需要显式默认值或报错 |

选择结构的依据是数据语义，不是 API 是否方便。

## 必须先写的断言

- 节点数、边数与去重策略一致。
- 有向图中互为反向的两条边都能保留。
- 自环数量符合策略。
- 节点属性的键集合不超出节点集合。
- 训练/测试切分后两组边没有重叠。

断言应该在计算复杂指标前失败。等到 PageRank 或社区结果异常才回查输入，定位成本会高很多。

## 常见错误

1. **用 `set(tuple(sorted(edge)))` 处理有向边。** 这会把 $(u,v)$ 和 $(v,u)$ 合并。
2. **把重复事件直接当重复关系。** 事件次数可能应成为权重，而不是被静默丢弃。
3. **先建图后才记录清洗规则。** 最终无法判断边数变化来自数据还是代码。
4. **只检查程序没有报错。** 合法运行不等于图语义正确，必须检查不变量。

## 与课程的连接

阶段 1 会在这个数据契约上定义度、互惠、WCC、SCC 和 Bow-tie。后续阶段虽然更换算法，但都必须继承同一份原始数据、清洗清单和版本记录。

## 检索练习与通过标准

合上笔记后独立完成：

1. 解释 `DiGraph` 与 `MultiDiGraph` 的差别。
2. 写出不会破坏方向的边去重代码。
3. 为自环、重复边和缺失属性各写一个断言。
4. 修改最小例，使重复边次数成为 `weight`。

四项均完成且能解释每个断言防止什么错误，才算通过。只复制代码或只得到相同输出不算通过。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/01-社交网络挖掘"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
