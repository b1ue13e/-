from __future__ import annotations

import argparse
import json
from pathlib import Path

from manifest import load_manifest
from queue_model import build_queue_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the QF-ST04 queue-position and fill smoke workflow.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    summary = build_queue_summary(input_dir / "lob_events.csv")
    payload = {
        "package_id": manifest["id"],
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
                f"- initial_ahead: {summary['initial_ahead']}",
                f"- final_ahead: {summary['final_ahead']}",
                f"- observed_reached_front: {summary['observed_reached_front']}",
                f"- observed_filled: {summary['observed_filled']}",
                f"- reach_front_probability: {summary['reach_front_probability']}",
                f"- fill_probability: {summary['fill_probability']}",
                "",
                "## Next Step",
                manifest["next_step"],
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
