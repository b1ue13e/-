"""Repair broken explicit wikilinks when exactly one target basename exists.

The default mode is read-only. Use ``--apply`` with an empty backup directory
outside the vault to write changes. Aliases and heading/block anchors are kept.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from verify_links_and_paths import ROOT, WIKILINK_RE, audit, iter_visible_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="按唯一文件名候选修复已失效的显式 Wikilink 路径"
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--backup-dir",
        type=Path,
        help="应用修改时必填；必须是尚不存在的知识库外目录",
    )
    parser.add_argument("--limit", type=int, default=30)
    return parser.parse_args()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_raw_target(raw: str) -> tuple[str, str]:
    separators = [index for token in ("\\|", "|") if (index := raw.find(token)) >= 0]
    alias_index = min(separators) if separators else len(raw)
    head, alias = raw[:alias_index], raw[alias_index:]

    anchor_indexes = [index for token in ("#", "^") if (index := head.find(token)) >= 0]
    anchor_index = min(anchor_indexes) if anchor_indexes else len(head)
    target, anchor = head[:anchor_index], head[anchor_index:]
    return target.strip().lstrip("/"), anchor + alias


def build_repairs(root: Path) -> dict[tuple[str, str], str]:
    report = audit(root, include_archive=False)
    visible = iter_visible_files(root)
    by_name: dict[str, list[Path]] = defaultdict(list)
    by_stem: dict[str, list[Path]] = defaultdict(list)
    for path in visible:
        by_name[path.name.casefold()].append(path)
        if path.suffix.casefold() == ".md":
            by_stem[path.stem.casefold()].append(path)

    repairs: dict[tuple[str, str], str] = {}
    for item in report["broken"]:
        target = item["target"]
        if "/" not in target and "\\" not in target:
            continue
        target_path = Path(target.replace("\\", "/"))
        matches = (
            by_name.get(target_path.name.casefold(), [])
            if target_path.suffix
            else by_stem.get(target_path.name.casefold(), [])
        )
        if len(matches) != 1:
            continue
        match = matches[0]
        replacement = match.relative_to(root).as_posix()
        if match.suffix.casefold() == ".md":
            replacement = replacement[:-3]
        repairs[(item["source"], target)] = replacement
    return repairs


def rewrite_text(text: str, source: str, repairs: dict[tuple[str, str], str]) -> tuple[str, int]:
    changed = 0
    fence: str | None = None
    output: list[str] = []

    def replace(match) -> str:
        nonlocal changed
        raw = match.group(1)
        target, suffix = split_raw_target(raw)
        replacement = repairs.get((source, target))
        if replacement is None:
            return match.group(0)
        changed += 1
        return f"[[{replacement}{suffix}]]"

    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        marker = "```" if stripped.startswith("```") else "~~~" if stripped.startswith("~~~") else None
        if marker:
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            output.append(line)
            continue
        output.append(WIKILINK_RE.sub(replace, line) if fence is None else line)
    return "".join(output), changed


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    repairs = build_repairs(root)
    by_source: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for (source, old), new in repairs.items():
        by_source[source].append((old, new))

    print(f"可确定修复的链接目标: {len(repairs)}")
    print(f"涉及文件: {len(by_source)}")
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

    manifest: list[dict[str, object]] = []
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
                "before_sha256": sha256(before),
                "after_sha256": sha256(after),
            }
        )

    payload = {
        "created": datetime.now().isoformat(timespec="seconds"),
        "root": str(root),
        "changed_files": len(manifest),
        "replacement_count": total,
        "files": manifest,
    }
    (backup / "manifest.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"已修改文件: {len(manifest)}")
    print(f"已修复链接: {total}")
    print(f"备份: {backup}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
