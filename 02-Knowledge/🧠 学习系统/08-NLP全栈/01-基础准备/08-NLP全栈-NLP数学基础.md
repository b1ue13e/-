---
sources: ['Manning, C. D., & Schütze, H. (1999). Foundations of Statistical Natural Language Processing. MIT Press.', 'Jurafsky, D., & Martin, J. H. (2024). Speech and Language Processing (3rd ed. draft). Chapter 3.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "NLP数学基础"
created: 2026-08-06
status: completed
assessment_exempt: false
difficulty: beginner
stage_moc: "[[🧭 阶段1-基础准备]]"
upstream: ["[[08-NLP全栈-语言学基础]]"]
tags: [学习, NLP, 数学基础, N-gram, 语言模型, 齐夫定律]
---

# 08-NLP全栈-NLP数学基础

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 文本不是均匀分布的随机信号。现实世界中的词频分布呈现极度长尾效应（齐夫定律 Zipf's Law）。如何用数学概率模型刻画连续词序列的联合概率分布 $P(w_1, w_2, \dots, w_T)$，并解决未登录词 (OOV) 与零概率稀疏问题，是统计语言建模的核心关隘。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是经典 N-gram 语言模型、朴素贝叶斯文本分类、平滑算法 (Kneser-Ney Smoothing) 以及自回归 LLM 条件概率乘积法则的基础。
- **实际应用场景**：评估语言模型概率 $P(W)$、处理高频停用词与极低频长尾词、文本特征提取中的 TF-IDF 权重设计。

---

## 3. 正式定义与核心公式

### 1. 齐夫定律 (Zipf's Law)

在自然语言语料库中，词频 $f$ 与该词在词频表中的排名 $r$ 成反比关系：

$$f(r) \propto \frac{1}{r^s} \quad (s \approx 1)$$

即少数高频词（如 "the", "of", "是"）占据了绝大部分频次，而绝大多数词属于极低频词。

### 2. 语言模型的链式法则 (Chain Rule of Probability)

文本序列 $W = (w_1, w_2, \dots, w_T)$ 的联合概率表达为按顺序条件概率的乘积：

$$P(w_1, w_2, \dots, w_T) = \prod_{t=1}^T P(w_t \mid w_1, w_2, \dots, w_{t-1})$$

### 3. 马尔可夫假设与 N-gram 语言模型

在 $N$-gram 模型中，假设第 $t$ 个词的出现仅依赖于前 $N-1$ 个词：

$$P(w_t \mid w_1, \dots, w_{t-1}) \approx P(w_t \mid w_{t-N+1}, \dots, w_{t-1}) = \frac{C(w_{t-N+1}, \dots, w_t)}{C(w_{t-N+1}, \dots, w_{t-1})}$$

---

## 4. Python 实现：简单 Bigram (2-gram) 语言模型

```python
from collections import defaultdict, Counter

sentences = [
    ["<s>", "i", "like", "nlp", "</s>"],
    ["<s>", "i", "like", "pytorch", "</s>"],
    ["<s>", "nlp", "is", "great", "</s>"]
]

# 统计 Bigram 频次
unigram_counts = Counter()
bigram_counts = defaultdict(Counter)

for sentence in sentences:
    for i in range(len(sentence) - 1):
        w1, w2 = sentence[i], sentence[i+1]
        unigram_counts[w1] += 1
        bigram_counts[w1][w2] += 1

# 计算条件概率 P(like | i)
def get_bigram_prob(w1, w2):
    if unigram_counts[w1] == 0:
        return 0.0
    return bigram_counts[w1][w2] / unigram_counts[w1]

print("P(like | i) =", get_bigram_prob("i", "like")) # 1.0
print("P(nlp | like) =", get_bigram_prob("like", "nlp")) # 0.5
```

---


## 5. 常见误区与对比矩阵

| 评估维度 / 特性 | 方案 A / 经典范式 | 方案 B / 改进范式 | 权衡与选型建议 (Trade-offs) |
| :--- | :--- | :--- | :--- |
| **计算复杂度** | $\mathcal{O}(N^2)$ 或传统高阶复杂度 | $\mathcal{O}(N \log N)$ 或近似线性复杂度 | 高并发生产环境优先选择低复杂度方案 |
| **显存 / 存储占用** | 占用较高，受限于序列长度/维度 | 优化压缩，支持 Memory-efficient | 边缘设备或资源受限场景推荐优化方案 |
| **表征能力与精度** | 基础表达，易受局部噪声干扰 | 强特征提取，捕捉长距离依赖 | 高精度需求任务（如长文本理解/生成）推荐改进范式 |
| **工程落地门槛** | 开箱即用，工具链极为成熟 | 需特定依赖库 (如 CUDA / Triton) | 开发初期快速原型验证使用经典范式 |


## 5. 原有补全内容与 常见误区与易错点

### 误区：直接将多个条件概率相乘导致下溢 (Underflow)
- **错误计算**：当序列长度 $T$ 较长时，$P(W) = \prod_{t=1}^T P(w_t \mid \dots)$ 会迅速变成 `0.0`。
- **正确做法**：全过程使用**对数概率空间 (Log-Probability)** 计算求和：
  $$\log P(W) = \sum_{t=1}^T \log P(w_t \mid w_{t-N+1}, \dots, w_{t-1})$$

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

---

## 7. 参考文献与延伸阅读

- Manning, C. D., & Schütze, H. (1999). *Foundations of Statistical Natural Language Processing*. MIT Press.
- Jurafsky, D., & Martin, J. H. (2024). *Speech and Language Processing* (3rd ed. draft). Chapter 3.


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《NLP数学基础》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《NLP数学基础》的核心机制及其与上下游模块的连接逻辑。
2. **代数/代码自测**：手写关键代数推导步骤或 PyTorch/Python 核心实现伪代码。
3. **防错自测**：如果输入数据出现极小值或极大值离群点，该模块会发生什么异常？如何做数值稳定防护？


---

## 🛠️ 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
