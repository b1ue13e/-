---
sources: ['Jurafsky, D., & Martin, J. H. (2024). Speech and Language Processing (3rd ed. draft). Chapters 2 & 8.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "语言学基础"
created: 2026-08-06
status: completed
assessment_exempt: false
difficulty: beginner
stage_moc: "[[🧭 阶段1-基础准备]]"
upstream: ["[[08-NLP全栈-前置-PyTorch与NLP编程基础]]"]
tags: [学习, NLP, 语言学, 形态学, 词性标注]
---

# 08-NLP全栈-语言学基础

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 计算机无法直接理解人类自然语言的语法结构。自然语言包含多层次的结构：词素（Morphology）、词性（Part-of-Speech, POS）、句法成分（Constituency Parse Tree）与依存关系（Dependency Parser）。不懂语言学基本层次，就无法理解分词粒度对模型的影响，也无法设计精准的序列标注与实体识别任务。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是子词分词 (BPE/WordPiece)、序列标注 (POS Tagging/NER) 以及句法分析的学科基石。
- **实际应用场景**：中文分词歧义处理（如“结婚的和尚未结婚的”）、词干提取 (Stemming) 与词形还原 (Lemmatization)、命名实体识别的标签设计 (BIO / BIOES 标注体系)。

---


### 3.1 形式化定义与数学模型

在计算语言学中，语言模型的困惑度 (Perplexity, $PP$) 定义为句子序列 $\mathbf{W} = (w_1, w_2, \dots, w_N)$ 的交叉熵倒数：
$$PP(\mathbf{W}) = P(w_1, w_2, \dots, w_N)^{-\frac{1}{N}} = \exp\left( -\frac{1}{N} \sum_{i=1}^{N} \ln P(w_i \mid w_1, \dots, w_{i-1}) \right)$$

齐夫定律 (Zipf's Law) 的形式化表达为：词频 $f(r)$ 与词频排名 $r$ 成反比关系，常数 $C \approx 0.1$：
$$f(r) = \frac{C}{r^\alpha}, \quad \alpha \approx 1$$

Edit Distance（编辑距离/莱文斯坦距离）状态转移递归式定义为：
$$D[i,j] = \min \begin{cases} D[i-1, j] + 1 & \text{(Deletion)} \\ D[i, j-1] + 1 & \text{(Insertion)} \\ D[i-1, j-1] + \mathbb{I}(s_1[i] \neq s_2[j]) & \text{(Substitution)} \end{cases}$$


## 3. 正式定义与语言学层级

### 1. 语言学四大核心层级

| 语言学层级 | 研究对象 | NLP 对应技术与任务 |
| :--- | :--- | :--- |
| **形态学 (Morphology)** | 词根、词缀、词形变化 | 词干提取 (Porter Stemmer)、词形还原 (Lemmatization)、子词分词 |
| **词汇学与词性 (POS)** | 名词、动词、形容词等词性 | 词性标注 (Part-of-Speech Tagging)、HMM / CRF 序列标注 |
| **句法学 (Syntax)** | 词与词之间的短语结构与主谓宾依存关系 | 依存句法分析 (Dependency Parsing)、上下文无关文法 (CFG) |
| **语义学 (Semantics)** | 词义、句义、实体关系 | 命名实体识别 (NER)、词向量 (Word2Vec)、语义蕴含 (NLI) |

### 2. BIO / BIOES 序列标注规范

设实体类型为 `LOC`（地点），输入句子 `["I", "visited", "New", "York"]`：

- **BIO 标注**：`[O, O, B-LOC, I-LOC]`
- **BIOES 标注**：`[O, O, B-LOC, E-LOC]` （其中 `S` 表示 Single 单词实体）

---

## 4. Python 实践：词性标注与词形还原

```python
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# 下载 NLTK 依赖数据（首次运行需下载）
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

text = "The quick brown foxes are jumping over lazy dogs."
tokens = word_tokenize(text)

# 1. 词性标注 (POS Tagging)
pos_tags = nltk.pos_tag(tokens)
print("POS Tags:", pos_tags[:5]) # [('The', 'DT'), ('quick', 'JJ'), ('brown', 'NN'), ...]

# 2. 词形还原 (Lemmatization)
lemmatizer = WordNetLemmatizer()
lemmas = [lemmatizer.lemmatize(w, pos='n') for w, tag in pos_tags]
print("Lemmatized Words:", lemmas)
```

---


## 5. 常见误区与对比矩阵

| 语言学层级 | 分析对象 | 经典算法/模型 | 典型应用与局限 |
| :--- | :--- | :--- | :--- |
| **形态学 (Morphology)** | 词根、词缀、屈折变体 | Stemming (Porter), Lemmatization | 消除词形差异；基于规则易过拟合 |
| **句法学 (Syntax)** | 词性 (POS)、成分/依存树 | HMM, CRF, Dependency Parser | 提取语法树结构；难以建模跨句长距离语义 |
| **语义学 (Semantics)** | 词义、命名实体、语义角色 | Word2Vec, BERT, SRM | 捕捉向量概念分布；存在一词多义歧义 |
| **语用学 (Pragmatics)** | 上下文语境、言语行为 | Dialogue Act Classification, LLM | 决定指令意图；受限于世界知识和上下文窗口 |





## 6. 闭卷自测与验收入口

请在不查阅资料的前提下尝试解答以下问题，或完成对应关联作业：
1. 本知识点的核心定义与推导公式是什么？
2. 相比传统方法，它的核心优势与工程选型 Trade-offs 是什么？
3. 如何在 PyTorch / Python 中实现并校验其关键张量维度与运算逻辑？


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《语言学基础》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《语言学基础》的核心机制及其与上下游模块的连接逻辑。
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
