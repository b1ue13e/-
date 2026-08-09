---
type: study
topic: "检索增强生成RAG系统"
course: "数据挖掘与信息检索"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段4-可视化表达与前沿专题]]"
flow: knowledge
kind: concept
upstream: ["[[混合检索系统]]", "[[稠密检索与向量召回]]"]
tags: [学习, 数据挖掘与信息检索]
---
## 💡 动机与架构直觉

大型语言模型（LLM）在专业问答与海量垂直文档检索中存在三大固有瓶颈：
1. **知识时效性截止（Knowledge Cutoff）** 与训练成本高昂；
2. **幻觉（Hallucination）与不可溯源性**：自回归生成易生成虚假事实；
3. **私有领域数据隔离**：企业内部知识库不可直接注入公共权重。

**检索增强生成（Retrieval-Augmented Generation, RAG）** 通过将传统信息检索（IR）与自回归生成（LLM）解耦，形成 **“检索相关证据切片 $\to$ 注入提示词上下文 $\to$ 忠实生成答案并附带溯源出处”** 的端到端闭环。

---

## 📐 核心算法与数学推导

```
                       ┌───────────────────────────────┐
                       │ 用户查询 Query (自然语言)      │
                       └───────────────┬───────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
     ┌──────────────────────┐                      ┌──────────────────────┐
     │ 稀疏检索通道 (BM25)  │                      │ 稠密向量检索 (Dense)  │
     │ 倒排索引 + 词项匹配  │                      │ 语义嵌入 + HNSW 召回 │
     └──────────┬───────────┘                      └──────────┬───────────┘
                │ Rank r_sparse                               │ Rank r_dense
                └──────────────────────┬──────────────────────┘
                                       ▼
                       ┌───────────────────────────────┐
                       │ 倒数排名融合 (RRF Scoring)    │
                       └───────────────┬───────────────┘
                                       ▼ Top-K 候选
                       ┌───────────────────────────────┐
                       │ 交叉编码器精排 (Cross-Encoder)│
                       └───────────────┬───────────────┘
                                       ▼ Top-N 最佳切片
                       ┌───────────────────────────────┐
                       │ 提示词编排与 LLM 溯源生成     │
                       └───────────────────────────────┘
```

### 1. 文档切分与重叠滑动窗口（Chunking Strategy）
设长文档 $D$ 包含 $T$ 个字符，以窗口长度 $L$ 与重叠跨度 $S$（Overlap）进行滑动分块：
$$C_i = D[i \cdot (L - S) : i \cdot (L - S) + L]$$
- **重叠跨度的作用**：防止核心语义事实被硬性截断在两块边界处导致上下文丢失。

### 2. 倒数排名融合（Reciprocal Rank Fusion, RRF）
多路召回（BM25 词法匹配 + 向量稠密语义）通过 RRF 将不同量纲的相关性得分无参数统一：
$$\text{RRF\_Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
- 其中 $M = \{\text{sparse}, \text{dense}\}$ 为检索通道集合；
- $r_m(d)$ 为切片 $d$ 在通道 $m$ 中的排名（Rank，从 1 开始）；
- 常数 $k$（工业常用 $k=60$）用于平滑头部排名的权重，避免单路异常高分统治排序。

### 3. Cross-Encoder 二次精排（Re-ranking）
对多路召回的 Top-$K$ 候选切片，利用双向注意力交叉编码器计算深层交互得分：
$$\text{Score}(q, d) = \text{Softmax}\left(\mathbf{W} \cdot \text{Transformer}([CLS] \circ q \circ [SEP] \circ d)\right)$$

### 4. 生成评估指标（RAG Triad 评估）
- **Context Relevance（上下文相关度）**：$\frac{|C_{\text{useful}}|}{|C_{\text{retrieved}}|}$
- **Groundedness / Faithfulness（忠实度）**：生成内容中可由检索上下文支撑的事实断言比例；
- **Answer Relevance（答案契合度）**：最终生成结果与原始查询 $q$ 的意图匹配度。

---

## 💻 最小 Python 实践：全链路内存 RAG 检索与融合系统

```python
import math
from typing import List, Dict, Tuple
from collections import Counter, defaultdict

class InMemoRAGPipeline:
    def __init__(self, chunk_size: int = 50, chunk_overlap: int = 15):
        self.chunk_size = chunk_size
        self.overlap = chunk_overlap
        self.chunks: List[str] = []
        self.doc_freqs: Dict[str, int] = defaultdict(int)

    def chunk_document(self, doc_text: str) -> List[str]:
        step = self.chunk_size - self.overlap
        chunks = []
        for i in range(0, len(doc_text), step):
            c = doc_text[i : i + self.chunk_size]
            if c:
                chunks.append(c)
        return chunks

    def build_knowledge_base(self, documents: List[str]):
        for doc in documents:
            c_list = self.chunk_document(doc)
            self.chunks.extend(c_list)
        for c in self.chunks:
            for term in set(c.lower().split()):
                self.doc_freqs[term] += 1

    def sparse_bm25_search(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        """通道 1：BM25 词项检索"""
        q_terms = query.lower().split()
        N = len(self.chunks)
        avgdl = sum(len(c.split()) for c in self.chunks) / (N + 1e-9)
        scores = []
        for idx, chunk in enumerate(self.chunks):
            tokens = chunk.lower().split()
            dl = len(tokens)
            tf_map = Counter(tokens)
            score = 0.0
            for t in q_terms:
                if t in tf_map:
                    df = self.doc_freqs.get(t, 1)
                    idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)
                    tf = tf_map[t]
                    num = tf * 2.2
                    den = tf + 1.2 * (1 - 0.75 + 0.75 * (dl / avgdl))
                    score += idf * (num / den)
            scores.append((idx, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def mock_dense_search(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        """通道 2：模拟语义稠密向量检索（基于字符 n-gram Jaccard）"""
        q_set = set(query.lower())
        scores = []
        for idx, chunk in enumerate(self.chunks):
            c_set = set(chunk.lower())
            jaccard = len(q_set & c_set) / (len(q_set | c_set) + 1e-9)
            scores.append((idx, jaccard))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def hybrid_rrf_rerank(self, query: str, k: int = 60, top_n: int = 2) -> List[int]:
        """多路 RRF 融合排序"""
        bm25_res = self.sparse_bm25_search(query, top_k=5)
        dense_res = self.mock_dense_search(query, top_k=5)

        rrf_scores = defaultdict(float)
        for rank, (idx, _) in enumerate(bm25_res, 1):
            rrf_scores[idx] += 1.0 / (k + rank)
        for rank, (idx, _) in enumerate(dense_res, 1):
            rrf_scores[idx] += 1.0 / (k + rank)

        ranked = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return [idx for idx, _ in ranked[:top_n]]

    def generate_grounded_answer(self, query: str) -> Dict[str, str]:
        top_indices = self.hybrid_rrf_rerank(query, top_n=2)
        retrieved_contexts = [f"[{i}] {self.chunks[i]}" for i in top_indices]
        context_block = "\n".join(retrieved_contexts)
        
        # 模拟合成可溯源回答
        answer = f"基于引用资料：{retrieved_contexts[0]}，针对问题【{query}】的回答已准确对齐证据。"
        return {
            "query": query,
            "context": context_block,
            "answer": answer,
            "sources": str(top_indices)
        }

# 驱动验证
if __name__ == "__main__":
    rag = InMemoRAGPipeline(chunk_size=40, chunk_overlap=10)
    docs = [
        "Inverted Index is the core data structure for search engines. It maps terms to posting lists of document IDs.",
        "Retrieval Augmented Generation combines BM25 dense embeddings and Large Language Models to avoid hallucination."
    ]
    rag.build_knowledge_base(docs)
    result = rag.generate_grounded_answer("How does RAG avoid hallucination?")
    print("=== RAG Pipeline Output ===")
    print("Context:\n", result["context"])
    print("Answer:\n", result["answer"])
```

---

## ⚠️ 常见误区与避坑指南

1. **误区 1：迷信 Pure Dense 向量检索，弃用 BM25**
   - **机制**：Dense Embedding 对专有名词、产品型号（如 `iPhone 15 Pro`）、错误码（如 `ERR_404_NOT_FOUND`）存在灾难性语义模糊（语义空间距离不敏感）。
   - **工业对策**：必须使用 **Hybrid Search（BM25 稀疏精确词项 + Dense 向量语义）** 并结合 RRF 融合。

2. **误区 2：Lost in the Middle 现象**
   - **机制**：LLM 对超长 Context 窗口的头部与尾部信息敏感，位于中段的检索切片极易被忽略。
   - **工业对策**：限制 RAG 注入切片数量（Top 3~5），并对上下文按相关度得分进行重排序（将最相关切片置于首部和尾部）。

---

## 🃏 Anki 卡片

**Q: 什么是 RRF（Reciprocal Rank Fusion）？为什么在 RAG 多路召回中优于直接分数加权？**
**A**:
- **定义**：$\text{RRF}(d) = \sum_{m} \frac{1}{k + r_m(d)}$，根据文档在各通道的排名倒数进行加权求和。
- **优势**：BM25 得分（0~100+）与余弦相似度（-1~1）属于完全不同的得分分布且无标准化边界。RRF 纯基于离散排名，无需校准与调节通道权重即可实现鲁棒融合。

---

## 🔗 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```