---
type: concept
topic: RoPE 旋转位置编码
created: '{date}'
status: learning
difficulty: intermediate
concept: []
prerequisites: []
related: []
tags:
- 学习
- 深度学习
- NLP
- RoPE
- 旋转位置编码
- Transformer
- LLM
- 相对位置编码
title: RoPE 旋转位置编码 (Rotary Position Embedding)
date: 2026-07-27
course: NLP全栈 / 大语言模型
importance: A
upstream:
- '[[Transformer注意力]]'
- '[[09-高等代数/01-基础/复数与矩阵旋转|复数与矩阵旋转]]'
downstream:
- '[[🚀 第五阶段：大语言模型与前沿技术|大语言模型架构]]'
---

# 🎯 RoPE 旋转位置编码 (Rotary Position Embedding)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：RoPE（Rotary Position Embedding，旋转位置编码）由 Jianlin Su（苏剑林）等人于 2021 年提出，是当下**现代大语言模型（LLM）的绝对标配**（LLaMA 1/2/3、Qwen、Mistral、DeepSeek 等几乎所有主流开源与商业 LLM 均使用 RoPE）。它通过非常优雅的**复数旋转矩阵**，巧夺天工般地实现了“用绝对位置编码的乘法形式，自然蕴含相对位置衰减特性”，并具备强大的外推扩展能力（NTK-Aware Scaling）。不搞懂 RoPE，就无法理解现代大语言模型的架构细节与长文本上下文扩展。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem (我们遇到了什么麻烦)**：
> 在 Transformer 中，Self-Attention 机制是位置不敏感的（Permutation Invariant）。
> - **绝对位置编码 (Absolute Positional Embedding, 如 Sinusoidal / Absolute Learned)**：直接把位置向量加到 Token 词嵌入上。缺点是无法自然表达 Token 之间的相对距离（例如“第 2 个词与第 5 个词”的相对距离 3 很难显式捕捉），且文本长度超出训练窗口后，**外推性能极差（超出上下文长度模型直接崩溃）**。
> - **传统相对位置编码 (Relative Positional Embedding, 如 T5 / DeBERTa)**：需要修改 Attention 矩阵计算，在 Key/Query 相乘时加入额外的距离偏置。缺点是**引入了复杂的偏置矩阵，计算量巨大且无法使用 FlashAttention 算子加速**。
> 我们迫切需要一种**既能像绝对位置编码一样高效（不改变 Attention 计算结构），又能完美表达相对位置，且外推性能极佳**的位置编码！

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：RoPE 成功统一了绝对位置编码的表达形式与相对位置编码的理论优势。它是现代 LLM 能够处理长文本上下文（如从 4k 拓展到 32k、128k、1M 上下文）的基础核心。
- **实际应用场景**：LLaMA 系列、Qwen 系列、DeepSeek 系列、ChatGLM 等所有现代 LLM 的 Query 和 Key 投影运算。
- **高频考点/任务**：RoPE 二维复数旋转矩阵推导、内积满足 $\langle \mathbf{R}_m \mathbf{q}, \mathbf{R}_n \mathbf{k} \rangle = g(\mathbf{q}, \mathbf{k}, m-n)$ 的证明、RoPE 在 2D 向量上的旋转公式、长文本外推 (YaRN / Dynamic NTK-aware) 原理。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[Transformer注意力|Transformer 点积注意力]]**：$q_m$ 与 $k_n$ 的注意力得分取决于点积 $\mathbf{q}_m^T \mathbf{k}_n$。
2. **[[09-高等代数/01-基础/复数与矩阵旋转|欧拉公式与二维旋转矩阵]]**：复数 $e^{i\theta} = \cos\theta + i\sin\theta$；二维向量 $\mathbf{x} = (x_1, x_2)^T$ 旋转角度 $\theta$ 的矩阵为：
   $$\mathbf{R}_{\theta} = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$$

---

## 4. 用直觉语言解释它

> «“这东西其实就像……”»

- **直觉类比**：想象钟表上的时针与分针：
  - Token 的语义特征是指针的**长度**，而 Token 的绝对位置 $m$ 则是指针在表盘上被**顺时针旋转的角度 $m\theta$**。
  - 当第 $m$ 个 Token（Query）与第 $n$ 个 Token（Key）互相看对眼做点积时（计算 Attention），两个指针在表盘上重合相乘。
  - 它们的夹角恰好就是绝对位置之差 $(m - n)\theta$！
  - 无论这两个指针旋转到表盘的什么位置（绝对位置 $m$ 和 $n$ 是多少），只要它们的**相对角度差 $(m-n)\theta$ 一样**，它们算出来的点积得分就完全一样！
- **为什么很自然**：二维平面上的向量内积对旋转具有**不变性**（Rotation Invariance）！旋转 $\mathbf{q}$ 和 $\mathbf{k}$ 后，点积自然只取决于两者的相对旋转角差 $\mathbf{R}_m^T \mathbf{R}_n = \mathbf{R}_{n-m}$。
- **一句话直觉本质**：将特征向量按维度配成二维平面，用位置 $m$ 对应的角度旋转向量，使点积天然只依赖于相对位置差 $m-n$。

---

## 5. 正式定义、核心公式、符号解释

### 1. 核心定义与旋转矩阵
设第 $m$ 个位置的 Query 向量为 $\mathbf{q}_m \in \mathbb{R}^d$（维度 $d$ 为偶数）。将 $\mathbf{q}_m$ 拆分为 $d/2$ 个二维子向量，第 $i$ 个二维平面赋值旋转矩阵 $\mathbf{R}_{\Theta, m}^{(i)}$：
$$\mathbf{R}_{\Theta, m}^{(d)} = \text{diag}\left( \mathbf{R}_{\theta_1, m}, \mathbf{R}_{\theta_2, m}, \dots, \mathbf{R}_{\theta_{d/2}, m} \right)$$
其中二维块旋转矩阵定义为：
$$\mathbf{R}_{\theta_i, m} = \begin{pmatrix} \cos(m\theta_i) & -\sin(m\theta_i) \\ \sin(m\theta_i) & \cos(m\theta_i) \end{pmatrix}$$

### 2. 角度频率定义 ($\theta_i$)
借鉴 Transformer 正弦位置编码的频率设计：
$$\theta_i = 10000^{-2(i-1)/d}, \quad i \in \{1, 2, \dots, d/2\}$$

### 3. 相对位置内积证明性公式
对嵌入了 RoPE 的 $\tilde{\mathbf{q}}_m = \mathbf{R}_{\Theta, m} \mathbf{q}_m$ 与 $\tilde{\mathbf{k}}_n = \mathbf{R}_{\Theta, n} \mathbf{k}_n$ 求点积：
$$\langle \tilde{\mathbf{q}}_m, \tilde{\mathbf{k}}_n \rangle = (\mathbf{R}_{\Theta, m} \mathbf{q}_m)^T (\mathbf{R}_{\Theta, n} \mathbf{k}_n) = \mathbf{q}_m^T \mathbf{R}_{\Theta, m}^T \mathbf{R}_{\Theta, n} \mathbf{k}_n = \mathbf{q}_m^T \mathbf{R}_{\Theta, n-m} \mathbf{k}_n$$
内积结果仅与相对距离 $n-m$ 有关！

### 4. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $m, n$ | Token 的绝对位置索引 | $0, 1, 2, \dots, L-1$ | 序列中的位置 |
| $\mathbf{q}_m$ | 未施加位置编码的原始 Query 向量 | $\mathbb{R}^d$ | 线性层输出 |
| $\theta_i$ | 第 $i$ 个二维频道的基频 | $(0, 1]$ | 高频控制短距离，低频控制长距离 |
| $\mathbf{R}_{\Theta, m}$ | 高维块对角旋转矩阵 | $\mathbb{R}^{d \times d}$ | 正交矩阵 ($\mathbf{R}^T \mathbf{R} = \mathbf{I}$) |

---

## 6. 推导思路和思想来源

- **最初困难**：寻找一个函数 $f(\mathbf{x}, m)$，使得两个施加了位置信息的向量点积满足：
  $$\langle f(\mathbf{q}, m), f(\mathbf{k}, n) \rangle = g(\mathbf{q}, \mathbf{k}, m-n)$$
- **关键转念 1（借助复数表达）**：
  在二维复数平面上，向量 $\mathbf{x} = x_1 + i x_2$ 可以写成指数形式 $x = r e^{i\phi}$。
  令位置编码为乘以一个复数相量 $e^{i m \theta}$：
  $$f(\mathbf{q}, m) = \mathbf{q} \cdot e^{i m \theta}$$
  此时计算点积（复数内积 $\text{Re}[\mathbf{q}_m \mathbf{k}_n^*]$）：
  $$\text{Re}\left[ (\mathbf{q} e^{i m \theta}) (\mathbf{k} e^{i n \theta})^* \right] = \text{Re}\left[ \mathbf{q} \mathbf{k}^* e^{i (m-n) \theta} \right]$$
  复数相乘的模长不变、相位相减！绝对位置 $m$ 和 $n$ 在内积中神奇地相减消去，只留下了相对位置 $(m-n)$！
- **关键转念 2（高维推广）**：
  由于 $d$ 维向量可以等价拆分为 $d/2$ 个独立的二维复数平面，将 $d/2$ 个复数乘法转写为矩阵形式，即得到了块对角正交矩阵 $\mathbf{R}_{\Theta, m}$！

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（二维向量手算 RoPE 旋转）
- **题目**：已知某二维 Query 向量 $\mathbf{q} = (1, 0)^T$，基频 $\theta = \frac{\pi}{2}$，位置 $m = 1$。求施加 RoPE 旋转后的向量 $\tilde{\mathbf{q}}$。
- **解答过程**：
  1. 计算旋转角度：$m\theta = 1 \times \frac{\pi}{2} = \frac{\pi}{2}$。
  2. 构建二维旋转矩阵：
     $$\mathbf{R}_{\pi/2} = \begin{pmatrix} \cos(\pi/2) & -\sin(\pi/2) \\ \sin(\pi/2) & \cos(\pi/2) \end{pmatrix} = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$$
  3. 计算旋转后的向量：
     $$\tilde{\mathbf{q}} = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$$
- **🤔 追问**：若此时位置 $n = 3$ 的 Key 向量 $\mathbf{k} = (1, 0)^T$，求它们的 RoPE 点积 $\tilde{\mathbf{q}}_1^T \tilde{\mathbf{k}}_3$。
  - *答*：$\mathbf{R}_{3\pi/2} \mathbf{k} = (0, -1)^T$。点积 $\tilde{\mathbf{q}}_1^T \tilde{\mathbf{k}}_3 = 0\times 0 + 1\times(-1) = -1$。
  - 直接用相对位置 $n-m = 2$ 计算：旋转角 $2 \times \frac{\pi}{2} = \pi \implies \cos\pi = -1$，结果完全一致！

### 例子 2：中等例子（RoPE 的高效矩阵计算实现）
在实际代码中，显式乘以 $d \times d$ 稀疏矩阵非常慢。利用三角展开，RoPE 可以改写为逐元素按位相乘形式：
$$\mathbf{R}_{\Theta, m} \mathbf{x} = \mathbf{x} \odot \cos(m\boldsymbol{\Theta}) + \tilde{\mathbf{x}} \odot \sin(m\boldsymbol{\Theta})$$
其中 $\tilde{\mathbf{x}} = (-x_2, x_1, -x_4, x_3, \dots, -x_d, x_{d-1})$（把相邻元素对调并加负号）。这种逐元素实现使得 RoPE 的计算耗时几乎为 0！

### 例子 3：实际应用（PyTorch 手写 LLaMA 风格可运行 RoPE 模块）

```python
import torch
import torch.nn as nn

class RotaryEmbedding(nn.Module):
    def __init__(self, dim, max_position_embeddings=2048, base=10000):
        super().__init__()
        self.dim = dim
        # 1. 预计算频率 theta_i = 10000^(-2i/dim)
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq)
        
        # 2. 预建位置外积矩阵
        t = torch.arange(max_position_embeddings).float()
        freqs = torch.einsum("i,j->ij", t, self.inv_freq)
        # 扩展为 [cos, sin]
        emb = torch.cat((freqs, freqs), dim=-1)
        self.register_buffer("cos_cached", emb.cos()[None, None, :, :])
        self.register_buffer("sin_cached", emb.sin()[None, None, :, :])

    def _rotate_half(self, x):
        # 将 (-x2, x1, -x4, x3...)
        x1 = x[..., : self.dim // 2]
        x2 = x[..., self.dim // 2 :]
        return torch.cat((-x2, x1), dim=-1)

    def forward(self, q, k, seq_len=None):
        # q, k 维度: [batch, num_heads, seq_len, head_dim]
        cos = self.cos_cached[:, :, :seq_len, :]
        sin = self.sin_cached[:, :, :seq_len, :]
        
        # 应用 RoPE 旋转: q_embed = (q * cos) + (rotate_half(q) * sin)
        q_embed = (q * cos) + (self._rotate_half(q) * sin)
        k_embed = (k * cos) + (self._rotate_half(k) * sin)
        return q_embed, k_embed

# 验证代码
rope = RotaryEmbedding(dim=64)
q = torch.randn(2, 8, 512, 64) # Batch=2, Heads=8, Seq=512, HeadDim=64
k = torch.randn(2, 8, 512, 64)
q_out, k_out = rope(q, k, seq_len=512)
print("RoPE 作用后的 Query 维度:", q_out.shape) # [2, 8, 512, 64]
```

---

## 8. 常见误区和易混概念

### 误区 1：RoPE 施加在 Transformer 的输入 Embedding 层（像 Sinusoidal 一样）
- **错误直觉**：“RoPE 也是一种位置编码，应该像原始 Transformer 那样在最初 `x = token_embed + pos_embed` 一次性加进去。”
- **为什么错**：RoPE 必须在**每一层注意力机制的 Query 和 Key 计算完成之后、进行点积乘法之前**实时作用在 $q$ 和 $k$ 向量上！ Value 向量 $v$ 不需要施加 RoPE。

### 概念对比表

| 位置编码类型 | 相对位置表达能力 | 是否改变 Attention 逻辑 | 长文本外推能力 | 算子优化友好性 (FlashAttn) | 代表模型 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **绝对正弦 (Sinusoidal)** | 弱（依靠隐式拟合） | 否（直接相加） | 极差 | 极好 | Transformer, BERT |
| **T5 相对偏置** | 极强（显式距离表） | **是**（修改 Attn 矩阵） | 一般 | 极差（无法用 FlashAttn） | T5 |
| **RoPE 旋转编码** | **极强（正交旋转角）** | **否（作用于 q/k）** | **极强（可插值缩放）**| **极好（完美支持 FlashAttn）** | **LLaMA, Qwen, DeepSeek** |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[Transformer注意力]]：了解点积注意力 $\mathbf{q}^T \mathbf{k}$ 的核心计算方式。
- [[09-高等代数/01-基础/复数与矩阵旋转|复数与矩阵旋转]]：二维旋转矩阵与欧拉公式的几何含义。

### 下游延伸
- [[🚀 第五阶段：大语言模型与前沿技术|大语言模型架构]]：LLaMA, Qwen, DeepSeek 等模型的核心实现细节。

### 横向关联
- [[ALiBi]] ↔ [[RoPE 旋转位置编码|RoPE]]：两大主流长文本位置编码方案，ALiBi 采用线性偏置衰减，RoPE 采用旋转插值外推。

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清楚 RoPE 解决什么问题（结合绝对位置形式与相对位置表达，且支持长文本外推）。
- [ ] 2. 用直觉语言解释它（«“这东西其实就像表盘指针旋转与夹角……”»）。
- [ ] 3. 写出二维 RoPE 旋转矩阵与多维块对角矩阵。
- [ ] 4. 推导为什么 $\langle \mathbf{R}_m \mathbf{q}, \mathbf{R}_n \mathbf{k} \rangle$ 的内积只依赖于 $m-n$。
- [ ] 5. 解释为什么 RoPE 作用在 Query 和 Key 上，而不作用在 Value 上。
- [ ] 6. 说明 RoPE 如何用逐元素按位相乘 $\mathbf{x} \cos + \tilde{\mathbf{x}} \sin$ 代替稀疏矩阵乘法。
- [ ] 7. 手算二维向量 RoPE 旋转与点积。
- [ ] 8. 对比 RoPE 与 T5 相对位置编码在 FlashAttention 兼容性上的差异。
- [ ] 9. 手写包含 `_rotate_half` 的 PyTorch RoPE 核心代码。
- [ ] 10. 简述 Dynamic NTK-aware 缩放如何拓展 RoPE 的上下文长度（如 4k $\to$ 32k）。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | RoPE 的作用位置 |
| 2 | 公式计算 | 基础 | 二维向量 RoPE 旋转计算 |
| 3 | 条件判断 | 中等 | RoPE 旋转矩阵的正交性 |
| 4 | 变式/外推 | 中等 | NTK-Aware Scaling 扩展上下文原理 |
| 5 | 开放/证明 | 较难 | 证明复数旋转相乘导致相位相减 |

### 题目与解析

#### 1. RoPE（旋转位置编码）施加在 Transformer 架构的哪个模块中？
- A. 输入层（Input Embedding）之后
- B. Feed-Forward Network (FFN) 之后
- C. Self-Attention 中计算出 Query 和 Key 之后、计算点积得分之前
- D. Layer Normalization 之后

> [!question]- 答案解析
> - **答案**：C
> - **解析**：RoPE 专门作用于 Attention 模块中的 Query 向量 $\mathbf{q}$ 与 Key 向量 $\mathbf{k}$，利用正交旋转使点积 $\mathbf{q}^T \mathbf{k}$ 包含相对位置信息。
> - **对应误区**：误区 1。

#### 2. 已知某二维向量 $\mathbf{q} = (0, 2)^T$，位置 $m=1$，角度 $\theta = \frac{\pi}{6}$（$\cos(\pi/6) = \frac{\sqrt{3}}{2}, \sin(\pi/6) = \frac{1}{2}$）。求旋转后的向量 $\tilde{\mathbf{q}}$。
> [!question]- 答案解析
> - **答案**：$\tilde{\mathbf{q}} = (-1, \sqrt{3})^T$。
> - **解析**：
>   $$\tilde{\mathbf{q}} = \begin{pmatrix} \cos(\pi/6) & -\sin(\pi/6) \\ \sin(\pi/6) & \cos(\pi/6) \end{pmatrix} \begin{pmatrix} 0 \\ 2 \end{pmatrix} = \begin{pmatrix} \frac{\sqrt{3}}{2} & -\frac{1}{2} \\ \frac{1}{2} & \frac{\sqrt{3}}{2} \end{pmatrix} \begin{pmatrix} 0 \\ 2 \end{pmatrix} = \begin{pmatrix} -1 \\ \sqrt{3} \end{pmatrix}$$

#### 3. 为什么 RoPE 旋转矩阵 $\mathbf{R}_{\Theta, m}$ 满足正交矩阵性质 $\mathbf{R}^T \mathbf{R} = \mathbf{I}$ 对注意力计算极其关键？
> [!question]- 答案解析
> - **答案**：保证特征向量的模长（Norm）保持不变，不破坏 Attention 密度的数值稳定性。
> - **解析**：正交矩阵充当等距变换（Isometry），向量旋转后模长 $\|\mathbf{R} \mathbf{q}\| = \|\mathbf{q}\|$ 完全不改变，不会因为位置 $m$ 很大而导致 Query 或 Key 向量发生数值爆炸或消失。

#### 4. 在长文本拓展（Context Window Extension）中，动态 NTK-Aware Scaling 是如何修改 RoPE 的基频 $\text{base}=10000$ 的？
> [!question]- 答案解析
> - **答案**：将基频按照扩展倍数 $\alpha$ 增大，即 $\text{base}' = \text{base} \cdot \alpha^{\frac{d}{d-2}}$。
> - **解析**：直接外推高频部分会导致模型失去分辨率，直接插值低频部分会导致高频信号混叠。NTK-Aware Scaling 通过神经网络神经切线核 (NTK) 理论，保持高频信号不插值、放宽低频信号的旋转周期，从而实现免微调的情况下将上下文窗口无损扩大 4~8 倍。

#### 5. 【证明】利用复数欧拉公式 $e^{i\theta} = \cos\theta + i\sin\theta$，证明两复数旋转相乘点积只与角度差有关。
> [!question]- 答案解析
> - **证明**：
>   设复数 $q = r_q e^{i \phi_q}$，$k = r_k e^{i \phi_k}$。
>   位置 $m$ 旋转后的 $q_m = q \cdot e^{i m \theta} = r_q e^{i(\phi_q + m\theta)}$；
>   位置 $n$ 旋转后的 $k_n = k \cdot e^{i n \theta} = r_k e^{i(\phi_k + n\theta)}$。
>   两复数的内积定为 $\text{Re}[q_m k_n^*]$（其中 $k_n^*$ 为共轭）：
>   $$\text{Re}\left[ r_q e^{i(\phi_q + m\theta)} \cdot r_k e^{-i(\phi_k + n\theta)} \right] = r_q r_k \text{Re}\left[ e^{i(\phi_q - \phi_k + (m-n)\theta)} \right] = r_q r_k \cos(\phi_q - \phi_k + (m-n)\theta)$$
>   结果中位置项仅出现 $(m-n)$，证明完毕！

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

### 我的推导复现
> 不看上文，尝试写出核心公式或推导主线：

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型/`
- **建议双链**：
  - [[Transformer注意力]]
  - [[09-高等代数/01-基础/复数与矩阵旋转|复数与矩阵旋转]]
  - [[🚀 第五阶段：大语言模型与前沿技
