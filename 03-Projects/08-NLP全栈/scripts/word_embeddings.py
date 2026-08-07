"""
08-NLP全栈 课后作业 01: 词向量与文本表征
包含 TF-IDF 计算与 Skip-Gram Negative Sampling 核心实现
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import Counter, defaultdict


def compute_tf_idf(corpus):
    """
    计算简易语料库的 TF-IDF 矩阵
    corpus: List[str]
    returns: vocab (List[str]), tfidf_matrix (torch.Tensor [N, V])
    """
    docs_tokens = [doc.lower().split() for doc in corpus]
    vocab = sorted(list(set(token for doc in docs_tokens for token in doc)))
    vocab_map = {word: idx for idx, word in enumerate(vocab)}
    
    num_docs = len(corpus)
    num_vocab = len(vocab)
    
    # 1. 计算 Term Frequency (TF)
    tf_matrix = torch.zeros(num_docs, num_vocab)
    for i, doc in enumerate(docs_tokens):
        counts = Counter(doc)
        total_tokens = len(doc)
        for word, count in counts.items():
            tf_matrix[i, vocab_map[word]] = count / total_tokens
            
    # 2. 计算 Inverse Document Frequency (IDF)
    doc_freq = torch.zeros(num_vocab)
    for doc in docs_tokens:
        unique_words = set(doc)
        for word in unique_words:
            doc_freq[vocab_map[word]] += 1
            
    idf = torch.log((num_docs + 1.0) / (doc_freq + 1.0)) + 1.0
    tfidf_matrix = tf_matrix * idf
    
    # L2 归一化
    norms = torch.norm(tfidf_matrix, dim=1, keepdim=True)
    norms[norms == 0] = 1.0
    tfidf_matrix = tfidf_matrix / norms
    
    return vocab, tfidf_matrix


class SkipGramModel(nn.Module):
    """
    Skip-Gram 负采样词向量模型
    """
    def __init__(self, vocab_size: int, embed_dim: int = 64):
        super().__init__()
        self.in_embed = nn.Embedding(vocab_size, embed_dim)
        self.out_embed = nn.Embedding(vocab_size, embed_dim)
        # 初始化权重
        nn.init.uniform_(self.in_embed.weight, -0.5 / embed_dim, 0.5 / embed_dim)
        nn.init.zeros_(self.out_embed.weight)

    def forward(self, center_words: torch.Tensor, pos_words: torch.Tensor, neg_words: torch.Tensor):
        """
        center_words: [B]
        pos_words: [B]
        neg_words: [B, K]
        """
        v_c = self.in_embed(center_words)    # [B, D]
        v_pos = self.out_embed(pos_words)   # [B, D]
        v_neg = self.out_embed(neg_words)   # [B, K, D]

        pos_score = torch.sum(v_c * v_pos, dim=1) # [B]
        pos_loss = -F.logsigmoid(pos_score)

        neg_score = torch.bmm(v_neg, v_c.unsqueeze(2)).squeeze(2) # [B, K]
        neg_loss = -torch.sum(F.logsigmoid(-neg_score), dim=1)

        return torch.mean(pos_loss + neg_loss)
