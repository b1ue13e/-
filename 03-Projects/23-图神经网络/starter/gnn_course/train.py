from __future__ import annotations

import csv
from copy import deepcopy
import json
import random
from pathlib import Path
from time import perf_counter

import numpy as np
import torch

from .data import GraphData, make_toy_graph, sample_batch_subgraph
from .models import GAT, GCN, GraphSAGE, MLP
from .protocol import write_manifest


MODEL_TYPES = {"mlp": MLP, "gcn": GCN, "graphsage": GraphSAGE, "gat": GAT}


def _set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def _accuracy(logits: torch.Tensor, data: GraphData, mask: torch.Tensor) -> float:
    prediction = logits.argmax(dim=1)
    return float((prediction[mask] == data.y[mask]).float().mean())


def _macro_f1(logits: torch.Tensor, data: GraphData, mask: torch.Tensor, classes: int | None = None) -> float:
    predicted = logits.argmax(dim=1)
    classes = int(data.y.max().item()) + 1 if classes is None else classes
    values = []
    for label in range(classes):
        true_positive = int(((predicted == label) & (data.y == label) & mask).sum())
        false_positive = int(((predicted == label) & (data.y != label) & mask).sum())
        false_negative = int(((predicted != label) & (data.y == label) & mask).sum())
        precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
        recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
        values.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    return float(sum(values) / len(values))


def _parameter_vector(model: torch.nn.Module) -> torch.Tensor:
    return torch.cat([parameter.detach().flatten().cpu() for parameter in model.parameters()])


def _output_variance(model: torch.nn.Module, data: GraphData) -> float:
    with torch.no_grad():
        logits = model(data.x, data.adj)
    if logits.ndim != 2 or logits.shape[0] != data.num_nodes:
        raise AssertionError("model output must have shape [num_nodes, num_classes]")
    return float(logits.var(dim=0, unbiased=False).mean())


def run_model(
    model_name: str,
    seed: int,
    data: GraphData | None = None,
    epochs: int = 120,
    *,
    hidden_channels: int = 16,
    num_layers: int = 2,
    learning_rate: float = 0.03,
    weight_decay: float = 1e-4,
    patience: int | None = None,
    fanout: int | None = None,
    batch_size: int = 16,
    run_id: str | None = None,
) -> dict[str, object]:
    if epochs < 1:
        raise ValueError("epochs must be positive")
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    if model_name not in MODEL_TYPES:
        raise ValueError(f"unknown model: {model_name}")
    _set_seed(seed)
    data = data or make_toy_graph()
    if fanout is not None and model_name != "graphsage":
        raise ValueError("fanout sampling is only supported for GraphSAGE")
    model = MODEL_TYPES[model_name](
        data.x.shape[1],
        hidden_channels,
        int(data.y.max()) + 1,
        num_layers=num_layers,
    )
    initial_parameters = _parameter_vector(model)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    loss_fn = torch.nn.CrossEntropyLoss()
    initial_loss = None
    best_epoch = 0
    best_val_loss = float("inf")
    best_state = deepcopy(model.state_dict())
    epochs_without_improvement = 0
    started = perf_counter()
    sampled_nodes: list[int] = []
    sampled_edges: list[int] = []
    for epoch in range(epochs):
        model.train()
        epoch_losses: list[float] = []
        if fanout is None:
            optimizer.zero_grad()
            logits = model(data.x, data.adj)
            loss = loss_fn(logits[data.train_mask], data.y[data.train_mask])
            loss.backward()
            optimizer.step()
            epoch_losses.append(float(loss.detach()))
        else:
            train_nodes = torch.where(data.train_mask)[0]
            order_generator = torch.Generator().manual_seed(seed + epoch * 1009)
            ordered_nodes = train_nodes[torch.randperm(len(train_nodes), generator=order_generator)]
            for start in range(0, len(ordered_nodes), batch_size):
                targets = ordered_nodes[start : start + batch_size]
                node_ids, sub_adj, target_positions = sample_batch_subgraph(
                    data.adj,
                    targets,
                    tuple([fanout] * num_layers),
                    seed + epoch * 1009 + start,
                )
                optimizer.zero_grad()
                local_logits = model(data.x[node_ids], sub_adj)
                loss = loss_fn(local_logits[target_positions], data.y[node_ids][target_positions])
                loss.backward()
                optimizer.step()
                epoch_losses.append(float(loss.detach()))
                sampled_nodes.append(int(node_ids.numel()))
                sampled_edges.append(int(sub_adj.count_nonzero()))
        if initial_loss is None:
            initial_loss = epoch_losses[0]
        model.eval()
        with torch.no_grad():
            validation_logits = model(data.x, data.adj)
            validation_loss = float(loss_fn(validation_logits[data.val_mask], data.y[data.val_mask]))
        if validation_loss < best_val_loss - 1e-8:
            best_val_loss = validation_loss
            best_epoch = epoch + 1
            best_state = deepcopy(model.state_dict())
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1
        if patience is not None and epochs_without_improvement >= patience:
            break
    epochs_ran = epoch + 1
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        logits = model(data.x, data.adj)
        selected_train_loss = float(loss_fn(logits[data.train_mask], data.y[data.train_mask]))
    final_parameters = _parameter_vector(model)
    test_predictions = logits.argmax(dim=1)
    error_nodes = torch.where(data.test_mask & (test_predictions != data.y))[0].tolist()
    return {
        "run_id": run_id or f"{model_name}-seed-{seed}",
        "model": model_name,
        "seed": seed,
        "epochs_requested": epochs,
        "epochs_ran": epochs_ran,
        "best_epoch": best_epoch,
        "stopped_early": patience is not None and epochs_ran < epochs,
        "hidden_channels": hidden_channels,
        "num_layers": num_layers,
        "fanout": "full" if fanout is None else fanout,
        "batch_size": "not-applicable" if fanout is None else batch_size,
        "training_mode": "full-graph" if fanout is None else "sampled-subgraph-mini-batch",
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "parameter_delta_l2": float(torch.linalg.vector_norm(final_parameters - initial_parameters)),
        "initial_train_loss": initial_loss,
        "final_train_loss": selected_train_loss,
        "best_val_loss": best_val_loss,
        "val_accuracy": _accuracy(logits, data, data.val_mask),
        "test_accuracy": _accuracy(logits, data, data.test_mask),
        "test_macro_f1": _macro_f1(logits, data, data.test_mask),
        "output_variance": _output_variance(model, data),
        "sampled_nodes_mean": "not-applicable" if not sampled_nodes else float(np.mean(sampled_nodes)),
        "sampled_edges_mean": "not-applicable" if not sampled_edges else float(np.mean(sampled_edges)),
        "test_evaluations": 1,
        "test_error_count": len(error_nodes),
        "test_error_nodes": json.dumps(error_nodes),
        "runtime_seconds": perf_counter() - started,
    }


def run_suite(
    output: Path,
    seeds: tuple[int, ...] = (7, 42, 2026),
    epochs: int = 120,
    data: GraphData | None = None,
) -> list[dict[str, object]]:
    output.mkdir(parents=True, exist_ok=True)
    data = data or make_toy_graph()
    training_config = {
        "models": list(MODEL_TYPES),
        "hidden_channels": 16,
        "num_layers": 2,
        "epochs": epochs,
        "learning_rate": 0.03,
        "weight_decay": 1e-4,
        "early_stopping": None,
        "graphsage_fanout": "full",
        "batch_size": 16,
    }
    write_manifest(output / "split_manifest.json", data, seeds, training_config)
    rows = [run_model(model, seed, data, epochs) for model in MODEL_TYPES for seed in seeds]
    with (output / "runs.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary: dict[str, dict[str, float]] = {}
    for model in MODEL_TYPES:
        model_rows = [row for row in rows if row["model"] == model]
        summary[model] = {
            "val_accuracy_mean": float(np.mean([row["val_accuracy"] for row in model_rows])),
            "val_accuracy_std": float(np.std([row["val_accuracy"] for row in model_rows])),
            "test_accuracy_mean": float(np.mean([row["test_accuracy"] for row in model_rows])),
            "test_accuracy_std": float(np.std([row["test_accuracy"] for row in model_rows])),
            "test_macro_f1_mean": float(np.mean([row["test_macro_f1"] for row in model_rows])),
            "test_macro_f1_std": float(np.std([row["test_macro_f1"] for row in model_rows])),
            "runtime_seconds_mean": float(np.mean([row["runtime_seconds"] for row in model_rows])),
        }
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return rows
