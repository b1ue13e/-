"""Repair deterministic LaTeX commands damaged by control-character escapes.

The repair is intentionally narrow: it only replaces control bytes followed by
known LaTeX command suffixes (for example TAB + ``ext`` becomes ``\\text``).
Dry-run is the default. Applying changes requires an external, empty backup
directory; every changed file is copied there and recorded in a hash manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCOPE = ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统"
REPLACEMENTS = (
    (b"\text", b"\\text", "TAB+ext -> \\text"),
    (b"\times", b"\\times", "TAB+imes -> \\times"),
    (b"\theta", b"\\theta", "TAB+heta -> \\theta"),
    (b"\tau", b"\\tau", "TAB+au -> \\tau"),
    (b"\to", b"\\to", "TAB+o -> \\to"),
    (b"\right", b"\\right", "CR+ight -> \\right"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def repair(data: bytes) -> tuple[bytes, Counter[str]]:
    counts: Counter[str] = Counter()
    repaired = data
    for damaged, correct, label in REPLACEMENTS:
        count = repaired.count(damaged)
        if count:
            repaired = repaired.replace(damaged, correct)
            counts[label] = count
    return repaired, counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", type=Path, default=DEFAULT_SCOPE)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--backup-dir",
        type=Path,
        help="Required with --apply; must be outside the repository and empty.",
    )
    return parser.parse_args()


def validate_backup_dir(path: Path | None) -> Path:
    if path is None:
        raise ValueError("--backup-dir is required with --apply")
    backup = path.resolve()
    try:
        backup.relative_to(ROOT.resolve())
    except ValueError:
        pass
    else:
        raise ValueError("backup directory must be outside the repository")
    if backup.exists() and any(backup.iterdir()):
        raise ValueError(f"backup directory is not empty: {backup}")
    backup.mkdir(parents=True, exist_ok=True)
    return backup


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
        sys.stderr.reconfigure(errors="backslashreplace")
    args = parse_args()
    scope = args.scope.resolve()
    if not scope.is_dir():
        print(f"scope does not exist: {scope}", file=sys.stderr)
        return 2

    candidates = []
    totals: Counter[str] = Counter()
    for path in sorted(scope.rglob("*.md")):
        before = path.read_bytes()
        after, counts = repair(before)
        if counts:
            candidates.append((path, before, after, counts))
            totals.update(counts)

    print(f"mode: {'apply' if args.apply else 'dry-run'}")
    print(f"scope: {scope}")
    print(f"changed files: {len(candidates)}")
    print(f"replacements: {sum(totals.values())}")
    for label, count in totals.most_common():
        print(f"  {count:4d}  {label}")

    if not args.apply:
        for path, _, _, counts in candidates:
            detail = ", ".join(f"{key}={value}" for key, value in counts.items())
            print(f"  {path.relative_to(ROOT).as_posix()} [{detail}]")
        return 0

    try:
        backup = validate_backup_dir(args.backup_dir)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    manifest_entries = []
    for path, before, after, counts in candidates:
        relative = path.relative_to(ROOT)
        backup_path = backup / relative
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        backup_path.write_bytes(before)
        if backup_path.read_bytes() != before:
            raise OSError(f"backup verification failed: {backup_path}")

        temp_path = path.with_name(f".{path.name}.latex-repair.tmp")
        temp_path.write_bytes(after)
        os.replace(temp_path, path)
        manifest_entries.append(
            {
                "path": relative.as_posix(),
                "backup": str(backup_path),
                "before_sha256": sha256(before),
                "after_sha256": sha256(after),
                "replacements": dict(counts),
            }
        )

    manifest = {
        "created_at": datetime.now().astimezone().isoformat(),
        "repository": str(ROOT),
        "scope": str(scope),
        "changed_files": len(manifest_entries),
        "replacement_count": sum(totals.values()),
        "totals": dict(totals),
        "files": manifest_entries,
    }
    manifest_path = backup / "repair-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"backup manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
