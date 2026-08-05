#!/usr/bin/env python3
"""Fail on hidden control characters and likely broken TeX escapes in Markdown."""

from __future__ import annotations

import argparse
import re
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKIP_PARTS = {".git", ".recovery-hold", ".tmp", "node_modules"}
SUSPICIOUS_TEX = re.compile(
    r"(?<![\\A-Za-z])(qquad|frac|sqrt|le|ge)(?=(?:\\[A-Za-z]+|\s*[{_^]))"
)
MISSING_MATH_COMMAND = re.compile(
    r"(?<![\\A-Za-z])(qquad|quad|hat|tau|frac|sqrt)(?=\b|\s|[_^{])"
)
FORBIDDEN_SEPARATORS = {0x7F, 0x85, 0x2028, 0x2029}


def markdown_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix.lower() == ".md" else []
    return [
        path
        for path in target.rglob("*.md")
        if not any(part in SKIP_PARTS for part in path.parts)
    ]


def math_fragments(line: str, in_display: bool) -> tuple[list[str], bool]:
    """Return TeX fragments while preserving display-math state across lines."""
    fragments: list[str] = []
    buffer: list[str] = []
    in_inline = False
    index = 0
    while index < len(line):
        if line.startswith("$$", index):
            if in_display and buffer:
                fragments.append("".join(buffer))
                buffer.clear()
            in_display = not in_display
            index += 2
            continue
        char = line[index]
        if char == "$" and (index == 0 or line[index - 1] != "\\"):
            if in_inline:
                fragments.append("".join(buffer))
                buffer.clear()
            in_inline = not in_inline
            index += 1
            continue
        if in_display or in_inline:
            buffer.append(char)
        index += 1
    if buffer and in_display:
        fragments.append("".join(buffer))
    return fragments, in_display


def audit(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []

    # Scan the raw string before any line splitting. str.splitlines() treats
    # VT, FF and NEL as separators and would erase the evidence we need.
    for index, char in enumerate(text):
        value = ord(char)
        forbidden = (value < 32 and char not in "\n\r") or value in FORBIDDEN_SEPARATORS
        if forbidden:
            line_no = text.count("\n", 0, index) + 1
            last_newline = text.rfind("\n", 0, index)
            column = index - last_newline
            issues.append(
                f"line {line_no}, column {column}: forbidden control character U+{value:04X}"
            )

    in_fence = False
    in_display_math = False
    for line_no, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if "\ufffd" in line:
            issues.append(f"line {line_no}: Unicode replacement character U+FFFD")
        for match in SUSPICIOUS_TEX.finditer(line):
            issues.append(
                f"line {line_no}: likely missing TeX backslash before {match.group(1)!r}"
            )
        if not in_fence:
            fragments, in_display_math = math_fragments(line, in_display_math)
            for math in fragments:
                for match in MISSING_MATH_COMMAND.finditer(math):
                    issues.append(
                        f"line {line_no}: missing TeX backslash before "
                        f"{match.group(1)!r} inside math"
                    )
    if in_fence:
        issues.append("end of file: unclosed fenced code block")
    if in_display_math:
        issues.append("end of file: unclosed display-math block")
    return issues


def self_test() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        good = root / "good.md"
        good.write_text(
            "$$\n\\frac{1}{2}, \\qquad \\hat p, \\tau=1\n$$\n",
            encoding="utf-8",
        )
        assert audit(good) == []

        for value in (0x0B, 0x0C, 0x85):
            bad = root / f"bad-{value:04x}.md"
            bad.write_text(f"$$\n\\{chr(value)}frac{{1}}{{2}}\n$$\n", encoding="utf-8")
            findings = audit(bad)
            assert any(f"U+{value:04X}" in finding for finding in findings), findings

        missing = root / "missing-command.md"
        missing.write_text("$$\nqquad hat p, tau=1\n$$\n", encoding="utf-8")
        findings = audit(missing)
        assert sum("missing TeX backslash" in finding for finding in findings) == 3


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=ROOT,
        help="Markdown file or directory to audit (default: vault root)",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run injected control-character and TeX regression tests first",
    )
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("Self-test passed")
    target = args.root.resolve()
    if not target.exists():
        parser.error(f"path does not exist: {target}")

    failures = 0
    files = markdown_files(target)
    for path in files:
        for issue in audit(path):
            failures += 1
            print(f"{path}: {issue}")

    print(f"Audited {len(files)} Markdown files; issues={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
