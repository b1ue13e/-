---
title: "Transformer架构（HW05）"
date: "2026-08-03"
created: "2026-08-03"
type: concept
course: "机器学习"
importance: "A"
tags: [学习, 机器学习, 深度学习]
upstream: [自注意力机制Self-Attention, 多层神经网络, 反向传播算法BP]
downstream: [BERT自监督表征, GPT, 位置编码]
status: learning
concept: ["Transformer", "Seq2Seq", "多头注意力"]
prerequisites: ["自注意力机制Self-Attention", "多层神经网络", "深度学习优化器"]
related: ["自注意力机制Self-Attention", "BERT自监督表征", "RNN", "CNN"]
flow: project
kind: concept
template: Obsidian单知识点深度学习模板
---

# Transformer架构（HW05）

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：Transformer 是 HW05 的唯一核心（Seq2Seq 机器翻译），也是 HW07 BERT 与几乎所有现代大模型的骨架。不理解它，HW07 只是"调包"，读 NLP 论文会卡在 encoder/decoder、causal mask 与位置编码上。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> [[自注意力机制Self-Attention]] 只能做**编码**（输入序列 → 一组向量），而 HW05 要解决**序列到序列（Seq2Seq）**：输出序列长度、顺序都与输入不同，且要**逐个 token 自回归生成**。因此必须引入完整架构：**Encoder 编码输入，Decoder 基于它自回归生成输出**，并把 self-attention 扩展为 encoder-decoder attention（跨序列交互）——这就是 Transformer（Vaswani et al., 2017）。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：HW05 官方任务（机器翻译）就是标准 Transformer；HW07 BERT 只用 Encoder，现代 LLM（GPT 系）只用 Decoder——它是 HW04→HW05→HW07 注意力主线的心脏。
- **实际应用场景**：机器翻译、文本摘要、对话生成、语音识别、代码生成等一切"序列 → 序列"任务。
- **高频题型/任务**：解释缩放点积注意力的 $\sqrt{d_k}$；多头 vs 单头；位置编码为什么必要；teacher forcing 与自回归解码的区别；greedy vs beam search。

---

## 3. 学它之前需要哪些前置知识？

1. **[[自注意力机制Self-Attention]]**：Q/K/V、注意力权重、矩阵并行化——Transformer 的核心积木，HW04 已训练。
2. **[[🎯 多层神经网络 (MLP)]]**：FFN 子层、残差连接、LayerNorm 的层结构直觉。
3. **[[🎯 深度学习优化器 (Adam, RMSprop, Momentum)]]**：HW05 标配 Adam + warmup 学习率调度。

---

## 4. 用直觉语言解释它

> «"Transformer"是一间分工明确的翻译工坊：Encoder 是一群"阅读理解员"，把原文读透，写成互相标注过重点的便签（上下文表示）；Decoder 是一个"口译员"，一边看便签、一边看自己已说的话，逐字翻译——说下一个字时，绝不能偷看还没说的字。»

- **直觉类比/几何图像**：多头注意力 = 同时雇 $h$ 组侧重不同的审读员（语法/语义/指代），各组写便签后拼成综合便签；位置编码 = 给每个词贴"入场序号"，否则便签乱成一团。并行让训练快（RNN 无法并行）、attention 权重可可视化，天然可解释。
- **一句话直觉本质**：**Encoder 用（多头）自注意力编码上下文；Decoder 用 causal mask 自注意力 + 跨序列注意力，逐个 token 自回归生成。**

---

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义
Transformer 是 **encoder-decoder 架构**，$N$ 层堆叠：Encoder 每层 = 多头自注意力 + FFN（各带残差与 LayerNorm）；Decoder 每层 = masked 自注意力 + 交叉注意力（对 Encoder 输出）+ FFN。输入 token 经嵌入层加**位置编码**。

### 2. 核心公式
缩放点积注意力：
$$\text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V$$
多头注意力：
$$\text{MultiHead}(Q,K,V)=\text{Concat}(\text{head}_1,\dots,\text{head}_h)W^O,\quad \text{head}_i=\text{Attention}(QW_i^Q,KW_i^K,VW_i^V)$$
正弦位置编码：
$$PE_{(pos,2i)}=\sin\!\left(\frac{pos}{10000^{2i/d_{model}}}\right),\quad PE_{(pos,2i+1)}=\cos\!\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$
残差 + LayerNorm：$\text{LayerNorm}(x+\text{Sublayer}(x))$，$\text{LayerNorm}(x)=\gamma\odot\frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}+\beta$。

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $Q,K,V$ | 查询 / 键 / 值矩阵 | $\mathbb{R}^{n\times d_k}$ 等 | 由输入线性投影 |
| $d_k$ | 键维度（$=d_{model}/h$） | 正整数 | 除 $\sqrt{d_k}$ 防 softmax 饱和 |
| $h$ | 注意力头数 | 如 8 | 每头关注不同子空间 |
| $PE$ | 位置编码 | $\mathbb{R}^{n\times d_{model}}$ | 加在输入嵌入上 |
| $W^Q,W^K,W^V,W^O$ | 投影矩阵 | 可学习参数 | 每头独立 |

### 4. 常见变体与适用条件
- **变体**：Encoder-only（BERT）、Decoder-only（GPT）、Encoder-Decoder（原始 Transformer）；相对位置编码（T5/ALiBi）、RoPE。
- **限制条件**：注意力 $O(n^2)$ 内存与计算；无内置位置归纳偏置，小数据上不如 CNN/RNN 易收敛。

---

## 6. 推导思路和思想来源

- **最初困难**：RNN 无法并行、长距离依赖衰减；CNN 需叠很多层才能看远。而把 self-attention 直接用于 Seq2Seq 时，Decoder 训练"一次看完整句"会作弊——看到未来的 ground-truth。
- **关键"转念"**：**causal mask**：把未来位置的注意力分数置 $-\infty$，softmax 后权重为 0；训练用 teacher forcing（输入真实前缀）并行算整句，推理才逐 token 自回归。
- **推导主线与动机**：① 从 HW04 self-attention 加缩放 $\sqrt{d_k}$ 稳定梯度；② 多头并行捕获不同关系子空间；③ 位置编码注入顺序；④ 残差 + LayerNorm + FFN 组成可堆叠子层；⑤ Encoder 输出作 Decoder 交叉注意力的 $K,V$。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）
- **题目**：$d_k=2$，$q=[1,0]$，$k_1=[1,1]$，$k_2=[0,1]$。比较缩放前后的 softmax 权重。
- **解题思路与关键步骤**：$q\cdot k_1=1,\ q\cdot k_2=0$。不缩放：softmax([1,0])$\approx[0.731,0.269]$；缩放 $[1/\sqrt2,0]=[0.707,0]$：softmax$\approx[0.669,0.331]$。
- **最终答案**：缩放让分数更温和、softmax 更接近均匀，避免大分数把 softmax 推向饱和。维度越大未缩放方差越大（$O(d_k)$），故必须除 $\sqrt{d_k}$。
- **🤔 追问**：若 $d_k=64$ 不缩放？——方差 $O(64)$，softmax 趋近 one-hot，梯度趋近 0，几乎学不动。

### 例子 2：中等例子（条件判断与多步推理）
- **题目**：翻译训练 loss 很低但生成全是重复词/<unk>，如何排查？
- **解题思路与完整解答**：① 先分 train/valid：只 train 低是过拟合；都低则问题在**解码与训练不一致**。② 检查 decoder causal mask（缺失时训练偷看未来，推理必然崩——最经典 bug）。③ 检查 <bos>/<eos> 与词表处理。④ greedy 重复是常见现象：上 beam search、length penalty、label smoothing。**关键推理**：训练是"给定前缀预测下一个"，推理是"自己生成前缀"（exposure bias），必须用解码策略弥合。

### 例子 3：实际应用例子（真实场景/代码）
- **实际价值与转化**：HW05 官方任务即英中翻译：先固定 tokenizer/词表，最小 Transformer 跑通基线，再看样例输出，最后加 warmup/label smoothing/beam search。代码骨架：
```python
class TransformerDecoderLayer(nn.Module):
    def __init__(self, d_model, nhead, dim_ff):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.cross_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.ffn = nn.Sequential(nn.Linear(d_model, dim_ff), nn.ReLU(), nn.Linear(dim_ff, d_model))
        self.norms = nn.ModuleList([nn.LayerNorm(d_model) for _ in range(3)])

    def forward(self, x, memory, tgt_mask):
        x = self.norms[0](x + self.self_attn(x, x, x, attn_mask=tgt_mask)[0])   # causal mask
        return self.norms[2](x + self.ffn(self.norms[1](x + self.cross_attn(x, memory, memory)[0])))
```

---

## 8. 常见误区和易混概念

### 误区 1：训练用 teacher forcing，推理也直接"一次算完整句"
- **错误直觉**：训练并行算整句，推理当然也能并行。
- **为什么错**：推理没有 ground-truth 前缀，只能先预测第 1 个 token 再当输入预测第 2 个——自回归串行；强行并行等于偷看未来。
- **正确理解**：训练"用真实前缀教"，推理"用自己的输出续写"——不一致（exposure bias）正是 beam search 与 scheduled sampling 存在的原因。

### 误区 2：位置编码是"可选项"
- **错误直觉**：attention 本身能学出顺序。
- **为什么错**：self-attention 对 token 集合**置换等变**——打乱顺序输出只是重排，模型分不清"我爱你"和"你爱我"。
- **正确理解**：PE 是**必需**的顺序来源（正弦 PE 还能外推到更长序列）。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| Transformer | 并行 + 长程依赖 + Seq2Seq | encoder-decoder、多头、PE、无循环 | 翻译、摘要、生成 |
| [[自注意力机制Self-Attention]] | 序列内部交互 | 单层机制，无完整编解码 | 编码器组件（HW04） |
| [[BERT自监督表征]] | 预训练表征 | 只用 Encoder，双向 | 理解任务（HW07） |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[自注意力机制Self-Attention]]：Q/K/V 与注意力权重的直接来源（HW04）。

### 下游延伸
- [[BERT自监督表征]]：BERT = Encoder 预训练，HW07 直接复用本笔记 encoder 部分。

### 横向关联
- [[自注意力机制Self-Attention]] ↔ 本知识点：前者是"机制"、后者是"架构"；HW04 编码器 → HW05 完整 Seq2Seq。

### 应用场景
- [[机器学习 - HW05：Transformer 阶梯作业]]：HW05 全部实验（baseline、warmup/label smoothing、beam search、失败样例）的理论底座。
- [[🧭 开源作业体系-机器学习]]：HW05 在注意力主线（HW04→HW05→HW07）中的位置与验收方式。

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
- [ ] 1. 用一句话说清楚 Transformer 解决什么问题。
- [ ] 2. 用直觉语言解释它（«翻译工坊»…）。
- [ ] 3. 写出缩放点积注意力公式。
- [ ] 4. 写出多头注意力与位置编码公式。
- [ ] 5. 解释公式里每个符号的含义（$Q,K,V,d_k,h,PE$）。
- [ ] 6. 讲出推导主线：并行 → PE → 多头 → 残差/LayerNorm → 交叉注意力。
- [ ] 7. 手算 $d_k=2$ 的缩放例子并解释 $\sqrt{d_k}$ 的作用。
- [ ] 8. 说出两个常见误区（teacher forcing 与推理不一致、PE 可省略）。
- [ ] 9. 说出它和 self-attention、BERT、RNN 的区别。
- [ ] 10. 说出 HW05 中的一个真实应用场景（机器翻译 pipeline）。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 缩放因子 $\sqrt{d_k}$ 的作用 |
| 2 | 公式运用 | 基础 | 手算两点注意力权重 |
| 3 | 条件判断 | 中等 | causal mask 与 teacher forcing 的关系 |
| 4 | 变式/综合 | 中等 | BERT（Encoder-only）与 GPT（Decoder-only）差异 |
| 5 | 开放/证明/建模 | 较难 | 为什么位置编码是必需的（置换等变论证） |

### 题目与解析

#### 1. 为什么 attention 分数要除以 $\sqrt{d_k}$？
> [!question]- 答案解析
> - **答案**：$QK^{\top}$ 每元素是 $d_k$ 个独立随机变量的和，方差随 $d_k$ 线性增长；不缩放时分数过大，softmax 进入饱和区，梯度趋近 0。
> - **解析**：设 $q,k$ 各分量均值 0 方差 1，则 $q\cdot k$ 方差为 $d_k$；除以 $\sqrt{d_k}$ 后方差为 1。
> - **Obsidian 标签建议**：`#自测题/基础`

#### 2. 给定 $q=[1,0]$、$k_1=[1,1]$、$k_2=[0,1]$（$d_k=2$），写出缩放后 softmax 的近似权重。
> [!question]- 答案解析
> - **答案**：分数 $[1/\sqrt2,\ 0]\approx[0.707,0]$，softmax $\approx[0.669,0.331]$。
> - **解析**：$e^{0.707}/(e^{0.707}+e^{0})\approx2.028/3.028\approx0.669$。

#### 3. 训练时 Decoder 忘了加 causal mask，会发生什么？推理时呢？
> [!question]- 答案解析
> - **答案**：训练时每位置都能看到未来 ground-truth，损失被"偷看"压低；推理时没有未来可看，生成质量骤降——train loss 低但生成差。
> - **解析**：causal mask 把未来位置分数置 $-\infty$，softmax 后权重为 0；这是 HW05 说明书"常见坑"点名的经典 bug。

#### 4. BERT 与 GPT 都是 Transformer，为什么一个做理解、一个做生成？
> [!question]- 答案解析
> - **答案**：BERT 只用 Encoder（双向自注意力）→ 适合看完整句做判断；GPT 只用 Decoder（causal mask 单向）→ 适合自回归生成。
> - **解析**：架构决定信息流方向：双向 → 表征（HW07）；单向 → 生成（HW05 解码侧同理）。

#### 5. 论证：为什么去掉位置编码后 Transformer 无法区分"我爱你"和"你爱我"？
> [!question]- 答案解析
> - **答案**：self-attention 对输入是置换等变的：$\text{Attn}(\pi(X))=\pi(\text{Attn}(X))$（softmax 与线性组合对行重排可交换）。没有 PE 时输出只依赖 token 集合而非顺序，两句话输出完全相同。
> - **解析**：$QK^{\top}$ 经置换只是行列重排，softmax 按行归一不变，$V$ 行重排——顺序信息必须由 PE 显式注入。

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

- **适合文件夹**：`02-Knowledge/🧠 学习系统/17-机器学习/`
- **关联已有笔记**：[[机器学习 - HW05：Transformer 阶梯作业]]、[[自注意力机制Self-Attention]]、[[BERT自监督表征]]、[[🧭 开源作业体系-机器学习]]
- **建议标签**：`#学习` `#机器学习` `#深度学习` `#注意力机制`
- **拆分建议**：若 HW05 深入解码策略，可拆"解码策略：greedy vs beam search"独立笔记。
