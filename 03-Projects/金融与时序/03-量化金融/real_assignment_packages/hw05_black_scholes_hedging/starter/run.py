from __future__ import annotations

import argparse
import json
from pathlib import Path

from hedging import build_hedging_summary
from manifest import load_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the HW05 option hedging smoke workflow.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    summary = build_hedging_summary(
        input_dir / "underlying.smoke.csv",
        input_dir / "option_quotes.smoke.csv",
        input_dir / "risk_free.smoke.csv",
    )
    payload = {
        "homework_id": manifest["id"],
        "title": manifest["title"],
        "stage": manifest["stage"],
        "baseline": manifest["baseline"],
        "hedging_summary": summary,
    }
    (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (results_dir / "hedging_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "quick_start.md").write_text(
        "\n".join(
            [
                f"# {manifest['id']} Smoke Run",
                "",
                f"- hedge_cost_proxy: {summary['hedge_cost_proxy']}",
                f"- delta_proxy_path: {summary['delta_proxy_path']}",
                "",
                "## Next Step",
                manifest["next_step"],
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
