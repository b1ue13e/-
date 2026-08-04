from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from dataset import OFFICIAL_INPUT_DIM, OFFICIAL_NUM_CLASSES, TEST_FEATURES, TRAIN_FEATURES, TRAIN_LABELS


def build_smoke_arrays(seed: int = 7) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create tiny synthetic arrays with the same dimensions as the official task."""

    rng = np.random.default_rng(seed)
    samples_per_class = 4
    x = np.zeros((OFFICIAL_NUM_CLASSES * samples_per_class, OFFICIAL_INPUT_DIM), dtype=np.float32)
    y = np.repeat(np.arange(OFFICIAL_NUM_CLASSES, dtype=np.int64), samples_per_class)

    for row, label in enumerate(y):
        x[row, label] = 4.0
        x[row, 39 + label] = 2.0
        x[row] += rng.normal(0.0, 0.08, size=OFFICIAL_INPUT_DIM).astype(np.float32)

    test = x[::10].copy()
    permutation = rng.permutation(len(x))
    x = x[permutation]
    y = y[permutation]
    return x, y, test


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create deterministic HW02 smoke data.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--seed", type=int, default=7)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    train, labels, test = build_smoke_arrays(seed=args.seed)
    np.save(output_dir / TRAIN_FEATURES, train)
    np.save(output_dir / TRAIN_LABELS, labels)
    np.save(output_dir / TEST_FEATURES, test)
    print(f"WROTE smoke train={train.shape} labels={labels.shape} test={test.shape}")


if __name__ == "__main__":
    main()
