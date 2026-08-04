from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset

from dataset import apply_standardizer, load_test_array, save_submission, validate_official_contract
from model import MLPClassifier


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run HW02 phoneme-classification inference.")
    parser.add_argument("--data-dir", required=True, help="Directory containing test_11.npy.")
    parser.add_argument("--checkpoint", required=True, help="Path to your checkpoint.")
    parser.add_argument("--output", required=True, help="Path to submission file.")
    parser.add_argument("--batch-size", type=int, default=1024)
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    return parser.parse_args()


def choose_device(requested: str) -> torch.device:
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available")
    if requested == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(requested)


def main() -> None:
    args = parse_args()
    if args.batch_size <= 0:
        raise ValueError("batch_size must be positive")
    device = choose_device(args.device)
    checkpoint = torch.load(Path(args.checkpoint), map_location="cpu", weights_only=True)

    test = load_test_array(args.data_dir)
    validate_official_contract(
        test,
        input_dim=int(checkpoint["input_dim"]),
        num_classes=int(checkpoint["num_classes"]),
    )
    mean = checkpoint["mean"].numpy()
    std = checkpoint["std"].numpy()
    test = apply_standardizer(test, mean, std)

    model = MLPClassifier(
        input_dim=int(checkpoint["input_dim"]),
        num_classes=int(checkpoint["num_classes"]),
        hidden_dims=tuple(int(value) for value in checkpoint["hidden_dims"]),
        dropout=float(checkpoint["dropout"]),
    )
    model.load_state_dict(checkpoint["model_state"])
    model.to(device)
    model.eval()

    loader = DataLoader(TensorDataset(torch.from_numpy(test)), batch_size=args.batch_size)
    predictions: list[np.ndarray] = []
    with torch.no_grad():
        for (features,) in loader:
            logits = model(features.to(device))
            predictions.append(logits.argmax(dim=1).cpu().numpy())
    prediction_array = np.concatenate(predictions)
    save_submission(prediction_array, args.output)
    print(f"READY predictions={len(prediction_array)} output={Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
