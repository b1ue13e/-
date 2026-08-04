from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HW03 CNN starter training entry.")
    parser.add_argument("--train-data", required=False, help="Path to training data.")
    parser.add_argument("--output-dir", required=True, help="Directory to store checkpoints and logs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    print("HW03 CNN starter is ready.")
    print("Student TODOs:")
    print("1. Load and preprocess the official data")
    print("2. Implement your model in starter/model.py")
    print("3. Add your training loop and validation logic here")
    print("4. Save checkpoints and metrics to the output directory")


if __name__ == "__main__":
    main()
