"""
课后作业 01 单元测试: test_word2vec.py
测试 TF-IDF 计算矩阵 Shape、L2 归一化及 Skip-Gram 损失
"""

import sys
import os
import torch
import pytest

# 将 scripts 路径加入 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.word_embeddings import compute_tf_idf, SkipGramModel


def test_compute_tf_idf():
    corpus = [
        "natural language processing with python",
        "deep learning for natural language processing"
    ]
    vocab, matrix = compute_tf_idf(corpus)
    
    assert len(vocab) > 0
    assert matrix.shape[0] == 2
    assert matrix.shape[1] == len(vocab)
    
    # 测试 L2 归一化后各行范数为 1.0
    norms = torch.norm(matrix, dim=1)
    for n in norms:
        assert abs(n.item() - 1.0) < 1e-4


def test_skipgram_loss():
    vocab_size = 100
    embed_dim = 32
    model = SkipGramModel(vocab_size, embed_dim)
    
    batch_size = 4
    neg_k = 5
    center = torch.tensor([1, 5, 10, 20])
    pos = torch.tensor([2, 6, 11, 21])
    neg = torch.randint(0, vocab_size, (batch_size, neg_k))
    
    loss = model(center, pos, neg)
    
    assert isinstance(loss.item(), float)
    assert not torch.isnan(loss)
    assert loss.item() > 0.0
