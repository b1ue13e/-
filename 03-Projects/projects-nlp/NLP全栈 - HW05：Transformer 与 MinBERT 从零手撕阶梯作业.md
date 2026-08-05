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

> 🧠 **架构规约 (Architecture Contract)**：在开始写代码前，请先明确本作业采用 **Post-LN** 还是 **Pre-LN**（原版 BERT 使用 Post-LN，但在某些变体中 Pre-LN 更易收敛），并在你的代码注释中声明。必须手绘一份 `Q, K, V` 从生成到裂变 `[Batch, Heads, Seq_Len, D_k]` 的张量流转图作为前置检查点。

| 梯度级别 | 目标 GLUE SST-2 Acc | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | Acc ≥ 78.0% | 使用 HuggingFace `AutoModelForSequenceClassification` 加载预训练 `bert-base-uncased` 跑通评测。 |
| 🟡 **L2 - Medium Baseline** | Acc ≥ 83.5% | **手写 Self-Attention 模块**：实现 $Q, K, V$ 维度映射、Scaled Dot-Product Attention 与 Padding Mask。 |
| 🔴 **L3 - Strong Baseline** | Acc ≥ 89.0% | **CS224n HW5 模式**：从零用 PyTorch 实现完整 `BertSelfAttention`, `BertLayer`, `BertModel` 与 Classifier Head。 |
| 👑 **L4 - Boss Baseline** | Acc ≥ 89.0% 但训练快 | **手撕 PEFT**：在 L3 刚手写完的 MinBERT (约 110M 参数) 上实现 LoRA 插件。<br><br>**Hint 脚手架**：实现一个 `LoRALinear` 包裹现有的 `nn.Linear`。<br>`__init__`: 冻结原 Linear 参数；初始化 A 矩阵（正态分布）、B 矩阵（全零）；定义缩放系数 `scaling = alpha / r`。<br>`forward`: 返回 `base_layer(x) + (x @ A @ B) * scaling`。 |

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
    mask = torch.ones(2, 1, 1, 16) # (batch, 1, 1, seq_len) padding mask
    mask[0, 0, 0, -2:] = 0 # 模拟第一个 batch 的最后两个 token 被 pad 掉了
    
    out, weights = attn(Q, K, V, mask)
    assert out.shape == (2, 8, 16, 64)
    assert torch.allclose(weights.sum(dim=-1), torch.ones(2, 8, 16)), "Attention 权重每一行 Softmax 之和必须为 1"
    assert torch.allclose(weights[0, :, :, -2:], torch.zeros_like(weights[0, :, :, -2:])), "被 Mask 的位置概率必须趋近于 0"
```

---

## 🛠️ 排错避风港 (Debugging Heuristics)

> 当你被 Bug 卡住时，严禁无脑改代码，请先对照下表排查：

- **Failure Mode 1: Loss 一直降不下去或震荡**
  - 👉 检查 (1) Attention 分数是否除以了 $\sqrt{d_k}$；(2) 学习率是否过大，BERT 从零训练通常需要 Warmup。
- **Failure Mode 2: Loss 突然变成 NaN**
  - 👉 检查 Padding Mask 中填充的极小值，是用 `-1e9` 还是 `-inf`？如果用 `-inf`，在某些 FP16 混合精度下可能会导致数值溢出。
  - **深层原理解析**：Softmax 的梯度包含对 Mask 位置的偏导。该位置前向概率虽为 0，但反向传播计算梯度时会出现 `0 * -inf`，在 IEEE 浮点标准下这就是 `NaN`，从而毒化整个网络。
  - 🧪 **极简验证脚本**：你可以运行 `import torch; a = torch.tensor([0.0]); b = torch.tensor([-float('inf')]); print(a * b)` 看看结果。
- **Failure Mode 3: 梯度爆炸 / 模型无法收敛**
  - 👉 检查你的 LayerNorm 放在了哪里（Pre-LN 还是 Post-LN），以及残差连接 `x + sublayer(x)` 是否漏掉了 `x`。
  - **理论提示**：原版 BERT 用的 Post-LN 会导致梯度在靠近输入端时急剧消失（期望方差随层数积累变大）；而 Pre-LN 直接将输入沿旁路引至最后一层，梯度流动极其通畅，对 Warmup 不敏感，所以手撕代码时建议首选 Pre-LN。

---

## 🃏 Anki 卡片

- Q: 为何 Self-Attention 中点积后要除以 $\sqrt{d_k}$？
- A: 当 $d_k$ 较大时，点积数值变大，导致 Softmax 梯度落入极小饱和区。除以 $\sqrt{d_k}$ 将方差缩放回 1，使梯度保持平稳。

- Q: 给出 Self-Attention 的核心公式，并与 PyTorch 代码逐行对齐。
- A: 公式：$Attention(Q,K,V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$
  - `scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)`  # (B, H, L, d_k) @ (B, H, d_k, L) -> (B, H, L_q, L_k)
  - `scores = scores.masked_fill(mask == 0, -1e9)` # 应用 Mask 
    - ⚠️ **Shape 陷阱与演化图解**：传入的 padding mask 形状通常是 `(B, L_k)`。必须扩展为 `(B, 1, 1, L_k)`！
    - 为什么是两个 1？第二个 1 广播到所有的 Heads；第三个 1 广播到所有的 Query 位置（因为不管哪个 Query Token 来看，被 Pad 掉的 Key Token 都是不可见的）。这就完美对齐了四维的 `scores` 矩阵。
  - `p_attn = torch.nn.functional.softmax(scores, dim=-1)` # (B, H, L_q, L_k) 此时每一行（一个 Query 对所有 Key 的注意力分配）和为 1。
  - `context = torch.matmul(p_attn, V)` # (B, H, L_q, L_k) @ (B, H, L_k, d_k) -> (B, H, L_q, d_k)

- Q: 为什么 Transformer 必须要有残差连接（Residual Connection）？如果去掉残差，网络能有多深？
- A: 残差连接 `x + sublayer(x)` 为反向传播提供了一条“梯度高速公路”，直接将深层梯度无损传导到浅层，极大地缓解了梯度消失问题。如果没有残差，基于大量乘法和 Softmax 的网络顶多只能训练 4-6 层就会停止学习，而有了残差可以轻松堆叠数十上百层。
