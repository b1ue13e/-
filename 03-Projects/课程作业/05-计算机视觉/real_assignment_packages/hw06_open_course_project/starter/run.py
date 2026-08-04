from __future__ import annotations

import argparse
import json
from pathlib import Path

from manifest import load_manifest
from open_project import run_smoke


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the HW06 smoke workflow.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    result = run_smoke(
        input_dir / "project_plan.smoke.json",
        input_dir / "baseline_results.smoke.csv",
        input_dir / "improvement_results.smoke.csv",
    )
    payload = {
        "homework_id": manifest["id"],
        "title": manifest["title"],
        "stage": manifest["stage"],
        "baseline": manifest["baseline"],
        "project_summary": result,
    }
    (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (results_dir / "project_summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "quick_start.md").write_text(
        "\n".join(
            [
                f"# {manifest['id']} Smoke Run",
                "",
                f"- proposal_completeness: {result['proposal_completeness']}",
                f"- baseline_score: {result['baseline_score']}",
                f"- improvement_score: {result['improvement_score']}",
                f"- next_decision: {result['next_decision']}",
                "",
                "## Next Step",
                manifest["next_step"],
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
