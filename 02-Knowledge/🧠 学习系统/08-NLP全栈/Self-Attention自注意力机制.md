---
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
$$\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{Softmax}\left( \frac{\mathbf{Q} \mathbf{K}^T}{\sqrt{d_k}} 
ight) \mathbf{V}$$
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
    """
    手动实现 Scaled Dot-Product Attention
    Q, K, V: (B, N, dk)
    """
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
