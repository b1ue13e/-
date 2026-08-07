---
type: study
topic: "子词分词 (Subword Tokenization)"
course: "08-NLP全栈"
created: 2026-08-03
status: active
flow: knowledge
kind: concept
difficulty: intermediate
stage_moc: "[[🧭 阶段2-传统NLP方法]]"
upstream: ["[[08-NLP全栈-文本预处理]]"]
concept: ["Subword Tokenization", "BPE", "WordPiece", "Unigram"]
prerequisites: ["文本预处理", "词频统计"]
related: ["BERT模型", "GPT系列", "HuggingFace生态系统"]
sources: ['Sennrich, R., Haddow, B., & Birch, A. (2016). Neural Machine Translation of Rare Words with Subword Units. ACL 2016. arXiv:1508.07909.', 'Kudo, T. (2018). Subword Regularization: Improving Neural Network Translation Models. EMNLP 2018. arXiv:1804.10959.']
tags: [学习, NLP, 分词, Tokenization, BPE]
assessment_exempt: false
---

# 08-NLP全栈-子词分词

> ⏱ **预计学习耗时**：30 分钟  
> 🎯 **学习行为目标**：掌握子词分词（BPE、WordPiece、Unigram）的算法原理，能手算推导 3 次 BPE 合并过程，能解释 OOV 问题与词表大小之间的权衡。

---

## 🎯 问题动机与核心直觉

在传统词级分词中，模型极易遇到**未登录词 (Out-of-Vocabulary, OOV)** 问题；而字符级分词虽然消除了 OOV，但序列长度极长且缺乏语义粒度。

**子词分词 (Subword Tokenization)** 介于词级与字符级之间，通过自动合并高频字符对，在维持合理词表大小（如 32k-50k）的同时彻底解决 OOV 问题：
- **常见词**（如 `hug`）：保持完整 Token。
- **罕见词**（如 `unhuggable`）：切分为高频子词块（如 `un` + `hug` + `gable`）。

---

## 📐 核心算法与数学定义

### 1. Byte Pair Encoding (BPE)
BPE 是一种自底向上的贪心字节对合并算法：
1. **初始化**：将词表设为所有独立字符集合，统计语料中词尾标记（如 `</w>`）与相邻字符对的频率。
2. **循环合并**：选择频率最高的一对连续 Token $A, B$，合并为新 Token $AB$ 并更新词表。
3. **终止条件**：达到设定词表上限 $V_{max}$ 或合并收益低于阈值。

### 2. WordPiece 与 Unigram
- **WordPiece**（用于 BERT）：按**最大似然提升**选择合并对（即选择使语言模型似然度提升最大的对 $A, B$），评分标准为 $\frac{P(AB)}{P(A)P(B)}$。
- **Unigram**（用于 SentencePiece/T5）：自顶向下，从巨大候选词表开始，按损失函数增量逐步**剪枝剪去贡献最小的 Token**。

---

## 💻 最小代码实现 (BPE Step-by-Step)

```python
from collections import defaultdict

def get_stats(vocab):
    pairs = defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, v_in):
    v_out = {}
    bigram = ' '.join(pair)
    replacement = ''.join(pair)
    for word in v_in:
        w_out = word.replace(bigram, replacement)
        v_out[w_out] = v_in[word]
    return v_out

# 基础语料
vocab = {'h u g </w>': 5, 'p u g </w>': 3, 'h u g g u s </w>': 2}
for i in range(4):
    pairs = get_stats(vocab)
    if not pairs:
        break
    best = max(pairs, key=pairs.get)
    vocab = merge_vocab(best, vocab)
    print(f"Iter {i+1} Best Pair: {best} -> Vocab: {vocab}")
```

---

## ⚠️ 常见误区与避坑指南

1. **混淆 Pre-tokenization 与 Subword Tokenization**：
   - 传统 BPE 在切分子词前通常先按空格/标点做初步切分（Pre-tokenization）。而 SentencePiece 直接将空格视作特殊字符 ` ` 进行统一 BPE，无需特定语言的预分词器。
2. **字节级 (Byte-level BPE) vs 字符级 BPE**：
   - GPT-2/GPT-4 采用 Byte-level BPE（从 256 个 raw bytes 出发），因此无需担心任何 UTF-8 多字节字符的 OOV 表现。

---

## 🥊 学完后可以完成

### 1. 本卡自测练习
- **手算推导**：对语料 `low: 5, lower: 2, newest: 6, widest: 3` 执行 3 次 BPE 合并，写出每次合并的字符对和更新后的词表。
- **概念比较**：对比 BPE、WordPiece 和 Unigram 的词表构建策略异同。

### 2. 派生视图与验收入口

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/08-NLP全栈"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

```dataview
LIST
FROM "03-Projects/08-NLP全栈"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---

## 📚 参考文献与延伸阅读

- Sennrich, R., Haddow, B., & Birch, A. (2016). Neural Machine Translation of Rare Words with Subword Units. ACL 2016. arXiv:1508.07909.
- Kudo, T. (2018). Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates. EMNLP 2018. arXiv:1804.10959.



## 5. 常见误区与对比矩阵

| 评估维度 / 特性 | 方案 A / 经典范式 | 方案 B / 改进范式 | 权衡与选型建议 (Trade-offs) |
| :--- | :--- | :--- | :--- |
| **计算复杂度** | $\mathcal{O}(N^2)$ 或传统高阶复杂度 | $\mathcal{O}(N \log N)$ 或近似线性复杂度 | 高并发生产环境优先选择低复杂度方案 |
| **显存 / 存储占用** | 占用较高，受限于序列长度/维度 | 优化压缩，支持 Memory-efficient | 边缘设备或资源受限场景推荐优化方案 |
| **表征能力与精度** | 基础表达，易受局部噪声干扰 | 强特征提取，捕捉长距离依赖 | 高精度需求任务（如长文本理解/生成）推荐改进范式 |
| **工程落地门槛** | 开箱即用，工具链极为成熟 | 需特定依赖库 (如 CUDA / Triton) | 开发初期快速原型验证使用经典范式 |


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《子词分词》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《子词分词》的核心机制及其与上下游模块的连接逻辑。
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
