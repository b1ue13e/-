---
type: study
topic: "NER与POS应用"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段5-隐马尔可夫模型]]"
flow: knowledge
kind: concept
difficulty: intermediate
upstream: ["[[概率图模型-条件随机场]]", "[[概率图模型-隐马尔可夫模型HMM]]"]
concept: ["命名实体识别", "词性标注", "特征工程", "序列标注"]
related: ["概率图模型-条件随机场", "概率图模型-Viterbi解码"]
tags: [概率图模型, NER, POS, NLP]
---

# 概率图模型-NER与POS应用

> 本卡把 HMM/CRF 落到 NLP 的两大经典任务：**词性标注（POS）** 与 **命名实体识别（NER）**。重点在**特征工程**（为什么 CRF 优于 HMM）与**标签方案设计**（BIO），以及语音识别中的 HMM 角色。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：文本序列需要标注——每个词是名词/动词（POS），或人名/地名/机构（NER）。序列标注的核心挑战：①上下文依赖（"bank" 是名词还是动词看前后）；②长距离特征（词形、大小写、词典匹配）；③标签间的结构约束（BIO 方案中 I 必须跟在 B 后）。HMM 太弱（观测独立），CRF 用特征函数解决 ① ②，Viterbi 解决 ③。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：POS/NER 是 NLP 管线的基础（解析、关系抽取的前提）；HMM→CRF→BiLSTM-CRF 展示了特征工程到深度学习的演进。
- **实际应用场景**：搜索引擎实体识别、医疗文本信息抽取、语音助手语义解析。
- **高频考点**：BIO 标签方案、POS/NER 特征设计、CRF 相对 HMM 的收益、评价指标（F1）。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-条件随机场]]**：CRF 定义/推断/学习。
2. **[[概率图模型-隐马尔可夫模型HMM]]**：序列标注基线。
3. **[[概率图模型-Viterbi解码]]**：解码算法。

---

## 4. 定义与核心公式

### 4.1 词性标注（POS Tagging）

**任务**：给每个词标词性（名词 N、动词 V、形容词 J 等）。

**HMM 视角**：状态 = 词性，观测 = 词；$P(\text{词性序列}, \text{词序列}) = \prod P(\text{词性}_t \mid \text{词性}_{t-1}) P(\text{词}_t \mid \text{词性}_t)$。**局限**：每个词只能由一个词性生成（观测独立），无法用词形/上下文特征。

**CRF 视角**：特征如：
- 词形：$f_1 = \mathbb{1}[y_t = V \wedge x_t \text{ 以 } -ing \text{ 结尾}]$；
- 上下文：$f_2 = \mathbb{1}[y_t = N \wedge x_{t-1} = \text{"the"}]$；
- 大小写：$f_3 = \mathbb{1}[y_t = \text{NNP} \wedge x_t \text{ 首字母大写}]$。

### 4.2 命名实体识别（NER）与 BIO 方案

**任务**：标注实体（人名 PER、地名 LOC、机构 ORG）。

**BIO 标签**：B-（Begin，实体首词）、I-（Inside，实体内部）、O（Outside，非实体）。如 "Bill Gates 在 Microsoft"：`[B-PER, I-PER, O, B-ORG]`。

**约束**：I- 标签必须紧跟 B- 或 I- 同类型——CRF 的转移特征可编码此约束（$f = \mathbb{1}[y_{t-1} = O, y_t = I\text{-}PER]$ 权重低）。

**评价**：F1（精确率/召回率调和），实体级匹配（整实体正确才算对）。

### 4.3 语音识别中的 HMM

**音素 HMM**：每个音素一个 HMM（状态 = 音素内部子状态），词序列 = 音素 HMM 的级联；**解码** = Viterbi 找最可能词序列；**语言模型** $P(w_1,\dots,w_n)$ 提供词级先验（与声学模型联合）：

$$\hat{\mathbf{w}} = \arg\max_{\mathbf{w}} P(\text{语音} \mid \mathbf{w}) P(\mathbf{w})$$

（$P(\text{语音}\mid\mathbf{w})$ 声学模型 ≈ HMM，$P(\mathbf{w})$ 语言模型 ≈ n-gram。）

---

## 5. 关键推导

**推导：CRF 特征如何编码 BIO 约束**。

转移特征 $f_k(y_{t-1}, y_t) = \mathbb{1}[y_{t-1} = O, y_t = I\text{-}X]$（任意 $X$）配负权重——模型学到"I 不能跟 O"；解码（Viterbi）自然避免非法序列。约束进**特征 + 权重**，而非硬编码规则。∎

**推导：为什么 NER 用实体级 F1 而非词级**。
实体是"整体"（一个实体识别对错看整段）；词级正确率会把"识别出半个实体"算对。实体级 F1 反映任务真实目标（信息抽取质量）。∎

**推导：HMM 语音识别 = 贝叶斯组合**。
$\arg\max_\mathbf{w} P(\mathbf{w} \mid \text{audio}) \propto \arg\max_\mathbf{w} P(\text{audio} \mid \mathbf{w}) P(\mathbf{w})$——声学模型（HMM）× 语言模型（先验）。∎

---

## 6. 最小可手算例子

**例（POS 特征 vs HMM）**：句子 "The bank banked the river"。
- HMM：$P(\text{bank}_2 = V \mid \text{bank}_1 = N)$ 转移可区分，但观测相同（"bank" 两次出现）——HMM 只能靠转移，易错；
- CRF：特征 "前一词是 the → 当前为 N" 与 "后缀 -ed → V" 同时可用，更强。
- **手算**：$f_{\text{-ed}} = \mathbb{1}[y_2 = V \wedge x_2 \text{ 以 } ed \text{ 结尾}] = 1$（banked）→ 势 $\exp(\lambda_{\text{-ed}})$ 支持 $y_2 = V$。

**例（BIO 约束）**："Apple 在 Cupertino" → 标签 `[B-ORG, O, B-LOC]`。若模型给 `[B-ORG, O, I-LOC]`（I 无 B 开头），转移特征负权重压低该序列概率，Viterbi 纠正。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| NER 用词级准确率即可 | **错**。用实体级 F1（整实体匹配） |
| BIO 中 I 可任意出现 | **错**。I 必须跟在同类型 B/I 后（CRF 转移特征约束） |
| HMM 也能用任意特征 | **错**。HMM 观测由状态生成（生成式），特征受结构限制 |
| CRF 需要大量标注 | **部分**。CRF 比 HMM 数据需求高（参数多），但特征可移植/用预训练嵌入 |
| 语音识别 = 纯声学 | **错**。声学（HMM）× 语言模型联合解码 |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 写出 BIO 标签方案与 NER 评价指标。
2. POS 任务中 CRF 相对 HMM 的优势是什么？

### #自测题/中等
3. 设计 3 个 NER 特征（词形/上下文/词典）。
4. 说明语音识别如何组合声学模型与语言模型。

### #自测题/较难
5. 解释"BIO 约束如何通过 CRF 转移特征实现"，并说明 Viterbi 为何自动遵守。

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. B-实体首词、I-实体内部、O-非实体；实体级 F1。
2. CRF 可用任意重叠特征（词形/上下文），HMM 受观测独立限制。
3. 例：$f_1$ 词首大写→B-PER；$f_2$ 前词"in"→B-LOC；$f_3$ 词典匹配机构词表→B-ORG。
4. $\arg\max_w P(\text{audio}\mid w)P(w)$：声学 HMM × n-gram 语言模型。
5. 设 $f_{\text{bad}} = \mathbb{1}[y_{t-1}=O, y_t=I\text{-}X]$ 权重为负 → 序列概率被压低；Viterbi 最大化总权重和，自动避开非法转移。
</details>

---

## 9. 通过标准

- [ ] 能**默写** BIO 方案、NER 评价、语音识别贝叶斯组合；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**设计** POS/NER 特征；
- [ ] 能**说明** CRF 特征如何编码结构约束。

---

## 10. 来源

- Lafferty, McCallum & Pereira (2001). CRFs for sequence data. *ICML*.
- Tjong Kim Sang (2002). Introduction to the CoNLL-2003 shared task (NER).
- Rabiner (1989). HMMs and speech recognition. *Proc. IEEE*. 访问日期：2026-08-07。

---

## 11. 学完后可以完成

```dataview
LIST
FROM "03-Projects/14-概率图模型"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/14-概率图模型"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

> 直接下游：课程 Capstone（可选项）、NLP 全栈课程的序列标注衔接。
