#!/usr/bin/env python3
"""Export explicit Anki card sections from Obsidian notes to UTF-8 TSV.

Only notes with an ``anki_deck`` frontmatter field are considered, and only
cards under a ``## 🃏 Anki 卡片`` heading are exported. This intentionally
avoids treating unrelated ``::`` text elsewhere in the vault as flashcards.
"""

from __future__ import annotations

import argparse
import csv
import html
import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "99-System" / "exports" / "anki" / "anki-cards.tsv"
CARD_HEADING = "## 🃏 Anki 卡片"


@dataclass(frozen=True)
class Card:
    front: str
    back: str
    deck: str
    tags: str


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return {}, text
    raw, body = text[4:].split("\n---\n", 1)
    values: dict[str, str] = {}
    for line in raw.splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip("\"'")
    return values, body


def parse_list(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [
        item.strip().strip("\"'")
        for item in value.split(",")
        if item.strip().strip("\"'")
    ]


def obsidian_link(path: Path) -> str:
    relative = path.relative_to(ROOT).with_suffix("").as_posix()
    return f"obsidian://open?vault={quote(ROOT.name)}&file={quote(relative)}"


def card_lines(body: str) -> list[tuple[str, str]]:
    if CARD_HEADING not in body:
        return []
    section = body.split(CARD_HEADING, 1)[1]
    section = re.split(r"^##\s+", section, maxsplit=1, flags=re.MULTILINE)[0]
    cards: list[tuple[str, str]] = []
    for raw_line in section.splitlines():
        line = re.sub(r"^\s*[-*]\s+", "", raw_line.strip())
        if not line or line.startswith("<!--") or "::" not in line:
            continue
        front, back = (part.strip() for part in line.split("::", 1))
        if front and back:
            cards.append((front, back))
    return cards


def collect_cards() -> list[Card]:
    cards: list[Card] = []
    seen_fronts: dict[str, Path] = {}
    md_paths: list[Path] = []
    skip_dirs = {".git", ".obsidian", ".claude", "书籍资源", "tmp", "exports"}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith(".")]
        for f in filenames:
            if f.endswith(".md"):
                md_paths.append(Path(dirpath) / f)
    for path in sorted(md_paths):
        text = path.read_text(encoding="utf-8-sig")
        frontmatter, body = parse_frontmatter(text)
        deck = frontmatter.get("anki_deck", "")
        if not deck or frontmatter.get("template", "").lower() == "true":
            continue
        tags = parse_list(frontmatter.get("anki_tags", ""))
        tags.extend(["obsidian", "source_" + path.stem.replace(" ", "_")])
        tag_text = " ".join(dict.fromkeys(tag.replace(" ", "_") for tag in tags))
        source = (
            f'<br><small>来源：<a href="{html.escape(obsidian_link(path))}">'
            f"{html.escape(path.stem)}</a></small>"
        )
        for front, back in card_lines(body):
            if front in seen_fronts:
                previous = seen_fronts[front].relative_to(ROOT)
                current = path.relative_to(ROOT)
                raise RuntimeError(
                    f"Duplicate Anki front field: {front!r} in {previous} and {current}"
                )
            seen_fronts[front] = path
            cards.append(
                Card(
                    front=html.escape(front),
                    back=html.escape(back) + source,
                    deck=deck,
                    tags=tag_text,
                )
            )
    return cards


def write_tsv(cards: list[Card], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        handle.write("#separator:Tab\n")
        handle.write("#html:true\n")
        handle.write("#notetype:问答题\n")
        handle.write("#deck column:3\n")
        handle.write("#tags column:4\n")
        handle.write("#columns:正面\t背面\t牌组\t标签\n")
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        for card in cards:
            writer.writerow([card.front, card.back, card.deck, card.tags])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate card sources without writing the TSV file",
    )
    args = parser.parse_args()

    cards = collect_cards()
    if not cards:
        raise RuntimeError(
            f"No cards found. Add {CARD_HEADING!r} and anki_deck frontmatter first."
        )
    if not args.check:
        write_tsv(cards, args.output)
        print(f"Exported {len(cards)} cards to {args.output}")
    else:
        print(f"Validated {len(cards)} Anki cards.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
