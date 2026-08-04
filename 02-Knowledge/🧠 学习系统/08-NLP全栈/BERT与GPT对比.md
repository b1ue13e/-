---
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
    """
    仿真 BERT MLM Loss 与 GPT CLM (Causal Language Model) Loss
    logits: (B, N, V)
    labels: (B, N)
    """
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
