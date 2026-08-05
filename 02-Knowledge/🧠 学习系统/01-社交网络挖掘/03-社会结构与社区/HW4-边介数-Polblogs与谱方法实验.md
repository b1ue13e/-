---
type: study
topic: "HW4 边介数 Polblogs 与谱方法"
tags: [学习, 01-社交网络挖掘]
created: 2026-08-06
status: ongoing
difficulty: intermediate
concept: [HW4 边介数 Polblogs 与谱方法]
prerequisites: [图与网络基础, Python基础]
related: []
flow: knowledge
kind: problem-type
source: "合并自课程内已有笔记；原始来源见各节"
verification_status: "题面与示例代码已合并；正式数据与结果需复现"
---

# HW4：边介数、Polblogs 与谱方法实验

> **阅读顺序**：先实现单源 Brandes 依赖与近似边介数，再处理 Polblogs 数据和两类谱松弛。玩具图只能验证算法分支，不能代替正式数据结果。

## 原笔记：HW4-边介数自适应近似与BA实验

### 0. 先判断它值不值得深挖
- **类别**：A 类算法实验。
- **判断理由**：固定 $k$ 抽样只覆盖概念；HW4 要求累计依赖阈值停止、最多 $n/10$ 个源点、全边排序曲线和运行时间比较。

### 1. 这个知识点解决什么问题？
> 怎样从精确全源 Brandes 切换到自适应源点抽样，在高介数边上尽早停止，并判断近似排序是否保留桥边结构？

### 2. 为什么它重要？它有什么用？
- 训练自适应停止与固定样本估计的区别。
- 将理论保证、排序图与实际运行时间统一验证。
- 覆盖 HW4-Q2 的实现与交付物。

### 3. 学它之前需要哪些前置知识？
1. [[边介数与Brandes近似]]。
2. [[../02-网络结构与生成模型/随机网络模型-ER-WS-BA-配置模型]]。

### 4. 用直觉语言解释它
> “每次随机选择一个观察站，累积它看到某条边承载的最短路需求；高负载边很快越过证据阈值。”
- **一句话本质**：抽样源点估计全源依赖，自适应阈值把预算集中到足以排序的边。

### 5. 正式定义、核心公式、符号解释

#### 1. 精确值
$$B(e)=\sum_{s\in V}\delta_s(e).$$
无向图若用有序源/终点口径，最终与某些库的无序口径差 2；排序不受统一倍数影响。

#### 2. HW4 自适应算法
对一条目标边 $e$，有放回均匀抽源点并维护
$$Z_e(k)=\sum_{i=1}^k\delta_{s_i}(e).$$
它自己的停止时间是
$$K_e=\min\{k:Z_e(k)>cn\},$$
若到 $n/10$ 个源仍未越阈值，则在上限处停止并标记为 capped。估计为
$$\widehat B(e)=\frac n{K_e}Z_e(K_e).$$

模拟要求估计所有边时，可以让同一次 BFS 同时更新所有仍活跃边，但**每条边独立停止**：某条高介数边越阈值只冻结该边，不能停止其他边。全局采样仅在所有边均已停止或达到 $n/10$ 上限时结束。

#### 3. 定理的尺度解释
若 $B(e)=n^2/t$，随机源单次依赖的期望为 $n/t$。要把累计量推到 $cn$，期望上约需 $ct$ 个样本；高介数（小 $t$）边更快获得稳定证据。该结论与停止时间都针对固定目标边；不能把先停止边的保证转移给尚未越阈值的其他边。正式概率保证依赖题面给定的 $\epsilon,t$ 表述，不可把期望解释冒充完整证明。

#### 4. 排序曲线
分别按精确/近似分数降序排列各自边；横轴为 rank，纵轴为分数，使用对数 y 轴。还应补充 top-k 重合与 Spearman 相关作为诊断，但不替代官方图。

#### 5. 时间比较
精确无权无向 Brandes 为 $O(nm)$；抽 $k$ 源为 $O(km)$，加排序 $O(m\log m)$。计时需同机、同图、排除首次 import，并明确是否包含生成/绘图。

### 6. 推导思路和思想来源
1. 单源依赖是全源和的可抽样分量。
2. 高介数边的单源期望贡献高，更快越过累计阈值。
3. 缩放 $n/k$ 恢复全源量级。
4. 排名比逐边绝对误差更贴近“找桥边”用途。
5. 自适应停止的估计偏差/保证须依题面定理分析，不能直接套固定 $k$ 无偏性。

### 7. 例子：已解 → 半提示 → 可运行实验

#### 例子 1：已解
若 $n=1000,c=5$，阈值为 5000；最多抽 100 个源。某边在 20 个样本后累计依赖 120，则缩放估计为 $1000/20\times120=6000$，但尚未越过累计阈值 5000，说明此数值例的 $Z$/阈值口径需区分“目标边累计”与“缩放后估计”。

#### 例子 2：半提示
精确 $O(nm)$，抽样 $k=n/10$ 时主项为 `____`，理想主项加速约 `____` 倍。
> [!question]- 核对
> $O(nm/10)$；约 10 倍，忽略常数和排序。

#### 例子 3：逐边停止的可运行 BA 实现
```python
import random
import time
from collections import defaultdict, deque
import networkx as nx

def edge_key(u, v):
    return tuple(sorted((u, v)))

def single_source_edge_dependencies(graph, source):
    predecessors = {node: [] for node in graph}
    sigma = dict.fromkeys(graph, 0.0)
    distance = dict.fromkeys(graph, -1)
    sigma[source], distance[source] = 1.0, 0
    queue, stack = deque([source]), []
    while queue:
        node = queue.popleft()
        stack.append(node)
        for neighbor in graph[node]:
            if distance[neighbor] < 0:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
            if distance[neighbor] == distance[node] + 1:
                sigma[neighbor] += sigma[node]
                predecessors[neighbor].append(node)

    node_dependency = dict.fromkeys(graph, 0.0)
    edge_dependency = defaultdict(float)
    while stack:
        child = stack.pop()
        for parent in predecessors[child]:
            share = (sigma[parent] / sigma[child]) * (1.0 + node_dependency[child])
            edge_dependency[edge_key(parent, child)] += share
            node_dependency[parent] += share
    return edge_dependency

def exact_edge_betweenness(graph):
    exact = {edge_key(*edge): 0.0 for edge in graph.edges()}
    for source in graph:
        for edge, value in single_source_edge_dependencies(graph, source).items():
            exact[edge] += value
    return exact

def adaptive_all_edges(graph, max_samples, threshold_c=5, seed=0):
    rng = random.Random(seed)
    nodes = list(graph)
    edges = {edge_key(*edge) for edge in graph.edges()}
    accumulated = dict.fromkeys(edges, 0.0)
    active = set(edges)
    estimate, sample_count = {}, {}

    samples_used = 0
    while samples_used < max_samples and active:
        source = rng.choice(nodes)
        contribution = single_source_edge_dependencies(graph, source)
        samples_used += 1
        for edge in active:
            accumulated[edge] += contribution.get(edge, 0.0)

        crossed = {edge for edge in active
                   if accumulated[edge] > threshold_c * len(nodes)}
        for edge in crossed:
            sample_count[edge] = samples_used
            estimate[edge] = len(nodes) * accumulated[edge] / samples_used
        active.difference_update(crossed)

    # Capped edges use all available samples and must be reported separately.
    for edge in active:
        sample_count[edge] = samples_used
        estimate[edge] = len(nodes) * accumulated[edge] / samples_used
    return estimate, sample_count, active, samples_used

graph = nx.barabasi_albert_graph(120, 4, seed=7)
start = time.perf_counter()
exact = exact_edge_betweenness(graph)
exact_time = time.perf_counter() - start
start = time.perf_counter()
approximate, stopped_at, capped, samples = adaptive_all_edges(graph, 12, seed=7)
approx_time = time.perf_counter() - start
library = nx.edge_betweenness_centrality(graph, normalized=False)
assert all(abs(exact[edge_key(*edge)] - 2 * value) < 1e-9
           for edge, value in library.items())
assert set(approximate) == {edge_key(*edge) for edge in graph.edges()}
assert set(stopped_at) == set(approximate)
assert all(1 <= count <= 12 for count in stopped_at.values())
top_exact = {edge for edge, _ in sorted(exact.items(), key=lambda item: item[1], reverse=True)[:10]}
top_approx = {edge for edge, _ in sorted(approximate.items(), key=lambda item: item[1], reverse=True)[:10]}
print(samples, len(capped), round(exact_time, 4),
      round(approx_time, 4), len(top_exact & top_approx))
# 输出全局 BFS 数、达到上限仍未越阈值的边数、时间和 top-10 重合数。
```

#### 正式作业参数
- BA：`n=1000,m_attach=4`。
- 精确算法应使用自己的单源依赖实现，不直接提交库函数。
- 近似：`c=5`，有放回源点，最多 `n/10`。
- 为每条边保存 `K_e` 与是否 capped；不得用第一条越阈值边的 $K_e$ 缩放全部边。
- 两条 rank-score 曲线叠加，y 轴 log；报告运行时间和差异解释。

### 8. 常见误区和易混概念
- 用节点介数：对象必须是边。
- 把自适应估计称为固定样本无偏：停止时间依赖数据，论证不同。
- 任一边越阈值就停止整个程序：这只估好了该目标边，其余边仍欠采样。
- 全部边共用最终 $k$，却称为 Algorithm 2：这是统一固定预算替代法，不能冒充逐边停止保证。
- 两条曲线共用精确排序：题面要求各算法诱导自己的排序。
- 库函数子集归一化不一致：用 toy graph 校准倍数。

| 方法 | 源点数 | 主复杂度 | 输出风险 |
| :--- | :--- | :--- | :--- |
| 精确 | $n$ | $O(nm)$ | 慢 |
| 固定抽样 | 固定 $k$ | $O(km)$ | 需选预算 |
| 自适应单边 | 目标边停止时间 $K_e$ | $O(K_em)$ | 停止时间论证 |
| 自适应全边共享 BFS | 最大活跃停止时间或上限 | $O(K_{max}m)$ | 每边必须保存自己的 $K_e$ |

### 9. 相关知识点与 Obsidian 双链建议
- 上游：[[边介数与Brandes近似]]。
- 横向：[[社区发现-模块度与谱松弛]]。
- 实验：[[../06-表示学习与项目/可复现网络挖掘实验]]。
- 作业：CS224W 2017 HW4-Q2。

### 10. 闭卷复现任务
- [ ] 写精确全源和。
- [ ] 写每条边的累计量与独立停止条件。
- [ ] 记录真实样本数。
- [ ] 解释 $n/k$ 缩放。
- [ ] 区分固定/自适应论证。
- [ ] 生成 BA 图。
- [ ] 实现精确/近似。
- [ ] 画各自排序曲线。
- [ ] 比较 top-k。
- [ ] 公平计时。

### 11. 自测题：5 道
1. 近似抽样单位是什么？ #自测题/基础
   > [!question]- 均匀有放回的源点。
2. 估计为何乘 $n/k$？ #自测题/基础
   > [!question]- 样本源贡献和只覆盖 $k$ 个源，缩放到 $n$ 个源量级。
3. 高介数边为何更快停止？ #自测题/中等
   > [!question]- 每个随机源对它的期望依赖更高，累计值增长更快。
4. 第一条边越阈值后为什么不能停止全部边？ #自测题/中等
   > [!question]- 阈值与保证针对目标边；其他边有各自的累计量和停止时间，可能仍严重欠采样。
5. 为什么自适应停止不能直接称固定样本无偏？ #自测题/较难
   > [!question]- 样本量取决于已观察贡献，固定样本量的线性期望论证不再直接适用。

### 12. 我的主动回忆区
#### 我的闭卷复述
> 对比精确、固定抽样和自适应抽样的源点数、缩放与风险。
#### 我的推导复现
> 从 $B(e)=\sum_s\delta_s(e)$ 推出抽样估计与复杂度。
#### 我的错误与卡点
- [ ] 分数差倍数 → 统一有序/无序口径。
- [ ] 提前/从不停止 → 检查阈值使用未缩放累计量，并查看每边自己的 $K_e$。
- [ ] 低介数边分数异常 → 检查是否被其他边的停止事件提前终止。
- [ ] 曲线不公平 → 各自独立排序。
#### 失败后的回流
- 递推错：[[边介数与Brandes近似]]；停止错：第 5.2–5.3 节；实验错：第 7.3 节。

### 13. 给 Obsidian 的归档建议
- 文件夹：`03-社会结构与社区/`
- 关联：[[边介数与Brandes近似]]
- 标签：`#HW4` `#近似算法` `#BA实验`
- 拆分建议：自适应停止和 BA 对比共同构成 Q2 实验，保持一张卡。

### 🃏 Anki 卡片
- HW4 目标边的停止时间？::$K_e=\min\{k:Z_e(k)>cn\}$，达到样本上限仍未越阈值则标为 capped。
- HW4 边介数近似的缩放？::$\widehat B(e)=\frac n{K_e}\sum_{i=1}^{K_e}\delta_{s_i}(e)$。
- 自适应停止的核心风险？::样本量依赖已观察贡献，固定样本无偏论证不能直接照搬。

## 原笔记：HW4-Polblogs谱聚类端到端实验

### 0. 先判断它值不值得深挖
- **类别**：A 类真实数据实验。
- **判断理由**：谱公式能跑 Karate 图不等于完成 Q4.4；真实实验的主要风险是节点 ID/标签错位、孤立点、矩阵行序与 purity 标签翻转。

### 1. 这个知识点解决什么问题？
> 如何安全加载政治博客边表与标签，使邻接矩阵行、节点 ID 和真值一一对应，再用 NCut 与模块度两种谱法二分并计算组规模和 purity？

### 2. 为什么它重要？它有什么用？
- 训练真实图数据到线性代数矩阵的索引契约。
- 区分算法簇编号与语义标签。
- 完整覆盖 HW4-Q4.4 的端到端交付。

### 3. 学它之前需要哪些前置知识？
1. [[社区发现-模块度与谱松弛]]。
2. [[../06-表示学习与项目/可复现网络挖掘实验#原笔记：NetworkX-SNAP环境与数据工作流]]。

### 4. 用直觉语言解释它
> “特征向量只给两堆编号，编号正负可以整体翻转；purity 要为每堆选择其多数真实标签，而不是把正号硬认作某党派。”
- **一句话本质**：谱坐标与数据行序必须锁定，簇标签需按多数类评价。

### 5. 正式定义、核心公式、符号解释

#### 1. 数据契约
- 边表每行 `(u,v)`，读为无向简单图；若任一方向有链接即视为无向边。
- 标签表每行 `(node_id,label)`；不能假设行号等于节点 ID。
- `nodes=sorted(graph.nodes())`，建立 `index={node:i}`；矩阵、预测与标签全部通过同一列表对齐。

#### 2. NCut 谱法
$$\mathcal L=I-D^{-1/2}AD^{-1/2}.$$
取第二小特征向量 $v_2$，按题面使用对应连续坐标符号二分。图应连通且无孤立点；若数据不满足，先按题面/官方数据核验，不静默删除。

#### 3. 模块度谱法
$$B=A-\frac{dd^T}{2m}.$$
取最大代数特征值对应向量按符号二分。

#### 4. Purity
对预测簇 $C_0,C_1$ 和真标签 $y$：
$$purity=\frac1n\sum_{c\in\{0,1\}}\max_{\ell}|\{i\in C_c:y_i=\ell\}|.$$
该定义自动处理特征向量整体符号翻转。

#### 5. 验收输出
每种算法报告：两簇大小、purity、NCut/模块度原始目标、零特征值/最大特征值、节点/标签缺失数。

### 6. 推导思路和思想来源
1. 图算法以节点 ID 工作，矩阵算法以行号工作；显式 `nodes` 列表是桥梁。
2. 特征向量方向不唯一，簇编号没有语义。
3. purity 对每簇取多数标签，避免强制全局标签匹配。
4. 同时报原始优化目标可发现“purity 高但未优化题面目标”或标签泄漏。

### 7. 例子：已解 → 半提示 → 可运行骨架

#### 例子 1：已解 purity
簇 A 有 8 个标签 0、2 个标签 1；簇 B 有 1 个标签 0、9 个标签 1。purity=$(8+9)/20=0.85$。

#### 例子 2：半提示
若整体翻转簇编号，purity 是否改变？为什么？
> [!question]- 核对
> 不改变；求和遍历所有簇且每簇只取多数真实标签。

#### 例子 3：可运行端到端函数
```python
from pathlib import Path
import numpy as np
import networkx as nx

def load_graph(edge_path):
    graph = nx.Graph()
    with Path(edge_path).open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip() or line.startswith("#"):
                continue
            left, right = map(int, line.split()[:2])
            if left != right:
                graph.add_edge(left, right)
    return graph

def load_labels(label_path):
    labels = {}
    with Path(label_path).open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip() or line.startswith("#"):
                continue
            node, label = map(int, line.split()[:2])
            labels[node] = label
    return labels

def load_newman_gml(gml_path):
    # The authors' GML is directed and contains duplicate arcs. Preserve them
    # during parsing, then apply HW4's undirected-simple projection explicitly.
    text = Path(gml_path).read_text(encoding="utf-8")
    text = text.replace("  directed 1\n", "  directed 1\n  multigraph 1\n", 1)
    raw = nx.parse_gml(text.splitlines(), label=None)
    graph = nx.Graph()
    graph.add_nodes_from(raw.nodes(data=True))
    graph.add_edges_from((u, v) for u, v in raw.edges() if u != v)
    largest = max(nx.connected_components(graph), key=len)
    graph = graph.subgraph(largest).copy()
    labels = {int(node): int(data["value"])
              for node, data in graph.nodes(data=True)}
    assert set(labels) == set(graph) and set(labels.values()) == {0, 1}
    return graph, labels

def purity(prediction, truth):
    score = 0
    for cluster in np.unique(prediction):
        values = truth[prediction == cluster]
        score += np.bincount(values).max()
    return score / len(truth)

def spectral_partitions(graph, labels):
    nodes = sorted(graph)
    missing = set(nodes) - set(labels)
    if missing:
        raise ValueError(f"缺少 {len(missing)} 个节点标签")
    adjacency = nx.to_numpy_array(graph, nodelist=nodes)
    degree = adjacency.sum(axis=1)
    if np.any(degree == 0):
        raise ValueError("存在孤立节点，需按数据契约处理")
    laplacian = np.diag(degree) - adjacency
    inv_sqrt = np.diag(1 / np.sqrt(degree))
    normalized = inv_sqrt @ laplacian @ inv_sqrt
    _, vectors = np.linalg.eigh(normalized)
    ncut_prediction = (inv_sqrt @ vectors[:, 1] >= 0).astype(int)
    m = graph.number_of_edges()
    modularity = adjacency - np.outer(degree, degree) / (2 * m)
    _, mod_vectors = np.linalg.eigh(modularity)
    modularity_prediction = (mod_vectors[:, -1] >= 0).astype(int)
    truth = np.array([labels[node] for node in nodes], dtype=int)
    return {
        "ncut": (np.bincount(ncut_prediction).tolist(), purity(ncut_prediction, truth)),
        "modularity": (np.bincount(modularity_prediction).tolist(), purity(modularity_prediction, truth)),
    }

graph = nx.karate_club_graph()
labels = {node: int(graph.nodes[node]["club"] == "Officer") for node in graph}
print(spectral_partitions(graph, labels))
# 输出两种谱法的簇规模与 purity；正式实验替换为 polblogs 文件。
```

#### 正式数据步骤
1. Stanford HW4 PDF 给出的 `polblogs.txt`/`polblogs-labels.txt` 原链接当前返回 404，不得声称已从该镜像复现。
2. 可使用数据作者 Adamic 与 Glance 的 [Polblogs 原始公开数据](https://public.websites.umich.edu/~mejn/netdata/) 作为透明替代：压缩包 SHA-256 为 `e047...1ddb`，并按随附说明引用原论文。
3. 原始 GML 有 1490 节点、19090 条有向弧且包含重复弧。按题面投影为无向简单图并取最大连通分量后，验收规模为 1222 节点、16714 边；不能直接让 `nx.read_gml` 静默失败或随意删节点。
4. 检查 `set(graph)==set(labels)`，保存显式节点顺序；用稀疏 `eigsh` 运行 NCut 与模块度，检查特征对残差、两簇非空、簇大小和 purity。
5. 先在 PowerShell 执行 `Set-Location 'F:\-'`，再运行 `python 99-System/tools/smoke_test_polblogs.py --download --manifest 99-System/.tmp/social-network-course-audit/data/polblogs-manifest.json`。manifest 位于忽略目录，只作复现证据，不把生成结果抄成官方答案。

### 8. 常见误区和易混概念
- 用标签文件行号索引矩阵：节点 ID 可能不连续/不按序。
- 把正特征向量项固定解释为标签 1：整体符号可反转。
- 用最大绝对值模块度特征向量：应取最大代数特征值。
- 调阈值以最大化测试 purity：造成标签泄漏；题面使用符号 rounding。
- 直接用 `nx.read_gml` 读取作者文件：重复有向弧会报错；必须先按 `MultiDiGraph` 解析，再显式投影。
- 把作者原始 GML 与失效的 Stanford 预处理文本称为同一文件：来源、预处理和哈希必须分别记录。

| 层 | 不变量 | 失败表现 |
| :--- | :--- | :--- |
| 文件 | ID 集一致 | 缺标签/多标签 |
| 矩阵 | 行序=`nodes` | purity 异常 |
| 谱法 | 对称矩阵/eigh | 复数/排序错 |
| 评价 | 簇多数标签 | 符号翻转敏感 |

### 9. 相关知识点与 Obsidian 双链建议
- 上游：[[社区发现-模块度与谱松弛]]。
- 横向：[[社区发现-模块度与谱松弛]]。
- 实验：[[../06-表示学习与项目/可复现网络挖掘实验]]。
- 作业：CS224W 2017 HW4-Q4.4。

### 10. 闭卷复现任务
- [ ] 写数据契约。
- [ ] 显式节点顺序。
- [ ] 对齐标签。
- [ ] 实现 NCut 谱法。
- [ ] 实现模块度谱法。
- [ ] 写 purity。
- [ ] 处理符号翻转。
- [ ] 报簇大小。
- [ ] 报优化目标。
- [ ] 记录哈希与版本。

### 11. 自测题：5 道
1. 为什么要保存 `nodes` 列表？ #自测题/基础
   > [!question]- 它定义矩阵行、预测数组和标签数组的共同索引契约。
2. purity 如何处理簇编号翻转？ #自测题/基础
   > [!question]- 每簇独立取多数真实标签，编号交换不改变总和。
3. NCut 使用哪个矩阵？ #自测题/中等
   > [!question]- 对称归一化拉普拉斯 $D^{-1/2}LD^{-1/2}$。
4. 模块度使用哪个谱方向？ #自测题/中等
   > [!question]- $B=A-dd^T/(2m)$ 的最大代数特征值对应向量。
5. 为什么不能用测试标签调 rounding 阈值？ #自测题/较难
   > [!question]- 会把评价标签泄漏进算法选择，purity 不再是独立评估。

### 12. 我的主动回忆区
#### 我的闭卷复述
> 用“文件 ID—节点顺序—矩阵—预测—标签”复述对齐链。
#### 我的推导复现
> 重写两种谱矩阵和 purity，解释符号翻转不影响评价。
#### 我的错误与卡点
- [ ] 缺标签 → 比较 ID 集。
- [ ] purity 异常 → 检查 `nodes` 顺序。
- [ ] 二分反了 → 这是允许的，检查 purity 是否不变。
#### 失败后的回流
- 理论错：[[社区发现-模块度与谱松弛]]；数据错：第 5.1 节；代码错：第 7.3 节。

### 13. 给 Obsidian 的归档建议
- 文件夹：`03-社会结构与社区/`
- 关联：[[社区发现-模块度与谱松弛]]
- 标签：`#HW4` `#Polblogs` `#谱实验`
- 拆分建议：数据对齐与两种算法共享矩阵索引，保持一张实验卡。

### 🃏 Anki 卡片
- Polblogs 谱实验最关键的数据不变量？::邻接矩阵行顺序、预测数组与标签数组必须共享同一显式节点 ID 列表。
- 二分 purity 如何定义？::$n^{-1}\sum_c\max_\ell|\{i\in C_c:y_i=\ell\}|$。
