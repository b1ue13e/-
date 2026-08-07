---
type: study
topic: "BERT模型"
course: "08-NLP全栈"
created: 2026-08-06
status: active
stage_moc: "[[🧭 阶段4-Transformer与预训练模型]]"
upstream: ["[[08-NLP全栈-Transformer架构]]"]
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["BERT", "MLM (Masked LM)", "NSP (Next Sentence Prediction)", "Fine-Tuning"]
prerequisites: ["Transformer架构", "Self-Attention自注意力机制"]
related: ["BERT与GPT对比", "RoBERTa", "HuggingFace生态系统"]
anki_deck: NLP::Pretrained
anki_tags: ['#nlp', '#bert', '#pretrained']
assessment_exempt: false
---

# 08-NLP全栈-BERT模型

> ⏱ **预计学习耗时**：50 分钟  
> 🎯 **学习行为目标**：掌握 BERT 预训练两大任务（MLM 与 NSP）的原理；独立理解 `[CLS]` 与 `[SEP]` 标记的作用；能用 PyTorch 加载预训练权重并在下游情感分类任务做 Fine-tuning。

---

## 0. 核心概念与直觉起步

BERT (Bidirectional Encoder Representations from Transformers) 是 Google 在 2018 年提出的预训练语言模型。
它采用 **Transformer Encoder** 架构，最大的创新是打破了传统单向语言模型（如 GPT）的限制，实现了真正的**深层双向（Deep Bidirectional）**上下文表征。

---

## 1. 预训练两大任务

```text
[BERT 输入表达三层叠加]
Token Embeddings:    [CLS]   my  dog  is   cute [SEP]   he  likes  play [SEP]
Segment Embeddings:    A      A   A    A     A    A      B    B      B    B
Position Embeddings:   0      1   2    3     4    5      6    7      8    9
```

### 1. 掩码语言模型 (Masked Language Model, MLM)
随机掩蔽输入序列中 15% 的 Token：
- 80% 的时间替换为 `[MASK]` 标记。
- 10% 的时间替换为随机词。
- 10% 的时间保持原词不动。
模型根据双向上下文预测被掩蔽的原始词，损失函数为交叉熵。

### 2. 下句预测 (Next Sentence Prediction, NSP)
输入两个句子 A 和 B：
- 50% 的样本 B 是 A 的真实下一句 (Label: `IsNext`)。
- 50% 的样本 B 是随机抽取的句子 (Label: `NotNext`)。
通过取首位 `[CLS]` 标记的隐层向量做二分类判定。

---

## 3. PyTorch 微调下游分类示例

```python
import torch
import torch.nn as nn
from transformers import BertModel, BertConfig

class BertForSequenceClassification(nn.Module):
    """基于 BERT 预训练权重的序列分类模型"""
    def __init__(self, pretrained_model_name: str, num_classes: int = 2):
        super().__init__()
        self.bert = BertModel.from_pretrained(pretrained_model_name)
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_classes)

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor, token_type_ids: torch.Tensor = None):
        # 提取 BERT 输出
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids
        )
        # pooled_output 对应 [CLS] 的向量经 Dense + Tanh 变换后的结果
        pooled_output = outputs.pooler_output
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        return logits
```

---

## 12. 我的主动回忆区（Guided Recall）

1. BERT 预训练阶段 15% 被选中 Mask 的 Token 中，用 `[MASK]` 替换的概率是 `____`%。
2. 在句子二分类或匹配任务中，用作整句语义代表的特殊 Flag Token 是 `____`。
3. BERT 的架构类型是 Transformer 的 `____` 模块（Encoder / Decoder / Seq2Seq）。

---

## 13. 闭卷提取练习与分级自测

### 基础题
为什么 BERT 能够做到深层双向表征，而传统 GPT 不能？

<details>
<summary>▶ 答案与解释</summary>

BERT 在计算注意力时没有 Casual Mask（因果掩码），所有 Token 可以同时看到左侧和右侧的词；而 GPT 使用了自回归因果掩码，第 $t$ 个 Token 只能看到前 $t-1$ 个词，因此 GPT 是单向自回归模型。
</details>

---

## 🛠️ 学完后可以完成

### 派生作业与验收入口
```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

### 关联下游知识点
```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/08-NLP全栈"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```




## 5. 常见误区与对比矩阵

| 评估维度 / 特性 | 方案 A / 经典范式 | 方案 B / 改进范式 | 权衡与选型建议 (Trade-offs) |
| :--- | :--- | :--- | :--- |
| **计算复杂度** | $\mathcal{O}(N^2)$ 或传统高阶复杂度 | $\mathcal{O}(N \log N)$ 或近似线性复杂度 | 高并发生产环境优先选择低复杂度方案 |
| **显存 / 存储占用** | 占用较高，受限于序列长度/维度 | 优化压缩，支持 Memory-efficient | 边缘设备或资源受限场景推荐优化方案 |
| **表征能力与精度** | 基础表达，易受局部噪声干扰 | 强特征提取，捕捉长距离依赖 | 高精度需求任务（如长文本理解/生成）推荐改进范式 |
| **工程落地门槛** | 开箱即用，工具链极为成熟 | 需特定依赖库 (如 CUDA / Triton) | 开发初期快速原型验证使用经典范式 |


---

## 🛠️ 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
