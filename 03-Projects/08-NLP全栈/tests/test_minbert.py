"""
阶段作业 02: MinBERT 架构实现单元测试
测试 scripts/minbert.py 中的 BertSelfAttention 与 BertLayer
"""
import pytest
import torch
import sys
from pathlib import Path

# 动态引入 scripts 路径
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from minbert import BertSelfAttention, BertLayer

def test_bert_self_attention_shape():
    hidden_size = 768
    num_heads = 12
    batch_size, seq_len = 2, 16
    
    attn = BertSelfAttention(hidden_size=hidden_size, num_attention_heads=num_heads)
    hidden_states = torch.randn(batch_size, seq_len, hidden_size)
    output = attn(hidden_states)
    
    assert output.shape == (batch_size, seq_len, hidden_size), f"BertSelfAttention 输出形状错误, 实际为 {output.shape}"

def test_bert_layer_forward_pass():
    hidden_size = 768
    num_heads = 12
    batch_size, seq_len = 2, 16
    
    layer = BertLayer(hidden_size=hidden_size, num_heads=num_heads)
    hidden_states = torch.randn(batch_size, seq_len, hidden_size)
    output = layer(hidden_states)
    
    assert output.shape == (batch_size, seq_len, hidden_size), f"BertLayer 输出形状错误, 实际为 {output.shape}"
    assert not torch.isnan(output).any(), "BertLayer 输出张量中不应包含 NaN 数值"
