from __future__ import annotations

import argparse
from pathlib import Path

from dataset import load_regression_csv, save_predictions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HW01 starter inference entry.")
    parser.add_argument("--test-csv", required=True, help="Path to test csv.")
    parser.add_argument("--checkpoint", required=True, help="Path to your saved checkpoint.")
    parser.add_argument("--output", required=True, help="Path to prediction csv.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    checkpoint_path = Path(args.checkpoint)
    ids, _, _ = load_regression_csv(args.test_csv, has_target=False)

    print("HW01 starter inference is ready.")
    print(f"Loaded test ids: {len(ids)}")
    print(f"Expected checkpoint path: {checkpoint_path}")
    print("Student TODOs:")
    print("1. Load your checkpoint")
    print("2. Run your model on the standardized test features")
    print("3. Save predictions with header: id,tested_positive")

    # Placeholder so the script still shows the required submission format.
    save_predictions(ids, [0.0] * len(ids), args.output)
    print(f"Starter submission template saved to {args.output}")


if __name__ == "__main__":
    main()
