from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from time import perf_counter

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from starter.gnn_course.data import make_contextual_sbm, with_graph_inputs
from starter.gnn_course.protocol import build_manifest
from starter.gnn_course.train import run_model


def _load_config(path: Path) -> dict[str, object]:
    config = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "num_nodes",
        "feature_dim",
        "p_in",
        "p_out",
        "feature_signal",
        "data_seed",
        "seeds",
        "epochs",
        "patience",
        "hidden_channels",
        "learning_rate",
        "weight_decay",
        "fanout",
        "batch_size",
    }
    missing = sorted(required - config.keys())
    if missing:
        raise ValueError(f"config missing fields: {', '.join(missing)}")
    if not config["seeds"]:
        raise ValueError("config seeds must not be empty")
    return config


def _accuracy(logits: torch.Tensor, labels: torch.Tensor, mask: torch.Tensor) -> float:
    prediction = logits.argmax(dim=1)
    return float((prediction[mask] == labels[mask]).float().mean())


def _macro_f1(logits: torch.Tensor, labels: torch.Tensor, mask: torch.Tensor) -> float:
    prediction = logits.argmax(dim=1)
    values = []
    for label in range(int(labels.max()) + 1):
        true_positive = int(((prediction == label) & (labels == label) & mask).sum())
        false_positive = int(((prediction == label) & (labels != label) & mask).sum())
        false_negative = int(((prediction != label) & (labels == label) & mask).sum())
        precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
        recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
        values.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    return float(sum(values) / len(values))


def _baseline_row(data, baseline: str) -> dict[str, object]:
    started = perf_counter()
    classes = int(data.y.max()) + 1
    if baseline == "majority":
        majority = int(torch.mode(data.y[data.train_mask]).values)
        logits = torch.zeros((data.num_nodes, classes))
        logits[:, majority] = 1.0
    elif baseline == "label-propagation":
        augmented = data.adj + torch.eye(data.num_nodes)
        transition = augmented / augmented.sum(dim=1, keepdim=True).clamp_min(1.0)
        train_labels = torch.nn.functional.one_hot(data.y, classes).to(torch.float32)
        logits = torch.zeros_like(train_labels)
        logits[data.train_mask] = train_labels[data.train_mask]
        for _ in range(50):
            logits = transition @ logits
            logits[data.train_mask] = train_labels[data.train_mask]
    else:
        raise ValueError(f"unknown baseline: {baseline}")
    prediction = logits.argmax(dim=1)
    error_nodes = torch.where(data.test_mask & (prediction != data.y))[0].tolist()
    return {
        "run_id": baseline,
        "model": baseline,
        "seed": "deterministic",
        "epochs_requested": 0,
        "epochs_ran": 0,
        "best_epoch": 0,
        "stopped_early": False,
        "hidden_channels": 0,
        "num_layers": 0,
        "fanout": "not-applicable",
        "batch_size": "not-applicable",
        "training_mode": "non-neural-baseline",
        "parameters": 0,
        "parameter_delta_l2": 0.0,
        "initial_train_loss": "not-applicable",
        "final_train_loss": "not-applicable",
        "best_val_loss": "not-applicable",
        "val_accuracy": _accuracy(logits, data.y, data.val_mask),
        "test_accuracy": _accuracy(logits, data.y, data.test_mask),
        "test_macro_f1": _macro_f1(logits, data.y, data.test_mask),
        "output_variance": "not-applicable",
        "sampled_nodes_mean": "not-applicable",
        "sampled_edges_mean": "not-applicable",
        "test_evaluations": 1,
        "test_error_count": len(error_nodes),
        "test_error_nodes": json.dumps(error_nodes),
        "runtime_seconds": perf_counter() - started,
        "experiment": "non-neural-baseline",
        "status": "completed",
        "error": "",
    }


def run_reference(config: dict[str, object], output: Path) -> list[dict[str, object]]:
    output.mkdir(parents=True, exist_ok=True)
    data = make_contextual_sbm(
        num_nodes=int(config["num_nodes"]),
        feature_dim=int(config["feature_dim"]),
        p_in=float(config["p_in"]),
        p_out=float(config["p_out"]),
        feature_signal=float(config["feature_signal"]),
        seed=int(config["data_seed"]),
    )
    seeds = tuple(int(seed) for seed in config["seeds"])
    training_config = {
        "models": ["mlp", "gcn", "graphsage", "gat"],
        "hidden_channels": int(config["hidden_channels"]),
        "num_layers": 2,
        "epochs": int(config["epochs"]),
        "patience": int(config["patience"]),
        "learning_rate": float(config["learning_rate"]),
        "weight_decay": float(config["weight_decay"]),
        "sampled_subgraph_batch_size": 16,
        "selection": "validation_loss_only",
        "test_used_for_selection": False,
        "reference_submission": True,
    }
    manifest = build_manifest(data, seeds, training_config)
    manifest.update(
        {
            "assignment": "GNN-CAPSTONE",
            "submission_type": "reference_submission",
            "test_used_for_selection": False,
            "source_data": "locally generated contextual SBM; no external download",
            "ablation_plan": [
                "model comparison with shared split, budget and seeds",
                "GraphSAGE full-neighborhood versus sampled-subgraph fanout=3",
                "GCN depth 1 versus depth 2 versus depth 4",
                "feature signal removed while preserving graph and split",
            ],
        }
    )
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    rows: list[dict[str, object]] = []
    rows.extend([_baseline_row(data, "majority"), _baseline_row(data, "label-propagation")])

    def execute(run_id: str, model: str, **kwargs: object) -> None:
        for seed in seeds:
            row = run_model(
                model,
                seed,
                data,
                epochs=int(config["epochs"]),
                hidden_channels=int(config["hidden_channels"]),
                learning_rate=float(config["learning_rate"]),
                weight_decay=float(config["weight_decay"]),
                patience=int(config["patience"]),
                run_id=f"{run_id}-seed-{seed}",
                **kwargs,
            )
            row.update({"experiment": run_id, "status": "completed", "error": ""})
            rows.append(row)

    execute("model-comparison", "mlp")
    execute("model-comparison", "gcn")
    execute("model-comparison", "graphsage")
    execute(
        "graphsage-fanout-3",
        "graphsage",
        fanout=int(config["fanout"]),
        batch_size=int(config["batch_size"]),
    )
    execute("model-comparison", "gat")
    execute("gcn-depth-1", "gcn", num_layers=1)
    execute("gcn-depth-4", "gcn", num_layers=4)

    no_signal = data.x.clone()
    no_signal[:, 0] = 0.0
    ablated = with_graph_inputs(data, x=no_signal)
    for seed in seeds:
        row = run_model(
            "gcn",
            seed,
            ablated,
            epochs=int(config["epochs"]),
            hidden_channels=int(config["hidden_channels"]),
            learning_rate=float(config["learning_rate"]),
            weight_decay=float(config["weight_decay"]),
            patience=int(config["patience"]),
            run_id=f"gcn-no-feature-signal-seed-{seed}",
        )
        row.update({"experiment": "gcn-no-feature-signal", "status": "completed", "error": ""})
        rows.append(row)

    with (output / "runs.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = list(rows[0])
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    summary: dict[str, object] = {}
    groups = sorted({(str(row["experiment"]), str(row["model"])) for row in rows})
    for experiment, model in groups:
        group = [
            row
            for row in rows
            if row["experiment"] == experiment and row["model"] == model
        ]
        summary[f"{experiment}/{model}"] = {
            "experiment": experiment,
            "model": model,
            "runs": len(group),
            "test_accuracy_mean": sum(float(row["test_accuracy"]) for row in group) / len(group),
            "test_accuracy_min": min(float(row["test_accuracy"]) for row in group),
            "test_accuracy_max": max(float(row["test_accuracy"]) for row in group),
            "test_error_nodes": sorted(
                {
                    node
                    for row in group
                    for node in json.loads(str(row["test_error_nodes"]))
                }
            ),
            "early_stopping_epochs": [int(row["epochs_ran"]) for row in group],
        }
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    errors = {
        str(row["run_id"]): json.loads(str(row["test_error_nodes"]))
        for row in rows
        if json.loads(str(row["test_error_nodes"]))
    }
    (output / "error_nodes.json").write_text(json.dumps(errors, indent=2) + "\n", encoding="utf-8")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the GNN capstone reference submission")
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.json"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/capstone-reference"))
    args = parser.parse_args()
    rows = run_reference(_load_config(args.config), args.output)
    print(f"wrote {len(rows)} reference runs to {args.output}")


if __name__ == "__main__":
    main()
