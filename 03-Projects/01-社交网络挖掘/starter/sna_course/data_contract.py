from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, order=True)
class TemporalEdge:
    timestamp: int
    source: int
    target: int


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_temporal_edges(path: Path) -> list[TemporalEdge]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"timestamp", "source", "target"}
        if reader.fieldnames is None or not required <= set(reader.fieldnames):
            raise ValueError(f"{path} must contain columns {sorted(required)}")
        edges = [
            TemporalEdge(
                timestamp=int(row["timestamp"]),
                source=int(row["source"]),
                target=int(row["target"]),
            )
            for row in reader
        ]

    if not edges:
        raise ValueError(f"{path} contains no temporal edges")
    if edges != sorted(edges):
        raise ValueError(f"{path} must be sorted by timestamp, source, target")
    return edges


def read_node_features(path: Path) -> tuple[list[int], list[list[float]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or "node" not in reader.fieldnames:
            raise ValueError(f"{path} must contain a node column")
        forbidden = {"community", "label", "target", "split"}
        leaked = forbidden.intersection(reader.fieldnames)
        if leaked:
            raise ValueError(f"forbidden oracle columns in feature file: {sorted(leaked)}")
        feature_columns = [name for name in reader.fieldnames if name.startswith("feature_")]
        if not feature_columns:
            raise ValueError(f"{path} must contain at least one feature_* column")

        nodes: list[int] = []
        features: list[list[float]] = []
        for row in reader:
            nodes.append(int(row["node"]))
            features.append([float(row[name]) for name in feature_columns])

    if len(nodes) != len(set(nodes)):
        raise ValueError(f"{path} contains duplicate node rows")
    return nodes, features

