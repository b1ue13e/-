---
sources: ['Rabiner, L. R. (1989). A tutorial on Hidden Markov Models and selected applications in speech recognition. Proceedings of the IEEE.', 'Lafferty, J., McCallum, A., & Pereira, F. C. (2001). Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data. ICML 2001.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "序列标注"
created: 2026-08-06
status: completed
assessment_exempt: false
difficulty: intermediate
stage_moc: "[[🧭 阶段2-传统NLP方法]]"
upstream: ["[[08-NLP全栈-统计机器学习]]"]
tags: [学习, NLP, 序列标注, HMM, CRF, 维特比算法, NER, POS]
---

# 08-NLP全栈-序列标注

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 简单文本分类是对整篇文档给出一个分类标签（1-to-1）。但在词性标注 (POS) 和命名实体识别 (NER) 中，必须给输入文本序列中的每个 Token 都预测一个对应的类别标签（Sequence-to-Sequence 同长标注），且标签之间存在强约束（如 BIO 标注规范中 `I-PER` 绝不能接在 `B-LOC` 后面）。隐藏马尔可夫模型 (HMM) 与条件随机场 (CRF) 正是解决此类问题的经典概率模型。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是经典 HMM/CRF、BiLSTM-CRF 实体识别模型以及 Transformer Token Classification 头的理论源头。
- **实际应用场景**：POS 词性标注、NER 命名实体识别、中文分词（转换为 BMES 序列标注问题）、维特比算法 (Viterbi Decoding) 最优路径解码。

---

## 3. 正式定义与核心算法

### 1. 隐藏马尔可夫模型 (HMM)

HMM 是生成式模型，假设存在隐藏状态序列 $Y = (y_1, \dots, y_T)$ 和观察序列 $X = (x_1, \dots, x_T)$。

联合概率展开为转移概率与发射概率之积：

$$P(X, Y) = \prod_{t=1}^T P(y_t \mid y_{t-1}) P(x_t \mid y_t)$$

### 2. 条件随机场 (CRF)

CRF 是判别式无向图模型，直接建模条件概率 $P(Y \mid X)$：

$$P(Y \mid X) = \frac{1}{Z(X)} \exp \left( \sum_{t=1}^T \sum_k w_k f_k(y_{t-1}, y_t, X, t) \right)$$

其中 $Z(X)$ 为归一化配分函数，保证概率之和为 1。

### 3. 维特比解码算法 (Viterbi Algorithm)

利用动态规划在线性时间内求解最优隐状态序列 $Y^* = \arg\max_Y P(Y \mid X)$：

$$v_t(j) = \max_i \left[ v_{t-1}(i) \cdot a_{ij} \right] \cdot b_j(x_t)$$

---

## 4. Python 实现：利用 sklearn-crfsuite 进行 NER 标注

```python
import sklearn_crfsuite

# 构建简易训练特征与标签
X_train = [
    [{'word': 'Barack', 'is_capital': True}, {'word': 'Obama', 'is_capital': True}, {'word': 'visited', 'is_capital': False}, {'word': 'Paris', 'is_capital': True}]
]
y_train = [
    ['B-PER', 'I-PER', 'O', 'B-LOC']
]

# 训练 CRF 模型
crf = sklearn_crfsuite.CRF(algorithm='lbfgs', max_iterations=100)
crf.fit(X_train, y_train)

# 预测新序列
y_pred = crf.predict(X_train)
print("Predicted Sequence Labels:", y_pred[0])
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

### 误区：HMM 与 CRF 的根本区别
- **HMM (生成式模型)**：对联合概率 $P(X, Y)$ 建模，要求强假设（独立发射与一阶马尔可夫链），无法直接利用重叠上下文特征。
- **CRF (判别式模型)**：对条件概率 $P(Y \mid X)$ 建模，可引入任意全局上下文特征，且彻底解决了 HMM 的标注偏置问题 (Label Bias Problem)。

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

- Rabiner, L. R. (1989). A tutorial on Hidden Markov Models and selected applications in speech recognition. *Proceedings of the IEEE*.
- Lafferty, J., McCallum, A., & Pereira, F. C. (2001). Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data. *ICML 2001*.


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《序列标注》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《序列标注》的核心机制及其与上下游模块的连接逻辑。
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
