from __future__ import annotations

import argparse
import json
from pathlib import Path

from frontier import summarize_frontier
from manifest import load_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the HW02 Markowitz smoke workflow.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    frontier = summarize_frontier(input_dir / "asset_returns.smoke.csv")
    payload = {
        "homework_id": manifest["id"],
        "title": manifest["title"],
        "stage": manifest["stage"],
        "baseline": manifest["baseline"],
        "frontier_summary": frontier,
    }
    (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (results_dir / "frontier_summary.json").write_text(json.dumps(frontier, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "quick_start.md").write_text(
        "\n".join(
            [
                f"# {manifest['id']} Smoke Run",
                "",
                f"- assets: {', '.join(frontier['assets'])}",
                f"- equal_weight: {frontier['equal_weight']}",
                f"- inverse_vol_weight: {frontier['inverse_vol_weight']}",
                "",
                "## Next Step",
                manifest["next_step"],
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
