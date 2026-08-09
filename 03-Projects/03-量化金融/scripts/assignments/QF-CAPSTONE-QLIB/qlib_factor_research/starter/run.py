from __future__ import annotations

import argparse
import json
from pathlib import Path

from manifest import load_manifest
from protocol import build_protocol_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the Qlib capstone execution contract without running Qlib.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    summary = build_protocol_summary(
        input_dir / "qlib_manifest.json",
        input_dir / "workflow_config.yaml",
        input_dir / "baseline_protocol.json",
    )
    payload = {
        "assignment_id": manifest["id"],
        "title": manifest["title"],
        "contract_summary": summary,
    }
    (results_dir / "summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if summary["contract_status"] not in {
        "contract_template_ready",
        "contract_config_declared_unverified",
    }:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
