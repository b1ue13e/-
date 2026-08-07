"""
大作业 Capstone 单元测试: test_rag_pipeline.py
测试 BM25 稀疏检索、RRF 融合与 Error Audit 指标
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.hybrid_rag import BM25Retriever, reciprocal_rank_fusion
from scripts.error_audit import compute_retrieval_metrics


def test_bm25_retriever():
    corpus = [
        "Deep learning models for natural language processing",
        "Computer vision and image classification using CNNs",
        "Natural language processing with PyTorch and Transformers"
    ]
    bm25 = BM25Retriever(corpus)
    scores = bm25.get_scores("natural language processing")
    
    assert len(scores) == 3
    # 文档 0 与 文档 2 应该包含相关词，得分高于文档 1
    assert scores[0] > scores[1]
    assert scores[2] > scores[1]


def test_reciprocal_rank_fusion():
    dense_ranks = [1, 2, 3, 4]
    sparse_ranks = [2, 1, 4, 3]
    
    fused_docs = reciprocal_rank_fusion(dense_ranks, sparse_ranks, k=60)
    
    assert len(fused_docs) == 4
    # 文档 1 和 2 应该排在前两位
    assert fused_docs[0] in [1, 2]
    assert fused_docs[1] in [1, 2]


def test_retrieval_metrics():
    retrieved = [10, 20, 30, 40, 50]
    ground_truth = [20, 60]
    
    metrics = compute_retrieval_metrics(retrieved, ground_truth, k_list=[1, 3])
    
    assert "Precision@1" in metrics
    assert "Recall@3" in metrics
    assert "MRR" in metrics
    
    # 命中在位置 2 (1-indexed)，MRR 应该为 0.5
    assert abs(metrics["MRR"] - 0.5) < 1e-4
