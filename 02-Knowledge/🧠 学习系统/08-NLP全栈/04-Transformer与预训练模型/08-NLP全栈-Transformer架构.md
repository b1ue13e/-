---
type: study
topic: "Transformer架构"
course: "08-NLP全栈"
created: 2026-08-06
status: active
stage_moc: "[[🧭 阶段4-Transformer与预训练模型]]"
upstream: ["[[08-NLP全栈-Self-Attention自注意力机制]]"]
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Transformer", "Encoder-Decoder", "Positional Encoding", "Residual Connection", "LayerNorm"]
prerequisites: ["Self-Attention自注意力机制", "Layer Normalization", "前馈神经网络 (FFN)"]
related: ["BERT模型", "GPT系列模型", "RoPE旋转位置编码"]
anki_deck: NLP::Transformer
anki_tags: ['#nlp', '#transformer', '#encoder_decoder']
assessment_exempt: false
---

# 08-NLP全栈-Transformer架构

> ⏱ **预计学习耗时**：60 分钟  
> 🎯 **学习行为目标**：能绘制 Transformer 编码器-解码器整体结构图；理解 Positional Encoding 位置编码公式与 LayerNorm 位置（Pre-LN vs Post-LN）；能够用 PyTorch 完整实现 `BertLayer` 与 `TransformerEncoder`。

---

## 0. 核心概念与直觉起步

### 为什么需要 Transformer 架构？
Transformer 摒弃了传统的 RNN 循环和 CNN 卷积结构，完全建立在自注意力机制之上。它由 **Encoder（编码器）** 与 **Decoder（解码器）** 堆叠而成：
- **Encoder**：双向注意力（Bidirectional），负责提取文本特征（如 BERT）。
- **Decoder**：单向/因果注意力（Causal Masked Attention），结合 Encoder 的输出通过 Cross-Attention 生成文本（如 GPT、T5）。

```text
[Transformer 架构整体流向]
       输入序列 X                   目标序列 Y
           │                            │
    [ Embedding ]                [ Embedding ]
           │                            │
[ Positional Encoding ]      [ Positional Encoding ]
           │                            │
           ▼                            ▼
┌─────────────────────┐      ┌─────────────────────┐
│  Encoder Block x N  │ ───► │  Decoder Block x N  │
│ - Multi-Head Attn   │ (K,V)│ - Masked MH-Attn    │
│ - Add & LayerNorm   │      │ - Cross MH-Attn     │
│ - Feed Forward (FFN)│      │ - Feed Forward      │
└─────────────────────┘      └─────────────────────┘
                                        │
                                   [ Linear ]
                                        │
                                   [ Softmax ]
```

---

## 1. 核心数学表达与组件公式

### 1. 正弦位置编码 (Positional Encoding)
由于 Self-Attention 本身对输入顺序无感知，需要手动加入位置向量 $PE$:
$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i / d_{\text{model}}}}\right)$$
$$PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i / d_{\text{model}}}}\right)$$

### 2. 残差连接与 Layer Standard Normalization
在 Post-LN 架构中：
$$\text{SubLayerOutput} = \text{LayerNorm}(X + \text{SubLayer}(X))$$

### 3. 位置前馈网络 (Position-wise Feed-Forward Network)
包含两次线性变换与中间激活函数（通常为 ReLU 或 GELU）：
$$\text{FFN}(x) = \max(0, x W_1 + b_1) W_2 + b_2$$

---

## 2. PyTorch 完整 Transformer Encoder Layer 实现

```python
import torch
import torch.nn as nn
from typing import Optional

class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_len: int = 512):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-torch.log(torch.tensor(10000.0)) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0)) # Shape: [1, max_len, d_model]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.pe[:, :x.size(1)]

class TransformerEncoderLayer(nn.Module):
    """标准的 Pre-LN Transformer 编码器层"""
    def __init__(self, d_model: int, num_heads: int, dim_feedforward: int = 2048, dropout: float = 0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(d_model, num_heads, dropout=dropout, batch_first=True)
        self.linear1 = nn.Linear(d_model, dim_feedforward)
        self.linear2 = nn.Linear(dim_feedforward, d_model)
        
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
        self.activation = nn.GELU()

    def forward(self, src: torch.Tensor, src_mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        # Pre-LN 结构更易训练稳定
        # 1. Self-Attention + Residual
        src_norm = self.norm1(src)
        attn_out, _ = self.self_attn(src_norm, src_norm, src_norm, attn_mask=src_mask)
        src = src + self.dropout(attn_out)
        
        # 2. Feed-Forward + Residual
        src_norm = self.norm2(src)
        ff_out = self.linear2(self.dropout(self.activation(self.linear1(src_norm))))
        src = src + self.dropout(ff_out)
        return src
```

---

## 4. 常见误区与避坑指南

> [!WARNING]
> 1. **Pre-LN 与 Post-LN 的区别**：原始 2017 Transformer 论文使用的是 Post-LN（在残差之后做 LayerNorm），这种结构在层数加深时容易导致梯度不稳定，需要繁琐的 Warmup 策略；现代模型（如 Megatron-LM、LLaMA）普遍改用 Pre-LN 或 RMSNorm。
> 2. **Decoder 的 Mask 差异**：Decoder 的第一级 Self-Attention 必须加 Casual Mask（下三角矩阵，未来位置填 `-inf`），防止在解码第 $t$ 个词时窥探到第 $t+1$ 及以后的目标词。

---

## 12. 我的主动回忆区（Guided Recall）

1. 正弦位置编码使用 `____` 和 `____` 函数交替填充偶数和奇数维度。
2. Transformer Encoder 层的两个子模块分别是 `____` 和 `____`。
3. Layer Normalization 是在 `____` 维度（Batch 维度还是 Hidden 维度）上做归一化？

---

## 13. 闭卷提取练习与分级自测

### 基础题
解释 BatchNorm 和 LayerNorm 的主要区别，以及为什么 NLP 任务普遍选择 LayerNorm。

<details>
<summary>▶ 答案与解释</summary>

- **BatchNorm**：对同 Batch 样本同一维特征求均值和方差。要求 Batch Size 较大，且受序列变长 Padding 影响巨大。
- **LayerNorm**：对单个样本在所有 Hidden 维度上求均值和方差。独立于 Batch Size 和序列长度，非常适合 NLP 变长文本处理。
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




## 5. 常见误区与对比矩阵

| 评估维度 / 特性 | 方案 A / 经典范式 | 方案 B / 改进范式 | 权衡与选型建议 (Trade-offs) |
| :--- | :--- | :--- | :--- |
| **计算复杂度** | $\mathcal{O}(N^2)$ 或传统高阶复杂度 | $\mathcal{O}(N \log N)$ 或近似线性复杂度 | 高并发生产环境优先选择低复杂度方案 |
| **显存 / 存储占用** | 占用较高，受限于序列长度/维度 | 优化压缩，支持 Memory-efficient | 边缘设备或资源受限场景推荐优化方案 |
| **表征能力与精度** | 基础表达，易受局部噪声干扰 | 强特征提取，捕捉长距离依赖 | 高精度需求任务（如长文本理解/生成）推荐改进范式 |
| **工程落地门槛** | 开箱即用，工具链极为成熟 | 需特定依赖库 (如 CUDA / Triton) | 开发初期快速原型验证使用经典范式 |


---

## 🛠️ 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
