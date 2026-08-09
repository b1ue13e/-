from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from starter.gnn_course.train import run_suite


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the dependency-light GNN course baseline suite")
    parser.add_argument("--output", type=Path, default=Path("artifacts/starter-smoke"))
    parser.add_argument("--epochs", type=int, default=120)
    args = parser.parse_args()
    rows = run_suite(args.output, epochs=args.epochs)
    print(f"wrote {len(rows)} runs to {args.output}")


if __name__ == "__main__":
    main()
