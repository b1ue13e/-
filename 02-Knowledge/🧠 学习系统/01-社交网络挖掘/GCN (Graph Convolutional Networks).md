---
title: "GCN"
date: 2026-07-31
type: concept
kind: concept
flow: knowledge
course: "01-社交网络挖掘"
importance: "A"
tags: [学习, 核心概念, 图表示学习, GNN]
upstream: ["[[图结构基础]]", "[[谱图理论]]", "[[卷积神经网络]]"]
downstream: ["[[GraphSAGE]]", "[[GAT]]"]
status: learning
---
# GCN (Graph Convolutional Networks)

> [!NOTE] 核心直觉：近朱者赤，近墨者黑
> **类比**：你要想判断一个人的性格和爱好（节点特征），不仅要看他自己（自身特征），还要看他的朋友圈（邻居节点的特征）。GCN 就是通过不断聚合一个人“朋友圈”的特征，来更新对这个人的认知。每一层 GCN，就相当于向外扩展了一圈朋友圈（朋友的朋友）。

## 1. 为什么需要这个知识点？
- **背景**：在现实世界中，很多数据是以非欧几里得空间（Non-Euclidean）的图结构存在的（如社交网络、分子结构、交通网络），而传统的 CNN 主要处理像图像这样的欧几里得网格数据。
- **痛点**：传统的 CNN 无法直接应用于节点度数不固定、没有排列顺序的图结构数据；而早期的网络表示学习（如 DeepWalk, Node2Vec）缺乏对节点自身属性（Feature）的利用，且多为直推式学习，难以泛化。
- **意义**：GCN 成功地将卷积操作推广到了图数据上，完美结合了图的拓扑结构信息和节点的属性特征，是图神经网络（GNN）领域的里程碑式模型。

## 2. 核心定义与公式/代码
GCN 的核心在于如何利用图的邻接矩阵来聚合邻居的信息。

**核心层级传播规则（Layer-wise Propagation Rule）**：
$$H^{(l+1)} = \sigma(\tilde{D}^{-\frac{1}{2}}\tilde{A}\tilde{D}^{-\frac{1}{2}}H^{(l)}W^{(l)})$$

- $\tilde{A} = A + I_N$：带有自环的邻接矩阵（表示节点不仅要考虑邻居，还要保留自己的信息）。
- $\tilde{D}$：$\tilde{A}$ 的度矩阵，其中 $\tilde{D}_{ii} = \sum_j \tilde{A}_{ij}$。
- $\tilde{D}^{-\frac{1}{2}}\tilde{A}\tilde{D}^{-\frac{1}{2}}$：对称归一化的邻接矩阵。它的作用是防止度数很大的节点在聚合时主导了特征分布，使特征尺度保持稳定。
- $H^{(l)}$：第 $l$ 层的节点特征矩阵（$H^{(0)} = X$ 为初始输入特征）。
- $W^{(l)}$：第 $l$ 层的可学习权重矩阵，用于特征维度的变换（特征提取）。
- $\sigma$：非线性激活函数（如 ReLU）。

**PyTorch Geometric (PyG) 核心代码直觉**：
```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class GCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GCN, self).__init__()
        # 定义两层 GCN 卷积层
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        # x: 节点特征矩阵, edge_index: 边索引（图结构）
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)
```

## 3. 具体应用案例
**场景**：论文引用网络的节点分类（如 Cora 数据集）。
在学术网络中，每篇论文是一个节点，论文之间的引用关系构成了边。每篇论文包含一些词汇特征（即节点的初始特征向量），我们需要预测这篇论文属于哪个子领域（如机器学习、自然语言处理等）。
GCN 不仅通过论文自身使用的词汇来判断，还通过这篇论文“引用了哪些其他论文”、“被哪些论文引用”（邻居节点的特征）来进行综合判定，这相比仅依赖文本特征的模型能大幅提高分类准确率。

## 4. 常见误区与陷阱 (Pitfalls)
> [!WARNING] 踩坑预警
> - **认为 GCN 层数越深越好 (过平滑 Over-smoothing)**: 这是一个常见误区。实际上，当 GCN 层数过深（通常超过 3-4 层）时，所有节点的表征会趋同，变得无法区分。因为多次聚合相当于在图上进行全局随机游走，最终所有节点特征趋于稳态分布。
> - **认为 GCN 轻松适用于大图**: 原始的 GCN (Full-batch) 在训练时需要把整个图结构（$\tilde{A}$）和所有节点特征（$X$）加载入内存，这使得它难以直接应用于工业级的亿级规模大图（由此催生了 GraphSAGE 等基于采样的算法）。
> - **忽视了异质性**: 原生 GCN 假定所有节点和边的类型是相同的（同构图），同时也蕴含着“同质性假设”（即相连的节点很可能是同类的）。对于包含多种实体关系的异构图或具有异质性的网络，直接应用效果往往不佳。

## 5. 跨学科链接与双链
- **上游知识**：[[谱图理论]]、[[卷积神经网络 (CNN)]]、[[马尔可夫链]]
- **下游知识**：[[GraphSAGE]] (用于大图的归纳学习)、[[GAT]] (引入注意力机制动态分配邻居权重)、[[Over-smoothing 现象]]
- **跨领域关联**：信号处理（GCN 本质上是一个图上的低通滤波器）、社会学（同质性理论 Homophily）。

## 6. 费曼自测清单 (Active Recall)
- [ ] 为什么要对邻接矩阵进行加自环（$\tilde{A} = A + I$）操作？如果不加会怎样？
- [ ] 为什么要进行对称归一化（$\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}$）而不是简单的行归一化（$D^{-1}A$）？两者效果有何差异？
- [ ] 从信号处理的角度看，GCN 本质上是低通滤波器还是高通滤波器？这对节点特征有什么影响？
- [ ] GCN 为什么会出现过平滑现象（Over-smoothing）？在实际工程中通常有哪些缓解策略？
