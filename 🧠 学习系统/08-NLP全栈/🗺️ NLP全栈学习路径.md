---
type: index
topic: NLP 全栈学习路径
created: 2026-04-11
status: active
tags:
- 学习路径
- NLP
- 自然语言处理
- 大语言模型
- LLM
description: 从数学基础到LLM前沿的完整NLP全栈学习路线图
---

# 🗺️ NLP 全栈学习路径

> "语言是思维的载体，NLP 是让机器理解人类思维的桥梁。"

```dataviewjs
// 学习进度统计
const stage1 = dv.pages('"🧠 学习系统/08-NLP全栈/01-基础准备"').where(p => p.status === "completed").length;
const stage1Total = dv.pages('"🧠 学习系统/08-NLP全栈/01-基础准备"').length;
const stage2 = dv.pages('"🧠 学习系统/08-NLP全栈/02-传统NLP方法"').where(p => p.status === "completed").length;
const stage2Total = dv.pages('"🧠 学习系统/08-NLP全栈/02-传统NLP方法"').length;
const stage3 = dv.pages('"🧠 学习系统/08-NLP全栈/03-深度学习NLP基础"').where(p => p.status === "completed").length;
const stage3Total = dv.pages('"🧠 学习系统/08-NLP全栈/03-深度学习NLP基础"').length;
const stage4 = dv.pages('"🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型"').where(p => p.status === "completed").length;
const stage4Total = dv.pages('"🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型"').length;
const stage5 = dv.pages('"🧠 学习系统/08-NLP全栈/05-大语言模型与前沿技术"').where(p => p.status === "completed").length;
const stage5Total = dv.pages('"🧠 学习系统/08-NLP全栈/05-大语言模型与前沿技术"').length;
const stage6 = dv.pages('"🧠 学习系统/08-NLP全栈/06-专业方向深入"').where(p => p.status === "completed").length;
const stage6Total = dv.pages('"🧠 学习系统/08-NLP全栈/06-专业方向深入"').length;

const totalCompleted = stage1 + stage2 + stage3 + stage4 + stage5 + stage6;
const totalNotes = stage1Total + stage2Total + stage3Total + stage4Total + stage5Total + stage6Total;
const totalProgress = totalNotes > 0 ? Math.round((totalCompleted / totalNotes) * 100) : 0;

dv.paragraph(`**总体进度: ${totalProgress}%** | 已完成: ${totalCompleted} / ${totalNotes} 主题`);
```

---

## 📚 阶段1：基础准备

| 状态 | 主题 | 核心概念 | 操作 |
|:---:|:---|:---|:---:|
| ⬜ | [[NLP数学基础]] | 线性代数、概率论、信息论基础 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/01-基础准备/NLP数学基础.md) |
| ⬜ | [[Python编程与NLP工具]] | NLTK、spaCy、正则表达式、文本处理 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/01-基础准备/Python编程与NLP工具.md) |
| ⬜ | [[语言学基础]] | 语音、词汇、句法、语义学基础 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/01-基础准备/语言学基础.md) |
| ⬜ | [[数据集与评测指标]] | 语料库、F1、BLEU、ROUGE、困惑度 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/01-基础准备/数据集与评测指标.md) |

---

## 📜 阶段2：传统NLP方法

| 状态 | 主题 | 核心概念 | 操作 |
|:---:|:---|:---|:---:|
| ⬜ | [[文本预处理]] | 分词、归一化、停用词、词干提取 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/02-传统NLP方法/文本预处理.md) |
| ⬜ | [[文本表示方法]] | One-hot、TF-IDF、n-gram、共现矩阵 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/02-传统NLP方法/文本表示方法.md) |
| ⬜ | [[统计机器学习]] | Naive Bayes、SVM、CRF、最大熵 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/02-传统NLP方法/统计机器学习.md) |
| ⬜ | [[序列标注]] | HMM、MEMM、CRF、BIO标注 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/02-传统NLP方法/序列标注.md) |
| ⬜ | [[主题模型]] | LSA、LDA、pLSA、文档主题分布 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/02-传统NLP方法/主题模型.md) |
| ⬜ | [[句法分析]] | 上下文无关文法、PCFG、依存句法 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/02-传统NLP方法/句法分析.md) |

---

## 🧠 阶段3：深度学习NLP基础

| 状态 | 主题 | 核心概念 | 操作 |
|:---:|:---|:---|:---:|
| ⬜ | [[词向量与Word2Vec]] | CBOW、Skip-gram、负采样、层次Softmax | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/03-深度学习NLP基础/词向量与Word2Vec.md) |
| ⬜ | [[GloVe与稠密向量]] | 共现矩阵分解、全局统计、向量空间 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/03-深度学习NLP基础/GloVe与稠密向量.md) |
| ⬜ | [[循环神经网络RNN]] | RNN结构、BPTT、梯度消失/爆炸 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/03-深度学习NLP基础/循环神经网络RNN.md) |
| ⬜ | [[LSTM与GRU]] | 门控机制、长程依赖、变体比较 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/03-深度学习NLP基础/LSTM与GRU.md) |
| ⬜ | [[Seq2Seq与注意力机制]] | 编码器-解码器、Bahdanau注意力、Luong注意力 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/03-深度学习NLP基础/Seq2Seq与注意力机制.md) |
| ⬜ | [[CNN在NLP中的应用]] | TextCNN、卷积特征、池化操作 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/03-深度学习NLP基础/CNN在NLP中的应用.md) |

---

## ⚡ 阶段4：Transformer与预训练模型

| 状态 | 主题 | 核心概念 | 操作 |
|:---:|:---|:---|:---:|
| ⬜ | [[Transformer架构]] | Self-Attention、多头注意力、位置编码 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/04-Transformer与预训练模型/Transformer架构.md) |
| ⬜ | [[BERT及其变体]] | MLM、NSP、RoBERTa、ALBERT、DistilBERT | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/04-Transformer与预训练模型/BERT及其变体.md) |
| ⬜ | [[GPT系列]] | 自回归LM、GPT-1/2/3、生成能力 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/04-Transformer与预训练模型/GPT系列.md) |
| ⬜ | [[其他预训练模型]] | XLNet、T5、ELECTRA、DeBERTa | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/04-Transformer与预训练模型/其他预训练模型.md) |
| ⬜ | [[参数高效微调PEFT]] | Adapter、Prompt Tuning、LoRA、Prefix Tuning | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/04-Transformer与预训练模型/参数高效微调PEFT.md) |
| ⬜ | [[HuggingFace生态系统]] | Transformers库、Datasets、Tokenizers、Trainer | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/04-Transformer与预训练模型/HuggingFace生态系统.md) |

---

## 🚀 阶段5：大语言模型与前沿技术

| 状态 | 主题 | 核心概念 | 操作 |
|:---:|:---|:---|:---:|
| ⬜ | [[Scaling Laws]] | 规模效应、涌现能力、计算最优训练 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/05-大语言模型与前沿技术/Scaling%20Laws.md) |
| ⬜ | [[指令微调与对齐]] | Instruction Tuning、SFT、RLHF、DPO | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/05-大语言模型与前沿技术/指令微调与对齐.md) |
| ⬜ | [[提示工程]] | Zero/Few-shot、CoT、ToT、AutoPrompt | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/05-大语言模型与前沿技术/提示工程.md) |
| ⬜ | [[检索增强生成RAG]] | 向量检索、稠密表示、RAG架构、多跳推理 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/05-大语言模型与前沿技术/检索增强生成RAG.md) |
| ⬜ | [[Agent与工具使用]] | ReAct、Toolformer、Function Calling、多Agent | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/05-大语言模型与前沿技术/Agent与工具使用.md) |
| ⬜ | [[LLM推理优化]] | KV Cache、量化、投机解码、PagedAttention | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/05-大语言模型与前沿技术/LLM推理优化.md) |

---

## 🎯 阶段6：专业方向深入

| 状态 | 主题 | 核心概念 | 操作 |
|:---:|:---|:---|:---:|
| ⬜ | [[信息抽取]] | NER、关系抽取、事件抽取、UIE | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/06-专业方向深入/信息抽取.md) |
| ⬜ | [[文本生成]] | 可控生成、文本摘要、机器翻译、风格迁移 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/06-专业方向深入/文本生成.md) |
| ⬜ | [[对话系统]] | 任务型对话、开放域聊天、多轮管理、情感对话 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/06-专业方向深入/对话系统.md) |
| ⬜ | [[问答系统]] | 阅读理解、KBQA、开放域问答、多文档QA | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/06-专业方向深入/问答系统.md) |
| ⬜ | [[多模态NLP]] | 视觉-语言模型、图文检索、VQA、文档理解 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/06-专业方向深入/多模态NLP.md) |
| ⬜ | [[文本分类与情感分析]] | 情感分类、意图识别、立场检测、讽刺检测 | [新建](obsidian://new?file=🧠%20学习系统/08-NLP全栈/06-专业方向深入/文本分类与情感分析.md) |

---

## 🗺️ 索引二：横向知识地图

| 维度 | 核心技术 | 代表模型/方法 | 入口 |
|:---|:---|:---|:---|
| **🔢 数学基础** | 线性代数、概率论、信息论 | SVD、贝叶斯、熵 | [[知识地图/🔢 数学基础维度\|查看]] |
| **📜 传统方法** | 分词、文本表示、统计ML | HMM、CRF、LDA | [[知识地图/📜 传统方法维度\|查看]] |
| **🧠 深度学习** | 词向量、序列模型、Seq2Seq | Word2Vec、LSTM、Attention | [[知识地图/🧠 深度学习维度\|查看]] |
| **⚡ Transformer** | 自注意力、预训练模型、PEFT | BERT、GPT、LoRA | [[知识地图/⚡ Transformer维度\|查看]] |
| **🚀 LLM前沿** | 大模型理论、提示工程、RAG | ChatGPT、RAG系统 | [[知识地图/🚀 LLM前沿维度\|查看]] |
| **🎯 专业应用** | 信息抽取、生成、对话、多模态 | UIE、可控生成、VLM | [[知识地图/🎯 专业应用维度\|查看]] |

---

## 🎯 当前学习重点

```dataviewjs
dv.table(
    ["笔记", "阶段", "更新日期", "状态"],
    dv.pages('"🧠 学习系统/08-NLP全栈"')
        .where(p => !p.file.path.includes("🗺️"))
        .sort(p => p.file.mtime, 'desc')
        .limit(5)
        .map(p => {
            let stage = "-";
            if (p.file.path.includes("01-")) stage = "📚 基础";
            else if (p.file.path.includes("02-")) stage = "📜 传统";
            else if (p.file.path.includes("03-")) stage = "🧠 深度";
            else if (p.file.path.includes("04-")) stage = "⚡ Trans";
            else if (p.file.path.includes("05-")) stage = "🚀 LLM";
            else if (p.file.path.includes("06-")) stage = "🎯 专业";
            return [p.file.link, stage, p.file.mtime.toFormat("MM-dd"), p.status || "ongoing"];
        })
);
```

---

## 📚 推荐学习资源

### 经典教材

| 书名 | 作者 | 特点 | 适用阶段 |
|:---|:---|:---|:---:|
| 《Speech and Language Processing》| Jurafsky & Martin | NLP圣经，免费在线 | 全阶段 |
| 《Neural Network Methods for NLP》| Yoav Goldberg | 深度学习NLP | 阶段3-4 |
| 《Natural Language Processing with PyTorch》| Rao & McMahan | 实战导向 | 阶段3-5 |

### 在线资源

| 资源 | 类型 | 说明 |
|:---|:---|:---|
| Stanford CS224n | 课程 | 深度学习NLP经典 |
| Hugging Face | 平台 | 模型、数据集、教程 |
| LangChain文档 | 文档 | Agent/RAG开发 |

- 想按阶段直接找教材，或者看哪些主教材还没下载：[[🧠 学习系统/08-NLP全栈/📚 教材挂载索引|进入教材挂载索引]]

---

## 🔗 知识连接索引

| 本路径概念 | 关联路径 | 关联概念 |
|:---|:---|:---|
| 数学基础 | [[🗺️ 机器学习学习路径\|机器学习]] | 线性代数、概率统计、信息论 |
| 深度学习基础 | [[🗺️ 机器学习学习路径\|机器学习]] | 神经网络、反向传播、梯度下降 |
| Transformer | [[🗺️ 计算机视觉学习路径\|计算机视觉]] | Vision Transformer、多模态融合 |
| 优化算法 | [[🗺️ 最优化方法学习路径\|最优化方法]] | Adam、学习率调度、训练优化 |
| 注意力机制 | [[🗺️ 计算机视觉学习路径\|计算机视觉]] | 自注意力、空间注意力 |
| 强化学习对齐 | [[🗺️ 强化学习学习路径\|强化学习]] | RLHF、PPO、策略优化 |
| 词向量表示 | [[🗺️ 社交网络挖掘学习路径\|社交网络挖掘]] | 网络嵌入、节点表示学习 |
| 主题模型 | [[🗺️ 概率图模型学习路径\|概率图模型]] | LDA、概率生成模型 |
| 多模态NLP | [[🗺️ 计算机视觉学习路径\|计算机视觉]] | CLIP、视觉-语言预训练 |

---

## 🎓 课程挂载补充

| 课程 | 路径内落点 | 备注 |
|:---|:---|:---|
| 自然语言处理 | [[🗺️ NLP全栈学习路径\|本路径总览]] | 已存在主路径 |
| 自然语言处理前沿课题研究 | [[06-专业方向深入/🎯 第六阶段：专业方向深入\|阶段6]] | 对应前沿专题、RAG、多模态与新范式 |
| 计算语言学 | [[01-基础准备/📚 第一阶段：基础准备\|阶段1]] | 作为语言学底层与形式化表示入口 |
| 语音信号数字处理 | [[01-基础准备/📚 第一阶段：基础准备\|阶段1]] / [[🧠 学习系统/12-信号与系统/🗺️ 信号与系统学习路径\|信号与系统]] | 跨 NLP 与信号处理双路径挂载 |
| 神经与认知计算 | [[06-专业方向深入/🎯 第六阶段：专业方向深入\|阶段6]] | 对应认知建模、神经表征与语言理解 |

---

## 🔗 快速导航

### 纵向路线
- [[01-基础准备/📚 第一阶段：基础准备\|📚 第一阶段：基础准备]]
- [[02-传统NLP方法/📜 第二阶段：传统NLP方法\|📜 第二阶段：传统NLP方法]]
- [[03-深度学习NLP基础/🧠 第三阶段：深度学习NLP基础\|🧠 第三阶段：深度学习NLP基础]]
- [[04-Transformer与预训练模型/⚡ 第四阶段：Transformer与预训练模型\|⚡ 第四阶段：Transformer与预训练模型]]
- [[05-大语言模型与前沿技术/🚀 第五阶段：大语言模型与前沿技术\|🚀 第五阶段：大语言模型与前沿技术]]
- [[06-专业方向深入/🎯 第六阶段：专业方向深入\|🎯 第六阶段：专业方向深入]]
- [[🧠 学习系统/08-NLP全栈/📚 教材挂载索引|📚 教材挂载索引]]

### 横向知识地图
- [[知识地图/🗺️ 横向知识地图\|🗺️ 横向知识地图总览]]

### 关联路径
- [[🗺️ 机器学习学习路径\|机器学习]]
- [[🗺️ 计算机视觉学习路径\|计算机视觉]]
- [[🗺️ 最优化方法学习路径\|最优化方法]]
- [[🗺️ 强化学习学习路径\|强化学习]]

---

*路线图更新：2026-04-14*
