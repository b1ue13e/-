import os
import re

vault_dir = r'f:\-\02-Knowledge\🧠 学习系统'

# 1. 最近点对问题处理
p1 = os.path.join(vault_dir, r'10-数据结构与算法\01-算法入门与基本分析\最近点对问题.md')
p2 = os.path.join(vault_dir, r'10-数据结构与算法\05-算法思想进阶\最近点对问题.md')
if os.path.exists(p2):
    content_p2 = f"""---
title: "最近点对问题"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "C类：路由引导"
tags:
  - 学习
  - 数据结构与算法
  - 最近点对问题
upstream:
  - "[[01-算法入门与基本分析/最近点对问题|最近点对问题主卡]]"
status: mastered
topic: "最近点对问题"
created: 2026-07-28
updated: 2026-07-28
flow: knowledge
kind: concept
aliases:
  - "最近点对问题"
---

# 最近点对问题

> **所属课程**：数据结构与算法  
> **理论主卡**：[[01-算法入门与基本分析/最近点对问题|最近点对问题 (01阶段主卡)]]  
> **学习定位**：C类：路由引导（已归并至第一阶段 Canonical 主卡）

---

### 0. 路由引导说明

为了维护全库“唯一概念主卡”治理标准，关于最近点对问题（Closest Pair of Points）的分治法推导、鸽巢原理 6 框剪枝以及 C++ 归并分治代码实现，已统一收录在第一阶段的主卡中：

👉 **请直接跳至理论主卡**：[[01-算法入门与基本分析/最近点对问题|最近点对问题]]
"""
    with open(p2, 'w', encoding='utf-8') as f:
        f.write(content_p2.strip() + '\n')
    print("Handled 重复卡: 最近点对问题")

# 2. LU分解处理
lu1 = os.path.join(vault_dir, r'09-高等代数\04-精通拓展\LU分解.md')
lu2 = os.path.join(vault_dir, r'09-高等代数\04-精通拓展\LU分解_深度补全.md')
if os.path.exists(lu2):
    os.remove(lu2)
    print("Removed 重复卡: LU分解_深度补全.md")

# 3. 多元线性回归模型处理
m1 = os.path.join(vault_dir, r'30-应用回归分析\01-线性回归基础\多元线性回归模型.md')
m2 = os.path.join(vault_dir, r'30-应用回归分析\10-概念笔记\多元线性回归模型-概念卡.md')
if os.path.exists(m2):
    os.remove(m2)
    print("Removed 重复卡: 多元线性回归模型-概念卡.md")

# 4. 度量学习领域应用卡改造
ml_app = os.path.join(vault_dir, r'05-计算机视觉\03-视觉核心任务\度量学习-CV应用.md')
if os.path.exists(ml_app):
    content_ml_app = """---
title: "度量学习-CV应用"
date: 2026-07-28
type: concept
course: 计算机视觉
importance: "A类：领域应用卡"
tags:
  - 学习
  - 计算机视觉
  - 度量学习
  - 图像检索
upstream:
  - "[[度量学习]]"
downstream:
  - "[[计算机视觉]]"
status: learning
topic: "度量学习-CV应用"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "度量学习"
prerequisites:
  - "度量学习"
related:
  - "人脸识别"
flow: knowledge
kind: concept
aliases:
  - "Metric Learning in CV"
---

# 度量学习-CV应用

> **所属课程**：计算机视觉  
> **理论主卡**：[[度量学习]] (机器学习理论主卡)  
> **学习定位**：A类：领域应用卡

---

### 0. 领域应用背景

在计算机视觉中，度量学习（Metric Learning）主要用于**图像检索（Image Retrieval）、人脸识别（Face Verification）与行人重识别（Re-ID）**。
相比于传统的分类任务（Softmax 交叉熵），视觉度量学习的核心目标是：**学习一个卷积嵌入映射 $f(x)$，使同类图像在特征空间中的欧氏距离尽量近，异类图像的距离大于给定的 Margin $\alpha$。**

---

### 1. 经典 Loss 架构：Triplet Loss（三元组损失）

设锚点图像 $a$ (Anchor)、正例图像 $p$ (Positive)、负例图像 $n$ (Negative)：
$$L = \max(0, \ \|f(a) - f(p)\|_2^2 - \|f(a) - f(n)\|_2^2 + \alpha)$$

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class TripletLoss(nn.Module):
    def __init__(self, margin=1.0):
        super(TripletLoss, self).__init__()
        self.margin = margin

    def forward(self, anchor, positive, negative):
        distance_positive = (anchor - positive).pow(2).sum(1)
        distance_negative = (anchor - negative).pow(2).sum(1)
        losses = F.relu(distance_positive - distance_negative + self.margin)
        return losses.mean()
```

---

### 2. 自测题：1 道

#### 1. [CV应用] 为什么在 Open-set 人脸识别（测试集中包含训练集没见过的陌生人）中，不能直接用 Softmax 分类器，而必须采用度量学习？

> [!question]- 答案解析
> **答案**：因为 Softmax 分类器的输出类别数在训练时固定。对于 Open-set 测试集中的未见过的陌生人，系统无法输出新类别索引。度量学习通过比较特征嵌入的欧氏距离/余弦相似度，能够对任意未见过的新样本进行直接对比分类。  
> **Obsidian 标签**：`#自测题 #CV应用`

---

### 3. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/05-计算机视觉`
- **理论主卡**：[[度量学习]]
"""
    with open(ml_app, 'w', encoding='utf-8') as f:
        f.write(content_ml_app.strip() + '\n')
    print("Refactored 度量学习-CV应用.md")

# 5. Skip-gram 领域应用卡改造
sg_app = os.path.join(vault_dir, r'23-图神经网络\01-图学习基础\图学习基础-经典图嵌入-Skip-gram.md')
if os.path.exists(sg_app):
    content_sg_app = """---
title: "Skip-gram-图嵌入应用"
date: 2026-07-28
type: concept
course: 图神经网络
importance: "A类：领域应用卡"
tags:
  - 学习
  - 图神经网络
  - Skip-gram
  - DeepWalk
upstream:
  - "[[Skip-gram]]"
downstream:
  - "[[图神经网络]]"
status: learning
topic: "Skip-gram-图嵌入应用"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "Skip-gram"
prerequisites:
  - "Skip-gram"
related:
  - "随机游走"
flow: knowledge
kind: concept
aliases:
  - "Skip-gram in Graph Embedding"
---

# Skip-gram-图嵌入应用

> **所属课程**：图神经网络  
> **理论主卡**：[[Skip-gram]] (NLP 理论主卡)  
> **学习定位**：A类：领域应用卡

---

### 0. 领域应用背景

在图神经网络（GNN）的前身——经典图嵌入算法（如 DeepWalk、Node2Vec）中，**Skip-gram 模型被直接跨界应用于无向图节点的无监督向量表征**：
- **NLP 中**：句子为词序列，使用 Skip-gram 通过中心词预测上下文词；
- **图学习中**：将节点当作“词”，在图上运行**随机游走（Random Walk）**生成的节点序列作为“句子”，直接使用 Skip-gram 学习节点的低维向量 $z_u$！

---

### 1. 目标函数与负采样

$$\max_{f} \sum_{u \in V} \log P(N(u) \mid f(u))$$
其中 $N(u)$ 是通过随机游走采集到的 $u$ 的邻域节点集合。结合负采样（Negative Sampling）实现线性扩展。

---

### 2. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/23-图神经网络`
- **理论主卡**：[[Skip-gram]]
"""
    with open(sg_app, 'w', encoding='utf-8') as f:
        f.write(content_sg_app.strip() + '\n')
    print("Refactored Skip-gram-图嵌入应用.md")

print("=== ALL CANONICAL MERGES & APPLICATION CARDS EXECUTED SUCCESSFULLY ===")
