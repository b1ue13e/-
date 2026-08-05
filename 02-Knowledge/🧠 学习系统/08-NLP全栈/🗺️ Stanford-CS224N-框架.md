---
type: index
topic: "Stanford CS224N 课程框架"
created: 2026-08-06
status: active
tags: [索引, NLP, CS224N]
---

# 🗺️ Stanford CS224N: Natural Language Processing with Deep Learning

> **课程定位**：NLP 领域标杆课程，侧重深度学习在 NLP 中的工程与应用实践。
> **适用对象**：具备基础机器学习与 Python/PyTorch 能力，希望系统构建 NLP 全栈知识库的学习者。
> **参考教材**：Dan Jurafsky & James H. Martin: *Speech and Language Processing* (3rd ed.)
> 🆘 **入场券与避风港**：在进入核心网络与 Transformer 推导前，请务必先复习微积分链式法则与矩阵求导。如果卡壳，请查阅前置数学速查表（Math Cheat Sheet），切勿在工程卡点前死磕纯数学。

---

## 🗂️ 核心模块与知识点映射

本框架将 CS224N 的 Lecture 讲义与对应的 Assignment 映射至 `08-NLP全栈` 下的原子知识卡片中。

### 模块一：词向量与基础神经网络 (Lectures 1-3)
**核心概念**：Word2Vec, GloVe, SVD, 神经网络反向传播
- [[词向量与Word2Vec.md]]：CBOW 与 Skip-gram 模型，负采样优化。
- [[GloVe与稠密向量.md]]：基于全局词频统计的词向量模型。
- [[文本分类与情感分析.md]]：基于神经网络的文本分类基础。
- [[NLP数学基础.md]]：反向传播与矩阵求导基础。
> 📝 **对应作业**：`Assignment 1: Exploring Word Vectors`（探索词向量与共现矩阵）

> 🌉 **Evolutionary Bridge (演进桥梁)**：词向量解决了单词的离散表示问题，但无法理解句子的结构和单词的上下文语境。我们需要引入序列模型来处理长文本。

### 模块二：句法分析与语言模型 (Lectures 4-5)
**核心概念**：依存句法分析, N-gram, 循环神经网络 (RNN)
- [[句法分析.md]]：基于 Transition-based 的依存句法分析。
- [[循环神经网络RNN.md]]：RNN 的前向传播、BPTT、梯度消失/爆炸问题及 LSTM/GRU。
> 📝 **对应作业**：`Assignment 2: Dependency Parsing`（用神经网络实现依存句法分析器）

> 🌉 **Evolutionary Bridge (演进桥梁)**：RNN 虽然能处理序列，但在长文本中面临严重的梯度消失问题。为了让长距离的单词也能产生关联，并且解决机器翻译中的对齐问题，我们必须引入 Attention 机制。
> - **加性注意力 (Bahdanau Attention, 2014)**：最早的 Attention，通过一个小型单隐层神经网络动态计算 Q 和 K 的对齐权重。
> - **点积注意力 (Luong Attention, 2015)**：抛弃了神经网络，直接让 Q 和 K 做点积（或矩阵乘法），极大加快了计算速度。
> - **自注意力 (Self-Attention, 2017)**：Q、K、V 全部来自句子本身，彻底摆脱 RNN 的序列依赖。

### 模块三：机器翻译、Seq2Seq 与注意力机制 (Lectures 6-8)
**核心概念**：Seq2Seq, 机器翻译 (NMT), 注意力机制 (Attention)
- [[Seq2Seq与注意力机制.md]]：编码器-解码器架构，基础的 Attention 机制。
- [[数据集与评测指标.md]]：BLEU、ROUGE 评测指标及计算方法。
> 📝 **对应作业**：`Assignment 3: Neural Machine Translation (RNN)`（构建基于 RNN 的机器翻译系统）

> 🌉 **Evolutionary Bridge (演进桥梁)**：基于 RNN 的 Attention 虽然有效，但 RNN 的串行计算本质打破了 GPU 并行加速的优势。既然 Attention 这么好用，我们为什么不抛弃 RNN，只用 Attention 呢？这就是 Transformer 诞生的前奏。

### 模块四：Transformer 与预训练模型 (Lectures 9-10)
**核心概念**：Self-Attention, Transformer, BERT, GPT
- [[Self-Attention自注意力机制.md]]：缩放点积注意力，Q/K/V 的直觉与推导。
- [[Transformer架构.md]]：多头注意力、位置编码、残差连接与 LayerNorm。
- [[BERT及其变体.md]]：掩码语言模型 (MLM)、下一句预测 (NSP)。
- [[BERT与GPT对比.md]]：自编码器 (Autoencoder) vs 自回归 (Autoregressive) 的优劣对比。
> 📝 **对应作业**：`Assignment 4: NMT with Attention` & `Assignment 5: Self-Attention & Pretraining`

> 🌉 **Evolutionary Bridge (演进桥梁)**：Transformer 的出现彻底解决了并行计算问题，算力终于可以暴力堆叠。由此，NLP 进入了大模型（LLM）的“涌现”时代。如何让这些满腹经纶的庞然大物听懂人类指令，成为了新的难题。

> 🧠 **心智图谱前置**：在进入模块五前，请先在脑海中建立大模型对齐的宏观流水线（请注意有两条独立分支）：
> - **基于 RL 的古典路线 (PPO)**：无监督预训练 (Next-Token Prediction) -> SFT (指令微调教它怎么说话) -> RM (奖励模型教它人类喜好) -> PPO (强化学习让它自我进化)
> - **无 RL 的现代路线 (DPO)**：无监督预训练 -> SFT -> 偏好数据 -> DPO (直接把偏好数据通过数学等价转化作为损失函数，彻底干掉 RM 和 PPO 的复杂性)。
> 不要把它们当成孤立的知识点，它们是演进中的工业流水线。

### 模块五：大语言模型与前沿应用 (Lectures 11-14)
**核心概念**：Prompting, RLHF, 文本生成, RAG
- [[文本生成.md]]：解码策略（Greedy, Beam Search, Top-k, Top-p）。
- [[提示工程.md]]：In-Context Learning (ICL), Chain of Thought (CoT)。
- [[指令微调与对齐.md]]：SFT, RLHF, 奖励模型, PPO/DPO。
- [[检索增强生成RAG.md]]：外挂知识库检索与生成流程。
- [[问答系统.md]] / [[对话系统.md]]：现代问答与对话系统的构建。

> 🌉 **Evolutionary Bridge (演进桥梁)**：大模型虽然强大，但在长篇复杂文本中极易产生指代混乱与幻觉。为了将其接入严谨的业务系统，我们需要更精确的信息抽取与语义解析技术。

### 模块六：指代消解与高级语言理解 (Lectures 15-18)
**核心概念**：Coreference Resolution, Information Extraction, Semantic Parsing
- [[信息抽取.md]]：实体链接、关系抽取（Relation Extraction）。
- [[句法分析.md]]：除了依存句法，扩展指代消解（Mention Detection, Coreference）。
- [[序列标注.md]]：NER（命名实体识别）与高级 CRF 模型。
> 📝 **拓展挑战**：实现基于神经网络的指代消解系统。

### 模块七：多模态与其他前沿扩展 (Lectures 19-22)
**核心概念**：Multimodal NLP, Ethics in NLP, Future Trends
- [[多模态NLP.md]]：CLIP (图文连连看), LLaVA 架构，视觉与语言的对齐。
- [[其它预训练模型.md]]：探讨 T5, ALBERT, ELECTRA 等不同技术路线。
- [[参数高效微调PEFT.md]]：LoRA (给大模型外挂小体积知识包), Prefix Tuning, P-Tuning 实战。

---

## 🚀 阶段性学习建议与前置知识 (Prerequisites)

1. **先决条件**：在学习本框架前，建议已完成 [[Python编程与NLP工具.md]] 和 PyTorch 的基本入门。
2. **作业验收**：所有 CS224N 的 Assignments 均作为**必做闭卷验收项**，实现在 [[代码实践.md]] 和相关的知识卡片中。
3. **理论与直觉并重**：对于 Attention 和 Transformer，务必掌握其矩阵维度的变换，做到能手推维度。

---
## 🔄 知识依赖图谱 (Related)
- **上游依赖**：17-机器学习（梯度下降、交叉熵）
- **下游延伸**：多模态NLP (如 CLIP, LLaVA)，高效微调 (PEFT, LoRA)，LLM 推理优化 (KV Cache, FlashAttention)
