---
title: "NLP全栈 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "NLP全栈 4-Tier 阶梯作业规范"
course: "NLP全栈"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [NLP全栈, 4Tier作业, 阶梯作业, 编程实战, PyTest, CS224N]
---

# 🗣️ NLP全栈 4-Tier 阶梯作业全景规范说明书 (Jurafsky & Stanford CS224N 范式)

> 本说明书为 **08-NLP全栈** 路径（基于 Jurafsky 《Speech and Language Processing (3e draft)》与 Stanford CS224N）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ HuggingFace Pipeline 调包 / TF-IDF / N-gram 跑通分类
🟡 L2 - Medium Baseline   │ GloVe 词向量 / RNN 文本分类 / Teacher Forcing 训练 Seq2Seq
🔴 L3 - Strong Baseline   │ [核心] 不调用 Transformer 高级库，从零手撕 Self-Attention / Beam Search / RoPE / RAG
👑 L4 - Boss Baseline     │ 7B 大模型 QLoRA 微调 / vLLM 连续批处理推理优化 / 形式化困惑度评估
```

---

## 🎯 NLP 全栈阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 词向量与分布式语义 (Word Vectors & GloVe / Word2Vec)
- **开源溯源**：Jurafsky Ch 6 / Stanford CS224N Assignment 1 & 2
- 🟢 **L1**: 使用 Gensim 加载预训练 GloVe/Word2Vec 词向量，计算词语余弦相似度。
- 🟡 **L2**: 实现 Word2Vec Skip-Gram 模型的负采样 (Negative Sampling) 损失函数。
- 🔴 **L3 (手撕核心)**：**从零手撕 Skip-Gram 与 CBOW 的梯度推导与 NumPy 前向反向传播**：
  $$ J_{\text{NEG}}(\theta) = -\log \sigma(v_{w_O}'^T v_{w_I}) - \sum_{k=1}^K \log \sigma(-v_{w_k}'^T v_{w_I}) $$
- 👑 **L4**: 实现 FastText 子词 (Subword / Character n-grams) 词向量。

### 2. HW02 - 依存句法分析 (Dependency Parsing)
- **开源溯源**：Jurafsky Ch 18 / Stanford CS224N Assignment 3
- 🟢 **L1**: 使用 spaCy / Stanza 跑通依存句法树提取。
- 🟡 **L2**: 构建基于转移 (Transition-Based) 的神经网络句法分析器。
- 🔴 **L3 (手撕核心)**：**手撕 Shift-Reduce 依存句法分析器的 Stack / Buffer / Arcs 转移状态机**。
- 👑 **L4**: 实现 Graph-Based 依存句法分析算法 (Eisner 算法 / MST)。

### 3. HW03 - 神经机器翻译 (NMT with Attention & Beam Search)
- **开源溯源**：Jurafsky Ch 10 / Stanford CS224N Assignment 4
- 🟢 **L1**: 使用 BiLSTM Encoder + LSTM Decoder 实现中英机器翻译。
- 🟡 **L2**: 引入 Bahdanau (加法) 与 Luong (乘法) 注意力机制。
- 🔴 **L3 (手撕核心)**：**从零手撕 Beam Search 解码器算法（包含长度惩罚 Length Penalty 与重复词惩罚）**。
- 👑 **L4**: 实现相对位置编码 (Relative Positional Encoding) 与 BLEU-4 评估。

### 4. HW04 - 从零手撕 Transformer 架构 (Self-Attention & RoPE)
- **开源溯源**：Jurafsky Ch 9 & 10 / Stanford CS224N Assignment 5
- 🟢 **L1**: 使用 PyTorch `nn.Transformer` 跑通 Seq2Seq 任务。
- 🟡 **L2**: 实现 Scaled Dot-Product Attention 与 Multi-Head Attention。
- 🔴 **L3 (手撕核心)**：**从零手撕 Transformer Decoder 层（包含 Causal Mask 掩码、RoPE 旋转位置编码与 LayerNorm）**：
  $$ R_{\Theta, m}^d = \text{diag}\left(R_{\theta_1, m}, R_{\theta_2, m}, \dots, R_{\theta_{d/2}, m}\right) $$
- 👑 **L4**: 实现 FlashAttention 算子并比较 CUDA 内存占用。

### 5. HW05 - 检索增强生成与向量数据库 (RAG & Dense Retrieval)
- **开源溯源**：Jurafsky Ch 14 / Stanford CS246
- 🟢 **L1**: 使用 LangChain / LlamaIndex + FAISS 跑通文档问答。
- 🟡 **L2**: 构建 BM25 稀疏检索与 Dense Passage Retrieval (DPR) 混合检索 (Hybrid Search)。
- 🔴 **L3 (手撕核心)**：**手撕 BM25 评分公式与基于 Cosine 相似度的向量倒排索引检索器**。
- 👑 **L4**: 实现 Re-ranking 交叉编码器 (Cross-Encoder) 与幻觉检测 (Hallucination Audit)。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-nlp/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-nlp/tests/test_hw01_word2vec.py
pytest 03-Projects/projects-nlp/tests/test_hw03_beam_search.py
pytest 03-Projects/projects-nlp/tests/test_hw04_transformer.py
```
