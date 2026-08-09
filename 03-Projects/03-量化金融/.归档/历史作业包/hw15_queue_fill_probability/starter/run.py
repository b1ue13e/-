from __future__ import annotations

import argparse
import json
from pathlib import Path

from manifest import load_manifest
from queue_model import build_queue_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the HW15 queue/fill smoke workflow.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    summary = build_queue_summary(input_dir / "lob_events.smoke.csv")
    payload = {
        "homework_id": manifest["id"],
        "title": manifest["title"],
        "stage": manifest["stage"],
        "baseline": manifest["baseline"],
        "queue_summary": summary,
    }
    (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (results_dir / "queue_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "quick_start.md").write_text(
        "\n".join(
            [
                f"# {manifest['id']} Smoke Run",
                "",
                f"- queue_depth_proxy: {summary['queue_depth_proxy']}",
                f"- fill_probability_proxy: {summary['fill_probability_proxy']}",
                "",
                "## Next Step",
                manifest["next_step"],
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
