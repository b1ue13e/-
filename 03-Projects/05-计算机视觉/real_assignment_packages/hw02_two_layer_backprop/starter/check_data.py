from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Check smoke data files for HW02.")
    parser.add_argument("--input-dir", required=True)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    required: list[str] = []
required.append('tiny_batch.smoke.csv')
required.append('overfit_batch.smoke.csv')
    missing = [name for name in required if not (input_dir / name).exists()]
    if missing:
        raise SystemExit("Missing smoke files: " + ", ".join(missing))
    print("smoke_data_ok")


if __name__ == "__main__":
    main()
