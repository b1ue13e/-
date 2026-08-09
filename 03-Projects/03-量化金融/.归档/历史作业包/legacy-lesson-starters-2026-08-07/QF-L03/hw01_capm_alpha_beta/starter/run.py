from __future__ import annotations

import argparse
import json
from pathlib import Path

from capm import estimate_capm
from manifest import load_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the HW01 CAPM smoke workflow.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    result = estimate_capm(
        input_dir / "prices.smoke.csv",
        input_dir / "benchmark.smoke.csv",
        input_dir / "risk_free.smoke.csv",
    )
    payload = {
        "homework_id": manifest["id"],
        "title": manifest["title"],
        "stage": manifest["stage"],
        "baseline": manifest["baseline"],
        "capm_summary": result,
    }
    (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (results_dir / "capm_summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "quick_start.md").write_text(
        "\n".join(
            [
                f"# {manifest['id']} Smoke Run",
                "",
                f"- ticker: {result['ticker']}",
                f"- observations: {result['observations']}",
                f"- alpha: {result['alpha']}",
                f"- beta: {result['beta']}",
                "",
                "## Next Step",
                manifest["next_step"],
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
