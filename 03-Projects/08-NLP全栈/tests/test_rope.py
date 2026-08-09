"""
课后作业 03: RoPE 旋转位置编码单元测试
"""
import pytest
import torch

def apply_rotary_pos_emb(x: torch.Tensor, dim: int = 64):
    """手写简单的 2D RoPE 转换测试实现"""
    seq_len = x.shape[1]
    inv_freq = 1.0 / (10000 ** (torch.arange(0, dim, 2).float() / dim))
    t = torch.arange(seq_len).float()
    freqs = torch.einsum('i,j->ij', t, inv_freq)
    emb = torch.cat((freqs, freqs), dim=-1)
    cos = emb.cos().unsqueeze(0).unsqueeze(2) # [1, seq_len, 1, dim]
    sin = emb.sin().unsqueeze(0).unsqueeze(2)
    
    # 旋转矩阵逻辑: [-x2, x1]
    x1 = x[..., :dim//2]
    x2 = x[..., dim//2:]
    rotate_half_x = torch.cat((-x2, x1), dim=-1)
    
    return (x * cos) + (rotate_half_x * sin)

def test_rope_output_shape():
    batch_size, seq_len, n_heads, head_dim = 2, 16, 4, 64
    x = torch.randn(batch_size, seq_len, n_heads, head_dim)
    out = apply_rotary_pos_emb(x, dim=head_dim)
    
    assert out.shape == x.shape, f"RoPE 变换后张量形状应保持不变, 预期 {x.shape}, 实际 {out.shape}"

def test_rope_pos_0_identity():
    # 当 pos = 0 时, cos=1, sin=0, 输出等于输入
    batch_size, seq_len, n_heads, head_dim = 1, 1, 1, 64
    x = torch.randn(batch_size, seq_len, n_heads, head_dim)
    out = apply_rotary_pos_emb(x, dim=head_dim)
    
    assert torch.allclose(out, x, atol=1e-5), "Pos=0 时 RoPE 变换应接近恒等映射"
