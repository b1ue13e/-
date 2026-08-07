---
type: project
kind: project
track: 机器学习与AI应用
project_type: homework
course: "08-NLP全栈"
assignment_id: "08-NLP全栈-HW02"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[08-NLP全栈-子词分词]]", "[[08-NLP全栈-文本预处理]]"]
source_type: open_source_project_task
source: "Hugging Face Tokenizers & MinGPT Tokenizer Labs"
source_url: "https://github.com/huggingface/tokenizers"
created: 2026-08-07
status: planned
flow: project
tags: [作业, NLP, BPE, 子词分词, Tokenizer]
assessment_exempt: false
---

# 08-NLP全栈-课后作业-02-子词分词与BPE算法

> ⏱ **预计完成耗时**：2.5 小时  
> 🎯 **对应阶段**：阶段 2 - 传统统计 NLP 方法 / 阶段 4 - Transformer 与预训练模型

---

## 🎯 学习目标

1. 深入理解现代大语言模型（如 GPT, LLaMA）分词器（Tokenizer）的核心底层机制：Byte Pair Encoding (BPE)。
2. 纯 Python 从零实现 BPE 训练过程：字符频率统计、相邻词对（Pair）频次统计与合并（Merge）规则表迭代生成。
3. 实现根据 Merge 规则表对全新文本进行 Tokenize（编码）与 Decode（还原解码）的完整流水线。

---

## 🚧 任务边界

- **包含**：基于纯 Python 实现包含字符串预预处理、词频字典初始化、Top-1 高频 Pair 合并规则学习、Encode / Decode 函数。
- **不包含**：Rust / C++ 底层并发分词性能优化（如 `tokenizers` 库的底层加速实现）、Byte-level BPE 的位级映射。

---

## 📋 详细题目与实施步骤

### 任务 1：BPE 词表训练算法实现 (`train_bpe`)
给定一个小型文本语料集 $D$，输入目标词表大小 $V_{target}$（假设基础字符表大小为 $V_{init}$，需要迭代合并 $k = V_{target} - V_{init}$ 次）：
1. 将语料中的单词按照字符拆解，末尾添加结尾标记符号（如 `</w>`）。
2. 在每一步迭代中，统计当前语料中所有连续相邻符号对 $(s_i, s_{i+1})$ 的全局频次。
3. 挑选频次最高的最高频符号对 $(s_{top1}, s_{top2})$，将其合并为新符号 $s_{new} = s_{top1} + s_{top2}$，并记录合并规则 $(s_{top1}, s_{top2}) \to s_{new}$。
4. 重复上述步骤，直到达到目标词表大小或无可用合并对。

### 任务 2：分词器编码与解码逻辑 (`encode` & `decode`)
1. **`encode(text, merges)`**：根据已训练好的 `merges` 规则优先级，将未知文本分词为 BPE Token 序列。
2. **`decode(tokens)`**：将 Token 序列拼接，去除 `</w>` 标记，还原原始自然语言文本。

---

## 📦 提交产物

1. `scripts/bpe_tokenizer.py`：包含 `BPETokenizer` 类及其 `train()`, `encode()`, `decode()` 方法。
2. `reports/hw02_bpe_report.md`：记录在 sample 语料上的前 10 次合并规则表与未登录词（OOV）编码测试结果。

---

## ⚖️ 验收标准 (Rubric)

| 评分项 | 权重 | 通过标准 |
| :--- | :--- | :--- |
| **BPE 训练算法** | 40% | 正确统计最高频 Pair，合并规则迭代无误，词表扩展到指定大小停止 |
| **Encode / Decode** | 40% | 编码过程严格遵守规则优先级，解码可无损还原未包含特殊字符的文本 |
| **单元测试** | 20% | 运行 `pytest 03-Projects/08-NLP全栈/tests/test_bpe.py` 100% 通过 |

---

## 🔍 引导与自检

- [ ] 是否在词尾加上了 `</w>` 区别词中与词尾相同字符？
- [ ] 当出现多个频次并列最高的 Pair 时，是否具备稳定决胜逻辑（如按字典序）？
- [ ] `encode` 算法中，遇到未在基础字符集中出现的完全未知字符是如何处理的？

---

## 🧪 验证与测试

```bash
pytest 03-Projects/08-NLP全栈/tests/test_bpe.py
```
