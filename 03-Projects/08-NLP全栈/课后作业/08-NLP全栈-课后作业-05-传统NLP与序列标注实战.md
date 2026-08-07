---
type: project
kind: project
track: 机器学习与AI应用
project_type: homework
course: "08-NLP全栈"
assignment_id: "08-NLP全栈-HW05"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[08-NLP全栈-NLP数学基础]]", "[[08-NLP全栈-Python编程与NLP工具]]", "[[08-NLP全栈-倒排索引]]", "[[08-NLP全栈-语言学基础]]", "[[08-NLP全栈-主题模型]]", "[[08-NLP全栈-句法分析]]", "[[08-NLP全栈-序列标注]]", "[[08-NLP全栈-统计机器学习]]", "[[08-NLP全栈-WordPiece与SentencePiece分词]]"]
source_type: official_assignment
source: "Stanford CS224n & NLTK Traditional NLP Assignment"
source_url: "https://github.com/stanfordnlp/cs224n-assignments"
created: 2026-08-07
status: planned
flow: project
tags: [作业, NLP, 序列标注, HMM, 倒排索引, 句法分析]
assessment_exempt: false
---

# 08-NLP全栈-课后作业-05-传统NLP与序列标注实战

> ⏱ **预计完成耗时**：3 小时  
> 🎯 **对应阶段**：阶段 1 - 基础准备 / 阶段 2 - 传统 NLP 方法

---

## 🎯 学习目标

1. 掌握倒排索引 (Inverted Index) 构建与 BM25/TF-IDF 布尔检索算法。
2. 深入理解 HMM (隐马尔可夫模型) 转移矩阵与发射矩阵推导，动手实现维特比 (Viterbi) 动态规划解码。
3. 理解转换句法分析 (Transition-based Dependency Parsing) 的 Shift-Reduce 栈推演过程。

---

## 🚧 任务边界

- **包含**：倒排索引类构建、HMM 词性标注 Viterbi 解码器、基于朴素贝叶斯/SVM 的传统文本特征提取。
- **不包含**：深度神经网络 (RNN/BERT) 序列标注。

---

## 📋 详细题目与实施步骤

### 任务 1：倒排索引与 BM25 检索算子
实现一个倒排索引 `InvertedIndex` 类，支持 `add_document(doc_id, text)` 与 `search_bm25(query, top_k)` 方法。

### 任务 2：HMM 维特比 (Viterbi) 解码算子
根据给定的状态转移概率 $A_{i,j} = P(S_t = s_j \mid S_{t-1} = s_i)$ 和发射概率 $B_{j, k} = P(O_t = o_k \mid S_t = s_j)$：

$$\delta_t(j) = \max_{i=1}^N [\delta_{t-1}(i) a_{ij}] \cdot b_j(o_t)$$

手写 Viterbi 算法在 POS Tagging 数据集上求解最优隐状态序列。

---

## 📦 提交产物

1. `scripts/traditional_nlp.py`：包含 `InvertedIndex` 和 `HMMViterbiTagger` 的实现。
2. `tests/test_traditional_nlp.py`：通过 pytest 测试。

---

## ⚖️ 验收标准 (Rubric)

| 评分项 | 权重 | 通过标准 |
| :--- | :--- | :--- |
| **倒排索引** | 40% | 正确构建 Token -> List[DocID] 映射，BM25 Score 计算准确 |
| **Viterbi 算法** | 60% | 在 500 条测试文本上 POS 标注 Accuracy $\ge 90\%$ |

---

## 🔍 引导与自检

- [ ] 是否正确为 $IDF$ 加 1 平滑避免除零异常？
- [ ] Viterbi 算法解码时是否保存了回溯指针矩阵 (Backpointer Matrix) 以恢复隐状态序列？
- [ ] 词性标注在测试集中遇到未登录词 (OOV) 时是否设置了平滑发射概率？

---

## 🧪 验证与测试

```bash
pytest 03-Projects/08-NLP全栈/tests/test_traditional_nlp.py
```
