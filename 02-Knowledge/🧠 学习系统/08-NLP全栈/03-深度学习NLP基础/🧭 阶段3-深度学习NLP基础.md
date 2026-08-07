---
type: study
topic: "第三阶段：深度学习NLP基础 (Deep Learning for NLP)"
course: "08-NLP全栈"
created: 2026-08-06
status: active
flow: knowledge
kind: moc
tags: [学习, NLP, MOC, 深度学习]
sources: ['Stanford CS224N: Deep Learning for NLP', 'Jurafsky, D., & Martin, J. H. (2024).']
assessment_exempt: true
assessment_exempt_reason: 阶段 MOC 导航与学习目标总览页
---

# 🧭 08-NLP全栈 - 阶段 3：深度学习 NLP 基础

> ⏱ **预计完成耗时**：8 小时  
> 🎯 **阶段目标**：掌握 Word2Vec、GloVe 词嵌入、RNN/LSTM/GRU 序列建模、Seq2Seq 架构与 Bahdanau 注意力机制。

---

## 🧭 为什么现在学 & 学习顺序

分布表征（Dense Embeddings）与循环神经网络彻底改变了 NLP 领域。掌握 Seq2Seq + Attention 机制是通往 Transformer 的直接前置桥梁。
按以下顺序学习：
1. [[08-NLP全栈-词向量与Word2Vec|词向量与Word2Vec]]：Skip-gram, CBOW 与 Negative Sampling
2. [[08-NLP全栈-GloVe与稠密向量|GloVe与稠密向量]]：全局矩阵分解与词向量对齐
3. [[08-NLP全栈-CNN在NLP中的应用|CNN在NLP中的应用]]：TextCNN 与局部 n-gram 特征抽取
4. [[08-NLP全栈-循环神经网络RNN|循环神经网络RNN]]：RNN, LSTM, GRU 与梯度消失/爆炸
5. [[08-NLP全栈-Seq2Seq与注意力机制|Seq2Seq与注意力机制]]：Encoder-Decoder 架构与 Bahdanau/Luong Attention
6. [[08-NLP全栈-Attention计算|Attention计算]]：加法、点积与缩放点积注意力打分
7. [[08-NLP全栈-文本分类与情感分析|文本分类与情感分析]]：端到端深度文本分类模型
8. [[08-NLP全栈-数据集与评测指标|数据集与评测指标]]：Accuracy, F1, Perplexity, BLEU, ROUGE

---

## 📚 本阶段有序知识卡清单

- 1️⃣ [[08-NLP全栈-词向量与Word2Vec]]
- 2️⃣ [[08-NLP全栈-GloVe与稠密向量]]
- 3️⃣ [[08-NLP全栈-CNN在NLP中的应用]]
- 4️⃣ [[08-NLP全栈-循环神经网络RNN]]
- 5️⃣ [[08-NLP全栈-Seq2Seq与注意力机制]]
- 6️⃣ [[08-NLP全栈-Attention计算]]
- 7️⃣ [[08-NLP全栈-文本分类与情感分析]]
- 8️⃣ [[08-NLP全栈-数据集与评测指标]]

---

## 🧪 阶段验收与作业

- **关联作业 1**：[[08-NLP全栈-课后作业-01-词向量与文本表征|课后作业-01-词向量与文本表征]]
- **关联阶段作业**：[[08-NLP全栈-阶段作业-01-RNN与Seq2Seq注意力|阶段作业-01-RNN与Seq2Seq注意力]]
- **通过标准**：在 Multi30k 翻译任务中独立运行 BiLSTM+Seq2Seq 模型达到 BLEU $\ge 25.0$。

```dataview
TABLE assignment_id AS "ID", assignment_level AS "层级", status AS "状态"
FROM "03-Projects/08-NLP全栈"
WHERE stage_id = "03"
```

---

## 🔗 阶段导航

| ⬅️ 上一阶段 | 📋 课程主路径 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| [[02-传统NLP方法/🧭 阶段2-传统NLP方法\|阶段 2：传统NLP方法]] | [[02-Knowledge/🧠 学习系统/08-NLP全栈/🗺️ 08-NLP全栈学习路径\|08-NLP全栈学习路径]] | [[04-Transformer与预训练模型/🧭 阶段4-Transformer与预训练模型\|阶段 4：Transformer与预训练]] |
