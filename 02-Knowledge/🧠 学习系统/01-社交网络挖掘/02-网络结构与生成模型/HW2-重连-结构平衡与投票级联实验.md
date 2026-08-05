---
type: study
topic: "HW2 重连结构平衡与投票级联"
tags: [学习, 01-社交网络挖掘]
created: 2026-08-06
status: ongoing
difficulty: intermediate
concept: [HW2 重连结构平衡与投票级联]
prerequisites: [图与网络基础, Python基础]
related: []
flow: knowledge
kind: problem-type
source: "合并自课程内已有笔记；原始来源见各节"
verification_status: "题面与示例代码已合并；正式作业参数需复现"
---

# HW2：重连、结构平衡与投票级联实验

> **阅读顺序**：保度重连解决结构随机化，符号网络部分处理平衡性证明，投票级联部分处理动态过程。三部分共用 HW2 题面，但验收证据必须分别记录。

## 原笔记：HW2-保度重连与投票级联实验

### 0. 先判断它值不值得深挖
- **类别**：A 类作业实验。
- **判断理由**：重连要逐次保持简单图与度序列；投票要严格复现轮次、tie 和预算。任何口径漂移都会改变曲线或赢家。

### 1. 这个知识点解决什么问题？
> 怎样实现可审计的双边交换，观察聚类向配置基线衰减；又怎样在同一图上公平比较定向广告与高度节点干预？

### 2. 为什么它重要？它有什么用？
- 把“保度随机化”落实为可验证 Markov 链。
- 把官方投票规则落实为可审计的顺序状态机与预算实验。
- 覆盖 HW2-Q1.2、Q3.1–Q3.4。

### 3. 学它之前需要哪些前置知识？
1. [[随机网络模型-ER-WS-BA-配置模型]]。
2. [[../05-传播与影响力/阈值模型与网络级联]]。

### 4. 用直觉语言解释它
> “重连像交换两条电话线的端点：每人线路数不变，但朋友圈三角形被逐渐打散；干预则是在相同规则下只改变初始支持者。”
- **一句话本质**：控制度序列或预算，随机化/改变其余因素。

### 5. 正式定义、核心公式、符号解释

#### 1. 简单图双边交换
随机取两条不同边 $(u,v),(w,x)$，随机定向端点后候选为 $(u,w),(v,x)$。仅当四端点与新边满足：无自环、无已有边、两新边不同，才删除旧边并加入新边。

#### 2. 不变量
每个涉及节点失去一条边又获得一条边，所以度数不变；成功交换前后 $m$ 不变。拒绝交换不计为成功，但可计为尝试。

#### 3. 聚类轨迹
每 100 次**尝试或成功交换**记录一次必须预先声明。HW2 题面以迭代过程为口径；同时报告接受率，便于解释横轴。

#### 4. HW2 官方投票状态机
- 节点 ID 末位 `0-3` 是坚定 A，`4-7` 是坚定 B，`8-9` 是最初未决定者。
- 只有“最初未决定且未被广告冻结”的节点在 10 轮中反复更新；坚定选民永不改变。
- 每轮按节点 ID 递增处理，并**原地更新**。处理节点 $u$ 时，小于 $u$ 且本轮已处理节点使用新状态，其余节点使用当前保存状态。
- 只统计邻居当前的 A/B，第一轮尚未决定的邻居忽略。
- A/B 数相等时使用一个全网络共享的交替器，第一次 tie 给 A，第二次给 B；交替器跨节点、跨轮次持续，不在新一轮重置。
- 广告发生在决策期前；被广告覆盖者立即成为冻结 A，即使原先是坚定 B 或未决定者也不再更新。

#### 5. 公平干预
- 广告：按题面指定 ID 范围与单位成本选种子。
- 高度：按初始图度排序；并列按固定 ID 或记录随机规则。
- 所有策略用同预算、同初始状态、同轮数。

### 6. 推导思路和思想来源
1. 双边交换是局部保度操作；大量接受交换逐渐破坏高阶相关。
2. 早期聚类下降快，是因为实证三角形结构远离随机保度平衡；后期趋平台。
3. HW2 刻意采用 Gauss-Seidel 式顺序更新：本轮较小 ID 的新决定会影响较大 ID，遍历顺序是模型定义的一部分。
4. PA 图的高度节点更极端，定向 hub 的级联影响可能大于 ER；需要结合度尾验证。

### 7. 例子：已解 → 半提示 → 可运行实验

#### 例子 1：已解
边 $(a,b),(c,d)$ 交换为 $(a,c),(b,d)$：四节点各失一得一，度不变；若 $(a,c)$ 已存在则拒绝。

#### 例子 2：半提示
若策略预算 3，节点度为 `{0:5,1:5,2:4,3:3}`，按“度降序、ID 升序”选哪些？
> [!question]- 核对
> 0、1、2。

#### 例子 3：可运行实现
```python
import random
import networkx as nx

def degree_preserving_rewire(graph, attempts, seed=0):
    rng = random.Random(seed)
    graph = graph.copy()
    initial_degrees = dict(graph.degree())
    accepted = 0
    for _ in range(attempts):
        first, second = rng.sample(list(graph.edges()), 2)
        u, v = first if rng.random() < 0.5 else first[::-1]
        w, x = second if rng.random() < 0.5 else second[::-1]
        if len({u, v, w, x}) < 4 or graph.has_edge(u, w) or graph.has_edge(v, x):
            continue
        graph.remove_edges_from([(u, v), (w, x)])
        graph.add_edges_from([(u, w), (v, x)])
        accepted += 1
    assert dict(graph.degree()) == initial_degrees
    return graph, accepted

def initial_vote(node):
    last_digit = node % 10
    if last_digit <= 3:
        return "A"
    if last_digit <= 7:
        return "B"
    return None

def ordered_vote(graph, rounds=10, persuaded=()):
    state = {node: initial_vote(node) for node in graph}
    mutable = {node for node, vote in state.items() if vote is None}

    # Advertising happens before day 1 and permanently freezes these voters at A.
    for node in persuaded:
        if node in state:
            state[node] = "A"
            mutable.discard(node)

    next_tie_vote = "A"
    history = []
    for _ in range(rounds):
        for node in sorted(mutable):
            a_votes = sum(state[neighbor] == "A" for neighbor in graph[node])
            b_votes = sum(state[neighbor] == "B" for neighbor in graph[node])
            if a_votes > b_votes:
                state[node] = "A"
            elif b_votes > a_votes:
                state[node] = "B"
            else:
                state[node] = next_tie_vote
                next_tie_vote = "B" if next_tie_vote == "A" else "A"
        history.append((sum(vote == "A" for vote in state.values()),
                        sum(vote == "B" for vote in state.values())))
    return state, history

graph = nx.watts_strogatz_graph(30, 4, 0.1, seed=1)
rewired, accepted = degree_preserving_rewire(graph, 200, seed=7)

# Regression 1: node 8 becomes A first; node 9 must see that same-round update.
order_graph = nx.Graph([(0, 8), (8, 9), (4, 9)])
ordered, _ = ordered_vote(order_graph, rounds=1)
assert ordered[8] == "A" and ordered[9] == "A"

# Regression 2: a single isolated mutable voter alternates across rounds.
tie_graph = nx.empty_graph([8])
after_two, history = ordered_vote(tie_graph, rounds=2)
assert history == [(1, 0), (0, 1)] and after_two[8] == "B"

# Regression 3: initially decided voters never update despite hostile neighbors.
fixed_graph = nx.Graph([(0, 4), (0, 5), (0, 6)])
fixed, _ = ordered_vote(fixed_graph, rounds=3)
assert fixed[0] == "A"

# Regression 4: advertising freezes an originally undecided voter at A.
ad_graph = nx.Graph([(4, 8)])
advertised, _ = ordered_vote(ad_graph, rounds=3, persuaded={8})
assert advertised[8] == "A"

print(accepted, round(nx.average_clustering(graph), 3),
      round(nx.average_clustering(rewired), 3), ordered, history)
# 输出重连统计与两组状态机证据；所有规则区分断言均通过。
```

#### 正式图加载与实验循环
1. 读无向边表后显式 `graph.add_nodes_from(range(10000))`，保留可能没有边的合法节点。
2. Q3.1 对每张图重新初始化状态并运行 10 轮，报告 A/B 票数、赢家和绝对票差。
3. Q3.2 对每个广告预算重新从原始状态开始；不能在前一个预算结果上继续追加。
4. Q3.3 高度干预先按题面选节点，再将其冻结为 A；保存节点 ID、度与 tie-breaking。
5. Q3.4 的度分布只用于解释机制，不能反向修改投票规则。

### 8. 常见误区和易混概念
- 删除旧边后才发现候选非法：应先检查，避免回滚遗漏。
- 把尝试数与成功交换数混为横轴：报告接受率并声明。
- 用新字典同步更新：忽略题面规定的同轮顺序依赖，会改变赢家和票差。
- 每轮重置 tie 为 A：官方只允许一个跨全图、跨轮次交替器。
- 让坚定选民随多数改变，或只让未决定者更新第一轮：都误读了“最初未决定者反复参加 10 轮”。
- 广告只影响未决定者：题面说明看到广告的所有选民都被冻结为 A。
- 高度策略每轮重新选：题目干预通常固定初始集合。

| 过程 | 固定项 | 改变量 | 验收不变量 |
| :--- | :--- | :--- | :--- |
| 双边交换 | 度序列、$n,m$ | 高阶结构 | 每节点度 |
| 广告干预 | 图、预算、规则 | 指定 ID 种子 | 成本 |
| 高度干预 | 图、预算、规则 | 高度种子 | tie 规则 |

### 9. 相关知识点与 Obsidian 双链建议
- 上游：[[随机网络模型-ER-WS-BA-配置模型]]。
- 下游：[[../05-传播与影响力/阈值模型与网络级联]]。
- 横向：[[聚类系数与网络距离]]、[[../04-排序与链接预测/中心性度量]]。
- 作业：CS224W 2017 HW2-Q1.2、Q3.1–Q3.4。

### 10. 闭卷复现任务
- [ ] 写双边交换候选。
- [ ] 列四个拒绝条件。
- [ ] 证明度不变。
- [ ] 报告接受率。
- [ ] 绘聚类轨迹。
- [ ] 写按 ID 递增的原地更新。
- [ ] 让全局 tie 交替器跨轮次持续。
- [ ] 区分坚定、可更新与广告冻结集合。
- [ ] 固定预算。
- [ ] 实现广告/高度策略。
- [ ] 用度分布解释差异。

### 11. 自测题：5 道
1. 双边交换保持什么？ #自测题/基础
   > [!question]- 每个节点度数与总边数。
2. 为什么四端点相异是安全条件？ #自测题/基础
   > [!question]- 避免候选自环和退化交换；更一般实现也可逐项检查。
3. 聚类为何趋向配置基线？ #自测题/中等
   > [!question]- 度固定而三角形等高阶相关逐渐被随机化。
4. 为什么 HW2 不能使用新字典同步更新？ #自测题/中等
   > [!question]- 题面要求较大 ID 节点立即读取较小 ID 节点在本轮的新状态，必须按 ID 原地更新。
5. 哪些对象永不再改变，tie 状态在哪里重置？ #自测题/较难
   > [!question]- 初始坚定选民和广告覆盖者永不改变；tie 交替器只在整次模拟开始时置 A，轮次之间不重置。

### 12. 我的主动回忆区
#### 我的闭卷复述
> 复述“保度重连”和“坚定/可更新/广告冻结三集合”的控制变量逻辑。
#### 我的推导复现
> 证明交换度不变，并写按 ID 原地更新和全局 tie 交替伪代码。
#### 我的错误与卡点
- [ ] 度变了 → 检查候选边与删除/新增配对。
- [ ] 曲线横轴不清 → 区分尝试/接受。
- [ ] 顺序更新结果不对 → 检查是否按 ID、是否读取同轮较小 ID 的新值。
- [ ] 第二轮 tie 错 → 检查交替器是否被错误重置。
#### 失败后的回流
- 重连错：第 5.1–5.3 节；投票错：第 5.4–5.5 节；代码错：第 7.3 节。

### 13. 给 Obsidian 的归档建议
- 文件夹：`02-网络结构与生成模型/`
- 关联：[[随机网络模型-ER-WS-BA-配置模型]]
- 标签：`#HW2` `#重连` `#级联实验`
- 拆分建议：两部分共同训练“只改变一个因素”的实验设计，保留同一作业卡。

### 🃏 Anki 卡片
- 简单图双边交换的验收不变量？::所有节点度数与总边数保持不变，新边不得产生自环或重边。
- HW2 投票为什么必须原地更新？::题面规定按 ID 递增处理，较大 ID 必须读取较小 ID 在当前轮的新状态。
- HW2 tie 交替器何时重置？::只在整次模拟开始时初始化为 A，随后跨节点和轮次持续交替。

## 原笔记：HW2-符号网络动态与新节点相容性证明

### 0. 先判断它值不值得深挖
- **类别**：A 类证明/模拟卡。
- **判断理由**：Q2.5–2.6 的关键不是试完 $2^n$ 种符号，而是识别新节点符号约束等价于原图已结构平衡。

### 1. 这个知识点解决什么问题？
> 给完整符号图加入新节点 $X$，何时能给所有新边赋符号，使每个包含 $X$ 的三元组平衡？局部随机修复过程又为什么可能不单调？

### 2. 为什么它重要？它有什么用？
- 训练把三元组条件写成代数相容方程。
- 用一般定理替代指数枚举。
- 覆盖 HW2-Q2.3–Q2.6。

### 3. 学它之前需要哪些前置知识？
1. [[符号网络与结构平衡]]。
2. 乘积符号、路径乘积和反证。

### 4. 用直觉语言解释它
> “新人的每段关系像给旧节点贴 ± 标签；旧边必须等于两端标签的乘积。若旧网内部已有矛盾三角形，任何标签都会冲突。”
- **一句话本质**：新节点相容赋号存在，当且仅当旧完整符号图强平衡。

### 5. 正式定义、核心公式、符号解释

#### 1. 新节点约束
令 $x_i=s_{Xi}\in\{\pm1\}$，旧边为 $s_{ij}$。新三元组 $(X,i,j)$ 平衡当且仅当
$$x_ix_js_{ij}=+1\iff s_{ij}=x_ix_j.$$

#### 2. 必要性
若存在一组 $x_i$ 满足所有旧边，则对任意旧三元组：
$$s_{ij}s_{jk}s_{ik}=(x_ix_j)(x_jx_k)(x_ix_k)=x_i^2x_j^2x_k^2=+1.$$
所以旧图所有三元组平衡；不平衡旧图不可能加入完全相容的新节点。

#### 3. 充分性
若旧完整符号图平衡，任选参考节点 $r$，令 $x_r=+1$、$x_i=s_{ri}$。由三元组 $(r,i,j)$ 平衡：
$$s_{ri}s_{rj}s_{ij}=+1\Rightarrow s_{ij}=x_ix_j.$$
因此所有新三元组平衡。整体翻转全部 $x_i$ 给出等价第二组赋号。

#### 4. 阵营解释
$x_i=+1$ 与 $x_i=-1$ 将旧节点分成至多两组；同组旧边正、跨组旧边负，正是强结构平衡定理。

#### 5. 动态局部修复
随机选不平衡三元组并翻一条边只保证目标三元组被修复；该边还属于 $n-3$ 个三元组，可破坏它们。能量（不平衡三元组数）不一定每步下降，需用仿真记录轨迹/循环。

HW2-Q2.4 的精确协议是：每次在 10 节点完全图上独立以 $p=1/2$ 初始化每条边；每步从**全部三元组**均匀抽一个，平衡则不变，不平衡则从三边均匀抽一条翻号；最多 1,000,000 步，达到全局结构平衡即可提前停止；独立重复 100 张图。输出至少包括平衡比例、每次停止步数，以及未在上限内平衡的 censored 次数。

### 6. 推导思路和思想来源
1. 用 $x_i$ 把“新边怎么取”改写成二元标签问题。
2. 必要性通过三条旧边相乘消去所有 $x$。
3. 充分性固定一个参考点，由平衡三元组恢复所有旧边。
4. 该等价同时解释两阵营结构与新节点赋号。
5. 动态模拟若每步重新扫描全部三元组会浪费大量时间；预先建立“边到所含三元组”的倒排表，翻边时只更新相关三元组的平衡状态。

### 7. 例子：已解 → 半提示 → 可运行验证

#### 例子 1：已解
旧三角形边符号为 `(+,+,-)`，乘积负。假设有 $x_1,x_2,x_3$ 满足 $s_{ij}=x_ix_j$，三边相乘必为正，矛盾，因此无相容新节点。

#### 例子 1B：Q2.3 的具体反例
在 5 节点完全图中令边 `01,02,03,04,13,14,23,24,34` 为正，边 `12` 为负。三元组 `012` 不平衡，而 `013`、`014` 平衡。若过程选中 `012` 并恰好翻转边 `01`，则 `012` 变平衡，但 `013`、`014` 同时变不平衡；其他三元组不受影响，所以全图平衡三元组数净减 1。这直接否定“局部修复使平衡数不减”。

#### 例子 2：半提示
旧图两组 `{1,2}` 与 `{3}`，组内正、跨组负。取 $x_1=x_2=+1$，则 $x_3=____`。
> [!question]- 核对
> $-1$；此时 $s_{ij}=x_ix_j$。

#### 例子 3：可运行动态模拟与相容性 oracle
```python
import random
from itertools import product, combinations

def edge_key(a, b):
    return tuple(sorted((a, b)))

def make_signed_complete_graph(n, rng):
    return {edge_key(a, b): rng.choice((-1, 1))
            for a, b in combinations(range(n), 2)}

def dynamic_balance_once(n=10, max_steps=1_000_000, seed=0, verify=False):
    rng = random.Random(seed)
    signs = make_signed_complete_graph(n, rng)
    triads = list(combinations(range(n), 3))
    triad_edges = [tuple(edge_key(a, b) for a, b in combinations(triad, 2))
                   for triad in triads]
    edge_to_triads = {edge: [] for edge in signs}
    products = []
    for triad_id, edges in enumerate(triad_edges):
        value = signs[edges[0]] * signs[edges[1]] * signs[edges[2]]
        products.append(value)
        for edge in edges:
            edge_to_triads[edge].append(triad_id)

    unbalanced = sum(value == -1 for value in products)
    if unbalanced == 0:
        return True, 0
    for step in range(1, max_steps + 1):
        triad_id = rng.randrange(len(triads))
        if products[triad_id] == -1:
            edge = rng.choice(triad_edges[triad_id])
            signs[edge] *= -1
            for affected in edge_to_triads[edge]:
                if products[affected] == -1:
                    unbalanced -= 1
                else:
                    unbalanced += 1
                products[affected] *= -1
        if verify:
            assert unbalanced == sum(value == -1 for value in products)
        if unbalanced == 0:
            return True, step
    return False, max_steps

def run_balance_experiment(repeats=100, n=10, max_steps=1_000_000,
                           seed=0, verify=False):
    outcomes = [dynamic_balance_once(n, max_steps, seed + run, verify)
                for run in range(repeats)]
    fraction = sum(success for success, _ in outcomes) / repeats
    return fraction, outcomes

def compatible_assignments(nodes, signs):
    solutions = []
    for values in product((-1, 1), repeat=len(nodes)):
        label = dict(zip(nodes, values))
        if all(signs[tuple(sorted((i, j)))] == label[i] * label[j]
               for i, j in combinations(nodes, 2)):
            solutions.append(label)
    return solutions

balanced_signs = {(0, 1): 1, (0, 2): -1, (1, 2): -1}
unbalanced_signs = {(0, 1): 1, (0, 2): 1, (1, 2): -1}
fraction, smoke = run_balance_experiment(
    repeats=20, n=6, max_steps=20_000, seed=7, verify=True)
assert 0.0 <= fraction <= 1.0 and len(smoke) == 20
print(len(compatible_assignments(range(3), balanced_signs)),
      len(compatible_assignments(range(3), unbalanced_signs)),
      fraction, sum(not success for success, _ in smoke))
# 输出相容解数、缩小实验平衡比例和 censored 次数；正式作业改用题面参数。
```

正式运行使用 `run_balance_experiment(repeats=100, n=10, max_steps=1_000_000, seed=...)`。保存随机种子、每次停止步数与 censored 标志；不要把缩小烟雾测试的比例当作正式答案。

### 8. 常见误区和易混概念
- 只检查某一个新三元组：赋号必须同时满足所有节点对。
- 说“加入新节点修复旧不平衡三元组”：旧边未改，旧三元组仍不平衡。
- 充分性直接引用两阵营定理却不证明：可用参考节点三行完成。
- 局部修复一定收敛：目标三元组改善不等于全局能量单调。
- 只从不平衡三元组抽样：题面先从全部三元组均匀抽取，抽到平衡三元组时应原地不动。
- 每次翻固定边或用全局最优边：题面要求从被选中不平衡三元组的三条边中均匀抽一条。
- 只报告平衡比例：还应保存停止步数和达到上限仍未平衡的运行，才能诊断实现与计算预算。

| 命题 | 条件 | 结论 |
| :--- | :--- | :--- |
| 新节点相容 | 存在 $x_i$ 使 $s_{ij}=x_ix_j$ | 所有新三元组平衡 |
| 旧图平衡 | 所有旧三元组乘积正 | 相容赋号存在 |
| 旧图不平衡 | 至少一个乘积负 | 相容赋号不存在 |

### 9. 相关知识点与 Obsidian 双链建议
- 上游：[[符号网络与结构平衡]]。
- 横向：[[三元闭包弱关系与同质性]]。
- 作业：CS224W 2017 HW2-Q2.3–Q2.6。

### 10. 闭卷复现任务
- [ ] 写新节点约束。
- [ ] 证明必要性。
- [ ] 证明充分性。
- [ ] 解释整体翻转。
- [ ] 恢复两阵营。
- [ ] 构造不相容三角形。
- [ ] 用穷举验证小图。
- [ ] 解释局部修复非单调。
- [ ] 设计不平衡数轨迹。
- [ ] 复现 10 节点、100 次、1,000,000 步与提前停止协议。
- [ ] 区分“新三元组全平衡”和“全图平衡”。

### 11. 自测题：5 道
1. 新三元组平衡的代数条件？ #自测题/基础
   > [!question]- $s_{ij}=x_ix_j$。
2. 三条旧边相乘为何消去标签？ #自测题/基础
   > [!question]- 每个 $x_i$ 出现两次，平方为 1。
3. 充分性如何选标签？ #自测题/中等
   > [!question]- 固定参考点 $r$，取 $x_r=1,x_i=s_{ri}$。
4. Q2.4 每步从哪里抽三元组和待翻边？ #自测题/中等
   > [!question]- 从全部三元组均匀抽；若不平衡，再从其三条边均匀抽一条翻号。抽到平衡三元组不操作。
5. 新节点能让旧不平衡图整体平衡吗？ #自测题/较难
   > [!question]- 不能；旧不平衡三元组仍存在，且相容新边赋号本身也不存在。

### 12. 我的主动回忆区
#### 我的闭卷复述
> 用标签相容性解释“存在新节点赋号 iff 旧图平衡”。
#### 我的推导复现
> 独立写必要性/充分性证明，并写出动态过程的抽样、翻边、提前停止和重复实验协议。
#### 我的错误与卡点
- [ ] 只证明一方向 → 补必要与充分。
- [ ] 忘记旧图完整性 → 非完整图需改成 cycle 相容条件。
- [ ] 动态过程误判单调 → 画共享边三元组。
- [ ] 模拟过慢 → 只更新包含被翻边的三元组，并在全局平衡时提前停止。
#### 失败后的回流
- 定义错：第 5.1 节；证明错：第 5.2–5.3 节；模拟错：第 5.5 节。

### 13. 给 Obsidian 的归档建议
- 文件夹：`03-社会结构与社区/`
- 关联：[[符号网络与结构平衡]]
- 标签：`#HW2` `#结构平衡` `#证明`
- 拆分建议：新节点两题共享同一 iff 定理，保持一张卡。

### 🃏 Anki 卡片
- 新节点符号相容性的核心方程？::$s_{ij}=x_ix_j$。
- 相容新节点何时存在？::当且仅当旧完整符号图结构平衡。
- HW2-Q2.4 每一步如何抽样？::先从全部三元组均匀抽；若其不平衡，再从三条边均匀抽一条翻转；平衡则不操作。
