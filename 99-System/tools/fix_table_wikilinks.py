#!/usr/bin/env python3
"""Audit and repair unescaped Obsidian wikilink aliases in Markdown tables."""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


WIKILINK_WITH_ALIAS = re.compile(r"\[\[[^\]]*(?<!\\)\|[^\]]*\]\]")
WIKILINK = re.compile(r"\[\[[^\]]+\]\]")
CODE_WRAPPED_WIKILINK = re.compile(r"`(\[\[(?!\.\.\.)[^\]]+\]\])`")
TABLE_SEPARATOR_CELL = re.compile(r":?-{3,}:?")
ARCHIVE_DIR = "🗄️ 归档"
EXCLUDED_DIRS = {".git", ".obsidian", "tmp", "exports"}


def without_eol(line: str) -> str:
    return line.rstrip("\r\n")


def unescaped_pipe_parts(line: str) -> list[str]:
    content = without_eol(line).strip().strip("|")
    return [part.strip() for part in re.split(r"(?<!\\)\|", content)]


def is_table_separator(line: str) -> bool:
    stripped = without_eol(line).strip()
    parts = unescaped_pipe_parts(line)
    return (
        stripped.startswith("|")
        and stripped.endswith("|")
        and len(parts) >= 2
        and all(TABLE_SEPARATOR_CELL.fullmatch(part) for part in parts)
    )


def find_table_rows(lines: list[str]) -> set[int]:
    rows: set[int] = set()
    in_fence = False
    index = 0

    while index < len(lines):
        stripped = without_eol(lines[index]).lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            index += 1
            continue

        if (
            not in_fence
            and index + 1 < len(lines)
            and stripped.startswith("|")
            and is_table_separator(lines[index + 1])
        ):
            cursor = index
            while cursor < len(lines):
                row = without_eol(lines[cursor]).strip()
                if not (row.startswith("|") and row.endswith("|")):
                    break
                rows.add(cursor)
                cursor += 1
            index = cursor
            continue

        index += 1

    return rows


def escape_alias_pipes(match: re.Match[str]) -> str:
    return re.sub(r"(?<!\\)\|", r"\\|", match.group(0))


def normalize_wikilink_target(match: re.Match[str]) -> str:
    content = match.group(0)[2:-2]
    escaped_alias = content.find(r"\|")
    plain_alias_match = re.search(r"(?<!\\)\|", content)
    plain_alias = plain_alias_match.start() if plain_alias_match else -1
    candidates = [position for position in (escaped_alias, plain_alias) if position >= 0]

    if candidates:
        split_at = min(candidates)
        delimiter_length = 2 if content[split_at : split_at + 2] == r"\|" else 1
        target = content[:split_at]
        alias = content[split_at + delimiter_length :]
        delimiter = content[split_at : split_at + delimiter_length]
    else:
        target = content
        alias = None
        delimiter = ""

    normalized = target.replace("\\", "/")
    if alias is not None:
        normalized += delimiter + alias
    return f"[[{normalized}]]"


def repair_file(path: Path, apply: bool) -> int:
    raw = path.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    lines = text.splitlines(keepends=True)
    changed = 0

    table_rows = find_table_rows(lines)
    in_fence = False

    for index, line in enumerate(lines):
        stripped = without_eol(line).lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        repaired = WIKILINK.sub(normalize_wikilink_target, line)
        if index in table_rows:
            repaired = WIKILINK.sub(escape_alias_pipes, repaired)
            repaired = CODE_WRAPPED_WIKILINK.sub(r"\1", repaired)

        if repaired != line:
            lines[index] = repaired
            changed += 1

    if apply and changed:
        output = "".join(lines).encode("utf-8")
        if has_bom:
            output = b"\xef\xbb\xbf" + output
        temporary = path.with_name(f".{path.name}.table-link-fix.tmp")
        temporary.write_bytes(output)
        os.replace(temporary, path)

    return changed


def iter_markdown_files(root: Path):
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if ARCHIVE_DIR in relative.parts:
            continue
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    affected_files = 0
    affected_rows = 0

    for path in iter_markdown_files(root):
        count = repair_file(path, args.apply)
        if count:
            affected_files += 1
            affected_rows += count

    mode = "repaired" if args.apply else "found"
    print(f"{mode}_files={affected_files}")
    print(f"{mode}_rows={affected_rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
