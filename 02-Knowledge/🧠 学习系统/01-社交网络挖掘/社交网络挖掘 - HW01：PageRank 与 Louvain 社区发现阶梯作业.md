---
title: "社交网络挖掘-题型-PageRank与Louvain社区发现阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "社交网络挖掘作业"
course: "01-社交网络挖掘"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: intermediate
importance: A
concept: ["图挖掘", "PageRank", "社区发现"]
prerequisites: ["[[01-社交网络挖掘/01-图与网络基础/🕸️ 阶段1：图与网络基础|社交网络挖掘路线]]"]
related: ["[[图神经网络-题型-GCN与GraphSAGE节点分类阶梯作业]]"]
upstream: ["[[01-社交网络挖掘/01-图与网络基础/🕸️ 阶段1：图与网络基础|社交网络挖掘路线]]"]
downstream: []
tags: [学习, 01-社交网络挖掘, 作业, 实战, 阶梯作业]
aliases: ["SNM-HW01-PageRank作业"]
---

# 社交网络挖掘 - HW01：PageRank 与 Louvain 社区发现阶梯作业

> 🎯 **作业目标**：在真实社交图谱中实现幂迭代 PageRank 算法与 Louvain 模块度最大化社区发现算法。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-snm/hw01_pagerank_louvain.ipynb`
- **开源标杆仓库**：[snap-stanford/cs224w-qualification](https://github.com/snap-stanford)
- **核心依赖**：`networkx`, `numpy`, `scipy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 Metric / 验收标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | NetworkX 验证通过 | 计算无标度网络与小世界网络的度分布、聚集系数与介数中心性。 |
| 🟡 **L2 - Medium Baseline** | 阻尼系数 0.85 收敛 | **手写 PageRank 幂迭代算法**，加入 Dead Ends 与 Spider Traps 处理。 |
| 🔴 **L3 - Strong Baseline** | 模块度 Q ≥ 0.45 | **手撕 Louvain 社区发现算法**：局部节点移动与社区聚合两阶段迭代。 |
| 👑 **L4 - Boss Baseline** | 挑选收益 $\ge 1-1/e$ | 模拟独立级联模型 (ICM) 影响力和最大化挑选问题 (贪心算法保证)。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import networkx as nx
import numpy as np

def test_pagerank_convergence():
    G = nx.karate_club_graph()
    from snm_solvers import manual_pagerank
    pr = manual_pagerank(G, alpha=0.85, tol=1e-6)
    
    ref_pr = nx.pagerank(G, alpha=0.85)
    for node in G.nodes():
        assert np.isclose(pr[node], ref_pr[node], atol=1e-4), f"Node {node} PageRank 不匹配"
```

---

## 🃏 Anki 卡片

- Q: Louvain 算法在计算模块度增量 $\Delta Q$ 时，其优化公式的物理含义是什么？
- A: $\Delta Q$ 衡量了将一个节点放入相邻社区后，社区内部连边密度相对于随机期望图连边密度的增加值，增量大于 0 说明合并能增强社区凝聚力。
