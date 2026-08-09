from __future__ import annotations

import json
from pathlib import Path
import platform
import sys
from typing import Iterable

import numpy as np
import torch

from .data import GraphData, graph_hash


def assert_disjoint_masks(data: GraphData) -> None:
    masks = [data.train_mask, data.val_mask, data.test_mask]
    for index, left in enumerate(masks):
        for right in masks[index + 1 :]:
            if bool((left & right).any()):
                raise AssertionError("train/val/test masks overlap")
    for mask in masks:
        if mask.dtype != torch.bool or mask.shape != (data.num_nodes,):
            raise AssertionError("each split mask must be boolean with shape [num_nodes]")
        if not bool(mask.any()):
            raise AssertionError("each split must contain at least one node")
    if not bool(torch.stack(masks).any(dim=0).all()):
        raise AssertionError("every node must belong to a split")


def assert_graph_contract(data: GraphData) -> None:
    if data.x.ndim != 2 or data.x.shape[0] != data.num_nodes:
        raise AssertionError("x must have shape [num_nodes, num_features]")
    if data.adj.shape != (data.num_nodes, data.num_nodes):
        raise AssertionError("adj must be square and aligned with x")
    if data.y.shape != (data.num_nodes,):
        raise AssertionError("y must have shape [num_nodes]")
    if not torch.isfinite(data.x).all() or not torch.isfinite(data.adj).all():
        raise AssertionError("graph inputs must be finite")
    if not torch.equal(data.adj, data.adj.T):
        raise AssertionError("course datasets must use an undirected adjacency matrix")
    assert_disjoint_masks(data)


def build_manifest(
    data: GraphData,
    seeds: Iterable[int],
    training_config: dict[str, object] | None = None,
) -> dict[str, object]:
    assert_graph_contract(data)
    return {
        "dataset": data.name,
        "graph_sha256": graph_hash(data),
        "num_nodes": data.num_nodes,
        "num_edges": int(data.adj.sum().item() // 2),
        "num_features": int(data.x.shape[1]),
        "num_classes": int(data.y.max().item()) + 1,
        "protocol": "transductive-node-classification",
        "structure_visible": True,
        "labels_used_for_loss": "train_mask_only",
        "seeds": list(seeds),
        "split_indices": {
            "train": torch.where(data.train_mask)[0].tolist(),
            "validation": torch.where(data.val_mask)[0].tolist(),
            "test": torch.where(data.test_mask)[0].tolist(),
        },
        "split_counts": {
            "train": int(data.train_mask.sum()),
            "validation": int(data.val_mask.sum()),
            "test": int(data.test_mask.sum()),
        },
        "metrics": ["accuracy", "macro_f1"],
        "training_config": training_config or {},
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "torch": torch.__version__,
            "numpy": np.__version__,
        },
    }


def write_manifest(
    path: Path,
    data: GraphData,
    seeds: Iterable[int],
    training_config: dict[str, object] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(build_manifest(data, seeds, training_config), indent=2) + "\n",
        encoding="utf-8",
    )
