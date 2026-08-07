"""
08-NLP全栈 阶段作业 01: RNN 与 Seq2Seq 注意力机制
含 Bahdanau Attention 与 Seq2Seq 模块实现
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class BahdanauAttention(nn.Module):
    def __init__(self, hidden_dim: int):
        super().__init__()
        self.W_q = nn.Linear(hidden_dim, hidden_dim)
        self.W_k = nn.Linear(hidden_dim, hidden_dim)
        self.V = nn.Linear(hidden_dim, 1)

    def forward(self, query: torch.Tensor, keys: torch.Tensor, mask: torch.Tensor = None):
        """
        query: [B, 1, H]  (Decoder 上一时刻隐藏状态)
        keys: [B, S, H]   (Encoder 状态输出)
        mask: [B, S]      (Padding 掩码, 1 表示有效, 0 表示填充)
        returns: context [B, 1, H], attn_weights [B, S]
        """
        q_proj = self.W_q(query) # [B, 1, H]
        k_proj = self.W_k(keys)  # [B, S, H]
        
        scores = self.V(torch.tanh(q_proj + k_proj)).squeeze(2) # [B, S]
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
            
        attn_weights = F.softmax(scores, dim=-1) # [B, S]
        context = torch.bmm(attn_weights.unsqueeze(1), keys) # [B, 1, H]
        
        return context, attn_weights


class Seq2SeqEncoder(nn.Module):
    def __init__(self, vocab_size: int, embed_dim: int, hidden_dim: int):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, hidden_dim)

    def forward(self, x: torch.Tensor):
        # x: [B, S]
        embed = self.embedding(x)
        outputs, hidden = self.gru(embed) # outputs: [B, S, 2*H]
        # 融合双向最后一个时刻隐藏状态
        combined_hidden = torch.tanh(self.fc(outputs)) # [B, S, H]
        return combined_hidden
