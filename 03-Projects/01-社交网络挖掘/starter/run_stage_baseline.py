from __future__ import annotations

import argparse
import json
from pathlib import Path

from sna_course.stage_baselines import run_stage_baseline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a small, inspectable stage baseline.")
    parser.add_argument("--stage", choices=("01", "02", "03", "05"), required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    report = run_stage_baseline(args.stage, args.data_dir, args.output, args.seed)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()

