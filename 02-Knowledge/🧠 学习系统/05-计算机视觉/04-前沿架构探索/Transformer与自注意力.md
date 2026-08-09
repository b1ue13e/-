---
type: study
course: "05-计算机视觉"
topic: "Transformer与自注意力机制"
created: 2026-08-05
status: ongoing
difficulty: advanced
concept: ["Transformer","自注意力","多头注意力","位置编码","ViT"]
prerequisites: ["反向传播与计算图", "Softmax与SVM损失函数", "线性代数基础CV"]
related: ["ViT","SwinTransformer","CLIP","CNN"]
flow: knowledge
upstream: ["[[Softmax与SVM损失函数]]", "[[批归一化BatchNorm]]"]
stage_moc: "[[🧭 阶段4-前沿架构探索]]"
kind: concept
source: "CS231n A3; D2L Ch.11"
anki_deck: "05-计算机视觉::04-前沿架构探索"
anki_tags: ["计算机视觉","Transformer","自注意力"]
tags: [学习,计算机视觉,Transformer,自注意力,注意力机制]
---

# 🔷 Transformer 与自注意力机制

---

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：Transformer 由 Vaswani 等人在 "Attention Is All You Need" (NeurIPS 2017) 中提出，最初在 NLP 领域彻底替代 RNN/LSTM，随后以 ViT (Dosovitskiy et al., 2021) 大规模入侵计算机视觉，成为**当代 CV 架构的第一性原理基石**。此后的 Swin Transformer、DETR、CLIP、Stable Diffusion 等全部建立在 Self-Attention 之上。不搞懂 QKV 机制与 Multi-Head Attention，就无法理解 2022 年之后的任何前沿模型。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem（我们遇到了什么麻烦）**：
> 卷积神经网络 (CNN) 的卷积核受限于**局部感受野 (Local Receptive Field)**——一个 $3 \times 3$ 的卷积核一次只能看见局部邻域 9 个像素。虽然堆叠多层可以增大感受野，但这种增长是**线性的（随层数增加）**和**间接的（需逐层传递）**。对于语义分割中相距很远的两个像素是否属于同一物体（如远处桌子的左腿和右腿），CNN 需要几十层才能让信号跨越整张特征图。
>
> 更关键的是：**CNN 的局部连接是一种硬编码的"归纳偏置 (Inductive Bias)"**——它在数据少时帮助泛化，但也限制了模型学习"任意位置之间的任意关系"的能力。我们想要一种机制：**让特征图上的每两个位置之间都能直接通信，不再依赖层数逐层传递**。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：Self-Attention 是 Transformer 的核心引擎，也是 Vision Transformer (ViT)、DETR、MAE、CLIP 等全部现代 CV 模型的共享基础件。它把"序列建模"从 NLP 带到了 CV，催生了多模态大一统架构。
- **实际应用场景**：图像分类 (ViT)、目标检测 (DETR)、语义分割 (SegFormer)、图像生成 (DiT / Stable Diffusion 3)、视觉-语言多模态对齐 (CLIP)。
- **高频考点/任务**：手写 Scaled Dot-Product Attention 的 PyTorch 实现、推导 $\sqrt{d_k}$ 缩放的必要性、Multi-Head 的分组并行与维度拆分、正弦位置编码的公式推导、与 CNN 的归纳偏置比较。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[Softmax与SVM损失函数|Softmax 函数]]**：将一组注意力分数转化为概率分布 $\text{softmax}(\mathbf{s})_i = \frac{\exp(s_i)}{\sum_j \exp(s_j)}$。
2. **矩阵乘法**：理解 $QK^T$ 的批次维度与特征维度的对应关系是掌握 Self-Attention 的核心前提。
3. **[[批归一化BatchNorm|层归一化 (Layer Normalization)]]**：Transformer Encoder 中 Add & Norm 的归一化组件，不同于 CNN 常用的 BatchNorm。

---

## 4. 用直觉语言解释它

> «"这东西其实就像……"»

- **直觉类比**：Self-Attention 像是**会议室讨论**——每个 token 是一个参会者。他发出 **Query**（"谁跟我相关？"），每个人提供 **Key**（"这是我的资料卡"）供检索。Query 与 Key 匹配度高的，就大量采纳对方的 **Value**（"你的想法"）。与 CNN 不同：CNN 只能和邻居说话（局部感受野），Self-Attention 全屋所有人同时交流——**一层即全局**。
- **一句话直觉本质**：让每个位置根据内容相似度（$QK^T$）动态聚合全局信息（加权 $V$），实现"该看谁、看多少"的内容寻址。

---

## 5. 正式定义、核心公式、符号解释

### 5.1 Scaled Dot-Product Attention（缩放点积注意力）

从输入序列 $\mathbf{X} \in \mathbb{R}^{N \times d_{\text{model}}}$ 出发（$N$ = 序列长度 / token 数，$d_{\text{model}}$ = 模型维度），通过三个可学习的线性投影得到 Query、Key、Value：

$$\mathbf{Q} = \mathbf{X} \mathbf{W}^Q, \quad \mathbf{K} = \mathbf{X} \mathbf{W}^K, \quad \mathbf{V} = \mathbf{X} \mathbf{W}^V$$

其中 $\mathbf{W}^Q, \mathbf{W}^K, \mathbf{W}^V \in \mathbb{R}^{d_{\text{model}} \times d_k}$（通常 $d_k = d_{\text{model}} / h$）。

**核心公式**：

$$\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(\frac{\mathbf{Q} \mathbf{K}^T}{\sqrt{d_k}}\right) \mathbf{V}$$

**逐步解读**（从内到外）：

1. **$\mathbf{Q}\mathbf{K}^T \in \mathbb{R}^{N \times N}$**：注意力得分矩阵。第 $(i, j)$ 个元素 = token $i$ 的 Query 与 token $j$ 的 Key 的点积，衡量 $i$ 对 $j$ 的"关注度"。
2. **$\frac{\cdot}{\sqrt{d_k}}$**：缩放因子。当 $d_k$ 较大时，点积值的方差 = $d_k$，导致 Softmax 进入饱和区（梯度趋近于 0）。除以 $\sqrt{d_k}$ 将方差稳定在 1，保持梯度健康。
3. **$\text{softmax}(\cdot)$**：沿每一行（每个 Query 对所有 Key）归一化为概率分布，$\sum_{j} \alpha_{ij} = 1$。
4. **$\times \mathbf{V}$**：用注意力权重对 Value 加权求和，得到每个 token 的上下文聚合输出。

### 5.2 Multi-Head Attention（多头注意力）

单头注意力只能捕获一种"关系模式"（如语法关系）。多头注意力让模型同时从 $h$ 个不同的子空间学习不同类型的依赖：

$$\text{MultiHead}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) \mathbf{W}^O$$

其中每个 head 独立计算：

$$\text{head}_i = \text{Attention}(\mathbf{X} \mathbf{W}_i^Q, \mathbf{X} \mathbf{W}_i^K, \mathbf{X} \mathbf{W}_i^V)$$

投影矩阵维度：$\mathbf{W}_i^Q, \mathbf{W}_i^K, \mathbf{W}_i^V \in \mathbb{R}^{d_{\text{model}} \times d_k}$，其中 $d_k = d_{\text{model}} / h$（拼接后恢复原维度）。

### 5.3 Positional Encoding（位置编码）

Self-Attention 本身是**置换等变 (Permutation Equivariant)** 的——打乱输入顺序，输出也相应打乱，但输出的值不变。这意味着它**天然对位置不敏感**，必须显式注入位置信息。

**正弦位置编码 (Sinusoidal PE)**——原始 Transformer 使用：

$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i / d_{\text{model}}}}\right)$$

$$PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i / d_{\text{model}}}}\right)$$

- $pos$：token 在序列中的位置（0, 1, 2, ...）。
- $i$：维度索引（0, 1, ..., $d_{\text{model}}/2 - 1$）。
- **直觉**：不同维度 $i$ 对应不同波长的正弦波（从高频到低频），这使得位置编码像一个"多分辨率时钟"，每个位置有一个独一无二的签名。而且 $PE_{pos+k}$ 可以表示为 $PE_{pos}$ 的线性函数，赋予了模型外推到训练未见长度的能力。

**可学习位置编码 (Learnable PE)**：ViT 等现代 CV 模型常用——直接将位置编码初始化为可学习参数 $\mathbf{E}_{\text{pos}} \in \mathbb{R}^{N \times d_{\text{model}}}$，加在输入上一起训练。

### 5.4 Transformer Encoder 完整结构

一个 Encoder Block（标准 Transformer Encoder 的重复单元）：

```
输入 X
  │
  ├──→ Multi-Head Self-Attention ──→ Add & LayerNorm ──→ │
  │                                                       ├──→ 输出
  └──→ Feed-Forward Network (FFN) ──→ Add & LayerNorm ──→ │
```

1. **Multi-Head Self-Attention**：全局交互——每个 token 与所有 token 交换信息。
2. **Add (Residual Connection)**：$\mathbf{X}_{\text{out}} = \mathbf{X} + \text{Sublayer}(\mathbf{X})$，确保梯度流畅传递、支持深层训练。
3. **LayerNorm**：对每个 token 的特征维度归一化（不同于 BatchNorm 跨 batch 归一化）。
4. **Feed-Forward Network (FFN)**：两层 MLP，通常 $\text{FFN}(\mathbf{x}) = \text{GELU}(\mathbf{x}\mathbf{W}_1 + \mathbf{b}_1)\mathbf{W}_2 + \mathbf{b}_2$，中间维度为 $4 \times d_{\text{model}}$。FFN 提供逐位置的"思考"能力——Attention 负责"跟谁交流"，FFN 负责"交流后的独立思考"。

### 5.5 符号说明表

| 符号 | 含义 | 形状 / 维度 | 备注 |
| :--- | :--- | :--- | :--- |
| $\mathbf{X}$ | 输入序列 / token 嵌入 | $\mathbb{R}^{N \times d_{\text{model}}}$ | N = 序列长度，如图像 patch 数 |
| $\mathbf{Q}, \mathbf{K}, \mathbf{V}$ | Query / Key / Value 矩阵 | $\mathbb{R}^{N \times d_k}$ | 三个投影并行独立计算 |
| $\mathbf{W}^Q, \mathbf{W}^K, \mathbf{W}^V$ | QKV 投影权重 | $\mathbb{R}^{d_{\text{model}} \times d_k}$ | 每个头一组独立参数 |
| $\mathbf{W}^O$ | 多头拼接后输出投影 | $\mathbb{R}^{h d_k \times d_{\text{model}}}$ | 恢复 $d_{\text{model}}$ 维度 |
| $d_{\text{model}}$ | 模型隐藏维度 | 标量，如 512 / 768 | 贯穿整个 Encoder 的恒定维度 |
| $d_k$ | 单头 Key/Query 维度 | 标量，$d_{\text{model}} / h$ | 如 $512 / 8 = 64$ |
| $h$ | 注意力头数 | 标量，如 8 / 12 | 并行子空间数量 |
| $N$ | 序列长度 | 标量 | 对于 ViT：图像 patch 数 + 1 (CLS) |
| $\sqrt{d_k}$ | 缩放因子 | 标量 | 稳定 Softmax 梯度 |

---

## 6. 推导思路和思想来源

- **最初困难**：在 RNN/LSTM 时代，序列建模依赖循环连接——第 $t$ 步必须等待第 $t-1$ 步完成，计算不可并行；且长距离依赖需要信号穿过 $O(N)$ 个时间步，梯度易消失/爆炸。
- **Attention 的早期形态 (Bahdanau, 2015)**：在 Seq2Seq 中作为"对齐机制"，让 Decoder 在生成每个输出词时可以动态"看向"Encoder 的不同位置。但 Attention 仍只是 RNN 的辅助配件，不是主体。
- **关键转念 (Vaswani et al., 2017)**：完全抛弃循环结构，**用 Attention 做唯一的信息传递机制**。核心洞察是：如果每个 token $i$ 都需要从所有 token 聚合信息，最自然的做法就是计算 $i$ 与每个 $j$ 的匹配分数，然后 softmax 加权求和。这个过程全部是矩阵乘法——高度并行，GPU 友好！
- **QKV 的设计来源**：借鉴信息检索领域——Query（用户查询）匹配 Key（文档索引），返回 Value（文档内容）。Self-Attention 的"Self"体现在 Q、K、V 来自同一个序列——让序列自己查询自己，从而发现内部依赖关系。
- **为什么是 $\frac{1}{\sqrt{d_k}}$ 而不是别的常数？**：假设 $\mathbf{q}, \mathbf{k}$ 的每个分量独立 $\sim \mathcal{N}(0, 1)$，点积 $\mathbf{q} \cdot \mathbf{k} = \sum_{i=1}^{d_k} q_i k_i$ 的方差 = $\sum \text{Var}(q_i k_i) = d_k$。当 $d_k$ 大（如 64~128）时，点积值可能很大（如 $\pm 20$），Softmax 输出逼近 one-hot（梯度 $\to 0$）。除以 $\sqrt{\text{Var}} = \sqrt{d_k}$ 将方差拉回 1。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（2 个 token 的 Self-Attention 手算）

**题目**：设 $d_{\text{model}} = 2$，$d_k = 2$（单头），两个 token $\mathbf{x}_1 = [1, 0]^T$，$\mathbf{x}_2 = [0, 1]^T$。权重矩阵为：

$$\mathbf{W}^Q = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}, \quad \mathbf{W}^K = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}, \quad \mathbf{W}^V = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$$

计算 Self-Attention 输出。

**解答过程**：

1. **计算 Q, K, V**：
   $$\mathbf{Q} = \mathbf{X} \mathbf{W}^Q = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$$
   $$\mathbf{K} = \mathbf{X} \mathbf{W}^K = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$$

2. **计算注意力得分** $\mathbf{Q}\mathbf{K}^T$：
   $$\mathbf{Q}\mathbf{K}^T = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}^T = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$$
   解读：token 1 对 token 1 的得分为 0，对 token 2 为 1；token 2 对 token 1 为 1，对自己为 0。

3. **缩放** $\frac{\cdot}{\sqrt{2}} \approx \frac{\cdot}{1.414}$：
   $$\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{2}} = \begin{bmatrix} 0 & 0.707 \\ 0.707 & 0 \end{bmatrix}$$

4. **Softmax（每行）**：
   $$\text{softmax}(\text{第1行}) = \left[ \frac{e^0}{e^0+e^{0.707}}, \frac{e^{0.707}}{e^0+e^{0.707}} \right] \approx [0.330, 0.670]$$
   $$\text{softmax}(\text{第2行}) \approx [0.670, 0.330]$$
   $$\mathbf{A} = \begin{bmatrix} 0.330 & 0.670 \\ 0.670 & 0.330 \end{bmatrix}$$

5. **加权 Value（$\mathbf{V} = \mathbf{X}$，因为 $\mathbf{W}^V = \mathbf{I}$）**：
   $$\text{Output} = \mathbf{A} \mathbf{V} = \begin{bmatrix} 0.330 & 0.670 \\ 0.670 & 0.330 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 0.330 & 0.670 \\ 0.670 & 0.330 \end{bmatrix}$$

- **🤔 追问**：$\mathbf{x}_1 = [1,0]$ 的输出变成了 $[0.330, 0.670]$。这意味着什么？
  - *答*：token 1 只花了 33% 注意力在自己身上，却花了 67% 注意力在 token 2 身上——因为它发现自己的 Key 与 token 2 的 Query 更匹配（注意这里的 K 矩阵做了交换，$K_1 = [0,1]$ 匹配 $Q_2 = [0,1]$）。Self-Attention 让每个 token 根据内容相似度聚合了整个序列的信息。

### 例子 2：中等例子（Multi-Head 维度拆分推导）

**题目**：设 $d_{\text{model}} = 6$，$h = 3$，$N = 4$。说明 Multi-Head Attention 如何将输入 $\mathbf{X} \in \mathbb{R}^{4 \times 6}$ 拆分计算并拼接。

**解答**：
- 单头维度 $d_k = d_{\text{model}} / h = 6 / 3 = 2$。
- $\mathbf{W}^Q \in \mathbb{R}^{6 \times 6}$（所有头合并投影），将其拆分为 $[\mathbf{W}_1^Q | \mathbf{W}_2^Q | \mathbf{W}_3^Q]$ 三块，每块 $\mathbb{R}^{6 \times 2}$。
- head 1：$\mathbf{Q}_1 = \mathbf{X} \mathbf{W}_1^Q \in \mathbb{R}^{4 \times 2}$，$\mathbf{K}_1, \mathbf{V}_1$ 同理 → $\text{head}_1 = \text{softmax}(\frac{\mathbf{Q}_1 \mathbf{K}_1^T}{\sqrt{2}}) \mathbf{V}_1 \in \mathbb{R}^{4 \times 2}$。
- head 2、head 3 同理并行计算。
- 拼接：$\text{Concat}(\text{head}_1, \text{head}_2, \text{head}_3) \in \mathbb{R}^{4 \times 6}$。
- 输出投影：$\text{MultiHead} = \text{Concat} \cdot \mathbf{W}^O \in \mathbb{R}^{4 \times 6}$。

### 例子 3：实际应用（PyTorch 完整实现）

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class MultiHeadSelfAttention(nn.Module):
    def __init__(self, d_model=512, num_heads=8, dropout=0.1):
        super().__init__()
        assert d_model % num_heads == 0
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.W_qkv = nn.Linear(d_model, 3 * d_model, bias=False)  # QKV 合并投影
        self.W_o   = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # x: (B, N, D)   输出: (B, N, D)
        B, N, D = x.shape
        qkv = self.W_qkv(x).reshape(B, N, 3, self.num_heads, self.d_k)
        qkv = qkv.permute(2, 0, 3, 1, 4)       # (3, B, h, N, d_k)
        Q, K, V = qkv[0], qkv[1], qkv[2]

        # Scaled Dot-Product Attention
        scale = math.sqrt(self.d_k)
        attn = F.softmax((Q @ K.transpose(-2, -1)) / scale, dim=-1)
        attn = self.dropout(attn)
        context = attn @ V                        # (B, h, N, d_k)

        # 拼接 + 输出投影
        context = context.transpose(1, 2).reshape(B, N, D)
        return self.W_o(context)


class TransformerEncoderBlock(nn.Module):
    """Encoder Block: x → MHA(Pre-LN) → Add → FFN(Pre-LN) → Add"""
    def __init__(self, d_model=512, num_heads=8, d_ff=2048, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadSelfAttention(d_model, num_heads, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff), nn.GELU(), nn.Dropout(dropout),
            nn.Linear(d_ff, d_model), nn.Dropout(dropout),
        )

    def forward(self, x):
        x = x + self.self_attn(self.norm1(x))    # MHA + Add&Norm
        x = x + self.ffn(self.norm2(x))           # FFN + Add&Norm
        return x
```

---

## 8. 常见误区和易混概念

### 误区 1：Self-Attention 和 Cross-Attention 是一回事
- **错误**：Self-Attention 的 Q、K、V 来自同一序列（自己查自己）；Cross-Attention 的 Q 来自 Decoder，K、V 来自 Encoder。前者负责序列内部整合，后者负责序列间桥接。

### 误区 2：Transformer 不需要位置编码也能工作
- **错误**：$Q_i \cdot K_j$ 中没有位置信息。没有 PE 时 Self-Attention 是置换等变的（"猫追狗"和"狗追猫"输出相同）。PE 是 Transformer 感知顺序的唯一通道。

### 误区 3：Multi-Head 就是多做几次取平均
- **错误**：每个头有独立的投影矩阵 $\mathbf{W}_i^Q, \mathbf{W}_i^K, \mathbf{W}_i^V$，在不同子空间学习互补的关系模式（语法、语义、位置等），不是简单取平均。

### 概念对比表

| 概念 | 核心运算 | 交互范围 | 参数依赖性 | CV 应用代表 |
| :--- | :--- | :--- | :--- | :--- |
| **卷积 (Conv)** | $W * X$（局部滑动） | 局部固定核窗口 | 权重与输入值无关 | ResNet, VGG |
| **Self-Attention** | $\text{softmax}(QK^T/\sqrt{d_k}) V$ | 全局所有位置 | 权重依赖输入内容 | ViT, DETR |
| **Cross-Attention** | $\text{softmax}(Q_{\text{dec}} K_{\text{enc}}^T/\sqrt{d_k}) V_{\text{enc}}$ | Dec→Enc 全局 | Q和KV来源不同 | CLIP, DETR Decoder |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[Softmax与SVM损失函数]]：Softmax 将得分转化为概率分布，是 Attention 的归一化层。
- [[批归一化BatchNorm]]：Transformer 使用的归一化方式，对每个 token 的特征维度归一化。
- Residual Connection：Add 操作的来源——ResNet 提出的跳跃连接是 Transformer 深层可训练的关键。

### 下游延伸
- [[计算机视觉-ViT]] (Vision Transformer)：将图像切割为 patch 序列，直接喂入 Transformer Encoder 做分类。
- [[计算机视觉-SwinTransformer]]：引入窗口注意力和移位窗口，让 Transformer 兼容高分辨率视觉任务。
- [[目标检测RCNN与YOLO]]：用 Transformer Encoder-Decoder + Object Query 做端到端目标检测。
- [[自监督学习SimCLR与CLIP]]：双塔 Transformer + Cross-Modal Contrastive Loss 实现图文对齐。

### 横向关联
- [[卷积神经网络CNN]] ↔ Transformer：CNN 的局部归纳偏置 vs Transformer 的全局注意力——前者少数据时泛化好，后者大数据时上限高。现代网络（如 CoAtNet、ConvNeXt）正在融合两者。
- Transformer与自注意力 ↔ Self-Attention：位置编码是 Transformer 的空间感知机制——正弦 PE（理论优雅，可外推）vs 可学习 PE（灵活但受训长度限制）vs 相对位置偏置（Swin, T5 使用）。

### 与 CNN 的归纳偏置对比总结

| 属性 | CNN (如 ResNet) | Transformer (如 ViT) |
| :--- | :--- | :--- |
| **局部性 (Locality)** | 硬编码：$3 \times 3$ 核只看邻居 | 无：每层都可看全局 |
| **平移等变性 (Translation Equivariance)** | 天然具备（权重共享） | 无（需位置编码补偿） |
| **权重共享** | 空间共享同一个卷积核 | 无空间共享（参数随序列长度增长） |
| **数据效率** | 高（强偏置在小数据上帮助大） | 低（需要大量数据学出偏置） |
| **计算复杂度** | $O(N \cdot k^2 \cdot C^2)$ | $O(N^2 \cdot d)$（二次于序列长度） |
| **感受野增长** | 线性（随层数） | 一层即全局 |

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清楚 Transformer 解决了 CNN 的什么核心问题。
- [ ] 2. 用直觉语言解释 Self-Attention 中的 Q、K、V 分别做什么。
- [ ] 3. 写出 Scaled Dot-Product Attention 的核心公式并解释每一项。
- [ ] 4. 解释为什么要除以 $\sqrt{d_k}$，不除会怎样。
- [ ] 5. 解释 Multi-Head Attention 的结构——每个 head 做什么、如何合并。
- [ ] 6. 写出正弦位置编码的公式，解释为什么用 sin/cos 而不是单一函数。
- [ ] 7. 画出 Transformer Encoder Block 的流程图（MHA → Add&Norm → FFN → Add&Norm）。
- [ ] 8. 手算 2 个 token 的完整 Self-Attention 过程。
- [ ] 9. 说出 Self-Attention 与 Cross-Attention 的核心区别。
- [ ] 10. 对比 CNN 和 Transformer 的归纳偏置（至少列出 3 点差异）。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | Self-Attention vs Cross-Attention |
| 2 | 公式运用 | 基础 | $\sqrt{d_k}$ 缩放的原因 |
| 3 | 条件判断 | 中等 | 位置编码的必要性 |
| 4 | 计算推导 | 中等 | 注意力得分矩阵维度推导 |
| 5 | 架构理解 | 较难 | Multi-Head 的维度拆分与拼接 |

### 题目与解析

#### 1. 关于 Self-Attention 的 Q、K、V，以下说法正确的是？
- A. Q、K、V 必须是三个完全不同的输入序列
- B. Self-Attention 中 Q、K、V 来自同一序列，是对输入的三个不同线性投影
- C. K 和 V 必须维度相同，Q 可以不同
- D. 自注意力中只有 Q 和 K 参与计算，V 是可选的

> [!question]- 答案解析
> - **答案**：B
> - **解析**：Self 意味着三个投影都来自 $\mathbf{X}$。Q、K 必须同维度做点积。对应误区 1。

#### 2. 在 Scaled Dot-Product Attention 中，当 $d_k = 256$ 时，如果不除以 $\sqrt{d_k}$，最可能发生什么？
- A. 计算速度变慢
- B. Softmax 输出趋近均匀分布
- C. Softmax 输出趋近 one-hot，梯度消失
- D. 注意力权重全部变为负数

> [!question]- 答案解析
> - **答案**：C
> - **解析**：点积方差 $\propto d_k$，大值使 Softmax 饱和 → 梯度消失。除以 $\sqrt{d_k}$ 将方差稳定在 1。

#### 3. 如果去掉 Transformer 的位置编码，对于序列"猫追狗" vs "狗追猫"的区分任务，模型表现会怎样？
- A. 表现不变，Self-Attention 会自己学出位置关系
- B. 完全无法区分，二者产生相同的池化后表示
- C. 收敛变慢但最终能区分
- D. 只有 Multi-Head 模式受影响

> [!question]- 答案解析
> - **答案**：B
> - **解析**：无 PE 时 Self-Attention 是置换等变的。经全局池化后两个序列输出完全相同。对应误区 2。

#### 4. 输入 $\mathbf{X} \in \mathbb{R}^{B \times N \times D}$ 经 Multi-Head Self-Attention（$h$ 头，$d_k=D/h$）后，输出维度是？
- A. $\mathbb{R}^{B \times N \times D}$
- B. $\mathbb{R}^{B \times N \times h \cdot D}$
- C. $\mathbb{R}^{B \times N \times d_k}$
- D. $\mathbb{R}^{B \times h \times N \times d_k}$

> [!question]- 答案解析
> - **答案**：A
> - **解析**：$h$ 个头各输出 $N \times d_k$，拼接后 $N \times (h \cdot d_k) = N \times D$，再经 $\mathbf{W}^O$ 投影。输入输出维度不变，可任意堆叠。

#### 5. FFN 在 Transformer Encoder Block 中的核心作用是？
- A. FFN 是多余的，Self-Attention 已足够
- B. 提供逐位置的非线性变换，补充 Attention 的"交流后思考"
- C. FFN 负责跨 token 信息融合，Attention 负责单 token 变换
- D. 降低模型参数量

> [!question]- 答案解析
> - **答案**：B
> - **解析**：Attention = "通信"（跨 token 交互），FFN = "思考"（逐位置非线性变换）。C 说反了。对应 Section 5.4。

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

- **归档目录**：`04-前沿架构探索/`（已在此）
- **建议双链**：
  - [[计算机视觉-ViT]] — Transformer 的 CV 分类直接应用
  - [[计算机视觉-SwinTransformer]] — 解决二次复杂度与多尺度问题
  - [[目标检测RCNN与YOLO]] — Transformer 用于目标检测
  - [[自监督学习SimCLR与CLIP]] — 基于 Transformer 的图文多模态
  - Transformer与自注意力 — 可拆分的细节卡（核心公式）
  - Transformer与自注意力 — 可拆分的细节卡（多头机制）
  - Transformer与自注意力 — 可拆分的细节卡（PE 变体）
  - [[卷积神经网络CNN]] — 归纳偏置对比的参照物
- **建议标签**：`#学习` `#计算机视觉` `#Transformer` `#自注意力` `#注意力机制` `#ViT`
- **拆分建议**：当前为 B 类概念主卡，覆盖完整。若后续挖深，可将 Self-Attention 公式推导、位置编码变体（RoPE / ALiBi）、Sparse Attention 优化单独成卡。

---

## 学完后可以完成

> 下列作业在 `requires` 中引用了本卡，由 Dataview 实时派生（非人工维护反向链接）：

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 🔗 知识图谱

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

