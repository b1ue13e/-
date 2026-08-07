#!/usr/bin/env python3
"""Prefix legacy vault links in active content, with per-file backups."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKUP = ROOT / ".recovery-hold" / "2026-07-31-link-prefix-migration"
LOG = ROOT / "99-System" / "🗄️ 归档" / "迁移日志" / "2026-07-31-link-prefix-migration.json"
ROOT_FILES = [
    "🏠 主页.md",
    "📋 使用说明.md",
    "📊 项目追踪.md",
    "🗂️ 资源总索引.md",
    "🃏 费曼技巧卡片.md",
]
ROOT_DIRS = [
    "00-Inbox",
    "01-Active Sprint",
    "02-Knowledge",
    "03-Projects",
    "99-System/🗓️ 计划执行系统",
    "02-Knowledge/📚 书库",
    "02-Knowledge/📚 论文库",
]

PATTERNS = (
    (re.compile(r"(?<!02-Knowledge/)02-Knowledge/🧠 学习系统/"), "02-Knowledge/🧠 学习系统/"),
    (re.compile(r"(?<!99-System/)99-System/🗓️ 计划执行系统/"), "99-System/🗓️ 计划执行系统/"),
    (
        re.compile(r'''(["'])02-Knowledge/🧠 学习系统\1'''),
        lambda match: (
            match.group(1) + "02-Knowledge/🧠 学习系统" + match.group(1)
        ),
    ),
)


def active_files() -> list[Path]:
    files = [ROOT / name for name in ROOT_FILES if (ROOT / name).exists()]
    for relative in ROOT_DIRS:
        base = ROOT / relative
        if base.exists():
            files.extend(base.rglob("*.md"))
    return sorted(set(files))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    operations: list[dict[str, object]] = []
    total = 0
    for path in active_files():
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        if not text:
            continue
        updated = text
        count = 0
        for pattern, replacement in PATTERNS:
            updated, replaced = pattern.subn(replacement, updated)
            count += replaced
        if updated == text:
            continue
        relative = path.relative_to(ROOT)
        if args.check:
            operations.append({"file": str(relative), "replacements": count})
            total += count
            continue
        backup = BACKUP / relative
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
        path.write_text(updated, encoding="utf-8", newline="\n")
        operations.append(
            {
                "file": str(relative),
                "replacements": count,
                "backup": str(backup.relative_to(ROOT)),
            }
        )
        total += count

    report = {
        "run_id": "2026-07-31-link-prefix-migration",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "modified_files": len(operations),
        "replacements": total,
        "operations": operations,
    }
    if not args.check:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        LOG.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps({key: value for key, value in report.items() if key != "operations"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
