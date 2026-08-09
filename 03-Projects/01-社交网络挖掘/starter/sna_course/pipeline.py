from __future__ import annotations

import csv
import json
import random
from pathlib import Path

from .baselines import score_pairs, training_graph
from .data_contract import read_temporal_edges, sha256_file
from .metrics import average_precision, precision_at_k, roc_auc
from .split import temporal_link_split


def run_baseline_pipeline(
    events_path: Path,
    output: Path,
    seed: int = 42,
    directed: bool = True,
) -> dict[str, dict[str, float]]:
    events = read_temporal_edges(events_path)
    split = temporal_link_split(events, seed=seed, directed=directed)
    graph = training_graph(split.train_edges)

    candidates = [
        *((pair, 1) for pair in split.test_positive),
        *((pair, 0) for pair in split.test_negative),
    ]
    random.Random(seed).shuffle(candidates)
    pairs = [pair for pair, _ in candidates]
    labels = [label for _, label in candidates]
    model_scores = score_pairs(graph, pairs, seed=seed)

    output.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "events": str(events_path),
        "events_sha256": sha256_file(events_path),
        "seed": seed,
        "train_cutoff": split.train_cutoff,
        "validation_cutoff": split.validation_cutoff,
        "counts": {
            "train_edges": len(split.train_edges),
            "validation_positive": len(split.validation_positive),
            "validation_negative": len(split.validation_negative),
            "test_positive": len(split.test_positive),
            "test_negative": len(split.test_negative),
        },
        "policy": {
            "edge_identity": f"{'directed' if directed else 'undirected'} first occurrence",
            "candidate_nodes": "nodes observed by train cutoff",
            "negative_rule": f"{'directed' if directed else 'undirected'} pairs never observed in the full event window",
            "features": "training graph only",
        },
    }
    (output / "split_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    metrics: dict[str, dict[str, float]] = {}
    for model, scores in model_scores.items():
        metrics[model] = {
            "average_precision": average_precision(labels, scores),
            "roc_auc": roc_auc(labels, scores),
            "precision_at_10": precision_at_k(labels, scores, min(10, len(labels))),
        }
    (output / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with (output / "predictions.csv").open("w", encoding="utf-8", newline="") as handle:
        fieldnames = ["source", "target", "label", *model_scores]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index, ((source, target), label) in enumerate(candidates):
            row: dict[str, int | float] = {
                "source": source,
                "target": target,
                "label": label,
            }
            row.update({model: scores[index] for model, scores in model_scores.items()})
            writer.writerow(row)
    return metrics
