---
type: study
topic: "检索增强生成RAG"
course: "08-NLP全栈"
created: 2026-08-06
status: active
stage_moc: "[[🧭 阶段5-大语言模型与前沿技术]]"
upstream: ["[[08-NLP全栈-BERT模型]]", "[[08-NLP全栈-提示工程]]"]
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["RAG", "Vector Database", "Embedding", "Chunking", "Rerank"]
prerequisites: ["BERT模型", "余弦相似度", "Prompt Engineering"]
related: ["提示工程", "Agent与工具使用", "向量数据库"]
anki_deck: NLP::LLM
anki_tags: ['#nlp', '#rag', '#llm']
assessment_exempt: false
---

# 08-NLP全栈-检索增强生成RAG

> ⏱ **预计学习耗时**：50 分钟  
> 🎯 **学习行为目标**：掌握 RAG 的经典三阶段（Indexing, Retrieval, Generation）；理解文本切片（Chunking）策略与余弦向量相似度检索；能够用 Python 结合向量库实现简易知识库问答 RAG Pipeline。

---

## 0. 核心概念与直觉起步

### 为什么需要 RAG？
大语言模型 (LLM) 存在**幻觉 (Hallucination)**、**时效性滞后**以及**缺少私域知识**三大痛点。
**RAG (Retrieval-Augmented Generation)** 将外部知识库嵌入向量空间，在回答用户问题时，先去知识库中检索相关文档 Top-K 块（Chunk），将检索到的上下文与原始问题拼成 Prompt 送给 LLM 生成解答。

```text
[RAG 标准运作架构]
用户提问 Q ──► [ Dense Embedding ] ──► 向量 Query ──┐
                                                    ▼
知识库文件 ──► Chunking ──► Embedding ──► [ Vector DB 检索 Top-K ]
                                                    │
                                                    ▼
                                            上下文 Context + Q
                                                    │
                                                    ▼
                                          [ LLM 生成可信回答 ]
```

---

## 1. 核心流程与三阶段拆解

1. **索引阶段 (Indexing)**：文档切分（如按 512 字符 + 50 字符 Overlap） $\rightarrow$ 嵌入矩阵编码 $\rightarrow$ 写入 Vector DB。
2. **检索阶段 (Retrieval)**：用户 Query 向量化 $\rightarrow$ 余弦相似度 / 欧式距离寻找相似 Top-K $\rightarrow$ (可选) 重排模型 (Reranker) 重新精打分。
3. **生成阶段 (Generation)**：结合 Prompt 模板构建 System Message，让大模型在约束范围内输出回答。

---

## 3. Python 可运行简易 RAG Pipeline 实现

```python
import numpy as np
from typing import List, Dict

class SimpleVectorRAG:
    """基于 Cosine Similarity 的极简内嵌 RAG 系统"""
    def __init__(self, mock_embedding_fn):
        self.embed_fn = mock_embedding_fn
        self.doc_chunks: List[str] = []
        self.vectors: List[np.ndarray] = []

    def add_documents(self, docs: List[str]):
        for doc in docs:
            self.doc_chunks.append(doc)
            v = self.embed_fn(doc)
            self.vectors.append(v / np.linalg.norm(v)) # L2 归一化

    def retrieve(self, query: str, top_k: int = 2) -> List[str]:
        q_vec = self.embed_fn(query)
        q_vec = q_vec / np.linalg.norm(q_vec)
        
        # 计算余弦相似度
        scores = [np.dot(q_vec, d_vec) for d_vec in self.vectors]
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self.doc_chunks[i] for i in top_indices]

    def generate_prompt(self, query: str, top_k: int = 2) -> str:
        retrieved_docs = self.retrieve(query, top_k=top_k)
        context_str = "\n".join([f"- {d}" for d in retrieved_docs])
        prompt = f"请根据以下参考资料回答问题。如果资料中未提及，请回答不知道。\n\n【资料】:\n{context_str}\n\n【问题】: {query}\n【回答】:"
        return prompt
```

---

## 12. My Guided Recall (主动回忆)

1. RAG 三大核心阶段分别是 `____`（索引）、`____`（检索）与 `____`（生成）。
2. 在切分较长长文本时，添加一定比例的 `____`（重叠度）可以有效防止信息在切片边界处丢失。
3. 如果模型输出了知识库中完全未提及的编造信息，这种现象被称为 `____`。

---

## 13. 闭卷提取自测

### 基础题
为什么在 RAG 检索后常常需要加入 Reranker（重排模型）？

<details>
<summary>▶ 答案与解释</summary>

初检索（通常用 Embedding 余弦相似度或 BM25）虽然速度快，但只能捕捉到双向表示在空间上的全局粗粒度相似度；而 Reranker 使用 Cross-Encoder 模型将 Query 和 Candidate Chunk 拼接后整体算 Attention，能够捕捉到极高精度的局部匹配语义，大幅提升 Prompt 中 Context 的相关度。
</details>

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




## 5. 常见误区与对比矩阵

| 评估维度 / 特性 | 方案 A / 经典范式 | 方案 B / 改进范式 | 权衡与选型建议 (Trade-offs) |
| :--- | :--- | :--- | :--- |
| **计算复杂度** | $\mathcal{O}(N^2)$ 或传统高阶复杂度 | $\mathcal{O}(N \log N)$ 或近似线性复杂度 | 高并发生产环境优先选择低复杂度方案 |
| **显存 / 存储占用** | 占用较高，受限于序列长度/维度 | 优化压缩，支持 Memory-efficient | 边缘设备或资源受限场景推荐优化方案 |
| **表征能力与精度** | 基础表达，易受局部噪声干扰 | 强特征提取，捕捉长距离依赖 | 高精度需求任务（如长文本理解/生成）推荐改进范式 |
| **工程落地门槛** | 开箱即用，工具链极为成熟 | 需特定依赖库 (如 CUDA / Triton) | 开发初期快速原型验证使用经典范式 |


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《检索增强生成RAG》的核心机制及其与上下游模块的连接逻辑。
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
