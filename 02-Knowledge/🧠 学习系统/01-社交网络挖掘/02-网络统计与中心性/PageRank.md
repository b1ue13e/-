---
type: study
topic: "PageRank"
created: 2026-04-18
updated: 2026-08-01
status: completed
difficulty: intermediate
concept: ["PageRank", "随机游走", "中心性"]
prerequisites: ["有向图", "马尔可夫链", "特征向量"]
related: ["Katz中心性", "HITS算法", "PPR"]
tags: [学习, 社交网络挖掘, 中心性]
flow: knowledge
kind: concept
---

# PageRank

PageRank 根据**高质量入链的传递性**为有向图节点排序：被重要节点指向，比被许多低权重节点指向更有价值。它可解释为带随机跳转的随机游走的平稳分布。

## 1. 随机游走模型

令 $P$ 为行随机转移矩阵：若节点 $j$ 的出度为 $d_j^+$，则沿其出边到 $i$ 的概率为 $P_{ji}=1/d_j^+$。采用列向量表示排名时，PageRank 满足

$$
r=\alpha P^\top r+(1-\alpha)v,
$$

其中：

- $r_i\ge 0$ 且 $\sum_i r_i=1$；
- $0<\alpha<1$ 是继续沿链接移动的概率，常用 0.85；
- $v$ 是概率和为 1 的跳转或个性化向量。

等价线性系统为

$$
(I-\alpha P^\top)r=(1-\alpha)v.
$$

随机跳转使模型不被汇点或封闭子图永久困住，并在常见设定下得到唯一稳定排名。

## 2. 悬挂节点必须显式处理

出度为 0 的节点称为悬挂节点。它在 $P$ 中对应全零行，破坏概率守恒。标准处理是把该行替换为 $v^\top$，即到达悬挂节点后按跳转分布重新出发。实现时不要静默忽略这一步。

## 3. 幂迭代

从任意概率向量 $r^{(0)}$ 出发，重复

$$
r^{(t+1)}=\alpha P^\top r^{(t)}+(1-\alpha)v
$$

直到 $\|r^{(t+1)}-r^{(t)}\|_1<\varepsilon$。稀疏图上每轮主要成本为稀疏矩阵—向量乘法，约为 $O(m)$。

## 4. 最小例子与验证

考虑 $A\to B$、$B\to C$、$C\to A$ 和 $C\to B$。$B$ 同时获得 $A$ 与 $C$ 的入链，而 $C$ 只获得 $B$ 的入链；最终分数由整个递归结构共同决定，不能只比较入度。

```python
import networkx as nx

G = nx.DiGraph([("A", "B"), ("B", "C"), ("C", "A"), ("C", "B")])
rank = nx.pagerank(G, alpha=0.85, tol=1e-12)
assert abs(sum(rank.values()) - 1.0) < 1e-10
assert rank["B"] > rank["A"]
```

验证时至少检查：分数非负、总和为 1、增大某个高分节点到目标节点的权重后目标分数是否按预期变化。

## 5. 边界与误区

1. **PageRank 不等于入度**：每条入链的贡献取决于来源节点排名及其出度。
2. **方向不能颠倒**：使用邻接矩阵前先确认 $A_{ij}$ 的边方向约定。
3. **高分不等于真实权威**：排名只反映给定图和跳转机制，垃圾链接、采样偏差会影响结果。
4. **个性化向量会改变问题**：PPR 衡量相对于指定种子或偏好的重要性，不应与全局 PageRank 混报。

## 6. 知识连接

- [[02-Knowledge/🧠 学习系统/01-社交网络挖掘/02-网络统计与中心性/Katz中心性|Katz 中心性]]同样递归累计远距离节点的影响，但其衰减形式与归一化方式不同。
- [[02-Knowledge/🧠 学习系统/01-社交网络挖掘/02-网络统计与中心性/PPR|个性化 PageRank（PPR）]]通过非均匀 $v$ 把排名集中到种子节点附近。
- [[02-Knowledge/🧠 学习系统/01-社交网络挖掘/HITS算法|HITS]]分别计算 hub 与 authority 两类分数，而 PageRank 只维护一个稳定分布。

## 参考资料

- Page, L., Brin, S., Motwani, R. & Winograd, T. *The PageRank Citation Ranking: Bringing Order to the Web*, Stanford Technical Report, 1999：https://ilpubs.stanford.edu/422/
- NetworkX `pagerank` 官方文档：https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html
