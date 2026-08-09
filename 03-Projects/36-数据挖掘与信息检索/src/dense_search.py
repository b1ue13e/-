"""
稠密向量检索与伪相关反馈模块：IVF-Flat 质心多探针索引与 Rocchio 向量漂移优化
"""

import numpy as np
from typing import List, Dict, Tuple, Optional

class DenseVectorIndex:
    """
    IVF-Flat (Inverted File Flat) 稠密向量索引引擎
    - 训练阶段：K-Means 聚类生成 nlist 个 Voronoi 空间质心 (Centroids)
    - 构建阶段：将高维向量按最近质心分配到对应的倒排列表 (Inverted Lists)
    - 检索阶段：对查询向量先找最近的 nprobe 个质心，仅在候选倒排桶内执行精确内积/余弦计算
    """
    def __init__(self, dim: int, nlist: int = 4, nprobe: int = 2):
        self.dim = dim
        self.nlist = nlist
        self.nprobe = min(nprobe, nlist)
        self.centroids: Optional[np.ndarray] = None
        self.inv_lists: Dict[int, List[Tuple[str, np.ndarray]]] = {i: [] for i in range(nlist)}
        self.doc_vectors: Dict[str, np.ndarray] = {}

    @staticmethod
    def _normalize(vecs: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vecs, axis=-1, keepdims=True)
        norms[norms == 0] = 1e-12
        return vecs / norms

    def train_and_build(self, doc_ids: List[str], vectors: np.ndarray, max_iter: int = 20):
        assert len(doc_ids) == vectors.shape[0]
        vectors = self._normalize(vectors)
        for d_id, vec in zip(doc_ids, vectors):
            self.doc_vectors[d_id] = vec

        N = vectors.shape[0]
        actual_nlist = min(self.nlist, N)
        np.random.seed(42)
        # 初始化质心
        init_indices = np.random.choice(N, actual_nlist, replace=False)
        self.centroids = vectors[init_indices].copy()

        # K-Means 迭代优化质心
        for _ in range(max_iter):
            # (N, nlist)
            sim_matrix = np.dot(vectors, self.centroids.T)
            assignments = np.argmax(sim_matrix, axis=1)
            
            new_centroids = np.zeros_like(self.centroids)
            for c_idx in range(actual_nlist):
                members = vectors[assignments == c_idx]
                if len(members) > 0:
                    new_centroids[c_idx] = np.mean(members, axis=0)
                else:
                    new_centroids[c_idx] = self.centroids[c_idx]
            self.centroids = self._normalize(new_centroids)

        # 构建倒排链表
        for c_idx in range(self.nlist):
            self.inv_lists[c_idx] = []

        sim_matrix = np.dot(vectors, self.centroids.T)
        assignments = np.argmax(sim_matrix, axis=1)
        for i, (d_id, c_idx) in enumerate(zip(doc_ids, assignments)):
            self.inv_lists[int(c_idx)].append((d_id, vectors[i]))

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        if self.centroids is None:
            return []
        q_norm = self._normalize(query_vector.reshape(1, -1)).squeeze(0)
        
        # 1. 计算查询向量与所有质心的余弦相似度
        centroid_sims = np.dot(self.centroids, q_norm)
        # 2. 选取最相似的 nprobe 个质心
        probe_indices = np.argsort(centroid_sims)[::-1][:self.nprobe]
        
        # 3. 遍历候选质心桶内的所有向量
        candidates: List[Tuple[str, float]] = []
        for c_idx in probe_indices:
            bucket = self.inv_lists.get(int(c_idx), [])
            for d_id, d_vec in bucket:
                score = float(np.dot(d_vec, q_norm))
                candidates.append((d_id, score))
                
        # 4. 全局 Top-K 排序
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:top_k]


class RocchioFeedback:
    """
    Rocchio 伪相关反馈 (Pseudo-Relevance Feedback) 向量偏移
    q_new = alpha * q_0 + beta * (1 / |Dr|) * sum(Dr) - gamma * (1 / |Dnr|) * sum(Dnr)
    """
    def __init__(self, alpha: float = 1.0, beta: float = 0.75, gamma: float = 0.15):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def shift_query_vector(self, query_vec: np.ndarray, relevant_vecs: np.ndarray, non_relevant_vecs: Optional[np.ndarray] = None) -> np.ndarray:
        q_shifted = self.alpha * query_vec
        if relevant_vecs is not None and len(relevant_vecs) > 0:
            q_shifted += self.beta * np.mean(relevant_vecs, axis=0)
        if non_relevant_vecs is not None and len(non_relevant_vecs) > 0:
            q_shifted -= self.gamma * np.mean(non_relevant_vecs, axis=0)
            
        norm = np.linalg.norm(q_shifted)
        if norm > 0:
            q_shifted = q_shifted / norm
        return q_shifted
