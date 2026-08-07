---
type: study
topic: "第四阶段：Transformer与预训练模型 (Transformer & Pretrained Language Models)"
course: "08-NLP全栈"
created: 2026-08-06
status: active
flow: knowledge
kind: moc
tags: [学习, NLP, MOC, Transformer, BERT, GPT]
sources: ['Vaswani et al. (2017). Attention Is All You Need.', 'Devlin et al. (2019). BERT.']
assessment_exempt: true
assessment_exempt_reason: 阶段 MOC 导航与学习目标总览页
---

# 🧭 08-NLP全栈 - 阶段 4：Transformer 与预训练模型

> ⏱ **预计完成耗时**：10 小时  
> 🎯 **阶段目标**：掌握 Self-Attention、Multi-Head Attention、Transformer Encoder/Decoder 架构、BERT、GPT 系列与 RoPE 相对位置编码。

---

## 🧭 为什么现在学 & 学习顺序

Transformer 是现代大语言模型与 NLP 基础设施的核心技术。理解 Self-Attention 的并行计算与预训练-微调范式是全栈 NLP 学习的最关键枢纽。
按以下顺序学习：
1. [[08-NLP全栈-Self-Attention自注意力机制|Self-Attention自注意力机制]]：$Q, K, V$ 投影与 Scaled Dot-Product
2. [[08-NLP全栈-Transformer架构|Transformer架构]]：Encoder-Decoder, FFN, Pre-LN/Post-LN 与残差连接
3. [[08-NLP全栈-BERT模型|BERT模型]]：Masked LM, Next Sentence Prediction 预训练任务
4. [[08-NLP全栈-BERT及其变体|BERT及其变体]]：RoBERTa, ALBERT, DeBERTa 优化
5. [[08-NLP全栈-BERT与GPT对比|BERT与GPT对比]]：Encoder-only (Autoencoding) vs Decoder-only (Autoregressive)
6. [[08-NLP全栈-GPT系列|GPT系列]]：GPT-1/2/3 生成式预训练原理
7. [[08-NLP全栈-其他预训练模型|其他预训练模型]]：T5, BART, XLNet 序列到序列模型
8. [[08-NLP全栈-HuggingFace生态系统|HuggingFace生态系统]]：Transformers, Datasets, Evaluate 工具库
9. [[08-NLP全栈-RoPE旋转位置编码|RoPE旋转位置编码]]：复数旋转矩阵与相对位置编码

---

## 📚 本阶段有序知识卡清单

- 1️⃣ [[08-NLP全栈-Self-Attention自注意力机制]]
- 2️⃣ [[08-NLP全栈-Transformer架构]]
- 3️⃣ [[08-NLP全栈-FlashAttention与KVCache显存优化]]
- 4️⃣ [[08-NLP全栈-BERT模型]]
- 5️⃣ [[08-NLP全栈-BERT及其变体]]
- 6️⃣ [[08-NLP全栈-BERT与GPT对比]]
- 7️⃣ [[08-NLP全栈-GPT系列]]
- 8️⃣ [[08-NLP全栈-其他预训练模型]]
- 9️⃣ [[08-NLP全栈-HuggingFace生态系统]]
- 🔟 [[08-NLP全栈-RoPE旋转位置编码]]

---

## 🧪 阶段验收与作业

- **关联阶段作业**：[[08-NLP全栈-阶段作业-02-Transformer与MinBERT实现|阶段作业-02-Transformer与MinBERT实现]]、[[08-NLP全栈-课后作业-06-文本分类与评测指标|课后作业-06-文本分类与评测指标]]
- **通过标准**：手写补全 MinBERT 算子并在 SST-2 验证集上微调达到 Acc $\ge 85\%$。

```dataview
TABLE assignment_id AS "ID", assignment_level AS "层级", status AS "状态"
FROM "03-Projects/08-NLP全栈"
WHERE stage_id = "04"
```

---

## 🔗 阶段导航

| ⬅️ 上一阶段 | 📋 课程主路径 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| [[03-深度学习NLP基础/🧭 阶段3-深度学习NLP基础\|阶段 3：深度学习NLP基础]] | [[02-Knowledge/🧠 学习系统/08-NLP全栈/🗺️ 08-NLP全栈学习路径\|08-NLP全栈学习路径]] | [[05-大语言模型与前沿技术/🧭 阶段5-大语言模型与前沿技术\|阶段 5：LLM与前沿技术]] |
