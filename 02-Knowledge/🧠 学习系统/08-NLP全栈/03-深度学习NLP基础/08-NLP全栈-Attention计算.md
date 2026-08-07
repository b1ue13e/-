---
sources: ['Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention Is All You Need. NeurIPS 2017.', 'Bahdanau, D., Cho, K., & Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. ICLR 2015.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "Attention计算"
created: 2026-04-18
status: completed
assessment_exempt: false
difficulty: intermediate
stage_moc: "[[🧭 阶段3-深度学习NLP基础]]"
upstream: ["[[08-NLP全栈-Seq2Seq与注意力机制]]"]
tags: [学习, NLP, Attention, 缩放点积注意力, Seq2Seq]
---

# 08-NLP全栈-Attention计算

---

## 1. 动机 (Motivation)

在传统的 Seq2Seq (Encoder-Decoder) 模型中，Encoder 必须将整个输入序列的所有信息压缩成一个固定长度的**上下文向量 (Context Vector, $c$)**。这带来了一个致命瓶颈（信息瓶颈）：对于长序列，早期输入的信息在压缩过程中会严重丢失。

**Attention（注意力机制）** 的核心思想是：与其试图把整个句子压缩成一个固定向量，不如让 Decoder 在生成每个目标词时，“回头看”输入序列，并动态决定当前最需要关注哪些输入词。

---

## 2. 核心定义与计算流程

Attention 的本质是一个**加权求和**过程，其计算可以被抽象为 Query (查询), Key (键), Value (值) 三个概念的交互：
- **Query ($q$)**: Decoder 当前时刻的隐藏状态 $s_{t-1}$
- **Key ($k$)**: Encoder 各个时刻的隐藏状态 $h_i$
- **Value ($v$)**: 同上，通常也是 Encoder 的隐藏状态 $h_i$

### 计算步骤 (以 Luong 乘性 Attention 为例)

1. **计算注意力打分 (Attention Scores)**：
   - 点积 (Dot-product): $e_{t, i} = q^\top k_i$
   - 缩放点积 (Scaled Dot-product): $e_{t, i} = \frac{q^\top k_i}{\sqrt{d_k}}$
   - 带有权重矩阵 (General): $e_{t, i} = q^\top W k_i$
   - 拼接前馈 (Additive/Bahdanau): $e_{t, i} = v^\top \tanh(W_q q + W_k k_i)$

2. **计算注意力权重 (Attention Weights)**：
   使用 Softmax 对得分进行归一化：
   $$\alpha_{t, i} = \text{softmax}(e_{t, i}) = \frac{\exp(e_{t, i})}{\sum_{j=1}^N \exp(e_{t, j})}$$

3. **计算上下文向量 (Context Vector)**：
   $$c_t = \sum_{i=1}^N \alpha_{t, i} v_i$$

---

## 3. 代码示例 (PyTorch)

```python
import torch
import torch.nn.functional as F
import math

def scaled_dot_product_attention(query, key, value, mask=None):
    """
    计算缩放点积注意力
    query, key, value 形状: [batch_size, seq_len, d_k]
    """
    d_k = query.size(-1)
    
    # 1. 计算打分 (Scores): Q * K^T
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
    
    # 可选：掩码 (Masking)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
        
    # 2. 计算权重 (Weights): Softmax
    p_attn = F.softmax(scores, dim=-1)
    
    # 3. 计算加权和 (Context Vector)
    return torch.matmul(p_attn, value), p_attn

# 测试用例
batch_size, seq_len, d_k = 2, 5, 64
q = torch.randn(batch_size, seq_len, d_k)
k = torch.randn(batch_size, seq_len, d_k)
v = torch.randn(batch_size, seq_len, d_k)

context, weights = scaled_dot_product_attention(q, k, v)
print(f"Context vector shape: {context.shape}") # [2, 5, 64]
print(f"Attention weights shape: {weights.shape}") # [2, 5, 5]
```

---

## 4. 边界条件与限制

- **计算复杂度**：点积注意力的计算复杂度是 $\mathcal{O}(N^2)$，其中 $N$ 是序列长度。当处理超长文本时，显存是最大瓶颈。
- **无位置信息**：纯点积操作是**排列等价**的，因此 Transformer 必须引入位置编码 (Positional Encoding)。

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

- Vaswani, A., et al. (2017). Attention Is All You Need. NeurIPS 2017.
- Bahdanau, D., Cho, K., & Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. ICLR 2015.



## 5. 常见误区与对比矩阵

| 评估维度 / 特性 | 方案 A / 经典范式 | 方案 B / 改进范式 | 权衡与选型建议 (Trade-offs) |
| :--- | :--- | :--- | :--- |
| **计算复杂度** | $\mathcal{O}(N^2)$ 或传统高阶复杂度 | $\mathcal{O}(N \log N)$ 或近似线性复杂度 | 高并发生产环境优先选择低复杂度方案 |
| **显存 / 存储占用** | 占用较高，受限于序列长度/维度 | 优化压缩，支持 Memory-efficient | 边缘设备或资源受限场景推荐优化方案 |
| **表征能力与精度** | 基础表达，易受局部噪声干扰 | 强特征提取，捕捉长距离依赖 | 高精度需求任务（如长文本理解/生成）推荐改进范式 |
| **工程落地门槛** | 开箱即用，工具链极为成熟 | 需特定依赖库 (如 CUDA / Triton) | 开发初期快速原型验证使用经典范式 |


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《Attention计算》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《Attention计算》的核心机制及其与上下游模块的连接逻辑。
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
