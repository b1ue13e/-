---
sources: ['Yang, Z., et al. (2019). XLNet: Generalized Autoregressive Pretraining for Language Understanding. NeurIPS 2019.', 'Raffel, C., et al. (2020). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (T5). JMLR 2020.', 'Lewis, M., et al. (2020). BART: Denoising Sequence-to-Sequence Pre-training. ACL 2020.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "其他预训练模型"
created: 2026-08-06
status: completed
assessment_exempt: false
difficulty: intermediate
stage_moc: "[[🧭 阶段4-Transformer与预训练模型]]"
upstream: ["[[08-NLP全栈-GPT系列]]"]
tags: [学习, NLP, T5, BART, XLNet, ELECTRA, 预训练模型]
---

# 08-NLP全栈-其他预训练模型

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 除了简单的 Encoder-only (BERT) 和 Decoder-only (GPT) 之外，很多自然语言处理任务（如句子改写、摘要生成、语法纠错）属于 Sequence-to-Sequence 结构。如何设计结合 Masked 噪声还原（BART）、统一 Text-to-Text 范式（T5）以及判别式替换检测（ELECTRA），填补了更高效预训练算法的版图。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是经典 Encoder-Decoder 预训练架构（BART / T5）与高效生成式对抗预训练（ELECTRA / Discriminator）的代表。
- **实际应用场景**：T5 / BART 文本摘要与翻译、ELECTRA 高效低资源 NLU 训练。

---


### 3.1 形式化目标与算子数学定义

1. **XLNet Permutation Language Modeling (PLM)**：
目标是在全排列概率下最大化因子化对数似然：
$$\max_{\theta} \mathbb{E}_{\mathbf{z} \sim \mathcal{Z}_T} \left[ \sum_{t=c+1}^{T} \log p_\theta(x_{z_t} \mid \mathbf{x}_{\mathbf{z}_{<t}}) \right]$$

2. **T5 Span Corruption Objective**：
将连续掩码片段替换为单独的 Sentinel Token $\langle X \rangle, \langle Y \rangle$，目标是预测被遮蔽的文本片段序列：
$$\mathcal{L}_{\text{T5}} = -\sum_{j \in \text{Masked}} \log P(x_j \mid x_{<j}, \mathbf{x}_{\text{unmasked}})$$

3. **DeBERTa Disentangled Attention**：
解耦位置与内容注意力，计算内容-内容、内容-位置和位置-内容三分量：
$$A_{i,j} = \mathbf{Q}_i^C (\mathbf{K}_j^C)^T + \mathbf{Q}_i^C (\mathbf{K}_{\delta(i,j)}^P)^T + \mathbf{K}_j^C (\mathbf{Q}_{\delta(j,i)}^P)^T$$


## 3. 典型预训练模型架构速查表

| 模型 | 架构类型 | 预训练目标 (Objective) | 核心特点 |
| :--- | :--- | :--- | :--- |
| **T5 (Text-to-Text Transfer)** | Encoder-Decoder | 破坏片段还原 (Span Corruption) | 统一所有 NLP 任务为 "text -> text" 形式（如 `"translate English to German: ..."`） |
| **BART** | Encoder-Decoder | 去噪自编码器 (Denoising Autoencoder) | 支持 Token 掩码、删除、替换、句子打乱与旋转 |
| **ELECTRA** | Encoder-only | 替换 Token 检测 (Replaced Token Detection, RTD) | 类似 GAN，生成器填充掩码，判别式判定 Token 是否被替换；样本利用率达 100% |
| **XLNet** | Encoder-like | 排列语言模型 (Permutation Language Model, PLM) | 基于双流注意力 (Two-Stream Attention) 克服 BERT [MASK] 的独立性假设 |

---

## 4. Python 代码示例：使用 T5 进行零样本翻译与摘要

```python
from transformers import T5ForConditionalGeneration, T5Tokenizer

tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# 1. 任务 1：翻译
input_text = "translate English to German: The house is wonderful."
input_ids = tokenizer.encode(input_text, return_tensors="pt")
outputs = model.generate(input_ids)
print("T5 Translation:", tokenizer.decode(outputs[0], skip_special_tokens=True))

# 2. 任务 2：摘要
summarize_text = "summarize: State Bank of India provides online banking services to its customers across the globe."
input_ids = tokenizer.encode(summarize_text, return_tensors="pt")
outputs = model.generate(input_ids, max_length=20)
print("T5 Summary:", tokenizer.decode(outputs[0], skip_special_tokens=True))
```

---


## 5. 常见误区与对比矩阵

| 模型架构 | 预训练范式 (Objective) | 编码器/解码器结构 | 核心优势与适配场景 |
| :--- | :--- | :--- | :--- |
| **RoBERTa** | 动态掩码 (Dynamic MLM) | Only-Encoder | 相比 BERT 剔除 NSP，在大语料上收敛更稳定 |
| **XLNet** | 全排列语言模型 (PLM) | Two-Stream Self-Attention | 克服 MLM 的独立性假设与预训练/微调不一致 |
| **T5** | Span Corruption 文本到文本 | Encoder-Decoder | 统一所有 NLP 任务为 Text-to-Text 范式 |
| **DeBERTa** | 解耦注意力机制 (Disentangled) | Enc-Dec / Only-Encoder | 分离内容向量与相对位置向量，性能超越 Human Baseline |





## 6. 闭卷自测与验收入口

请在不查阅资料的前提下尝试解答以下问题，或完成对应关联作业：
1. 本知识点的核心定义与推导公式是什么？
2. 相比传统方法，它的核心优势与工程选型 Trade-offs 是什么？
3. 如何在 PyTorch / Python 中实现并校验其关键张量维度与运算逻辑？


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《其他预训练模型》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《其他预训练模型》的核心机制及其与上下游模块的连接逻辑。
2. **代数/代码自测**：手写关键代数推导步骤或 PyTorch/Python 核心实现伪代码。
3. **防错自测**：如果输入数据出现极小值或极大值离群点，该模块会发生什么异常？如何做数值稳定防护？


---

## 🛠️ 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
