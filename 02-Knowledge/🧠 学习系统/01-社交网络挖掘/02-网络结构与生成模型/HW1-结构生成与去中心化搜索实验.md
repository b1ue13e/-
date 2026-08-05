---
type: study
topic: "HW1 结构生成与去中心化搜索"
tags: [学习, 01-社交网络挖掘]
created: 2026-08-06
status: ongoing
difficulty: intermediate
concept: [HW1 结构生成与去中心化搜索]
prerequisites: [图与网络基础, Python基础]
related: []
flow: knowledge
kind: problem-type
source: "合并自课程内已有笔记；原始来源见各节"
verification_status: "题面与示例代码已合并；正式作业数据与参数需复现"
---

# HW1：结构生成与去中心化搜索实验

> **阅读顺序**：先完成指定网络生成与结构统计，再学习层次模型中的去中心化搜索证明与仿真。正式作业参数和数据结果未复现前，本卡不能标记为完成。

## 原笔记：HW1-指定网络生成与结构统计实验

### 0. 先判断它值不值得深挖
- **类别**：A 类作业实验。
- **判断理由**：HW1 指定的 ER 是自写 $G(n,m)$，小世界是“二近邻环格 + 4000 条随机非边”，都不能用名字相近的库函数替代。

### 1. 这个知识点解决什么问题？
> 怎样严格复现题面生成过程，在相同 $n,m$ 下公平比较度分布、余度分布和聚类，并保证数据去重、自环处理与绘图口径正确？

### 2. 为什么它重要？它有什么用？
- 把生成模型从概念变成可审计实验。
- 训练“按题面实现，而非按模型名字猜 API”的能力。
- 为 HW1-Q1.1–1.3 产出图、数值和机制解释。

### 3. 学它之前需要哪些前置知识？
1. [[随机网络模型-ER-WS-BA-配置模型]]。
2. [[度分布余度与幂律估计]]、[[聚类系数与网络距离]]。

#### 先备诊断
- [ ] 知道简单无向图候选边数为 $\binom n2$。
- [ ] 能从 $p_k$ 推出 $q_k=(k+1)p_{k+1}/E[D]$。
- [ ] 能手算局部聚类系数。

### 4. 用直觉语言解释它
> “三个网络参加同一体检：人数和关系总数相同，只改变关系生成机制，再比较尾部、朋友的朋友和三角闭包。”
- **一句话本质**：公平对比要求固定规模与统计口径，只改变机制。

### 5. 正式定义、核心公式、符号解释

#### 1. 自写 $G(n,m)$
从全部无序非自环节点对中**无放回均匀抽取** $m$ 对。每张含 $m$ 条边的简单标号图概率相同。

#### 2. HW1 指定小世界
节点排成环；每个节点连接距离 1 和 2 的邻居，形成 $2n$ 条无向边；再从当前非边中无放回抽取 $r$ 条。官方参数 $n=5242,r=4000$，故 $m=2n+r=14484$。

#### 3. 度与余度分布
$$p_k=\frac{n_k}{n},\qquad q_k=\frac{(k+1)p_{k+1}}{\sum_j j p_j}.$$
$$E[D]=\sum_k k p_k,\qquad E[K]=\sum_k k q_k.$$

#### 4. 平均局部聚类
$$C=\frac1n\sum_v C_v,\qquad C_v=\frac{2e_v}{d_v(d_v-1)}\quad(d_v\ge2).$$
必须自写邻居交集计数；库函数只用于验证，不作为提交实现。

#### 5. 数据清洗口径
`ca-GrQc` 作为无向简单图读入：跳过注释；把 `(u,v)` 规范化为排序元组；删除 `u=v`；集合去重。应核对官方题面给出的 $n=5242,m=14484$。

### 6. 推导思路和思想来源
1. $G(n,m)$ 无放回抽样保证边数精确；$G(n,p)$ 只能固定期望边数。
2. 环格的每个节点基础度为 4，高聚类来自相邻邻居之间已有边。
3. 随机非边提供远程连接并拓宽度分布，但不会像 BA 形成强 hub。
4. 余度按度 size-bias，因此其期望通常高于普通度期望。
5. 三图用同一统计函数，避免实现差异伪造成模型差异。

### 7. 例子：已解 → 半提示 → 端到端代码

#### 例子 1：已解手算
$n=6$ 的距离 1/2 环格有 $2n=12$ 条边，每个节点度 4。再加 2 条非边后 $m=14$，平均度 $2m/n=14/3$。

#### 例子 2：半提示
对度序列 `[2,2,2,4,4,4]`：先算 $p_2,p_4,E[D]$，再补 $q_1,q_3,E[K]$。
> [!question]- 核对
> $p_2=p_4=1/2,E[D]=3$；$q_1=1/3,q_3=2/3,E[K]=7/3$。

#### 例子 3：可运行完整骨架
```python
import random
from collections import Counter
import networkx as nx

def gnm_graph(n, m, seed=0):
    rng = random.Random(seed)
    candidates = [(u, v) for u in range(n) for v in range(u + 1, n)]
    if m > len(candidates):
        raise ValueError("m 超过简单图最大边数")
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from(rng.sample(candidates, m))
    return graph

def assigned_small_world(n, extra_edges, seed=0):
    rng = random.Random(seed)
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    for node in range(n):
        for offset in (1, 2):
            graph.add_edge(node, (node + offset) % n)
    non_edges = list(nx.non_edges(graph))
    graph.add_edges_from(rng.sample(non_edges, extra_edges))
    return graph

def distributions(graph):
    degree = [value for _, value in graph.degree()]
    counts, n = Counter(degree), graph.number_of_nodes()
    p = {k: count / n for k, count in sorted(counts.items())}
    mean = sum(k * value for k, value in p.items())
    q = {k - 1: k * value / mean for k, value in p.items() if k > 0}
    return p, q, mean, sum(k * value for k, value in q.items())

def average_clustering_from_scratch(graph):
    total = 0.0
    for node in graph:
        neighbors = set(graph[node])
        degree = len(neighbors)
        if degree < 2:
            continue
        neighbor_edges = sum(1 for u in neighbors for v in graph[u]
                             if v in neighbors) / 2
        total += 2 * neighbor_edges / (degree * (degree - 1))
    return total / graph.number_of_nodes()

er = gnm_graph(30, 70, seed=7)
small_world = assigned_small_world(30, 10, seed=7)
for name, graph in [("ER", er), ("SW", small_world)]:
    p, q, mean_d, mean_excess = distributions(graph)
    clustering = average_clustering_from_scratch(graph)
    assert graph.number_of_edges() == 70
    assert abs(clustering - nx.average_clustering(graph)) < 1e-12
    print(name, round(mean_d, 3), round(mean_excess, 3), round(clustering, 3))
# 输出两图的平均度、平均余度、聚类；边数均严格为 70。
```

#### 正式实验替换参数
- `gnm_graph(5242, 14484, seed)`。
- `assigned_small_world(5242, 4000, seed)`。
- 实证图读入后断言 `n=5242,m=14484`。
- 绘图过滤 $p_k=0/q_k=0$ 后使用 `plt.xscale("log")` 与 `plt.yscale("log")`；不要对 0 取对数。

### 8. 常见误区和易混概念
- 用 `gnp_random_graph` 替代 $G(n,m)$：边数不固定。
- 用 Watts–Strogatz 重连替代“环格加非边”：生成过程不同。
- 候选非边有放回抽样：会出现重复，实际新增边不足。
- 用 NetworkX 聚类直接提交：违反自写要求；可作为单元测试 oracle。

| 实验对象 | 固定项 | 改变项 | 预期重点 |
| :--- | :--- | :--- | :--- |
| ER $G(n,m)$ | $n,m$ | 均匀边 | 窄度、低聚类 |
| 指定小世界 | $n,m$ | 环格+非边 | 高聚类、短路 |
| ca-GrQc | 实证 $n,m$ | 真实机制 | 重尾与高聚类 |

### 9. 相关知识点与 Obsidian 双链建议
- 上游：[[随机网络模型-ER-WS-BA-配置模型]]。
- 下游：[[../01-图与网络基础/路径连通与Bow-tie结构#原笔记：Bow-tie抽样估计与可达率实验]]。
- 横向：[[度分布余度与幂律估计]]、[[聚类系数与网络距离]]。
- 作业：CS224W 2017 HW1-Q1.1–Q1.3。

### 10. 闭卷复现任务
- [ ] 区分 $G(n,m)$ 与 $G(n,p)$。
- [ ] 重建指定小世界边数。
- [ ] 写出实证图清洗不变量。
- [ ] 自写度/余度分布。
- [ ] 自写聚类系数。
- [ ] 解释 log-log 零值处理。
- [ ] 用 toy graph 与库函数交叉验证。
- [ ] 固定 seed 并记录版本。
- [ ] 运行三图同一统计管线。
- [ ] 用机制而非形容词解释差异。

### 11. 自测题：5 道
1. 为什么 Q1 的 ER 不能用 $G(n,p)$？ #自测题/基础
   > [!question]- 题面固定精确边数 $m$，而 $G(n,p)$ 只固定期望。
2. 指定小世界基础环格为何有 $2n$ 条边？ #自测题/基础
   > [!question]- 每点连距离 1/2 共度 4，握手定理给 $4n/2=2n$。
3. 为什么随机非边必须无放回？ #自测题/中等
   > [!question]- 保证每次都新增不同边，从而最终边数精确。
4. 平均余度为何常高于平均度减一？ #自测题/中等
   > [!question]- 沿边抽样按度加权，更常到达高度节点。
5. 如何证明自写聚类实现可信？ #自测题/较难
   > [!question]- 先对三角形、路径、星图手算，再与独立库函数在多个小图交叉验证。

### 12. 我的主动回忆区
#### 我的闭卷复述
> 复述三个网络的生成/清洗过程及必须固定的 $n,m$。
#### 我的推导复现
> 从度频数推出 $p,q,E[D],E[K]$，并重写自定义聚类伪代码。
#### 我的错误与卡点
- [ ] 边数不等于目标 → 检查无放回与非边集合。
- [ ] 小世界统计不对 → 检查是否误用 WS 重连。
- [ ] log 图报错 → 过滤零值而非加任意常数。
#### 失败后的回流
- 生成器错：第 5.1–5.2 节；分布错：第 5.3 节；聚类错：第 5.4 节；数据错：第 5.5 节。

### 13. 给 Obsidian 的归档建议
- 文件夹：`02-网络结构与生成模型/`
- 关联：[[随机网络模型-ER-WS-BA-配置模型]]
- 标签：`#HW1` `#实验` `#图生成`
- 拆分建议：生成、分布和聚类必须共享同一数据口径，保留一张作业实验卡。

### 🃏 Anki 卡片
- HW1 指定小世界如何生成？::距离 1/2 的环格产生 $2n$ 条边，再从当前非边中无放回增加指定数量随机边。
- 自写 $G(n,m)$ 的核心抽样是什么？::从全部无序非自环节点对中无放回均匀抽取恰好 $m$ 对。

## 原笔记：HW1-层次去中心化搜索-证明与仿真

### 0. 先判断它值不值得深挖
- **类别**：A 类作业证明。
- **判断理由**：Q3.1 是五步相依证明；少写一个计数因子、对数底转换或 union bound 条件，后续“高概率可导航”就不成立。

### 1. 这个知识点解决什么问题？
> 在只知道邻居及其与目标的层次距离时，怎样证明每个节点高概率拥有一条“更接近目标”的边，从而在对数步内完成搜索？不同距离衰减参数下，仿真结果为何先改善后恶化？

### 2. 为什么它重要？它有什么用？
- 展示“候选数增长 × 单点概率衰减”的尺度平衡。
- 训练逐步概率下界、指数界和 union bound。
- 完整覆盖 HW1-Q3.1(a–e) 与 Q3.2 的能力链。

### 3. 学它之前需要哪些前置知识？
1. [[小世界与去中心化搜索]]。
2. $1-x\le e^{-x}$、对数换底、union bound、无放回抽样。

#### 先备诊断
- [ ] 能解释完全 $b$ 叉树高度 $h$ 有 $b^h$ 个叶子。
- [ ] 能把 $e^{-a\log_bN}$ 写成 $N$ 的幂。
- [ ] 能说明事件并集概率至多各事件概率之和。

### 4. 用直觉语言解释它
> “目标所在的下一层子树含很多候选；虽然每个远端点概率小，但候选数量刚好补偿。每步只需进入目标所在的更小盒子。”
- **一句话本质**：尺度匹配使每层进步概率约为 $1/log N$，用 $O(log^2N)$ 条边把失败概率压成 $N^{-\theta}$。

### 5. 正式定义、核心公式、符号解释

#### 1. 层次模型
网络节点是高度 $H=\log_bN$ 的完全 $b$ 叉树叶子。$h(v,w)$ 是二者最低公共祖先所根子树的高度。$alpha=1$ 时：
$$p_v(w)=\frac{b^{-h(v,w)}}{Z},\qquad Z=\sum_{w\ne v}b^{-h(v,w)}.$$

#### 2. Q3.1(a)：距离壳层计数
距固定叶子 $v$ 恰为 $d$ 的叶子位于高度 $d$ 的祖先子树中，但不在含 $v$ 的高度 $d-1$ 子树：
$$n_d=b^d-b^{d-1}=(b-1)b^{d-1}.$$

#### 3. Q3.1(b)：归一化上界
$$
Z=\sum_{d=1}^{H}(b^d-b^{d-1})b^{-d}
=\sum_{d=1}^{H}\left(1-\frac1b\right)
=H\left(1-\frac1b\right)\le H=\log_bN.
$$

#### 4. Q3.1(c)：进入目标子树的单边概率
设当前 $v$ 与目标 $t$ 的距离为 $d$。目标所在、但不含 $v$ 的下一层子树 $T'$ 高度 $d-1$，含 $b^{d-1}$ 个叶子；每个 $u\in T'$ 都满足 $h(v,u)=d$：
$$
P(v\to T')=b^{d-1}\frac{b^{-d}}Z
=\frac1{bZ}\ge\frac1{b\log_bN}=:p.
$$

#### 5. Q3.1(d)：无进步边的概率与高概率条件
每个节点无放回选择 $k=c(\log_bN)^2$ 个不同邻居。在“此前尚未命中 $T'$”的条件下，只移除了 $T'$ 外候选，命中概率不会低于初始 $p$，因此
$$
P(\text{no edge to }T')\le(1-p)^k\le e^{-kp}
\le e^{-(c/b)\log_bN}=N^{-\theta},
$$
$$
\theta=\frac{c}{b\ln b}.
$$
对固定目标 $t$，对最多 $N$ 个当前节点作 union bound：
$$P(\exists v\text{ 无进步边})\le N^{1-\theta}.$$
当 $\theta>1$（即 $c>b\ln b$）时，该概率随 $N\to\infty$ 趋 0。若要同时保证所有有序 $(v,t)$，需对 $N^2$ 对 union bound，要求更强的 $\theta>2$。

#### 6. Q3.1(e)：搜索步数
$h(v,t)$ 是 $0,1,\ldots,H$ 的整数。每步选择一个严格减小 $h$ 的邻居，因此至多经过 $H=\log_bN$ 次下降到 0，即到达 $t$：
$$L_{search}\le\log_bN=O(\log_bN).$$

#### 7. Q3.2 广义模型
$$p_v(w)\propto b^{-\alpha h(v,w)}.$$
$\alpha$ 太小使边近似跨尺度随机、缺少目标方向；太大使边过度局部、难跨大尺度；中间匹配区间兼顾方向与跨度。

### 6. 推导思路和思想来源
1. 先数距离壳层，避免把“子树叶子数”和“恰好距离数”混淆。
2. 壳层数量与 $b^{-d}$ 抵消，得到 $Z=O(\log N)$。
3. 不要求一步命中目标，只要求命中目标所在的下一层子树。
4. 用 $O(\log^2N)$ 次独立/无放回机会把每层失败压成多项式小。
5. union bound 把单节点保证升级为所有当前节点保证。
6. 层次距离每步至少降 1，给出对数路径长度。

### 7. 例子：已解 → 半提示 → 完整仿真

#### 例子 1：已解
$b=2,N=8,H=3$。距固定叶子 $d=1,2,3$ 的叶子数为 $1,2,4$；$Z=3/2$，而 $Z\le3$。若当前与目标距离 3，$T'$ 有 4 个叶子，单边命中概率为 $4\cdot2^{-3}/Z=1/3$。

#### 例子 2：半提示
取 $b=2,c=4$。补全 $\theta=c/(b\ln b)=\_\_$，并判断固定目标下 union bound 是否趋 0。
> [!question]- 核对
> $\theta=2/\ln2\approx2.885>1$，所以 $N^{1-\theta}\to0$；也满足所有有序对所需的 $>2$。

#### 例子 3：可运行 α 扫描骨架
```python
import random
import math

def hierarchical_distance(left, right, height):
    xor = left ^ right
    return 0 if xor == 0 else xor.bit_length()

def generate_hierarchical_graph(height=6, degree=5, alpha=1.0, seed=0):
    rng = random.Random(seed)
    n = 2 ** height
    adjacency = {node: set() for node in range(n)}
    for source in range(n):
        candidates = [node for node in range(n) if node != source]
        weights = [2 ** (-alpha * hierarchical_distance(source, node, height))
                   for node in candidates]
        for _ in range(degree):
            target = rng.choices(candidates, weights=weights, k=1)[0]
            index = candidates.index(target)
            adjacency[source].add(target)
            candidates.pop(index); weights.pop(index)
    return adjacency

def greedy_search(adjacency, source, target, height):
    current, steps = source, 0
    while current != target:
        neighbors = adjacency[current]
        if not neighbors:
            return None
        next_node = min(neighbors,
                        key=lambda node: hierarchical_distance(node, target, height))
        if hierarchical_distance(next_node, target, height) >= hierarchical_distance(current, target, height):
            return None
        current, steps = next_node, steps + 1
    return steps

def evaluate(alpha, height=6, degree=5, pairs=200, seed=0):
    graph = generate_hierarchical_graph(height, degree, alpha, seed)
    rng, n = random.Random(seed + 1), 2 ** height
    lengths = []
    for _ in range(pairs):
        source, target = rng.sample(range(n), 2)
        length = greedy_search(graph, source, target, height)
        if length is not None:
            lengths.append(length)
    return len(lengths) / pairs, (sum(lengths) / len(lengths) if lengths else math.nan)

for alpha in (0.2, 1.0, 3.0):
    success, conditional_length = evaluate(alpha, seed=7)
    print(alpha, round(success, 3), round(conditional_length, 3))
# 输出每个 alpha 的成功率与“仅成功搜索”的条件平均长度。
```

#### 正式 Q3.2 升级
- 参数替换为 `height=10, degree=5`。
- $\alpha=0.1,0.2,\ldots,10.0$ 共 100 个值。
- 每个 $\alpha$ 新建网络并抽 1000 个唯一有序对。
- 分别绘制成功率和成功条件下平均路径；失败不能作为 0 长度混入。
- 至少再跑 3 个图 seed，确认曲线形状不是单个随机图偶然。

### 8. 常见误区和易混概念
- 壳层计数写成 $b^d$：漏减含 $v$ 的子树。
- $e^{-a\log_bN}$ 直接写 $N^{-a}$：漏换底因子 $1/\ln b$。
- 从单节点失败界直接说“所有节点”：必须 union bound 并检查 $\theta>1$。
- 把无放回抽样当独立：本证明使用“未命中条件下成功概率不降”得到乘积上界。
- 只报成功路径均值：必须同时报告成功率。

| 层次 | 事件 | 概率/步数 |
| :--- | :--- | :--- |
| 单边 | 命中目标下一层子树 | $\ge1/(b\log_bN)$ |
| 单节点 $k$ 边 | 无进步边 | $\le N^{-\theta}$ |
| 固定目标全节点 | 任一节点无进步边 | $\le N^{1-\theta}$ |
| 搜索路径 | 每步严格降层 | $O(\log_bN)$ |

### 9. 相关知识点与 Obsidian 双链建议
- 上游：[[小世界与去中心化搜索]]。
- 横向：[[随机网络模型-ER-WS-BA-配置模型]]。
- 实验：[[../06-表示学习与项目/可复现网络挖掘实验]]。
- 作业：CS224W 2017 HW1-Q3.1(a–e)、Q3.2。

### 10. 闭卷复现任务
- [ ] 推出壳层计数。
- [ ] 推出 $Z$ 上界。
- [ ] 算 $T'$ 叶子数。
- [ ] 推出单边命中下界。
- [ ] 用指数界处理 $k$ 条边。
- [ ] 正确换对数底得到 $\theta$。
- [ ] 做固定目标 union bound。
- [ ] 推出搜索步数。
- [ ] 实现 α 扫描。
- [ ] 同时报成功率与条件长度。

### 11. 自测题：5 道
1. 恰距 $d$ 的叶子为何不是 $b^d$？ #自测题/基础
   > [!question]- 要减去与 $v$ 同处高度 $d-1$ 子树的 $b^{d-1}$ 个叶子。
2. $T'$ 为什么含 $b^{d-1}$ 个叶子？ #自测题/基础
   > [!question]- 它是完全 $b$ 叉树中高度 $d-1$ 的子树。
3. $\theta$ 为什么含 $\ln b$？ #自测题/中等
   > [!question]- $\log_bN=\ln N/\ln b$，把指数写成 $N$ 的幂必须换底。
4. 固定目标下“所有节点有进步边”需要什么条件？ #自测题/中等
   > [!question]- union bound 上界 $N^{1-\theta}\to0$，需 $\theta>1$。
5. 为什么 α 实验必须同时画两条曲线？ #自测题/较难
   > [!question]- 条件平均路径排除失败，只有结合成功率才能判断模型是否真正可导航。

### 12. 我的主动回忆区
#### 我的闭卷复述
> 用“壳层计数—单层命中—指数压尾—union bound—距离下降”五步复述证明。
#### 我的推导复现
> 不看笔记推出 $p,k,\theta$ 及固定目标的全节点失败界。
#### 我的错误与卡点
- [ ] $\theta$ 错 → 检查对数换底。
- [ ] 高概率范围说大了 → 明确固定节点、固定目标还是所有节点对。
- [ ] 仿真均值异常低 → 检查是否把失败当 0。
#### 失败后的回流
- 计数错：第 5.2 节；概率错：第 5.4–5.5 节；步数错：第 5.6 节；代码错：第 7.3 节。

### 13. 给 Obsidian 的归档建议
- 文件夹：`02-网络结构与生成模型/`
- 关联：[[小世界与去中心化搜索]]
- 标签：`#HW1` `#概率证明` `#去中心化搜索`
- 拆分建议：五个证明子题构成单一依赖链，保持一张推导卡。

### 🃏 Anki 卡片
- 层次搜索单边进入目标下一层子树的概率下界？::$1/(bZ)\ge1/(b\log_bN)$。
- $k=c(\log_bN)^2$ 时无进步边概率指数？::$N^{-\theta}$，其中 $\theta=c/(b\ln b)$。
- 为什么搜索只需 $O(\log_bN)$ 步？::层次距离是至多 $\log_bN$ 的非负整数，每步严格下降至少 1。
