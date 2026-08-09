from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a real Qlib qrun workflow and preserve its evidence.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    qrun = shutil.which("qrun")
    if qrun is None:
        raise SystemExit("qrun is unavailable; activate the locked Qlib environment first")
    config = Path(args.config).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [qrun, str(config)],
        cwd=config.parent,
        text=True,
        capture_output=True,
        check=False,
    )
    (output_dir / "qrun.stdout.log").write_text(completed.stdout, encoding="utf-8")
    (output_dir / "qrun.stderr.log").write_text(completed.stderr, encoding="utf-8")
    evidence = {
        "command": [qrun, str(config)],
        "returncode": completed.returncode,
        "qlib_execution_status": "passed" if completed.returncode == 0 else "failed",
    }
    (output_dir / "qrun.evidence.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
