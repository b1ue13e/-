from __future__ import annotations

from collections.abc import Sequence

import torch
from torch import nn


def parse_hidden_dims(raw: str | Sequence[int]) -> tuple[int, ...]:
    if isinstance(raw, str):
        values = tuple(int(value.strip()) for value in raw.split(",") if value.strip())
    else:
        values = tuple(int(value) for value in raw)
    if not values or any(value <= 0 for value in values):
        raise ValueError("hidden_dims must contain one or more positive integers")
    return values


class MLPClassifier(nn.Module):
    """A deliberately small, editable baseline for frame-level phoneme classification."""

    def __init__(
        self,
        input_dim: int,
        num_classes: int,
        hidden_dims: Sequence[int] = (256, 128),
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        if input_dim <= 0 or num_classes <= 1:
            raise ValueError("input_dim must be positive and num_classes must be greater than one")
        if not 0.0 <= dropout < 1.0:
            raise ValueError("dropout must be in [0, 1)")

        layers: list[nn.Module] = []
        previous_dim = input_dim
        for hidden_dim in parse_hidden_dims(hidden_dims):
            layers.extend(
                [
                    nn.Linear(previous_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Dropout(dropout),
                ]
            )
            previous_dim = hidden_dim
        layers.append(nn.Linear(previous_dim, num_classes))
        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)
