"""
08-NLP全栈 大作业 Capstone: 稀疏检索到 Transformer 文本误差审计
包含 BM25 + 向量密检索 + RRF (Reciprocal Rank Fusion) 融合检索器
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import Counter


class BM25Retriever:
    """简易 BM25 稀疏检索器"""
    def __init__(self, corpus, k1: float = 1.5, b: float = 0.75):
        self.corpus = [doc.lower().split() for doc in corpus]
        self.k1 = k1
        self.b = b
        self.doc_len = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_len) / len(self.corpus) if self.corpus else 0
        self.doc_freqs = []
        self.idf = {}
        self._initialize()

    def _initialize(self):
        df = Counter()
        for doc in self.corpus:
            frequencies = Counter(doc)
            self.doc_freqs.append(frequencies)
            for word in frequencies:
                df[word] += 1
                
        num_docs = len(self.corpus)
        for word, count in df.items():
            self.idf[word] = math.log((num_docs - count + 0.5) / (count + 0.5) + 1.0)

    def get_scores(self, query: str):
        query_words = query.lower().split()
        scores = [0.0] * len(self.corpus)
        for i, doc_freq in enumerate(self.doc_freqs):
            dl = self.doc_len[i]
            for word in query_words:
                if word in doc_freq:
                    freq = doc_freq[word]
                    num = self.idf.get(word, 0) * freq * (self.k1 + 1)
                    denom = freq + self.k1 * (1 - self.b + self.b * (dl / self.avgdl))
                    scores[i] += num / denom
        return scores


def reciprocal_rank_fusion(dense_ranks, sparse_ranks, k: int = 60):
    """
    RRF (Reciprocal Rank Fusion) 融合算子
    dense_ranks: List[int] (doc_ids by dense rank)
    sparse_ranks: List[int] (doc_ids by sparse rank)
    returns: fused_sorted_doc_ids (List[int])
    """
    rrf_score = {}
    
    for rank, doc_id in enumerate(dense_ranks):
        rrf_score[doc_id] = rrf_score.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
        
    for rank, doc_id in enumerate(sparse_ranks):
        rrf_score[doc_id] = rrf_score.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
        
    sorted_docs = sorted(rrf_score.keys(), key=lambda x: rrf_score[x], reverse=True)
    return sorted_docs
