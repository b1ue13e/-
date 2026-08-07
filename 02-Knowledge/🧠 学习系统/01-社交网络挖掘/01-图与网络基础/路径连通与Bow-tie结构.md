---
type: study
topic: "路径连通与 Bow-tie 结构"
course: "社交网络挖掘"
tags: [学习, 01-社交网络挖掘]
created: 2026-08-06
status: ongoing
difficulty: intermediate
concept: [路径连通与 Bow-tie 结构]
prerequisites: [图与网络基础, Python基础]
related: []
flow: knowledge
kind: concept
stage_moc: "[[🧭 阶段1-图与网络基础]]"
source: "合并自课程内已有笔记；原始来源见各节"
source_url: "https://snap.stanford.edu/class/cs224w-2017/handouts.html"
accessed: 2026-08-06
license: "课程讲义与题面默认 link-only；原论文按其页面条款使用"
assessment_exempt: false
verification_status: "概念与示例已合并；抽样实验需按数据版本复现"
---

# 路径连通与 Bow-tie 结构：概念与抽样实验

> **阅读顺序**：先掌握 BFS、连通分量和可达性，再进入 Bow-tie 分区与抽样估计。抽样实验尚未形成正式数据结果，因此本卡保持 `ongoing`。

## 原笔记：路径连通与Bow-tie结构

### 0. 学习边界

- **类别**：**A 类（核心算法与作业主线）**。
- **判断理由**：BFS 是连通分量、最短路、介数近似和传播模拟的共同底座；有向网络的 Bow-tie 结构是 HW1 的完整大题。

### 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：知道直接邻居还不够。我们需要回答“能否沿关系到达”“最少经过几步”“网络被分成哪些可达区域”。

### 2. 为什么它重要？它有什么用？

- **连接大图景**：BFS 产生无权最短路层；SCC 描述循环可达核心；Bow-tie 描述有向网络宏观可达结构。
- **实际应用场景**：网页爬取范围、消息能否传播、供应链可达性、账户资金路径。
- **高频任务**：WCC/SCC、前向/后向 BFS、随机节点对可达概率、Bow-tie 区域大小。

### 3. 学它之前需要哪些前置知识？

1. **[[图与网络基础]]**：邻接表与路径。
2. **[[有向网络统计与数据清洗]]**：方向与反向图。

### 4. 用直觉语言解释它

> “BFS 像水波逐层扩散；SCC 是从任何点出发都能绕回来的一座岛。”

- **直觉类比**：前向 BFS 顺箭头走，后向 BFS 在反向图走。
- **为什么自然**：队列保证先发现的层就是最短步数。
- **一句话直觉本质**：连通性是“路径是否存在”，距离是“最短路径有多长”。

### 5. 正式定义、核心公式、符号解释

#### 1. 最核心定义

路径是顶点序列 $(v_0,\ldots,v_k)$，每个相邻节点对都有边；长度为 $k$。有向图中，若 $u\leadsto v$ 且 $v\leadsto u$，二者强连通。

#### 2. 核心公式

无权最短路距离：
$$d(s,v)=\min\{k:\exists\text{ 长度 }k\text{ 的 }s\to v\text{ 路径}\}.$$

BFS 时间复杂度（邻接表）：$O(|V|+|E|)$。

#### 3. 符号说明表

| 符号 | 含义 | 备注 |
| :--- | :--- | :--- |
| $u\leadsto v$ | $u$ 可达 $v$ | 有向路径存在 |
| WCC | 弱连通分量 | 忽略方向后连通 |
| SCC | 强连通分量 | 分量内两两互达 |
| IN/OUT | 能到核心/可由核心到达 | Bow-tie 主翼 |

#### 4. 常见变体与适用条件

- BFS 只保证无权图最短路；非负加权图用 Dijkstra。
- Bow-tie 常分为 SCC、IN、OUT、TENDRILS/TUBES 和 DISCONNECTED。
- 实际网络可能有多个 SCC；Bow-tie 通常围绕最大 SCC 定义。

### 6. 推导思路和思想来源

- **最初困难**：DFS 能找可达点，但其发现顺序不保证最短路层。
- **关键“转念”**：先处理所有距离 $k$ 的点，再进入距离 $k+1$。
- **推导主线**：队列存储边界；首次发现节点时记录父节点与距离；每条边最多检查一次。
- **Bow-tie 构造**：取最大 SCC 为核心；反向可达核心但核心不可达的是 IN；核心可达但不能回到核心的是 OUT；其余在最大 WCC 中的节点为 tendrils/tubes。
- **为什么自然**：前向与后向可达集合的交、差直接刻画方向角色。

### 7. 例子：基础 → 中等 → 实际应用

#### 例子 1：基础例子（可手算）

- **题目**：有向边 $(1,2),(2,3),(3,2),(3,4),(5,1)$。
- **最终答案**：最大 SCC 为 $\{2,3\}$；IN 为 $\{1,5\}$；OUT 为 $\{4\}$；从 5 到 4 的最短路长度为 4。
- **易错点**：节点 1 能到 SCC，但 SCC 不能回到 1，因此 1 属于 IN 而不是 SCC。
- **🤔 追问**：删除 $(3,4)$ 后，4 变为 disconnected（若无其他边）。

#### 例子 2：中等例子（条件判断与多步推理）

对随机起点分别做前向、后向 BFS：若覆盖规模呈明显“双峰”，常暗示存在巨型可达核心；但仅凭有限样本估计区域大小必须报告抽样误差。

#### 例子 3：实际应用例子（真实场景/代码）

```python
from collections import deque

adjacency = {1: [2], 2: [3], 3: [2, 4], 4: [], 5: [1]}

def bfs_distances(graph, source):
    distance = {source: 0}
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in distance:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return distance

print(bfs_distances(adjacency, 5))
# 输出：{5: 0, 1: 1, 2: 2, 3: 3, 4: 4}
```

### 8. 常见误区和易混概念

#### 误区 1：WCC 内任意两点都可按方向互达

- **为什么错**：WCC 先忽略方向。
- **正确理解**：只有 SCC 才保证有向双向可达。

#### 概念对比表

| 概念 | 核心问题 | 关键区别 | 使用场景 |
| :--- | :--- | :--- | :--- |
| BFS | 无权最短路与可达层 | 队列、逐层 | 距离、介数 |
| DFS | 深入探索与结构分解 | 栈/递归 | SCC、拓扑性质 |
| WCC | 忽略方向是否连通 | 弱条件 | 粗粒度组件 |
| SCC | 是否两两互达 | 强条件 | 有向核心 |

### 9. 相关知识点与 Obsidian 双链建议

#### 上游依赖
- [[有向网络统计与数据清洗]]：正确方向是可达性的前提。

#### 下游延伸
- [[小世界与去中心化搜索]]：从可达性进入路径效率。
- [[边介数与Brandes近似]]：BFS DAG 用于边介数依赖递推。

#### 横向关联
- [[SIR网络流行病模型]]：传播过程受可达结构上界约束。

#### 应用场景
- HW0 最大 WCC；HW1 Epinions/Email Bow-tie。

### 10. 闭卷复现任务

- [ ] 定义路径、可达、WCC、SCC。
- [ ] 写出 BFS 队列算法与复杂度。
- [ ] 解释为何首次发现给出无权最短距离。
- [ ] 手算例 1 的五个 Bow-tie 区域。
- [ ] 用反向图解释后向 BFS。
- [ ] 区分 BFS 与 DFS。
- [ ] 解释随机 BFS 覆盖分布如何提示巨型核心。
- [ ] 说明加权图为何不能直接用 BFS。
- [ ] 复现代码。
- [ ] 设计一个随机节点对可达概率估计实验。

### 11. 自测题：5 道

1. WCC 与 SCC 的区别是什么？ #自测题/基础
   > [!question]- 答案解析
   > WCC 忽略方向后连通；SCC 要求分量内节点沿方向两两互达。
2. BFS 的时间复杂度为何是 $O(n+m)$？ #自测题/基础
   > [!question]- 答案解析
   > 每个节点入队至多一次，每条邻接边检查至多一次。
3. 节点能到核心但核心不能回到它，属于哪个区域？ #自测题/中等
   > [!question]- 答案解析
   > IN。
4. 如何用两次 BFS 判断节点是否属于给定 SCC？ #自测题/中等
   > [!question]- 答案解析
   > 从节点在原图和反向图分别搜索；与核心代表点双向可达才属于同一 SCC。
5. 为什么用 100 个随机起点估计 Bow-tie 区域会有偏差？ #自测题/较难
   > [!question]- 答案解析
   > 区域大小、度和可达范围影响抽样覆盖；有限样本有方差，且由 BFS 覆盖反推区域需要额外结构假设。

### 12. 我的主动回忆区

#### 我的闭卷复述
> 画出 Bow-tie 并写出各区域的可达关系。

#### 我的推导复现
> 证明 BFS 首次发现的距离最短。

#### 我的错误与卡点
- [ ] BFS 距离错 → 检查“入队即标记”与逐层队列。
- [ ] WCC/SCC 混淆 → 在反向图重做双向可达。
- [ ] Bow-tie 区域数不守恒 → 用[[路径连通与Bow-tie结构#原笔记：Bow-tie抽样估计与可达率实验]]的集合分区核对。
#### 失败后的回流
- BFS：第 5–7 节；Bow-tie 实验：[[路径连通与Bow-tie结构#原笔记：Bow-tie抽样估计与可达率实验]]。

#### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

### 13. 给 Obsidian 的归档建议

- **适合文件夹**：`01-图与网络基础/`
- **关联已有笔记**：[[图与网络基础]]、[[小世界与去中心化搜索]]
- **建议标签**：`#学习` `#BFS` `#连通性`
- **拆分建议**：BFS 与 Bow-tie 在作业中高度耦合，保持同一卡。

### 🃏 Anki 卡片

- Bow-tie 结构中的 IN 与 OUT 如何定义？::IN 能到达最大 SCC 但不能由 SCC 到达；OUT 可由 SCC 到达但不能返回 SCC。
- 为什么 BFS 给出无权最短路？::它按距离层逐层扩展，节点第一次被发现时不存在更短但尚未处理的路径。

## 原笔记：Bow-tie抽样估计与可达率实验

### 0. 学习边界
- **类别**：A 类作业实验。
- **判断理由**：知道 IN/OUT 定义不足以完成 HW1；还需从双向 BFS 样本画 CDF、估计区域规模，并单独估计全图/WCC 的有向可达率。

### 1. 这个知识点解决什么问题？
> 如何把 100 个随机起点的前向/后向覆盖规模转成可解释分布，并用精确 SCC 分区或抽样估计回答 Bow-tie 区域与随机节点对可达概率？

### 2. 为什么它重要？它有什么用？
- 训练从算法输出到统计估计的完整链。
- 区分“弱连通”与“按方向可达”。
- 对应 HW1-Q2.1–Q2.4 的四类交付物。

### 3. 学它之前需要哪些前置知识？
1. [[路径连通与Bow-tie结构]]。
2. 经验 CDF、均匀抽样与标准误。

### 4. 用直觉语言解释它
> “从不同入口放水并记录覆盖量；向前/向后覆盖的大小组合，暴露入口处在核心、入口翼还是出口翼。”
- **一句话本质**：双向可达集合是有向角色的指纹，CDF 展示随机起点看到的覆盖分布。

### 5. 正式定义、核心公式、符号解释

#### 1. 双向覆盖
$F(v)=\{u:v\leadsto u\}$，$B(v)=\{u:u\leadsto v\}$。对最大 SCC 中任一代表 $c$：
$$C=F(c)\cap B(c),\quad IN=B(c)\setminus F(c),\quad OUT=F(c)\setminus B(c).$$
在最大 WCC 内其余节点为 tendrils/tubes；最大 WCC 外为 disconnected。

#### 2. 经验 CDF
覆盖样本 $x_1,\ldots,x_r$ 的经验 CDF：
$$\widehat F(x)=\frac1r\sum_{i=1}^r\mathbb I[x_i\le x].$$
绘图应排序样本，以纵轴 `1/r,2/r,...,1` 作阶梯线。

#### 3. 可达率估计
均匀独立抽取有序对 $(s,t),s\ne t$：
$$\hat p=\frac1R\sum_{r=1}^R\mathbb I[t_r\in F(s_r)],\qquad
SE(\hat p)\approx\sqrt{\hat p(1-\hat p)/R}.$$
全图与最大 WCC 要分别定义抽样框；WCC 内抽样不代表全图。

#### 4. 精确分区优先
若资源允许，先求全部 SCC 和缩点 DAG，得到精确区域；随机 BFS 样本用于复现题面行为与不确定性，而不是在可精确计算时强行猜区域大小。

### 6. 推导思路和思想来源
1. 核心节点前向覆盖含 SCC+OUT，后向覆盖含 SCC+IN。
2. IN 节点常有大前向、小后向；OUT 相反；tendril 两者通常较小。
3. 覆盖规模可能双峰，CDF 比均值更能显示混合角色。
4. 可达率是 Bernoulli 均值，可报告标准误或 Wilson 区间。
5. 用有序对是因为有向可达不对称。

### 7. 例子：已解 → 半提示 → 可运行骨架

#### 例子 1：已解
边 `5→1→2↔3→4`：核心 `{2,3}`，IN `{1,5}`，OUT `{4}`。从 5 前向覆盖 5、后向覆盖 1；从 4 前向覆盖 1、后向覆盖 5。

#### 例子 2：半提示
若随机点的前向覆盖 CDF 在小值与接近 $n$ 处各有质量，而后向类似，解释可能角色混合。
> [!question]- 核对
> 大前向常对应 IN/核心，大后向常对应 OUT/核心；两者都小常对应 tendril/disconnected，需结合 WCC/SCC 才能定类。

#### 例子 3：可运行实验函数
```python
import random
import networkx as nx

def reachable(graph, source, reverse=False):
    target = graph.reverse(copy=False) if reverse else graph
    return set(nx.descendants(target, source)) | {source}

def bow_tie_regions(graph):
    core = max(nx.strongly_connected_components(graph), key=len)
    representative = next(iter(core))
    forward = reachable(graph, representative)
    backward = reachable(graph, representative, reverse=True)
    weak = max(nx.weakly_connected_components(graph), key=len)
    inside = set(core)
    region_in = backward - forward
    region_out = forward - backward
    tendrils = set(weak) - inside - region_in - region_out
    disconnected = set(graph) - set(weak)
    return inside, region_in, region_out, tendrils, disconnected

def ecdf(values):
    ordered = sorted(values)
    n = len(ordered)
    return ordered, [(index + 1) / n for index in range(n)]

def reachability_rate(graph, trials=1000, seed=0, nodes=None):
    rng = random.Random(seed)
    population = list(nodes if nodes is not None else graph.nodes())
    success = 0
    for _ in range(trials):
        source, target = rng.sample(population, 2)
        success += target in reachable(graph, source)
    rate = success / trials
    standard_error = (rate * (1 - rate) / trials) ** 0.5
    return rate, standard_error

graph = nx.DiGraph([(5,1),(1,2),(2,3),(3,2),(3,4),(10,11)])
regions = bow_tie_regions(graph)
assert regions == ({2,3}, {1,5}, {4}, set(), {10,11})
sizes = [len(reachable(graph, node)) for node in graph]
print([len(part) for part in regions], ecdf(sizes), reachability_rate(graph, 500, 7))
# 输出区域大小、覆盖 ECDF 点与可达率估计/标准误。
```

#### 正式实验协议
- 分别加载官方 [soc-Epinions1](https://snap.stanford.edu/data/soc-Epinions1.html) 与 [email-EuAll](https://snap.stanford.edu/data/email-EuAll.html) 为 `DiGraph`；signed Epinions 是另一数据集，不能替代。
- 在知识库根目录运行 `python 99-System/tools/smoke_test_social_network_datasets.py --dataset soc-epinions1`，先通过行数、节点数、方向度数和 SCC/WCC smoke。
- 固定候选节点全集，均匀无放回抽 100 个起点；前向/后向 BFS 各记录覆盖数。
- 四张 CDF：两网络 × 两方向；轴与样本数一致。
- 区域规模用精确 SCC/WCC 分区交叉验证题面抽样推断。
- 可达率至少 100 对；建议 1000+，分别全图与最大 WCC，报告 seed、试验数、$\hat p$、标准误。

### 8. 常见误区和易混概念
- 把 BFS 访问顺序当 CDF：CDF 的变量是覆盖节点数，不是 BFS 层。
- 从同一小批起点重复抽目标：会低估起点层面的方差。
- 把无序节点对用于有向可达：$(s,t)$ 与 $(t,s)$ 不是同一事件。
- tendrils 简化成“WCC 剩余”时要声明 tubes 也被合并在内。

| 量 | 抽样单位 | 回答的问题 |
| :--- | :--- | :--- |
| 前向覆盖 | 起点 | 能影响多少节点 |
| 后向覆盖 | 起点 | 多少节点能影响它 |
| 全图可达率 | 有序节点对 | 任意两点有路概率 |
| WCC 可达率 | WCC 内有序对 | 排除弱断连后的方向障碍 |

### 9. 相关知识点与 Obsidian 双链建议
- 上游：[[路径连通与Bow-tie结构]]。
- 横向：[[小世界与去中心化搜索]]。
- 下游：[[边介数与Brandes近似]]。
- 作业：CS224W 2017 HW1-Q2.1–Q2.4。

### 10. 闭卷复现任务
- [ ] 写出 $F(v),B(v)$。
- [ ] 从核心代表构造五区。
- [ ] 写经验 CDF。
- [ ] 区分全图/WCC 抽样框。
- [ ] 写可达率与标准误。
- [ ] 解释覆盖双峰。
- [ ] 运行 toy graph 分区。
- [ ] 设计 100 起点实验。
- [ ] 设计至少 100 对可达实验。
- [ ] 报告抽样不确定性。

### 11. 自测题：5 道
1. IN 节点相对核心的可达关系？ #自测题/基础
   > [!question]- 能到核心，但核心不能返回该节点。
2. 经验 CDF 的纵坐标是什么？ #自测题/基础
   > [!question]- 样本中不超过给定覆盖规模的比例。
3. 为什么可达率要抽有序对？ #自测题/中等
   > [!question]- 有向路径不对称，反转端点可能改变事件。
4. WCC 内可达率为何通常高于全图？ #自测题/中等
   > [!question]- 排除了弱不连通导致必然不可达的跨分量节点对。
5. 区域规模为何优先用精确 SCC 缩点图？ #自测题/较难
   > [!question]- 抽样覆盖反推依赖结构假设且有方差；SCC/WCC 可直接得到精确集合。

### 12. 我的主动回忆区
#### 我的闭卷复述
> 画 Bow-tie，并用前向/后向覆盖解释每类起点的典型指纹。
#### 我的推导复现
> 重建 ECDF、可达率与标准误；写出全图和 WCC 两套抽样框。
#### 我的错误与卡点
- [ ] 区域错 → 回到第 5.1 节画可达集合。
- [ ] CDF 轴错 → 回到第 5.2 节。
- [ ] 可达率不稳定 → 增加有序对数并报告标准误。
#### 失败后的回流
- 算法错：[[路径连通与Bow-tie结构]]；统计错：第 5.2–5.3 节；实验错：第 7.3 节。

### 13. 给 Obsidian 的归档建议
- 文件夹：`01-图与网络基础/`
- 关联：[[路径连通与Bow-tie结构]]
- 标签：`#HW1` `#BowTie` `#抽样`
- 拆分建议：CDF、区域与可达率共享双向 BFS 结果，保留一张实验卡。

### 🃏 Anki 卡片
- Bow-tie 抽样为什么同时做前向和后向 BFS？::两种覆盖分别测“我能到谁”和“谁能到我”，组合后区分 SCC、IN、OUT 等方向角色。
- 有向可达率的抽样单位？::均匀有序节点对 $(s,t)$；全图与最大 WCC 必须分别定义抽样框。

## 🧪 学完本节后可完成的作业

- **可立即完成**：[[社交网络挖掘-课后作业-02-结构生成与去中心化搜索#2. 非 Web 网络的 Bow-tie 结构（30 分，Silviana、Ziyi）|课后作业 02 题 2]]。
- **为什么现在能做**：已覆盖前向/反向 BFS、WCC/SCC、Bow-tie 区域与有序对可达率。
- **提交产物**：区域集合、守恒检查、ECDF、抽样框与标准误。

