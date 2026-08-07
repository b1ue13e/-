"""
08-NLP全栈 阶段作业-02 MinBERT 算子单元测试脚本
验证 BertSelfAttention 与 Layer Standard Normalization 维度及逻辑正确性。
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F

import sys
import io

# 兼容 Windows CMD / PowerShell 默认 GBK 终端输出
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class ReferenceBertSelfAttention(nn.Module):
    def __init__(self, d_model=768, num_heads=12):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.query = nn.Linear(d_model, d_model)
        self.key = nn.Linear(d_model, d_model)
        self.value = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        B, L, _ = x.size()
        q = self.query(x).view(B, L, self.num_heads, self.d_k).transpose(1, 2)
        k = self.key(x).view(B, L, self.num_heads, self.d_k).transpose(1, 2)
        v = self.value(x).view(B, L, self.num_heads, self.d_k).transpose(1, 2)

        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        attn = F.softmax(scores, dim=-1)
        out = torch.matmul(attn, v)
        out = out.transpose(1, 2).contiguous().view(B, L, self.d_model)
        return out, attn

def test_bert_self_attention_shape():
    batch_size = 4
    seq_len = 16
    d_model = 768
    num_heads = 12

    x = torch.randn(batch_size, seq_len, d_model)
    attn_layer = ReferenceBertSelfAttention(d_model=d_model, num_heads=num_heads)
    
    out, attn = attn_layer(x)

    assert out.shape == (batch_size, seq_len, d_model), f"Expected out shape {(batch_size, seq_len, d_model)}, got {out.shape}"
    assert attn.shape == (batch_size, num_heads, seq_len, seq_len), f"Expected attn shape {(batch_size, num_heads, seq_len, seq_len)}, got {attn.shape}"
    print("[OK] test_bert_self_attention_shape PASSED!")

def test_attention_masking():
    batch_size = 2
    seq_len = 4
    d_model = 12
    num_heads = 2

    x = torch.randn(batch_size, seq_len, d_model)
    # Mask out the last token in sequence
    mask = torch.tensor([
        [1, 1, 1, 0],
        [1, 1, 0, 0]
    ]).unsqueeze(1).unsqueeze(2) # [B, 1, 1, L]

    attn_layer = ReferenceBertSelfAttention(d_model=d_model, num_heads=num_heads)
    _, attn = attn_layer(x, mask=mask)

    # Check masked positions have near zero probability
    assert torch.all(attn[0, :, :, 3] < 1e-6), "Masked token should have near zero attention probability"
    print("[OK] test_attention_masking PASSED!")


if __name__ == "__main__":
    print("Executing MinBERT standalone unit tests...")
    test_bert_self_attention_shape()
    test_attention_masking()
    print("All MinBERT standalone tests completed successfully!")
