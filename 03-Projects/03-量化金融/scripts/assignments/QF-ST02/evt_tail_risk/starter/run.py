from __future__ import annotations

import argparse
import json
from pathlib import Path

from manifest import load_manifest
from tail_risk import build_tail_risk_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the QF-ST02 POT/GPD smoke workflow.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    summary = build_tail_risk_summary(input_dir / "returns.csv")
    payload = {
        "package_id": manifest["id"],
        "title": manifest["title"],
        "stage": manifest["stage"],
        "baseline": manifest["baseline"],
        "tail_risk_summary": summary,
    }
    (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (results_dir / "tail_risk_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "quick_start.md").write_text(
        "\n".join(
            [
                f"# {manifest['id']} POT/GPD Smoke Run",
                "",
                f"- threshold_loss: {summary['threshold_loss']}",
                f"- tail_event_count: {summary['tail_event_count']}",
                f"- var: {summary['var']}",
                f"- expected_shortfall: {summary['expected_shortfall']}",
                "",
                "## Next Step",
                manifest["next_step"],
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
