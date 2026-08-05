"""Audit Obsidian wikilinks without touching the vault.

By default this scans active Markdown only. Recovery snapshots, temporary files,
Obsidian internals, Git internals, and archived source notes are excluded so the
report reflects links that can affect the current workflow.
"""

from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
IGNORED_PARTS = {".git", ".obsidian", ".recovery-hold", ".pytest_cache", ".tmp"}
ARCHIVE_PARTS = {"🗄️ 归档"}
GENERATED_PREFIXES = (
    ("00-Inbox", "恢复待确认"),
    ("04-Review", "知识库审计"),
)
TEMPLATE_PREFIX = "99-System/📇 模板/"

BROKEN_CATEGORY_LABELS = {
    "unreadable-source": "源文件读取失败",
    "template-placeholder": "模板占位链接",
    "missing-attachment": "缺失附件",
    "broken-explicit-path": "失效显式路径",
    "unresolved-short-link": "未解析短链接",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="检查 Obsidian Wikilink 路径")
    parser.add_argument("--root", type=Path, default=ROOT, help="知识库根目录")
    parser.add_argument(
        "--include-archive",
        action="store_true",
        help="同时把归档 Markdown 作为待检查的来源",
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--limit", type=int, default=40, help="每类最多显示多少条")
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        metavar="RELATIVE_PATH",
        help="只检查指定 Markdown；可重复传入",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="存在断链或歧义链接时返回非零退出码",
    )
    return parser.parse_args()


def is_ignored(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in IGNORED_PARTS for part in parts)


def is_archive(path: Path, root: Path) -> bool:
    try:
        return any(part in ARCHIVE_PARTS for part in path.relative_to(root).parts)
    except ValueError:
        return False


def is_generated_or_quarantined(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False
    return any(parts[: len(prefix)] == prefix for prefix in GENERATED_PREFIXES)


def iter_visible_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        dirnames[:] = [
            name
            for name in dirnames
            if not name.startswith(".")
            and name not in IGNORED_PARTS
            and not is_ignored(current / name, root)
            and not is_generated_or_quarantined(current / name, root)
        ]
        files.extend(current / name for name in filenames)
    return files


def without_code_fences(text: str) -> str:
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            continue
        if fence is None:
            kept.append(line)
    return "\n".join(kept)


def clean_target(raw: str) -> str:
    # Obsidian table links commonly escape the alias separator as ``\|``.
    target = raw.replace("\\|", "|").split("|", 1)[0]
    target = target.split("#", 1)[0].split("^", 1)[0]
    return target.strip().lstrip("/")


def rel_key(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix().casefold()


def candidate_keys(source: Path, target: str, root: Path) -> list[str]:
    variants = [target]
    if not Path(target).suffix:
        variants.append(f"{target}.md")

    keys: list[str] = []
    source_dir = source.parent.relative_to(root).as_posix()
    for variant in variants:
        normalized = variant.replace("\\", "/")
        keys.append(normalized.casefold())
        relative = posixpath.normpath(posixpath.join(source_dir, normalized))
        if relative != ".." and not relative.startswith("../"):
            keys.append(relative.casefold())
    return list(dict.fromkeys(keys))


def broken_category(source: str, target: str, reason: str) -> str:
    """Classify a broken target so reports separate cleanup debt by type."""
    if reason != "目标不存在":
        return "unreadable-source"
    if source.startswith(TEMPLATE_PREFIX):
        return "template-placeholder"

    suffix = Path(target).suffix.casefold()
    if suffix and suffix != ".md":
        return "missing-attachment"
    if "/" in target or "\\" in target:
        return "broken-explicit-path"
    return "unresolved-short-link"


def audit(
    root: Path,
    include_archive: bool,
    selected_sources: list[str] | None = None,
) -> dict[str, object]:
    root = root.resolve()
    visible_files = iter_visible_files(root)
    markdown_files = [path for path in visible_files if path.suffix.casefold() == ".md"]
    if selected_sources:
        sources = []
        for relative in selected_sources:
            source = root / relative
            if not source.is_file() or source.suffix.casefold() != ".md":
                raise FileNotFoundError(f"待检查 Markdown 不存在: {relative}")
            sources.append(source)
    else:
        sources = [
            path for path in markdown_files if include_archive or not is_archive(path, root)
        ]

    by_path = {rel_key(path, root): path for path in visible_files}
    by_name: dict[str, list[Path]] = defaultdict(list)
    by_stem: dict[str, list[Path]] = defaultdict(list)
    for path in visible_files:
        by_name[path.name.casefold()].append(path)
        if path.suffix.casefold() == ".md":
            by_stem[path.stem.casefold()].append(path)

    broken: list[dict[str, str]] = []
    ambiguous: list[dict[str, object]] = []
    link_count = 0

    for source in sources:
        try:
            content = source.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            source_relative = source.relative_to(root).as_posix()
            reason = str(exc)
            broken.append(
                {
                    "source": source_relative,
                    "target": "<读取失败>",
                    "reason": reason,
                    "category": broken_category(source_relative, "<读取失败>", reason),
                }
            )
            continue

        for raw in WIKILINK_RE.findall(without_code_fences(content)):
            target = clean_target(raw)
            if not target or "${" in target or "<%" in target:
                continue
            link_count += 1

            explicit = "/" in target or "\\" in target
            resolved = [by_path[key] for key in candidate_keys(source, target, root) if key in by_path]
            resolved = list(dict.fromkeys(resolved))
            if resolved:
                continue

            target_path = Path(target)
            if explicit:
                matches: list[Path] = []
            elif target_path.suffix:
                matches = by_name.get(target_path.name.casefold(), [])
            else:
                matches = by_stem.get(target_path.name.casefold(), [])

            if not matches:
                source_relative = source.relative_to(root).as_posix()
                reason = "目标不存在"
                broken.append(
                    {
                        "source": source_relative,
                        "target": target,
                        "reason": reason,
                        "category": broken_category(source_relative, target, reason),
                    }
                )
            elif len(matches) > 1:
                ambiguous.append(
                    {
                        "source": source.relative_to(root).as_posix(),
                        "target": target,
                        "matches": [path.relative_to(root).as_posix() for path in matches],
                    }
                )

    broken_by_category = Counter(item["category"] for item in broken)
    broken_target_counts = Counter(item["target"] for item in broken)
    ambiguous_target_counts = Counter(item["target"] for item in ambiguous)

    return {
        "root": str(root),
        "source_files": len(sources),
        "wikilinks": link_count,
        "broken_count": len(broken),
        "ambiguous_count": len(ambiguous),
        "broken_by_category": dict(broken_by_category.most_common()),
        "top_broken_targets": [
            {"target": target, "count": count}
            for target, count in broken_target_counts.most_common(20)
        ],
        "top_ambiguous_targets": [
            {"target": target, "count": count}
            for target, count in ambiguous_target_counts.most_common(20)
        ],
        "broken": broken,
        "ambiguous": ambiguous,
    }


def print_human(report: dict[str, object], limit: int) -> None:
    print(f"知识库: {report['root']}")
    print(f"扫描 Markdown: {report['source_files']}")
    print(f"Wikilink: {report['wikilinks']}")
    print(f"断链: {report['broken_count']}")
    print(f"歧义链接: {report['ambiguous_count']}")

    categories = report.get("broken_by_category", {})
    if isinstance(categories, dict) and categories:
        print("断链分类:")
        for category, count in categories.items():
            label = BROKEN_CATEGORY_LABELS.get(category, category)
            print(f"  {label}: {count}")

    for label, key in (("高频断链目标", "top_broken_targets"), ("高频歧义目标", "top_ambiguous_targets")):
        items = report.get(key, [])
        if not isinstance(items, list) or not items:
            continue
        print(f"\n{label}（最多 {min(limit, 20)} 条）:")
        for item in items[: min(limit, 20)]:
            print(f"  {item['count']:>4}  [[{item['target']}]]")

    for label, key in (("断链示例", "broken"), ("歧义示例", "ambiguous")):
        items = report[key]
        if not isinstance(items, list) or not items:
            continue
        print(f"\n{label}（最多 {limit} 条）:")
        for item in items[:limit]:
            category = item.get("category")
            suffix = f" ({BROKEN_CATEGORY_LABELS.get(category, category)})" if category else ""
            print(f"  {item['source']} -> [[{item['target']}]]{suffix}")
            if "matches" in item:
                for match in item["matches"]:
                    print(f"    - {match}")


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"目录不存在: {root}", file=sys.stderr)
        return 2

    try:
        report = audit(root, args.include_archive, args.source)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report, max(args.limit, 0))

    has_findings = bool(report["broken_count"] or report["ambiguous_count"])
    return 1 if args.strict and has_findings else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
