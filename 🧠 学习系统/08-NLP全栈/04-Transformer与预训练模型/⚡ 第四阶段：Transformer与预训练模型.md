---
type: stage
topic: 第四阶段：Transformer 与预训练模型 (The Transformer Era)
tags:
- NLP
- Transformer
- BERT
- GPT
- T5
- PEFT
- LoRA
created: 2026-04-11
status: planned
difficulty: intermediate
concept: []
prerequisites: []
related: []
phase: 4
---

# ⚡ 第四阶段：Transformer 与预训练模型 (The Transformer Era)

> "Attention is all you need. 这一句话开启了NLP的新纪元。"

---

## 📊 阶段进度

```dataviewjs
const total = dv.pages('"🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型"').length - 1;
const completed = dv.pages('"🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型"').where(p => p.status === "completed").length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**阶段进度: ${progress}%** (${completed}/${total} 模块)`);
```

---

## ⚡ Transformer 深度拆解

### 自注意力 (Self-Attention)

| 概念 | 公式 | 意义 | 状态 | 笔记 |
|:---|:---|:---:|:---:|:---|
| **Q/K/V** | Query/Key/Value | 三个投影 | ⬜ | [[QKV]] |
| **注意力分数** | QK^T/√d_k | 相似度计算 | ⬜ | [[注意力分数]] |
| **Softmax+加权** | softmax(QK^T/√d_k)V | 加权求和 | ⬜ | [[Attention输出]] |
| **复杂度** | O(n²d) | 序列长度瓶颈 | ⬜ | [[Attention复杂度]] |

### 多头注意力

| 概念 | 内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **多头** | h组独立注意力 | ⬜ | [[多头注意力]] |
| **拼接投影** | Concat(head_1,...,head_h)W^O | ⬜ | [[多头拼接]] |
| **意义** | 不同子空间表示 | ⬜ | [[多头意义]] |

### 位置编码

| 类型 | 方法 | 特点 | 状态 | 笔记 |
|:---|:---|:---:|:---:|:---|
| **绝对位置编码** | sin/cos函数 | Transformer原版 | ⬜ | [[正弦位置编码]] |
| **可学习位置编码** | 嵌入层 | BERT使用 | ⬜ | [[可学习位置编码]] |
| **RoPE** | 旋转位置编码 | 相对位置 | ⬜ | [[RoPE]] |
| **ALiBi** | 线性偏置 | 外推性好 | ⬜ | [[ALiBi]] |

### 残差连接与 LayerNorm

| 组件 | 作用 | 位置 | 状态 | 笔记 |
|:---|:---|:---:|:---:|:---|
| **残差连接** | 梯度流动 | 子层前后 | ⬜ | [[残差连接]] |
| **LayerNorm** | 稳定训练 | 子层后 | ⬜ | [[🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型/LayerNorm|LayerNorm]] |
| **Pre/Post Norm** | 归一化位置 | 两种变体 | ⬜ | [[PrePostNorm]] |

### Transformer 整体架构

| 组件 | Encoder | Decoder | 状态 | 笔记 |
|:---|:---:|:---:|:---:|:---|
| **自注意力** | ✓ (双向) | ✓ (因果) | ⬜ | [[Transformer注意力]] |
| **交叉注意力** | ✗ | ✓ | ⬜ | [[交叉注意力]] |
| **前馈网络** | ✓ | ✓ | ⬜ | [[FFN]] |

---

## 🏗️ 预训练范式

### BERT 家族

| 模型 | 改进点 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **BERT** | MLM+NSP | ⬜ | [[BERT]] |
| **RoBERTa** | 去掉NSP，更多数据 | ⬜ | [[RoBERTa]] |
| **ALBERT** | 参数共享，因子化嵌入 | ⬜ | [[ALBERT]] |
| **ELECTRA** | 判别式预训练 | ⬜ | [[ELECTRA]] |
| **DeBERTa** | 解耦注意力 | ⬜ | [[DeBERTa]] |

### GPT 系列

| 版本 | 特点 | 规模 | 状态 | 笔记 |
|:---|:---|:---:|:---:|:---|
| **GPT-1** | 生成式预训练 | 117M | ⬜ | [[GPT-1]] |
| **GPT-2** | 更大规模 | 1.5B | ⬜ | [[GPT-2]] |
| **GPT-3** | 上下文学习 | 175B | ⬜ | [[GPT-3]] |

### T5 架构

| 特点 | 内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **统一框架** | 所有任务转为text-to-text | ⬜ | [[T5]] |
| **Span Corruption** | 连续掩码 | ⬜ | [[T5预训练]] |

### 中文特定预训练模型

| 模型 | 特点 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **MacBERT** | 纠正BERT中文问题 | ⬜ | [[MacBERT]] |
| **BERT-wwm** | 全词掩码 | ⬜ | [[BERT-wwm]] |
| **Chinese-RoBERTa** | 中文优化 | ⬜ | [[Chinese-RoBERTa]] |

---

## 🔧 微调技术 (PEFT)

### LoRA

| 概念 | 内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **思想** | 低秩适配 | ⬜ | [[🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型/LoRA|LoRA]] |
| **公式** | W = W_0 + BA | ⬜ | [[LoRA公式]] |
| **优势** | 参数量极少 | ⬜ | [[LoRA优势]] |

### 其他PEFT方法

| 方法 | 思想 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **Adapter** | 插入小模块 | ⬜ | [[Adapter]] |
| **Prefix-Tuning** | 前缀嵌入 | ⬜ | [[Prefix-Tuning]] |
| **P-Tuning** | 连续提示 | ⬜ | [[P-Tuning]] |
| **Prompt-Tuning** | 软提示 | ⬜ | [[Prompt-Tuning]] |

---

## 🔗 阶段导航

| ⬅️ 上一阶段 | 📋 总览 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| [[🧠 第三阶段：深度学习NLP基础\|返回第三阶段]] | [[🗺️ NLP全栈学习路径\|返回总览]] | [[🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型/🚀 第五阶段：大语言模型与前沿技术|进入第五阶段]] |

---

*阶段创建：2026-04-11*
