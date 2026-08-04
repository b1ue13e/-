from __future__ import annotations

import argparse
import json
from pathlib import Path

from manifest import load_manifest
from two_layer_net import run_smoke


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the HW02 smoke workflow.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    result = run_smoke(input_dir / "tiny_batch.smoke.csv", input_dir / "overfit_batch.smoke.csv")
    payload = {
        "homework_id": manifest["id"],
        "title": manifest["title"],
        "stage": manifest["stage"],
        "baseline": manifest["baseline"],
        "training_summary": result,
    }
    (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (results_dir / "training_summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "quick_start.md").write_text(
        "\n".join(
            [
                f"# {manifest['id']} Smoke Run",
                "",
                f"- initial_loss: {result['initial_loss']}",
                f"- after_one_step_loss: {result['after_one_step_loss']}",
                f"- gradient_diff: {result['gradient_diff']}",
                f"- overfit_final_loss: {result['overfit_final_loss']}",
                "",
                "## Next Step",
                manifest["next_step"],
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
