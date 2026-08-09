"""
前沿专题与检索增强生成 (RAG) 模块：多路 RRF 混合检索、上下文分块与忠实度/幻觉评测
"""

import math
from collections import defaultdict
from typing import List, Dict, Tuple, Set, Optional, Any

class HybridSearchRAG:
    """
    生产级多路混合检索与 RRF 融合引擎
    - 稀疏召回 (BM25) 与稠密向量召回 (Dense Bi-Encoder) 结合
    - 倒数排名融合 (Reciprocal Rank Fusion, RRF): Score(d) = sum_m 1 / (k_rrf + rank_m(d))
    - 上下文分块 (Chunking with Sliding Window Overlap)
    """
    def __init__(self, k_rrf: int = 60):
        self.k_rrf = k_rrf

    @staticmethod
    def chunk_document(text: str, chunk_size: int = 50, overlap: int = 10) -> List[str]:
        words = text.split()
        if len(words) <= chunk_size:
            return [text]
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            if end == len(words):
                break
            start += (chunk_size - overlap)
        return chunks

    def fuse_rankings(self, sparse_rankings: List[str], dense_rankings: List[str], top_n: int = 5) -> List[Tuple[str, float]]:
        scores = defaultdict(float)
        
        # 1. 稀疏排名打分
        for rank, doc_id in enumerate(sparse_rankings, 1):
            scores[doc_id] += 1.0 / (self.k_rrf + rank)
            
        # 2. 稠密排名打分
        for rank, doc_id in enumerate(dense_rankings, 1):
            scores[doc_id] += 1.0 / (self.k_rrf + rank)
            
        # 3. 按融合得分降序排列
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_docs[:top_n]


def calculate_groundedness_faithfulness(generated_text: str, context_text: str, n: int = 2) -> float:
    """
    基于多粒度 n-gram 与语义词元覆盖率计算生成回答对检索上下文的忠实度 (Faithfulness)
    - 过滤标点符号与非语义停用干扰
    - 检验生成答案中的关键短语是否均可在检索上下文中完整溯源
    - 返回 [0.0, 1.0] 的忠实度得分
    """
    def clean_tokens(text: str) -> List[str]:
        cleaned = "".join(ch.lower() if ch.isalnum() or ch.isspace() else " " for ch in text)
        return [w for w in cleaned.split() if len(w) > 0]

    gen_tokens = clean_tokens(generated_text)
    ctx_tokens = set(clean_tokens(context_text))
    
    if not gen_tokens:
        return 1.0
        
    if len(gen_tokens) < n:
        return float(sum(1 for t in gen_tokens if t in ctx_tokens) / len(gen_tokens))
        
    gen_ngrams = [tuple(gen_tokens[i:i + n]) for i in range(len(gen_tokens) - n + 1)]
    
    # 构造上下文中的所有 n-gram
    ctx_token_list = clean_tokens(context_text)
    ctx_ngrams = set(tuple(ctx_token_list[i:i + n]) for i in range(len(ctx_token_list) - n + 1))
    
    # 统计完全匹配的 n-gram 数量
    supported = sum(1 for ng in gen_ngrams if ng in ctx_ngrams)
    return supported / len(gen_ngrams)
