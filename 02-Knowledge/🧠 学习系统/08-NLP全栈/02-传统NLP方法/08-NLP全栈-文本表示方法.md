---
sources: ['Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to Information Retrieval. Chapter 6.', 'Jurafsky, D., & Martin, J. H. (2024). Speech and Language Processing (3rd ed. draft). Chapter 6.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "文本表示方法"
created: 2026-08-06
status: completed
assessment_exempt: false
difficulty: beginner
stage_moc: "[[🧭 阶段2-传统NLP方法]]"
upstream: ["[[08-NLP全栈-文本预处理]]"]
tags: [学习, NLP, 文本表示, One-hot, Bag-of-Words, TF-IDF]
---

# 08-NLP全栈-文本表示方法

---

## 1. 这个知识点解决什么问题？

> **We Encountered What Problem**:
> 计算机只懂数字，无法直接计算字符串。如何将离散的文本符号转化为数值向量，使数学模型（如 Logistic Regression, SVM, 余弦相似度）能够量化计算文本之间的相似度与分类边界，是传统 NLP 的核心基础。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是从 One-hot 独热编码、词袋模型 (Bag-of-Words, BoW)、TF-IDF 发展到稠密向量 (Word2Vec / Transformer Embedding) 的必经之路。
- **实际应用场景**：文本分类 baseline 搭建、文档相似度匹配、基于 TF-IDF / BM25 的稀疏检索。

---

## 3. 正式定义与核心公式

### 1. 词袋模型 (Bag-of-Words, BoW)

忽略词语出现的顺序与语法，仅将文档视为词频的集合。设词表大小为 $V$，文档 $d$ 的 BoW 表示为向量 $\mathbf{x}_d \in \mathbb{R}^V$。

### 2. TF-IDF (Term Frequency-Inverse Document Frequency)

TF-IDF 衡量词项 $t$ 在文档 $d$ 中的重要性：

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

- **词频 (Term Frequency)**：$\text{TF}(t, d) = \frac{f_{t, d}}{\sum_{t' \in d} f_{t', d}}$
- **逆文档频率 (Inverse Document Frequency)**：$\text{IDF}(t, D) = \log \left( \frac{|D|}{1 + |\{d \in D : t \in d\}|} \right)$

### 3. 余弦相似度 (Cosine Similarity)

计算两篇文档向量 $\mathbf{u}, \mathbf{v}$ 的夹角余弦值：

$$\text{CosSim}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2} = \frac{\sum_{i=1}^V u_i v_i}{\sqrt{\sum_{i=1}^V u_i^2} \sqrt{\sum_{i=1}^V v_i^2}}$$

---

## 4. Python 实现：Scikit-learn 手写 TF-IDF 与相似度

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

corpus = [
    "natural language processing with python",
    "deep learning for natural language processing",
    "computer vision and image recognition"
]

# 1. 提取 TF-IDF 矩阵
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

print("Vocabulary size:", len(vectorizer.get_feature_names_out()))
print("TF-IDF Matrix Shape:", tfidf_matrix.shape) # (3, V)

# 2. 计算文档 0 与文档 1 的余弦相似度
sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
print("Similarity (Doc 0 vs Doc 1):", sim[0][0])
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

### 误区：TF-IDF 能捕获词语语义与词序
- **局限性 1 (正交性/维度灾难)**：One-hot / TF-IDF 中，`cat` 与 `dog` 的向量完全正交（点积为 0），无法体现语义相似。
- **局限性 2 (语序缺失)**："not good, very bad" 与 "good, not very bad" 在 BoW 中向量完全相同。

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

- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Chapter 6.
- Jurafsky, D., & Martin, J. H. (2024). *Speech and Language Processing* (3rd ed. draft). Chapter 6.


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《文本表示方法》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《文本表示方法》的核心机制及其与上下游模块的连接逻辑。
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
