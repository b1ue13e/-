---
title: "Seq2Seq与注意力机制"
date: "2026-08-02"
type: concept
course: "NLP全栈"
importance: "A"
tags: [学习, NLP全栈, Seq2Seq, 注意力机制, 机器翻译, NMT]
upstream: [循环神经网络RNN, 词向量与Word2Vec]
downstream: [Transformer架构, Self-Attention自注意力机制, 检索增强生成RAG]
status: learning
concept: ["序列到序列", "注意力机制", "机器翻译"]
prerequisites: ["RNN/LSTM", "softmax与交叉熵", "Beam Search"]
related: ["循环神经网络RNN", "Transformer架构", "Self-Attention自注意力机制", "数据集与评测指标"]
flow: project
kind: concept
template: Obsidian单知识点深度学习模板
created: 2026-08-02
---

# Seq2Seq与注意力机制

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：Seq2Seq + 注意力是 CS224N HW04（NMT）的全部内容，也是注意力机制的诞生地（Bahdanau 2014）。HW04 要求手写编码器-解码器、Bahdanau 注意力与 beam search；不理解注意力如何解决"信息瓶颈"，就无法理解 Transformer 的 Self-Attention 从何而来。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 很多 NLP 任务是"序列 → 序列"：翻译（中文句 → 英文句）、摘要（长文 → 短文）、对话（问 → 答）。输出长度与输入长度无关，且输出是**逐个词生成**的。RNN 语言模型只能生成"延续"，不能"换一种语言重新表达"。
> 直接做法是"编码器-解码器"：编码器把源句压缩成一个向量（最后一个隐藏状态），解码器从这个向量开始逐词生成。但这里有个致命缺陷——**信息瓶颈**：无论源句多长，全部信息都要挤进一个固定维度的向量 $h_T$ 里；句子越长，开头的信息被"稀释"得越厉害。引入**注意力机制**后，解码器每一步都能"回头看"源句的所有位置，按需取用——瓶颈被打破。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：注意力是 HW04 的核心考点，更是 Transformer 一切的基础（[[Self-Attention自注意力机制]] 就是"注意力内部化"）。学完本卡，Transformer 的 Q/K/V 只是"注意力的一般化"。
- **实际应用场景**：机器翻译（Google 早期 NMT）、文本摘要、语音识别（CTC+attention）、代码生成、图像描述（show-attend-tell）。
- **高频题型/任务**：HW04 手写 Bahdanau/Luong 注意力并 BLEU 验收；面试常问"attention 为什么缓解长句退化""Bahdanau 与 Luong 的区别""teacher forcing 是什么、为什么训练和推理不一致（exposure bias）"。

---

## 3. 学它之前需要哪些前置知识？

1. **[[循环神经网络RNN]]**：编码器与解码器都是 LSTM；隐藏状态、BPTT 是基础。
2. **Beam Search 解码**：生成时不再是贪心取最大概率词，而是维护 $k$ 个候选（见 [[03-深度学习NLP基础/Beam Search原理|Beam Search原理]]）。
3. **Softmax 与交叉熵**：每步生成的词分布与序列损失（teacher forcing 下的逐词交叉熵）。

---

## 4. 用直觉语言解释它

> «"没有注意力的 Seq2Seq 就像一个只能瞄一眼全文就闭卷答题的学生——记得住梗概，但引经据典时总丢三落四。注意力机制让他变成开卷考试：翻译到每个词时，都可以回头翻看源句的任意位置，给相关词更高的'注意力权重'。比如翻译 'the cat sat on the mat' 时，输出 'mat' 时他会重点看源句的 'mat' 而不是 'cat'。"»

- **直觉类比/几何图像**：注意力 = "软性查表"：解码器每步发出一个查询（query，即当前解码状态），与源句所有位置的键（key，编码器状态）算相似度，得到权重，再对源句的值（value，编码器状态）加权求和——这就是"上下文向量"。它让每一步生成都有"专属的源句摘要"。
- **为什么很自然**：人翻译时本来就是逐词对齐的（word alignment 是统计 MT 的核心）；注意力把"对齐"变成了可微分的软对齐，无需显式标注。
- **一句话直觉本质**：**解码器每步动态地从源句所有位置加权取信息（软对齐），打破固定向量瓶颈，让长句翻译不再退化。**

---

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义
**Seq2Seq**：编码器将源序列 $x_1,\dots,x_T$ 编码为状态序列 $\{h_1,\dots,h_T\}$；解码器在每一步 $t$ 用注意力计算上下文向量 $c_t$，与自身状态 $s_t$ 融合后预测目标词 $y_t$。

**Bahdanau（加性）注意力**：
$$e_{tj} = v_a^\top \tanh(W_a s_{t-1} + U_a h_j), \qquad \alpha_{tj} = \frac{\exp(e_{tj})}{\sum_{j'}\exp(e_{tj'})}, \qquad c_t = \sum_j \alpha_{tj} h_j$$

**Luong（乘性/点积）注意力**（三种打分：dot / general / concat）：
$$e_{tj} = s_t^\top h_j \quad(\text{dot}), \qquad e_{tj} = s_t^\top W_a h_j \quad(\text{general}), \qquad e_{tj} = v_a^\top \tanh(W_a [s_t; h_j])$$

### 2. 核心公式
**解码器状态更新与输出**（Luong 局部/全局注意力版）：
$$s_t = \text{LSTM}(s_{t-1}, [\text{emb}(y_{t-1}); c_{t-1}]), \qquad \tilde{s}_t = \tanh(W_c [c_t; s_t]), \qquad P(y_t \mid y_{<t}, x) = \text{softmax}(W_s \tilde{s}_t)$$

**训练目标（teacher forcing）**：给定参考译文 $y^*$，
$$J = -\sum_{t=1}^{T'} \log P(y^*_t \mid y^*_{<t}, x)$$

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $h_j$ | 编码器第 $j$ 个位置的隐藏状态 | $\mathbb{R}^{d_h}$ | 注意力"键/值" |
| $s_t$ | 解码器第 $t$ 步状态 | $\mathbb{R}^{d_h}$ | 注意力"查询"来源 |
| $e_{tj}$ | 第 $t$ 步对源位置 $j$ 的注意力得分 | $\mathbb{R}$ | 未归一化 |
| $\alpha_{tj}$ | 注意力权重 | $[0,1]$，$\sum_j\alpha_{tj}=1$ | "软对齐" |
| $c_t$ | 上下文向量 | $\mathbb{R}^{d_h}$ | 加权源摘要 |
| $T, T'$ | 源/目标序列长度 | 整数 | 可不等长 |

### 4. 常见变体与适用条件
- **Bahdanau vs Luong**：Bahdanau 用 $\tanh$ 加性打分（查询用 $s_{t-1}$），适合长序列、更稳；Luong 用点积类打分（查询用 $s_t$），计算快、可并行，配合"局部注意力"（只对窗口内位置打分）降复杂度。HW04 通常两者都给，选一实现。
- **Teacher forcing vs 自由生成**：训练时把真实目标词喂给解码器（teacher forcing，收敛快）；推理时喂自己生成的词。中间方案 scheduled sampling 缓解 exposure bias。
- **限制条件**：注意力是 $O(T\cdot T')$ 的（源长×目标长），长文档（>5000 token）需稀疏/局部注意力；这是后续 Longformer、稀疏注意力的动机。

---

## 6. 推导思路和思想来源

- **最初困难**：Sutskever et al. 2014 的纯 Seq2Seq 把源句压进一个向量，长句（>30 词）翻译质量骤降。
- **直接方法局限**：把编码器改成"输出所有位置的状态"还不够——解码器不知道每一步该看哪里；若简单平均所有位置（mean pooling），又回到无差别摘要。
- **关键"转念"**（Bahdanau et al., 2014）：把"对齐"建模为**可学习的软权重**：让解码器每一步用当前状态去"检索"源句各位置（相似度打分 → softmax → 加权求和）。对齐不再是统计 MT 里的离散隐变量，而是端到端可微的一部分。
- **推导主线与动机**：① 编码器保留全部状态；② 定义打分函数 $e_{tj}=f(s_{t-1}, h_j)$；③ softmax 归一化得权重；④ 加权求和得 $c_t$；⑤ 把 $c_t$ 拼进解码器输入与输出层——整个模型仍是一个可微序列损失，BP 即可训练。
- **为什么自然得到此结论**：因为"生成每一步时需要的源信息不同"，而"按相关性加权"是信息检索/记忆网络的通用机制（soft attention 与 memory network 同年提出，思想同源）。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）
- **题目**：源句 3 个词，编码器状态 $h_1=(1,0)$，$h_2=(0,1)$，$h_3=(1,1)$。解码器当前状态 $s=(0.5,0.5)$。用 Luong dot 注意力算权重与上下文向量。
- **解题思路与关键步骤**：得分 $e_j = s^\top h_j$：$e_1 = 0.5$，$e_2 = 0.5$，$e_3 = 1.0$。softmax：$e^{0.5}+e^{0.5}+e^{1.0} = 2e^{0.5}+e$。权重：$\alpha_1=\alpha_2=\frac{e^{0.5}}{2e^{0.5}+e}\approx 0.232$，$\alpha_3=\frac{e}{2e^{0.5}+e}\approx 0.536$。
- **最终答案**：$c = 0.232(1,0)+0.232(0,1)+0.536(1,1) = (0.768, 0.768)$。
- **易错点**：softmax 用错底数（必须 $e$）；忘记权重和为 1 的校验。
- **🤔 追问**：若换成 Bahdanau（加性）打分，权重会一样吗？—— 通常不同：加性打分引入非线性 $\tanh$ 与可学习矩阵，表达能力更强，但手算需给定 $W_a, U_a, v_a$。

### 例子 2：中等例子（条件判断与多步推理）
- **题目**：为什么 teacher forcing 训练出的模型在推理时（自由生成）会累积错误？如何缓解？
- **解题思路与完整解答**：训练时输入是真实词 $y^*_{t-1}$，推理时输入是模型自己的输出 $\hat{y}_{t-1}$——两者分布不一致（exposure bias）。一旦推理早期出错，错误会滚雪球。缓解：① scheduled sampling（训练时按概率用模型输出）；② beam search（保留多候选，见 [[03-深度学习NLP基础/Beam Search原理|Beam Search]]）；③ 强化学习/序列级目标（直接优化 BLEU）；④ 训练时少量注入噪声（word dropout）。HW04 中 beam width 通常取 5-10，太大收益递减且慢。
- **易错点**：以为 teacher forcing 是推理策略——它是**训练**策略；推理必须用自回归生成。

### 例子 3：实际应用例子（真实场景/代码）
- **实际价值与转化**：HW04 实现"英文 → 德语"翻译：LSTM 编码器 + Bahdanau 注意力 + beam search，验收 BLEU 达到官方 baseline。代码形态：
```python
import torch, torch.nn as nn, torch.nn.functional as F

class BahdanauAttention(nn.Module):
    def __init__(self, d_hid):
        super().__init__()
        self.Wa = nn.Linear(d_hid, d_hid)   # 作用在 decoder 状态 s
        self.Ua = nn.Linear(d_hid, d_hid)   # 作用在 encoder 状态 h
        self.va = nn.Linear(d_hid, 1)

    def forward(self, s, enc_states, mask):
        # s: (B, d), enc_states: (B, T, d), mask: (B, T)
        e = self.va(torch.tanh(self.Wa(s).unsqueeze(1) + self.Ua(enc_states))).squeeze(-1)
        e = e.masked_fill(mask == 0, -1e9)      # padding mask
        alpha = F.softmax(e, dim=-1)             # (B, T)
        c = (alpha.unsqueeze(-1) * enc_states).sum(dim=1)   # (B, d)
        return c, alpha

# 解码一步：s_new = LSTM([emb(y_{t-1}); c], s_old)；输出 P(y_t) = softmax(W_s tanh(Wc[c;s_new]))
```

---

## 8. 常见误区和易混概念

### 误区 1：以为"注意力权重就是可解释的对齐"
- **错误直觉**：注意力矩阵一定对应语言学意义上的词对齐，可以直接当对齐用。
- **为什么错**：注意力是"任务驱动"的软权重，可能学到反直觉模式（如对 <EOS> 或高频词高权重）；论文证明其可解释性只是"有时"成立（"attention is not explanation"）。
- **正确理解**：注意力是模型内部的软检索机制，可解释性需谨慎，别当硬对齐标注用。

### 误区 2：以为"Self-Attention 和这里的注意力是两回事"
- **错误直觉**：Seq2Seq 注意力是对"源句"的注意力，Self-Attention 完全不同。
- **为什么错**：机制完全一样（Q/K/V 打分加权），只是 Self-Attention 的 Q、K、V 都来自**同一序列**（编码器内部互看）；Seq2Seq 注意力是"跨序列"（解码器看编码器，即 cross-attention）。
- **正确理解**：[[Transformer架构]] 的 cross-attention 就是本卡注意力的直接继承。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| Seq2Seq 注意力（本概念） | 解码器看源句 | 跨序列、query=解码状态 | NMT、摘要（HW04） |
| Self-Attention | 序列内部互看 | 同序列、Q=K=V 同源 | Transformer 编码器 |
| 硬注意力 | 只选一个位置 | 不可微（需采样） | 图像 caption 早期 |
| 局部注意力 | 窗口内软对齐 | 复杂度 $O(2D\cdot T')$ | 长序列 Luong |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[循环神经网络RNN]]：编码器/解码器的骨架。
- [[03-深度学习NLP基础/Beam Search原理|Beam Search原理]]：解码策略，HW04 验收必备。

### 下游延伸
- [[Transformer架构]]：注意力取代循环，Q/K/V 一般化。
- [[Self-Attention自注意力机制]]：本卡注意力的"内部化"版本。
- [[检索增强生成RAG]]：注意力是"软检索"，RAG 是"硬检索 + 生成"。

### 横向关联
- [[03-深度学习NLP基础/Bahdanau\|Bahdanau]] ↔ [[03-深度学习NLP基础/Luong\|Luong]]：两种打分方式的原子卡。
- [[03-深度学习NLP基础/Seq2Seq Encoder\|Seq2Seq Encoder]]、[[03-深度学习NLP基础/Seq2Seq Decoder\|Seq2Seq Decoder]]、[[03-深度学习NLP基础/上下文向量\|上下文向量]] ↔ 本知识点：组件原子卡。

### 应用场景
- [[🧭 开源作业体系-NLP全栈|开源作业体系]]：HW04 的模型与验收入口。
- [[数据集与评测指标]]：BLEU 是 HW04 的验收指标。

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
- [ ] 1. 用一句话说清楚它解决什么问题。
- [ ] 2. 用直觉语言解释它（«"开卷考试的学生…"»）。
- [ ] 3. 写出 Bahdanau 注意力的三个公式。
- [ ] 4. 写出 teacher forcing 的训练损失。
- [ ] 5. 解释 $h_j$、$s_t$、$\alpha_{tj}$、$c_t$ 的含义。
- [ ] 6. 讲出"信息瓶颈 → 软对齐"的推导主线。
- [ ] 7. 手算 3 位置 dot 注意力的权重与上下文向量。
- [ ] 8. 说出两个常见误区。
- [ ] 9. 说出它与 Self-Attention、Transformer、RAG 的关系。
- [ ] 10. 说出 HW04 的验收方式（BLEU + beam search）。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 注意力解决什么问题 |
| 2 | 公式运用 | 基础 | dot 注意力权重手算 |
| 3 | 条件判断 | 中等 | Bahdanau vs Luong 选择 |
| 4 | 变式/综合 | 中等 | teacher forcing 与 exposure bias |
| 5 | 开放/证明/建模 | 较难 | 注意力复杂度与长文档对策 |

### 题目与解析

#### 1. 注意力机制解决 Seq2Seq 的什么问题？为什么？
> [!question]- 答案解析
> - **答案**：解决信息瓶颈——纯 Seq2Seq 把源句压缩进一个固定向量 $h_T$，长句信息丢失；注意力让解码器每步加权读取源句全部位置，获得动态上下文向量 $c_t$。
> - **解析**：本质是把"静态摘要"换成"逐词软对齐摘要"，翻译质量在长句上显著提升（Bahdanau 2014 实验：>30 词句子 BLEU 翻倍）。
> - **易错原因**：答成"解决梯度消失"——那是 LSTM 的动机；注意力主要解决信息压缩损失（虽也缩短了信息路径）。
> - **Obsidian 标签建议**：`#自测题/基础`

#### 2. 源句 2 词，$h_1=(2,0)$，$h_2=(0,2)$，解码状态 $s=(1,1)$，求 Luong dot 注意力的 $\alpha$ 与 $c$。
> [!question]- 答案解析
> - **答案**：$e_1 = 2$，$e_2 = 2$，$\alpha_1=\alpha_2=0.5$，$c = 0.5(2,0)+0.5(0,2) = (1,1)$。
> - **解析**：两位置得分相同 → 均匀权重；$c=s$ 是巧合（本例对称）。
> - **易错原因**：忘记 softmax 归一化直接用得分加权。
> - **Obsidian 标签建议**：`#自测题/基础`

#### 3. 什么场景下选 Bahdanau 而非 Luong dot 注意力？
> [!question]- 答案解析
> - **答案**：源句较长、需要更灵活的非线性对齐时用 Bahdanau（加性打分容量大、更稳）；追求计算效率、可并行、短中序列时用 Luong dot/general。
> - **解析**：Bahdanau 每步要算 $\tanh$ 加性组合（含 $W_a, U_a$ 两个矩阵），稍慢；Luong 点积类可复用矩阵乘法加速。实践中 HW04 两者皆可，general 常作折中。
> - **易错原因**：以为 Bahdanau 一定更好——小数据集上 Luong 也常够用且更快。
> - **Obsidian 标签建议**：`#自测题/中等`

#### 4. 什么是 teacher forcing？训练与推理不一致会带来什么问题？如何缓解？
> [!question]- 答案解析
> - **答案**：训练时用真实目标词作解码器输入；推理时用模型自生成的词。不一致导致 exposure bias——训练分布（真实前缀）与推理分布（模型前缀）不同，错误会累积。
> - **解析**：缓解：scheduled sampling、beam search、序列级强化学习。HW04 里 beam search 是最实用的缓解手段。
> - **易错原因**：把 teacher forcing 当推理策略。
> - **Obsidian 标签建议**：`#自测题/中等`

#### 5. 注意力计算的复杂度是多少？处理 100k token 的文档翻译时有什么对策？
> [!question]- 答案解析
> - **答案**：$O(T\cdot T')$（源长×目标长）+ 存储注意力矩阵 $O(T\cdot T')$。$T=10^5$ 时注意力矩阵就是 $10^{10}$ 元素，不可行。
> - **解析**：对策：① 局部注意力/窗口注意力（Luong local attention，只对 $2D$ 窗口打分）；② 稀疏注意力（Longformer 的滑动窗口 + 全局 token）；③ 先检索再生成（[[检索增强生成RAG]]：只对检索到的段落做注意力）；④ 分块/层次编码。这些都是 HW04 之后的进阶话题。
> - **易错原因**：以为注意力复杂度只随目标长度线性——它同时依赖源长度。
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
- **关联已有笔记**：[[🧭 开源作业体系-NLP全栈]]、[[03-深度学习NLP基础/Seq2Seq Encoder|Seq2Seq Encoder]]、[[03-深度学习NLP基础/Seq2Seq Decoder|Seq2Seq Decoder]]、[[03-深度学习NLP基础/Bahdanau|Bahdanau]]、[[03-深度学习NLP基础/Luong|Luong]]、[[03-深度学习NLP基础/上下文向量|上下文向量]]、[[03-深度学习NLP基础/Beam Search原理|Beam Search]]、[[03-深度学习NLP基础/Attention计算|Attention计算]]
- **建议标签**：`#学习` `#NLP全栈` `#Seq2Seq` `#注意力` `#概念`
- **拆分建议**：母卡保留；HW04 的调试经验（mask 错误、beam 实现 bug）可拆错题笔记。
