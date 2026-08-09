import pytest
import os
import sys

# 导入工程模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.inverted_index import VariableByteCodec, InvertedIndex, BM25Scorer

def test_variable_byte_encoding_and_compression_ratio():
    # 测试常规数字与大数字编码
    raw_numbers = [5, 128, 500, 16384, 2097152]
    encoded_bytes = bytearray()
    for n in raw_numbers:
        encoded_bytes.extend(VariableByteCodec.encode_number(n))
        
    decoded = VariableByteCodec.decode_numbers(bytes(encoded_bytes))
    assert decoded == raw_numbers

def test_d_gaps_monotonic_compression():
    doc_ids = [100, 102, 105, 120, 250, 260, 300]
    compressed = VariableByteCodec.encode_gaps(doc_ids)
    
    # 相比 4-byte 整数存储，VB d-gaps 具备极高的压缩率
    raw_size = len(doc_ids) * 4
    compressed_size = len(compressed)
    assert compressed_size < raw_size
    
    recovered = VariableByteCodec.decode_gaps(compressed)
    assert recovered == doc_ids

def test_inverted_index_boolean_intersection_and_bm25():
    index = InvertedIndex(use_compression=True)
    
    index.add_document("doc_1", "information retrieval systems build inverted indexes for keyword search")
    index.add_document("doc_2", "dense retrieval and vector search models retrieve semantic information")
    index.add_document("doc_3", "inverted indexes compress posting lists using variable byte encoding")
    index.finalize()
    
    # 1. 布尔双指针交集查询: "inverted" AND "indexes"
    and_results = index.boolean_and_query(["inverted", "indexes"])
    assert "doc_1" in and_results
    assert "doc_3" in and_results
    assert "doc_2" not in and_results
    
    # 2. BM25 检索评分
    bm25_ranked = index.search_bm25("inverted indexes search", top_k=2)
    assert len(bm25_ranked) == 2
    top_doc_id, top_score = bm25_ranked[0]
    assert top_doc_id in ["doc_1", "doc_3"]
    assert top_score > 0.0
