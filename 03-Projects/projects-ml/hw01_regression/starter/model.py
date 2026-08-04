from __future__ import annotations

import torch
from torch import nn


class MLPRegressor(nn.Module):
    """Starter model skeleton for HW01.

    This module intentionally keeps only the minimal network definition.
    Students are expected to adjust hidden size, depth, dropout, residual ideas,
    and any feature-selection strategy on their own.
    """

    def __init__(self, input_dim: int, hidden_dim: int = 64, dropout: float = 0.1) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x).squeeze(-1)
