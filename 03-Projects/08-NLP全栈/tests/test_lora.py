"""
课后作业 04: LoRA 参数高效微调算子 单元测试
"""
import pytest
import torch
import torch.nn as nn
import math

class LoRALinear(nn.Module):
    def __init__(self, in_features: int, out_features: int, r: int = 8, lora_alpha: int = 16):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)
        self.r = r
        self.lora_alpha = lora_alpha
        self.scaling = lora_alpha / r

        if r > 0:
            self.lora_A = nn.Parameter(torch.zeros(r, in_features))
            self.lora_B = nn.Parameter(torch.zeros(out_features, r))
            nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))
            nn.init.zeros_(self.lora_B)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        result = self.linear(x)
        if self.r > 0:
            result += (x @ self.lora_A.T @ self.lora_B.T) * self.scaling
        return result

    def merge_weights(self):
        if self.r > 0:
            self.linear.weight.data += (self.lora_B @ self.lora_A) * self.scaling

def test_lora_initialization_equivalence():
    in_dim, out_dim, r = 128, 256, 8
    lora_layer = LoRALinear(in_dim, out_dim, r=r)
    x = torch.randn(4, 16, in_dim)
    
    # 初始状态下 lora_B 权重全 0, 输出应与普通 Linear 完全一致
    with torch.no_grad():
        out_lora = lora_layer(x)
        out_orig = lora_layer.linear(x)
    
    assert torch.allclose(out_lora, out_orig, atol=1e-6), "LoRA 初始输出应与原始 Base Linear 一致"

def test_lora_weight_merging():
    in_dim, out_dim, r = 64, 64, 4
    lora_layer = LoRALinear(in_dim, out_dim, r=r)
    # 填充非零参数
    nn.init.ones_(lora_layer.lora_B)
    x = torch.randn(2, in_dim)

    with torch.no_grad():
        out_before_merge = lora_layer(x)
        lora_layer.merge_weights()
        out_after_merge = lora_layer.linear(x)

    assert torch.allclose(out_before_merge, out_after_merge, atol=1e-5), "LoRA 权重 Merge 前后前向输出应保持数值一致"
