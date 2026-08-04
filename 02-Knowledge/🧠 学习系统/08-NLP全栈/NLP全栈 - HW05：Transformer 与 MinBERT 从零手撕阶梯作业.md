---
title: "NLP全栈-题型-Transformer与MinBERT手撕阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "NLP全栈作业"
course: "08-NLP全栈"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["Transformer", "Self-Attention", "BERT"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/17-机器学习/🗺️ 机器学习学习路径|机器学习]]"]
related: ["[[机器学习-题型-李宏毅式分类与深层模型阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/17-机器学习/01-基础概念/🌱 第一阶段：基础概念|NLP全栈学习路径]]"]
downstream: []
tags: [学习, 08-NLP全栈, 作业, 实战, 阶梯作业]
aliases: ["CS224n-HW5-MinBERT作业"]
---

# NLP全栈 - HW05：Transformer 与 MinBERT 从零手撕阶梯作业

> 🎯 **作业目标**：手写 Multi-Head Self-Attention、Positional Encoding 与完整 MinBERT 模型，并在 GLUE SST-2 情感分类任务上评测。

---

## 1. ⚙️ Environment & Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-nlp/hw05_minbert.ipynb`
- **开源标杆仓库**：[stanfordnlp/cs224n-winter2023-assignments](https://github.com/stanfordnlp/cs224n-winter2023-assignments)
- **核心依赖**：`torch`, `transformers`, `datasets`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 GLUE SST-2 Acc | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | Acc ≥ 78.0% | 使用 HuggingFace `AutoModelForSequenceClassification` 加载预训练 `bert-base-uncased` 跑通评测。 |
| 🟡 **L2 - Medium Baseline** | Acc ≥ 83.5% | **手写 Self-Attention 模块**：实现 $Q, K, V$ 维度映射、Scaled Dot-Product Attention 与 Causal/Padding Mask。 |
| 🔴 **L3 - Strong Baseline** | Acc ≥ 89.0% | **CS224n HW5 模式**：从零用 PyTorch 实现完整 `BertSelfAttention`, `BertLayer`, `BertModel` 与 Classifier Head。 |
| 👑 **L4 - Boss Baseline** | Acc ≥ 92.5% | 手写 LoRA (Low-Rank Adaptation) 插件，在参数量小于 1% 的限制下微调 8B 语言模型。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import torch

def test_self_attention_shape_and_values():
    from minbert import ScaledDotProductAttention
    attn = ScaledDotProductAttention(d_k=64)
    
    Q = torch.randn(2, 8, 16, 64) # (batch, heads, seq_len, d_k)
    K = torch.randn(2, 8, 16, 64)
    V = torch.randn(2, 8, 16, 64)
    
    out, weights = attn(Q, K, V)
    assert out.shape == (2, 8, 16, 64)
    assert torch.allclose(weights.sum(dim=-1), torch.ones(2, 8, 16)), "Attention 权重每一行 Softmax 之和必须为 1"
```

---

## 🃏 Anki 卡片

- Q: 为何 Self-Attention 中点积后要除以 $\sqrt{d_k}$？
- A: 当 $d_k$ 较小时，点积方差约为 1；当 $d_k$ 较大时，点积数值变大，导致 Softmax 梯度落入极小饱和区。除以 $\sqrt{d_k}$ 将方差缩放回 1，使梯度保持平稳。
