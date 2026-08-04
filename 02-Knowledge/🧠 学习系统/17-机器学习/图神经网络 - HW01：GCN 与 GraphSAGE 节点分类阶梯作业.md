---
title: "图神经网络-题型-GCN与GraphSAGE节点分类阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "图神经网络作业"
course: "23-图神经网络"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["图神经网络", "GCN", "GraphSAGE", "Message Passing"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/17-机器学习/🗺️ 机器学习学习路径|机器学习]]"]
related: ["[[社交网络挖掘-题型-PageRank与Louvain社区发现阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/23-图神经网络/🗺️ 图神经网络学习路径|图神经网络学习路径]]"]
downstream: []
tags: [学习, 23-图神经网络, 作业, 实战, 阶梯作业]
aliases: ["GNN-HW01-GCN与GraphSAGE作业"]
---

# 图神经网络 - HW01：GCN 与 GraphSAGE 节点分类阶梯作业

> 🎯 **作业目标**：手写 Node2Vec 生成节点嵌入、手写 Message Passing 消息传递机制、在 PyG 中实现 GCN 与 GraphSAGE 完成 Cora 数据集分类。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-gnn/hw01_gcn_sage.ipynb`
- **开源标杆仓库**：[snap-stanford/cs224w-qualification](https://github.com/snap-stanford) (Stanford CS224W)
- **核心依赖**：`torch`, `torch_geometric` (PyG), `networkx`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 Cora Acc | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | Node2Vec Acc ≥ 68.0% | NetworkX 生成图拓扑，用 Gensim Node2Vec 训练嵌入并用 Logistic Regression 分类。 |
| 🟡 **L2 - Medium Baseline** | Acc ≥ 76.0% | **手写基于 Adjacency Matrix 的单层 GCN 前向传播** $H^{(l+1)} = \sigma(\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}H^{(l)}W^{(l)})$。 |
| 🔴 **L3 - Strong Baseline** | Acc ≥ 81.5% | **在 PyG 中实现 2 层 GraphSAGE (Mean/LSTM Aggregator)** 与 GAT (Graph Attention Network)。 |
| 👑 **L4 - Boss Baseline** | OGB ROC-AUC ≥ 0.79 | 在 Open Graph Benchmark (OGB-MolPCBA / OGBN-ArXiv) 异质图分类任务中冲榜。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import torch

def test_gcn_layer_forward_shape():
    from gnn_layers import GCNConvManual
    conv = GCNConvManual(in_channels=16, out_channels=32)
    
    x = torch.randn(100, 16)
    adj = torch.eye(100) # 恒等邻接矩阵
    out = conv(x, adj)
    
    assert out.shape == (100, 32), "GCN 输出 Shape 必须为 (num_nodes, out_channels)"
```

---

## 🃏 Anki 卡片

- Q: GCN (Graph Convolutional Network) 中的规范化归一化矩阵为何是 $\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}$ 而非仅仅 $\tilde{D}^{-1}\tilde{A}$？
- A: 对称归一化 $\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}$ 在聚合邻居信息时，既考虑了源节点的度，也考虑了目标节点的度，避免高度节点在多层堆叠后特征数值爆炸，保持了谱图卷积在自环修正下的稳定性。
