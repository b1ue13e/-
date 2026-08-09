from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np


def _write_csv(path: Path, fieldnames: Sequence[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _weighted_directed_edges(node_count: int, edge_count: int, seed: int) -> list[tuple[int, int]]:
    rng = random.Random(seed)
    candidates: list[tuple[float, int, int]] = []
    for source in range(node_count):
        for target in range(node_count):
            if source == target:
                continue
            same_community = source // 8 == target // 8
            weight = 6.0 if same_community else 1.0
            # Exponential keys provide deterministic weighted sampling without replacement.
            key = -math.log(max(rng.random(), 1e-12)) / weight
            candidates.append((key, source, target))
    candidates.sort()
    return [(source, target) for _, source, target in candidates[:edge_count]]


def _unique_undirected(edges: Iterable[tuple[int, int]]) -> list[tuple[int, int]]:
    return sorted({(min(source, target), max(source, target)) for source, target in edges if source != target})


def generate_course_data(output: Path, seed: int = 42) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    for obsolete_name in ("community_edges.csv", "propagation_edges.csv"):
        (output / obsolete_name).unlink(missing_ok=True)
    node_count = 24
    temporal_pairs = _weighted_directed_edges(node_count=node_count, edge_count=140, seed=seed)

    temporal_rows = [
        {"timestamp": index + 1, "source": source, "target": target}
        for index, (source, target) in enumerate(temporal_pairs)
    ]
    _write_csv(output / "temporal_edges.csv", ["timestamp", "source", "target"], temporal_rows)

    np_rng = np.random.default_rng(seed)
    feature_rows = []
    for node in range(node_count):
        community = node // 8
        feature_rows.append(
            {
                "node": node,
                "feature_a": f"{community + np_rng.normal(0, 0.15):.6f}",
                "feature_b": f"{np_rng.normal(0, 1):.6f}",
            }
        )
    _write_csv(output / "node_features.csv", ["node", "feature_a", "feature_b"], feature_rows)

    undirected = _unique_undirected(temporal_pairs[:110])
    ring = [(node, (node + 1) % node_count) for node in range(node_count)]
    community_edges = sorted(set(undirected).union(_unique_undirected(ring)))
    _write_csv(
        output / "structure_edges.csv",
        ["source", "target"],
        ({"source": source, "target": target} for source, target in community_edges),
    )

    signed_rows = []
    for source, target in community_edges[:90]:
        sign = 1 if source // 8 == target // 8 else -1
        signed_rows.append({"source": source, "target": target, "sign": sign})
    _write_csv(output / "signed_edges.csv", ["source", "target", "sign"], signed_rows)

    node_rows = [
        {"node": node, "group": f"g{node % 4}"}
        for node in range(node_count)
    ]
    _write_csv(output / "node_attributes.csv", ["node", "group"], node_rows)
    _write_csv(
        output / "node_labels.csv",
        ["node", "community"],
        ({"node": node, "community": node // 8} for node in range(node_count)),
    )

    directed_events = temporal_rows[:60] + [
        {"timestamp": 61, "source": 0, "target": 1},
        {"timestamp": 62, "source": 1, "target": 0},
        {"timestamp": 63, "source": 0, "target": 1},
        {"timestamp": 64, "source": 3, "target": 3},
    ]
    _write_csv(output / "directed_edges.csv", ["timestamp", "source", "target"], directed_events)

    for snapshot_index, size in enumerate((45, 85, 125), start=1):
        rows = temporal_rows[:size]
        _write_csv(
            output / f"evolution_snapshot_{snapshot_index:02d}.csv",
            ["timestamp", "source", "target"],
            rows,
        )

    generated_files = sorted(path for path in output.glob("*.csv"))
    manifest: dict[str, object] = {
        "schema_version": 1,
        "seed": seed,
        "node_count": node_count,
        "files": {
            path.name: {
                "rows": sum(1 for _ in path.open("r", encoding="utf-8")) - 1,
                "sha256": _sha256(path),
            }
            for path in generated_files
        },
        "limitations": [
            "Synthetic fixtures validate course protocols, not real social behavior.",
            "Community labels exist only in node_labels.csv and must not enter feature loading or unsupervised training.",
            "feature_a is a permitted pre-split synthetic covariate correlated with the planted structure.",
        ],
        "roles": {
            "node_features.csv": "model_input",
            "node_labels.csv": "evaluation_oracle_only",
            "node_attributes.csv": "descriptive_attribute",
            "structure_edges.csv": "shared_static_graph_for_structure_community_and_propagation",
            "temporal_edges.csv": "time_ordered_link_prediction_events",
        },
        "forbidden_feature_fields": ["community", "label", "target", "split"],
    }
    manifest_path = output / "generation_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate deterministic course fixtures.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    manifest = generate_course_data(args.output, args.seed)
    print(f"generated {len(manifest['files'])} files in {args.output}")


if __name__ == "__main__":
    main()
