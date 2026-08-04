from __future__ import annotations

import argparse
from pathlib import Path

from dataset import apply_standardizer, compute_standardizer, load_regression_csv, train_valid_split


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HW01 starter training entry.")
    parser.add_argument("--train-csv", required=True, help="Path to training csv.")
    parser.add_argument("--output-dir", required=True, help="Directory to store your checkpoints and logs.")
    parser.add_argument("--valid-ratio", type=float, default=0.25)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    _, x, y = load_regression_csv(args.train_csv, has_target=True)
    if y is None:
        raise ValueError("Training csv must contain target column.")

    x_train, y_train, x_valid, y_valid = train_valid_split(
        x, y, valid_ratio=args.valid_ratio, seed=args.seed
    )
    mean, std = compute_standardizer(x_train)
    x_train_std = apply_standardizer(x_train, mean, std)
    x_valid_std = apply_standardizer(x_valid, mean, std)

    print("HW01 starter is ready.")
    print(f"train samples: {len(x_train_std)}, valid samples: {len(x_valid_std)}")
    print("Next steps for the student:")
    print("1. Implement your model in starter/model.py")
    print("2. Add your training loop here in starter/train.py")
    print("3. Save checkpoint + metrics to the output directory")
    print("4. Keep the submission header as: id,tested_positive")


if __name__ == "__main__":
    main()
