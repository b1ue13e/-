import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = Path("F:/-")
NLP_DIR = VAULT_ROOT / "02-Knowledge" / "🧠 学习系统" / "08-NLP全栈"
if not NLP_DIR.exists():
    NLP_DIR = VAULT_ROOT / "🧠 学习系统" / "08-NLP全栈"

print(f"Stage 29: Upgrading Transformer, Self-Attention, and BERT/GPT in {NLP_DIR}...")

# 1. Self-Attention自注意力机制.md
sa_content = """---
title: "Self-Attention 自注意力机制 (Self-Attention Mechanism)"
course: "08-NLP全栈"
tags:
  - NLP
  - 深度学习
  - Self-Attention
  - 自注意力机制
  - Transformer
  - 缩放点积
type: knowledge_card
status: completed
created: 2026-07-31
---

# Self-Attention 自注意力机制 (Self-Attention Mechanism)

## 1. Self-Attention 自注意力机制的定义与核心动机

**Self-Attention 自注意力机制 (Self-Attention Mechanism)** 的核心定义是：一种允许序列中任意位置的 Token 直接计算与该序列中所有其他位置 Token 的相关性权重，并加权融合全局上下文表示的注意力计算模块。由 Vaswani 等人在 2017 年 *Attention Is All You Need* 中提出。

**基本性质与核心动机**：传统循环神经网络 (RNN/LSTM) 采用顺序步进（Step-by-Step）计算，面临长距离依赖丢失（梯度消失）与无法并行化计算的瓶颈。Self-Attention 自注意力机制将序列中任意两个 Token 之间的**交互距离降至 $O(1)$**，且全过程支持大规模矩阵并行乘法运算，奠定了现代大语言模型 (LLM) 的基石。

---

## 2. 缩放点积注意力 (Scaled Dot-Product Attention) 形式化推导

**输入与投影假设**：
设输入序列矩阵为 $\mathbf{X} \in \mathbb{R}^{N \times d_{\text{model}}}$。定义三个可学习权重矩阵 $\mathbf{W}_Q, \mathbf{W}_K \in \mathbb{R}^{d_{\text{model}} \times d_k}, \mathbf{W}_V \in \mathbb{R}^{d_{\text{model}} \times d_v}$：

$$\mathbf{Q} = \mathbf{X} \mathbf{W}_Q, \quad \mathbf{K} = \mathbf{X} \mathbf{W}_K, \quad \mathbf{V} = \mathbf{X} \mathbf{W}_V$$

**推导过程（缩放因子 $\frac{1}{\sqrt{d_k}}$ 的数学必然性）**：
1. **点积相似度矩阵**：$\mathbf{S} = \mathbf{Q} \mathbf{K}^T \in \mathbb{R}^{N \times N}$；
2. **缩放因子证明**：假设 $q_i$ 与 $k_j$ 的各个分量是均值为 0、方差为 1 的独立随机变量，则点积 $q_i \cdot k_j = \sum_{m=1}^{d_k} q_{im} k_{jm}$ 的均值为 0，**方差为 $d_k$**。若 $d_k$ 很大，点积数值会变得极大，导致 Softmax 函数落入**极度饱和区（梯度几乎为 0）**；
3. **除以 $\sqrt{d_k}$ 归一化方差**：除以 $\sqrt{d_k}$ 使点积方差重回 1，保证 Softmax 梯度的平稳反向传播；
4. **注意力输出方程**：
$$\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{Softmax}\left( \frac{\mathbf{Q} \mathbf{K}^T}{\sqrt{d_k}} \right) \mathbf{V}$$
5. **多头注意力 (Multi-Head Attention, MHA)**：将 $d_{\text{model}}$ 拆分为 $h$ 个独立头并行计算，拼接后投影：
$$\text{MHA}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) \mathbf{W}_O$$

---

## 3. Self-Attention 与 RNN / CNN 的复杂度及并行度对比

| 维度 | Self-Attention 自注意力机制 | 循环神经网络 (RNN/LSTM) | 卷积神经网络 (CNN 1D) |
|:---|:---|:---|:---|
| **每层计算复杂度** | **$O(N^2 \cdot d)$** | $O(N \cdot d^2)$ | $O(k \cdot N \cdot d^2)$ |
| **顺序操作步数 (并行度)**| **$O(1)$** (完全并行) | $O(N)$ (不可并行) | $O(1)$ (局部并行) |
| **最大路径长度 (长距离依赖)**| **$O(1)$** (直连) | $O(N)$ (逐步传递) | $O(\log_k(N))$ (树状堆叠) |
| **主导瓶颈** | 序列长度 $N$ 较长时的 $N^2$ 显存 | 序列长度 $N$ 导致的推理延迟 | 感受野受限于卷积核大小 $k$ |

**局限（误区）**：当序列长度 $N > 10^4$ 时，$O(N^2)$ 的注意力矩阵显存开销会发生爆显存；为此诞生了 FlashAttention、Linear Attention 等加速方案。此外，Self-Attention 具有**置换不变性 (Permutation Invariance)**，必须依靠位置编码 (Positional Encoding / RoPE) 注入位置信息。

关联知识点推荐：[[Transformer架构]]、[[BERT与GPT对比]]、[[梯度下降与Adam优化器]]、[[交叉熵损失函数]]。

---

## 4. Python 手写 Scaled Dot-Product Attention 与 Softmax 梯度自测断言

```python
import numpy as np

def scaled_dot_product_attention(Q: np.ndarray, K: np.ndarray, V: np.ndarray,
                                  mask: np.ndarray = None) -> tuple:
    \"\"\"
    手动实现 Scaled Dot-Product Attention
    Q, K, V: (B, N, dk)
    \"\"\"
    B, N, dk = Q.shape
    scores = np.matmul(Q, K.transpose(0, 2, 1)) / np.sqrt(dk)

    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)

    # Softmax
    scores_max = np.max(scores, axis=-1, keepdims=True)
    exp_scores = np.exp(scores - scores_max)
    attn_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)

    output = np.matmul(attn_weights, V)
    return output, attn_weights

if __name__ == "__main__":
    np.random.seed(42)
    B, N, dk = 1, 3, 4
    Q = np.random.randn(B, N, dk)
    K = np.random.randn(B, N, dk)
    V = np.random.randn(B, N, dk)

    output, weights = scaled_dot_product_attention(Q, K, V)

    # 自测验证 1: 注意力权重每行和必须严格等于 1.0 (概率分布)
    row_sums = np.sum(weights, axis=-1)
    assert np.allclose(row_sums, 1.0), f"Softmax 行和不为 1: {row_sums}"

    # 自测验证 2: 输出 Shape 断言
    assert output.shape == (B, N, dk)

    # 自测验证 3: Mask (因果掩码 Causal Mask) 自测
    causal_mask = np.tril(np.ones((N, N)))
    _, masked_weights = scaled_dot_product_attention(Q, K, V, mask=causal_mask)
    assert masked_weights[0, 0, 1] < 1e-6, "因果掩码必须封锁未来 Token 注意力"

    print("Self-Attention 自注意力机制注意力概率矩阵:")
    print(weights[0].round(3))
    print("Self-Attention 自注意力机制单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems (NIPS '17)*, 30, 5998-6008. DOI: https://doi.org/10.48550/arXiv.1706.03762 URL: https://arxiv.org/abs/1706.03762
- Bahdanau, D., Cho, K., & Bengio, Y. (2014). Neural machine translation by jointly learning to align and translate. *arXiv preprint arXiv:1409.0473*. URL: https://arxiv.org/abs/1409.0473
- Dao, T., et al. (2022). FlashAttention: Fast and memory-efficient exact attention with IO-awareness. *Advances in Neural Information Processing Systems (NeurIPS '22)*, 35, 16344-16359. URL: https://arxiv.org/abs/2205.14135
"""

# 2. Transformer架构.md
transformer_content = """---
title: "Transformer 架构与 Seq2Seq 模型 (Transformer Architecture)"
course: "08-NLP全栈"
tags:
  - NLP
  - 深度学习
  - Transformer
  - Encoder-Decoder
  - 位置编码
  - LayerNorm
type: knowledge_card
status: completed
created: 2026-07-31
---

# Transformer 架构与 Seq2Seq 模型 (Transformer Architecture)

## 1. Transformer 架构的定义与全局组件

**Transformer 架构与 Seq2Seq 模型 (Transformer Architecture)** 的核心定义 is：一种完全摒弃循环 (RNN) 与卷积 (CNN) 结构，纯粹基于多头自注意力机制 (Multi-Head Self-Attention) 和前馈神经网络 (FFN) 构筑的序列到序列 (Seq2Seq) 深度神经网络架构。由 Google 团队在 2017 年提出。

**核心四大组件**：
1. **Positional Encoding (位置编码)**：注入序列位置信息 $\mathbf{PE}_{(pos, 2i)} = \sin(pos/10000^{2i/d})$；
2. **Multi-Head Attention (多头注意力)**：多子空间提取语义关系；
3. **Residual Connection & LayerNorm (Residual & LN)**：深层网络稳定训练；
4. **Position-wise Feed-Forward Network (FFN)**：由两层线性变换与 ReLU/GELU 激活函数组成。

---

## 2. 正弦位置编码与 LayerNorm 形式化推导

**正弦位置编码 (Sinusoidal Positional Encoding) 相对位置推导**：
$$\mathbf{PE}_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right), \quad \mathbf{PE}_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$$

**相对位置线性映射证明**：对于固定的偏移量 $k$，存在线性变换矩阵 $\mathbf{R}_k$ 使得 $\mathbf{PE}_{pos+k} = \mathbf{R}_k \mathbf{PE}_{pos}$。利用三角函数和差化积公式：
$$\sin(\alpha + \beta) = \sin\alpha \cos\beta + \cos\alpha \sin\beta$$
**因此**，模型能够天然且泛化地学习到 Token 之间的相对位置距离。

**Layer Normalization (LN) 形式化推导**：
区别于 BatchNorm (对 Batch 维度归一化)，LayerNorm 在单个样本的 **Channel/Hidden 维度** 上计算均值 $\mu$ 与方差 $\sigma^2$：

$$\mu = \frac{1}{d} \sum_{i=1}^d x_i, \quad \sigma^2 = \frac{1}{d} \sum_{i=1}^d (x_i - \mu)^2, \quad \hat{x}_i = \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}} \cdot \gamma + \beta$$

LN 不受 Batch Size 大小影响，非常适合可变长序列的 NLP 任务。

---

## 3. Transformer Encoder 与 Decoder 的区别与对比

| 维度 | Transformer Encoder (编码器) | Transformer Decoder (解码器) |
|:---|:---|:---|
| **注意力类型** | **双向 Self-Attention** (可看上下文) | **Masked Self-Attention** (因果掩码) + Cross-Attn |
| **掩码机制** | 无 (或仅 Padding Mask) | **Causal Masking (三角掩码下半区)** |
| **输入输出范式** | 并行输入 $\to$ 密集特征表示 | 自回归 (Auto-Regressive) 逐字生成 |
| **代表模型** | **BERT**, RoBERTa, DeBERTa | **GPT-1/2/3/4**, LLaMA, DeepSeek |

**局限（误区）**：在解码器 Cross-Attention 中，$\mathbf{Q}$ 来自 Decoder 上一层，而 $\mathbf{K}, \mathbf{V}$ 来自 Encoder 的最终输出；混淆 Q/K/V 来源是理解 Transformer 架构的常见错误。

关联知识点推荐：[[Self-Attention自注意力机制]]、[[BERT与GPT对比]]、[[ResNet残差网络]]、[[Amdahl定律]]。

---

## 4. Python 手写 LayerNorm 与正弦位置编码自测断言

```python
import numpy as np

def layer_norm(x: np.ndarray, gamma: float = 1.0, beta: float = 0.0, eps: float = 1e-5) -> np.ndarray:
    \"\"\"手动实现 Layer Normalization (针对最后维度 d_model 归一化)\"\"\"
    mean = np.mean(x, axis=-1, keepdims=True)
    var = np.var(x, axis=-1, keepdims=True)
    x_norm = (x - mean) / np.sqrt(var + eps)
    return gamma * x_norm + beta

def get_positional_encoding(seq_len: int, d_model: int) -> np.ndarray:
    \"\"\"生成正弦位置编码矩阵 (seq_len, d_model)\"\"\"
    pe = np.zeros((seq_len, d_model))
    for pos in range(seq_len):
        for i in range(0, d_model, 2):
            div_term = np.power(10000.0, i / d_model)
            pe[pos, i] = np.sin(pos / div_term)
            if i + 1 < d_model:
                pe[pos, i + 1] = np.cos(pos / div_term)
    return pe

if __name__ == "__main__":
    np.random.seed(42)
    x = np.random.randn(2, 4, 8)  # Batch=2, SeqLen=4, d_model=8

    # 1. LayerNorm 验证
    ln_out = layer_norm(x)
    means = np.mean(ln_out, axis=-1)
    vars_ = np.var(ln_out, axis=-1)

    assert np.allclose(means, 0.0, atol=1e-5), "LayerNorm 均值必须归零"
    assert np.allclose(vars_, 1.0, atol=1e-3), "LayerNorm 方差必须归一"

    # 2. Positional Encoding 验证
    pe = get_positional_encoding(seq_len=10, d_model=16)
    assert pe.shape == (10, 16)
    assert abs(pe[0, 0] - 0.0) < 1e-5  # sin(0) = 0
    assert abs(pe[0, 1] - 1.0) < 1e-5  # cos(0) = 1

    print(f"LayerNorm 均值={means[0,0]:.4f}, 方差={vars_[0,0]:.4f} (校验成功)")
    print("Transformer 架构与 Seq2Seq 模型单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Vaswani, A., et al. (2017). Attention is all you need. *Advances in Neural Information Processing Systems (NIPS '17)*, 30, 5998-6008. DOI: https://doi.org/10.48550/arXiv.1706.03762 URL: https://arxiv.org/abs/1706.03762
- Ba, J. L., Kiros, J. R., & Hinton, G. E. (2016). Layer normalization. *arXiv preprint arXiv:1607.06450*. URL: https://arxiv.org/abs/1607.06450
- Shaw, P., Uszkoreit, J., & Vaswani, A. (2018). Self-attention with relative positional representations. *NAACL-HLT '18*, 464-468. URL: https://arxiv.org/abs/1803.02155
"""

# 3. BERT与GPT对比.md
bert_gpt_content = """---
title: "BERT 与 GPT 范式对比 (BERT vs GPT Architecture)"
course: "08-NLP全栈"
tags:
  - NLP
  - BERT
  - GPT
  - 大语言模型
  - 掩码语言模型
  - 自回归
type: knowledge_card
status: completed
created: 2026-07-31
---

# BERT 与 GPT 范式对比 (BERT vs GPT Architecture)

## 1. BERT 与 GPT 的定义与预训练范式

**BERT 与 GPT 范式对比 (BERT vs GPT Architecture)** 的核心定义是：代表现代 NLP 预训练大模型两大分支方向的架构范式对比——基于 Transformer Encoder 的双向掩码语言模型 **BERT (Bidirectional Encoder Representations from Transformers)** 与基于 Transformer Decoder 的单向自回归语言模型 **GPT (Generative Pre-trained Transformer)**。

- **BERT (Devlin et al., 2018)**：通过 Masked Language Model (MLM) 随机掩盖 15% Token，利用上下文双向注意力提取深层语义表示，擅长**自然语言理解 (NLU)** 任务（如文本分类、实体识别）；
- **GPT (Radford et al., 2018/2019/2020)**：通过自回归下一个 Token 预测 (Next-Token Prediction) 目标，利用因果掩码自向后单向生成，擅长**自然语言生成 (NLG)** 与通用提示词 (Prompt/In-Context Learning) 任务。

---

## 2. 预训练损失函数形式化推导

**BERT 双向 MLM 损失函数推导**：
设输入序列 $\mathbf{x} = (x_1, \dots, x_N)$，随机掩码位置集合为 $\mathcal{M}$。被掩盖词概率最大化目标：

$$\mathcal{L}_{\text{MLM}}(\theta) = -\sum_{i \in \mathcal{M}} \log P(x_i \mid \mathbf{x}_{\setminus \mathcal{M}}; \theta)$$

由于 $P(x_i \mid \mathbf{x}_{\setminus \mathcal{M}})$ 同时依赖 $x_i$ 左侧与右侧的所有 Token，其注意力为全通双向矩阵。

**GPT 单向自回归 (Auto-Regressive) 损失函数推导**：
根据概率链式法则 (Chain Rule of Probability)，最大化联合概率 $P(\mathbf{x}) = \prod_{i=1}^N P(x_i \mid x_1, \dots, x_{i-1})$ 的对数似然：

$$\mathcal{L}_{\text{GPT}}(\phi) = -\sum_{i=1}^N \log P(x_i \mid x_1, x_2, \dots, x_{i-1}; \phi)$$

**因此**：
1. BERT 无法直接用于长文本流畅生成（缺乏自回归因果链）；
2. GPT 在单向因果约束下天然具备了无限长文本下文预测的能力。

---

## 3. BERT 与 GPT 的全方位对比

| 维度 | BERT 范式 (Encoder-Only) | GPT 范式 (Decoder-Only) |
|:---|:---|:---|
| **核心架构** | Transformer Encoder | Transformer Decoder |
| **注意力机制** | **双向 Self-Attention** (看见前后) | **单向 Masked Attention** (只看左边) |
| **预训练目标** | Masked LM (MLM) + Next Sentence | Next-Token Prediction (CLD) |
| **核心优势领域** | **NLU 理解**（抽取、分类、相关性）| **NLG 生成 + In-Context Few-Shot** |
| **微调范式** | 微调 Task-Specific 头 (Fine-Tuning)| Zero/Few-Shot 提示词 / RLHF 对齐 |
| **现代模型代表** | RoBERTa, DeBERTa, StructBERT | **GPT-4, LLaMA-3, Qwen-2.5, DeepSeek** |

**局限（误区）**：早期学术界认为 Encoder-Only (BERT) 语义理解更强，但随着 Parameter Scaling Law 突破百亿/千亿关口，Decoder-Only (GPT) 展现出了惊人的涌现能力 (Emergent Abilities)，彻底统一了理解与生成任务。

关联知识点推荐：[[Transformer架构]]、[[Self-Attention自注意力机制]]、[[交叉熵损失函数]]、[[梯度下降与Adam优化器]]。

---

## 4. Python 简易 MLM 损失与自回归 Causal Loss 计算自测断言

```python
import numpy as np

def compute_mlm_and_clm_loss(logits: np.ndarray, labels: np.ndarray, mask_indices: list = None) -> tuple:
    \"\"\"
    仿真 BERT MLM Loss 与 GPT CLM (Causal Language Model) Loss
    logits: (B, N, V)
    labels: (B, N)
    \"\"\"
    B, N, V = logits.shape
    # Softmax
    exp_l = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
    probs = exp_l / np.sum(exp_l, axis=-1, keepdims=True)

    # 1. BERT MLM Loss (仅对 masked 位置算 Cross-Entropy)
    mlm_losses = []
    for b in range(B):
        for idx in mask_indices:
            target_tok = labels[b, idx]
            mlm_losses.append(-np.log(probs[b, idx, target_tok] + 1e-10))
    mlm_loss = float(np.mean(mlm_losses))

    # 2. GPT CLM Loss (对所有位置自回归算 Cross-Entropy)
    clm_losses = []
    for b in range(B):
        for i in range(N):
            target_tok = labels[b, i]
            clm_losses.append(-np.log(probs[b, i, target_tok] + 1e-10))
    clm_loss = float(np.mean(clm_losses))

    return mlm_loss, clm_loss

if __name__ == "__main__":
    np.random.seed(42)
    B, N, V = 1, 4, 10
    logits = np.random.randn(B, N, V)
    labels = np.array([[2, 5, 8, 1]])
    masked_pos = [1, 3]  # 位置 1 和 3 被 MASK

    mlm_l, clm_l = compute_mlm_and_clm_loss(logits, labels, masked_pos)

    # 自测验证 1: 损失标量正常断言
    assert mlm_l > 0.0 and clm_l > 0.0

    # 自测验证 2: 完美预测时 损失趋近于 0
    perfect_logits = np.zeros((B, N, V))
    for i in range(N):
        perfect_logits[0, i, labels[0, i]] = 100.0
    p_mlm, p_clm = compute_mlm_and_clm_loss(perfect_logits, labels, masked_pos)
    assert p_mlm < 1e-4 and p_clm < 1e-4, "完美预测下损失必须趋近 0"

    print(f"BERT MLM 损失 = {mlm_l:.4f}, GPT CLM 损失 = {clm_l:.4f}")
    print("BERT 与 GPT 范式对比单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2018). BERT: Pre-training of deep bidirectional transformers for language understanding. *NAACL-HLT '19*, 4171-4186. DOI: https://doi.org/10.48550/arXiv.1810.04805 URL: https://arxiv.org/abs/1810.04805
- Radford, A., Narasimhan, K., Salimans, T., & Sutskever, I. (2018). Improving language understanding by generative pre-training (GPT-1). *OpenAI Blog*. URL: https://openai.com/research/language-unsupervised
- Brown, T. B., et al. (2020). Language models are few-shot learners (GPT-3). *Advances in Neural Information Processing Systems (NeurIPS '20)*, 33, 1877-1901. URL: https://arxiv.org/abs/2005.14165
"""

# Write files
(NLP_DIR / "Self-Attention自注意力机制.md").write_text(sa_content, encoding="utf-8")
(NLP_DIR / "Transformer架构.md").write_text(transformer_content, encoding="utf-8")
(NLP_DIR / "BERT与GPT对比.md").write_text(bert_gpt_content, encoding="utf-8")

print("Stage 29: Successfully written Self-Attention, Transformer, and BERT/GPT!")
