---
type: project
project_type: homework
course: "数据挖掘与信息检索"
assignment_id: "36-CAPSTONE-01"
assignment_level: capstone
assignment_format: project
stage_id: "04"
requires: ["[[混合检索系统]]", "[[检索增强生成RAG系统]]", "[[搜索前沿研究综述]]", "[[信息检索的前沿研究]]", "[[倒排索引系统]]", "[[稠密检索与向量召回]]"]
source_type: open_source_project_task
source_url: "https://www.langchain.com/"
created: 2026-08-07
status: completed
flow: project
tags: [大作业, 综合项目, RAG, 混合检索, 搜索引擎]
---

# 36-数据挖掘与信息检索 - 大作业：端到端海量文档混合搜索与 RAG 检索增强生成系统

> **项目定位**：融合经典信息检索（BM25 词项索引）与前沿大模型检索增强技术（Dense Embedding + HNSW + Cross-Encoder + RRF 融合 + 忠实度生成），打造具备工业级性能的端到端可落地检索增强生成系统。

---

## 🎯 学习目标

本大作业为整门课程的终极 Capstone 综合实战项目，学习目标包括：
1. **多路混合召回引擎（Hybrid Search）**：
   - 稀疏检索通道：构建基于 BM25 的倒排索引；
   - 稠密检索通道：构建基于语义向量余弦相似度的近邻召回通道；
   - 融合排序：实现倒数排名融合（RRF, $k=60$），将多路异构得分平滑对齐；
2. **Cross-Encoder 交叉重排与上下文压缩**：
   - 提取 Top-20 候选切片，利用双向注意力机制计算深层交互相关度，精选 Top-5 证据切片；
3. **可溯源生成与防幻觉评测（RAGAS Triad）**：
   - 注入结构化 Prompt 并生成带有精准引用角标 `[1]`, `[2]` 的回答；
   - 从 Context Relevance、Faithfulness（忠实度）与 Answer Relevance 三个维度实现自动化自评。

---

## 🔒 任务边界与环境要求

- **代码规范**：清晰的类与模块封装（`HybridRetriever`, `RRFReranker`, `RAGPipeline`）；
- **数据输入**：`data/sample_documents.json`（支持多主题长文档自动切块）；
- **测试验收**：必须 100% 通过 `pytest tests/` 下所有单元测试与集成测试，全维评估得分 $\ge 85$。

---

## 📝 题目详细内容

### 任务 1：文档切块与多路倒排建立
1. 将长文本按 100 字符切块，重叠跨度 20 字符；
2. 建立词项倒排表与全局 IDF 统计，同时生成文档切片的稠密语义向量。

### 任务 2：RRF 倒数排名融合算法实现
实现 RRF 融合公式：
$$\text{RRF\_Score}(d) = \sum_{m \in \{\text{sparse}, \text{dense}\}} \frac{1}{60 + r_m(d)}$$
输出 Top-10 综合推荐候选。

### 任务 3：回答生成与可信度自评
构建结构化 Prompt，生成带有引用出处的文本答案，并通过上下文匹配计算生成忠实度得分（Faithfulness $\ge 0.9$）。

---

## 💻 核心架构与工程 Starter Code

```python
import math
from typing import List, Dict, Tuple, Any
from collections import defaultdict, Counter

class ProductionRAGSystem:
    def __init__(self, chunk_size: int = 100, chunk_overlap: int = 20, rrf_k: int = 60):
        self.chunk_size = chunk_size
        self.overlap = chunk_overlap
        self.rrf_k = rrf_k
        self.chunks: List[str] = []
        self.doc_freqs: Dict[str, int] = defaultdict(int)

    def ingest_documents(self, raw_docs: List[str]):
        """分块与词频统计"""
        step = self.chunk_size - self.overlap
        for doc in raw_docs:
            for i in range(0, len(doc), step):
                chunk = doc[i : i + self.chunk_size]
                if chunk:
                    self.chunks.append(chunk)
        for c in self.chunks:
            for term in set(c.lower().split()):
                self.doc_freqs[term] += 1

    def hybrid_search_and_fuse(self, query: str, top_n: int = 3) -> List[Tuple[int, float]]:
        """实现 BM25 + 稠密模拟 + RRF 融合"""
        q_tokens = query.lower().split()
        N = len(self.chunks)
        
        # 1. 稀疏得分
        sparse_scores = []
        for idx, chunk in enumerate(self.chunks):
            tokens = chunk.lower().split()
            tf_map = Counter(tokens)
            score = sum(math.log((N - self.doc_freqs.get(t, 0) + 0.5) / (self.doc_freqs.get(t, 0) + 0.5) + 1.0) * tf_map[t] for t in q_tokens)
            sparse_scores.append((idx, score))
        sparse_ranked = sorted(sparse_scores, key=lambda x: x[1], reverse=True)

        # 2. 稠密得分
        q_set = set(query.lower())
        dense_scores = []
        for idx, chunk in enumerate(self.chunks):
            c_set = set(chunk.lower())
            jaccard = len(q_set & c_set) / (len(q_set | c_set) + 1e-9)
            dense_scores.append((idx, jaccard))
        dense_ranked = sorted(dense_scores, key=lambda x: x[1], reverse=True)

        # 3. RRF 融合
        rrf_map = defaultdict(float)
        for rank, (idx, _) in enumerate(sparse_ranked, 1):
            rrf_map[idx] += 1.0 / (self.rrf_k + rank)
        for rank, (idx, _) in enumerate(dense_ranked, 1):
            rrf_map[idx] += 1.0 / (self.rrf_k + rank)

        return sorted(rrf_map.items(), key=lambda x: x[1], reverse=True)[:top_n]
```

---

## 📐 评分标准 (Rubric)

- **[30%] 混合检索与 RRF 融合**：稀疏与稠密双通道召回及融合算法严谨；
- **[30%] 精排与上下文编排**：切块重叠设计合理，Prompt 上下文注入规范；
- **[25%] 可溯源生成与评估**：具备回答溯源出处与忠实度校验逻辑；
- **[15%] 工程实现与测试**：代码架构优良，全量单元与集成测试通过。

---

## 📦 提交产物

1. 完整生产代码：`capstone_rag_system.py`；
2. 全链路测试用例及端到端运行演示日志。

---

## 💡 引导与自检

- **思考 1**：为什么在多路召回中，直接将 BM25 得分与余弦相似度线性相加（如 $\text{score} = \alpha S_{\text{bm25}} + \beta S_{\text{dense}}$）往往效果不佳？
- **思考 2**：如何通过自动化断言检测大模型生成内容是否存在无证据支撑的幻觉？
- **自检**：运行 `pytest tests/test_rag_pipeline.py` 验证端到端召回与评估。
