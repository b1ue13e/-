---
type: study
topic: "Unicode、UTF-8 字节与 BPE Tokenizer 训练"
tags: [学习, 45-生成式AI基础与Prompt工程, Tokenizer, BPE]
created: 2026-08-05
status: completed
mastery: not_started
difficulty: intermediate
concept: ["Unicode编码", "字节级BPE", "Tokenizer"]
prerequisites: ["课程前置-Python-JSON测试与实验复现", "生成式AI-基础-概率生成Token与能力边界"]
related: ["Transformer与大语言模型-架构-Transformer工作原理", "Stanford-CS336-A1-逐节知识点映射"]
flow: knowledge
kind: concept
source: "Stanford CS336 Spring 2025 Assignment 1 Basics tokenizer section, MIT License"
anki_deck: "45-生成式AI基础与Prompt工程::Tokenizer工程"
anki_tags: [Unicode, UTF8, BPE, Tokenizer]
---

# Tokenizer 工程：Unicode、字节与 BPE 训练

## 0. 先判断它值不值得深挖

- **类别**：A 类（Stanford CS336 A1 §2 的必需知识卡）。
- **判断理由**：把“Token 是词”当定义会在中文、emoji、罕见字符、特殊 token 和可逆解码处失败。BPE 作业还要求训练、性能、语料差异和边界测试。

## 1. 这个知识点解决什么问题？

> 模型只能接收整数 ID，但人类文本包含不同语言、组合字符和任意字节。怎样把文本稳定、可逆地变成有限词表中的 ID，同时让常见片段更短？

Tokenizer 是数据到模型的正式接口。编码不一致会使训练和推理看到不同序列；特殊 token 处理错误还可能造成边界混淆或注入风险。

## 2. 为什么它重要？它有什么用？

- **正确性**：理解 code point、UTF-8 bytes、token ID 的三层映射。
- **可逆性**：普通文本应满足 `decode(encode(text)) == text`。
- **效率**：BPE 把高频相邻单元合并，减少常见文本的序列长度。
- **作业定位**：直接支撑 CS336 A1 的 `unicode1/2`、`train_bpe*`、`tokenizer`、`tokenizer_experiments`。

## 3. 学它之前需要哪些前置知识？

1. [[课程前置-Python-JSON测试与实验复现]]：bytes、字典、排序、文件 I/O 和单元测试。
2. [[生成式AI-基础-概率生成Token与能力边界]]：Token ID 是模型概率分布的离散事件。

## 4. 用直觉语言解释它

> “Unicode 给字符分配抽象号码，UTF-8 把号码装成 1–4 个字节，BPE 再把经常结伴出现的字节片段粘成快捷块。”

- code point 是抽象字符编号，不等于屏幕上的一个字形。
- UTF-8 是从文本到 bytes 的可变长编码。
- byte-level BPE 以 256 个单字节为保底，因此原则上可覆盖任意 UTF-8 文本。
- 一句话本质：**Tokenizer 是一套有版本、有顺序、有特殊符号规则的可逆编解码协议。**

## 5. 正式定义、核心公式、符号解释

### 1. 三层对象

$$\text{text}\xrightarrow{UTF-8}\text{bytes}\xrightarrow{BPE merges}\text{tokens}\xrightarrow{vocab}\text{ids}.$$

训练时，在当前序列集合中统计相邻 token 对频数：

$$c(a,b)=\sum_{s\in\mathcal{D}}\#\{i:(s_i,s_{i+1})=(a,b)\}.$$

选择最高频对 $(a^*,b^*)$，创建新 token $a^*\Vert b^*$，按确定规则替换所有**不重叠**出现；重复直到达到目标词表大小或没有可合并对。

| 对象 | 示例 | 边界 |
| :--- | :--- | :--- |
| Unicode code point | `中` 是 U+4E2D | 一个字形可由多个 code point 组合 |
| UTF-8 bytes | `中`.encode() 为 3 字节 | bytes 不能直接按字符切片理解 |
| BPE token | 若干 bytes 的元组 | 可能不是独立合法 UTF-8 |
| token ID | 非负整数 | 只在特定 vocab 版本内有意义 |
| special token | `<|endoftext|>` | 应先作为不可拆原子处理 |

### 2. 确定性与复杂度

- 最高频 pair 并列时必须定义稳定 tie-break，例如按 bytes 字典序。
- 朴素训练每轮全量重数 pair，便于验证但慢；优化实现维护 pair→位置索引和惰性失效堆。
- 合并表的**顺序**属于模型参数；编码时按训练优先级迭代，不能只保存无序集合。

## 6. 推导思路和思想来源

1. 字符词表无法覆盖所有语言，整词词表又会产生大量 OOV。
2. 从 bytes 开始可保证覆盖；但逐字节序列过长。
3. 统计高频相邻对并合并，让语料自身决定常用子串。
4. 特殊 token 在普通 BPE 前分段，避免其字符被意外拆开或跨边界合并。
5. 编码与解码必须共享同一 vocab、merge rank 和 special-token 配置。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

语料 `low low lower` 先按字符观察，`l-o`、`lo-w` 会高频出现。若先合并 `(l,o)` 为 `lo`，再合并 `(lo,w)` 为 `low`，常见词的 token 数下降；`lower` 仍可表示为 `low+e+r`。

### 例子 2：中等例子

`é` 可以是单一 code point U+00E9，也可以是 `e` 加组合重音。它们视觉近似但 UTF-8 bytes 不同。Tokenizer 是否做 Unicode normalization 必须显式声明；训练和推理策略不同会导致 ID 不同。

### 例子 3：实际应用例子（可运行 Python）

```python
# 输入：UTF-8 文本语料；输出：确定性 byte-level BPE merge 列表及可逆编码。
from collections import Counter

def train_bpe(texts: list[str], merge_count: int):
    sequences = [[bytes([value]) for value in text.encode("utf-8")] for text in texts]
    merges = []
    for _ in range(merge_count):
        counts = Counter(pair for seq in sequences for pair in zip(seq, seq[1:]))
        if not counts:
            break
        best = min((pair for pair, count in counts.items() if count == max(counts.values())))
        merges.append(best)
        merged_sequences = []
        for seq in sequences:
            out, index = [], 0
            while index < len(seq):
                if index + 1 < len(seq) and (seq[index], seq[index + 1]) == best:
                    out.append(seq[index] + seq[index + 1])
                    index += 2
                else:
                    out.append(seq[index])
                    index += 1
            merged_sequences.append(out)
        sequences = merged_sequences
    return merges

def encode(text: str, merges):
    tokens = [bytes([value]) for value in text.encode("utf-8")]
    for pair in merges:
        out, index = [], 0
        while index < len(tokens):
            if index + 1 < len(tokens) and (tokens[index], tokens[index + 1]) == pair:
                out.append(tokens[index] + tokens[index + 1])
                index += 2
            else:
                out.append(tokens[index])
                index += 1
        tokens = out
    return tokens

corpus = ["low", "lower", "low", "你好"]
merges = train_bpe(corpus, 6)
for sample in ["lower", "你好", "unseen🙂"]:
    tokens = encode(sample, merges)
    restored = b"".join(tokens).decode("utf-8")
    print(ascii(sample), len(tokens), ascii(restored))
    assert restored == sample
```

## 8. 常见误区和易混概念

- **误区 1**：一个 Unicode 字符总是一个 byte。UTF-8 使用 1–4 bytes，组合字符还可能含多个 code point。
- **误区 2**：单个 byte token 必须能独立 decode。多字节字符的中间 byte 不能单独解码，解码应先拼 bytes。
- **误区 3**：统计到最高频 pair 后可任意替换。重叠 pair、tie-break 和合并顺序会影响结果。
- **误区 4**：special token 就是普通字符串。它通常是协议控制符，应优先匹配并限制允许范围。

| 概念 | 核心问题 | 关键区别 | 使用场景 |
| :--- | :--- | :--- | :--- |
| 字符级 | 按 code point/字符切分 | 词表小、序列长 | 简单教学 |
| byte-level BPE | 从 bytes 学合并 | 无 OOV、可逆 | GPT 类 tokenizer |
| WordPiece | 基于似然/评分选子词 | 训练准则不同 | BERT 类模型 |
| Unigram LM | 从大词表删减 | 概率模型选分词 | SentencePiece |

## 9. 相关知识点与 Obsidian 双链建议

- 上游：[[生成式AI-基础-概率生成Token与能力边界]]。
- 下游：[[Transformer与大语言模型-架构-Transformer工作原理]]、[[Transformer与大语言模型-训练-GPT与自回归语言模型]]。
- 作业：[[Stanford-CS336-A1-逐节知识点映射]]。
- 工程：[[Prompt工程-安全-提示注入与分层防护]]，关注不可见字符与边界混淆。

## 10. 闭卷复现任务

- [ ] 区分 code point、UTF-8 bytes、token 与 token ID。
- [ ] 写出 BPE 一轮训练的输入、计数、选择和替换。
- [ ] 解释 byte-level 起始词表为何能避免 OOV。
- [ ] 说明单个 byte token 为什么不一定能独立解码。
- [ ] 设计 pair 并列时的确定规则。
- [ ] 解释重叠 pair 应怎样替换。
- [ ] 写出 encode/decode 可逆性测试。
- [ ] 说明 special token 为什么先分段。
- [ ] 比较朴素计数与增量索引的复杂度。
- [ ] 设计中文、emoji、空串和特殊 token 边界测试。

## 11. 自测题：5 道

1. `len("中")` 与 `len("中".encode("utf-8"))` 分别是什么？ `#自测题/基础`
2. 为什么 byte-level BPE 的解码先拼 bytes 再 decode？ `#自测题/基础`
3. 对序列 `a a a` 合并 pair `(a,a)`，一次不重叠替换得到什么？ `#自测题/中等`
4. 设计 special token 与普通文本相邻时的三个测试。 `#自测题/中等`
5. 说明怎样把朴素 BPE 的重复全量统计优化为增量维护，同时保证结果与 tie-break 完全一致。 `#自测题/较难`

> [!question]- 参考答案与评分点
> 1. Python 中通常为 1 和 3。2. 单 token 可能只是多字节字符的一部分。3. `[aa,a]`，不能复用中间元素。4. 单独、连续、前后紧邻普通文本，并验证不跨边界合并。5. 维护 pair 频数与出现位置，合并后只更新邻域；堆项惰性失效；使用相同字典序 tie-break。

## 12. 我的主动回忆区

- **三层映射**：
- **BPE 一轮**：
- **边界测试**：
- [ ] 明天  [ ] 3 天后  [ ] 7 天后  [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- 本卡合并 Unicode、BPE 与 Tokenizer 协议，因为三者共同构成 CS336 §2 的完整数据边界。
- 性能优化必须先与朴素参考实现逐样本对齐，再做 profile；不要先写复杂缓存。

## 🃏 Anki 卡片

Q: byte-level BPE 为什么原则上没有未知字符？
A: 初始词表覆盖全部 256 个 byte，任何 UTF-8 文本都能退化为 byte 序列。

Q: BPE 合并表为什么必须有顺序？
A: 后续 token 基于先前 token 构造，编码必须按训练优先级重放，顺序改变会改变切分。
