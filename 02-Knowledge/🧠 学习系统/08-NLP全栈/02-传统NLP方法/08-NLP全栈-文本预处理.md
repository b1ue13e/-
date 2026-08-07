---
sources: ['Jurafsky, D., & Martin, J. H. (2024). Speech and Language Processing (3rd ed. draft). Chapter 2.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "文本预处理"
created: 2026-08-06
status: completed
assessment_exempt: false
difficulty: beginner
stage_moc: "[[🧭 阶段2-传统NLP方法]]"
upstream: ["[[08-NLP全栈-倒排索引]]"]
tags: [学习, NLP, 文本预处理, 分词, 正则表达式, 停用词]
---

# 08-NLP全栈-文本预处理

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 原始文本（如网页爬虫、社交媒体帖子、OCR 识别结果）充满了噪音、格式错乱、特殊符号与冗余词汇。直接输入模型会导致词表急剧膨胀、收敛变慢甚至降低模型表现。如何设计标准化、可重现的文本预处理流水线（包含正则正则清洗、分词、停用词过滤与标准化），是 NLP 的第一道关口。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是文本表示（TF-IDF / 词向量）、倒排索引检索及大型语言模型数据集清洗 (Data Cleaning / Quality Filtering) 的第一步。
- **实际应用场景**：删除 HTML 标签与无意义标点、处理 URL 与 Email 占位符、过滤高频停用词 (Stopwords)。

---

## 3. 预处理关键步骤与算法

### 1. 正规化 (Normalization) 与 Unicode 规范化

- **大小写折叠 (Case Folding)**：将所有字符转为小写（在某些特定任务如 NER 中需谨慎使用）。
- **Unicode NFKC 规范化**：消除全角/半角字符、特殊兼容字符的歧义（如 `①` -> `1`, `full-width Ａ` -> `A`）。

### 2. 停用词 (Stopwords) 过滤准则

定义基于词频与信息量的保留条件：

$$\text{Keep}(w) = \begin{cases} \text{False} & \text{if } w \in \mathcal{S}_{\text{stopwords}} \text{ or } f(w) < f_{\min} \\ \text{True} & \text{otherwise} \end{cases}$$

---

## 4. Python 实践：标准文本清洗 Pipeline

```python
import re
import unicodedata

def clean_text(text: str) -> str:
    # 1. Unicode NFKC 规范化
    text = unicodedata.normalize('NFKC', text)
    # 2. 去除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    # 3. 替换 URL 与 Email
    text = re.sub(r'http[s]?://\S+', '[URL]', text)
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)
    # 4. 规范多余空白符
    text = re.sub(r'\s+', ' ', text).strip()
    return text

raw_sample = "<p>Check our website at https://ai.org! Contact info: test@domain.com.  </p>"
print("Cleaned:", clean_text(raw_sample))
# 输出: Cleaned: Check our website at [URL]! Contact info: [EMAIL].
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

### 误区：在所有 NLP 任务中无脑过滤停用词与小写化
- **反例 (NER 命名实体识别)**：在 `US President` 中，若小写化为 `us`，`US`（美国）会变成代词 `us`（我们）；若过滤掉停用词 `in`, `at`，实体边界识别精度会严重下降。**深度学习/LLM 时代通常不主动删除停用词**。

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

- Jurafsky, D., & Martin, J. H. (2024). *Speech and Language Processing* (3rd ed. draft). Chapter 2.


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《文本预处理》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《文本预处理》的核心机制及其与上下游模块的连接逻辑。
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
