---
type: index
topic: "⚡ Transformer维度"
course: "NLP全栈"
tags: [索引, NLP全栈, 知识地图]
flow: knowledge
kind: moc
created: 2026-08-03
---

# ⚡ Transformer维度

> "注意力即一切"——从自注意力到预训练模型家族，现代 NLP 的地基维度。

## 🧭 维度定位

- **核心思想**：完全去掉循环，用 Self-Attention 实现并行 + 全局建模；预训练 + 微调成为标准范式。
- **主线脉络**：[[Transformer架构]] → [[BERT及其变体]] / [[GPT系列]] → [[参数高效微调PEFT]]。
- **对应阶段**：第四阶段《Transformer与预训练模型》，承接 [[🧠 深度学习维度]]，通向 [[🚀 LLM前沿维度]]。

## 📋 主题笔记清单

- [[Transformer架构]]：Self-Attention、多头注意力、位置编码与残差/LayerNorm 的完整拆解（本维度主卡）。
- [[Self-Attention自注意力机制]]：QKV 打分-加权范式的快速记忆卡。
- [[🎯 RoPE 旋转位置编码 (Rotary Position Embedding)]]：现代 LLM 的主流相对位置编码。
- [[BERT及其变体]]：MLM 预训练范式与 RoBERTa/ALBERT/ELECTRA/DeBERTa 家族。
- [[GPT系列]]：自回归生成路线，从 GPT-1 到 GPT-3 的能力跃迁。
- [[其他预训练模型]]：T5、XLNet 等架构变体与多任务预训练。
- [[参数高效微调PEFT]]：Adapter、Prompt/Prefix Tuning、LoRA 等低成本微调。
- [[HuggingFace生态系统]]：transformers 工具链与模型库使用。
- [[BERT与GPT对比]]：编码器 vs 解码器两大路线的系统对照。

## 🔗 维度导航

- [[🗺️ NLP全栈学习路径|返回学习路径总览]]
- 姊妹维度：[[🔢 数学基础维度]] · [[📜 传统方法维度]] · [[🧠 深度学习维度]] · [[🚀 LLM前沿维度]] · [[🎯 专业应用维度]]
