#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描当前仓库中 Markdown frontmatter 的完整度与规范性。"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# 默认扫描知识库根目录（本文件位于 99-System/tools/ 下，根目录是上两级）；
# 也可通过 `python scan_frontmatter.py <目录>` 指定扫描根。
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
SKIP_DIRS = {
    ".git",
    ".obsidian",
    ".pandoc",
    ".trash",
    ".tmp.drivedownload",
    ".tmp.driveupload",
    ".recovery-hold",
    "tmp",
    ".tmp",
    "__pycache__",
    "tools",
    "Assistants",
}
SKIP_FILES = {"AGENTS.md"}
FRONTMATTER_RE = re.compile(r"^\ufeff?---\s*\n(.*?)\n---", re.DOTALL)
ALLOWED_TYPES = {
    "study",
    "stage",
    "paper",
    "book",
    "project",
    "index",
    "question",
    "prompt",
    "journal",
    "feynman",
    "template",
}
REQUIRED_FIELDS = {
    "study": ["type", "topic", "created", "status", "difficulty"],
    "stage": ["type", "topic", "created", "status"],
    "paper": ["type", "topic", "created", "status", "year"],
    "book": ["type", "title", "created", "status"],
    "project": ["type", "topic", "created", "status", "progress"],
    "index": ["type", "topic", "created", "status"],
}
RECOMMENDED_FIELDS = {
    "study": ["domain", "concept", "prerequisites", "related"],
    "paper": ["domain", "concept", "related"],
    "book": ["domain", "concept", "related"],
    "project": ["project_type", "focus", "domain"],
}
STATUS_RULES = {
    "study": {"planned", "ongoing", "completed"},
    "stage": {"planned", "ongoing", "completed"},
    "paper": {"unread", "reading", "finished"},
    "book": {"unread", "reading", "finished"},
    "project": {"active", "paused", "completed", "ongoing"},
    "index": {"active", "archived"},
    "question": {"unseen", "practicing", "completed"},
    "prompt": {"draft", "active", "completed"},
    "journal": {"active", "archived", "logged"},
    "feynman": {"planned", "ongoing", "completed"},
    "template": set(),
}
EXAMPLE_LIMIT = 8


def iter_markdown_files():
    for md_file in sorted(ROOT.rglob("*.md")):
        rel = md_file.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if md_file.name in SKIP_FILES:
            continue
        yield md_file


def parse_frontmatter(content: str) -> dict[str, str] | None:
    match = FRONTMATTER_RE.search(content)
    if not match:
        return None

    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line.startswith(" ") or line.startswith("\t") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.split("#", 1)[0].strip().strip('"').strip("'")
    return data


def add_example(bucket: list[str], text: str) -> None:
    if len(bucket) < EXAMPLE_LIMIT:
        bucket.append(text)


def print_section(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


def main() -> None:
    total_files = 0
    files_with_frontmatter = 0
    template_files = 0
    missing_frontmatter: list[str] = []
    unknown_type: list[str] = []
    missing_required: list[str] = []
    invalid_status: list[str] = []
    missing_frontmatter_count = 0
    unknown_type_count = 0
    missing_required_count = 0
    invalid_status_count = 0
    suspicious_content: list[str] = []
    suspicious_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    type_template_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    recommended_coverage: dict[str, Counter[str]] = defaultdict(Counter)

    for md_file in iter_markdown_files():
        total_files += 1
        rel_path = str(md_file.relative_to(ROOT))
        content = md_file.read_text(encoding="utf-8", errors="replace")
        question_mark_runs = content.count("???")
        replacement_chars = content.count("\ufffd")
        if question_mark_runs or replacement_chars:
            suspicious_counts["files"] += 1
            suspicious_counts["question_mark_runs"] += question_mark_runs
            suspicious_counts["replacement_chars"] += replacement_chars
            add_example(
                suspicious_content,
                f"{rel_path} -> ??? x{question_mark_runs}, replacement-char x{replacement_chars}",
            )
        frontmatter = parse_frontmatter(content)

        if frontmatter is None:
            missing_frontmatter_count += 1
            add_example(missing_frontmatter, rel_path)
            continue

        files_with_frontmatter += 1
        note_type = frontmatter.get("type", "").strip()
        if not note_type:
            unknown_type_count += 1
            add_example(unknown_type, f"{rel_path} -> [缺少 type]")
            continue

        type_counts[note_type] += 1
        if note_type not in ALLOWED_TYPES:
            unknown_type_count += 1
            add_example(unknown_type, f"{rel_path} -> {note_type}")

        if frontmatter.get("template", "").lower() == "true":
            template_files += 1
            type_template_counts[note_type] += 1
            continue

        status = frontmatter.get("status", "").strip()
        if status:
            status_counts[status] += 1

        required = REQUIRED_FIELDS.get(note_type, [])
        missing = [field for field in required if not frontmatter.get(field, "").strip()]
        if missing:
            missing_required_count += 1
            add_example(missing_required, f"{rel_path} -> 缺少 {', '.join(missing)}")

        allowed_status = STATUS_RULES.get(note_type)
        if allowed_status and status and status not in allowed_status:
            invalid_status_count += 1
            add_example(
                invalid_status,
                f"{rel_path} -> {status}（允许值: {', '.join(sorted(allowed_status))}）",
            )

        for field in RECOMMENDED_FIELDS.get(note_type, []):
            if frontmatter.get(field, "").strip():
                recommended_coverage[note_type][field] += 1

    print("=" * 72)
    print("FRONTMATTER / 元数据体检报告")
    print("=" * 72)
    print()
    print("[总体统计]")
    print(f"   仓库根目录: {ROOT}")
    print(f"   扫描 Markdown 文件数: {total_files}")
    print(f"   有 frontmatter: {files_with_frontmatter}")
    print(f"   模板文件数(template: true): {template_files}")
    print(f"   无 frontmatter: {missing_frontmatter_count} (仅展示前 {EXAMPLE_LIMIT} 条)")

    print_section("[类型统计]")
    for note_type, count in type_counts.most_common():
        print(f"   {note_type:12} {count}")

    print_section("[状态统计]")
    for status, count in status_counts.most_common():
        print(f"   {status:12} {count}")

    print_section("[缺少 frontmatter 的文件示例]")
    if missing_frontmatter_count == 0:
        print("   无")
    else:
        for item in missing_frontmatter:
            print(f"   - {item}")

    print_section("[未知或缺失 type 的文件示例]")
    if unknown_type_count == 0:
        print("   无")
    else:
        for item in unknown_type:
            print(f"   - {item}")

    print_section("[缺少关键字段的文件示例]")
    if missing_required_count == 0:
        print("   无")
    else:
        for item in missing_required:
            print(f"   - {item}")

    print_section("[状态枚举异常示例]")
    if invalid_status_count == 0:
        print("   无")
    else:
        for item in invalid_status:
            print(f"   - {item}")

    print_section("[Suspicious content examples]")
    if not suspicious_content:
        print("   None")
    else:
        print(
            f"   files: {suspicious_counts['files']}, "
            f"question_mark_runs: {suspicious_counts['question_mark_runs']}, "
            f"replacement_chars: {suspicious_counts['replacement_chars']}"
        )
        for item in suspicious_content:
            print(f"   - {item}")

    print_section("[治理字段覆盖率]")
    if not recommended_coverage:
        print("   无")
    else:
        for note_type, fields in RECOMMENDED_FIELDS.items():
            non_template_count = type_counts.get(note_type, 0) - type_template_counts.get(note_type, 0)
            if non_template_count == 0:
                continue
            print(f"   {note_type}")
            for field in fields:
                covered = recommended_coverage[note_type].get(field, 0)
                percent = covered / non_template_count * 100 if non_template_count else 0
                print(f"      - {field:14} {covered:4} / {non_template_count:<4} ({percent:5.1f}%)")

    print()
    if missing_frontmatter_count or unknown_type_count or missing_required_count or invalid_status_count:
        print("扫描完成。建议优先修复：无 frontmatter / 缺少关键字段 / 状态枚举异常。")
    elif suspicious_content:
        print("Scan complete. Frontmatter checks passed; suspicious content damage remains.")
    else:
        print("扫描完成。当前 frontmatter 规范项已通过检查；下一步可继续提升治理字段覆盖率。")


if __name__ == "__main__":
    main()
