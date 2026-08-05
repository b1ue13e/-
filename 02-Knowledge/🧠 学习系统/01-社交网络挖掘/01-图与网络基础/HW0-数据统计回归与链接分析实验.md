---
type: study
topic: "HW0 数据统计、回归与链接分析实验"
tags: [学习, 01-社交网络挖掘, HW0, NetworkX, SNAP]
created: 2026-08-05
status: ongoing
difficulty: beginner
concept: [有向统计, log-log回归, 链接分析]
prerequisites: [可复现网络挖掘实验与环境工作流, 有向网络统计与数据清洗, PageRank-HITS-PPR与Spam-Farm]
related: [度分布余度与幂律估计, 路径连通与Bow-tie结构]
flow: knowledge
kind: problem-type
source: "Stanford CS224W 2017 HW0-Q1-Q3; public wiki-Vote and StackOverflow-Java datasets"
verification_status: "题面、流程与示例代码已整理；需保存真实数据运行记录后才能完成"
anki_deck: "社交网络挖掘::作业实验"
anki_tags: [HW0, wiki-Vote, polyfit, PageRank, HITS]
---

# HW0 数据统计、回归与链接分析实验

## 0. 先判断它值不值得深挖
- **类别**：A 类小白作业入口。
- **判断理由**：HW0 建立全课的数据/方向/工具口径；若互惠边、零度节点或 log 回归做错，后续结果都会静默偏离。

## 1. 这个知识点解决什么问题？
> 如何从公开压缩边表可靠构造有向图，完成 9 个统计、log-log 频数回归、WCC、PageRank 和 HITS，并对 SNAP/NetworkX 输出统一口径？

## 2. 为什么它重要？它有什么用？
- 形成第一条真实数据端到端路径。
- 训练有向/无向/互惠三种边计数与零度节点。
- 建立 `polyfit`、排序与组件提取的可复现习惯。

## 3. 学它之前需要哪些前置知识？
1. [[../06-表示学习与项目/可复现网络挖掘实验#原笔记：NetworkX-SNAP环境与数据工作流]]。
2. [[有向网络统计与数据清洗]]、[[../04-排序与链接预测/PageRank-HITS-PPR与Spam-Farm]]。

## 4. 用直觉语言解释它
> “先确认箭头和计数单位，再画分布、拟合趋势，最后让递归排名寻找被高质量用户认可的专家。”
- **一句话本质**：数据契约→不变量→统计/回归→链接分析。

## 5. 正式定义、核心公式、符号解释

### 1. Q1 九项统计
- 节点数；含自环节点数；非自环有向边数。
- 无向边数：非自环有向边投影成无序对后的集合大小。
- 互惠对数：同时存在 $(u,v),(v,u)$ 的无序节点对数。
- 零出度/零入度；出度 $>10$；入度 $<10$ 的节点数。

### 2. Q2 频数而非概率
$x$ 是正出度，$y_x$ 是出度恰为 $x$ 的**节点数**。过滤 $x=0$ 和 $y=0$，以 base 10：
$$X=\log_{10}x,\quad Y=\log_{10}y,\qquad Y=aX+b.$$
`numpy.polyfit(X,Y,1)` 返回斜率 $a$、截距 $b$；原尺度为 $y=10^b x^a$。

### 3. Q3 WCC 与链接分析
- WCC 在忽略方向后求连通分量。
- 最大 WCC 报节点数与边数，边数仍按原有向子图计。
- PageRank 排全局链接声望；HITS 分别排 hub 与 authority。排序时固定 `(-score,node_id)`，避免并列不稳定。

### 4. SNAP/NetworkX 语义映射
| 任务 | SNAP 2017 | NetworkX 验证 |
| :--- | :--- | :--- |
| WCC | `GetWccs` | `weakly_connected_components` |
| 最大 WCC | `GetMxWcc` | 最大 WCC 节点诱导子图 |
| PageRank | `GetPageRank` | `pagerank` |
| HITS | `GetHits` | `hits` |

## 6. 推导思路和思想来源
1. 用集合投影统一无向/互惠计数，避免对有向边循环重复加倍。
2. 零度节点必须来自完整节点集合，不能只看边端点的某一侧。
3. log-log LS 拟合的是频数点，不是概率似然；仅完成题面趋势线，不证明幂律。
4. 递归排名的库实现需用小图/概率和检查，而非盲信默认参数。

## 7. 例子：已解 → 半提示 → 可运行骨架

### 例子 1：官方同构小图手算
边 `(1,2),(2,1),(1,3),(1,1)`：节点 3；含自环节点 1；非自环有向边 3；无向投影 2；互惠对 1；零出度节点 1；零入度节点 0。

### 例子 2：半提示
若 log 回归得到 `a=-1.5,b=2`，原尺度趋势线为 `y=____`。
> [!question]- 核对
> $y=10^2x^{-1.5}=100x^{-1.5}$。

### 例子 3：可运行端到端函数
```python
from collections import Counter
import numpy as np
import networkx as nx

def directed_statistics(graph):
    nodes = set(graph)
    non_loop = {(u, v) for u, v in graph.edges() if u != v}
    undirected = {tuple(sorted((u, v))) for u, v in non_loop}
    reciprocal = {pair for pair in undirected
                  if pair in non_loop and pair[::-1] in non_loop}
    return {
        "nodes": len(nodes),
        "self_loop_nodes": len(list(nx.nodes_with_selfloops(graph))),
        "directed_non_loop_edges": len(non_loop),
        "undirected_edges": len(undirected),
        "reciprocal_pairs": len(reciprocal),
        "zero_out": sum(graph.out_degree(node) == 0 for node in nodes),
        "zero_in": sum(graph.in_degree(node) == 0 for node in nodes),
        "out_gt_10": sum(graph.out_degree(node) > 10 for node in nodes),
        "in_lt_10": sum(graph.in_degree(node) < 10 for node in nodes),
    }

def outdegree_polyfit(graph):
    counts = Counter(value for _, value in graph.out_degree() if value > 0)
    x = np.array(sorted(counts), dtype=float)
    y = np.array([counts[int(value)] for value in x], dtype=float)
    slope, intercept = np.polyfit(np.log10(x), np.log10(y), 1)
    return slope, intercept

graph = nx.DiGraph([(1,2),(2,1),(1,3),(1,1)])
stats = directed_statistics(graph)
assert stats["nodes"] == 3 and stats["reciprocal_pairs"] == 1
larger = nx.gn_graph(50, seed=7).reverse()
slope, intercept = outdegree_polyfit(larger)
pagerank = nx.pagerank(graph)
hubs, authorities = nx.hits(graph, max_iter=1000, normalized=True)
print(stats)
print(round(slope, 3), round(intercept, 3), max(pagerank, key=pagerank.get),
      max(hubs, key=hubs.get), max(authorities, key=authorities.get))
# 输出九项统计、回归系数及 PageRank/hub/authority 最高节点。
```

### 正式数据步骤
1. 从官方 [wiki-Vote](https://snap.stanford.edu/data/wiki-Vote.html) 与 HW0 PDF 给出的 StackOverflow-Java 链接下载 `.gz`。
2. 记录 SHA-256；用 `gzip.open(..., "rt")` 跳过 `#` 注释并读前两列整数。
3. `DiGraph` 读入；检查是否有重复边被集合化。
4. Q2 绘散点与 $10^b x^a$ 线，双轴 base-10 log；报告 $a,b$。
5. Q3 输出 WCC 数、最大 WCC 的节点/有向边数、top-3 PageRank/hub/authority。

## 8. 常见误区和易混概念
- 互惠边计 2：题面计唯一无序对，应计 1。
- 非自环有向边仍包含自环：必须过滤 `u!=v`。
- Q2 把 y 归一化成概率：题面要求节点频数。
- 最大 WCC 边数用无向投影：题面网络仍是有向图子图。
- top-3 只打印分数不打印节点 ID，或不固定并列顺序。

| 统计 | 单位 | 自环 | 方向 |
| :--- | :--- | :--- | :--- |
| directed edges | ordered pair | 排除 | 保留 |
| undirected edges | unordered pair | 排除 | 忽略 |
| reciprocated | unordered pair | 排除 | 要求双向 |

## 9. 相关知识点与 Obsidian 双链建议
- 上游：[[有向网络统计与数据清洗]]。
- 横向：[[../02-网络结构与生成模型/度分布余度与幂律估计]]。
- 下游：[[路径连通与Bow-tie结构]]、[[../04-排序与链接预测/PageRank-HITS-PPR与Spam-Farm]]。
- 作业：CS224W 2017 HW0-Q1.1–Q1.9、Q2.1–Q2.2、Q3.1–Q3.4。

## 10. 闭卷复现任务
- [ ] 手算九项统计。
- [ ] 用集合实现无向/互惠。
- [ ] 处理零度节点。
- [ ] 构造频数表。
- [ ] 做 base-10 polyfit。
- [ ] 还原原尺度线。
- [ ] 求 WCC/最大 WCC。
- [ ] 运行 PageRank/HITS。
- [ ] 固定 top-3 排序。
- [ ] 记录数据哈希/版本。

## 11. 自测题：5 道
1. 一对互惠有向边贡献几个 reciprocal edge？ #自测题/基础
   > [!question]- 1 个唯一无序节点对。
2. Q2 的纵轴是频数还是比例？ #自测题/基础
   > [!question]- 出度恰为 x 的节点数（频数）。
3. `polyfit` 斜率对应什么？ #自测题/中等
   > [!question]- $log_{10}y=a\log_{10}x+b$ 中的 $a$。
4. 最大 WCC 的边数保留方向吗？ #自测题/中等
   > [!question]- WCC 节点集合按忽略方向得到，但诱导子图边数仍按原有向边计。
5. PageRank 与 HITS authority 为什么可能给不同专家？ #自测题/较难
   > [!question]- PageRank 是单稳态全局声望，HITS 在 hub-authority 双角色反馈中评分，结构目标不同。

## 12. 我的主动回忆区
### 我的闭卷复述
> 按 Q1→Q2→Q3 复述数据、统计、回归和链接分析管线。
### 我的推导复现
> 手算集合计数并从 log 回归还原 $y=10^bx^a$。
### 我的错误与卡点
- [ ] 互惠数翻倍 → 使用无序对集合。
- [ ] 回归点不对 → 检查 y 是频数且过滤 0。
- [ ] 排名不稳定 → 固定分数降序、ID 升序。
### 失败后的回流
- 计数错：[[有向网络统计与数据清洗]]；回归错：第 5.2 节；排名错：[[../04-排序与链接预测/PageRank-HITS-PPR与Spam-Farm]]。

## 13. 给 Obsidian 的归档建议
- 文件夹：`01-图与网络基础/`
- 关联：[[有向网络统计与数据清洗]]
- 标签：`#HW0` `#数据实验` `#链接分析`
- 拆分建议：HW0 是单一端到端入门作业，保持一张实验卡。

## 🃏 Anki 卡片
- HW0 互惠边如何计数？::同时存在双向边的唯一无序节点对数，每对计 1。
- HW0 log-log 回归的原尺度形式？::$\log_{10}y=a\log_{10}x+b$ 等价于 $y=10^bx^a$。
