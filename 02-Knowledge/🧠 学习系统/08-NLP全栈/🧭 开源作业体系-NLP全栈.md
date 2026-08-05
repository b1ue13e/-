---
type: index
topic: "开源作业体系-NLP全栈"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [索引, 开源课程, 作业体系, NLP全栈, CS224N, HuggingFace]
template: Obsidian单知识点深度学习模板
---

# 🧭 开源作业体系-NLP全栈

> 本页是「NLP全栈」的开源名校教材与作业的**唯一挂载点**：教材主线、官方作业链、知识点覆盖矩阵、验收方式全部在此对齐。作业体系来源：**Stanford CS224N 官方 Assignments 1-5**（https://web.stanford.edu/class/cs224n/，GitHub: https://github.com/stanfordnlp/cs224n-winter2023-assignments）+ **Hugging Face Course**（https://huggingface.co/learn/nlp-course）。

---

## 📚 教材主线（Spine）

| 角色 | 来源 | 用途 |
|:---|:---|:---|
| 主线教材 | [Speech and Language Processing 3e (SLP3)](https://web.stanford.edu/~jurafsky/slp3/)（Jurafsky & Martin 官方免费草稿） | 语言模型 → 词向量 → 序列建模 → Transformer → 预训练 LLM 的完整知识主线；详见 [[📚 教材挂载索引]] |
| 官方作业 | [Stanford CS224N Assignments 1-5](https://web.stanford.edu/class/cs224n/)（官方仓库 `stanfordnlp/cs224n-winter2023-assignments`） | 每份作业一个可自动评测的项目，即本体系 HW01-HW05 |
| 工程补丁 | [Hugging Face Course](https://huggingface.co/learn/nlp-course)（Apache-2.0，每章含 Lab） | tokenizer / datasets / Trainer / evaluation 的工程实践，补齐 CS224N 不覆盖的工具链 |
| 补充参考 | 李宏毅《机器学习》深度学习章节（RNN/Attention/Transformer 直觉版）+ CS224N 官方讲义与录屏 | 直觉类比、作业思路的另一种讲法 |

**Honor Code 说明**：CS224N 官方作业（含 starter code、solutions）**仅用于自学自测**——作业 PDF 与 solutions 不公开传播、不重新分发、不用于任何商业用途；本地实现必须自己完成，完成后可对照官方 solutions 复盘。Hugging Face Course 为 Apache-2.0 开源，可自由学习与引用。

---

## 🎯 作业体系（CS224N Assignments 1-5）

| HW | 主题 | 官方 Assignment | 所需知识点（双链） | 验收方式 |
|:---|:---|:---:|:---|:---|
| HW01 | Word2Vec 词向量 | Assignment 1（+ A2 的 word2vec 部分） | [[词向量与Word2Vec]]、[[GloVe与稠密向量]]、[[文本预处理]] | 手写 sigmoid/softmax 梯度、实现 naive 与负采样版本的 skip-gram，数值梯度校验通过 |
| HW02 | 文本分类：TF-IDF / 线性模型 / 神经网络对照 | Assignment 2（依存分析前置的文本表示与分类热身） | [[文本分类与情感分析]]、[[数据集与评测指标]] | 在同一数据集上跑 TF-IDF+逻辑回归 vs MLP vs 微调模型，对比报告 |
| HW03 | 序列标注 / 依存分析 | Assignment 3（依存句法分析，transition-based parser） | [[循环神经网络RNN]]、[[数据集与评测指标]] | 实现基于 MLP 的 arc-standard 转移解析器，UAS/LAS 达到官方 baseline |
| HW04 | Seq2Seq / Attention / NMT | Assignment 4（NMT with RNNs + attention） | [[Seq2Seq与注意力机制]]、[[循环神经网络RNN]] | 实现编码器-解码器 + Bahdanau attention + beam search，BLEU 达标 |
| HW05 | Transformer / MinBERT 手撕 | Assignment 5（MinBERT / self-attention / fine-tuning） | [[Transformer架构]]、[[Self-Attention自注意力机制]]、[[BERT及其变体]]、[[NLP全栈 - HW05：Transformer 与 MinBERT 从零手撕阶梯作业\|HW05 阶梯作业]] | 从零实现 multi-head self-attention 与 MinBERT，SST-2 微调达标（见阶梯作业 4 档 Rubric） |

> 分层验收原则：HW01 是向量地基（必须先过数值梯度校验）；HW02 是"传统 vs 神经网络"的分水岭对照；HW03-04 是序列建模双璧（标注/句法与翻译）；HW05 是整条链的 Capstone——从零手撕 Transformer 编码器。HW01-04 目前为**规划状态**（官方 PDF 自测），HW05 已有完整阶梯作业可执行。

---

## 🧠 框架内知识点笔记（模板卡）

按 HW01-HW05 覆盖矩阵规划的模板笔记（用 `Obsidian单知识点深度学习模板` 填充）：

| HW | 模板笔记（本次已建） | 已有笔记（不重复建） |
|:---|:---|:---|
| HW01 | [[词向量与Word2Vec]]、[[GloVe与稠密向量]] | [[03-深度学习NLP基础/CBOW\|CBOW]]、[[03-深度学习NLP基础/Skip-gram\|Skip-gram]]、[[03-深度学习NLP基础/负采样\|负采样]]、[[03-深度学习NLP基础/层次Softmax\|层次Softmax]]、[[03-深度学习NLP基础/词向量相似度\|词向量相似度]]、[[03-深度学习NLP基础/词向量类比\|词向量类比]] |
| HW02 | [[文本分类与情感分析]]、[[文本预处理]]、[[数据集与评测指标]] | [[02-传统NLP方法/TF-IDF\|TF-IDF]]、[[02-传统NLP方法/BoW\|BoW]]、[[02-传统NLP方法/朴素贝叶斯\|朴素贝叶斯]]、[[02-传统NLP方法/One-Hot\|One-Hot]] |
| HW03 | [[循环神经网络RNN]] | [[03-深度学习NLP基础/RNN结构\|RNN结构]]、[[03-深度学习NLP基础/RNN BPTT\|RNN BPTT]]、[[03-深度学习NLP基础/RNN梯度消失\|RNN梯度消失]]、[[03-深度学习NLP基础/RNN梯度爆炸\|RNN梯度爆炸]]、[[03-深度学习NLP基础/Bi-LSTM\|Bi-LSTM]]、[[03-深度学习NLP基础/GRU结构\|GRU结构]]、[[02-传统NLP方法/依存分析\|依存分析]] |
| HW04 | [[Seq2Seq与注意力机制]] | [[03-深度学习NLP基础/Seq2Seq Encoder\|Seq2Seq Encoder]]、[[03-深度学习NLP基础/Seq2Seq Decoder\|Seq2Seq Decoder]]、[[03-深度学习NLP基础/Bahdanau\|Bahdanau]]、[[03-深度学习NLP基础/Luong\|Luong]]、[[03-深度学习NLP基础/Beam Search原理\|Beam Search]]、[[03-深度学习NLP基础/上下文向量\|上下文向量]] |
| HW05 | [[Transformer架构]]、[[BERT及其变体]]、[[GPT系列]] | [[Self-Attention自注意力机制]]、[[BERT与GPT对比]]、[[🎯 RoPE 旋转位置编码 (Rotary Position Embedding)\|RoPE 旋转位置编码]]、[[04-Transformer与预训练模型/QKV\|QKV]]、[[04-Transformer与预训练模型/多头注意力\|多头注意力]]、[[04-Transformer与预训练模型/LayerNorm\|LayerNorm]]、[[04-Transformer与预训练模型/残差连接\|残差连接]] |
| 工具链 | [[HuggingFace生态系统]] | [[04-Transformer与预训练模型/BERT\|BERT]]、[[04-Transformer与预训练模型/RoBERTa\|RoBERTa]]、[[04-Transformer与预训练模型/ALBERT\|ALBERT]]、[[04-Transformer与预训练模型/GPT-1\|GPT-1]]、[[04-Transformer与预训练模型/GPT-2\|GPT-2]]、[[04-Transformer与预训练模型/GPT-3\|GPT-3]]、[[02-传统NLP方法/子词切分\|子词切分]]、[[02-传统NLP方法/N-gram定义\|N-gram]] |
| 应用链 | [[检索增强生成RAG]] | [[05-大语言模型与前沿技术/向量数据库\|向量数据库]]、[[05-大语言模型与前沿技术/RAG Embedding\|RAG Embedding]]、[[05-大语言模型与前沿技术/切分策略\|切分策略]]、[[05-大语言模型与前沿技术/Reranking\|Reranking]]、[[05-大语言模型与前沿技术/混合检索\|混合检索]] |

### 待补清单（下一批）
- [ ] LSTM 与门控机制（HW03 进阶，已有 [[03-深度学习NLP基础/GRU vs LSTM\|GRU vs LSTM]] 原子卡可聚合）
- [ ] 机器翻译评测与错误分析（HW04 报告用，可并入 [[数据集与评测指标]]）
- [ ] 微调与 Trainer 实践卡（HW05 工具链，HF Course Ch.3）

---

## ✅ 验收方式与评分

1. **CS224N 原版作业自测**：每份官方 Assignment 的 starter code 跑通 + 数值梯度/单元测试通过为准；实现存档到 `03-Projects/projects-nlp/`。
2. **Hugging Face Course 每章 Lab**：HF Course 每章末尾的 Lab notebook 全部执行通过（tokenizer → datasets → trainer → evaluation → RAG 逐章推进），作为工程验收。
3. **报告 Rubric**（每个 HW 完成后交一份 1-2 页报告）：
   - 方法简述（模型结构、损失、超参）—— 40%
   - 实验对照（baseline vs 实现、消融或对比表）—— 30%
   - 错误分析（3 个以上典型错误样例 + 归因）—— 20%
   - 与讲义/教材的对照反思（1 个"课本没讲但作业里踩到"的点）—— 10%
4. **满分线**：HW01-04 官方测试全过（各 15 分）+ HW05 阶梯作业 4 档达标（20 分）+ 5 份报告（各 4 分）= 100 分。

---

## 🔗 相关入口

- [[🗺️ NLP全栈学习路径|NLP 全栈学习路径]]
- [[📚 教材挂载索引|教材挂载索引]]
- [[📋 知识点卡清单|知识点卡清单]]
- [[NLP全栈 - HW05：Transformer 与 MinBERT 从零手撕阶梯作业|HW05 阶梯作业]]
- 官方仓库：https://github.com/stanfordnlp/cs224n-winter2023-assignments
- HF Course：https://huggingface.co/learn/nlp-course
