---
title: "OGB项目"
date: 2026-07-31
type: concept
kind: concept
flow: knowledge
course: "01-社交网络挖掘"
importance: "A"
tags: [学习, 核心概念, 图神经网络基准]
upstream: ["[[图神经网络框架]]", "[[节点与图分类]]", "[[链路预测算法]]"]
downstream: ["[[大规模图计算]]", "[[异质图神经网络]]", "[[图自监督学习]]"]
status: learning
---

> [!NOTE] 核心直觉：标准化“奥运会竞技场”
> **类比**：OGB（Open Graph Benchmark）就像是图神经网络领域的“奥运会田径场”。在过去，每个科研团队都在自家小区楼下跑步（使用小规模且随机划分的 Karate Club 或 Cora 数据集），随意声称自己跑得最快。而 OGB 统一了跑道规格（标准化图数据集与真实应用场景）、裁判打分标准（定制化评估指标 `Evaluator`）以及入场规则（现实世界时间/域漂移的数据划分），让各类 GNN 模型能在真正的超大规模真实图结构上进行公平、可复现的竞技。

## 1. 为什么需要这个知识点？
- **背景**：早期图神经网络（GNN）研究长期依赖小规模玩具数据集（如 Cora, Citeseer, Pubmed），节点数仅几千个。随着 GNN 在社交网络分析、推荐系统、生物分子建模和知识图谱中的深入应用，模型必须应对千万级节点与十亿级边的大规模真实图。
- **痛点**：
  1. **数据规模失真**：传统数据集规模太小，模型在 Cora 上的表现无法推导至千万级节点的真实社交网络；
  2. **数据划分泄露 (Data Leakage)**：均匀随机划分节点打乱了真实网络的时空与拓扑分布，导致过拟合与性能虚高；
  3. **评估指标混乱**：不同实验室采用不同的 Loss 和 Metrics，缺乏标准化评估框架；
  4. **任务类型单一**：缺乏覆盖节点预测（Node-level）、链路预测（Link-level）和图分类（Graph-level）全栈任务的统一标准库。
- **意义**：OGB（Open Graph Benchmark）由斯坦福大学团队提出，建立了涵盖 Node, Link, Graph 三大层级的现实世界大规模图基准，提供了开箱即用的 Data Loader、领域相关的官方划分方案（如时间划分、分子结构划分）与统一评估器 `Evaluator`，成为现代图机器学习研究与实战工程不可或缺的标准基石。

## 2. 核心定义与公式/代码

### 1. OGB 数据集命名规范与任务架构
OGB 数据集遵循 `ogb[n/l/g]-[dataset]` 的统一命名规范：
- `ogbn-`：**节点级预测 (Node-level)**（例如 `ogbn-arxiv` 计算机论文分类、`ogbn-products` 商品类别预测、`ogbn-mag` 异质图学术网络）
- `ogbl-`：**链路级预测 (Link-level)**（例如 `ogbl-collab` 作者合作链路预测、`ogbl-citation2` 引用关系预测、`ogbl-wikikg2` 知识图谱补全）
- `ogbg-`：**图级预测 (Graph-level)**（例如 `ogbg-molhiv` 分子活性分类、`ogbg-ppa` 生物蛋白质互作分类）

### 2. 核心评估器与指标定义
在链路预测中，由于负样本数量远多于正样本，传统 ROC-AUC 指标容易给出虚高的分数。OGB 在 `ogbl-collab` 等任务中引入了 **Hits@K** 标准评价指标：
$$
\text{Hits@K} = \frac{1}{|E_{\text{eval}}|} \sum_{e=(u,v) \in E_{\text{eval}}} \mathbb{I}\left( \text{Rank}(e) \le K \right)
$$
其中 $E_{\text{eval}}$ 表示评估验证/测试集中的正例边集合，$\text{Rank}(e)$ 为模型对真实正例边 $e$ 在对应负采样候选集（如 100,000 条负例边）中的打分排名，$\mathbb{I}(\cdot)$ 为指示函数。

### 3. OGB + PyTorch Geometric (PyG) 完整实战代码
以下是在 `ogbn-arxiv` 数据集上构建、训练和评估多层 GCN 模型的标准化工作流：

```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from ogb.nodeproppred import PygNodePropPredDataset, Evaluator

# 1. 加载 OGB 标准数据集与官方划分方案
dataset = PygNodePropPredDataset(name='ogbn-arxiv', root='./data')
split_idx = dataset.get_idx_split()  # 获取官方划分索引 ('train', 'valid', 'test')
data = dataset[0]  # PyG Data 对象

# 2. 构建图卷积神经网络 (GCN)
class OGBGCN(torch.nn.Module):
    def __init__(self, in_feats, hidden_feats, out_feats, num_layers, dropout):
        super(OGBGCN, self).__init__()
        self.convs = torch.nn.ModuleList()
        self.convs.append(GCNConv(in_feats, hidden_feats))
        for _ in range(num_layers - 2):
            self.convs.append(GCNConv(hidden_feats, hidden_feats))
        self.convs.append(GCNConv(hidden_feats, out_feats))
        self.dropout = dropout

    def forward(self, x, edge_index):
        for i, conv in enumerate(self.convs[:-1]):
            x = conv(x, edge_index)
            x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.convs[-1](x, edge_index)
        return x.log_softmax(dim=-1)

# 3. 初始化设备、模型、优化器与 OGB Evaluator
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = OGBGCN(
    in_feats=dataset.num_features,
    hidden_feats=256,
    out_feats=dataset.num_classes,
    num_layers=3,
    dropout=0.5
).to(device)

data = data.to(device)
train_idx = split_idx['train'].to(device)
valid_idx = split_idx['valid'].to(device)
test_idx = split_idx['test'].to(device)

optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-5)
evaluator = Evaluator(name='ogbn-arxiv')

# 4. 训练与评估例程
def train():
    model.train()
    optimizer.zero_grad()
    out = model(data.x, data.edge_index)
    loss = F.nll_loss(out[train_idx], data.y[train_idx].squeeze(1))
    loss.backward()
    optimizer.step()
    return loss.item()

@torch.no_grad()
def test():
    model.eval()
    out = model(data.x, data.edge_index)
    y_pred = out.argmax(dim=-1, keepdim=True)
    
    train_acc = evaluator.eval({'y_true': data.y[train_idx], 'y_pred': y_pred[train_idx]})['acc']
    valid_acc = evaluator.eval({'y_true': data.y[valid_idx], 'y_pred': y_pred[valid_idx]})['acc']
    test_acc = evaluator.eval({'y_true': data.y[test_idx], 'y_pred': y_pred[test_idx]})['acc']
    return train_acc, valid_acc, test_acc

# 5. 循环训练
for epoch in range(1, 101):
    loss = train()
    if epoch % 10 == 0 or epoch == 1:
        train_acc, valid_acc, test_acc = test()
        print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}, Train Acc: {train_acc:.4f}, Valid Acc: {valid_acc:.4f}, Test Acc: {test_acc:.4f}')
```

## 3. 具体应用案例
**场景**：学术社交网络论文类别预测与大规模分布偏移评估（`ogbn-arxiv` 项目落地）
- **问题描述**：学术网络拥有大约 17 万篇论文节点与 116 万条有向引用边，每篇论文附带 128 维 Word2Vec 特征，目标是预测 40 个 arXiv CS 子领域。
- **现实挑战与解决方案**：
  1. **基于时间的官方划分 (Time-based Split)**：学报与论文发表具有严格的时间演进特征。OGB 采用按发表年份分割方案：2017 年及之前的论文作为训练集，2018 年作为验证集，2019 年及以后作为测试集。这真实逼近了“用历史论文训练模型预测未来发表论文”的实际落地场景。
  2. **评估指标统一**：通过 `Evaluator(name='ogbn-arxiv')` 输入 `y_true` 与 `y_pred`，自动计算 Top-1 分类准确率（Accuracy），消除了自定义 Metric 造成的评判歧义。
  3. **超大规模扩展 (OGB-LSC)**：对于包含 1 亿节点、13 亿边的 `ogbn-papers100M` 数据集，传统全图卷积无法装入 GPU 显存，结合 PyG 的 `NeighborLoader` 或 GraphSAINT 进行子图采样 Mini-batch 训练成为工业级落地的标准解答。

## 4. 常见误区与陷阱 (Pitfalls)
> [!WARNING] 踩坑预警
> - **[混淆划分机制：弃用 `dataset.get_idx_split()` 而使用随机切分]**：习惯性使用 `train_test_split` 随机打乱节点进行 80/20 划分会导致信息泄露。OGB 的核心优势之一就是提供了符合现实领域特性的划分（如按时间切分、按分子骨架 Scaffolds 切分）。随意重新划分为均匀随机分布将使实验完全失去对比价值。
> - **[形状不匹配与 Evaluator 键名报错]**：`data.y` 在 OGB 中通常以列向量二阶张量 `[N, 1]` 形式存在。在损失函数（如 `F.nll_loss`）计算时需使用 `.squeeze(1)` 展平成一阶 `[N]`；但在传入 `evaluator.eval()` 时，传入字典的键名必须严格匹配官方要求（例如 `{'y_true': y_true, 'y_pred': y_pred}`），且形状需保持 `[N, 1]` 保持一致。

## 5. 跨学科链接与双链
- **上游知识**：
  - [[图神经网络框架]]：PyG (PyTorch Geometric) 与 DGL (Deep Graph Library) 为 OGB 提供了底层计算图与图卷积层实现。
  - [[节点与图分类]]：图拓扑结构与节点属性融合作业的基本概念。
  - [[链路预测算法]]：基于负采样的边预测与排序评价机制。
- **下游知识**：
  - [[大规模图计算]]：处理 OGB-LSC (Large-Scale Challenge) 超大规模图所需的分布式训练与采样策略。
  - [[异质图神经网络]]：如在包含多种节点与边类型的 `ogbn-mag` 异质图上应用 RGCN / HGT 算法。
  - [[图自监督学习]]：在 OGB 无标签/部分标签图上利用 GraphMAE、GraphCL 等模型进行对比学习预训练。
- **跨领域关联**：
  - **AI 制药与生物信息**：OGB 的 `ogbg-molhiv` 与 `ogbg-molpcba` 数据集被广泛用于药物分子活性筛选与小分子性质预测。
  - **知识图谱与语义推理**：OGB 的 `ogbl-wikikg2` 促进了自然语言处理与大规模结构化知识图谱补全。

## 6. 费曼自测清单 (Active Recall)
- [ ] OGB 数据集命名中的 `ogbn`, `ogbl`, `ogbg` 前缀分别对应图机器学习中的哪三种任务层级？
- [ ] 为什么 OGB 链路预测任务（如 `ogbl-collab`）优先采用 Hits@K 评价指标，而非传统的 ROC-AUC？
- [ ] OGB 的官方数据集划分（如基于发表时间或分子骨架划分）相比简单的均匀随机划分解决了什么核心问题？
- [ ] 试写出利用 PyG 和 `ogb.nodeproppred.Evaluator` 完成节点分类预测并计算 Test Accuracy 的核心代码步骤。
