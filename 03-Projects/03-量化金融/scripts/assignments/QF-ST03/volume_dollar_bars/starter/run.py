from __future__ import annotations

import argparse
import json
from pathlib import Path

from bars import build_bar_summary
from manifest import load_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the QF-ST03 information-bar smoke workflow.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    summary = build_bar_summary(input_dir / "ticks.csv")
    payload = {
        "package_id": manifest["id"],
        "title": manifest["title"],
        "stage": manifest["stage"],
        "baseline": manifest["baseline"],
        "bar_summary": summary,
    }
    (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (results_dir / "bar_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "quick_start.md").write_text(
        "\n".join(
            [
                f"# {manifest['id']} Smoke Run",
                "",
                f"- volume_bar_count: {len(summary['volume_bars'])}",
                f"- dollar_bar_count: {len(summary['dollar_bars'])}",
                f"- volume_conserved: {summary['volume_conserved']}",
                f"- dollar_conserved: {summary['dollar_conserved']}",
                "",
                "## Next Step",
                manifest["next_step"],
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
