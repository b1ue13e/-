---
type: project
kind: project
track: 机器学习与AI应用
project_type: homework
course: "08-NLP全栈"
assignment_id: "08-NLP全栈-HW02"
assignment_level: stage
assignment_format: lab
stage_id: "03"
requires: ["[[08-NLP全栈-循环神经网络RNN]]", "[[08-NLP全栈-Seq2Seq与注意力机制]]", "[[08-NLP全栈-Attention计算]]"]
source_type: official_assignment
source: "Stanford CS224n Assignment 3: Dependency Parsing & NMT RNN"
source_url: "https://github.com/stanfordnlp/cs224n-assignments/tree/master/assignment3"
created: 2026-08-06
status: planned
flow: project
tags: [作业, NLP, RNN, Seq2Seq, Attention]
assessment_exempt: false
---

# 08-NLP全栈-阶段作业-01-RNN与Seq2Seq注意力

> ⏱ **预计完成耗时**：4 小时  
> 🎯 **对应阶段**：阶段 3 - 深度学习 NLP 基础阶段综合作业

---

## 🎯 学习目标

1. 掌握基于 PyTorch 从零构建基于 Attention 机制的 Seq2Seq 机器翻译/文本生成模型。
2. 深入理解 Bahdanau (加法) 注意力与 Luong (乘积) 注意力的打分函数差异。
3. 掌握 Teacher Forcing 训练策略与 Beam Search 解码算法。

---

## 🚧 任务边界

- **包含**：BiLSTM Encoder、Bahdanau/Luong Attention 模块、Decoder 循环推导、BLEU 指标评估以及 Beam Search 解码器实现。
- **不包含**：Transformer 自注意力层、Large Language Model 权重加载。

---

## 📋 任务分层要求 (基础 / 进阶 / 综合)

### 1. 基础要求
- [ ] 手写双向 LSTM (Bi-LSTM) 编码器，正确映射隐藏状态维度 `[2, B, H]` 至解码器维度 `[1, B, H]`。
- [ ] 实现 Bahdanau 加法注意力计算函数 $e_{ij} = v_a^\top \tanh(W_a s_{i-1} + U_a h_j)$。

### 2. 进阶要求
- [ ] 构建完整的 Encoder-Decoder 神经机器翻译架构，支持 Teacher Forcing Ratio 衰减。
- [ ] 实现 Beam Search 解码器 (Beam Width=5)，维护 Log 概率累加与 EOS 终止判断。

### 3. 综合要求
- [ ] 在 Multi30k 英德翻译数据集上完成完整训练，独立测试集 BLEU Score $\ge 25.0$。

---

## 📦 提交产物

1. `scripts/seq2seq_attention.py`：包含 `EncoderRNN`, `BahdanauAttention`, `Seq2SeqDecoder` 类的完整 PyTorch 代码。
2. `scripts/beam_search.py`：Beam Search 解码器逻辑实现。
3. `reports/stage01_report.md`：训练 Loss 曲线、注意力权重热力图 (Attention Map) 绘制及 BLEU 评估得分报告。

---

## ⚖️ 验收标准 (Rubric)

| 评分项 | 权重 | 通过标准 |
| :--- | :--- | :--- |
| **Attention 维度与实现** | 30% | 广播与点积正确，形状匹配 `[B, 1, SrcLen]`，无矩阵维度错位 |
| **Beam Search 解码** | 30% | 概率累积计算正确，未出现重复节点坍缩，正确在 `<EOS>` 截止 |
| **BLEU 指标与性能** | 40% | 机器翻译测试集 BLEU 得分达到 25.0 以上 |

---

## 🔍 引导与自检

- [ ] 解码时刻 $t$ 的 Query 是否只包含历史状态 $s_{t-1}$ 而不泄露未来词？
- [ ] Attention Weight 在 Softmax 归一化时是否对 Padding 位置施加了包含 $-\infty$ 的 Mask？
- [ ] Teacher Forcing 是否在 Validation 阶段完全关闭？

---

## 🧪 验证与测试

```bash
pytest 03-Projects/08-NLP全栈/tests/test_seq2seq.py
```
