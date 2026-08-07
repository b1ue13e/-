"""
08-NLP全栈 阶段作业 02: SST-2 情感分类器与微调引擎
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from .minbert import BertLayer


class MinBertForSequenceClassification(nn.Module):
    def __init__(self, vocab_size: int = 30522, hidden_size: int = 768, num_classes: int = 2, num_layers: int = 4):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.pos_embedding = nn.Embedding(512, hidden_size)
        
        self.layers = nn.ModuleList([
            BertLayer(hidden_size=hidden_size, num_heads=12)
            for _ in range(num_layers)
        ])
        self.classifier = nn.Linear(hidden_size, num_classes)

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor = None):
        # input_ids: [B, S]
        seq_len = input_ids.size(1)
        pos_ids = torch.arange(seq_len, dtype=torch.long, device=input_ids.device).unsqueeze(0)
        
        x = self.embedding(input_ids) + self.pos_embedding(pos_ids)
        
        if attention_mask is not None:
            # 扩展加性掩码 [B, 1, 1, S]
            extended_mask = (1.0 - attention_mask.unsqueeze(1).unsqueeze(2)) * -10000.0
        else:
            extended_mask = None

        for layer in self.layers:
            x = layer(x, extended_mask)

        # 取 [CLS] Token (第一个位置 0) 进分类头
        cls_token = x[:, 0, :]
        logits = self.classifier(cls_token)
        return logits
