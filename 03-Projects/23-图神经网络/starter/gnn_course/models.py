from __future__ import annotations

import torch
from torch import nn


def _with_self_loops(adj: torch.Tensor) -> torch.Tensor:
    return adj + torch.eye(adj.shape[0], dtype=adj.dtype, device=adj.device)


def _symmetric_normalize(adj: torch.Tensor) -> torch.Tensor:
    augmented = _with_self_loops(adj)
    degree = augmented.sum(dim=1).clamp_min(1.0)
    scale = degree.pow(-0.5)
    return scale[:, None] * augmented * scale[None, :]


def _neighbor_normalize(adj: torch.Tensor) -> torch.Tensor:
    """Return neighbor-only mean weights; the SAGE update concatenates self separately."""
    return adj / adj.sum(dim=1, keepdim=True).clamp_min(1.0)


def _local_attention(scores: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
    """Apply a row-wise softmax over each target node's declared neighborhood."""
    augmented = _with_self_loops(adj)
    masked = torch.where(
        augmented > 0,
        torch.nn.functional.leaky_relu(scores, negative_slope=0.2),
        torch.full_like(scores, -torch.inf),
    )
    return torch.softmax(masked, dim=1)


def _layer_dimensions(
    in_channels: int,
    hidden_channels: int,
    out_channels: int,
    num_layers: int,
) -> list[tuple[int, int]]:
    if num_layers < 1:
        raise ValueError("num_layers must be at least 1")
    if num_layers == 1:
        return [(in_channels, out_channels)]
    return (
        [(in_channels, hidden_channels)]
        + [(hidden_channels, hidden_channels)] * (num_layers - 2)
        + [(hidden_channels, out_channels)]
    )


class MLP(nn.Module):
    def __init__(
        self,
        in_channels: int,
        hidden_channels: int,
        out_channels: int,
        num_layers: int = 2,
    ) -> None:
        super().__init__()
        self.layers = nn.ModuleList(
            nn.Linear(source, target)
            for source, target in _layer_dimensions(in_channels, hidden_channels, out_channels, num_layers)
        )

    def forward(self, x: torch.Tensor, adj: torch.Tensor | None = None) -> torch.Tensor:
        for layer in self.layers[:-1]:
            x = torch.relu(layer(x))
        return self.layers[-1](x)

    def encode(self, x: torch.Tensor, adj: torch.Tensor | None = None) -> torch.Tensor:
        if len(self.layers) == 1:
            return self.layers[0](x)
        for layer in self.layers[:-1]:
            x = torch.relu(layer(x))
        return x


class GCN(nn.Module):
    def __init__(
        self,
        in_channels: int,
        hidden_channels: int,
        out_channels: int,
        num_layers: int = 2,
    ) -> None:
        super().__init__()
        self.layers = nn.ModuleList(
            nn.Linear(source, target, bias=False)
            for source, target in _layer_dimensions(in_channels, hidden_channels, out_channels, num_layers)
        )

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        normalized = _symmetric_normalize(adj)
        for layer in self.layers[:-1]:
            x = torch.relu(normalized @ layer(x))
        return normalized @ self.layers[-1](x)

    def encode(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        normalized = _symmetric_normalize(adj)
        if len(self.layers) == 1:
            return normalized @ self.layers[0](x)
        for layer in self.layers[:-1]:
            x = torch.relu(normalized @ layer(x))
        return x


class GraphSAGE(nn.Module):
    def __init__(
        self,
        in_channels: int,
        hidden_channels: int,
        out_channels: int,
        num_layers: int = 2,
    ) -> None:
        super().__init__()
        self.layers = nn.ModuleList(
            nn.Linear(source * 2, target)
            for source, target in _layer_dimensions(in_channels, hidden_channels, out_channels, num_layers)
        )

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        normalized = _neighbor_normalize(adj)
        for layer in self.layers[:-1]:
            neighbor = normalized @ x
            x = torch.relu(layer(torch.cat([x, neighbor], dim=1)))
        neighbor = normalized @ x
        return self.layers[-1](torch.cat([x, neighbor], dim=1))

    def encode(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        normalized = _neighbor_normalize(adj)
        if len(self.layers) == 1:
            neighbor = normalized @ x
            return self.layers[0](torch.cat([x, neighbor], dim=1))
        for layer in self.layers[:-1]:
            neighbor = normalized @ x
            x = torch.relu(layer(torch.cat([x, neighbor], dim=1)))
        return x


class DenseGATLayer(nn.Module):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.projection = nn.Linear(in_channels, out_channels, bias=False)
        self.att_src = nn.Linear(out_channels, 1, bias=False)
        self.att_dst = nn.Linear(out_channels, 1, bias=False)

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        projected = self.projection(x)
        scores = self.att_src(projected) + self.att_dst(projected).T
        attention = _local_attention(scores, adj)
        return attention @ projected, attention


class GAT(nn.Module):
    def __init__(
        self,
        in_channels: int,
        hidden_channels: int,
        out_channels: int,
        num_layers: int = 2,
    ) -> None:
        super().__init__()
        self.layers = nn.ModuleList(
            DenseGATLayer(source, target)
            for source, target in _layer_dimensions(in_channels, hidden_channels, out_channels, num_layers)
        )
        self.last_attention: torch.Tensor | None = None

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        for layer in self.layers[:-1]:
            x, _ = layer(x, adj)
            x = torch.relu(x)
        x, attention = self.layers[-1](x, adj)
        self.last_attention = attention.detach()
        return x

    def encode(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        if len(self.layers) == 1:
            x, _ = self.layers[0](x, adj)
            return x
        for layer in self.layers[:-1]:
            x, _ = layer(x, adj)
            x = torch.relu(x)
        return x
