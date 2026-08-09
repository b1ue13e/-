import pytest
import os
import sys
import numpy as np

# 导入工程模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.dense_search import DenseVectorIndex, RocchioFeedback

def test_ivf_flat_indexing_and_nprobe_recall():
    np.random.seed(42)
    dim = 16
    n_docs = 50
    doc_ids = [f"doc_{i}" for i in range(n_docs)]
    vectors = np.random.randn(n_docs, dim)
    
    index = DenseVectorIndex(dim=dim, nlist=5, nprobe=3)
    index.train_and_build(doc_ids, vectors)
    
    # 用第 0 个文档的向量作为精确查询
    query_vec = vectors[0]
    results = index.search(query_vec, top_k=5)
    
    assert len(results) > 0
    top_doc_id, top_sim = results[0]
    # 精确匹配的余弦相似度应当为 1.0 (或极其接近)
    assert top_doc_id == "doc_0"
    assert abs(top_sim - 1.0) < 1e-4

def test_rocchio_pseudo_relevance_feedback_shift():
    dim = 8
    q0 = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    
    # 模拟反馈：正相关文档在第 1 维和第 2 维有强特征
    d_rel = np.array([
        [0.8, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.7, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ])
    # 负相关文档
    d_non_rel = np.array([
        [0.0, 0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0]
    ])
    
    rocchio = RocchioFeedback(alpha=1.0, beta=0.75, gamma=0.25)
    q_new = rocchio.shift_query_vector(q0, d_rel, d_non_rel)
    
    # 验证新查询在第 1 维权重显著上升，第 2 维受惩罚抑制
    assert q_new[1] > 0.2
    assert q_new[2] < 0.0
    assert abs(np.linalg.norm(q_new) - 1.0) < 1e-5
