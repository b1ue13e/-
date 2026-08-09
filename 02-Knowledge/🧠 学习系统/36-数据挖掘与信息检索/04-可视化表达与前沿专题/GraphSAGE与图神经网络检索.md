---
type: study
topic: "GraphSAGE与图神经网络检索"
course: "数据挖掘与信息检索"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段4-可视化表达与前沿专题]]"
flow: knowledge
kind: concept
upstream: ["[[PageRank与链接分析]]", "[[稠密检索与向量召回]]"]
tags: [学习, 数据挖掘与信息检索]
---
## 💡 动机与直觉

在海量电商搜索与推荐、学术文献检索、社交网络挖掘场景中，数据不仅存在文本特征，更天然构成了庞大的异质图（如“用户-查询-商品”三元图、“网页-超链接”图）。

- **传统图嵌入（DeepWalk / Node2Vec）缺陷**：属于直推式（Transductive），无法泛化到新节点，且更新全图节点 Embeddings 的开销极大。
- **GraphSAGE (Sample and Aggregate)**：归纳式（Inductive）图神经网络。通过在节点局部 $k$-阶邻域进行**随机采样（Sampling）**与**邻居特征聚合（Aggregation）**，无需在内存中维护全图矩阵，即可为未见节点（Out-of-Vocabulary / New Item）实时生成高性能的低维表征 Vector，直接喂给后端 ANN 稠密向量索引。

```
目标节点 v ──▶ 1 阶邻居均匀采样 (如 5 个) ──▶ 2 阶邻居均匀采样 (如 10 个)
                     │                                 │
                     ▼                                 ▼
             特征聚合 Aggregator               特征聚合 Aggregator
                     └───────────────┬─────────────────┘
                                     ▼
                        产生节点 v 的 Embedding Vector
```

---

## 📐 算法原理与数学表达

### 1. 前向传播与邻居聚合方程

对于图中的节点 $v \in V$，其在第 $k$ 层的状态更新公式如下：

1. **邻居采样与聚合**：
   $$h_{\mathcal{N}(v)}^{(k)} = \text{AGGREGATE}_k \left( \left\{ h_u^{(k-1)}, \forall u \in \mathcal{N}(v) \right\} \right)$$

2. **状态拼接与非线性更新**：
   $$h_v^{(k)} = \sigma \left( W^{(k)} \cdot \left[ h_v^{(k-1)} \,||\, h_{\mathcal{N}(v)}^{(k)} \right] \right)$$

3. **L2 归一化**：
   $$h_v^{(k)} = \frac{h_v^{(k)}}{\|h_v^{(k)}\|_2}$$

### 2. 常用聚合函数 (Aggregators)
- **Mean Aggregator**：邻居向量算术平均（类似 GCN）。
- **LSTM Aggregator**：具备更强的表达能力，需先对邻居进行随机洗牌。
- **Pooling (Max-Pooling) Aggregator**：先对每个邻居通过多层感知机 (MLP) 变换，再按维度取最大值：

$$\text{AGGREGATE}_k^{\text{pool}} = \max_{u \in \mathcal{N}(v)} \left( \sigma (W_{\text{pool}} h_u^{(k-1)} + b) \right)$$

---

## 💻 最小 Python / PyTorch 实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class GraphSAGELayer(nn.Module):
    def __init__(self, in_features: int, out_features: int):
        super(GraphSAGELayer, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        # 拼接自身与聚合邻居后映射变换
        self.weight = nn.Linear(in_features * 2, out_features, bias=False)

    def forward(self, self_feats: torch.Tensor, neighbor_feats: torch.Tensor) -> torch.Tensor:
        """
        self_feats: [batch_size, in_features]
        neighbor_feats: [batch_size, num_neighbors, in_features]
        """
        # Mean Aggregator
        aggregated_neighbors = torch.mean(neighbor_feats, dim=1)  # [batch_size, in_features]

        # 拼接自身与邻居特征
        combined = torch.cat([self_feats, aggregated_neighbors], dim=1)

        # 线性映射 + ReLU 激活
        out = self.weight(combined)
        out = F.relu(out)

        # L2 归一化
        out = F.normalize(out, p=2, dim=1)
        return out

# 验证测试
if __name__ == "__main__":
    layer = GraphSAGELayer(in_features=16, out_features=32)
    batch_size = 4
    num_neighbors = 5

    # 随机模拟节点与邻居特征
    node_x = torch.randn(batch_size, 16)
    neighbors_x = torch.randn(batch_size, num_neighbors, 16)

    output_embeddings = layer(node_x, neighbors_x)
    print("GraphSAGE 输出节点向量尺寸:", output_embeddings.shape)
    assert output_embeddings.shape == (batch_size, 32)
```

---

## ⚠️ 常见误区与避坑指南

1. **误区：全图全邻居参与卷积**
   - 避坑：工业级 GraphSAGE 成功的前提是**固定采样数量**（如 1 阶采 10 个，2 阶采 25 个），否则遇到大 V 节点（度数为数十万）会导致内存爆炸与爆炸式递归计算。

---

## 🃏 Anki 卡片

**Q: GraphSAGE 与传统 DeepWalk 图嵌入相比的核心突破是什么？**
**A**:
- **归纳式学习（Inductive）**：通过训练“采样+聚合”神经网络函数，直接从节点属性和邻居拓扑中预测新节点的 Embedding，无需重训全图，支持海量异质图搜索引擎在线推导。

---

---

## 🔗 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```