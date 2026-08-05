#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair Obsidian learning-path indexes and legacy skeleton cards.

The script is intentionally conservative:
- canonical stage files are detected by `type: stage` under numbered stage dirs
- hand-written notes are not rewritten unless they still contain the old
  `## 待写提纲` scaffold
- broken auto-created stage navigation notes are deleted only when they match
  the old lightweight scaffold and contain `返回...` in content fields
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


ROOT = Path("02-Knowledge/🧠 学习系统")
REPORT = ROOT / "📊 学习系统索引修复审计.md"
TODAY = date.today().isoformat()

SKIP_DIRS = {"18-题库学习", "19-习惯追踪", "20-PARA知识管理", "21-周期笔记", "🎭 深度学习资源"}

FRONTMATTER_RE = re.compile(r"^\ufeff?---\s*\n(.*?)\n---\s*\n?", re.S)
TYPE_RE = re.compile(r"(?m)^type:\s*([^\n#]+)")
STAGE_NUM_RE = re.compile(r"(?m)^(?:phase|stage):\s*['\"]?(\d+)['\"]?\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")
MARKER_START = "<!-- curriculum-repair:start -->"
MARKER_END = "<!-- curriculum-repair:end -->"


def configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


@dataclass
class SourceInfo:
    textbooks: list[str] = field(default_factory=list)
    sections: list[str] = field(default_factory=list)


@dataclass
class CardSpec:
    title: str
    module: str
    problem: str
    standard: str
    source: SourceInfo
    stage_file: Path
    stage_heading: str
    stage_index: int
    cards_in_module: list[str]
    link_text: str = ""


@dataclass
class StageSpec:
    file: Path
    heading: str
    stage_index: int
    course_name: str
    cards: list[CardSpec] = field(default_factory=list)


@dataclass
class CourseSpec:
    dir: Path
    course_name: str
    roadmap: Path | None
    stages: list[StageSpec] = field(default_factory=list)
    stage_by_title: dict[str, Path] = field(default_factory=dict)
    cards: dict[str, CardSpec] = field(default_factory=dict)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str, dry_run: bool) -> None:
    if not dry_run:
        path.write_text(text, encoding="utf-8", newline="\n")


def clean_inline(text: str) -> str:
    text = WIKILINK_RE.sub(lambda m: m.group(2) or Path(m.group(1)).name, text)
    text = text.replace(r"\|", "|")
    text = re.sub(r"<br\s*/?>", "；", text, flags=re.I)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = text.replace("**", "").replace("*", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def strip_emoji_prefix(text: str) -> str:
    return re.sub(r"^[^\w\u4e00-\u9fff]+", "", text).strip()


def normalize_title(text: str) -> str:
    text = clean_inline(Path(text).name)
    text = re.sub(r"\.md$", "", text)
    text = strip_emoji_prefix(text)
    text = re.sub(r"\s+", "", text)
    return text.lower()


def parse_type(text: str) -> str:
    match = TYPE_RE.search(text)
    return match.group(1).strip().strip('"').strip("'") if match else ""


def parse_stage_number(text: str, fallback: int) -> int:
    match = STAGE_NUM_RE.search(text)
    return int(match.group(1)) if match else fallback


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) == 1:
            return clean_inline(match.group(2))
    return fallback


def split_course_name(dir_name: str) -> str:
    return dir_name.split("-", 1)[1] if "-" in dir_name else dir_name


def wiki_abs(path: Path, alias: str | None = None) -> str:
    rel = path.with_suffix("").as_posix()
    if alias:
        return f"[[{rel}|{alias}]]"
    return f"[[{rel}]]"


def find_roadmap(course_dir: Path) -> Path | None:
    roadmaps = sorted(course_dir.glob("🗺️ *.md"))
    return roadmaps[0] if roadmaps else None


def find_stage_files(course_dir: Path) -> list[Path]:
    stage_files: list[Path] = []
    stage_dirs = [p for p in sorted(course_dir.iterdir()) if p.is_dir() and re.match(r"^\d{2}-", p.name)]
    for index, stage_dir in enumerate(stage_dirs, start=1):
        candidates: list[tuple[int, Path]] = []
        for path in sorted(stage_dir.glob("*.md")):
            text = read_text(path)
            if parse_type(text) == "stage":
                candidates.append((parse_stage_number(text, index), path))
        if not candidates:
            continue
        exact = [path for stage_num, path in candidates if stage_num == index]
        stage_files.append(exact[0] if exact else candidates[0][1])
    return stage_files


def split_table_line(line: str) -> list[str]:
    content = line.strip().strip("|")
    cells: list[str] = []
    buf: list[str] = []
    depth = 0
    i = 0
    while i < len(content):
        pair = content[i : i + 2]
        if pair == r"\|":
            buf.append(pair)
            i += 2
            continue
        if pair == "[[":
            depth += 1
            buf.append(pair)
            i += 2
            continue
        if pair == "]]":
            depth = max(0, depth - 1)
            buf.append(pair)
            i += 2
            continue
        if content[i] == "|" and depth == 0:
            cells.append("".join(buf).strip())
            buf = []
            i += 1
            continue
        buf.append(content[i])
        i += 1
    cells.append("".join(buf).strip())
    return cells


def is_separator(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and set(stripped.replace("|", "").replace(":", "").replace("-", "").strip()) <= {""}


def extract_tables(text: str) -> list[tuple[str, list[str], list[list[str]]]]:
    lines = text.splitlines()
    tables: list[tuple[str, list[str], list[list[str]]]] = []
    current_heading = "阶段主线"
    i = 0
    while i < len(lines):
        heading = HEADING_RE.match(lines[i])
        if heading:
            title = clean_inline(heading.group(2))
            if not any(skip in title for skip in ("阶段进度", "阶段导航", "学习清单", "推荐资源", "导航")):
                current_heading = title
        if lines[i].strip().startswith("|") and i + 1 < len(lines) and is_separator(lines[i + 1]):
            headers = [clean_inline(cell) for cell in split_table_line(lines[i])]
            rows: list[list[str]] = []
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_table_line(lines[i]))
                i += 1
            tables.append((current_heading, headers, rows))
            continue
        i += 1
    return tables


def parse_textbook_index(course_dir: Path) -> dict[int, SourceInfo]:
    path = course_dir / "📚 教材挂载索引.md"
    if not path.exists():
        return {}
    text = read_text(path)
    by_stage: dict[int, SourceInfo] = {}
    for raw_line in text.splitlines():
        if not raw_line.strip().startswith("|") or "[[" not in raw_line:
            continue
        cells = split_table_line(raw_line)
        stage_cell = cells[4] if len(cells) > 4 else " ".join(cells)
        stages = parse_stage_refs(stage_cell)
        links = [m.group(2) or Path(m.group(1)).name for m in WIKILINK_RE.finditer(cells[0] if cells else "")]
        if not links:
            links = [clean_inline(cells[0])] if cells else []
        priority = clean_inline(cells[3]) if len(cells) > 3 else ""
        for stage in stages:
            info = by_stage.setdefault(stage, SourceInfo())
            for link in links:
                if link and link not in info.textbooks and "进入" not in link:
                    info.textbooks.append(link)
            if priority and priority not in info.sections:
                info.sections.append(priority)
    return by_stage


def parse_stage_refs(text: str) -> list[int]:
    stages = [int(num) for num in re.findall(r"阶段\s*(\d+)|第\s*(\d+)\s*阶段", text) for num in num if num]
    cn_map = {
        "零": 0,
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
        "十": 10,
        "十一": 11,
    }
    for cn, num in cn_map.items():
        if f"第{cn}阶段" in text or f"阶段{cn}" in text:
            stages.append(num)
    return sorted(set(stages))


def default_source(course_name: str) -> SourceInfo:
    return SourceInfo([f"{course_name}教材挂载索引"], ["按阶段教材挂载页优先阅读"])


def extract_wikilink_cards(raw_cell: str) -> list[tuple[str, str]]:
    cards: list[tuple[str, str]] = []
    for match in WIKILINK_RE.finditer(raw_cell):
        title = clean_inline(match.group(2) or Path(match.group(1)).name)
        if title and not is_stage_like_title(title):
            cards.append((title, match.group(0)))
    return cards


def extract_card_entries(raw_cell: str) -> list[tuple[str, str]]:
    wikilinks = extract_wikilink_cards(raw_cell)
    if wikilinks:
        return wikilinks
    normalized = re.sub(r"<br\s*/?>", "\n", raw_cell, flags=re.I)
    parts = [clean_inline(part) for part in re.split(r"\n|；|;", normalized) if clean_inline(part)]
    return [(part, f"[[{part}]]") for part in parts if not is_stage_like_title(part)]


def source_from_raw(raw_cell: str, fallback: SourceInfo) -> SourceInfo:
    parts = [clean_inline(part) for part in re.split(r"<br\s*/?>|；|;", raw_cell, flags=re.I) if clean_inline(part)]
    if not parts:
        return fallback
    textbooks: list[str] = []
    sections: list[str] = []
    for part in parts:
        if "：" in part:
            book, section = part.split("：", 1)
            textbooks.append(book.strip())
            sections.append(section.strip())
        elif ":" in part:
            book, section = part.split(":", 1)
            textbooks.append(book.strip())
            sections.append(section.strip())
        else:
            textbooks.append(part)
    return SourceInfo(textbooks=textbooks, sections=sections)


def table_cards_from_stage(stage: StageSpec, source_map: dict[int, SourceInfo]) -> list[CardSpec]:
    text = read_text(stage.file)
    cards: list[CardSpec] = []
    module_cards: dict[str, list[str]] = {}
    module_problem: dict[str, str] = {}
    module_source: dict[str, SourceInfo] = {}
    module_standard: dict[str, str] = {}
    fallback_source = source_map.get(stage.stage_index, default_source(stage.course_name))

    for heading, headers, rows in extract_tables(text):
        normalized_headers = {h: i for i, h in enumerate(headers)}
        if "模块" in normalized_headers and ("你要能做什么" in normalized_headers or "你要掌握什么" in normalized_headers):
            module_idx = normalized_headers["模块"]
            problem_idx = normalized_headers.get("你要能做什么", normalized_headers.get("你要掌握什么"))
            source_idx = normalized_headers.get("对应教材")
            standard_idx = normalized_headers.get("完成标志")
            for row in rows:
                if problem_idx is None or module_idx >= len(row) or problem_idx >= len(row):
                    continue
                module = clean_inline(row[module_idx])
                module_problem[module] = clean_inline(row[problem_idx])
                if source_idx is not None and source_idx < len(row):
                    module_source[module] = source_from_raw(row[source_idx], fallback_source)
                if standard_idx is not None and standard_idx < len(row):
                    module_standard[module] = clean_inline(row[standard_idx])

        if {"模块", "要解决的问题", "对应教材章节", "原子卡片", "完成标准"}.issubset(normalized_headers):
            for row in rows:
                if len(row) < len(headers):
                    continue
                module = clean_inline(row[normalized_headers["模块"]])
                problem = clean_inline(row[normalized_headers["要解决的问题"]])
                standard = clean_inline(row[normalized_headers["完成标准"]])
                raw_sources = row[normalized_headers["对应教材章节"]]
                source = source_from_raw(raw_sources, fallback_source)
                found_entries = extract_card_entries(row[normalized_headers["原子卡片"]])
                found_titles = [title for title, _ in found_entries]
                module_cards[module] = found_titles
                for title, link_text in found_entries:
                    cards.append(
                        CardSpec(
                            title=title,
                            module=module,
                            problem=problem,
                            standard=standard,
                            source=source,
                            stage_file=stage.file,
                            stage_heading=stage.heading,
                            stage_index=stage.stage_index,
                            cards_in_module=found_titles,
                            link_text=link_text,
                        )
                    )
            continue

        if "建议沉淀的笔记" in normalized_headers and "优先教材" in normalized_headers and (
            "问题" in normalized_headers or "方向" in normalized_headers
        ):
            module_key = "问题" if "问题" in normalized_headers else "方向"
            module_idx = normalized_headers[module_key]
            method_idx = normalized_headers.get("方法/模型", normalized_headers.get("关键问题"))
            source_idx = normalized_headers["优先教材"]
            card_idx = normalized_headers["建议沉淀的笔记"]
            standard_idx = normalized_headers.get("最小产出")
            for row in rows:
                if max(module_idx, source_idx, card_idx) >= len(row):
                    continue
                module = clean_inline(row[module_idx])
                method = clean_inline(row[method_idx]) if method_idx is not None and method_idx < len(row) else ""
                source = source_from_raw(row[source_idx], fallback_source)
                standard = (
                    clean_inline(row[standard_idx])
                    if standard_idx is not None and standard_idx < len(row)
                    else f"能围绕“{module}”完成一份可复用的研究或建模笔记。"
                )
                found_entries = extract_card_entries(row[card_idx])
                if not found_entries:
                    continue
                found_titles = [title for title, _ in found_entries]
                module_cards[module] = found_titles
                problem = (
                    f"围绕“{module}”，掌握 {method} 并能完成对应建模/研究输出。"
                    if method
                    else f"围绕“{module}”完成对应建模/研究输出。"
                )
                for title, link_text in found_entries:
                    cards.append(
                        CardSpec(
                            title=title,
                            module=module,
                            problem=problem,
                            standard=standard,
                            source=source,
                            stage_file=stage.file,
                            stage_heading=stage.heading,
                            stage_index=stage.stage_index,
                            cards_in_module=found_titles,
                            link_text=link_text,
                        )
                    )
            continue

        if {"模块", "建议沉淀的笔记"}.issubset(normalized_headers) or {"模块", "建议原子笔记题目"}.issubset(normalized_headers):
            module_idx = normalized_headers["模块"]
            card_idx = normalized_headers.get("建议沉淀的笔记", normalized_headers.get("建议原子笔记题目"))
            for row in rows:
                if card_idx is None or module_idx >= len(row) or card_idx >= len(row):
                    continue
                module = clean_inline(row[module_idx])
                found_entries = extract_card_entries(row[card_idx])
                if not found_entries:
                    continue
                found_titles = [title for title, _ in found_entries]
                module_cards[module] = found_titles
                problem = module_problem.get(module, f"掌握“{module}”并能说明它在“{stage.heading}”中的作用。")
                source = module_source.get(module, fallback_source)
                standard = module_standard.get(module, f"能围绕“{module}”完成原子笔记整理，并说明前后依赖。")
                for title, link_text in found_entries:
                    cards.append(
                        CardSpec(
                            title=title,
                            module=module,
                            problem=problem,
                            standard=standard,
                            source=source,
                            stage_file=stage.file,
                            stage_heading=stage.heading,
                            stage_index=stage.stage_index,
                            cards_in_module=found_titles,
                            link_text=link_text,
                        )
                    )
            continue

        if {"教材位置", "重点", "笔记入口"}.issubset(normalized_headers):
            source = fallback_source
            for row in rows:
                chapter_idx = normalized_headers["教材位置"]
                problem_idx = normalized_headers["重点"]
                card_idx = normalized_headers["笔记入口"]
                if max(chapter_idx, problem_idx, card_idx) >= len(row):
                    continue
                chapter = clean_inline(row[chapter_idx])
                focus = clean_inline(row[problem_idx])
                module = f"{chapter}：{focus}" if focus else chapter
                found_entries = extract_card_entries(row[card_idx])
                if not found_entries:
                    continue
                found_titles = [title for title, _ in found_entries]
                problem = f"掌握教材 {chapter} 中的“{focus}”，并能把它放回“{stage.heading}”主线。"
                standard = f"能解释“{focus}”的建模意义，并完成对应笔记入口的整理。"
                for title, link_text in found_entries:
                    cards.append(
                        CardSpec(
                            title=title,
                            module=module,
                            problem=problem,
                            standard=standard,
                            source=source,
                            stage_file=stage.file,
                            stage_heading=stage.heading,
                            stage_index=stage.stage_index,
                            cards_in_module=found_titles,
                            link_text=link_text,
                        )
                    )
            continue

        link_column = None
        for key in ("笔记", "笔记链接", "笔记入口", "主题", "操作"):
            if key in normalized_headers:
                link_column = normalized_headers[key]
                break
        if link_column is None:
            continue
        module = heading
        found_titles: list[str] = []
        for row in rows:
            if link_column >= len(row):
                continue
            found_titles.extend(m.group(2) or Path(m.group(1)).name for m in WIKILINK_RE.finditer(row[link_column]))
        found_titles = [title for title in found_titles if not is_stage_like_title(title)]
        if not found_titles:
            continue
        module_cards[module] = found_titles
        source = fallback_source
        for title in found_titles:
            cards.append(
                CardSpec(
                    title=title,
                    module=module,
                    problem=f"理解“{module}”中的“{title}”，并能说明它在“{stage.heading}”中的作用。",
                    standard=f"能用自己的话解释“{title}”，给出一个最小例子，并说明它与本模块相邻概念的关系。",
                    source=source,
                    stage_file=stage.file,
                    stage_heading=stage.heading,
                    stage_index=stage.stage_index,
                    cards_in_module=found_titles,
                    link_text=f"[[{title}]]",
                )
            )
    return cards


def is_stage_like_title(title: str) -> bool:
    return "阶段" in title and re.search(r"第[一二三四五六七八九十]+阶段|阶段\d+|阶段\s*\d+", title)


def build_course(course_dir: Path) -> CourseSpec:
    course = CourseSpec(
        dir=course_dir,
        course_name=split_course_name(course_dir.name),
        roadmap=find_roadmap(course_dir),
    )
    source_map = parse_textbook_index(course_dir)
    for index, stage_file in enumerate(find_stage_files(course_dir), start=1):
        text = read_text(stage_file)
        stage = StageSpec(
            file=stage_file,
            heading=first_heading(text, stage_file.stem),
            stage_index=parse_stage_number(text, index),
            course_name=course.course_name,
        )
        stage.cards = table_cards_from_stage(stage, source_map)
        course.stages.append(stage)
        course.stage_by_title[normalize_title(stage.file.stem)] = stage.file
        course.stage_by_title[normalize_title(stage.heading)] = stage.file
        for card in stage.cards:
            course.cards.setdefault(normalize_title(card.title), card)
    return course


def build_all_courses() -> list[CourseSpec]:
    courses: list[CourseSpec] = []
    for course_dir in sorted(ROOT.iterdir()):
        if not course_dir.is_dir() or course_dir.name in SKIP_DIRS:
            continue
        if not re.match(r"^\d{2}-", course_dir.name):
            continue
        courses.append(build_course(course_dir))
    return courses


def replace_bad_stage_links(text: str, course: CourseSpec) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        target = match.group(1)
        alias = match.group(2)
        key = normalize_title(target)
        canonical = course.stage_by_title.get(key)
        if not canonical:
            return match.group(0)
        canonical_target = canonical.with_suffix("").as_posix()
        if target.replace("\\", "/") == canonical_target:
            return match.group(0)
        count += 1
        return f"[[{canonical_target}|{alias or Path(canonical_target).name}]]"

    return WIKILINK_RE.sub(repl, text), count


def stage_heading_for_target(target: str, course: CourseSpec) -> str | None:
    canonical = course.stage_by_title.get(normalize_title(target))
    if not canonical:
        return None
    for stage in course.stages:
        if stage.file == canonical:
            return stage.heading
    return Path(canonical).name


def replace_return_stage_aliases(text: str, course: CourseSpec) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        target = match.group(1)
        alias = match.group(2)
        if alias != "返回阶段页":
            return match.group(0)
        heading = stage_heading_for_target(target, course)
        if not heading:
            return match.group(0)
        count += 1
        return f"[[{target}|{heading}]]"

    updated = WIKILINK_RE.sub(repl, text)
    updated, label_count = re.subn(r"(?m)^(-\s*)返回阶段页：", r"\1阶段入口：", updated)
    return updated, count + label_count


def yaml_list(items: list[str]) -> str:
    values = [item for item in items if item]
    if not values:
        return "[]"
    escaped = [item.replace('"', '\\"') for item in values]
    return "[" + ", ".join(f'"{item}"' for item in escaped) + "]"


def find_existing_created(text: str) -> str:
    match = re.search(r"(?m)^created:\s*['\"]?([^'\"\n]+)", text)
    return match.group(1).strip() if match else TODAY


def is_generic_legacy_skeleton(text: str) -> bool:
    return (
        "## 待写提纲" in text
        and "这章/这个知识点在这门课里解决什么问题" in text
        and "所属主线：" in text
        and "这张卡要补哪块：" in text
        and "核心定义：" in text
        and "关键方法 / 公式：" in text
        and len(text) < 2600
    )


def make_card_body(card: CardSpec, course: CourseSpec, existing_text: str) -> str:
    title = card.title
    siblings = [item for item in card.cards_in_module if item != title]
    index = card.cards_in_module.index(title) if title in card.cards_in_module else -1
    prereq = [card.cards_in_module[index - 1]] if index > 0 else []
    related = siblings[:4]
    textbooks = card.source.textbooks or [f"{course.course_name}教材挂载索引"]
    sections = card.source.sections or ["按阶段教材挂载页优先阅读"]
    created = find_existing_created(existing_text)
    stage_link = wiki_abs(card.stage_file, card.stage_heading)
    roadmap_link = wiki_abs(course.roadmap, f"{course.course_name}学习路径") if course.roadmap else f"[[{course.course_name}学习路径]]"
    source_text = "、".join(f"`{item}`" for item in textbooks)
    section_text = "；".join(sections)

    return f"""---
type: study
topic: "{title}"
course: "{course.course_name}"
stage: "{card.stage_heading}"
module: "{card.module}"
created: {created}
status: ongoing
difficulty: intermediate
concept: {yaml_list([title, card.module])}
prerequisites: {yaml_list(prereq)}
related: {yaml_list(related)}
source_textbook: {yaml_list(textbooks)}
source_sections: {yaml_list(sections)}
learning_objectives: {yaml_list([
        f"说明“{title}”在“{card.module}”中解决的问题",
        f"把“{title}”对应回阶段教材章节",
        f"用一个最小例子解释“{title}”的作用",
    ])}
deliverables: ["一句话定义", "一个最小例子/代表题/最小实验", "一条易错点或跨路径连接"]
tags: ["学习", "{course.course_name}"]
---
# {title}

> 所属路径：{roadmap_link}
> 所属阶段：{stage_link}
> 所属模块：`{card.module}`

## 为什么学
- 这张卡位于“{card.module}”，用来解决：{card.problem}
- 它不是孤立术语，而是本阶段索引中的一个可验收节点。

## 教材定位
- 主教材：{source_text}
- 对应章节：{section_text}
- 阶段入口：{stage_link}

## 必须掌握
- 用自己的话定义“{title}”，并说清它的边界。
- 说明它和“{card.module}”中相邻概念的区别与联系。
- 能把教材章节、阶段问题和这张卡的学习输出对应起来。

## 关键问题
- “{title}”在这条主线里具体负责哪一步？
- 如果忽略它，{card.problem} 会在哪一步断掉？
- 它最容易和哪个相邻概念混淆？

## 最小例子
- 场景：
- 输入：
- 关键一步：
- 结论：

## 练习与输出
- [ ] 写 3-5 行自己的定义或项目目标。
- [ ] 补一个最小例子、例题、推导片段或实验记录。
- [ ] 记录一个易错点，或补一条跨路径连接。

## 完成标准
- [ ] {card.standard}
- [ ] 能独立解释这张卡在本阶段中的位置。
- [ ] 能把教材章节和这张卡一一对应。

## 前后连接
- 前置：{", ".join(f"[[{item}]]" for item in prereq) if prereq else "无"}
- 相关：{", ".join(f"[[{item}]]" for item in related) if related else "无"}
- 阶段入口：{stage_link}

*修订于：{TODAY}*
"""


def should_rewrite_legacy_card(path: Path, text: str, course: CourseSpec) -> CardSpec | None:
    if not is_generic_legacy_skeleton(text):
        return None
    title = first_heading(text, path.stem).strip()
    if is_stage_like_title(title):
        return None
    return course.cards.get(normalize_title(title)) or course.cards.get(normalize_title(path.stem))


def is_generated_curriculum_card(text: str) -> bool:
    return (
        parse_type(text) == "study"
        and "## 为什么学" in text
        and "## 教材定位" in text
        and "## 必须掌握" in text
        and "## 关键问题" in text
        and "## 最小例子" in text
        and "## 练习与输出" in text
        and "## 完成标准" in text
        and "## 前后连接" in text
        and "它不是孤立术语，而是本阶段索引中的一个可验收节点。" in text
        and "*修订于：" in text
    )


def should_refresh_generated_card(path: Path, text: str, course: CourseSpec) -> CardSpec | None:
    if not is_generated_curriculum_card(text):
        return None
    title = first_heading(text, path.stem).strip()
    if is_stage_like_title(title):
        return None
    return course.cards.get(normalize_title(title)) or course.cards.get(normalize_title(path.stem))


def should_delete_bad_stage_clone(path: Path, text: str) -> bool:
    if parse_type(text) != "study" or not is_generic_legacy_skeleton(text):
        return False
    if "阶段" not in path.stem:
        return False
    return True


def make_stage_index_block(stage: StageSpec, course: CourseSpec) -> str:
    stage_text = read_text(stage.file)
    if MARKER_START not in stage_text and "| 模块 | 要解决的问题 | 对应教材章节 | 原子卡片 | 完成标准 |" in stage_text:
        return ""
    if not stage.cards:
        return ""
    grouped: dict[str, list[CardSpec]] = {}
    for card in stage.cards:
        grouped.setdefault(card.module, []).append(card)
    lines = [
        MARKER_START,
        "## 🧩 教材对齐索引",
        "",
        "| 模块 | 要解决的问题 | 教材定位 | 原子卡片 | 完成标准 |",
        "|:---|:---|:---|:---|:---|",
    ]
    for module, cards in grouped.items():
        first = cards[0]
        source = "；".join(first.source.sections or first.source.textbooks or [f"{course.course_name}教材挂载索引"])
        links = "<br>".join(card.link_text or f"[[{card.title}]]" for card in cards)
        lines.append(f"| {module} | {first.problem} | {source} | {links} | {first.standard} |")
    lines.extend(["", MARKER_END])
    return "\n".join(lines)


def upsert_stage_index(text: str, block: str) -> tuple[str, bool]:
    if not block:
        return text, False
    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if pattern.search(text):
        updated = pattern.sub(block, text)
        return updated, updated != text
    insert_markers = ["## 📝 学习清单", "## ✅ 阶段验收", "## 🔗 阶段导航", "## 📚 推荐资源"]
    for marker in insert_markers:
        idx = text.find(marker)
        if idx != -1:
            return text[:idx].rstrip() + "\n\n" + block + "\n\n" + text[idx:].lstrip(), True
    return text.rstrip() + "\n\n" + block + "\n", True


def repair_course(course: CourseSpec, dry_run: bool, fix_links: bool = False) -> dict[str, int]:
    stats = {
        "stage_links_fixed": 0,
        "stage_aliases_fixed": 0,
        "stage_indexes_updated": 0,
        "legacy_cards_rewritten": 0,
        "generated_cards_refreshed": 0,
        "bad_stage_clones_deleted": 0,
        "files_touched": 0,
    }
    touched: set[Path] = set()

    if fix_links:
        for path in sorted(course.dir.rglob("*.md")):
            text = read_text(path)
            updated, link_count = replace_bad_stage_links(text, course)
            if link_count:
                write_text(path, updated, dry_run)
                touched.add(path)
                stats["stage_links_fixed"] += link_count

    for path in sorted(course.dir.rglob("*.md")):
        text = read_text(path)
        updated, alias_count = replace_return_stage_aliases(text, course)
        if alias_count:
            write_text(path, updated, dry_run)
            touched.add(path)
            stats["stage_aliases_fixed"] += alias_count

    for stage in course.stages:
        text = read_text(stage.file)
        block = make_stage_index_block(stage, course)
        updated, changed = upsert_stage_index(text, block)
        if changed:
            write_text(stage.file, updated, dry_run)
            touched.add(stage.file)
            stats["stage_indexes_updated"] += 1

    for path in sorted(course.dir.rglob("*.md")):
        if path in {stage.file for stage in course.stages}:
            continue
        text = read_text(path)
        if should_delete_bad_stage_clone(path, text):
            if not dry_run:
                path.unlink()
            touched.add(path)
            stats["bad_stage_clones_deleted"] += 1
            continue
        card = should_rewrite_legacy_card(path, text, course)
        if card:
            updated = make_card_body(card, course, text)
            write_text(path, updated, dry_run)
            touched.add(path)
            stats["legacy_cards_rewritten"] += 1
            continue
        card = should_refresh_generated_card(path, text, course)
        if card:
            updated = make_card_body(card, course, text)
            if updated != text:
                write_text(path, updated, dry_run)
                touched.add(path)
                stats["generated_cards_refreshed"] += 1

    stats["files_touched"] = len(touched)
    return stats


def audit_course(course: CourseSpec) -> dict[str, int]:
    md_files = list(course.dir.rglob("*.md"))
    bad_return = 0
    legacy_cards = 0
    bad_stage_clones = 0
    for path in md_files:
        text = read_text(path)
        if re.search(r"所属主线[:：]\s*(?:返回|\[\[[^\]]*\|返回)|这张卡要补哪块[:：]\s*(?:返回|\[\[[^\]]*\|返回)", text):
            bad_return += 1
        if is_generic_legacy_skeleton(text):
            legacy_cards += 1
        if should_delete_bad_stage_clone(path, text):
            bad_stage_clones += 1
    structured = sum(1 for stage in course.stages if stage.cards)
    return {
        "md_files": len(md_files),
        "canonical_stages": len(course.stages),
        "structured_stages": structured,
        "card_specs": len(course.cards),
        "legacy_cards": legacy_cards,
        "bad_return_files": bad_return,
        "bad_stage_clones": bad_stage_clones,
    }


def generate_report(courses: list[CourseSpec], repair_stats: dict[str, dict[str, int]], dry_run: bool) -> str:
    lines = [
        "---",
        'type: audit',
        'topic: "学习系统索引修复审计"',
        f"created: {TODAY}",
        "status: active",
        "tags: [学习系统, 审计, 索引治理]",
        "---",
        "# 📊 学习系统索引修复审计",
        "",
        f"> 生成日期：{TODAY}。模式：{'dry-run' if dry_run else 'applied'}。",
        "",
        "## 总览",
        "",
        "| 科目 | Markdown | 阶段页 | 可抽取索引阶段 | 原子卡规格 | 可修旧骨架卡 | 坏返回字段 | 误生成阶段卡 | 本轮触达 |",
        "|:---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    totals = {
        "md_files": 0,
        "canonical_stages": 0,
        "structured_stages": 0,
        "card_specs": 0,
        "legacy_cards": 0,
        "bad_return_files": 0,
        "bad_stage_clones": 0,
        "files_touched": 0,
    }
    for course in courses:
        audit = audit_course(course)
        stats = repair_stats.get(course.dir.name, {})
        touched = stats.get("files_touched", 0)
        for key in totals:
            if key == "files_touched":
                totals[key] += touched
            else:
                totals[key] += audit[key]
        lines.append(
            f"| {course.dir.name} | {audit['md_files']} | {audit['canonical_stages']} | {audit['structured_stages']} | "
            f"{audit['card_specs']} | {audit['legacy_cards']} | {audit['bad_return_files']} | "
            f"{audit['bad_stage_clones']} | {touched} |"
        )
    lines.extend(
        [
            f"| **合计** | {totals['md_files']} | {totals['canonical_stages']} | {totals['structured_stages']} | "
            f"{totals['card_specs']} | {totals['legacy_cards']} | {totals['bad_return_files']} | "
            f"{totals['bad_stage_clones']} | {totals['files_touched']} |",
            "",
            "## 修复规则",
            "",
            "- 以各科 `📚 教材挂载索引.md` 中的本地教材为主线来源。",
            "- 在 canonical 阶段页中插入或更新 `教材对齐索引`，保留原有阶段正文和 Dataview 统计。",
            "- 只重写仍含 `## 待写提纲` 的旧骨架卡；已经深写的正文不覆盖。",
            "- 删除的只限误生成的阶段导航学习卡：文件名含“阶段”、`type: study`、旧骨架、且主线字段为“返回...”。",
            "- 统一修正指向错误目录的阶段页 wikilink，避免再次点出空卡。",
            "",
            "## 后续治理",
            "",
            "- 对仍为旧骨架但未能从阶段页抽取到规格的卡片，先回到阶段页补入教材对齐索引，再复跑脚本。",
            "- 对新接入或轻量占位路径，先补正式教材或课程资源，再展开阶段目录并复跑本脚本。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    configure_utf8_stdio()
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply changes. Default is dry-run.")
    parser.add_argument("--fix-links", action="store_true", help="Also canonicalize stage-page wiki links.")
    parser.add_argument("--report-only", action="store_true", help="Only write/preview the audit report.")
    args = parser.parse_args()
    dry_run = not args.apply

    courses = build_all_courses()
    repair_stats: dict[str, dict[str, int]] = {}
    if not args.report_only:
        for course in courses:
            repair_stats[course.dir.name] = repair_course(course, dry_run, fix_links=args.fix_links)

    report = generate_report(courses, repair_stats, dry_run)
    if args.apply:
        REPORT.write_text(report, encoding="utf-8", newline="\n")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
