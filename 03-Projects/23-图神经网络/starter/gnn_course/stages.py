from __future__ import annotations

import csv
from copy import deepcopy
import json
from pathlib import Path

import torch

from .data import GraphData, make_toy_graph
from .models import GCN
from .protocol import build_manifest
from .train import run_model, run_suite


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _accuracy(logits: torch.Tensor, labels: torch.Tensor, mask: torch.Tensor) -> float:
    return float((logits.argmax(dim=1)[mask] == labels[mask]).float().mean())


def _linear_probe(
    features: torch.Tensor,
    data: GraphData,
    seed: int,
    epochs: int,
) -> dict[str, float]:
    if epochs < 1:
        raise ValueError("probe epochs must be positive")
    torch.manual_seed(seed)
    probe = torch.nn.Linear(features.shape[1], int(data.y.max()) + 1)
    optimizer = torch.optim.Adam(probe.parameters(), lr=0.05, weight_decay=1e-4)
    loss_fn = torch.nn.CrossEntropyLoss()
    best_val_loss = float("inf")
    best_state = deepcopy(probe.state_dict())
    for _ in range(epochs):
        probe.train()
        optimizer.zero_grad()
        logits = probe(features)
        loss = loss_fn(logits[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
        probe.eval()
        with torch.no_grad():
            logits = probe(features)
            val_loss = float(loss_fn(logits[data.val_mask], data.y[data.val_mask]))
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = deepcopy(probe.state_dict())
    probe.load_state_dict(best_state)
    probe.eval()
    with torch.no_grad():
        logits = probe(features)
    return {
        "val_accuracy": _accuracy(logits, data.y, data.val_mask),
        "test_accuracy": _accuracy(logits, data.y, data.test_mask),
    }


def _walk_cooccurrence(
    adj: torch.Tensor,
    seed: int,
    walks_per_node: int = 5,
    walk_length: int = 8,
    window: int = 2,
) -> torch.Tensor:
    if min(walks_per_node, walk_length, window) < 1:
        raise ValueError("walk settings must be positive")
    generator = torch.Generator().manual_seed(seed)
    counts = torch.zeros_like(adj)
    transition = adj / adj.sum(dim=1, keepdim=True).clamp_min(1.0)
    for start in range(adj.shape[0]):
        for _ in range(walks_per_node):
            path = [start]
            current = start
            for _ in range(walk_length - 1):
                current = int(torch.multinomial(transition[current], 1, generator=generator))
                path.append(current)
            for center, node in enumerate(path):
                left = max(0, center - window)
                right = min(len(path), center + window + 1)
                for context in path[left:right]:
                    if context != node:
                        counts[node, context] += 1
    return counts


def run_s01(output: Path, seed: int = 42, probe_epochs: int = 60) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    data = make_toy_graph()
    cooccurrence = _walk_cooccurrence(data.adj, seed)
    u, singular_values, _ = torch.linalg.svd(cooccurrence)
    walk_embedding = u[:, :2] * singular_values[:2]
    degree = torch.diag(data.adj.sum(dim=1))
    _, eigenvectors = torch.linalg.eigh(degree - data.adj)
    spectral_embedding = eigenvectors[:, 1:3]
    representations = {
        "raw-features": data.x,
        "walk-svd": walk_embedding,
        "laplacian": spectral_embedding,
    }
    rows = []
    for offset, (name, features) in enumerate(representations.items()):
        metrics = _linear_probe(features.detach(), data, seed + offset, probe_epochs)
        rows.append({"representation": name, **metrics})

    with (output / "metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with (output / "cooccurrence.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerows(cooccurrence.to(torch.int64).tolist())
    manifest = build_manifest(data, [seed], {"probe_epochs": probe_epochs})
    manifest.update(
        {
            "assignment": "GNN-S01",
            "starter_status": "worked-example",
            "walk_config": {"walks_per_node": 5, "walk_length": 8, "window": 2},
            "embedding_dim": 2,
        }
    )
    _write_json(output / "manifest.json", manifest)
    summary = {
        "rows": rows,
        "singular_values": singular_values[:4].tolist(),
        "cooccurrence_total": int(cooccurrence.sum()),
    }
    _write_json(output / "summary.json", summary)
    return summary


def run_s02(
    output: Path,
    seeds: tuple[int, ...] = (7, 42, 2026),
    epochs: int = 60,
) -> list[dict[str, object]]:
    return run_suite(output, seeds=seeds, epochs=epochs)


def _masked_views(x: torch.Tensor, rate: float, generator: torch.Generator) -> tuple[torch.Tensor, torch.Tensor]:
    if not 0.0 < rate < 1.0:
        raise ValueError("mask rate must be between zero and one")
    first = x * (torch.rand(x.shape, generator=generator) >= rate)
    second = x * (torch.rand(x.shape, generator=generator) >= rate)
    return first, second


def run_s03(
    output: Path,
    seed: int = 7,
    pretrain_epochs: int = 40,
    probe_epochs: int = 60,
    mask_rate: float = 0.25,
    temperature: float = 0.5,
) -> dict[str, object]:
    if pretrain_epochs < 1:
        raise ValueError("pretrain epochs must be positive")
    output.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(seed)
    data = make_toy_graph()
    encoder = GCN(data.x.shape[1], 8, 8, num_layers=2)
    optimizer = torch.optim.Adam(encoder.parameters(), lr=0.02, weight_decay=1e-4)
    generator = torch.Generator().manual_seed(seed)
    labels = torch.arange(data.num_nodes)
    losses = []
    for _ in range(pretrain_epochs):
        first, second = _masked_views(data.x, mask_rate, generator)
        z1 = torch.nn.functional.normalize(encoder(first, data.adj), dim=1)
        z2 = torch.nn.functional.normalize(encoder(second, data.adj), dim=1)
        similarities = z1 @ z2.T / temperature
        loss = 0.5 * (
            torch.nn.functional.cross_entropy(similarities, labels)
            + torch.nn.functional.cross_entropy(similarities.T, labels)
        )
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))

    encoder.eval()
    with torch.no_grad():
        pretrained = encoder(data.x, data.adj)
    frozen_metrics = _linear_probe(pretrained, data, seed, probe_epochs)
    supervised = run_model("gcn", seed, data, epochs=probe_epochs, patience=max(2, probe_epochs // 5))
    rows = [
        {"protocol": "pretrained-frozen", **frozen_metrics},
        {
            "protocol": "supervised-from-scratch",
            "val_accuracy": supervised["val_accuracy"],
            "test_accuracy": supervised["test_accuracy"],
        },
    ]
    with (output / "runs.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    manifest = build_manifest(data, [seed], {"probe_epochs": probe_epochs})
    manifest.update(
        {
            "assignment": "GNN-S03",
            "starter_status": "worked-example",
            "pretraining_labels_visible": False,
            "mask_rate": mask_rate,
            "temperature": temperature,
            "pretrain_epochs": pretrain_epochs,
        }
    )
    _write_json(output / "manifest.json", manifest)
    summary = {
        "initial_pretrain_loss": losses[0],
        "final_pretrain_loss": losses[-1],
        "rows": rows,
        "claim_boundary": "toy worked example; no stable self-supervised gain claim",
    }
    _write_json(output / "summary.json", summary)
    return summary


def estimate_attention_cost(nodes: int, edges: int, hidden_dim: int, dtype_bytes: int = 4) -> dict[str, int]:
    if nodes < 1 or edges < 0 or hidden_dim < 1 or dtype_bytes < 1:
        raise ValueError("nodes, hidden_dim and dtype_bytes must be positive; edges may be zero")
    return {
        "nodes": nodes,
        "edges": edges,
        "hidden_dim": hidden_dim,
        "dense_score_elements": nodes * nodes,
        "sparse_score_elements": edges,
        "dense_score_bytes": nodes * nodes * dtype_bytes,
        "sparse_score_bytes": edges * dtype_bytes,
        "dense_attention_main_ops": nodes * nodes * hidden_dim,
        "sparse_attention_main_ops": edges * hidden_dim,
    }


def run_s04(output: Path) -> list[dict[str, int]]:
    output.mkdir(parents=True, exist_ok=True)
    rows = [
        estimate_attention_cost(nodes=1_000, edges=5_000, hidden_dim=64),
        estimate_attention_cost(nodes=100_000, edges=1_000_000, hidden_dim=64),
        estimate_attention_cost(nodes=100, edges=0, hidden_dim=64),
    ]
    with (output / "estimates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    _write_json(
        output / "assumptions.json",
        {
            "assignment": "GNN-S04",
            "starter_status": "worked-example",
            "scope": "attention-score tensor and leading multiply terms only",
            "excluded": ["optimizer state", "activations", "communication", "kernel overhead", "latency"],
        },
    )
    return rows
