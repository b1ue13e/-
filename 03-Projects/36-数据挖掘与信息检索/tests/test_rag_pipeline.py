import pytest
import os
import sys

# 导入工程模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.rag_pipeline import HybridSearchRAG, calculate_groundedness_faithfulness

def test_rrf_multi_channel_fusion():
    pipeline = HybridSearchRAG(k_rrf=60)
    
    # 模拟真实稀疏召回 (BM25) 与稠密向量召回 (Dense HNSW) 结果
    sparse_list = ["doc_A", "doc_B", "doc_C", "doc_D", "doc_E"]
    dense_list = ["doc_B", "doc_A", "doc_F", "doc_G", "doc_H"]
    
    fused = pipeline.fuse_rankings(sparse_list, dense_list, top_n=3)
    top_doc_ids = [doc_id for doc_id, _ in fused]
    
    # doc_A 与 doc_B 同时在两路排名前 2，其 RRF 得分应显著高于只在一路出现的文档
    assert "doc_A" in top_doc_ids[:2]
    assert "doc_B" in top_doc_ids[:2]
    assert fused[0][1] > fused[2][1]

def test_rag_groundedness_and_hallucination_penalty():
    context = (
        "Inverted Index stores mapping from words to document IDs. "
        "BM25 incorporates term frequency saturation and document length normalization. "
        "Dense retrieval uses bi-encoder embeddings to capture semantic similarity."
    )
    
    # 1. 忠实回答：所有核心事实均来自检索上下文
    faithful_answer = "BM25 incorporates term frequency saturation and document length normalization for inverted index."
    faithfulness_high = calculate_groundedness_faithfulness(faithful_answer, context, n=2)
    assert faithfulness_high >= 0.80

    # 2. 幻觉回答：混入未经检索上下文支撑的臆造内容
    hallucinated_answer = "Quantum computing uses superconducting qubits to teleport database records across parallel universes."
    faithfulness_low = calculate_groundedness_faithfulness(hallucinated_answer, context, n=2)
    assert faithfulness_low < 0.20
