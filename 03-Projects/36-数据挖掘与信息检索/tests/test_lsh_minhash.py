import pytest
import os
import sys
import numpy as np

# 导入工程模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.lsh_minhash import MinHashLSH

def test_minhash_signature_and_jaccard_consistency():
    lsh = MinHashLSH(num_perm=100, num_bands=25)
    
    text_1 = "Data mining algorithms extract interesting patterns from massive datasets using association rules."
    text_2 = "Data mining systems extract useful patterns from massive datasets using association rules."
    text_3 = "Quantum mechanics explores wave particle duality and atomic energy states in physics."
    
    shingles_1 = MinHashLSH.get_shingles(text_1, k=1)
    shingles_2 = MinHashLSH.get_shingles(text_2, k=1)
    shingles_3 = MinHashLSH.get_shingles(text_3, k=1)
    
    exact_jaccard_1_2 = MinHashLSH.jaccard_similarity(shingles_1, shingles_2)
    exact_jaccard_1_3 = MinHashLSH.jaccard_similarity(shingles_1, shingles_3)
    
    lsh.insert("doc_1", shingles_1)
    lsh.insert("doc_2", shingles_2)
    lsh.insert("doc_3", shingles_3)
    
    est_jaccard_1_2 = lsh.estimate_similarity("doc_1", "doc_2")
    est_jaccard_1_3 = lsh.estimate_similarity("doc_1", "doc_3")
    
    # 验证估计相似度与真实 Jaccard 相似度高度一致
    assert abs(est_jaccard_1_2 - exact_jaccard_1_2) < 0.20
    assert abs(est_jaccard_1_3 - exact_jaccard_1_3) < 0.10
    assert est_jaccard_1_2 > est_jaccard_1_3

def test_lsh_candidate_pair_retrieval():
    lsh = MinHashLSH(num_perm=100, num_bands=25)
    
    text_original = "Inverted index and BM25 ranking are the cornerstones of modern text retrieval search systems."
    text_near_dup = "Inverted index and BM25 ranking are the cornerstones of modern text retrieval search engines."
    text_unrelated = "Convolutional neural networks process 2D spatial grid images with kernel filters in vision."
    
    shingles_orig = MinHashLSH.get_shingles(text_original, k=1)
    shingles_near = MinHashLSH.get_shingles(text_near_dup, k=1)
    shingles_unrelated = MinHashLSH.get_shingles(text_unrelated, k=1)
    
    lsh.insert("orig", shingles_orig)
    lsh.insert("near_dup", shingles_near)
    lsh.insert("unrelated", shingles_unrelated)
    
    candidates = lsh.query_candidates("orig")
    # 高相似度文档必须被召回为候选对，而无关文档不应被碰撞召回
    assert "near_dup" in candidates
    assert "unrelated" not in candidates
