---
type: study
topic: "Self-Attention自注意力机制"
course: "08-NLP全栈"
created: 2026-08-06
status: active
stage_moc: "[[🧭 阶段4-Transformer与预训练模型]]"
upstream: ["[[08-NLP全栈-词向量与Word2Vec]]", "[[08-NLP全栈-Seq2Seq与注意力机制]]"]
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Self-Attention", "Scaled Dot-Product Attention", "Multi-Head Attention"]
prerequisites: ["矩阵乘法", "Softmax函数", "词嵌入 (Embedding)"]
related: ["Transformer", "BERT", "RoPE位置编码"]
anki_deck: NLP::Transformer
anki_tags: ['#nlp', '#transformer', '#attention']
assessment_exempt: false
---

# 08-NLP全栈-Self-Attention自注意力机制

> ⏱ **预计学习耗时**：45 分钟  
> 🎯 **学习行为目标**：能用手算推导 2-Token 输入的 $Q,K,V$ 相似度与加权和；能够独立用 PyTorch 实现 `ScaledDotProductAttention` 模块并处理 batch 和 mult-head 的 4D Tensor 维度变换 (`[B, H, L, D]`)。

---

## 0. 核心概念与直觉起步

### 为什么需要自注意力机制？
在传统的 RNN 序列模型中，计算必须从左往右按时间步 $\vec{h}_t = f(\vec{h}_{t-1}, \vec{x}_t)$ 严格顺序执行，无法并行；同时对于长距离依赖，梯度容易衰减。
**Self-Attention（自注意力）** 允许序列中的任意两个 Token 直接计算关联强度（无论相距多远，路径长度均为 $\mathcal{O}(1)$），并通过矩阵乘法在 GPU 上高度并行化。

```text
[直觉图解：Token 间如何互相“打分”注意力]
"The animal didn't cross the street because it was too tired."
                                       │
                              (it 关注什么？)
                                       │
                      ┌────────────────┴────────────────┐
                      ▼                                 ▼
                   animal (权重 0.85)                street (权重 0.05)
```

### 🐣 极简退化例子 0（标量/1D起步）
假设只有 2 个词的句子 `"Cat sleeps"`，每个词用 2 维向量表示：
- $\vec{x}_{\text{cat}} = [1, 0]$
- $\vec{x}_{\text{sleeps}} = [0, 1]$

设定简单投影矩阵 $W^Q = W^K = W^V = I_2$（单位矩阵）：
1. 线性变换得到：$\vec{q}_{\text{cat}} = [1, 0], \vec{k}_{\text{sleeps}} = [0, 1], \vec{v}_{\text{sleeps}} = [0, 1]$。
2. 计算点积关联度：$s = \vec{q}_{\text{cat}} \cdot \vec{k}_{\text{sleeps}} = 1 \times 0 + 0 \times 1 = 0$。
   - 这意味着在最简单的正交情况下，cat 和 sleeps 点积分数为 0。而 $\vec{q}_{\text{cat}} \cdot \vec{k}_{\text{cat}} = 1$，说明 cat 最关注自身。

---

## 1. 数学定义与公式表达

给定输入序列的词嵌入矩阵 $X \in \mathbb{R}^{N \times d_{\text{model}}}$（$N$ 为序列长度，$d_{\text{model}}$ 为隐藏维数），引入三个可学习权重矩阵：
$$W^Q \in \mathbb{R}^{d_{\text{model}} \times d_k}, \quad W^K \in \mathbb{R}^{d_{\text{model}} \times d_k}, \quad W^V \in \mathbb{R}^{d_{\text{model}} \times d_v}$$

### Query, Key, Value 的含义
- **Query ($Q = X W^Q$)**：查询向量，代表“当前词在寻找什么信息”。
- **Key ($K = X W^K$)**：键向量，代表“当前词能提供什么关键标识”。
- **Value ($V = X W^V$)**：值向量，代表“当前词包含的具体语义内容”。

### 缩放点积注意力 (Scaled Dot-Product Attention) 公式
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$

维度说明：
- $Q K^T \in \mathbb{R}^{N \times N}$：序列中任意两词之间的原始相似度得分矩阵。
- $\frac{1}{\sqrt{d_k}}$：缩放因子（Scaling Factor），防止 $d_k$ 较大时点积数值过大导致 Softmax 进入梯度饱和区。

---

## 2. 逐步计算过程与张量维度变换

```text
Step 1: 投影         Q = X W^Q (N x d_k),  K = X W^K (N x d_k),  V = X W^V (N x d_v)
Step 2: 相似度矩阵   Scores = Q @ K^T  (N x N)
Step 3: 缩放         Scaled_Scores = Scores / sqrt(d_k)
Step 4: 掩码 (可选)  Masked_Scores = Scaled_Scores + Mask (如 Causal Mask -inf)
Step 5: 概率化       Weights = Softmax(Masked_Scores, dim=-1)  (N x N)
Step 6: 加权聚合     Output = Weights @ V  (N x d_v)
```

---

## 3. PyTorch 标准实现代码

以下为零依赖的 PyTorch 缩放点积注意力与多头注意力实现代码：

```python
import math
import torch
import torch.nn as nn
import torch.nn.functional as F

class ScaledDotProductAttention(nn.Module):
    """缩放点积注意力机制"""
    def __init__(self, dropout: float = 0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)

    def forward(self, q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, mask: torch.Tensor = None):
        # q, k, v shape: [batch_size, num_heads, seq_len, d_k]
        d_k = q.size(-1)
        # 计算注意力得分: [B, H, L_q, d_k] x [B, H, d_k, L_k] -> [B, H, L_q, L_k]
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(d_k)
        
        if mask is not None:
            # 将 mask 为 0 的位置填入极小负值 (防止 softmax 计算权重)
            scores = scores.masked_fill(mask == 0, -1e9)
            
        attn_weights = F.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        
        # 权重加权输出: [B, H, L_q, L_k] x [B, H, L_k, d_v] -> [B, H, L_q, d_v]
        output = torch.matmul(attn_weights, v)
        return output, attn_weights

class MultiHeadSelfAttention(nn.Module):
    """多头自注意力机制 (Multi-Head Attention)"""
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1):
        super().__init__()
        assert d_model % num_heads == 0, "d_model 必须能被 num_heads 整除"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)
        self.w_o = nn.Linear(d_model, d_model)
        
        self.attention = ScaledDotProductAttention(dropout=dropout)

    def forward(self, x: torch.Tensor, mask: torch.Tensor = None):
        batch_size, seq_len, _ = x.size()
        
        # 1. 线性投影并拆分多头: [B, L, d_model] -> [B, L, H, d_k] -> [B, H, L, d_k]
        q = self.w_q(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        k = self.w_k(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        v = self.w_v(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        
        # 2. 算注意力
        out, attn_weights = self.attention(q, k, v, mask=mask)
        
        # 3. 拼接多头并线性变换: [B, H, L, d_k] -> [B, L, H, d_k] -> [B, L, d_model]
        out = out.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        return self.w_o(out), attn_weights
```

---

## 4. 常见误区与避坑指南

> [!WARNING]
> 1. **忘记缩放因子 $\sqrt{d_k}$**：如果去掉除以 $\sqrt{d_k}$，当 $d_k$ 很大时，$Q K^T$ 的方差将随着 $d_k$ 增长到 $d_k$ 级别，导致 Softmax 的输出趋近于 one-hot 分布，反向传播时梯度非常小（梯度消失）。
> 2. **Transpose 与 View 的内存连续性问题**：在 PyTorch 中使用 `.transpose(1, 2)` 后，内存是不连续的，直接调用 `.view()` 会报错。必须先调用 `.contiguous().view(...)`。
> 3. **Mask 的类型误解**：Casual Mask 掩码矩阵中，未来位置应设置为 0（或者 `True` 对应的掩码位置），填充值为 `-1e9` 或 `-inf`，不能设为 0。

---


## 5. 常见误区与对比矩阵

| 评估维度 / 特性 | 方案 A / 经典范式 | 方案 B / 改进范式 | 权衡与选型建议 (Trade-offs) |
| :--- | :--- | :--- | :--- |
| **计算复杂度** | $\mathcal{O}(N^2)$ 或传统高阶复杂度 | $\mathcal{O}(N \log N)$ 或近似线性复杂度 | 高并发生产环境优先选择低复杂度方案 |
| **显存 / 存储占用** | 占用较高，受限于序列长度/维度 | 优化压缩，支持 Memory-efficient | 边缘设备或资源受限场景推荐优化方案 |
| **表征能力与精度** | 基础表达，易受局部噪声干扰 | 强特征提取，捕捉长距离依赖 | 高精度需求任务（如长文本理解/生成）推荐改进范式 |
| **工程落地门槛** | 开箱即用，工具链极为成熟 | 需特定依赖库 (如 CUDA / Triton) | 开发初期快速原型验证使用经典范式 |


## 5. 原有补全内容与 常见面试题与解答

- **Q1: 为什么 Q 和 K 的维度必须相同，而 V 的维度可以不同？**
  - **A1**: 点积运算 $Q K^T$ 要求 $Q$ 的最后一个维度和 $K$ 的最后一个维度必须相等（均为 $d_k$）。但 Softmax 计算出注意力权重得分矩阵 $A \in \mathbb{R}^{N \times N}$ 后，只需要对 $V \in \mathbb{R}^{N \times d_v}$ 做矩阵乘法，所以 $V$ 的维数 $d_v$ 可以独立选择（在实际 Transformer 中为了简便常设 $d_k = d_v = d_{\text{model}} / H$）。

---

## 6. 与作业的连接与实战应用

在 [`08-NLP全栈-阶段作业-02-Transformer与MinBERT实现`](file:///f:/-/03-Projects/08-NLP全栈/阶段作业/08-NLP全栈-阶段作业-02-Transformer与MinBERT实现.md) 中：
- 对应任务：实现 `BertSelfAttention` 模块。
- 关键验证：你需要确保 `q`, `k`, `v` 在经过 `Linear` 变换后，正确调用 `.view(batch_size, seq_len, num_heads, head_size).permute(0, 2, 1, 3)` 将多头维度放到第二维。

---

## 12. 我的主动回忆区（Guided Recall）

请先闭卷回忆并填空下列关键名词/维度：

1. 缩放点积注意力公式中，分子是 $Q K^T$，分母缩放因子是 `____`。
2. 假设 `x` 的 Shape 为 `[16, 64, 768]`（Batch=16, Seq=64, Hidden=768），多头数为 12，则每个 Head 的维度 $d_k$ 为 `____`。
3. 如果序列长度为 $L$，自注意力算子计算相似度得分矩阵的内存与计算复杂度为 $\mathcal{O}(`____`)$。

---

## 13. 闭卷提取练习与分级自测

> [!IMPORTANT]
> 请闭卷作答，思考完毕后再展开下方解答。

### 基础题
写出 $Q, K, V$ 矩阵的英文全称，并解释为什么要用 3 个独立矩阵而不是只用输入 $X$ 做点积。

<details>
<summary>▶ 答案与解释</summary>

- 全称：Query (查询), Key (键), Value (值)。
- 原因：如果只用 $X X^T$，相似度矩阵必然是对称矩阵（因为 $X_i X_j^T = X_j X_i^T$），这意味着“A 对 B 的关注度”强制等于“B 对 A 的关注度”，无法表达语言中的单向修饰关系（如动词关注宾语，而宾语对动词的关注度并不对称）。通过投影到不同的 $W^Q$ 和 $W^K$，解耦了查询与被查询的表达能力。
</details>

---

### 进阶代码题
手写一行 PyTorch 代码：将张量 `q` (Shape `[B, L, H, D]`) 转化为算点积所需的 `[B, H, L, D]`。

<details>
<summary>▶ 答案与代码</summary>

```python
q = q.transpose(1, 2)  # 或 q.permute(0, 2, 1, 3)
```
</details>

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

## 🛠️ 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
