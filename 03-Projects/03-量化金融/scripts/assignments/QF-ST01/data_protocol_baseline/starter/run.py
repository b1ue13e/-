from __future__ import annotations

import argparse
import json
from pathlib import Path

from baseline import build_baseline_summary
from manifest import load_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the QF-ST01 no-leakage baseline smoke workflow.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    manifest = load_manifest()
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    summary = build_baseline_summary(Path(args.input_dir) / "ohlcv.csv")
    payload = {"package_id": manifest["id"], "title": manifest["title"], "baseline_summary": summary}
    (results_dir / "summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
