---
sources: ['Sutskever, I., Vinyals, O., & Le, Q. V. (2014). Sequence to Sequence Learning with Neural Networks. NeurIPS 2014.', 'Bahdanau, D., Cho, K., & Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. ICLR 2015.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "Seq2Seq与注意力机制"
created: 2026-08-06
status: completed
assessment_exempt: false
difficulty: intermediate
stage_moc: "[[🧭 阶段3-深度学习NLP基础]]"
upstream: ["[[08-NLP全栈-循环神经网络RNN]]"]
tags: [学习, NLP, Seq2Seq, Encoder-Decoder, Attention, 机器翻译, 教师迫导]
---

# 08-NLP全栈-Seq2Seq与注意力机制

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 序列标注任务要求输入与输出长度完全相同（$N \to N$）。然而在机器翻译、文本摘要、对话系统中，输入句子长度与输出句子长度往往不同（如英文 "Thank you" 对应中文 "谢谢你"），且存在词序倒置与重排。Seq2Seq (Encoder-Decoder) 架构解决了不等长变长序列到变长序列的映射问题。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是机器翻译、Auto-regressive 文本生成、Teacher Forcing（教师迫导）训练机制及现代 Transformer Encoder-Decoder (T5 / BART) 的原型范式。
- **实际应用场景**：神经机器翻译 (NMT)、自动摘要生成、问答系统、代码生成。

---

## 3. 正式定义与 Seq2Seq 机制

### 1. Encoder-Decoder 结构

- **Encoder**：将变长源序列 $\mathbf{x} = (x_1, \dots, x_T)$ 编码为隐藏状态 $h_1, \dots, h_T$。
- **Decoder**：基于上下文向量 $c$ 逐字自回归解码生成目标序列 $\mathbf{y} = (y_1, \dots, y_{T'})$：

$$P(y_t \mid y_{<t}, \mathbf{x}) = \text{softmax}\left( \text{Decoder}(y_{t-1}, s_t, c_t) \right)$$

### 2. Teacher Forcing (教师迫导) 训练策略

在训练阶段，Decoder 的输入不是上一步模型预测的概率最高词 $\hat{y}_{t-1}$，而是**真实目标标签 $y_{t-1}^*$**（Ground Truth），以加速模型收敛并稳定梯度。在推理阶段才切换为自回归解码。

---

## 4. PyTorch 实践：带有 Attention 的 Seq2Seq 解码器

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class BahdanauAttentionDecoder(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        # 匹配 Query (s_{t-1}) 与 Key (h_i)
        self.W_q = nn.Linear(hidden_dim, hidden_dim)
        self.W_k = nn.Linear(hidden_dim, hidden_dim)
        self.V = nn.Linear(hidden_dim, 1)
        
        self.gru = nn.GRU(embed_dim + hidden_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim * 2, vocab_size)

    def forward(self, input_step, hidden, encoder_outputs):
        # input_step: [B, 1], hidden: [1, B, H], encoder_outputs: [B, S, H]
        embed = self.embedding(input_step) # [B, 1, E]
        
        # 1. 计算 Bahdanau 加性 Attention 权重
        # hidden: [B, 1, H]
        query = self.W_q(hidden.permute(1, 0, 2))
        keys = self.W_k(encoder_outputs)
        scores = self.V(torch.tanh(query + keys)) # [B, S, 1]
        attn_weights = F.softmax(scores, dim=1)
        
        # 2. 上下文向量: [B, 1, H]
        context = torch.bmm(attn_weights.permute(0, 2, 1), encoder_outputs)
        
        # 3. GRU 步进
        gru_input = torch.cat([embed, context], dim=2)
        output, hidden = self.gru(gru_input, hidden)
        
        # 4. 预测输出概率
        logits = self.fc(torch.cat([output, context], dim=2).squeeze(1))
        return logits, hidden, attn_weights

# 试运行
decoder = BahdanauAttentionDecoder(vocab_size=1000, embed_dim=64, hidden_dim=128)
input_step = torch.tensor([[10], [20]]) # Batch=2
hidden = torch.randn(1, 2, 128)
encoder_outputs = torch.randn(2, 7, 128) # Batch=2, SeqLen=7

logits, next_hidden, attn = decoder(input_step, hidden, encoder_outputs)
print("Decoder Logits shape:", logits.shape) # [2, 1000]
print("Attention Weights shape:", attn.shape) # [2, 7, 1]
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

### 误区：Exposure Bias (暴露偏差)
- **原因**：由于训练时开启了 Teacher Forcing（每次输入都是完美正确的前文），而推理阶段模型只能依赖自己可能预测错的前文。如果训练与推理阶段的分布不一致，模型会产生一步错、步步错的误差累积。

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

- Sutskever, I., Vinyals, O., & Le, Q. V. (2014). Sequence to Sequence Learning with Neural Networks. *NeurIPS 2014*.
- Bahdanau, D., Cho, K., & Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. *ICLR 2015*.


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《Seq2Seq与注意力机制》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《Seq2Seq与注意力机制》的核心机制及其与上下游模块的连接逻辑。
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
