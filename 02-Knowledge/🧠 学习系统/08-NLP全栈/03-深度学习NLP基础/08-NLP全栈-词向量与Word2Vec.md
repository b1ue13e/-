---
sources: ['Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). Efficient Estimation of Word Representations in Vector Space. ICLR 2013.', 'Mikolov, T., Sutskever, I., Chen, K., Corrado, G. S., & Dean, J. (2013). Distributed Representations of Words and Phrases and their Compositionality. NeurIPS 2013.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "词向量与Word2Vec"
created: 2026-08-06
status: completed
assessment_exempt: false
difficulty: intermediate
stage_moc: "[[🧭 阶段3-深度学习NLP基础]]"
upstream: ["[[08-NLP全栈-文本表示方法]]"]
tags: [学习, NLP, 词向量, Word2Vec, Skip-gram, CBOW, 负采样]
---

# 08-NLP全栈-词向量与Word2Vec

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> One-hot 编码维度极高且彼此正交，无法表示 `king` 与 `queen`、`apple` 与 `pear` 之间的语义相似度与代数线性运算关系（如 $\text{Vector}("king") - \text{Vector}("man") + \text{Vector}("woman") \approx \text{Vector}("queen")$）。Word2Vec（分布式假说）解决了将离散词高效映射到低维稠密向量空间的问题。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是 NLP 深度学习革命的奠基石，奠定了分布式词嵌入 (Word Embedding)、负采样 (Negative Sampling) 损失函数及语义向量几何结构。
- **实际应用场景**：词语语义相似度计算、近义词推荐、Embedding 预训练权重初始化。

---

## 3. 正式定义与核心公式

Word2Vec 包含两大模型架构与两大加速算法：

### 1. 架构：Skip-gram vs CBOW

- **Skip-gram**：根据中心词 $w_t$ 预测上下文词 $w_{t+j}$（小语料/罕见词效果好）：
  $$\mathcal{L}_{\text{Skip-gram}} = \sum_{t=1}^T \sum_{-c \le j \le c, j \neq 0} \log P(w_{t+j} \mid w_t)$$

- **CBOW (Continuous Bag-of-Words)**：根据上下文词预测中心词 $w_t$（训练速度更快）。

### 2. 目标函数与负采样 (Negative Sampling)

原始 Softmax 分母需对全词表求和，开销为 $\mathcal{O}(|V|)$。负采样将其转化为二分类判定问题，将开销降低为 $\mathcal{O}(K)$（$K$ 为负样本数，通常取 $5 \sim 20$）：

$$\log P(w_o \mid w_c) = \log \sigma(\mathbf{v}'_{w_o} \cdot \mathbf{v}_{w_c}) + \sum_{i=1}^K \mathbb{E}_{w_i \sim P_n(w)} \left[ \log \sigma(-\mathbf{v}'_{w_i} \cdot \mathbf{v}_{w_c}) \right]$$

其中负采样分布为一元词频的 $3/4$ 次方：$P_n(w) \propto f(w)^{0.75}$。

---

## 4. PyTorch 手写 Skip-gram 负采样最小实现

```python
import torch
import torch.nn as nn

class SkipGramNegativeSampling(nn.Module):
    def __init__(self, vocab_size, embed_dim):
        super().__init__()
        # 中心词向量矩阵 与 上下文向量矩阵
        self.in_embed = nn.Embedding(vocab_size, embed_dim)
        self.out_embed = nn.Embedding(vocab_size, embed_dim)

    def forward(self, center_words, pos_words, neg_words):
        # center: [B], pos: [B], neg: [B, K]
        v_c = self.in_embed(center_words)    # [B, D]
        v_pos = self.out_embed(pos_words)   # [B, D]
        v_neg = self.out_embed(neg_words)   # [B, K, D]

        # 1. 正样本点积损失 (越大越好)
        pos_score = torch.sum(v_c * v_pos, dim=1) # [B]
        pos_loss = -torch.log(torch.sigmoid(pos_score) + 1e-8)

        # 2. 负样本点积损失 (越小越好)
        neg_score = torch.bmm(v_neg, v_c.unsqueeze(2)).squeeze(2) # [B, K]
        neg_loss = -torch.sum(torch.log(torch.sigmoid(-neg_score) + 1e-8), dim=1)

        return torch.mean(pos_loss + neg_loss)

# 测试模型初始化与前向传递
model = SkipGramNegativeSampling(vocab_size=10000, embed_dim=128)
center = torch.tensor([12, 45])
pos = torch.tensor([13, 46])
neg = torch.tensor([[100, 200, 300, 400, 500], [101, 201, 301, 401, 501]])

loss = model(center, pos, neg)
print("Skip-gram Loss:", loss.item())
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

### 误区：Word2Vec 能区分同一个词在不同上下文中的多义性
- **局限性（静态词向量）**：Word2Vec 为每个词分配**固定的唯一向量**。例如 `Apple`（苹果公司）与 `apple`（水果苹果）在向量空间中被强行平均压缩为一个点。多义性问题的解决需要后续的上下文动态词向量（如 ELMo、BERT）。

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

- Mikolov, T., et al. (2013). Efficient Estimation of Word Representations in Vector Space. *ICLR 2013*.
- Mikolov, T., et al. (2013). Distributed Representations of Words and Phrases and their Compositionality. *NeurIPS 2013*.


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《词向量与Word2Vec》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《词向量与Word2Vec》的核心机制及其与上下游模块的连接逻辑。
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
