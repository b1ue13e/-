#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 pilot 路径的结构化阶段页里重建/重写“任务型标准卡”。

阶段页要求：
1. frontmatter 里标记 `type: stage`
2. 至少包含一张下列表头的 Markdown 表：
   `模块 | 要解决的问题 | 对应教材章节 | 原子卡片 | 完成标准`
3. `原子卡片` 单元格内使用 wiki link，并按学习顺序排列

脚本行为：
1. 只处理指定课程的 canonical 阶段页。
2. 只创建缺失卡片，或重写明显的旧轻骨架卡片。
3. 不覆盖看起来已经人工深写过的笔记。
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


ROOT = Path("02-Knowledge/🧠 学习系统")
TODAY = date.today().isoformat()

PILOT_COURSES = [
    "07-最优化方法",
    "09-高等代数",
    "17-机器学习",
    "22-概率论与数理统计",
]

STAGE_TABLE_HEADERS = {
    "模块": "module",
    "要解决的问题": "problem",
    "对应教材章节": "sources",
    "原子卡片": "cards",
    "完成标准": "standard",
}

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.S)
TYPE_RE = re.compile(r"(?m)^type:\s*(\S+)\s*$")
PHASE_RE = re.compile(r"(?m)^(?:phase|stage):\s*(\d+)\s*$")


@dataclass
class SourceRef:
    textbook: str
    section: str


@dataclass
class StageRow:
    module: str
    problem: str
    sources: list[SourceRef]
    cards: list[str]
    standard: str


@dataclass
class StageSpec:
    course_dir: Path
    course_name: str
    roadmap_name: str
    stage_file: Path
    stage_heading: str
    phase: int
    total_stages: int
    rows: list[StageRow]


@dataclass
class NoteSpec:
    course_name: str
    roadmap_name: str
    stage_file: Path
    stage_heading: str
    phase: int
    total_stages: int
    title: str
    module: str
    problem: str
    sources: list[SourceRef]
    standard: str
    prerequisites: list[str]
    related: list[str]
    note_type: str


def split_course_name(course_dir_name: str) -> str:
    return course_dir_name.split("-", 1)[1] if "-" in course_dir_name else course_dir_name


def clean_markdown(text: str) -> str:
    text = WIKILINK_RE.sub(lambda m: m.group(2) or Path(m.group(1)).name, text)
    text = text.replace(r"\|", "|")
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = text.replace("**", "").replace("*", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def format_yaml_list(items: Iterable[str]) -> str:
    values = [item for item in items if item]
    if not values:
        return "[]"
    escaped = [value.replace('"', '\\"') for value in values]
    return "[" + ", ".join(f'"{value}"' for value in escaped) + "]"


def split_table_line(raw_line: str) -> list[str]:
    line = raw_line.strip().strip("|")
    cells: list[str] = []
    buf: list[str] = []
    link_depth = 0
    i = 0

    while i < len(line):
        pair = line[i : i + 2]
        if pair == "[[":
            link_depth += 1
            buf.append(pair)
            i += 2
            continue
        if pair == "]]":
            link_depth = max(0, link_depth - 1)
            buf.append(pair)
            i += 2
            continue
        if line[i] == "|" and link_depth == 0:
            cells.append("".join(buf).strip())
            buf = []
            i += 1
            continue
        buf.append(line[i])
        i += 1

    cells.append("".join(buf).strip())
    return cells


def looks_like_separator(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and set(stripped.replace("|", "").replace(":", "").replace("-", "").strip()) == set()


def extract_frontmatter_type(text: str) -> str:
    match = TYPE_RE.search(text)
    return match.group(1).strip() if match else ""


def extract_phase(text: str, fallback: int) -> int:
    match = PHASE_RE.search(text)
    if match:
        return int(match.group(1))
    return fallback


def find_roadmap_name(course_dir: Path) -> str:
    roadmaps = sorted(course_dir.glob("🗺️ *.md"))
    if roadmaps:
        return roadmaps[0].stem
    return f"🗺️ {split_course_name(course_dir.name)}学习路径"


def find_stage_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return clean_markdown(line[2:])
    return fallback


def find_stage_files(course_dir: Path) -> list[Path]:
    stage_files: list[Path] = []
    stage_dirs = sorted([path for path in course_dir.iterdir() if path.is_dir() and re.match(r"^\d{2}-", path.name)])

    for index, stage_dir in enumerate(stage_dirs, start=1):
        candidates = []
        for md_file in sorted(stage_dir.glob("*.md")):
            text = md_file.read_text(encoding="utf-8")
            if extract_frontmatter_type(text) == "stage":
                candidates.append(md_file)
        if not candidates:
            continue
        phase_matches = []
        for candidate in candidates:
            phase = extract_phase(candidate.read_text(encoding="utf-8"), index)
            if phase == index:
                phase_matches.append(candidate)
        stage_files.append(phase_matches[0] if phase_matches else candidates[0])

    return stage_files


def parse_source_refs(raw_cell: str) -> list[SourceRef]:
    normalized = re.sub(r"<br\s*/?>", "\n", raw_cell, flags=re.I)
    parts = [clean_markdown(part) for part in re.split(r"\n|；|;", normalized) if clean_markdown(part)]
    refs: list[SourceRef] = []
    for part in parts:
        if "：" in part:
            textbook, section = part.split("：", 1)
        elif ":" in part:
            textbook, section = part.split(":", 1)
        else:
            textbook, section = part, ""
        refs.append(SourceRef(textbook=textbook.strip(), section=section.strip()))
    return refs


def normalize_note_target(target: str) -> str:
    target = target.strip().rstrip("\\")
    return Path(target).name if "/" in target or "\\" in target else target


def parse_stage_tables(stage_text: str) -> list[StageRow]:
    lines = stage_text.splitlines()
    rows: list[StageRow] = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith("|") or i + 1 >= len(lines):
            i += 1
            continue
        if not looks_like_separator(lines[i + 1]):
            i += 1
            continue

        header_cells = [clean_markdown(cell) for cell in split_table_line(lines[i])]
        header_map: dict[str, int] = {}
        for idx, header in enumerate(header_cells):
            if header in STAGE_TABLE_HEADERS:
                header_map[STAGE_TABLE_HEADERS[header]] = idx

        if set(STAGE_TABLE_HEADERS.values()) - set(header_map.keys()):
            i += 1
            continue

        i += 2
        while i < len(lines) and lines[i].strip().startswith("|"):
            raw_line = lines[i]
            if looks_like_separator(raw_line):
                i += 1
                continue

            raw_cells = split_table_line(raw_line)
            padded = raw_cells + [""] * (len(header_cells) - len(raw_cells))
            module = clean_markdown(padded[header_map["module"]])
            problem = clean_markdown(padded[header_map["problem"]])
            sources = parse_source_refs(padded[header_map["sources"]])
            standard = clean_markdown(padded[header_map["standard"]])
            cards = [
                normalize_note_target(match.group(1))
                for match in WIKILINK_RE.finditer(padded[header_map["cards"]])
            ]

            if module and problem and cards:
                rows.append(
                    StageRow(
                        module=module,
                        problem=problem,
                        sources=sources,
                        cards=cards,
                        standard=standard,
                    )
                )
            i += 1
        continue

    return rows


def build_stage_specs(course_dir: Path) -> list[StageSpec]:
    course_name = split_course_name(course_dir.name)
    roadmap_name = find_roadmap_name(course_dir)
    stage_files = find_stage_files(course_dir)
    total_stages = len(stage_files)
    specs: list[StageSpec] = []

    for default_phase, stage_file in enumerate(stage_files, start=1):
        stage_text = stage_file.read_text(encoding="utf-8")
        rows = parse_stage_tables(stage_text)
        if not rows:
            continue
        specs.append(
            StageSpec(
                course_dir=course_dir,
                course_name=course_name,
                roadmap_name=roadmap_name,
                stage_file=stage_file,
                stage_heading=find_stage_heading(stage_text, stage_file.stem),
                phase=extract_phase(stage_text, default_phase),
                total_stages=total_stages,
                rows=rows,
            )
        )
    return specs


def build_note_specs(stage_spec: StageSpec) -> list[NoteSpec]:
    ordered_cards: list[tuple[str, StageRow]] = []
    for row in stage_spec.rows:
        for card in row.cards:
            ordered_cards.append((card, row))

    specs: list[NoteSpec] = []
    titles = [title for title, _ in ordered_cards]
    for index, (title, row) in enumerate(ordered_cards):
        prev_items = [titles[index - 1]] if index > 0 else []
        next_items = titles[index + 1 : index + 3]
        note_type = "project" if title.startswith("项目-") or "项目" in row.module else "study"
        specs.append(
            NoteSpec(
                course_name=stage_spec.course_name,
                roadmap_name=stage_spec.roadmap_name,
                stage_file=stage_spec.stage_file,
                stage_heading=stage_spec.stage_heading,
                phase=stage_spec.phase,
                total_stages=stage_spec.total_stages,
                title=title,
                module=row.module,
                problem=row.problem,
                sources=row.sources,
                standard=row.standard,
                prerequisites=prev_items,
                related=next_items,
                note_type=note_type,
            )
        )
    return specs


def infer_difficulty(note_type: str, phase: int, total_stages: int) -> str:
    if note_type == "project":
        return "advanced"
    if phase <= max(1, total_stages // 3):
        return "beginner"
    if phase >= max(3, (2 * total_stages + 1) // 3):
        return "advanced"
    return "intermediate"


def render_link_list(items: list[str]) -> str:
    if not items:
        return "无"
    return "、".join(f"[[{item}]]" for item in items)


def render_source_strings(sources: list[SourceRef]) -> tuple[list[str], list[str]]:
    textbooks: list[str] = []
    sections: list[str] = []
    for source in sources:
        if source.textbook and source.textbook not in textbooks:
            textbooks.append(source.textbook)
        section_text = source.section or source.textbook
        if section_text and section_text not in sections:
            sections.append(section_text)
    return textbooks, sections


def render_learning_objectives(spec: NoteSpec) -> list[str]:
    textbooks, sections = render_source_strings(spec.sources)
    chapter_hint = sections[0] if sections else "对应教材章节"
    return [
        f"说明 {spec.title} 在“{spec.module}”里解决的具体问题",
        f"把 {spec.title} 对应回 {chapter_hint}",
        f"用一个最小例子或代表题解释 {spec.title} 的作用",
    ]


def render_deliverables(spec: NoteSpec) -> list[str]:
    items = [
        "一句话定义或项目目标",
        "一个最小例子/代表题/最小实验",
        "一条易错点或跨路径连接",
    ]
    if spec.standard:
        items.append(spec.standard)
    return items


def render_source_block(sources: list[SourceRef]) -> str:
    if not sources:
        return "- 主教材：待补\n- 对应章节：待补"

    textbooks, sections = render_source_strings(sources)
    return (
        f"- 主教材：{'、'.join(f'`{item}`' for item in textbooks)}\n"
        f"- 对应章节：{'；'.join(sections)}"
    )


def render_questions(spec: NoteSpec) -> list[str]:
    return [
        f"{spec.title} 在“{spec.module}”这条主线里具体负责哪一步？",
        f"如果忽略 {spec.title}，{spec.problem} 会在哪一步断掉？",
        f"{spec.title} 和相邻概念的边界是什么？",
    ]


def render_note(spec: NoteSpec) -> str:
    difficulty = infer_difficulty(spec.note_type, spec.phase, spec.total_stages)
    textbooks, sections = render_source_strings(spec.sources)
    learning_objectives = render_learning_objectives(spec)
    deliverables = render_deliverables(spec)
    tags = [spec.course_name, "学习"]
    if spec.note_type == "project":
        tags.append("项目")

    source_sections = sections if sections else ["待补"]
    source_textbooks = textbooks if textbooks else ["待补"]

    lines = [
        "---",
        f"type: {spec.note_type}",
        f'topic: "{spec.title}"',
        f'course: "{spec.course_name}"',
        f'stage: "{spec.stage_heading}"',
        f'module: "{spec.module}"',
        f"created: {TODAY}",
        "status: ongoing",
        f"difficulty: {difficulty}",
        f"concept: {format_yaml_list([spec.title, spec.module])}",
        f"prerequisites: {format_yaml_list(spec.prerequisites)}",
        f"related: {format_yaml_list(spec.related)}",
        f"source_textbook: {format_yaml_list(source_textbooks)}",
        f"source_sections: {format_yaml_list(source_sections)}",
        f"learning_objectives: {format_yaml_list(learning_objectives)}",
        f"deliverables: {format_yaml_list(deliverables)}",
        f"tags: {format_yaml_list(tags)}",
        "---",
        f"# {spec.title}",
        "",
        f"> 所属路径：[[../{spec.roadmap_name}|{spec.course_name}学习路径]]",
        f"> 所属阶段：[[{spec.stage_file.stem}|返回阶段页]]",
        f"> 所属模块：`{spec.module}`",
        "",
        "## 为什么学",
        f"- 这张卡位于“{spec.module}”，用来解决：{spec.problem}",
        f"- 它是你从 {render_link_list(spec.prerequisites)} 走向 {render_link_list(spec.related)} 的桥梁。",
        "",
        "## 教材定位",
        render_source_block(spec.sources),
        f"- 阶段入口：[[{spec.stage_file.stem}|{spec.stage_heading}]]",
        "",
        "## 必须掌握",
        f"- 用自己的话定义 `{spec.title}`，并说清它的边界。",
        f"- 解释 `{spec.title}` 为什么是“{spec.problem}”这条问题链的一部分。",
        f"- 说明它和同阶段相邻概念的区别与联系。",
        "",
        "## 关键问题",
    ]

    for question in render_questions(spec):
        lines.append(f"- {question}")

    lines.extend(
        [
            "",
            "## 最小例子",
            "- 场景：",
            "- 输入：",
            "- 关键一步：",
            "- 结论：",
            "",
            "## 练习与输出",
            "- [ ] 写 3-5 行自己的定义或项目目标。",
            "- [ ] 补一个最小例子、例题、推导片段或实验记录。",
            "- [ ] 记录一个易错点，或补一条跨路径连接。",
            "",
            "## 完成标准",
        ]
    )

    if spec.standard:
        lines.append(f"- [ ] {spec.standard}")
    lines.extend(
        [
            "- [ ] 能独立解释这张卡在本阶段中的位置。",
            "- [ ] 能把教材章节和这张卡一一对应。",
            "",
            "## 前后连接",
            f"- 前置：{render_link_list(spec.prerequisites)}",
            f"- 相关：{render_link_list(spec.related)}",
            f"- 返回阶段页：[[{spec.stage_file.stem}|{spec.stage_heading}]]",
            "",
            f"*创建于：{TODAY}*",
            "",
        ]
    )
    return "\n".join(lines)


def is_lightweight_note(text: str) -> bool:
    markers = (
        "## 待写提纲",
        "## 待写",
        "## 学习定位",
        "## 一句话定义",
        "## 最小自测",
        "## 项目定位",
        "## 对应教材",
        "## 最小交付",
        "## 实施步骤",
        "## 复盘问题",
    )
    has_new_frontmatter = all(
        field in text
        for field in (
            "course:",
            "stage:",
            "module:",
            "source_textbook:",
            "source_sections:",
            "learning_objectives:",
            "deliverables:",
        )
    )
    return (not has_new_frontmatter) and any(marker in text for marker in markers)


def write_notes(specs: list[NoteSpec], dry_run: bool, rewrite_lightweight: bool) -> tuple[int, int, int]:
    created = 0
    rewritten = 0
    skipped = 0

    for spec in specs:
        note_path = spec.stage_file.parent / f"{spec.title}.md"
        new_text = render_note(spec)

        if note_path.exists():
            existing = note_path.read_text(encoding="utf-8")
            if rewrite_lightweight and is_lightweight_note(existing):
                if not dry_run:
                    note_path.write_text(new_text, encoding="utf-8")
                rewritten += 1
            else:
                skipped += 1
            continue

        if not dry_run:
            note_path.write_text(new_text, encoding="utf-8")
        created += 1

    return created, rewritten, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="按结构化阶段表生成/重写任务型原子卡。")
    parser.add_argument("--dry-run", action="store_true", help="只统计，不写入文件。")
    parser.add_argument(
        "--courses",
        nargs="*",
        default=PILOT_COURSES,
        help="要处理的课程目录名，默认是四条 pilot 路径。",
    )
    parser.add_argument(
        "--rewrite-lightweight",
        action="store_true",
        help="重写旧的轻骨架笔记（待写/旧模板/自动生成卡）。",
    )
    args = parser.parse_args()

    total_created = 0
    total_rewritten = 0
    total_skipped = 0

    for course_name in args.courses:
        course_dir = ROOT / course_name
        if not course_dir.exists():
            print(f"[skip] {course_name}: 路径不存在")
            continue

        stage_specs = build_stage_specs(course_dir)
        note_specs: list[NoteSpec] = []
        for stage_spec in stage_specs:
            note_specs.extend(build_note_specs(stage_spec))

        created, rewritten, skipped = write_notes(
            note_specs,
            dry_run=args.dry_run,
            rewrite_lightweight=args.rewrite_lightweight,
        )
        total_created += created
        total_rewritten += rewritten
        total_skipped += skipped
        print(
            f"{course_name}: stage_pages={len(stage_specs)}, "
            f"note_specs={len(note_specs)}, create={created}, "
            f"rewrite_lightweight={rewritten}, skip_existing={skipped}"
        )

    mode = "DRY-RUN" if args.dry_run else "DONE"
    print(
        f"{mode}: create={total_created}, "
        f"rewrite_lightweight={total_rewritten}, skip_existing={total_skipped}"
    )


if __name__ == "__main__":
    main()
