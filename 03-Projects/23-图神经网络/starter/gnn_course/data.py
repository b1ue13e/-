from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib

import torch


@dataclass(frozen=True)
class GraphData:
    x: torch.Tensor
    adj: torch.Tensor
    y: torch.Tensor
    train_mask: torch.Tensor
    val_mask: torch.Tensor
    test_mask: torch.Tensor
    name: str = "synthetic-two-community-v1"

    @property
    def num_nodes(self) -> int:
        return int(self.x.shape[0])


def make_toy_graph() -> GraphData:
    """Return a deterministic two-community graph for smoke experiments."""
    generator = torch.Generator().manual_seed(2026)
    num_nodes = 12
    adj = torch.zeros((num_nodes, num_nodes), dtype=torch.float32)
    for start in (0, 6):
        nodes = list(range(start, start + 6))
        for offset, node in enumerate(nodes):
            for step in (1, 2):
                other = nodes[(offset + step) % len(nodes)]
                adj[node, other] = 1.0
                adj[other, node] = 1.0
    for left, right in ((2, 8), (4, 10)):
        adj[left, right] = 1.0
        adj[right, left] = 1.0

    x = torch.randn((num_nodes, 4), generator=generator)
    x[:, 0] = (adj.sum(dim=1) - adj.sum(dim=1).mean()) / adj.sum(dim=1).std()
    y = torch.tensor([0] * 6 + [1] * 6, dtype=torch.long)
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)
    train_mask[[0, 1, 2, 6, 7, 8]] = True
    val_mask[[3, 4, 9]] = True
    test_mask[[5, 10, 11]] = True
    return GraphData(x, adj, y, train_mask, val_mask, test_mask)


def make_contextual_sbm(
    num_nodes: int = 120,
    feature_dim: int = 8,
    p_in: float = 0.12,
    p_out: float = 0.02,
    feature_signal: float = 0.35,
    seed: int = 2026,
) -> GraphData:
    """Build a deterministic contextual stochastic block model.

    The graph is large enough for meaningful train/validation/test counts while
    remaining CPU-friendly. Labels affect graph and feature generation only;
    the training protocol still restricts supervised loss to ``train_mask``.
    """
    if num_nodes < 40 or num_nodes % 2:
        raise ValueError("num_nodes must be even and at least 40")
    if feature_dim < 2:
        raise ValueError("feature_dim must be at least 2")
    if not 0.0 <= p_out < p_in <= 1.0:
        raise ValueError("expected 0 <= p_out < p_in <= 1")

    generator = torch.Generator().manual_seed(seed)
    half = num_nodes // 2
    y = torch.tensor([0] * half + [1] * half, dtype=torch.long)
    same_block = y[:, None] == y[None, :]
    probabilities = torch.where(
        same_block,
        torch.full((num_nodes, num_nodes), p_in),
        torch.full((num_nodes, num_nodes), p_out),
    )
    sampled = torch.rand((num_nodes, num_nodes), generator=generator) < probabilities
    upper = torch.triu(sampled, diagonal=1).to(torch.float32)
    adj = upper + upper.T

    # Guarantee that neither block contains isolated nodes, without encoding labels
    # in a feature column or changing the evaluation masks.
    for start in (0, half):
        for offset in range(half):
            left = start + offset
            right = start + ((offset + 1) % half)
            adj[left, right] = 1.0
            adj[right, left] = 1.0

    x = torch.randn((num_nodes, feature_dim), generator=generator)
    direction = torch.where(y == 0, -1.0, 1.0)
    x[:, 0] += feature_signal * direction
    degree = adj.sum(dim=1)
    x[:, 1] = (degree - degree.mean()) / degree.std().clamp_min(1e-6)

    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)
    train_per_class = max(8, half // 4)
    val_per_class = max(8, half // 4)
    for label in (0, 1):
        members = torch.where(y == label)[0]
        order = members[torch.randperm(len(members), generator=generator)]
        train_mask[order[:train_per_class]] = True
        val_mask[order[train_per_class : train_per_class + val_per_class]] = True
        test_mask[order[train_per_class + val_per_class :]] = True

    return GraphData(
        x=x,
        adj=adj,
        y=y,
        train_mask=train_mask,
        val_mask=val_mask,
        test_mask=test_mask,
        name="contextual-sbm-v1",
    )


def with_graph_inputs(
    data: GraphData,
    *,
    x: torch.Tensor | None = None,
    adj: torch.Tensor | None = None,
) -> GraphData:
    """Return an ablation copy without mutating the source data contract."""
    return replace(data, x=data.x if x is None else x, adj=data.adj if adj is None else adj)


def sample_neighbor_adjacency(adj: torch.Tensor, fanout: int, seed: int) -> torch.Tensor:
    """Sample at most ``fanout`` neighbors per target node.

    Sampling is row-wise and intentionally keeps a directed computation graph:
    a target selecting a source does not force the reverse message. The model
    still adds self information explicitly.
    """
    if fanout < 1:
        raise ValueError("fanout must be positive")
    generator = torch.Generator(device=adj.device).manual_seed(seed)
    sampled = torch.zeros_like(adj)
    for target in range(adj.shape[0]):
        neighbors = torch.where(adj[target] > 0)[0]
        if len(neighbors) <= fanout:
            selected = neighbors
        else:
            order = torch.randperm(len(neighbors), generator=generator, device=adj.device)
            selected = neighbors[order[:fanout]]
        sampled[target, selected] = adj[target, selected]
    return sampled


def sample_batch_subgraph(
    adj: torch.Tensor,
    target_nodes: torch.Tensor,
    fanouts: tuple[int, ...],
    seed: int,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Build a layered, deduplicated computation subgraph for target nodes.

    Returns ``(node_ids, sub_adj, target_positions)``. ``node_ids`` preserves
    original graph identity, while ``target_positions`` indexes the output
    nodes whose loss should be computed. Each discovered node is expanded once,
    so every sampled row respects the declared fanout. Sampling uses structure
    only and never reads labels or split membership.
    """
    if adj.ndim != 2 or adj.shape[0] != adj.shape[1]:
        raise ValueError("adj must be a square matrix")
    if not fanouts or any(fanout < 1 for fanout in fanouts):
        raise ValueError("fanouts must contain positive values")
    targets = torch.unique(target_nodes.to(dtype=torch.long), sorted=True)
    if targets.numel() == 0 or bool((targets < 0).any()) or bool((targets >= adj.shape[0]).any()):
        raise ValueError("target_nodes must contain valid, non-empty node ids")

    generator = torch.Generator(device=adj.device).manual_seed(seed)
    ordered_nodes = [int(node) for node in targets.tolist()]
    seen = set(ordered_nodes)
    frontier = ordered_nodes.copy()
    sampled_edges: list[tuple[int, int]] = []
    for fanout in fanouts:
        next_frontier: list[int] = []
        for node in frontier:
            candidates = torch.where(adj[node] > 0)[0]
            if candidates.numel() > fanout:
                order = torch.randperm(candidates.numel(), generator=generator, device=adj.device)
                candidates = candidates[order[:fanout]]
            for source_tensor in candidates:
                source = int(source_tensor)
                sampled_edges.append((node, source))
                if source not in seen:
                    ordered_nodes.append(source)
                    seen.add(source)
                    next_frontier.append(source)
        frontier = list(dict.fromkeys(next_frontier))

    node_ids = torch.tensor(ordered_nodes, dtype=torch.long, device=adj.device)
    local_index = {node: index for index, node in enumerate(ordered_nodes)}
    sub_adj = torch.zeros((len(ordered_nodes), len(ordered_nodes)), dtype=adj.dtype, device=adj.device)
    for target, source in sampled_edges:
        sub_adj[local_index[target], local_index[source]] = adj[target, source]
    target_positions = torch.arange(len(targets), dtype=torch.long, device=adj.device)
    return node_ids, sub_adj, target_positions


def graph_hash(data: GraphData) -> str:
    digest = hashlib.sha256()
    for tensor in (data.x, data.adj, data.y, data.train_mask, data.val_mask, data.test_mask):
        digest.update(tensor.detach().cpu().numpy().tobytes())
    return digest.hexdigest()
