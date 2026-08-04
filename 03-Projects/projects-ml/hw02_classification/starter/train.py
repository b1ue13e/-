from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from dataset import (
    OFFICIAL_NUM_CLASSES,
    apply_standardizer,
    compute_standardizer,
    confusion_matrix,
    load_training_arrays,
    macro_f1_from_confusion,
    save_confusion_matrix,
    stratified_train_valid_split,
    validate_official_contract,
)
from model import MLPClassifier, parse_hidden_dims


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the HW02 phoneme-classification baseline.")
    parser.add_argument("--data-dir", required=True, help="Directory containing train_11.npy and labels.")
    parser.add_argument("--output-dir", required=True, help="Directory to store checkpoints and logs.")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-5)
    parser.add_argument("--valid-ratio", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--hidden-dims", default="256,128")
    parser.add_argument("--dropout", type=float, default=0.2)
    parser.add_argument("--num-classes", type=int, default=OFFICIAL_NUM_CLASSES)
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    parser.add_argument("--max-train-samples", type=int, default=None)
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def choose_device(requested: str) -> torch.device:
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available")
    if requested == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(requested)


def evaluate(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
    num_classes: int,
) -> tuple[float, float, float, np.ndarray]:
    model.eval()
    total_loss = 0.0
    targets: list[np.ndarray] = []
    predictions: list[np.ndarray] = []
    with torch.no_grad():
        for features, labels in loader:
            features = features.to(device)
            labels = labels.to(device)
            logits = model(features)
            total_loss += float(criterion(logits, labels).item()) * len(labels)
            targets.append(labels.cpu().numpy())
            predictions.append(logits.argmax(dim=1).cpu().numpy())

    y_true = np.concatenate(targets)
    y_pred = np.concatenate(predictions)
    matrix = confusion_matrix(y_true, y_pred, num_classes)
    accuracy = float((y_true == y_pred).mean())
    macro_f1 = macro_f1_from_confusion(matrix)
    return total_loss / len(y_true), accuracy, macro_f1, matrix


def main() -> None:
    args = parse_args()
    if args.epochs <= 0 or args.batch_size <= 0:
        raise ValueError("epochs and batch_size must be positive")

    set_seed(args.seed)
    device = choose_device(args.device)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    x, y = load_training_arrays(args.data_dir)
    validate_official_contract(x, y, num_classes=args.num_classes)
    if args.max_train_samples is not None:
        if args.max_train_samples < args.num_classes * 2:
            raise ValueError("max_train_samples must leave enough rows for a stratified split")
        rng = np.random.default_rng(args.seed)
        chosen = rng.choice(len(x), size=min(args.max_train_samples, len(x)), replace=False)
        x, y = x[chosen], y[chosen]

    train_idx, valid_idx = stratified_train_valid_split(
        y, valid_ratio=args.valid_ratio, seed=args.seed
    )
    mean, std = compute_standardizer(x[train_idx])
    x_train = apply_standardizer(x[train_idx], mean, std)
    x_valid = apply_standardizer(x[valid_idx], mean, std)
    y_train, y_valid = y[train_idx], y[valid_idx]

    train_set = TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train))
    valid_set = TensorDataset(torch.from_numpy(x_valid), torch.from_numpy(y_valid))
    generator = torch.Generator().manual_seed(args.seed)
    train_loader = DataLoader(
        train_set, batch_size=args.batch_size, shuffle=True, generator=generator
    )
    valid_loader = DataLoader(valid_set, batch_size=args.batch_size, shuffle=False)

    hidden_dims = parse_hidden_dims(args.hidden_dims)
    model = MLPClassifier(
        input_dim=x.shape[1],
        num_classes=args.num_classes,
        hidden_dims=hidden_dims,
        dropout=args.dropout,
    ).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay
    )

    history: list[dict[str, float | int]] = []
    best_accuracy = -1.0
    best_epoch = 0
    best_matrix = np.zeros((args.num_classes, args.num_classes), dtype=np.int64)
    checkpoint_path = output_dir / "checkpoint.pt"

    for epoch in range(1, args.epochs + 1):
        model.train()
        train_loss_sum = 0.0
        for features, labels in train_loader:
            features = features.to(device)
            labels = labels.to(device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(features)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            train_loss_sum += float(loss.item()) * len(labels)

        train_loss = train_loss_sum / len(train_set)
        valid_loss, valid_accuracy, valid_macro_f1, matrix = evaluate(
            model, valid_loader, criterion, device, args.num_classes
        )
        row = {
            "epoch": epoch,
            "train_loss": train_loss,
            "valid_loss": valid_loss,
            "valid_accuracy": valid_accuracy,
            "valid_macro_f1": valid_macro_f1,
        }
        history.append(row)
        print(
            f"epoch={epoch:03d} train_loss={train_loss:.5f} valid_loss={valid_loss:.5f} "
            f"valid_accuracy={valid_accuracy:.5f} valid_macro_f1={valid_macro_f1:.5f}"
        )

        if valid_accuracy > best_accuracy:
            best_accuracy = valid_accuracy
            best_epoch = epoch
            best_matrix = matrix
            torch.save(
                {
                    "format_version": 1,
                    "task": "ml2021-hw02-phoneme-classification",
                    "input_dim": int(x.shape[1]),
                    "num_classes": int(args.num_classes),
                    "hidden_dims": list(hidden_dims),
                    "dropout": float(args.dropout),
                    "mean": torch.from_numpy(mean),
                    "std": torch.from_numpy(std),
                    "model_state": {key: value.detach().cpu() for key, value in model.state_dict().items()},
                    "best_epoch": best_epoch,
                    "best_valid_accuracy": best_accuracy,
                },
                checkpoint_path,
            )

    metrics = {
        "task": "ML2021 HW02 phoneme classification",
        "data_dir": str(Path(args.data_dir).resolve()),
        "train_samples": len(train_set),
        "valid_samples": len(valid_set),
        "input_dim": int(x.shape[1]),
        "num_classes": int(args.num_classes),
        "seed": args.seed,
        "device": str(device),
        "best_epoch": best_epoch,
        "best_valid_accuracy": best_accuracy,
        "history": history,
    }
    (output_dir / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (output_dir / "history.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(history[0]))
        writer.writeheader()
        writer.writerows(history)
    save_confusion_matrix(best_matrix, output_dir / "confusion_matrix.csv")
    print(f"READY checkpoint={checkpoint_path} best_valid_accuracy={best_accuracy:.5f}")


if __name__ == "__main__":
    main()
