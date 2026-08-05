---
title: "Kaggle图竞赛"
date: 2026-07-31
type: concept
kind: concept
flow: knowledge
course: "01-社交网络挖掘"
importance: "A"
tags: [学习, 核心概念, 综合实战]
upstream: ["[[图机器学习概述]]", "[[Node2Vec]]", "[[GCN]]", "[[GraphSAGE]]"]
downstream: ["[[OGB图基准数据集]]", "[[工业级图推荐系统]]"]
status: learning
---

> [!NOTE] 核心直觉：侦探破案与“图-表融合”战术
> **类比**：Kaggle 图竞赛就像是一场高维度的侦探破案赛。传统表格竞赛只看每个嫌疑人自己的“履历档案”（节点属性特征），而图竞赛不仅要看履历，还要调取整个城市的“通话记录与社交亲密度网络”（拓扑结构）。顶尖选手就像老练的刑警，一方面手工提取社交网络的拓扑几何特征（如度数、PageRank、K-Hop 团伙结构），另一方面使用神经网络（GNN）自动传递情报；最后将二者融合，并严防“剧透泄露”（Transductive Leakage）。

## 1. 为什么需要这个知识点？
- **背景**：在 Kaggle、KDD Cup 以及 OGB (Open Graph Benchmark) 等顶级数据科学竞赛中，基于图结构的数据挖掘（如节点分类、链路预测/边预测、图分类/分子属性预测）已成为高分冲榜的关键战场。现实数据如金融交易网、社交关注网、分子结构图均具备非欧几里得属性。
- **痛点**：传统表格模型（LightGBM/XGBoost）无法直接吸收图的拓扑连通性与高阶邻居关系；直接套用原生 PyG/DGL 图神经网络（GNN）模型又极易面临超参数难调、异配图（Heterophily）效果差、表达能力瓶颈（Over-smoothing）以及严重的数据泄露（Transductive Leakage）问题导致线下 CV 与线上 LB 脱节。
- **意义**：掌握 Kaggle 图竞赛的方法论与实战框架，能建立“手工图特征工程 + GNN 消息传递 + GBDT/Stacking 模型融合 + 后处理 Label Propagation”的全栈竞赛金牌方案，将图论理论落地为工业级别的最高分表现。

## 2. 核心定义与公式/代码

### 2.1 竞赛中的数学公式与算法框架

#### 1. 图数据分割与穿越防护（Transductive vs Inductive Split）
对于图中的链路预测或节点分类，图划分为训练子图 $G_{train}=(V, E_{train})$ 以及测试边集 $E_{test}$。在提取拓扑特征（如 PageRank $\mathbf{pr}$）时，**必须严格只在 $E_{train}$ 上计算**，防止测试集拓扑反向泄露：
$$\mathbf{pr}^{(t+1)} = \alpha \mathbf{pr}^{(t)} \cdot \mathbf{A}_{train} \mathbf{D}_{train}^{-1} + (1-\alpha) \frac{\mathbf{1}}{N}$$

#### 2. 拓扑相似度指标（链路预测核心特征工程）
对于节点对 $(u, v)$，常用手工拓扑重叠特征：
- **Jaccard 相似度系数**：
  $$J(u, v) = \frac{|\Gamma(u) \cap \Gamma(v)|}{|\Gamma(u) \cup \Gamma(v)|}$$
- **Adamic-Adar 指数（低度数共邻节点加权）**：
  $$AA(u, v) = \sum_{z \in \Gamma(u) \cap \Gamma(v)} \frac{1}{\log |\Gamma(z)|}$$

#### 3. C&S (Correct & Smooth) 后处理平滑算法
在 GNN 预测得出基础概率矩阵 $\mathbf{Z}^{(0)}$ 后，计算训练集残差 $\mathbf{E}^{(0)}$ 并在图拓扑上做马尔可夫平滑传播：
$$\mathbf{E}^{(t+1)} = (1 - \alpha) \mathbf{E}^{(0)} + \alpha \mathbf{D}^{-1/2} \mathbf{A} \mathbf{D}^{-1/2} \mathbf{E}^{(t)}$$
$$\mathbf{Z}_{final} = \mathbf{Z}^{(0)} + s \cdot \mathbf{E}^{(T)}$$

### 2.2 竞赛级端到端实战代码 (PyG + NetworkX + LightGBM 融合)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv
import networkx as nx
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

# 1. 拓扑特征工程函数 (严格只在训练图结构上提取，防止泄露)
def extract_graph_features(G: nx.Graph, node_list: list) -> np.ndarray:
    """提取节点的局部与全局拓扑标量特征"""
    print("正在计算图拓扑特征 (PageRank, Degree, Clustering, Betweenness)...")
    pagerank = nx.pagerank(G, alpha=0.85)
    degree_dict = dict(G.degree())
    clustering = nx.clustering(G)
    
    features = []
    for node in node_list:
        features.append([
            degree_dict.get(node, 0),
            pagerank.get(node, 0.0),
            clustering.get(node, 0.0)
        ])
    return np.array(features)

# 2. PyG 竞赛级 GraphSAGE 提取高维节点 Embedding
class GraphSAGEEncoder(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GraphSAGEEncoder, self).__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels, aggregator='mean')
        self.conv2 = SAGEConv(hidden_channels, out_channels, aggregator='mean')
        self.dropout = nn.Dropout(0.3)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        return x

# 3. GNN 与 GBDT 的竞赛融合 Pipeline 框架
def train_kaggle_graph_pipeline(data, labels, train_mask, test_mask):
    """
    data: PyG Data 对象 (包含 x, edge_index)
    labels: 节点分类标签
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = GraphSAGEEncoder(data.num_features, 64, 32).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    
    # 训练 GraphSAGE Encoder
    data = data.to(device)
    model.train()
    for epoch in range(1, 101):
        optimizer.zero_grad()
        out = model(data.x, data.edge_index)
        loss = F.cross_entropy(out[train_mask], labels[train_mask])
        loss.backward()
        optimizer.step()
        
    # 获取 GNN 输出的低维节点 Embedding
    model.eval()
    with torch.no_grad():
        gnn_embeddings = model(data.x, data.edge_index).cpu().numpy()
        
    # 构建训练图并提取 NetworkX 拓扑特征
    G = nx.Graph()
    train_edges = data.edge_index.cpu().numpy().T
    G.add_edges_from(train_edges)
    topo_features = extract_graph_features(G, list(range(data.num_nodes)))
    
    # 特征拼接: [原始属性特征 | GNN Embeddings | 手工拓扑特征]
    raw_x = data.x.cpu().numpy()
    X_full = np.hstack([raw_x, gnn_embeddings, topo_features])
    y_full = labels.cpu().numpy()
    
    # 5-Fold Cross Validation + LightGBM 拟合
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    oof_preds = np.zeros(train_mask.sum().item())
    test_preds = np.zeros(test_mask.sum().item())
    
    X_train_val = X_full[train_mask.cpu().numpy()]
    y_train_val = y_full[train_mask.cpu().numpy()]
    X_test = X_full[test_mask.cpu().numpy()]
    
    for fold, (train_idx, val_idx) in enumerate(skf.split(X_train_val, y_train_val)):
        X_tr, y_tr = X_train_val[train_idx], y_train_val[train_idx]
        X_va, y_va = X_train_val[val_idx], y_train_val[val_idx]
        
        clf = lgb.LGBMClassifier(n_estimators=300, learning_rate=0.05, random_state=42)
        clf.fit(X_tr, y_tr, eval_set=[(X_va, y_va)], callbacks=[lgb.early_stopping(50, verbose=False)])
        
        oof_preds[val_idx] = clf.predict_proba(X_va)[:, 1]
        test_preds += clf.predict_proba(X_test)[:, 1] / 5.0
        
    print(f"OOF AUC Score: {roc_auc_score(y_train_val, oof_preds):.4f}")
    return test_preds
```

## 3. 具体应用案例
**场景**：Kaggle 某电商异构图反作弊竞赛（Heterogeneous Anti-Fraud Link Prediction）。

1. **业务问题**：给定由“买家-商家-设备IP-银行卡”构建的异构图，预测指定买家与商家之间是否存在虚假交易刷单行为（链路预测任务）。
2. **特征解构**：
   - **节点属性**：用户注册时长、设备类型、历史消费金额。
   - **拓扑特征**：用户与商家在异构图中的 2-Hop 路径条数（Meta-path: User-IP-User-Merchant）、Adamic-Adar 重叠分、PageRank 值。
3. **模型融合攻防战**：
   - 使用 RGCN / HeteroSage 提取异构图的节点表征向量。
   - 将抽取出的异构向量作为新列喂给 CatBoost / LightGBM 树模型。
   - 应用 Post-Processing 标签传播：若某团伙内部多个节点已被标记为黑产，将该团伙内未标记节点的异常得分进行图上扩散加权。
4. **竞赛结果**：该组合拳方案成功解决纯 GNN 无法很好拟合连续数值属性、以及纯树模型丢失高阶拓扑关联的瓶颈，提升 AUC 分数约 3.2%。

## 4. 常见误区与陷阱 (Pitfalls)
> [!WARNING] 踩坑预警
> - **误区 1：跨验证集全局提取图拓扑特征导致严重穿越（Transductive Leakage）**
>   在计算全局 PageRank、Degree 或训练 Node2Vec 时，直接在包含 Validation/Test 边的完整图上执行。这会导致线下 5-Fold CV AUC 高达 0.98，但提交到 Kaggle Leaderboard 时因穿越无效而直接暴跌。**必须在每一折 CV 内重新切割图结构提取特征**。
> - **误区 2：盲目堆叠深层 GNN 导致过平滑（Over-smoothing）**
>   在 8 层以上的 GCN 中，节点表征收敛至均匀状态，失掉区分度。应对策略：引入 JK-Net (Jumping Knowledge Hub)、APPNP、Residual Connections 或 改用 Graph Transformer。
> - **误区 3：只依赖深度 GNN，忽略 GBDT + 手工图特征（Hand-crafted Graph Features）**
>   在许多图竞赛（特别是异配图或包含大量表格特征的图数据集）中，LightGBM 吃满 PageRank、K-Hop 邻居重叠度（Jaccard Index, Adamic-Adar）、K-Core 壳数等特征后，表现往往优于未调优的 GNN。最稳妥的冲榜策略是 **GNN + GBDT 双路 Stacking 融合**。

## 5. 跨学科链接与双链
- **上游知识**：
  - [[图机器学习概述]]：提供图表示学习与消息传递机制的基础理论。
  - [[Node2Vec]]：无监督图游走提取节点 Embedding 的经典方法。
  - [[GCN]]：图卷积网络表征提取。
  - [[GraphSAGE]]：归纳式（Inductive）子图采样与邻居聚合。
- **下游知识**：
  - [[OGB图基准数据集]]：Stanford Open Graph Benchmark 官方权威竞赛标准集。
  - [[工业级图推荐系统]]：将 Kaggle 竞赛中的图算法迁移落地到亿级用户推荐场景。
- **跨领域关联**：
  - **金融风控与反欺诈**：黑产洗钱团伙检测（Group Fraud Detection）。
  - **生物医药 (Bioinformatics)**：KDD Cup 分子图（Molecular Graph）活性预测与蛋白质相互作用网络（PPI）。

## 6. 费曼自测清单 (Active Recall)
- [ ] 1. 在 5-Fold Cross Validation 中，对链路预测（Link Prediction）任务进行无泄露切分的具体步骤是什么？
- [ ] 2. 什么是 Correct & Smooth (C&S) 后处理算法？它为什么能在 OGB 榜单上为 GNN 显著提分？
- [ ] 3. 在图特征工程中，Jaccard 相似度、Adamic-Adar 指数和 Resource Allocation 指数分别如何计算？
- [ ] 4. 当面临亿级节点的超大图竞赛时，如何在单机显存受限情况下训练 PyG 模型？（提示：NeighborLoader 采样子图）
