"""Make ambiguous short wikilinks explicit when context selects one active file.

Safe selection rules are deliberately narrow: prefer the only non-archive
candidate, then the only candidate in the source course, or the only candidate
inside the plan system for plan pages. Default mode is read-only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from repair_unique_explicit_links import rewrite_text
from verify_links_and_paths import ROOT, audit


ARCHIVE_PREFIX = ("99-System", "🗄️ 归档")
PLAN_PREFIX = ("99-System", "99-System/🗓️ 计划执行系统")
COURSE_RE = re.compile(r"^(?:0[1-9]|1[0-9]|2[0-9]|3[0-7])-.+")
NON_COURSE_PARTS = {"02-Knowledge", "03-Projects", "04-Review", "99-System"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="按上下文消除可唯一判定的 Wikilink 歧义")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--backup-dir", type=Path)
    parser.add_argument("--limit", type=int, default=30)
    return parser.parse_args()


def is_archive(relative: str) -> bool:
    return tuple(relative.split("/")[:2]) == ARCHIVE_PREFIX


def choose(source: str, matches: list[str]) -> tuple[str, str] | None:
    active = [match for match in matches if not is_archive(match)]
    if len(active) == 1:
        return active[0], "only-active-candidate"

    source_parts = source.split("/")
    course_parts = [
        part
        for part in source_parts
        if part not in NON_COURSE_PARTS and COURSE_RE.fullmatch(part)
    ]

    # Project cards have one canonical storage layer even when an old learning
    # path still contains a same-name copy.
    if Path(matches[0]).stem.startswith("项目-"):
        project_matches = [match for match in active if match.startswith("03-Projects/")]
        if len(course_parts) == 1:
            same_course_projects = [
                match for match in project_matches if course_parts[0] in match.split("/")
            ]
            if len(same_course_projects) == 1:
                return same_course_projects[0], "canonical-project-course"
        if len(project_matches) == 1:
            return project_matches[0], "canonical-project"

    if len(course_parts) == 1:
        same_course = [match for match in active if course_parts[0] in match.split("/")]
        if len(same_course) == 1:
            return same_course[0], "same-course"

    if tuple(source_parts[:2]) == PLAN_PREFIX:
        same_system = [match for match in active if tuple(match.split("/")[:2]) == PLAN_PREFIX]
        if len(same_system) == 1:
            return same_system[0], "same-plan-system"
    return None


def build_repairs(root: Path) -> tuple[dict[tuple[str, str], str], dict[str, int]]:
    report = audit(root, include_archive=False)
    repairs: dict[tuple[str, str], str] = {}
    reasons: dict[str, int] = defaultdict(int)
    for item in report["ambiguous"]:
        selected = choose(item["source"], item["matches"])
        if selected is None:
            continue
        target, reason = selected
        replacement = target[:-3] if target.casefold().endswith(".md") else target
        repairs[(item["source"], item["target"])] = replacement
        reasons[reason] += 1
    return repairs, dict(reasons)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    repairs, reasons = build_repairs(root)
    by_source: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for (source, old), new in repairs.items():
        by_source[source].append((old, new))

    print(f"可安全显式化的歧义目标: {len(repairs)}")
    print(f"涉及文件: {len(by_source)}")
    print(f"判定规则: {json.dumps(reasons, ensure_ascii=False)}")
    for (source, old), new in list(repairs.items())[: max(args.limit, 0)]:
        print(f"  {source}: [[{old}]] -> [[{new}]]")

    if not args.apply:
        print("只读检查完成；传入 --apply 与 --backup-dir 才会修改。")
        return 0
    if args.backup_dir is None:
        print("--apply 必须同时提供 --backup-dir", file=sys.stderr)
        return 2
    backup = args.backup_dir.resolve()
    try:
        backup.relative_to(root)
    except ValueError:
        pass
    else:
        print("备份目录必须位于知识库外", file=sys.stderr)
        return 2
    if backup.exists():
        print(f"备份目录已存在: {backup}", file=sys.stderr)
        return 2
    backup.mkdir(parents=True)

    manifest = []
    total = 0
    for source in sorted(by_source):
        path = root / source
        before = path.read_bytes()
        bom = before.startswith(b"\xef\xbb\xbf")
        text = before.decode("utf-8-sig")
        updated, count = rewrite_text(text, source, repairs)
        if count == 0:
            continue
        backup_path = backup / "files" / source
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_path)
        after = updated.encode("utf-8")
        if bom:
            after = b"\xef\xbb\xbf" + after
        path.write_bytes(after)
        total += count
        manifest.append(
            {
                "path": source,
                "replacements": count,
                "before_sha256": digest(before),
                "after_sha256": digest(after),
            }
        )

    payload = {
        "created": datetime.now().isoformat(timespec="seconds"),
        "root": str(root),
        "rules": reasons,
        "changed_files": len(manifest),
        "replacement_count": total,
        "files": manifest,
    }
    (backup / "manifest.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"已修改文件: {len(manifest)}")
    print(f"已显式化链接: {total}")
    print(f"备份: {backup}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
