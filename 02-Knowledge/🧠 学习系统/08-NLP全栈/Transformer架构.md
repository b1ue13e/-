---
title: "Transformer架构"
date: "2026-08-02"
type: concept
course: "NLP全栈"
importance: "A"
tags: [学习, NLP全栈, Transformer, 自注意力, 位置编码, 深度学习]
upstream: [Seq2Seq与注意力机制, 循环神经网络RNN, 词向量与Word2Vec]
downstream: [BERT及其变体, GPT系列, HuggingFace生态系统, Self-Attention自注意力机制]
status: learning
concept: ["注意力机制", "序列建模", "深度学习架构"]
prerequisites: ["Seq2Seq与注意力机制", "softmax", "残差网络与LayerNorm"]
related: ["Seq2Seq与注意力机制", "Self-Attention自注意力机制", "BERT与GPT对比", "🎯 RoPE 旋转位置编码 (Rotary Position Embedding)"]
flow: project
kind: concept
template: Obsidian单知识点深度学习模板
created: 2026-08-02
---

# Transformer架构

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：Transformer（Vaswani et al., 2017, *Attention Is All You Need*）是 HW05 的全部内容——从零手写 Multi-Head Self-Attention 与 MinBERT；也是 BERT/GPT 及一切现代 LLM 的底座。HW05 要求实现并微调，不深挖到"每个矩阵的维度与 mask 位置"就无法通过。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> RNN 有两个结构性缺陷：①**无法并行**——第 $t$ 步必须等第 $t-1$ 步算完，GPU 利用率低，训练大模型慢到不可接受；②**长距离依赖弱**——即使 LSTM，1000 步外的信息也很难精确传递。
> CNN 可以并行（卷积核扫过整个序列），但感受野需要堆很多层才能覆盖长距离，且卷积是"局部"的。
> 因此需要一种**并行 + 全局**的序列建模方式。Transformer 的回答：完全去掉循环，用 **Self-Attention**（每个 token 直接与所有 token 交互，$O(1)$ 步到达任意位置、可整体并行），配以位置编码注入顺序信息，配以残差 + LayerNorm 保证深层可训练。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：HW05 手写它；[[BERT及其变体]] 是它的 Encoder 栈，[[GPT系列]] 是它的 Decoder 栈；[[HuggingFace生态系统]] 的 `transformers` 库就是围绕它的实现。不理解 Transformer，整个现代 NLP 都是黑盒。
- **实际应用场景**：全部主流 LLM（GPT、BERT、T5、LLaMA、Qwen）；机器翻译（Google 2018 起全线替换 RNN）；图像（ViT）、语音（Whisper）、代码（Codex）的 backbone。
- **高频题型/任务**：HW05 手写 attention + 位置编码 + 微调；面试必问"为什么除以 $\sqrt{d_k}$""Q/K/V 是什么""位置编码为什么必要""Pre-Norm vs Post-Norm""注意力复杂度 $O(N^2)$ 及优化（FlashAttention）"。

---

## 3. 学它之前需要哪些前置知识？

1. **[[Seq2Seq与注意力机制]]**：注意力打分-加权范式是 Self-Attention 的直接前身。
2. **[[Self-Attention自注意力机制]]**：缩放点积注意力公式与 mask 的完整推导（已有笔记，本卡复用其结论）。
3. **残差连接与 LayerNorm**：深层网络训练的稳定器（见 [[04-Transformer与预训练模型/LayerNorm|LayerNorm]]、[[04-Transformer与预训练模型/残差连接|残差连接]]）。

---

## 4. 用直觉语言解释它

> «"Transformer 像一个全员圆桌会议：每个词（token）都同时发言，也同时听所有人发言——先算'我跟谁最相关'（注意力权重），再按相关性吸收别人的信息（加权求和）。为了让发言不混乱，每个词发言前先戴上'身份标签'（位置编码）表明自己排第几。整场会议可以一步开完（并行），开完一轮再开下一轮（多层），每轮发言都做'总结归档'（残差+LayerNorm）防止信息跑偏。"»

- **直觉类比/几何图像**：Self-Attention = 全连接图上的消息传递：$N$ 个节点，每个节点聚合所有邻居的信息，权重由"查询-键"相似度决定。一层 = 一次全局消息传递；多层 = 多轮，形成越来越抽象的表示。
- **为什么很自然**：把"注意力"从 Seq2Seq 的"解码器看源句"推广为"序列内部互看"，是注意力思想最自然的延伸——既然注意力能对齐任意两个位置，何必还要循环结构？
- **一句话直觉本质**：**用"并行 + 全局 + 可微"的自注意力层堆叠，替代顺序循环：每层内 token 全连接交互，层间用残差与归一化稳定训练，位置编码补上顺序信息。**

---

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义
**Transformer 编码器层**：输入 $X \in \mathbb{R}^{N\times d_{\text{model}}}$，经过 ①多头自注意力（含残差 + LayerNorm）②前馈网络（含残差 + LayerNorm），输出同形状张量。解码器在每层中间多一个**交叉注意力**（对编码器输出做注意力），且自注意力带**因果 mask**。

### 2. 核心公式
**缩放点积注意力**（$d_k$ = 每个头的键维度）：
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right) V$$

**多头注意力**（$h$ 个头，拼接后投影）：
$$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1,\dots,\text{head}_h)W_O,\qquad \text{head}_i = \text{Attention}(XW_i^Q, XW_i^K, XW_i^V)$$

**位置编码（正弦）**：
$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d}}\right),\qquad PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d}}\right)$$

**残差 + LayerNorm（Pre-Norm 形式，现代默认）**：
$$x' = x + \text{Attn}(\text{LN}(x)), \qquad x'' = x' + \text{FFN}(\text{LN}(x'))$$

**前馈网络（FFN）**：$FFN(x) = \text{ReLU}(xW_1 + b_1)W_2 + b_2$（$d_{\text{ff}} = 4 d_{\text{model}}$）

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $N$ | 序列长度 | 整数 | 注意力矩阵是 $N\times N$ |
| $d_{\text{model}}$ | 模型宽度 | 512（base） | 嵌入/输出维度 |
| $d_k, d_v$ | 每头 Q/K、V 维度 | $d_{\text{model}}/h$ | base: 64 |
| $h$ | 头数 | 8（base） | 并行子空间数 |
| $X$ | 输入（词嵌入+位置） | $\mathbb{R}^{N\times d}$ | 编码器输入 |
| $W_i^Q,W_i^K,W_i^V,W_O$ | 投影矩阵 | 见备注 | 每头一组，可学习 |

### 4. 常见变体与适用条件
- **Encoder-only**（BERT）：双向自注意力，适合理解类任务（分类、NER）。
- **Decoder-only**（GPT）：因果掩码自注意力，适合生成（自回归 LM）。
- **Encoder-Decoder**（T5、原始 Transformer）：机器翻译等转换任务。
- **Pre-Norm vs Post-Norm**：现代模型用 Pre-Norm（LN 在残差之前）训练更稳（见 [[04-Transformer与预训练模型/PrePostNorm|PrePostNorm]]）。
- **限制条件**：$O(N^2)$ 注意力复杂度；位置编码外推问题（RoPE/ALiBi 缓解，见 [[🎯 RoPE 旋转位置编码 (Rotary Position Embedding)|RoPE]]）；训练对学习率 warmup 与初始化敏感。

---

## 6. 推导思路和思想来源

- **最初困难**：RNN 无法并行、长距离弱；CNN 局部感受野。
- **直接方法局限**：把 RNN 加深/加宽只是缓解；把 CNN 核做大代价 $O(k)$ 参数且仍非全局。
- **关键"转念"**：注意力已经证明能对齐任意两个位置（Seq2Seq），那**让序列内部两两直接交互**（Self-Attention），一层就覆盖全局，且所有位置的 Q/K/V 计算是独立矩阵乘——完全可并行。这就是"Attention Is All You Need"。
- **推导主线与动机**：① 去掉循环，用自注意力层；② 多头：把 $d$ 维空间切成 $h$ 个子空间，让不同头关注不同关系（语法 vs 指代）；③ 位置编码：注意力是置换不变的，必须注入顺序；④ 残差 + LayerNorm：深层堆叠（base 6 层 × 2 子层）需要梯度直通与归一化。
- **为什么自然得到此结论**：每个组件都回答一个具体失败模式：并行（无循环）、全局（自注意力）、顺序（位置编码）、可训练深度（残差+LN）、表达力（多头+FFN）。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）
- **题目**：$N=2$，$d_k=2$。$Q=(q_1;q_2)$，$K=(k_1;k_2)$，$V=(v_1;v_2)$，其中 $q_1=k_1=(1,0)$，$q_2=k_2=(0,1)$，$v_1=(1,0)$，$v_2=(0,1)$。计算注意力输出。
- **解题思路与关键步骤**：$QK^\top = \begin{pmatrix}1&0\\0&1\end{pmatrix}$（$q_1\cdot k_1=1, q_1\cdot k_2=0$ 等）。除以 $\sqrt{2}$ 得 $\begin{pmatrix}0.707&0\\0&0.707\end{pmatrix}$。softmax 每行：行 1 为 $\frac{e^{0.707}}{e^{0.707}+1}\approx 0.669$ 与 $0.331$；行 2 对称。
- **最终答案**：输出行 1 $= 0.669(1,0)+0.331(0,1) = (0.669, 0.331)$；行 2 $= (0.331, 0.669)$。
- **易错点**：忘记除以 $\sqrt{d_k}$（本例 $d_k=2$，$\sqrt{2}\approx1.414$）；softmax 逐行归一化。
- **🤔 追问**：如果 $q_1=k_1=(10,0)$（模长大 10 倍），权重会怎样？—— 得分 $10^2/1.414 \approx 70.7$，softmax 后几乎 one-hot（饱和），梯度趋零——这正是除以 $\sqrt{d_k}$ 的原因。

### 例子 2：中等例子（条件判断与多步推理）
- **题目**：为什么解码器需要因果 mask？编码器为什么不需要？
- **解题思路与完整解答**：解码器做自回归生成，第 $t$ 个位置的输出只能依赖 $<t$ 的 token，否则训练时"偷看未来"、推理时无法复现（推理根本没有未来）。因果 mask 把 $QK^\top$ 的上三角置为 $-\infty$，softmax 后权重为 0。编码器做理解任务（如分类），每个 token 应看到全句上下文（双向），所以不 mask。HW05 的 MinBERT（编码器）不加因果 mask；若手写 GPT 需加。
- **易错点**：在编码器里也加因果 mask（会退化成单向，丢双向信息）；或 mask 实现时把对角线也遮掉（应保留当前位置）。

### 例子 3：实际应用例子（真实场景/代码）
- **实际价值与转化**：HW05 从零实现后与 `transformers` 库对照验证（输出一致断言）。代码形态：
```python
import torch, torch.nn as nn, math

class MultiHeadSelfAttention(nn.Module):
    def __init__(self, d_model=768, h=12):
        super().__init__()
        self.h, self.dk = h, d_model // h
        self.Wq = nn.Linear(d_model, d_model); self.Wk = nn.Linear(d_model, d_model)
        self.Wv = nn.Linear(d_model, d_model); self.Wo = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        B, N, _ = x.shape
        Q = self.Wq(x).view(B, N, self.h, self.dk).transpose(1, 2)   # (B, h, N, dk)
        K = self.Wk(x).view(B, N, self.h, self.dk).transpose(1, 2)
        V = self.Wv(x).view(B, N, self.h, self.dk).transpose(1, 2)
        scores = Q @ K.transpose(-2, -1) / math.sqrt(self.dk)        # (B, h, N, N)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        attn = torch.softmax(scores, dim=-1)
        out = (attn @ V).transpose(1, 2).reshape(B, N, -1)           # 拼接
        return self.Wo(out), attn
```

---

## 8. 常见误区和易混概念

### 误区 1：以为"除以 $\sqrt{d_k}$ 只是数值稳定的小技巧"
- **错误直觉**：不除也不会错，只是防止溢出。
- **为什么错**：根本原因是**方差**：$q,k$ 分量方差为 1 时，点积方差 $=d_k$，$d_k$ 大则得分方差大，softmax 进入饱和区、梯度消失（见 [[Self-Attention自注意力机制]] 的推导）。除 $\sqrt{d_k}$ 把方差归一化回 1。
- **正确理解**：它是**梯度健康性**的必要设计，不是可选技巧。

### 误区 2：以为"位置编码可以不要，因为注意力能学出顺序"
- **错误直觉**：注意力权重本身就是顺序信息。
- **为什么错**：Self-Attention 对输入**置换不变**——把句子打乱顺序，输出只是对应行交换；没有位置信息，模型根本无法区分 "A 打 B" 和 "B 打 A"。
- **正确理解**：位置编码（正弦/可学习/RoPE/ALiBi）是 Transformer 的必备组件，负责注入顺序（见 [[🎯 RoPE 旋转位置编码 (Rotary Position Embedding)|RoPE]]）。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| Transformer（本概念） | 并行全局序列建模 | 自注意力 + 位置编码 + 残差 LN | 现代 NLP 全部 |
| RNN/LSTM | 顺序记忆 | 串行、长距离弱 | 短序列、在线流式 |
| CNN | 局部特征 | 并行但感受野局部 | 文本分类（TextCNN） |
| 纯 Seq2Seq 注意力 | 跨序列对齐 | 需编码器-解码器结构 | 翻译（HW04） |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[Seq2Seq与注意力机制]]：注意力的来源与打分-加权范式。
- [[Self-Attention自注意力机制]]：本卡的核心子模块完整推导（已有笔记）。

### 下游延伸
- [[BERT及其变体]]：Encoder-only 的预训练实例。
- [[GPT系列]]：Decoder-only 的自回归实例。
- [[HuggingFace生态系统]]：工程实现与微调工具。

### 横向关联
- [[BERT与GPT对比]] ↔ 本知识点：同一架构的两种配置（双向 vs 因果）。
- [[🎯 RoPE 旋转位置编码 (Rotary Position Embedding)|RoPE 旋转位置编码]] ↔ 本知识点：位置编码的现代替代（相对位置、外推）。
- [[04-Transformer与预训练模型/QKV\|QKV]]、[[04-Transformer与预训练模型/多头注意力\|多头注意力]]、[[04-Transformer与预训练模型/LayerNorm\|LayerNorm]]、[[04-Transformer与预训练模型/残差连接\|残差连接]]：组件原子卡。

### 应用场景
- [[🧭 开源作业体系-NLP全栈|开源作业体系]]：HW05 从零手撕 + 微调验收。
- [[NLP全栈 - HW05：Transformer 与 MinBERT 从零手撕阶梯作业|HW05 阶梯作业]]：4 档 Rubric 的实操页。

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
- [ ] 1. 用一句话说清楚它解决什么问题。
- [ ] 2. 用直觉语言解释它（«"全员圆桌会议…"»）。
- [ ] 3. 写出缩放点积注意力与多头注意力的公式。
- [ ] 4. 写出正弦位置编码公式。
- [ ] 5. 解释 $N$、$d_{\text{model}}$、$d_k$、$h$、$X$ 的含义。
- [ ] 6. 讲出"去掉循环、自注意力化"的推导主线。
- [ ] 7. 手算 2 token 的注意力输出。
- [ ] 8. 说出两个常见误区。
- [ ] 9. 说出它与 BERT、GPT、RoPE 的关系。
- [ ] 10. 说出 HW05 的验收方式（自注意力断言 + SST-2 微调）。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | Transformer 各组件职责 |
| 2 | 公式运用 | 基础 | 缩放点积注意力手算 |
| 3 | 条件判断 | 中等 | 因果 mask 的使用位置 |
| 4 | 变式/综合 | 中等 | 多头 vs 单头的意义与复杂度 |
| 5 | 开放/证明/建模 | 较难 | 为什么 Self-Attention 需要位置编码（置换不变性） |

### 题目与解析

#### 1. Transformer 编码器层的四个组成部分及其职责是什么？
> [!question]- 答案解析
> - **答案**：① 多头自注意力（全局交互、并行）；② 残差连接（梯度直通）；③ LayerNorm（稳定训练）；④ FFN（逐位置非线性变换、增加容量）。
> - **解析**：残差与 LN 成对包裹每个子层（Pre-Norm：$x+\text{SubLayer}(\text{LN}(x))$）；FFN 的 $d_{\text{ff}}=4d_{\text{model}}$ 提供每 token 独立的大容量变换。
> - **易错原因**：漏掉残差或 LN 之一，或把 FFN 误当成跨 token 操作（它是逐位置的）。
> - **Obsidian 标签建议**：`#自测题/基础`

#### 2. $N=2$，$d_k=1$：$q_1=k_1=v_1=1$，$q_2=k_2=v_2=2$，求注意力输出。
> [!question]- 答案解析
> - **答案**：$QK^\top = \begin{pmatrix}1&2\\2&4\end{pmatrix}$，除以 $\sqrt{1}=1$ 不变。softmax 行 1：$e^1/(e^1+e^2)\approx 0.269$、$0.731$；行 2：$e^2/(e^2+e^4)\approx 0.119$、$0.881$。输出 $= (0.269\cdot1+0.731\cdot2,\ 0.119\cdot1+0.881\cdot2) = (1.731, 1.881)$。
> - **解析**：行 2 自权重更高（$q_2\cdot k_2=4$ 最大），输出偏向 $v_2=2$。
> - **易错原因**：softmax 对整矩阵而非逐行归一化；$d_k=1$ 时 $\sqrt{d_k}=1$ 别忘了写。
> - **Obsidian 标签建议**：`#自测题/基础`

#### 3. 何时需要因果 mask？举例说明。
> [!question]- 答案解析
> - **答案**：自回归生成类模型（GPT 类解码器、语言模型）需要：第 $t$ 位置不能看到 $>t$ 的 token。理解类模型（BERT 编码器）不需要。
> - **解析**：实现上把 $QK^\top$ 上三角置 $-\infty$（含 $j>i$ 的元素），softmax 后权重为 0；HW05 的 MinBERT 不加，手写 GPT 要加。
> - **易错原因**：把对角线也遮掉（当前位置必须可见）；或在编码器误加。
> - **Obsidian 标签建议**：`#自测题/中等`

#### 4. 多头注意力的"头"到底学到了什么？头数增加复杂度如何变化？
> [!question]- 答案解析
> - **答案**：不同头关注不同的关系模式（如语法依赖、指代、位置近邻），且每个头在 $d_k = d/h$ 的子空间工作，降低单头表达负担。复杂度：参数随 $h$ 线性增加（总 $4d^2$ 不变——三个投影 + 输出投影，与 $h$ 无关），计算复杂度不变（$O(N^2 d)$）；增加的是并行子空间的数量。
> - **解析**：$W_i^Q \in \mathbb{R}^{d\times d_k}$，$h$ 个头合计 $d\times d$，与单头参数相同；多头是"同参数预算下的多视角分解"。
> - **易错原因**：以为多头使参数量翻 $h$ 倍——总投影维度不变。
> - **Obsidian 标签建议**：`#自测题/中等`

#### 5. 证明 Self-Attention 是置换等变的，并说明为什么因此必须加位置编码。
> [!question]- 答案解析
> - **答案**：对任意置换 $\pi$，令输入行交换为 $X_\pi = P_\pi X$（$P_\pi$ 为置换矩阵），则 $Q_\pi K_\pi^\top = P_\pi Q K^\top P_\pi^\top$，softmax 逐行作用于置换后的矩阵得 $P_\pi A P_\pi^\top$，输出 $= P_\pi A P_\pi^\top V_\pi = P_\pi (A V)$——即输出只是输入的对应行置换，**交互关系完全不变**。因此模型无法区分不同词序，必须用位置编码注入顺序信息。
> - **解析**：这也是为什么"把句子乱序后注意力权重只是跟着换行"——没有位置编码，Transformer 看到的"猫咬狗"和"狗咬猫"是同一个东西。
> - **易错原因**：只背结论"需要位置编码"，讲不出置换等变性的证明。
> - **Obsidian 标签建议**：`#自测题/较难`

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

- **适合文件夹**：`02-Knowledge/🧠 学习系统/08-NLP全栈/`
- **关联已有笔记**：[[🧭 开源作业体系-NLP全栈]]、[[Self-Attention自注意力机制]]、[[NLP全栈 - HW05：Transformer 与 MinBERT 从零手撕阶梯作业|HW05 阶梯作业]]、[[04-Transformer与预训练模型/QKV|QKV]]、[[04-Transformer与预训练模型/多头注意力|多头注意力]]、[[04-Transformer与预训练模型/LayerNorm|LayerNorm]]、[[04-Transformer与预训练模型/残差连接|残差连接]]、[[04-Transformer与预训练模型/正弦位置编码|正弦位置编码]]、[[04-Transformer与预训练模型/FFN|FFN]]
- **建议标签**：`#学习` `#NLP全栈` `#Transformer` `#概念`
- **拆分建议**：母卡保留；"手写 Multi-Head Attention 的维度调试"可拆错题笔记，"HW05 实现对照 transformers 库"可拆题型笔记。
