---
type: stage
topic: 阶段 5：图表示学习与图神经网络入门
tags:
- 社交网络
- 图表示学习
- GNN
created: 2026-04-11
status: planned
difficulty: intermediate
concept: []
prerequisites: []
related: []
phase: 5
---

# 🧠 阶段 5：图表示学习与图神经网络入门

> "将图的世界映射到向量的海洋，让深度学习读懂网络的语言。"

---

## 📊 阶段进度

```dataviewjs
const total = dv.pages('"🧠 学习系统/01-社交网络挖掘/05-图表示学习与GNN"').length - 1;
const completed = dv.pages('"🧠 学习系统/01-社交网络挖掘/05-图表示学习与GNN"').where(p => p.status === "completed").length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**阶段进度: ${progress}%** (${completed}/${total} 模块)`);
```

---

## 📐 从特征工程到学习

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **为什么需要Embedding** | 传统方法的局限、向量化的优势 | ⬜ | [[为什么需要图嵌入]] |
| **Embedding质量评估** | 可视化、下游任务性能 | ⬜ | [[Embedding评估]] |
| **同构vs异构图** | 单一类型 vs 多类型节点/边 | ⬜ | [[图类型与嵌入]] |

---

## 🚶 浅层嵌入方法

| 算法 | 核心思想 | 游走策略 | 复杂度 | 状态 | 笔记 |
|:---|:---|:---|:---:|:---:|:---|
| **DeepWalk** | 随机游走+Word2Vec | 均匀随机 | O(n) | ⬜ | [[DeepWalk]] |
| **Node2Vec** | 有偏随机游走 | BFS/DFS平衡 | O(n) | ⬜ | [[Node2Vec]] |
| **LINE** | 一阶+二阶邻近度 | 边采样 | O(n) | ⬜ | [[LINE]] |
| **SDNE** | 自编码器重构 | 邻接矩阵 | O(n²) | ⬜ | [[SDNE]] |
| **Struc2Vec** | 结构等价性 | 结构相似度游走 | O(n²) | ⬜ | [[Struc2Vec]] |

### 🎯 实践任务
- [ ] 实现DeepWalk算法
- [ ] 对比不同游走策略的效果
- [ ] 可视化节点嵌入（t-SNE/UMAP）

---

## 🧠 深度学习进阶：图神经网络

### 基础模型

| 模型 | 核心思想 | 聚合方式 | 时间 | 状态 | 笔记 |
|:---|:---|:---|:---:|:---:|:---|
| **GCN** | 谱域卷积近似 | 均值聚合 | 2016 | ⬜ | [[GCN]] |
| **GraphSAGE** | 归纳式学习 | 采样聚合 | 2017 | ⬜ | [[GraphSAGE]] |
| **GAT** | 注意力机制 | 注意力加权 | 2018 | ⬜ | [[GAT]] |
| **GIN** | 图同构网络 | 可区分图结构 | 2019 | ⬜ | [[GIN]] |

### GCN深入理解

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **谱图理论基础** | 图傅里叶变换、拉普拉斯 | ⬜ | [[谱图理论]] |
| **ChebNet到GCN** | 切比雪夫多项式近似 | ⬜ | [[GCN推导]] |
| **空间域理解** | 邻居特征聚合视角 | ⬜ | [[GCN空间域]] |

### GraphSAGE详解

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **归纳式学习** | 训练未见节点 | ⬜ | [[归纳式GNN]] |
| **邻居采样** | 固定采样数量 | ⬜ | [[邻居采样]] |
| **聚合器设计** | Mean/LSTM/Pool | ⬜ | [[GraphSAGE聚合器]] |

### 图注意力网络 (GAT)

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **注意力机制** | Self-Attention on Graph | ⬜ | [[图注意力机制]] |
| **多头注意力** | Multi-head GAT | ⬜ | [[多头GAT]] |
| **与Transformer对比** | 图结构 vs 序列 | ⬜ | [[GATvsTransformer]] |

---

## 🛠️ 工具进阶：PyTorch Geometric

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **PyG安装配置** | CUDA支持、依赖安装 | ⬜ | [[PyG安装]] |
| **Data对象** | 图数据的表示 | ⬜ | [[PyG Data]] |
| **Dataset加载** | 内置数据集、自定义数据 | ⬜ | [[PyG Dataset]] |
| **Message Passing** | 消息传递基类 | ⬜ | [[PyG MP]] |
| **自定义GNN层** | 实现自定义传播 | ⬜ | [[自定义GNN]] |
| **训练流程** | 节点/边/图级任务 | ⬜ | [[PyG训练]] |

### 🎯 实践任务
- [ ] 用PyG实现节点分类（Cora数据集）
- [ ] 实现链接预测任务
- [ ] 自定义一个GNN层

---

## 🔮 前沿方向

| 方向 | 核心挑战 | 代表工作 | 状态 | 笔记 |
|:---|:---|:---|:---:|:---|
| **大规模图训练** | 显存限制、效率 | Cluster-GCN, GraphSAINT | ⬜ | [[大规模GNN]] |
| **动态图神经网络** | 时序演化 | DCRNN, STGNN | ⬜ | [[动态GNN]] |
| **图Transformer** | 全局注意力 | GraphTransformer | ⬜ | [[图Transformer]] |
| **知识图谱嵌入** | 多关系建模 | TransE, RotatE | ⬜ | [[KGE]] |

---

## 📝 学习清单

```dataviewjs
dv.table(
    ["主题", "类型", "状态", "更新日期"],
    dv.pages('"🧠 学习系统/01-社交网络挖掘/05-图表示学习与GNN"')
        .where(p => !p.file.path.includes("🧠"))
        .sort(p => p.file.name)
        .map(p => [
            p.file.link,
            p.topic || "-",
            p.status || "ongoing",
            p.file.mtime.toFormat("yyyy-MM-dd")
        ])
);
```

---

## 🔗 阶段导航

| ⬅️ 上一阶段 | 📋 总览 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| [[🧠 学习系统/01-社交网络挖掘/05-图表示学习与GNN/🌊 阶段4：传播建模与应用|返回阶段4]] | [[🗺️ 社交网络挖掘学习路径\|返回总览]] | [[🎯 综合实战板块\|进入实战]] |

---

## 📚 必读论文

1. **DeepWalk** (KDD 2014) - 图嵌入开山之作
2. **Node2Vec** (KDD 2016) - 有偏随机游走
3. **GCN** (ICLR 2017) - 图卷积网络
4. **GraphSAGE** (NeurIPS 2017) - 归纳式图学习
5. **GAT** (ICLR 2018) - 图注意力网络

---

*阶段创建：2026-04-11*
