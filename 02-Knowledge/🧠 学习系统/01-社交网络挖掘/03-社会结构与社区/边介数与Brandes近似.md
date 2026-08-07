---
type: study
topic: "边介数与 Brandes 近似"
course: "社交网络挖掘"
tags: [学习, 01-社交网络挖掘, 边介数, Brandes, HW4]
created: 2026-08-05
status: completed
difficulty: advanced
concept: [边介数, 最短路DAG, 源点采样]
prerequisites: [路径连通与Bow-tie结构, BFS, 条件概率]
related: [社区发现-模块度与谱松弛, 社区发现-模块度与谱松弛, 中心性度量]
flow: knowledge
kind: derivation
stage_moc: "[[🧭 阶段3-社会结构与社区]]"
source: "Stanford CS224W 2017 HW4-Q2; NCM Chapter 3"
source_url: "https://snap.stanford.edu/class/cs224w-2017/handouts.html"
accessed: 2026-08-06
license: "课程讲义与题面默认 link-only；教材只作章节定位"
assessment_exempt: false
anki_deck: "社交网络挖掘::社会结构"
anki_tags: [边介数, Brandes, 最短路DAG, HW4]
---

# 边介数与 Brandes 近似

## 0. 学习边界
- **类别**：**A 类**；HW4-Q2 的对象是边，而不是节点。
- **判断理由**：Girvan–Newman 删除跨社区的高边介数边；若把节点依赖直接当作边分数，会从定义层面答错。

## 1. 这个知识点解决什么问题？
> **麻烦**：一条边可能不是高频边，却位于许多节点对的最短路上。逐对枚举路径既慢又会重复计算，怎样准确累积，并在大图上以可控代价近似？

## 2. 为什么它重要？它有什么用？
- **连接大图景**：把 BFS、最短路计数、社区桥梁和抽样估计串成一条算法链。
- **实际应用**：Girvan–Newman、脆弱链路识别、交通瓶颈和 HW4-Q2。
- **高频任务**：实现单源依赖递推、比较精确/近似排序、解释运行时间与抽样方差。

## 3. 学它之前需要哪些前置知识？
1. **[[路径连通与Bow-tie结构]]**：BFS 层级与最短路 DAG。
2. **条件期望与无偏估计**：样本源点均匀时，用总体规模除以样本量缩放样本和。

### 先备诊断
- [ ] 能在菱形图 `s-a-t`、`s-b-t` 上写出从 $s$ 到 $t$ 的最短路条数 2。
- [ ] 能说明 DAG 中前驱一定比当前节点离源点近一层。
- **失败补救**：任一项不会，先回看[[路径连通与Bow-tie结构#5. 正式定义、核心公式、符号解释]]。

## 4. 用直觉语言解释它
> “从一个源点向外放水：BFS 记录水能沿多少条最短渠道到达每处；回流时，终点需求按这些渠道的份额分给边。”
- **一句话本质**：先正向数最短路，再反向按路径份额分摊依赖。

## 5. 正式定义、核心公式、符号解释

### 1. 边介数定义
对无向边 $e\in E$，采用有序端点对口径：
$$
B(e)=\sum_{s\in V}\sum_{t\ne s}\frac{\sigma_{st}(e)}{\sigma_{st}},
$$
其中 $\sigma_{st}$ 是 $s\to t$ 最短路条数，$\sigma_{st}(e)$ 是包含 $e$ 的条数。若改用无序端点对，最终分数除以 2；必须声明口径。

### 2. 单源最短路计数
固定源点 $s$：
$$
\sigma_s(s)=1,\qquad
\sigma_s(w)=\sum_{v\in P_s(w)}\sigma_s(v),
$$
$P_s(w)$ 是最短路 DAG 中 $w$ 的前驱集合。

### 3. Brandes 边依赖递推
逆 BFS 顺序处理节点 $w$，对每个前驱 $v\in P_s(w)$：
$$
\delta_s(v,w)=\frac{\sigma_s(v)}{\sigma_s(w)}\left(1+\delta_s(w)\right),
\qquad
\delta_s(v)\mathrel{+}=\delta_s(v,w).
$$
单源对边的贡献是 $\delta_s(v,w)$；全源相加得到有序对口径的边介数。

### 4. 源点抽样近似
均匀有放回抽取 $k$ 个源点 $S=(s_1,\ldots,s_k)$：
$$
\widehat B(e)=\frac{n}{k}\sum_{i=1}^k\delta_{s_i}(e).
$$
因为 $E_{s\sim U(V)}[\delta_s(e)]=B(e)/n$，该固定样本量估计在此口径下无偏。CS224W HW4 还采用“累计依赖超过阈值或达到样本上限”的自适应停止；自适应停止会改变简单无偏论证，回答时应按题目给定保证分析。

### 5. 符号表
| 符号 | 含义 | 实现对象 |
| :--- | :--- | :--- |
| $P_s(w)$ | $w$ 的最短路前驱 | `predecessors[w]` |
| $\sigma_s(w)$ | $s\to w$ 最短路条数 | `sigma[w]` |
| $\delta_s(w)$ | $w$ 下游的累计依赖 | `node_dep[w]` |
| $\delta_s(v,w)$ | 源点 $s$ 对边 $(v,w)$ 的贡献 | `edge_dep[edge]` |

## 6. 推导思路和思想来源
1. BFS 保证只有相邻层间的边能位于从 $s$ 出发的最短路 DAG 上。
2. 到达 $w$ 的 $\sigma_s(w)$ 条最短路中，经前驱 $v$ 的有 $\sigma_s(v)$ 条，因此份额为 $\sigma_s(v)/\sigma_s(w)$。
3. 节点 $w$ 既代表“以 $w$ 为终点”的 1 单位需求，也承接其所有下游需求 $\delta_s(w)$。
4. 所以边 $(v,w)$ 分到 `路径份额 × (1 + 下游依赖)`；逆序确保 $w$ 的下游已经算完。
5. 对所有源点相加等价于定义中的所有端点对求和；只抽部分源点则用 Horvitz–Thompson 式缩放恢复总体量级。

## 7. 例子：已解 → 渐隐 → 独立应用

### 例子 1：已解例（菱形图手算）
图有边 $s-a,s-b,a-t,b-t$。从 $s$ 出发，$\sigma_s(a)=\sigma_s(b)=1$，$\sigma_s(t)=2$。逆推时，$(a,t)$ 和 $(b,t)$ 各分得 $1/2$；$a,b$ 各有依赖 $1/2$，于是 $(s,a)$、$(s,b)$ 各分得 $1+1/2=3/2$。

### 例子 2：渐隐例（只给脚手架）
在路径 $0-1-2-3$ 上从源点 0 出发：
1. 填写 $\sigma_0=(\_,\_,\_,\_)$。
2. 从节点 3 逆推，边 $(2,3)$ 的贡献是 `____`。
3. 边 $(0,1)$ 承担终点 1、2、3 的需求，贡献是 `____`。

> [!question]- 核对
> $\sigma_0=(1,1,1,1)$；贡献依次为 1、2、3。

### 例子 3：可运行实现
```python
from collections import defaultdict, deque
import networkx as nx

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
            share = sigma[parent] / sigma[child]
            value = share * (1.0 + node_dependency[child])
            edge = tuple(sorted((parent, child)))
            edge_dependency[edge] += value
            node_dependency[parent] += value
    return dict(edge_dependency)

graph = nx.Graph([(0, 1), (0, 2), (1, 3), (2, 3)])
print(single_source_edge_dependencies(graph, 0))
# {(1, 3): 0.5, (2, 3): 0.5, (0, 1): 1.5, (0, 2): 1.5}
```

## 8. 常见误区和易混概念
- **误区 1：把节点依赖当边介数。** 节点 $w$ 的累计量要按 $\sigma_s(v)/\sigma_s(w)$ 分到每条前驱边。
- **误区 2：不区分有序/无序端点对。** 无向图全源算法常把每条无序路径算两次；比较库输出前先统一归一化。
- **误区 3：遍历同层边。** 同层边不在从该源点出发的最短路 DAG 上，单源贡献为 0。

| 概念 | 评分对象 | 基础结构 | 社区用途 |
| :--- | :--- | :--- | :--- |
| 节点介数 | 节点 | 经过节点的最短路 | 找中介节点 |
| 边介数 | 边 | 经过边的最短路 | Girvan–Newman 删桥边 |
| 桥 | 边 | 删除后分量增加 | 纯拓扑脆弱性 |
| 流介数 | 节点/边 | 全流而非仅最短路 | 多路径传输 |

## 9. 相关知识点与 Obsidian 双链建议
- 上游：[[路径连通与Bow-tie结构]]。
- 下游：[[社区发现-模块度与谱松弛]]。
- 横向：[[社区发现-模块度与谱松弛]]、[[中心性度量]]。
- 作业：CS224W 2017 HW4-Q2；映射只保存题号与所需知识，不保存作业答案。

## 10. 闭卷复现任务
- [ ] 精确定义边介数并声明端点对口径。
- [ ] 在菱形图上正向计算 $P_s$ 与 $\sigma_s$。
- [ ] 从路径份额推出边依赖递推。
- [ ] 手算路径图的单源依赖。
- [ ] 不看笔记实现 BFS 正推与逆推。
- [ ] 证明固定样本量缩放估计的期望。
- [ ] 说明自适应停止为何需单独分析。
- [ ] 区分节点介数、边介数与桥。
- [ ] 解释 Girvan–Newman 为什么要重算介数。
- [ ] 报告精确/近似方法的时间和排序误差。

## 11. 自测题：5 道
1. HW4-Q2 的评分对象是什么？ #自测题/基础
   > [!question]- 无向边的介数，不是节点介数。
2. 为什么 $\sigma_s(w)$ 要对所有前驱求和？ #自测题/基础
   > [!question]- 每条到前驱的最短路再接边 $(v,w)$，构成一条到 $w$ 的最短路，且按最后一个前驱互斥划分。
3. 菱形图中 $(a,t)$ 为何只分到 $1/2$？ #自测题/中等
   > [!question]- 到 $t$ 有两条等长最短路，其中一条经 $a$。
4. 固定抽 $k$ 个均匀源点为何乘 $n/k$？ #自测题/中等
   > [!question]- 单个源贡献均值是全源总和的 $1/n$，样本和的期望是 $kB(e)/n$。
5. 如何判断近似排序是否足够用于删边？ #自测题/较难
   > [!question]- 除分数误差外比较 top-k 重合、秩相关和删边后社区结果，并报告多随机种子稳定性。

## 12. 我的主动回忆区
### 我的闭卷复述
> 不看公式，解释“正向数路径、反向分需求”，并说清评分对象为什么是边。
### 我的推导复现
> 从 $\sigma_s(v)/\sigma_s(w)$ 的路径份额出发，重建 $\delta_s(v,w)$；再证明 $n/k$ 缩放。
### 我的错误与卡点
- [ ] 我把节点依赖直接记到边上 → 回看第 5.3 节。
- [ ] 我忘记逆序处理 → 重做路径图渐隐例。
- [ ] 我与 NetworkX 差一倍 → 检查有序/无序端点对和归一化。
### 失败后的回流
- 定义错：第 5.1 节；递推错：第 6 节；代码错：第 7.3 节；抽样解释错：第 5.4 节。
- [ ] 明天重做渐隐例　[ ] 3 天后独立实现　[ ] 7 天后做混合辨析　[ ] 14 天后复测

## 13. 给 Obsidian 的归档建议
- 文件夹：`03-社会结构与社区/`
- 关联：[[社区发现-模块度与谱松弛]]、[[社区发现-模块度与谱松弛]]
- 标签：`#边介数` `#Brandes` `#HW4`
- 拆分建议：边介数具有独立定义、递推、代码和作业题，必须与谱聚类分卡。

## 🃏 Anki 卡片
- Brandes 的边依赖递推是什么？::$\delta_s(v,w)=\frac{\sigma_s(v)}{\sigma_s(w)}(1+\delta_s(w))$，并把该值累加到 $v$ 的节点依赖。
- 为什么边介数近似乘 $n/k$？::均匀源点的单源贡献期望为全源总和的 $1/n$，$k$ 个样本和乘 $n/k$ 恢复总体量级。
- 节点介数与边介数最关键区别？::求和对象分别是经过节点与经过边的最短路份额；Girvan–Newman 使用边介数。

## 🧪 学完本节后可完成的作业

- **可立即完成**：[[社交网络挖掘-课后作业-05-排序边介数Kronecker与谱聚类#2. 近似边介数中心性（25 分，Anunay、Praty）|课后作业 05 题 2]]。
- **为什么现在能做**：已覆盖 BFS DAG、路径计数、边依赖和逐边抽样停止。
- **提交产物**：小图手算、精确/近似曲线、每边样本数、capped 状态与计时。

