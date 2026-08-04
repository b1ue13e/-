from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HW14 Compression starter inference entry.")
    parser.add_argument("--test-data", required=False, help="Path to test data.")
    parser.add_argument("--checkpoint", required=True, help="Path to your checkpoint.")
    parser.add_argument("--output", required=True, help="Path to submission file.")
    return parser.parse_args()


def main() -> None:
    _ = parse_args()
    print("HW14 Compression starter inference is ready.")
    print("Student TODOs:")
    print("1. Load your checkpoint")
    print("2. Run inference on the official test split")
    print("3. Save a submission file in the required format")


if __name__ == "__main__":
    main()
