from __future__ import annotations

import argparse
import json
from pathlib import Path

from knn_softmax import evaluate
from manifest import load_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the HW01 smoke workflow.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    result = evaluate(input_dir / "train.smoke.csv", input_dir / "val.smoke.csv")
    payload = {
        "homework_id": manifest["id"],
        "title": manifest["title"],
        "stage": manifest["stage"],
        "baseline": manifest["baseline"],
        "classification_summary": result,
    }
    (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (results_dir / "classification_summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "quick_start.md").write_text(
        "\n".join(
            [
                f"# {manifest['id']} Smoke Run",
                "",
                f"- train_size: {result['train_size']}",
                f"- val_size: {result['val_size']}",
                f"- knn_accuracy: {result['knn_accuracy']}",
                f"- softmax_accuracy: {result['softmax_accuracy']}",
                "",
                "## Next Step",
                manifest["next_step"],
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
