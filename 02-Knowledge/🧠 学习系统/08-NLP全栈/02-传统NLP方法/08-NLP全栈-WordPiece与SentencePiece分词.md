---
type: study
topic: "WordPiece与SentencePiece分词"
course: "08-NLP全栈"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段2-传统NLP方法]]"
upstream: ["[[08-NLP全栈-子词分词]]"]
flow: knowledge
kind: concept
difficulty: intermediate
tags: [NLP, 分词, WordPiece, SentencePiece, BPE, Subword]
---

# 08-NLP全栈-WordPiece与SentencePiece分词

> **一句话总结**：WordPiece 基于语言模型似然最大化选择合并子词，而 SentencePiece 将文本视为无空格字符流并采用 Unigram 语言模型概率切分，彻底消除了语言特定的预分词依赖。

---

## 🎯 1. 概念动机与核心原理

在传统 BPE（Byte-Pair Encoding）算法中，子词合并依赖于字符对出现的**绝对频次**。然而，频次高的子词组合未必能最大程度提升语言模型的生成概率。为此：
1. **WordPiece**：在 BERT 等模型中使用，每次选择能够使训练集语言模型**似然概率增加最大**的两个子词进行合并。
2. **SentencePiece**：针对多语言（如中文、日语）无天然空格分隔的问题，将输入直接视为 Raw Byte/Unicode 流（将空格替换为特有符号 `_`），并通过 **Unigram Subword Model** 采用维特比 (Viterbi) 算法迭代剪枝得到最优切分。

---

## 📐 2. 数学推导与合并目标

### 2.1 WordPiece 的最大似然合并准则
假设将子词 $A$ 和 $B$ 合并为新子词 $AB$。合并前后整个词表语言模型的对数似然变化量相当于互信息 (Mutual Information)：

$$\text{Score}(A, B) = \frac{P(AB)}{P(A) \cdot P(B)} = \frac{\text{Count}(AB) \cdot N}{\text{Count}(A) \cdot \text{Count}(B)}$$

WordPiece 并不简单看 $\text{Count}(AB)$，而是计算当 $A$ 和 $B$ 独立出现概率的乘积与合并出现的联合概率的比值。分母对高频单字进行了惩罚，防止常见字过度合并。

### 2.2 SentencePiece (Unigram LM) 剪枝算法
Unigram 语言模型假设每个子词独立发生，句子 $W = (x_1, x_2, \dots, x_k)$ 的概率为：

$$P(W) = \prod_{i=1}^{k} P(x_i), \quad \sum_{x \in \mathcal{V}} P(x) = 1$$

查找最优切分算法使用动态规划（Viterbi 算法）：

$$W^* = \arg\max_{W \in \mathcal{S}(X)} P(W)$$

算法初始构建一个巨大 Vocab $\mathcal{V}$，每次计算移除某个子词 $x$ 后整体训练集似然函数 $\mathcal{L}$ 的损失 $\Delta \mathcal{L}_x$，并淘汰损失最小的前 $p\%$ (如 20%) 子词，直至词表收缩至预设大小。

---

## 💻 3. Python/HuggingFace 代码实现

```python
import tiktoken
from tokenizers import Tokenizer, models, pre_tokenizers, trainers

def demo_wordpiece_train():
    # 实例化 WordPiece 模型
    tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    
    trainer = trainers.WordPieceTrainer(
        vocab_size=1000, 
        special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"]
    )
    
    # 训练示例文本
    files = ["sample.txt"]  # 实际应传入语料路径
    print("[INFO] WordPiece Trainer initialized with Max Likelihood merge criteria.")

def run_sentencepiece_unigram():
    # 示范 Unigram 切分逻辑
    import sentencepiece as spm
    print("[INFO] SentencePiece provides loss-less tokenization with '_' space symbol.")

if __name__ == "__main__":
    demo_wordpiece_train()
```

---

## ⚠️ 4. 常见陷阱与避坑指南

1. **WordPiece 的前缀 `##` 机制**：BERT 中子词若非词首，会带有前缀 `##`（如 `playing` -> `play`, `##ing`）。在做 NER 序列标注对齐时需格外注意 Offset Mapping。
2. **SentencePiece 还原性 (Lossless Tokenization)**：SentencePiece 在解码时直接 `replace(' ', ' ').strip()` 即可完美恢复原始文本（包括多余空格），而 BPE/WordPiece 容易丢失原始空格信息。

---

## 🛠️ 5. 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：WordPiece 与 BPE 的合并得分函数 (Score) 有何本质不同？
- [ ] **问题 2**：SentencePiece 为何被称为无损切分 (Lossless Tokenization)？`_` 符号的作用是什么？
- [ ] **问题 3**：Unigram 语言模型分词算法与 BPE 自底向上合并的过程有何方向上的差异？

---

## 🃏 6. 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明 BERT 词表中 `##ing` 中 `##` 的含义及其在计算 Token 长度时的影响。
2. **代数推导**：给出 Unigram 分词中采用 Viterbi 求解最佳句子切分的转移概率与状态转移方程。
3. **防错自测**：在多语言 (中文/日文/英文) 混合场景下，为什么强烈推荐使用 SentencePiece 替代规则预分词？

---

## 🛠️ 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```


---

## 🛠️ 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
