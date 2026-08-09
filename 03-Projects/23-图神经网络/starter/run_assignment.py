from __future__ import annotations

import argparse
from pathlib import Path

from gnn_course.stages import run_s01, run_s02, run_s03, run_s04


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a verified GNN stage worked example")
    parser.add_argument("assignment", choices=("s01", "s02", "s03", "s04"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=40)
    parser.add_argument("--seeds", type=int, nargs="+", default=[7, 42, 2026])
    args = parser.parse_args()

    if args.assignment == "s01":
        run_s01(args.output, seed=args.seeds[0], probe_epochs=args.epochs)
    elif args.assignment == "s02":
        run_s02(args.output, seeds=tuple(args.seeds), epochs=args.epochs)
    elif args.assignment == "s03":
        run_s03(
            args.output,
            seed=args.seeds[0],
            pretrain_epochs=args.epochs,
            probe_epochs=args.epochs,
        )
    else:
        run_s04(args.output)
    print(f"completed {args.assignment} worked example: {args.output}")


if __name__ == "__main__":
    main()
