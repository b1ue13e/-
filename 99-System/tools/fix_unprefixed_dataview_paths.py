"""Migrate active Dataview source paths to the current knowledge root.

The old vault queried ``🧠 学习系统`` at the repository root. The directory now
lives below ``02-Knowledge``. This tool changes only quoted Dataview-style source
strings in active Markdown. It is a dry run unless ``--apply`` is supplied.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OLD_PREFIXES = ('"🧠 学习系统', "'🧠 学习系统")
NEW_PREFIXES = ('"02-Knowledge/🧠 学习系统', "'02-Knowledge/🧠 学习系统")
IGNORED_PARTS = {".git", ".obsidian", ".recovery-hold", ".tmp", "__pycache__"}
ARCHIVE_PARTS = {"🗄️ 归档"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="迁移 Dataview 学习系统来源路径")
    parser.add_argument("--root", type=Path, default=ROOT, help="知识库根目录")
    parser.add_argument("--apply", action="store_true", help="实际写入；默认仅预览")
    parser.add_argument(
        "--backup-dir",
        type=Path,
        help="仓库外备份目录；使用 --apply 时必填且必须为空或不存在",
    )
    parser.add_argument("--limit", type=int, default=30, help="最多显示多少个文件")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    return parser.parse_args()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_active_markdown(path: Path, root: Path) -> bool:
    if path.suffix.casefold() != ".md":
        return False
    relative = path.relative_to(root)
    return not any(
        part.startswith(".") or part in IGNORED_PARTS or part in ARCHIVE_PARTS
        for part in relative.parts
    )


def discover(root: Path) -> list[dict[str, object]]:
    changes: list[dict[str, object]] = []
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        dirnames[:] = [
            name
            for name in dirnames
            if not name.startswith(".")
            and name not in IGNORED_PARTS
            and name not in ARCHIVE_PARTS
        ]
        for name in filenames:
            path = current / name
            if not is_active_markdown(path, root):
                continue
            before_bytes = path.read_bytes()
            text = before_bytes.decode("utf-8-sig", errors="strict")
            replacement_count = 0
            updated = text
            for old, new in zip(OLD_PREFIXES, NEW_PREFIXES, strict=True):
                count = updated.count(old)
                if count:
                    updated = updated.replace(old, new)
                    replacement_count += count
            if replacement_count:
                bom = b"\xef\xbb\xbf" if before_bytes.startswith(b"\xef\xbb\xbf") else b""
                changes.append(
                    {
                        "path": path,
                        "relative": path.relative_to(root).as_posix(),
                        "before_bytes": before_bytes,
                        "after_bytes": bom + updated.encode("utf-8"),
                        "replacements": replacement_count,
                    }
                )
    return changes


def validate_backup_dir(root: Path, backup_dir: Path | None) -> Path:
    if backup_dir is None:
        raise ValueError("--apply 必须同时提供 --backup-dir")
    destination = backup_dir.resolve()
    try:
        destination.relative_to(root)
    except ValueError:
        pass
    else:
        raise ValueError("备份目录必须位于知识库之外")
    if destination.exists() and any(destination.iterdir()):
        raise ValueError(f"备份目录不是空目录: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    return destination


def apply_changes(root: Path, backup_dir: Path, changes: list[dict[str, object]]) -> dict[str, object]:
    manifest_files: list[dict[str, object]] = []
    for item in changes:
        source = item["path"]
        relative = Path(str(item["relative"]))
        before_bytes = bytes(item["before_bytes"])
        after_bytes = bytes(item["after_bytes"])
        backup = backup_dir / relative
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, backup)
        source.write_bytes(after_bytes)
        manifest_files.append(
            {
                "path": relative.as_posix(),
                "replacements": item["replacements"],
                "before_sha256": sha256(before_bytes),
                "after_sha256": sha256(after_bytes),
            }
        )

    manifest: dict[str, object] = {
        "created": datetime.now().astimezone().isoformat(timespec="seconds"),
        "root": str(root),
        "old_prefix": "🧠 学习系统",
        "new_prefix": "02-Knowledge/🧠 学习系统",
        "changed_files": len(changes),
        "replacement_count": sum(int(item["replacements"]) for item in changes),
        "files": manifest_files,
    }
    (backup_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"目录不存在: {root}")
        return 2

    changes = discover(root)
    report: dict[str, object] = {
        "mode": "apply" if args.apply else "dry-run",
        "root": str(root),
        "changed_files": len(changes),
        "replacement_count": sum(int(item["replacements"]) for item in changes),
        "files": [
            {"path": item["relative"], "replacements": item["replacements"]}
            for item in changes
        ],
    }

    if args.apply:
        try:
            backup_dir = validate_backup_dir(root, args.backup_dir)
        except ValueError as exc:
            print(str(exc))
            return 2
        manifest = apply_changes(root, backup_dir, changes)
        report["backup_dir"] = str(backup_dir)
        report["manifest"] = str(backup_dir / "manifest.json")
        report["changed_files"] = manifest["changed_files"]

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"模式: {report['mode']}")
        print(f"待修改文件: {report['changed_files']}")
        print(f"路径替换: {report['replacement_count']}")
        if "backup_dir" in report:
            print(f"备份目录: {report['backup_dir']}")
        limit = max(args.limit, 0)
        for item in report["files"][:limit]:
            print(f"  {item['replacements']:>3}  {item['path']}")
        remaining = len(report["files"]) - limit
        if remaining > 0:
            print(f"  ... 另有 {remaining} 个文件")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
