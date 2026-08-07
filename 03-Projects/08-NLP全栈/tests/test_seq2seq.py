"""
阶段作业 01 单元测试: test_seq2seq.py
测试 Bahdanau Attention 权重、Seq2Seq Encoder 和 Beam Search 解码断言
"""

import sys
import os
import torch
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.seq2seq_attention import BahdanauAttention, Seq2SeqEncoder
from scripts.beam_search import beam_search_decode


def test_bahdanau_attention():
    batch_size = 2
    seq_len = 5
    hidden_dim = 64
    
    attn = BahdanauAttention(hidden_dim)
    query = torch.randn(batch_size, 1, hidden_dim)
    keys = torch.randn(batch_size, seq_len, hidden_dim)
    mask = torch.tensor([[1, 1, 1, 0, 0], [1, 1, 1, 1, 1]])
    
    context, weights = attn(query, keys, mask)
    
    assert context.shape == (batch_size, 1, hidden_dim)
    assert weights.shape == (batch_size, seq_len)
    
    # 验证概率和为 1
    probs_sum = torch.sum(weights, dim=-1)
    for p in probs_sum:
        assert abs(p.item() - 1.0) < 1e-4
        
    # 验证 Padding 位置概率为 0
    assert weights[0, 3].item() < 1e-5
    assert weights[0, 4].item() < 1e-5


def test_seq2seq_encoder():
    vocab_size = 500
    embed_dim = 32
    hidden_dim = 64
    
    encoder = Seq2SeqEncoder(vocab_size, embed_dim, hidden_dim)
    x = torch.randint(0, vocab_size, (2, 7))
    out = encoder(x)
    
    assert out.shape == (2, 7, hidden_dim)


def test_beam_search_decode():
    vocab_size = 20
    start_token = 1
    end_token = 2
    
    # 假模型步进函数
    def dummy_step(token, hidden):
        logits = torch.randn(1, vocab_size)
        return logits, None
        
    best_seq, best_score = beam_search_decode(dummy_step, start_token, end_token, beam_width=3, max_len=10)
    
    assert isinstance(best_seq, list)
    assert best_seq[0] == start_token
    assert len(best_seq) <= 11
