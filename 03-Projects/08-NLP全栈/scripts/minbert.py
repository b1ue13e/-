"""
08-NLP全栈 阶段作业 02: Transformer 与 MinBERT 实现
包含 Multi-Head Attention, BertLayer, BertEncoder
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class BertSelfAttention(nn.Module):
    def __init__(self, hidden_size: int = 768, num_attention_heads: int = 12):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_size = hidden_size // num_attention_heads
        self.all_head_size = self.num_attention_heads * self.attention_head_size

        self.query = nn.Linear(hidden_size, self.all_head_size)
        self.key = nn.Linear(hidden_size, self.all_head_size)
        self.value = nn.Linear(hidden_size, self.all_head_size)

    def transpose_for_scores(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, S, H] -> [B, H_num, S, H_dim]
        new_x_shape = x.size()[:-1] + (self.num_attention_heads, self.attention_head_size)
        x = x.view(*new_x_shape)
        return x.permute(0, 2, 1, 3)

    def forward(self, hidden_states: torch.Tensor, attention_mask: torch.Tensor = None):
        mixed_query_layer = self.query(hidden_states)
        mixed_key_layer = self.key(hidden_states)
        mixed_value_layer = self.value(hidden_states)

        query_layer = self.transpose_for_scores(mixed_query_layer)
        key_layer = self.transpose_for_scores(mixed_key_layer)
        value_layer = self.transpose_for_scores(mixed_value_layer)

        # 缩放点积注意力
        attention_scores = torch.matmul(query_layer, key_layer.transpose(-1, -2))
        attention_scores = attention_scores / math.sqrt(self.attention_head_size)

        if attention_mask is not None:
            attention_scores = attention_scores + attention_mask

        attention_probs = F.softmax(attention_scores, dim=-1)
        context_layer = torch.matmul(attention_probs, value_layer)

        context_layer = context_layer.permute(0, 2, 1, 3).contiguous()
        new_context_layer_shape = context_layer.size()[:-2] + (self.all_head_size,)
        context_layer = context_layer.view(*new_context_layer_shape)

        return context_layer


class BertLayer(nn.Module):
    def __init__(self, hidden_size: int = 768, num_heads: int = 12):
        super().__init__()
        self.attention = BertSelfAttention(hidden_size, num_heads)
        self.dense1 = nn.Linear(hidden_size, hidden_size * 4)
        self.dense2 = nn.Linear(hidden_size * 4, hidden_size)
        self.LayerNorm1 = nn.LayerNorm(hidden_size)
        self.LayerNorm2 = nn.LayerNorm(hidden_size)

    def forward(self, hidden_states: torch.Tensor, attention_mask: torch.Tensor = None):
        # Residual + LayerNorm
        attn_output = self.attention(hidden_states, attention_mask)
        norm1 = self.LayerNorm1(hidden_states + attn_output)
        
        # FFN
        ffn_output = self.dense2(F.gelu(self.dense1(norm1)))
        norm2 = self.LayerNorm2(norm1 + ffn_output)
        
        return norm2
