---
sources: ['Su, J., Lu, Y., Pan, S., Murtadha, A., Wen, B., & Liu, Y. (2024). RoFormer: Enhanced Transformer with Rotary Position Embedding. Neurocomputing, 568. arXiv:2104.09864.', 'Peng, B., et al. (2023). YaRN: Efficient Context Window Extension of Large Language Models. arXiv:2309.00071.', 'Press, O., Smith, N. A., & Lewis, M. (2022). Train Short, Test Long: Attention with Linear Biases (ALiBi). ICLR 2022.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "RoPE旋转位置编码"
created: 2026-08-06
status: completed
assessment_exempt: false
difficulty: intermediate
stage_moc: "[[🧭 阶段4-Transformer与预训练模型]]"
upstream: ["[[08-NLP全栈-Self-Attention自注意力机制]]"]
tags: [学习, NLP, RoPE, 旋转位置编码, 相对位置编码, Transformer, LLM, LLaMA, YaRN, ALiBi]
---

# 08-NLP全栈-RoPE旋转位置编码

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 在 Transformer 中，Attention 机制本身是**置换不变 (Permutation Invariant)** 的。早期 Transformer 使用绝对位置编码（Sinusoidal 或 Learned Absolute Embedding），但这些编码在扩展长上下文（外推性）和捕捉相对距离衰减时效果受限。如何在不显式增加相对位置矩阵的情况下，将相对位置信息无缝注入到 $Q, K$ 内积中，是 RoPE 的核心突破。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是当代几乎所有 SOTA 大语言模型（LLaMA 1/2/3, Mistral, Qwen, Baichuan, DeepSeek）默认标配的位置编码。
- **核心优势**：
  1. 隐式捕捉相对位置信息 $n - m$。
  2. 保持正交性，不改变词向量模长 $\|\mathbf{q}\|_2$。
  3. 支持通过频率插值（NTK-scaling / YaRN）实现超长上下文长度外推 (Context Length Extension)。

---

## 3. 数学推导与公式证明

### 1. 二维平面旋转矩阵

对二维向量 $\mathbf{x} = [x_1, x_2]^T$ 在位置 $m$ 施加旋转角 $m\theta$：

$$R_{\Theta, m}^{(2)} \mathbf{x} = \begin{pmatrix} \cos m\theta & -\sin m\theta \\ \sin m\theta & \cos m\theta \end{pmatrix} \begin{pmatrix} x_1 \\ x_2 \end{pmatrix} = \begin{pmatrix} x_1 \cos m\theta - x_2 \sin m\theta \\ x_1 \sin m\theta + x_2 \cos m\theta \end{pmatrix}$$

在复数空间中，这等价于复数乘法：$\mathbf{x}_{\text{complex}} \cdot e^{i m \theta}$。

### 2. 相对位置不变性严格证明

计算位置 $m$ 的 Query $\mathbf{q}_m$ 与位置 $n$ 的 Key $\mathbf{k}_n$ 的旋转内积：

$$\langle R_{\Theta, m}^{(2)} \mathbf{q}_m, R_{\Theta, n}^{(2)} \mathbf{k}_n \rangle = \mathbf{q}_m^T \left( R_{\Theta, m}^{(2)} \right)^T R_{\Theta, n}^{(2)} \mathbf{k}_n$$

计算矩阵乘积 $R_{\Theta, m}^T R_{\Theta, n}$：

$$\begin{aligned}
\left( R_{\Theta, m}^{(2)} \right)^T R_{\Theta, n}^{(2)} &= \begin{pmatrix} \cos m\theta & \sin m\theta \\ -\sin m\theta & \cos m\theta \end{pmatrix} \begin{pmatrix} \cos n\theta & -\sin n\theta \\ \sin n\theta & \cos n\theta \end{pmatrix} \\
&= \begin{pmatrix} \cos m\theta \cos n\theta + \sin m\theta \sin n\theta & -\cos m\theta \sin n\theta + \sin m\theta \cos n\theta \\ -\sin m\theta \cos n\theta + \cos m\theta \sin n\theta & \sin m\theta \sin n\theta + \cos m\theta \cos n\theta \end{pmatrix} \\
&= \begin{pmatrix} \cos(n-m)\theta & -\sin(n-m)\theta \\ \sin(n-m)\theta & \cos(n-m)\theta \end{pmatrix} = R_{\Theta, n-m}^{(2)}
\end{aligned}$$

证明完毕：**点积结果仅与相对距离 $n - m$ 有关！**

### 3. 高维张量块对角化

对 $d$ 维向量（设 $d$ 为偶数），拆分成 $d/2$ 个二维子空间，使用频段 $\theta_i = 10000^{-2(i-1)/d}$：

$$R_{\Theta, m}^{(d)} = \text{diag}\left( R_{\Theta, m}^{(2, \theta_1)}, R_{\Theta, m}^{(2, \theta_2)}, \dots, R_{\Theta, m}^{(2, \theta_{d/2})} \right)$$

### 4. 长上下文外推扩展 (Context Extension: YaRN, NTK-Scaling, ALiBi)

为解决 RoPE 在超长上下文（如从 4k 外推至 32k/128k）时的高频高失真问题，主流外推技术为：

1. **NTK-aware Scaling**：对底数 $\Theta$ 重新缩放 $\Theta' = \Theta \cdot s^{\frac{d}{d-2}}$（其中 $s$ 为外推倍率），动态调整高低频比例。
2. **YaRN (Yet Another RoPE Extension)**：将频率分为高频（不插值）、低频（全插值）和中频（渐进过渡），结合 Attention 熵平滑的温度因子 $\gamma$，实现长文本零样本泛化。
3. **ALiBi (Attention with Linear Biases)**：抛弃旋转矩阵，在 Attention Score 中显式注入线性负偏置 $-m \cdot |i - j|$。

---

## 4. PyTorch 最小代码实现 (Complex-based RoPE with YaRN Scale)

```python
import torch

def precompute_freqs_cis(dim: int, seq_len: int, theta: float = 10000.0, scale_factor: float = 1.0):
    # 支持 NTK-aware Scaling 动态基数调整
    theta_scaled = theta * (scale_factor ** (dim / (dim - 2)))
    freqs = 1.0 / (theta_scaled ** (torch.arange(0, dim, 2)[: (dim // 2)].float() / dim)) # [dim/2]
    t = torch.arange(seq_len, dtype=torch.float32) # [seq_len]
    freqs = torch.outer(t, freqs) # [seq_len, dim/2]
    # 构造复数 e^(i * m * theta)
    freqs_cis = torch.polar(torch.ones_like(freqs), freqs) # [seq_len, dim/2] (complex64)
    return freqs_cis

def apply_rotary_emb(xq: torch.Tensor, xk: torch.Tensor, freqs_cis: torch.Tensor):
    # xq: [Batch, Seq_Len, Num_Heads, Head_Dim]
    xq_complex = torch.view_as_complex(xq.float().reshape(*xq.shape[:-1], -1, 2))
    xk_complex = torch.view_as_complex(xk.float().reshape(*xk.shape[:-1], -1, 2))
    
    freqs_cis = freqs_cis[:xq.shape[1]].unsqueeze(0).unsqueeze(2)
    
    xq_out = torch.view_as_real(xq_complex * freqs_cis).flatten(3)
    xk_out = torch.view_as_real(xk_complex * freqs_cis).flatten(3)
    
    return xq_out.type_as(xq), xk_out.type_as(xk)

# 验证 Shape
batch, seq_len, num_heads, head_dim = 2, 8, 4, 64
q = torch.randn(batch, seq_len, num_heads, head_dim)
k = torch.randn(batch, seq_len, num_heads, head_dim)

freqs_cis = precompute_freqs_cis(head_dim, seq_len, scale_factor=2.0)
q_rope, k_rope = apply_rotary_emb(q, k, freqs_cis)

assert q_rope.shape == q.shape
assert k_rope.shape == k.shape
print("RoPE Operator (with Extrapolation Scaling) Passed! Output Shape:", q_rope.shape)
```

---

## 5. 常见误区与对比矩阵

| 评估维度 / 特性 | 绝对位置编码 (Sinusoidal) | ALiBi 线性偏置 | RoPE 旋转位置编码 (YaRN 增强) |
| :--- | :--- | :--- | :--- |
| **计算复杂度** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ 逐步旋转 |
| **相对位置表达** | 间接，需多层 MLP 逼近 | 直接显式注入 $-m \|i-j\|$ | 完美理论证明 $\langle q_m, k_n \rangle = R_{n-m}$ |
| **上下文外推性** | 极差（超出训练长度坍缩） | 极佳 | 极佳（配合 YaRN 可外推 8x~32x 长度） |
| **主流大模型应用** | 经典 Transformer / BERT | BLOOM / MPT | LLaMA 1-3 / Qwen / Mistral / DeepSeek |

---

## 6. 常见误区与易错点

### 误区：RoPE 改变了向量模长
- **正交性判定**：旋转矩阵 $R_{\Theta, m}$ 是正交矩阵 ($R^T R = I$)，因此施加 RoPE **完全不改变** $q$ 和 $k$ 的 $\ell_2$ 范数模长，仅在二维平面旋转方向。

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

- Su, J., et al. (2024). RoFormer: Enhanced Transformer with Rotary Position Embedding. *Neurocomputing*, 568.
- Peng, B., et al. (2023). YaRN: Efficient Context Window Extension of Large Language Models. *arXiv:2309.00071*.
- Press, O., Smith, N. A., & Lewis, M. (2022). Train Short, Test Long: Attention with Linear Biases (ALiBi). *ICLR 2022*.

---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《RoPE旋转位置编码》的核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？

---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《RoPE旋转位置编码》的核心机制及其与上下游模块的连接逻辑。
2. **代数/代码自测**：手写关键代数推导步骤或 PyTorch/Python 核心实现伪代码。
3. **防错自测**：如果输入序列长度突破训练阈值，如何利用 YaRN / NTK-Scaling 对频率系数做重分配？
