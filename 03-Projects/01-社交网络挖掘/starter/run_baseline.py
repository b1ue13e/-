from __future__ import annotations

import argparse
import json
from pathlib import Path

from sna_course.pipeline import run_baseline_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the leak-resistant link baseline starter.")
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--undirected",
        action="store_true",
        help="Canonicalize each edge as an unordered pair before splitting and sampling.",
    )
    args = parser.parse_args()
    metrics = run_baseline_pipeline(args.events, args.output, args.seed, directed=not args.undirected)
    print(json.dumps(metrics, ensure_ascii=False))


if __name__ == "__main__":
    main()
