---
title: "图神经网络与社交网络挖掘 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "图神经网络 4-Tier 阶梯作业规范"
course: "图神经网络"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [图神经网络, 社交网络挖掘, 4Tier作业, 阶梯作业, 编程实战, PyTest, CS224W]
---

# 🕸️ 图神经网络与社交网络挖掘 4-Tier 阶梯作业全景规范说明书 (Stanford CS224W 范式)

> 本说明书为 **01-社交网络挖掘** 与 **23-图神经网络** 路径（基于 Leskovec 《Networks, Crowds, and Markets》与 Stanford CS224W）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ PyTorch Geometric (PyG) / NetworkX 调包 / 节点度数与 PageRank 计算
🟡 L2 - Medium Baseline   │ Node2Vec / DeepWalk 嵌入 / GCN 分类与链路预测
🔴 L3 - Strong Baseline   │ [核心] 不调用 PyG 库，从零手撕 PageRank 幂迭代 / GCN 邻接矩阵归一化 / GraphSAGE 采样聚合
👑 L4 - Boss Baseline     │ 异质图 (Heterogeneous Graph) 建模 / 异配图 (Heterophily) 优化 / GNN 解释性 (GNNExplainer)
```

---

## 🎯 GNN & 社交网络阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 图统计学与 PageRank 算法 (PageRank & Network Statistics)
- **开源溯源**：Stanford CS224W Homework 1
- 🟢 **L1**: 使用 NetworkX 计算 Karate Club 图的节点度数分布 (Degree Distribution)、聚类系数 (Clustering Coefficient) 与介数中心性 (Betweenness Centrality)。
- 🟡 **L2**: 计算 Katz 中心性与 Personalized PageRank (PPR)。
- 🔴 **L3 (手撕核心)**：**从零手撕带阻尼系数 $\beta=0.85$ 的 PageRank 幂迭代 (Power Iteration) 矩阵求解算法**：
  $$ r = \beta M r + \frac{1-\beta}{N} \mathbf{1} $$
- 👑 **L4**: 实现分布式 Random Walk with Restart (RWR) 大规模图采样。

### 2. HW02 - 节点表征学习与随机游走 (Node Embeddings: DeepWalk & Node2Vec)
- **开源溯源**：Stanford CS224W Homework 2 / Colab 1
- 🟢 **L1**: 使用 Gensim / Node2Vec 包生成 128 维节点嵌入。
- 🟡 **L2**: 在 2D 平面上使用 t-SNE 可视化节点嵌入，并运行 Logistic Regression 节点分类。
- 🔴 **L3 (手撕核心)**：**手撕带 $p$ (Return Parameter) 与 $q$ (In-out Parameter) 偏置的 2nd-order Random Walk 游走采样逻辑**。
- 👑 **L4**: 实现 Graph factorization 矩阵分解嵌入 (Laplacian Eigenmaps)。

### 3. HW03 - 卷积图神经网络 (Graph Convolutional Networks - GCN)
- **开源溯源**：Kipf & Welling (ICLR 2017) / CS224W Colab 2
- 🟢 **L1**: 使用 PyTorch Geometric `GCNConv` 在 Cora 数据集上跑通节点分类。
- 🟡 **L2**: 加入 Dropout、Self-Loops 与 2-Layer GCN 调参。
- 🔴 **L3 (手撕核心)**：**手撕对称归一化拉普拉斯矩阵 (Symmetric Normalized Laplacian) 核心算子**：
  $$ \tilde{A} = A + I_N, \quad \tilde{D}_{ii} = \sum_j \tilde{A}_{ij}, \quad \hat{A} = \tilde{D}^{-1/2} \tilde{A} \tilde{D}^{-1/2} $$
  使用 PyTorch 原生 sparse 矩阵乘法求解 $H^{(l+1)} = \sigma(\hat{A} H^{(l)} W^{(l)})$。
- 👑 **L4**: 证明 2-Layer GCN 与 Weisfeiler-Lehman (1-WL) 图同构检验的等价性。

### 4. HW04 - 归纳式图神经网络与采样 (GraphSAGE & Neighbor Sampling)
- **开源溯源**：Hamilton et al. (NIPS 2017) / CS224W Colab 3
- 🟢 **L1**: 使用 PyG `SAGEConv` 跑通 Inductive (归纳式) 节点分类。
- 🟡 **L2**: 对比 Mean, LSTM, Pool 三种聚合函数 (Aggregators)。
- 🔴 **L3 (手撕核心)**：**手撕分层邻居均匀采样算法 (Layer-wise Uniform Neighbor Sampling)**：
  $$ h_v^{(k)} = \sigma \left( W \cdot \text{CONCAT}\left(h_v^{(k-1)}, \text{AGG}\left(\{h_u^{(k-1)}, \forall u \in N(v)\}\right)\right) \right) $$
- 👑 **L4**: 实现 Cluster-GCN / GraphSAINT 大图训练分区。

### 5. HW05 - 图注意力网络 (Graph Attention Networks - GAT)
- **开源溯源**：Veličković et al. (ICLR 2018) / CS224W Colab 4
- 🟢 **L1**: 使用 PyG `GATConv` 实现多头注意力图节点分类。
- 🟡 **L2**: 绘制注意力系数 $\alpha_{ij}$ 热力图，解释邻居贡献度。
- 🔴 **L3 (手撕核心)**：**手撕单头与多头 Graph Attention 矩阵计算**：
  $$ \alpha_{ij} = \frac{\exp\left(\text{LeakyReLU}\left(\mathbf{a}^T [W h_i \| W h_j]\right)\right)}{\sum_{k \in N_i} \exp\left(\text{LeakyReLU}\left(\mathbf{a}^T [W h_i \| W h_k]\right)\right)} $$
- 👑 **L4**: 实现 Heterogeneous Graph Attention Network (HAN)。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-gnn/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-gnn/tests/test_hw01_pagerank.py
pytest 03-Projects/projects-gnn/tests/test_hw03_gcn.py
pytest 03-Projects/projects-gnn/tests/test_hw05_gat.py
```
