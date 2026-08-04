---
type: study
topic: "GCN"
created: 2026-04-18
updated: 2026-08-01
status: completed
difficulty: advanced
concept: ["图卷积网络", "消息传递", "邻接归一化"]
prerequisites: ["邻接矩阵", "图拉普拉斯矩阵", "神经网络基础"]
related: ["GraphSAGE", "GAT", "GCN推导", "GCN空间域"]
tags: [学习, 社交网络挖掘, GNN]
flow: knowledge
kind: concept
---

# GCN

图卷积网络（Graph Convolutional Network, GCN）把每个节点自身的特征与邻居特征聚合，再进行线性变换和非线性激活。Kipf 与 Welling 的经典两层模型主要用于固定图上的半监督节点分类。

## 1. 一层传播规则

设邻接矩阵为 $A$，节点特征为 $H^{(0)}=X\in\mathbb{R}^{n\times d_0}$。先加入自环：

$$
\tilde A=A+I,
$$

再令 $\tilde D_{ii}=\sum_j\tilde A_{ij}$，作对称归一化：

$$
\hat A=\tilde D^{-1/2}\tilde A\tilde D^{-1/2}.
$$

第 $\ell$ 层为

$$
H^{(\ell+1)}=\sigma\!\left(\hat A H^{(\ell)}W^{(\ell)}\right).
$$

维度追踪：若 $H^{(\ell)}\in\mathbb{R}^{n\times d_\ell}$、$W^{(\ell)}\in\mathbb{R}^{d_\ell\times d_{\ell+1}}$，则输出为 $n\times d_{\ell+1}$。$\hat A$ 负责聚合邻域，$W$ 负责特征变换。

## 2. 为什么加入自环和归一化

- 加入 $I$：节点更新时保留自身信息。
- 对称归一化：抑制度数大的节点在求和聚合中产生过大尺度，并保持与谱图卷积推导的一致形式。
- 多层堆叠：一层接收一跳邻居信息，$L$ 层最多传播到 $L$ 跳邻域，但深层会带来过平滑和训练困难。

## 3. 两层节点分类

经典形式为

$$
Z=\operatorname{softmax}\!\left(\hat A\,\operatorname{ReLU}(\hat A XW^{(0)})W^{(1)}\right).
$$

损失只在有标签节点集合 $\mathcal{V}_L$ 上计算：

$$
\mathcal L=-\sum_{i\in\mathcal V_L}\sum_c Y_{ic}\log Z_{ic}.
$$

无标签节点虽然不直接进入监督损失，但其特征和结构仍参与消息传播。

## 4. 最小实现与形状验证

```python
import torch
from torch_geometric.nn import GCNConv

n, in_dim, hidden, classes = 6, 4, 8, 3
x = torch.randn(n, in_dim)
edge_index = torch.tensor([[0, 1, 1, 2, 2, 3],
                           [1, 0, 2, 1, 3, 2]])

conv1 = GCNConv(in_dim, hidden)
conv2 = GCNConv(hidden, classes)
h = torch.relu(conv1(x, edge_index))
logits = conv2(h, edge_index)

assert h.shape == (n, hidden)
assert logits.shape == (n, classes)
```

数据划分应避免泄露：如果边或节点来自时间演化网络，训练时不能使用未来才出现的结构。

## 5. 适用边界

1. 经典 GCN 偏好相邻节点标签或特征相似的同配图；异配图上简单平滑可能有害。
2. 全图转导训练不能直接声称能泛化到完全未见的新图；归纳任务通常考虑[[GraphSAGE]]等设计。
3. 层数增加不等于感受野信息持续增加；过平滑会使节点表示趋同。
4. 稠密邻接矩阵成本高，工程实现应使用稀疏边索引或稀疏矩阵乘法。

## 参考资料

- Kipf, T. N. & Welling, M. *Semi-Supervised Classification with Graph Convolutional Networks*, ICLR 2017, arXiv:1609.02907：https://arxiv.org/abs/1609.02907
- PyTorch Geometric `GCNConv` 官方文档：https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.nn.conv.GCNConv.html

