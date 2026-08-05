---
title: "BERT及其变体"
date: "2026-08-02"
type: concept
course: "NLP全栈"
importance: "A"
tags: [学习, NLP全栈, BERT, 预训练, 微调, RoBERTa, ALBERT, DistilBERT]
upstream: [Transformer架构, 文本预处理, 词向量与Word2Vec]
downstream: [GPT系列, HuggingFace生态系统, 文本分类与情感分析, 检索增强生成RAG]
status: learning
concept: ["预训练语言模型", "迁移学习", "掩码语言模型"]
prerequisites: ["Transformer架构", "Self-Attention自注意力机制", "交叉熵"]
related: ["Transformer架构", "GPT系列", "BERT与GPT对比", "HuggingFace生态系统", "Self-Attention自注意力机制"]
flow: project
kind: concept
template: Obsidian单知识点深度学习模板
created: 2026-08-02
---

# BERT及其变体

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：BERT 是 HW05 的微调对象（MinBERT 就是最小版 BERT）；预训练-微调范式是 2018 年后 NLP 的绝对主流，[[文本分类与情感分析]] 的 HW02 进阶方案就是微调 BERT。变体（RoBERTa/ALBERT/DistilBERT）是面试高频对比题。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 传统 NLP 每个任务都要从零训练模型，且标注数据稀缺（标注 10 万条情感语料要花大量人力）。而**无标注文本几乎是无限的**（维基百科、网页、书籍）。词向量（Word2Vec）虽然利用了无标注数据，但只学到"词义"，学不到"句法/指代/语义角色"等高阶语言知识。
> BERT 的回答：先在海量无标注文本上做**预训练**（自监督：掩盖 15% 的词，让模型用双向上下文猜出来），把语言知识压缩进参数；再在少量标注数据上**微调**（加一个任务头，端到端小成本训练）。同一个预训练模型可以适配分类、NER、问答等几乎所有任务——这就是"预训练 + 微调"范式。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：BERT 是 Encoder-only 预训练的标杆（[[GPT系列]] 是 Decoder-only 对照）；HW05 的 MinBERT 直接复用其结构与 MLM 预训练概念；理解 BERT 才能理解 [[HuggingFace生态系统]] 里 `AutoModel` 的行为。
- **实际应用场景**：文本分类/情感分析（SST-2）、NER、问答（SQuAD）、语义相似度（STS）、检索排序（BERT 作为 reranker）；工业界大量"BERT 微调"服务。
- **高频题型/任务**：HW05 微调 SST-2（验收 Acc）；面试问"MLM 为什么掩盖 15%""为什么 [MASK] 要部分替换为原词/随机词""NSP 有什么用、RoBERTa 为什么去掉它""BERT 与 GPT 结构差异"。

---

## 3. 学它之前需要哪些前置知识？

1. **[[Transformer架构]]**：BERT = 多层双向 Transformer 编码器，子层全部复用。
2. **[[文本预处理]]**：WordPiece 分词（BERT 的 tokenizer）把词切成子词，解决 OOV。
3. **[[Self-Attention自注意力机制]]**：双向注意力（无因果 mask）是 BERT 与 GPT 的结构分界。

---

## 4. 用直觉语言解释它

> «"BERT 像一个'完形填空'高手：预训练阶段，把句子随机挖掉 15% 的词（盖上 [MASK]），让它根据左右两边猜被挖掉的词——猜得越准，说明它对语言的把握越深。它还要做'两句配对'判断：这两句话是前后文吗？练完后，它的'大脑'（参数）里装满了语法、常识和语义知识；到了新任务（比如判断电影评论是好是坏），只需在头顶加一个小'分类帽'（任务头），用少量标注数据稍加训练就行。"»

- **直觉类比/几何图像**：预训练 = "通识教育"，微调 = "岗前培训"。MLM 的"双向"是关键：猜 'bank' 时能同时看到 'river'（左边）和 'money'（右边），所以学到的表示比单向 GPT 更全面。
- **为什么很自然**：人类学语言也是"从上下文推断词义"；完形填空是语文课的经典题型——把教学法搬进损失函数。
- **一句话直觉本质**：**在无限无标注文本上用"双向完形填空（MLM）+ 句对关系（NSP）"自监督预训练，再用小标注数据微调，实现语言知识的迁移复用。**

---

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义
**BERT（Devlin et al., 2018）**：多层双向 Transformer 编码器。输入 = token 嵌入 + 段嵌入 + 位置嵌入；两个预训练任务：**MLM**（掩码语言模型）与 **NSP**（下一句预测）。输出 [CLS] 位置的表示用于分类，各 token 表示用于序列标注。

### 2. 核心公式
**MLM 损失**（$\mathcal{M}$ 为被掩码位置集合，$x_i$ 为被掩码 token）：
$$\mathcal{L}_{\text{MLM}} = -\sum_{i\in\mathcal{M}} \log P(x_i \mid x_{\setminus\mathcal{M}})$$

**NSP 损失**（二分类：B 是否是 A 的下一句）：
$$\mathcal{L}_{\text{NSP}} = -\log P(\text{IsNext} \mid [\text{CLS}]_A [\text{SEP}]_B)$$

**微调**（以分类为例，$W_c$ 为任务头）：
$$P(y \mid X) = \text{softmax}(W_c \cdot h_{[\text{CLS}]})$$

**掩码策略**（15% 选中 token 中）：80% 换 [MASK]，10% 换随机词，10% 保留原词（缓解预训练/微调不一致）。

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\mathcal{M}$ | 掩码位置集合 | 15% 的 token | 每句随机 |
| $[\text{CLS}]$ | 分类标志 token | 序列首位 | 表示聚合 |
| $[\text{SEP}]$ | 分隔 token | 句间/句尾 | 两句输入用 |
| $h_{[\text{CLS}]}$ | CLS 位置最终表示 | $\mathbb{R}^{d}$ | 微调任务头输入 |
| $L$ | 层数 | base: 12 | 参数量 110M |
| $d$ | 隐藏维度 | base: 768 | |

### 4. 常见变体与适用条件
- **RoBERTa**：去掉 NSP + 动态掩码 + 更大 batch/数据，效果超越 BERT（见 [[04-Transformer与预训练模型/RoBERTa|RoBERTa]]）。
- **ALBERT**：参数共享（跨层）+ 嵌入分解，参数量大减、速度提升（见 [[04-Transformer与预训练模型/ALBERT|ALBERT]]）。
- **DistilBERT**：知识蒸馏（学生模型模仿教师输出），体积减 40%、速度 1.6×、保留 97% 效果。
- **ELECTRA**：用"替换词检测"（判别被替换的 token）替代 MLM，计算效率更高。
- **适用条件**：理解类任务优先 BERT 系；生成任务用 GPT/T5 系；资源受限用 DistilBERT/ALBERT；中文场景用 BERT-wwm / Chinese-RoBERTa（全词掩码）。

---

## 6. 推导思路和思想来源

- **最初困难**：ELMo/GPT 已证明预训练有效，但 ELMo 是"浅层拼接"、GPT 是"单向"——无法同时利用左右上下文。
- **直接方法局限**：双向 LM 有"窥视"问题：普通双向 LM 中，预测 $x_i$ 时模型能直接看到 $x_i$ 本身（目标泄漏），学不到东西。
- **关键"转念"**：把 15% 的词**挖掉**再预测（MLM）——目标 token 不再出现在输入里，双向上下文就安全了。这是"denoising autoencoder"思想在语言上的应用。NSP 则是为了学句间关系（问答/推理任务需要）。
- **推导主线与动机**：① 挖词 → 双向预测（MLM）；② 句对任务（NSP）；③ 预训练完成后，任务头 + 微调；④ 后续变体逐项消融：RoBERTa 证明 NSP 没用、动态掩码更好；ALBERT 压缩参数；DistilBERT 蒸馏。
- **为什么自然得到此结论**：因为"语言理解 = 词义 + 句法 + 句间关系"，MLM 覆盖前三者、NSP 覆盖句间关系；变体的演进就是"用消融实验逐个检验每个设计是否必要"。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）
- **题目**：句子 "I love [MASK] processing"，词表 {NLP, hate, the}，模型输出的 logits 为 [2.0, 0.5, -1.0]，求 MLM 的交叉熵损失（正确答案 NLP）。
- **解题思路与关键步骤**：softmax：$e^2/(e^2+e^{0.5}+e^{-1}) \approx 7.389/(7.389+1.649+0.368) \approx 0.786$。损失 $= -\log 0.786 \approx 0.241$。
- **最终答案**：$\mathcal{L} \approx 0.241$（nats）。
- **易错点**：忘记对全词表归一化；NSP 与 MLM 的损失在预训练中是加和（$\mathcal{L} = \mathcal{L}_{\text{MLM}} + \mathcal{L}_{\text{NSP}}$）。
- **🤔 追问**：如果正确答案是 "the"（logits -1.0）呢？—— 损失 $= -\log 0.039 \approx 3.24$，比正确答案大 13 倍——模型会被强烈惩罚，这正是梯度信号。

### 例子 2：中等例子（条件判断与多步推理）
- **题目**：解释 80/10/10 掩码策略：为什么不是 100% 换 [MASK]？
- **解题思路与完整解答**：预训练时模型见过大量 [MASK]，但微调/推理时输入**没有** [MASK]——分布不一致（类似 teacher forcing 的 exposure bias）。10% 换随机词迫使模型"不信任输入中的任何词、必须依赖上下文"（防模型只记原词）；10% 保留原词迫使模型"即使没被掩盖也要输出正确词"（防模型只把 [MASK] 当信号）。全 [MASK] 会让模型对 [MASK] 过度特化。
- **易错点**：把 80/10/10 记成 80/20；或以为掩码比例 15% 是每句固定 15 个词（是 15% 的 token 数，按句随机）。

### 例子 3：实际应用例子（真实场景/代码）
- **实际价值与转化**：HW05 微调 SST-2：`bert-base-uncased` → 分类头 → 评测 Acc。代码形态（transformers 版，HW05 L1 档）：
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

def tok(batch):
    return tokenizer(batch["sentence"], padding="max_length", truncation=True, max_length=128)

ds = load_dataset("glue", "sst2").map(tok, batched=True)
trainer = Trainer(
    model=model,
    args=TrainingArguments(output_dir="./sst2", num_train_epochs=3, eval_strategy="epoch"),
    train_dataset=ds["train"], eval_dataset=ds["validation"],
)
trainer.train()
# 验收：trainer.evaluate() 的 eval_accuracy >= 78%（L1）
```

---

## 8. 常见误区和易混概念

### 误区 1：以为"BERT 的 [MASK] 在推理时也要用"
- **错误直觉**：既然预训练用 [MASK]，微调和推理也要插入 [MASK]。
- **为什么错**：微调/推理输入是自然句子，没有掩码；模型在预训练中已通过 10% 保留策略学会"无掩码也要正常输出"。这正是 80/10/10 设计的目的。
- **正确理解**：[MASK] 只是预训练的数据增强手段，不出现在下游输入。

### 误区 2：以为"BERT 的表示是上下文无关的，和 Word2Vec 一样"
- **错误直觉**：BERT 的输出向量就是词的静态向量，可以离线算好存起来。
- **为什么错**：BERT 输出**依赖整个上下文**——同一词 "bank" 在 "river bank" 和 "money bank" 中向量完全不同（这才是 BERT 的核心优势）。预计算静态向量会丢失上下文信息（除非用 [CLS] 或 pooling 的句子级表示做嵌入缓存）。
- **正确理解**：BERT 是上下文相关表示；静态缓存只适合句子级嵌入。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| BERT（本概念） | 双向预训练 | MLM + NSP、Encoder-only | 理解类任务（HW05） |
| GPT | 单向预训练 | 自回归 LM、Decoder-only | 生成类任务（见 [[GPT系列]]） |
| Word2Vec | 静态词向量 | 上下文无关 | 嵌入层初始化 |
| ELMo | 浅层双向 | 双向 LSTM 拼接、非微调 | 预训练早期 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[Transformer架构]]：BERT 的结构本体（Encoder 栈）。
- [[Self-Attention自注意力机制]]：双向注意力是 MLM 的机制基础。

### 下游延伸
- [[GPT系列]]：另一预训练范式的对照。
- [[HuggingFace生态系统]]：用 `AutoModel`/`Trainer` 微调 BERT 的工程路径。
- [[文本分类与情感分析]]：微调 BERT 是 HW02 的进阶终点。

### 横向关联
- [[BERT与GPT对比]] ↔ 本知识点：结构、任务、适用场景的系统对照（已有笔记）。
- [[04-Transformer与预训练模型/BERT\|BERT（原子卡）]]、[[04-Transformer与预训练模型/RoBERTa\|RoBERTa]]、[[04-Transformer与预训练模型/ALBERT\|ALBERT]]、[[04-Transformer与预训练模型/ELECTRA\|ELECTRA]] ↔ 本知识点：变体原子卡。
- [[04-Transformer与预训练模型/BERT-wwm\|BERT-wwm]]：中文全词掩码变体。

### 应用场景
- [[🧭 开源作业体系-NLP全栈|开源作业体系]]：HW05 微调验收。
- [[NLP全栈 - HW05：Transformer 与 MinBERT 从零手撕阶梯作业|HW05 阶梯作业]]：L1-L4 四档目标。

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
- [ ] 1. 用一句话说清楚它解决什么问题。
- [ ] 2. 用直觉语言解释它（«"完形填空高手…"»）。
- [ ] 3. 写出 MLM 与 NSP 的损失。
- [ ] 4. 写出 80/10/10 掩码策略。
- [ ] 5. 解释 $\mathcal{M}$、[CLS]、[SEP]、$h_{[CLS]}$ 的含义。
- [ ] 6. 讲出"目标泄漏 → 挖词预测"的推导主线。
- [ ] 7. 手算一个 MLM 位置的交叉熵。
- [ ] 8. 说出两个常见误区。
- [ ] 9. 说出它与 RoBERTa、ALBERT、DistilBERT 的关系。
- [ ] 10. 说出 HW05 的微调验收方式。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | MLM 与 NSP 的职责 |
| 2 | 公式运用 | 基础 | MLM 交叉熵手算 |
| 3 | 条件判断 | 中等 | 掩码策略 80/10/10 的原因 |
| 4 | 变式/综合 | 中等 | RoBERTa 为什么去掉 NSP |
| 5 | 开放/证明/建模 | 较难 | 设计一个低资源场景的 BERT 替代方案 |

### 题目与解析

#### 1. BERT 的两个预训练任务分别学什么？
> [!question]- 答案解析
> - **答案**：MLM 学"词级双向上下文理解"（掩码词预测）；NSP 学"句间关系"（下一句判断）。
> - **解析**：MLM 覆盖词义/句法/指代，NSP 服务问答与推理类任务；RoBERTa 消融证明 NSP 对大多数任务无益后被移除。
> - **易错原因**：把 NSP 说成"预测下一句内容"——它是二分类（IsNext/NotNext），不生成句子。
> - **Obsidian 标签建议**：`#自测题/基础`

#### 2. logits=[1.5, 0.0, -1.5]，词表 {cat, dog, bird}，正确答案 dog，求 MLM 损失。
> [!question]- 答案解析
> - **答案**：$e^{1.5}\approx4.482$，$e^0=1$，$e^{-1.5}\approx0.223$，和 $\approx5.705$；$P(\text{dog})=1/5.705\approx0.175$；$\mathcal{L}=-\log0.175\approx1.741$。
> - **解析**：softmax 归一化后取目标词概率的负对数。
> - **易错原因**：直接用 logit 0.0 当概率；忘记归一化。
> - **Obsidian 标签建议**：`#自测题/基础`

#### 3. 为什么掩码 token 中要保留 10% 原词、替换 10% 随机词？
> [!question]- 答案解析
> - **答案**：① 10% 随机词：迫使模型依赖上下文而非输入本身（防"抄答案"）；② 10% 保留原词：让模型学会"即使没有 [MASK] 也要正确预测"（缓解预训练/微调分布不一致）。
> - **解析**：如果 100% 换 [MASK]，模型会把 [MASK] 当成"必须预测"的开关，下游无掩码输入时行为退化。
> - **易错原因**：只答"防止泄漏"，漏掉分布一致性动机。
> - **Obsidian 标签建议**：`#自测题/中等`

#### 4. RoBERTa 相对 BERT 做了哪些关键改动？为什么有效？
> [!question]- 答案解析
> - **答案**：① 去掉 NSP（消融证明无益甚至有害）；② 动态掩码（每次 epoch 重新掩码）；③ 更大 batch、更长训练、更多数据；④ 用 byte-level BPE。效果提升主要来自数据与训练时长，结构本身几乎不变。
> - **解析**：BERT 的 110M 参数在更大数据上"欠训练"，RoBERTa 证明"同结构 + 更多数据/更长训练"即可超越；NSP 被移除是因为 MLM 已隐式包含句间信息（单句训练时）。
> - **易错原因**：把 RoBERTa 的提升归功于结构创新——它几乎没改结构。
> - **Obsidian 标签建议**：`#自测题/中等`

#### 5. 只有一张消费级 GPU（8GB 显存），要做一个中文情感分类服务，如何选模型与策略？给出方案与理由。
> [!question]- 答案解析
> - **答案**：方案：① 选轻量中文模型：`bert-base-chinese`（约 110M，fp16 下 8GB 可微调）或 `distilbert-base-chinese` / `albert_chinese_tiny`（更省）；② 冻结大部分层只微调顶层 + 分类头（或 LoRA/Adapter，见 [[参数高效微调PEFT]]）；③ 数据增强 + 更小 max_length（128 截断）；④ 用 `Trainer` + `fp16=True` 与梯度累积。
> - **解析**：8GB 显存微调 110M 模型可行（batch 16、seq 128、fp16）；参数量与显存的关键是 batch×seq×d；蒸馏模型（DistilBERT）是效果/资源最优平衡；PEFT 可把可训练参数降到 1% 以下。
> - **易错原因**：直接上 340M 的 RoBERTa-large；或忘记截断长度与 fp16。
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
- **关联已有笔记**：[[🧭 开源作业体系-NLP全栈]]、[[BERT与GPT对比]]、[[04-Transformer与预训练模型/BERT|BERT]]、[[04-Transformer与预训练模型/RoBERTa|RoBERTa]]、[[04-Transformer与预训练模型/ALBERT|ALBERT]]、[[04-Transformer与预训练模型/ELECTRA|ELECTRA]]、[[04-Transformer与预训练模型/BERT-wwm|BERT-wwm]]、[[04-Transformer与预训练模型/Chinese-RoBERTa|Chinese-RoBERTa]]
- **建议标签**：`#学习` `#NLP全栈` `#BERT` `#预训练` `#概念`
- **拆分建议**：母卡保留；HW05 微调踩坑（学习率、warmup、显存）可拆错题笔记。
