---
sources: ['Pang, B., & Lee, L. (2008). Opinion Mining and Sentiment Analysis. Foundations and Trends in Information Retrieval, 2(1-2), 1-135.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "文本分类与情感分析"
created: 2026-08-06
status: completed
assessment_exempt: false
difficulty: beginner
stage_moc: "[[🧭 阶段3-深度学习NLP基础]]"
upstream: ["[[08-NLP全栈-Seq2Seq与注意力机制]]"]
tags: [学习, NLP, 文本分类, 情感分析, 细粒度情感, 意图识别]
---

# 08-NLP全栈-文本分类与情感分析

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 文本分类是 NLP 中应用最广泛的任务。但在实际工业场景中，文本分类不仅仅是简单的二分类（如垃圾邮件识别），还包含多标签分类 (Multi-label)、细粒度情感分析（Aspect-based Sentiment Analysis, ABSA，如“菜品好吃但服务态度差”）以及意图识别 (Intent Classification)。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是评估几乎所有 NLP 模型的标准下游基准测试（如 GLUE / SuperGLUE 榜单中的 SST-2, MNLI, QQP）。
- **实际应用场景**：电商评论情感挖掘、客服工单智能派单、用户意图识别与槽位填充 (Intent Detection & Slot Filling)。

---

## 3. 分类任务类型与评估范式

### 1. 多标签分类 (Multi-Label Classification)

对于文档 $x$，模型输出概率向量 $\hat{\mathbf{y}} = \sigma(\mathbf{W} \mathbf{h} + \mathbf{b}) \in (0, 1)^C$。每个类别相互独立，损用 **BCEWithLogitsLoss**：

$$\mathcal{L}_{\text{Multi-Label}} = -\frac{1}{C} \sum_{c=1}^C \left[ y_c \log \hat{y}_c + (1 - y_c) \log (1 - \hat{y}_c) \right]$$

### 2. 基于属性的情感分析 (Aspect-Based Sentiment Analysis, ABSA)

给定三元组 $(\text{Text}, \text{Aspect}, \text{Sentiment})$。
例如：句子 `"The pizza is delicious, but the service is terrible."`
- Aspect: `pizza` $\to$ Sentiment: `Positive`
- Aspect: `service` $\to$ Sentiment: `Negative`

---

## 4. Python 代码示例：多标签文本分类训练片段

```python
import torch
import torch.nn as nn

# 模拟 3 个分类任务的多标签 Binary Cross Entropy
logits = torch.tensor([[2.1, -1.2, 0.5], [-0.5, 3.1, 1.8]])
targets = torch.tensor([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]]) # Multi-hot

loss_fn = nn.BCEWithLogitsLoss()
loss = loss_fn(logits, targets)

# 转换概率与二值化预测
probs = torch.sigmoid(logits)
predictions = (probs > 0.5).float()

print("Loss:", loss.item())
print("Probabilities:\n", probs)
print("Binary Predictions:\n", predictions)
```

---


## 5. 常见误区与对比矩阵

| 评估维度 / 特性 | 方案 A / 经典范式 | 方案 B / 改进范式 | 权衡与选型建议 (Trade-offs) |
| :--- | :--- | :--- | :--- |
| **计算复杂度** | $\mathcal{O}(N^2)$ 或传统高阶复杂度 | $\mathcal{O}(N \log N)$ 或近似线性复杂度 | 高并发生产环境优先选择低复杂度方案 |
| **显存 / 存储占用** | 占用较高，受限于序列长度/维度 | 优化压缩，支持 Memory-efficient | 边缘设备或资源受限场景推荐优化方案 |
| **表征能力与精度** | 基础表达，易受局部噪声干扰 | 强特征提取，捕捉长距离依赖 | 高精度需求任务（如长文本理解/生成）推荐改进范式 |
| **工程落地门槛** | 开箱即用，工具链极为成熟 | 需特定依赖库 (如 CUDA / Triton) | 开发初期快速原型验证使用经典范式 |


## 5. 原有补全内容与 常见误区与易错点

### 误区：使用 `Softmax` 解决多标签分类问题
- **错误**：Softmax 会强制所有类别的概率和为 1，产生类别间的竞争抑制。在**多标签分类中必须对每个类别单独施加 Sigmoid**。

---

## 🛠️ 学完后可以完成

### 派生作业与验收入口
```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

### 关联下游知识点
```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/08-NLP全栈"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

---

## 7. 参考文献与延伸阅读

- Pang, B., & Lee, L. (2008). Opinion Mining and Sentiment Analysis. *Foundations and Trends in Information Retrieval*, 2(1-2), 1-135.


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《文本分类与情感分析》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《文本分类与情感分析》的核心机制及其与上下游模块的连接逻辑。
2. **代数/代码自测**：手写关键代数推导步骤或 PyTorch/Python 核心实现伪代码。
3. **防错自测**：如果输入数据出现极小值或极大值离群点，该模块会发生什么异常？如何做数值稳定防护？


---

## 🛠️ 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
