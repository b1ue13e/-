---
type: study
topic: "PageRank、HITS 与个性化 PageRank"
course: "社交网络挖掘"
created: 2026-08-06
status: planned
difficulty: intermediate
concept: [PageRank, HITS, 个性化随机游走]
prerequisites: [有向图, 随机矩阵, 特征向量]
related: [中心性度量, PageRank-Spam-Farm与抗操纵, 链接预测与无泄漏评估]
flow: knowledge
kind: derivation
stage_moc: "[[🧭 阶段4-排序与链接预测]]"
upstream: ["[[中心性度量]]", "[[有向网络统计与数据清洗]]", "[[社交网络挖掘-线性代数与矩阵传播基础]]"]
source: "Stanford CS224W 2017 lecture Link Analysis and HW4-Q1"
source_url: "https://snap.stanford.edu/class/cs224w-2017/homeworks/hw4/hw4.pdf"
accessed: 2026-08-07
license: "课程材料公开访问但未核验开放再分发许可；仅保留公式方法与题号定位，link-only"
assessment_exempt: false
tags: [学习, 社交网络挖掘, PageRank, HITS, PPR]
---

# PageRank、HITS 与个性化 PageRank

## 问题动机

入度只计算票数，不区分投票者质量。PageRank 用随机游走递归传播声望，HITS 区分“好目录”和“好内容”，PPR 则把随机重启集中到特定用户或主题。

## 正式定义

采用列随机转移矩阵 $M$，PageRank/PPR 满足

$$
r=\beta Mr+(1-\beta)s,
$$

其中 $s$ 是和为 1 的 teleport 分布。$s=\mathbf 1/n$ 时是全局 PageRank；任意偏好分布给出 PPR。悬挂列必须替换为 $s$ 或预先声明的统一分布。

HITS 对邻接矩阵 $A$ 迭代

$$
a=A^Th,\qquad h=Aa,
$$

因此 authority 是 $A^TA$ 的主特征向量，hub 是 $AA^T$ 的主特征向量。矩阵方向取决于 $A_{ij}$ 的边约定，使用前必须写清。

## 为什么 teleport 必不可少

没有 teleport 时，随机游走可能陷入闭合子图或在周期结构中振荡。加入重启后可写成

$$
(I-\beta M)r=(1-\beta)s.
$$

这也说明 $r$ 对未归一化输入 $s$ 是线性的，从而可以组合预计算的主题 PageRank 向量。

## 已解手算例

两节点互相指向，$s=(1,0)$、$\beta=1/2$：

$$
r_1=\tfrac12r_2+\tfrac12,\qquad r_2=\tfrac12r_1,
$$

解得 $r=(2/3,1/3)$。回代后元素和为 1。

## 可运行例

```python
import networkx as nx

graph = nx.DiGraph([(0, 1), (1, 0), (2, 1)])
ppr = nx.pagerank(
    graph,
    alpha=0.85,
    personalization={0: 1.0, 1: 0.0, 2: 0.0},
)
hubs, authorities = nx.hits(graph, max_iter=1000, normalized=True)

assert abs(sum(ppr.values()) - 1.0) < 1e-10
assert max(authorities, key=authorities.get) == 1
print(ppr)
print(hubs, authorities)
```

## 概念对比

| 方法 | 递归对象 | 个性化 | 主要风险 |
| :--- | :--- | :--- | :--- |
| PageRank | 单一稳态声望 | 均匀重启 | 链接操纵、悬挂节点 |
| PPR | 单一稳态声望 | 任意 $s$ | 种子偏差、局部过窄 |
| HITS | hub/authority 双角色 | 通常基于查询子图 | 主题漂移、互相强化 |
| 入度 | 原始入边数 | 无 | 不考虑来源质量 |

## 常见错误

1. 行随机和列随机约定混用。
2. 忘记修复 dangling node，导致概率质量丢失。
3. 把 PageRank 当成入度排序。
4. 把 HITS 的 hub 与 authority 当成同一个分数。
5. 用测试期边构造排名图，再声称预测未来链接。

## 渐隐练习

在三节点链 `0 -> 1 -> 2` 上自行补全 dangling 规则，完成两轮 PageRank 迭代。只给检查点：每轮向量元素和必须为 1；改变 $s$ 后先判断哪一项注入改变，再计算数值。

## 闭卷验收

- 写出 PageRank/PPR 方程并解释每个符号。
- 手算两节点例并回代。
- 从两条 HITS 方程推出 $A^TA$ 与 $AA^T$。
- 解释 teleport 解决的两个马尔可夫链问题。
- 说明全局排名、个性化排名和 hub/authority 各适合什么任务。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/01-社交网络挖掘"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

