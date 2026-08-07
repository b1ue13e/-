from __future__ import annotations

import argparse
import json
from pathlib import Path

from manifest import load_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Check required real-data files.")
    parser.add_argument("--input-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    missing = [name for name in manifest["real_files"] if not (input_dir / name).exists()]
    print(json.dumps({"homework_id": manifest["id"], "input_dir": str(input_dir), "missing_files": missing}, ensure_ascii=False, indent=2))
    if missing:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
