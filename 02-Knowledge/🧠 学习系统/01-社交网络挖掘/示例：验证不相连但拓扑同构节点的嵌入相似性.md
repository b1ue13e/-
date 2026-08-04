---
title: "Struc2Vec"
date: 2026-07-31
type: concept
kind: concept
flow: knowledge
course: "01-社交网络挖掘"
importance: "A"
tags: [学习, 核心概念, 图表示学习]
upstream: ["[[DeepWalk]]", "[[Node2Vec]]", "[[Word2Vec]]"]
downstream: ["[[GraphSAGE]]", "[[GCN]]", "[[网络拓扑对齐]]"]
status: learning
---

> [!NOTE] 核心直觉：跨越空间距离的“职能角色定位器”
> **类比**：想象两家没有任何业务往来、位于不同国家的公司。两家公司里各有一位“首席财务官（CFO）”。这两位 CFO 彼此不认识，各自的社交圈（空间距离）毫无交集，但在各自公司的组织结构图中，他们的位置极度相似——下属都是几个财务经理，上级都是 CEO，所处的局部树状管理层级一模一样。Struc2Vec 就是一种不需要节点互为好友、仅凭各自周围的“组织拓扑结构模式”就能为它们赋予高度相似“角色向量”的表征学习算法。

## 1. 为什么需要这个知识点？
- **背景**：在图表示学习中，传统算法如 DeepWalk 和 Node2Vec 依赖网络近邻假设（Homophily Hypothesis）和局部空间同配性（Spatial Proximity），即物理上连接紧密或位于同一社群的节点会学习到相似的向量表示。
- **痛点**：对于网络中的“结构等价性/结构相似性”（Structural Equivalence），例如跨子网的关键枢纽（Hubs）、金字塔管理架构中的中层干部、不同金融欺诈团伙中的洗钱中间节点，它们可能分布在图的不同区域，地理/拓扑距离极远（甚至位于完全不连通的子图中）。传统近邻游走模型在这些节点间无法转移，无法捕获其相同的拓扑结构特征。
- **意义**：Struc2Vec（Ribeiro et al., KDD 2017）彻底解藕了节点嵌入对“空间距离”的依赖，定义了一套基于层次化度序列（Ordered Degree Sequences）与动态时间规整（DTW）的拓扑距离度量，并通过构建多层加权图（Multi-layer Graph）引入了结构维度的随机游走，实现了纯粹基于拓扑结构的节点角色嵌入。

## 2. 核心定义与公式/代码

### 2.1 算法三大核心步骤与数学公式

#### 步骤 1：定义 $k$-阶结构距离（Hierarchy of Structural Distance）
设 $R_k(u)$ 为节点 $u$ 的 $k$-阶邻域节点构成的有序度序列（Ordered Degree Sequence），序列按升序/降序排列。
节点 $u$ 和 $v$ 在 $k$-阶邻域上的结构距离 $f_k(u, v)$ 递归定义为：
$$f_k(u, v) = f_{k-1}(u, v) + g(R_k(u), R_k(v))$$
其中 $f_{-1}(u, v) = 0$。
函数 $g(A, B)$ 衡量两个不同长度的有序度序列 $A$ 和 $B$ 之间的距离，采用 **动态时间规整（Dynamic Time Warping, DTW）** 算法计算。对于序列中的两元素 $a, b$，其元素级非线性距离定义为：
$$g_0(a, b) = \frac{\max(a, b)}{\min(a, b)} - 1$$
DTW 算法通过动态规划解决变长度序列对齐的累积代价极小化问题。

#### 步骤 2：构建多层加权图（Multi-layer Graph Construction）
构建包含 $K+1$ 层的层次图 $M$（$k = 0, 1, \dots, K^*$，其中 $K^*$ 为图的有效直径）。
- **层内边权重（Intra-layer weights）**：在第 $k$ 层中，节点 $u$ 和 $v$ 之间的连接权重与它们的 $k$-阶结构距离成反比：
  $$w_k(u, v) = \exp(-f_k(u, v))$$
  结构相似度越高，层内边权重越大。
- **层间边权重（Inter-layer weights）**：同一个节点 $u$ 在相邻层 $u_k$ 与 $u_{k-1}$、$u_{k+1}$ 之间建立跨层直连边。
  向上跨层权重 $w(u_k, u_{k+1})$ 衡量节点 $u$ 在第 $k$ 层结构的独特程度：
  $$w(u_k, u_{k+1}) = \log(\Gamma_k(u) + e)$$
  其中 $\Gamma_k(u)$ 表示在第 $k$ 层中与 $u$ 的结构距离大于层内平均距离的节点数量；向下跨层权重固定设为 $w(u_k, u_{k-1}) = 1$。

#### 步骤 3：多层图上的偏置随机游走与 Skip-gram 训练
在多层图 $M$ 上进行偏置随机游走：
- **层内转移概率**：
  $$p_k(u, v) = \frac{w_k(u, v)}{Z_k(u)}, \quad \text{其中 } Z_k(u) = \sum_{v \in V, v \neq u} w_k(u, v)$$
- **跨层转移概率**：设定固定概率 $p_{\text{stay}}$ 在当前层游走，以 $1 - p_{\text{stay}}$ 的概率根据层间权重向上下层跨越。

游走生成的节点序列输入 Skip-gram 模型（Word2Vec）进行最大似然估计优化，学习每个节点的 $d$ 维结构向量表示 $\mathbf{z}_u \in \mathbb{R}^d$。

---

### 2.2 Struc2Vec 核心实现代码 (Python / NetworkX / Gensim)

```python
import numpy as np
import networkx as nx
from fastdtw import fastdtw
from gensim.models import Word2Vec
import random

def compute_degree_sequence(G, node, k):
    """获取节点 node 的 k-hop 邻域节点的排序度序列"""
    nodes_at_k = nx.single_source_shortest_path_length(G, node, cutoff=k)
    k_hop_nodes = [n for n, dist in nodes_at_k.items() if dist == k]
    deg_seq = sorted([G.degree(n) for n in k_hop_nodes])
    return deg_seq if deg_seq else [0]

def dtw_distance(seq1, seq2):
    """计算两个变长度序列之间的 DTW 结构距离"""
    dist_func = lambda a, b: (max(a, b) / (min(a, b) + 1e-5)) - 1
    distance, _ = fastdtw(seq1, seq2, dist=dist_func)
    return distance

class Struc2VecBuilder:
    def __init__(self, G, max_k=2):
        self.G = G
        self.nodes = list(G.nodes())
        self.max_k = max_k
        self.layer_distances = {}
        self.intra_weights = {}
        
    def build_structural_distances(self):
        """步骤 1: 递归计算所有节点对在各 k 阶的结构距离 f_k(u, v)"""
        num_nodes = len(self.nodes)
        for k in range(self.max_k + 1):
            deg_seqs = {u: compute_degree_sequence(self.G, u, k) for u in self.nodes}
            dist_matrix = np.zeros((num_nodes, num_nodes))
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    u, v = self.nodes[i], self.nodes[j]
                    dtw_d = dtw_distance(deg_seqs[u], deg_seqs[v])
                    if k > 0:
                        dtw_d += self.layer_distances[k-1][i, j]
                    dist_matrix[i, j] = dtw_d
                    dist_matrix[j, i] = dtw_d
            self.layer_distances[k] = dist_matrix
            # 计算层内边权重 w_k(u, v) = exp(-f_k(u, v))
            self.intra_weights[k] = np.exp(-dist_matrix)
            
    def generate_random_walks(self, num_walks=10, walk_length=20, p_stay=0.7):
        """步骤 2 & 3: 在多层结构图上生成随机游走序列"""
        walks = []
        num_nodes = len(self.nodes)
        for _ in range(num_walks):
            for start_node in self.nodes:
                curr_node_idx = self.nodes.index(start_node)
                curr_layer = 0
                walk = [str(start_node)]
                
                for _ in range(walk_length - 1):
                    # 决定层内游走还是跨层游走
                    if random.random() < p_stay or self.max_k == 0:
                        # 层内转移
                        weights = self.intra_weights[curr_layer][curr_node_idx].copy()
                        weights[curr_node_idx] = 0  # 不原地停留
                        sum_w = np.sum(weights)
                        if sum_w > 0:
                            probs = weights / sum_w
                            curr_node_idx = np.random.choice(num_nodes, p=probs)
                    else:
                        # 跨层转移
                        if curr_layer == 0:
                            curr_layer += 1
                        elif curr_layer == self.max_k:
                            curr_layer -= 1
                        else:
                            curr_layer += 1 if random.random() < 0.5 else -1
                            
                    walk.append(str(self.nodes[curr_node_idx]))
                walks.append(walk)
        return walks

# 示例：验证不相连但拓扑同构节点的嵌入相似性
if __name__ == "__main__":
    # 创建两个互相隔离但结构完全相同的星形网络 (Central hubs: Node 0 & Node 5)
    G = nx.disjoint_union(nx.star_graph(4), nx.star_graph(4))
    
    builder = Struc2VecBuilder(G, max_k=2)
    builder.build_structural_distances()
    walks = builder.generate_random_walks(num_walks=30, walk_length=15)
    
    # 训练 Skip-gram 表征模型
    model = Word2Vec(sentences=walks, vector_size=16, window=5, min_count=0, sg=1, workers=2)
    
    vec_hub1 = model.wv['0']
    vec_hub2 = model.wv['5']
    cos_sim = np.dot(vec_hub1, vec_hub2) / (np.linalg.norm(vec_hub1) * np.linalg.norm(vec_hub2))
    
    print(f"隔离星形中心点 (Node 0 & Node 5) 余弦相似度: {cos_sim:.4f}")
```

## 3. 具体应用案例
**场景**：跨电信诈骗子网中“洗钱中介/关键枢纽节点”的识别。

在反洗钱与网络安全监控中，非法团伙通常会建立多个互相隔离的地下资金通道（在资金交易图上表现为彼此不连通的连通分量）。洗钱枢纽节点（Hub）并不与其它诈骗分子的账户直接建立资金往来（空间距离无限大），但它们具有高度一致的“拓扑结构特征”：同时连接上游数十个小额汇入账户（特定入度分布），并迅速向少数几个高额提现账户转账（特定出度分布）。

- **经典方法局限**：DeepWalk 或 PageRank 依赖全局连通性或同质性，在无边相连的两个子网节点间无法传导权重，因而无法识别不同子网中的同类洗钱中介。
- **Struc2Vec 解决方案**：通过提取各节点 1-hop、2-hop 的度序列并计算 DTW 距离，Struc2Vec 在多层结构图上将具有相似资金分发模式的中介节点分配极高的邻接权重。最终生成的向量嵌入在低维空间中聚类在一起，使得欺诈检测模型（如 XGBoost / Random Forest）无需种子关联即可直接识别隐蔽的洗钱枢纽。

## 4. 常见误区与陷阱 (Pitfalls)
> [!WARNING] 踩坑预警
> - **误区 1：混淆“网络同质性 (Homophily)”与“结构等价性 (Structural Equivalence)”**
>   - *错误理解*：认为节点向量相似度高就代表它们在网络中互相连接或位于同一个社群。
>   - *正确理解*：DeepWalk / Node2Vec 优化的是同质性（拓扑临近度）；而 Struc2Vec 优化的是结构等价性。哪怕两个节点位于完全不连通的两个连通分量中，只要它们的局部度序列分布一致，其向量就会高度相似。
> - **误区 2：忽视 Struc2Vec 的高计算复杂度，盲目应用于超大图**
>   - *错误理解*：直接将 Struc2Vec 裸代码应用于千万级节点的全量图表示学习。
>   - *正确理解*：Struc2Vec 需要计算所有节点对 $(u, v)$ 在多个 $k$ 阶邻域的 DTW 距离，原始空间和时间复杂度高达 $O(K |V|^2)$。在工业级大图应用时，必须开启度序列压缩、邻域树修剪以及 FastDTW 近似优化。
> - **误区 3：尝试将 Struc2Vec 用于链路预测（Link Prediction）任务**
>   - *错误理解*：试图用 Struc2Vec 计算两节点向量点积来预测它们之间是否存在边。
>   - *正确理解*：Struc2Vec 完全剥离了节点的全局位置与几何连通信息。两个结构相同的节点即便向量极度相似，它们之间也可能完全没有连边。Struc2Vec 专用于节点角色分类（Node Role Classification）与结构异常检测，而非链路预测。

## 5. 跨学科链接与双链
- **上游知识**：
  - [[DeepWalk]]：基于随机游走与 Skip-gram 的经典图节点嵌入模型。
  - [[Node2Vec]]：通过偏置参数 $p, q$ 在 BFS（结构性）与 DFS（同质性）间权衡的前作。
  - [[Word2Vec]]：提供 Skip-gram 与负采样（Negative Sampling）的表示学习底座。
  - [[动态时间规整]]：解决变长序列间非线性匹配的动态规划算法。
- **下游知识**：
  - [[GraphSAGE]]：归纳式图神经网络，支持节点特征与局部拓扑的采样聚合。
  - [[GCN]]：图卷积网络，通过频域/空域卷积协同学习几何与属性信息。
  - [[网络拓扑对齐]]：利用结构角色向量匹配两个无锚点异构网络的拓扑节点。
- **跨领域关联**：
  - **计算社会学 (Computational Social Science)**：社交角色划分（Social Role Analysis），如识别网络中的“领袖”、“中间桥梁”、“边缘平民”。
  - **网络安全与风控 (Cybersecurity & Risk Control)**：跨子网僵尸网络（Botnet）C2 控制节点识别、黑灰产分发渠道挖掘。

## 6. 费曼自测清单 (Active Recall)
- [ ] 为什么 DeepWalk 和 Node2Vec 无法准确捕获不相连节点的“结构角色”（Structural Role）？
- [ ] Struc2Vec 如何使用动态时间规整（DTW）计算两个节点在 $k$-阶邻域上的度序列距离 $g(R_k(u), R_k(v))$？
- [ ] Struc2Vec 构建的多层图（Multi-layer Graph）中，层内边权重与跨层边权重各自表达了什么拓扑含义？
- [ ] 如果在无向图中有两个毫无关联且相距遥远但同构的“星形节点中心”，Struc2Vec 学习到的嵌入向量会呈现什么特点？为什么？
