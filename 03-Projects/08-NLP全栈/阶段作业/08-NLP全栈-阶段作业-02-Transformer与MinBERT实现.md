---
type: project
kind: project
track: 机器学习与AI应用
project_type: homework
course: "08-NLP全栈"
assignment_id: "08-NLP全栈-HW03"
assignment_level: stage
assignment_format: project
stage_id: "04"
requires: ["[[08-NLP全栈-Self-Attention自注意力机制]]", "[[08-NLP全栈-Transformer架构]]", "[[08-NLP全栈-BERT模型]]"]
source_type: official_assignment
source: "Stanford CS224n Assignment 5: MinBERT and Downstream Tasks"
source_url: "https://github.com/stanfordnlp/cs224n-assignments/tree/master/assignment5"
created: 2026-08-06
status: active
flow: project
tags: [作业, NLP, Transformer, MinBERT, SST-2]
assessment_exempt: false
---

# 08-NLP全栈-阶段作业-02-Transformer与MinBERT实现

> ⏱ **预计完成耗时**：5 小时  
> 🎯 **对应阶段**：阶段 4 - Transformer 与预训练模型阶段综合作业

---

## 🎯 学习目标

1. 参考 Stanford CS224N MinBERT 官方实践，从零手写补全 Transformer Encoder 架构的核心算子。
2. 掌握 Multi-Head Self-Attention (MHSA) 4D 张量（`[B, H, L, D]`）变换逻辑与 Mask 处理。
3. 掌握 BERT 预训练权重的加载映射，在 SST-2 情感分类任务上完成 Fine-tuning。

---

## 🚧 任务边界

- **包含**：`BertSelfAttention`、`BertLayer`、`BertEncoder` 算子实现、Embedding 加和、权重加载与 SST-2 微调。
- **不包含**：从零大规模 Pre-training、Decoder-only 架构的 KV Cache 优化。

---

## 📋 任务具体要求与维度规范

学员必须在配套的代码文件或 Notebook 中完成以下模块的编写，并确保满足维度转换约束：

```text
[维度流向规范]
输入 Tensor: [Batch, Seq_Len]
   │
[ Embedding Layer (Token + Position + Segment) ] -> [B, L, 768]
   │
┌──▼────────────────────────────────────────────┐
│ BertSelfAttention                              │
│  Q, K, V Projection -> [B, L, 768]             │
│  View & Transpose -> [B, H=12, L, D=64]        │
│  Scores = Q @ K^T / sqrt(64) -> [B, 12, L, L]  │
│  Softmax + Dropout                             │
│  Out = Scores @ V -> [B, 12, L, 64]            │
│  Transpose & Contiguous & View -> [B, L, 768]  │
└──┬────────────────────────────────────────────┘
   │
[ BertIntermediate & BertOutput (FFN) ]          -> [B, L, 768]
   │
[ Pooler Layer & Linear Classifier ]             -> [B, Num_Classes]
```

### 1. `BertSelfAttention` 算子实现
- 输入：`hidden_states` $[B, L, 768]$，`attention_mask` $[B, 1, 1, L]$ 或 $[B, 1, L, L]$
- 计算过程：
  1. 将输入线性投影为 $Q, K, V$ 三个矩阵。
  2. 重塑为多头维度 $[B, 12, L, 64]$。
  3. 计算注意力分数矩阵 $\frac{Q K^T}{\sqrt{64}}$，并应用 `attention_mask`（将被 Mask 位置用 `-1e9` 填满）。
  4. 使用 `F.softmax` 计算权重，与 $V$ 做矩阵乘法后拼接恢复 $[B, L, 768]$。

### 2. `BertLayer` 与 `BertEncoder` 堆叠
- 正确应用 Pre-LN / Post-LN 与 Residual Connection 残差连接：`x = x + self.dropout(attn_out)`。
- 堆叠 12 层 `BertLayer` 构成完整编码器。

### 3. SST-2 情感分类微调 (Fine-tuning)
- 加载 `bert-base-uncased` 预训练权重。
- 构建 AdamW 优化器（$\text{lr} = 2 \times 10^{-5}$，使用 Linear Warmup 调度器）。
- 在 SST-2 验证集上评估分类准确率。

---

## 📦 提交产物

1. `scripts/minbert.py`：完整的 `BertSelfAttention`, `BertLayer`, `BertModel` 源码实现。
2. `scripts/classifier.py`：SST-2 情感分类器微调训练与评估脚本。
3. `reports/stage02_report.md`：SST-2 验证集 Accuracy 评估结果与消融实验对比。

---

## ⚖️ 验收标准 (Rubric)

| 评分标准 (总分 100) | 提交标准与验收条件 | 对应代码与验证文件 |
|:---|:---|:---|
| **基础项 (60 分)** | 正确实现 `BertSelfAttention` 与 `BertLayer` 算子；通过本地 `test_minbert_standalone.py` 单元测试断言。 | `03-Projects/08-NLP全栈/scripts/test_minbert_standalone.py` |
| **进阶项 (85 分)** | 成功加载预训练权重并在 SST-2 数据集上完成微调，验证集分类准确率 $\ge 85\%$。 | 提交完整的 Training & Evaluation 运行脚本与 Log |
| **优秀项 (100 分)** | 扩展实现 RoPE (旋转位置编码) 优化，或在 MNLI 跨领域自然语言推理数据集上测试泛化 Acc $\ge 82\%$。 | 提交对比消融实验报告与准确率变化曲线图 |

---

## 🔍 引导与自检

- [ ] 多头拼接恢复维度时是否调用了 `.contiguous().view(B, L, C)`？
- [ ] 维度重塑 `[B, L, H, D]` 转置为 `[B, H, L, D]` 时是否避免了直接 `.view()` 造成的维度混淆？
- [ ] Attention Mask 扩展填充值是否采用了负无穷小（如 `-10000.0`）避免 Softmax 梯度 NaN？

---

## 🧪 本地自动化测试命令

在项目根目录下，运行以下脚本验证你实现的算子：

```bash
python 03-Projects/08-NLP全栈/scripts/test_minbert_standalone.py
```
