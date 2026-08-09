---
type: project
project_type: homework
course: "数据挖掘与信息检索"
assignment_id: "36-HW-05"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[稠密检索与向量召回]]", "[[查询扩展与伪相关反馈]]", "[[查询分析与纠错]]", "[[检索评测与AB测试]]"]
source_type: official_assignment
source_url: "https://github.com/facebookresearch/faiss"
created: 2026-08-07
status: completed
flow: project
tags: [作业, 向量检索, FAISS]
---

# 36-数据挖掘与信息检索 - 课后作业 05：稠密向量检索、FAISS 倒排量化与 Rocchio 伪相关反馈

> **名校开源出处**：[Facebook AI Research: FAISS Vector Search Tutorial & Stanford CS276 Feedback Lab](https://github.com/facebookresearch/faiss)

---

## 🎯 学习目标

1. 实现基于余弦相似度与内积的高维稠密向量空间最近邻（Exact Flat k-NN）；
2. 掌握并复现 **IVF-Flat（Inverted File with Flat Quantization）** 倒排索引与聚类中心划分；
3. 实现基于 **Rocchio 伪相关反馈（Pseudo-Relevance Feedback, PRF）** 的查询向量漂移与扩展优化；
4. 掌握检索评测标准指标（MRR, NDCG@K）并进行 A/B 测试统计显著性检验（t-test / bootstrap）。

---

## 🔒 任务边界与环境约束

- **技术约束**：纯 Python 3 / NumPy 实现 IVF 聚类倒排与 Rocchio 向量加权；
- **输入数据**：高维 Document Embeddings 与 Query Embeddings 矩阵；
- **自动化验收**：必须 100% 通过 `pytest tests/test_vector_dense_search.py`。

---

## 📝 题目详细内容

### 任务 1：高维向量相似度检索与精确 Top-K
计算查询向量 $\mathbf{q}$ 与所有文档向量 $\mathbf{d}_i$ 的余弦相似度：
$$\text{Cosine}(\mathbf{q}, \mathbf{d}) = \frac{\mathbf{q} \cdot \mathbf{d}}{\|\mathbf{q}\|_2 \|\mathbf{d}\|_2}$$

### 任务 2：IVF-Flat 倒排量化索引实现
1. 训练阶段：使用 K-Means 在文档向量空间聚类出 $C$ 个质心（Centroids）；
2. 构建倒排表：将每个文档分配至最近的质心倒排链表中；
3. 查询阶段（`nprobe` 调优）：仅在距离查询最近的 `nprobe` 个质心对应的倒排列表中检索，实现毫秒级近似最近邻（ANN）。

### 任务 3：Rocchio 伪相关反馈查询向量更新
利用首轮召回的 Top-$K$ 篇文档（伪正例 $D_r$）与低分文档（伪负例 $D_{nr}$）更新查询向量：
$$\mathbf{q}_m = \alpha \mathbf{q}_0 + \frac{\beta}{|D_r|} \sum_{\mathbf{d} \in D_r} \mathbf{d} - \frac{\gamma}{|D_{nr}|} \sum_{\mathbf{d} \in D_{nr}} \mathbf{d}$$

---

## 💻 Starter Code 骨架

```python
import numpy as np
from typing import List, Tuple, Dict
from collections import defaultdict

class InvertedFileIndex:
    def __init__(self, n_centroids: int = 4, nprobe: int = 2):
        self.n_centroids = n_centroids
        self.nprobe = nprobe
        self.centroids: np.ndarray = None
        self.inverted_lists: Dict[int, List[int]] = defaultdict(list)
        self.vectors: np.ndarray = None

    def train_and_index(self, doc_vectors: np.ndarray):
        self.vectors = doc_vectors / (np.linalg.norm(doc_vectors, axis=1, keepdims=True) + 1e-9)
        np.random.seed(42)
        idx = np.random.choice(len(doc_vectors), self.n_centroids, replace=False)
        self.centroids = self.vectors[idx].copy()
        
        sims = np.dot(self.vectors, self.centroids.T)
        cluster_assignments = np.argmax(sims, axis=1)
        for doc_id, c_id in enumerate(cluster_assignments):
            self.inverted_lists[c_id].append(doc_id)

    def search(self, query_vec: np.ndarray, top_k: int = 3) -> List[Tuple[int, float]]:
        q_norm = query_vec / (np.linalg.norm(query_vec) + 1e-9)
        c_sims = np.dot(self.centroids, q_norm)
        best_centroids = np.argsort(c_sims)[::-1][:self.nprobe]
        
        candidates = []
        for c_id in best_centroids:
            candidates.extend(self.inverted_lists[c_id])
            
        cand_vecs = self.vectors[candidates]
        scores = np.dot(cand_vecs, q_norm)
        ranked_idx = np.argsort(scores)[::-1][:top_k]
        return [(candidates[i], float(scores[i])) for i in ranked_idx]
```

---

## 📐 评分标准 (Rubric)

- **[35%] IVF 索引结构与近邻查找**：质心划分与 `nprobe` 剪枝搜索逻辑正确；
- **[35%] Rocchio PRF 向量优化**：向量更新公式精确无溢出，显著提升排序得分；
- **[15%] 检索评测指标（MRR/NDCG）**：指标实现符合 TREC 工业标准；
- **[15%] 单元测试**：100% 通过 `pytest tests/test_vector_dense_search.py`。

---

## 📦 提交产物

1. 源码实现：`hw5_dense_search.py`；
2. 单元测试验证：稠密检索与 PRF 反馈测试通过。

---

## 💡 引导与自检

- **思考 1**：当 IVF 的 `nprobe=1` 时检索速度最快，但召回率（Recall）可能会损失多少？
- **思考 2**：Rocchio 公式中将负样本权重 $\gamma$ 设得过大可能导致什么退化现象？
- **自检**：运行测试验证反馈后的向量偏移趋势。
