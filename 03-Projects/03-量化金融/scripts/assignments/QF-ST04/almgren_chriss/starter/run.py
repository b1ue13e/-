from __future__ import annotations

import argparse
import json
from pathlib import Path

from execution import build_execution_summary
from manifest import load_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the QF-ST04 Almgren-Chriss smoke workflow.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    summary = build_execution_summary(
        input_dir / "parent_order.csv",
        input_dir / "liquidity_profile.csv",
    )
    payload = {
        "package_id": manifest["id"],
        "title": manifest["title"],
        "stage": manifest["stage"],
        "baseline": manifest["baseline"],
        "execution_summary": summary,
    }
    (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (results_dir / "execution_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "quick_start.md").write_text(
        "\n".join(
            [
                f"# {manifest['id']} Smoke Run",
                "",
                f"- total_qty: {summary['total_qty']}",
                f"- inventory_conserved: {summary['inventory_conserved']}",
                f"- temporary_cost_estimate: {summary['temporary_cost_estimate']}",
                "",
                "## Next Step",
                manifest["next_step"],
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
