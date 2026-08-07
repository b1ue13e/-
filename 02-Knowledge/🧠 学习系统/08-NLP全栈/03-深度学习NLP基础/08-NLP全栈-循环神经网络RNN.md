---
sources: ['Elman, J. L. (1990). Finding Structure in Time. Cognitive Science, 14(2), 179-211.', 'Hochreiter, S., & Schmidhuber, J. (1997). Long Short-Term Memory. Neural Computation, 9(8), 1735-1780.', 'Cho, K., et al. (2014). Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation. EMNLP 2014.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "循环神经网络RNN"
created: 2026-08-06
status: completed
assessment_exempt: false
difficulty: intermediate
stage_moc: "[[🧭 阶段3-深度学习NLP基础]]"
upstream: ["[[08-NLP全栈-CNN在NLP中的应用]]"]
tags: [学习, NLP, RNN, LSTM, GRU, 梯度消失, BPTT, 门控机制]
---

# 08-NLP全栈-循环神经网络RNN

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 前馈神经网络（FFNN）和 CNN 要求固定尺寸的输入与输出，且忽略了时间/词语序列的前后时序依赖。前向传递时，原生 Simple RNN 在反向传播算法 (Backpropagation Through Time, BPTT) 中会面临**梯度消失 (Vanishing Gradient) 与梯度爆炸 (Exploding Gradient)**，无法保留超过 10~20 步的长距离历史记忆。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是从标准 RNN 演进到门控循环单元 (LSTM / GRU) 的关键里程碑，奠定了双向 RNN (BiLSTM) 与 Seq2Seq 架构的根基。
- **实际应用场景**：序列标注 (BiLSTM-CRF)、语言模型 $P(w_t \mid w_{<t})$ 递归生成、时间序列预测。

---

## 3. 正式定义与核心公式

### 1. 原生 Simple RNN 递推公式

$$h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h)$$

BPTT 梯度计算中，梯度包含雅可比矩阵的连乘项 $\prod_{k=j+1}^t W_{hh}^T$。当 $W_{hh}$ 的最大特征值小于 1 时，梯度指数级衰减趋近于 0（梯度消失）。

### 2. 长短期记忆网络 (LSTM) 门控结构

LSTM 引入**遗忘门 $f_t$、输入门 $i_t$、输出门 $o_t$** 与**细胞状态 $C_t$**（加性加法通道，解决梯度消失）：

$$\begin{aligned}
f_t &= \sigma(W_f [h_{t-1}, x_t] + b_f) \\
i_t &= \sigma(W_i [h_{t-1}, x_t] + b_i) \\
\tilde{C}_t &= \tanh(W_c [h_{t-1}, x_t] + b_c) \\
C_t &= f_t \odot C_{t-1} + i_t \odot \tilde{C}_t \quad (\text{加性加法更新，梯度直接穿透}) \\
o_t &= \sigma(W_o [h_{t-1}, x_t] + b_o) \\
h_t &= o_t \odot \tanh(C_t)
\end{aligned}$$

---

## 4. PyTorch 代码实现：BiLSTM 语言序列编码器

```python
import torch
import torch.nn as nn

class BiLSTMEncoder(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        # 双向 LSTM
        self.lstm = nn.LSTM(
            input_size=embed_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True
        )
        self.fc = nn.Linear(hidden_dim * 2, 2)

    def forward(self, x):
        # x: [Batch, Seq_Len]
        embed = self.embedding(x) # [Batch, Seq_Len, Embed_Dim]
        # output: [Batch, Seq_Len, Hidden_Dim * 2]
        output, (hn, cn) = self.lstm(embed)
        # 取最后一个时刻的输出进行分类
        last_hidden = output[:, -1, :]
        return self.fc(last_hidden)

model = BiLSTMEncoder(vocab_size=5000, embed_dim=128, hidden_dim=256)
x = torch.randint(0, 5000, (2, 10))
logits = model(x)
print("BiLSTM Logits shape:", logits.shape) # [2, 2]
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

### 误区：GRU 一定比 LSTM 效果好
- **对比**：GRU 将 LSTM 的遗忘门与输入门合并为更新门 $z_t$，参数量减少约 $1/3$，训练速度更快。但在海量数据集与长文本下，LSTM 的表达能力与容量依然略强于 GRU。

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

- Hochreiter, S., & Schmidhuber, J. (1997). Long Short-Term Memory. *Neural Computation*, 9(8), 1735-1780.
- Cho, K., et al. (2014). Learning Phrase Representations using RNN Encoder-Decoder. *EMNLP 2014*.


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《循环神经网络RNN》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《循环神经网络RNN》的核心机制及其与上下游模块的连接逻辑。
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
