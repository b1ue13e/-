"""Build an actionable repair queue from the latest merciless audit.

This tool never rewrites knowledge notes. It combines audit severity with
resolved inbound wikilinks so the queue favors damaged notes that other notes
actually depend on, rather than blindly expanding thousands of low-value files.
"""

from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT_DIR = ROOT / "99-System" / "🗄️ 归档" / "知识库审计"
DEFAULT_OUTPUT = ROOT / "04-Review" / "知识质量修复队列.md"
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
IGNORED_PARTS = {
    ".git",
    ".obsidian",
    ".recovery-hold",
    ".tmp",
    "__pycache__",
    "🗄️ 归档",
}
IGNORED_PREFIXES = {
    ("00-Inbox", "恢复待确认"),
    ("04-Review", "知识库审计"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="根据极严审计生成知识质量修复队列")
    parser.add_argument("--audit-json", type=Path, help="指定审计 JSON；默认取最新文件")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="输出 Markdown")
    parser.add_argument("--limit", type=int, default=30, help="每个队列最多输出多少条")
    return parser.parse_args()


def newest_audit_json() -> Path:
    candidates = sorted(
        AUDIT_DIR.glob("knowledge_notes_merciless_scores_*.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError(f"没有找到审计 JSON: {AUDIT_DIR}")
    return candidates[0]


def active_markdown() -> list[Path]:
    paths: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        current = Path(dirpath)
        kept_dirs: list[str] = []
        for name in dirnames:
            candidate = current / name
            relative = candidate.relative_to(ROOT).parts
            if name.startswith(".") or name in IGNORED_PARTS:
                continue
            if any(relative[: len(prefix)] == prefix for prefix in IGNORED_PREFIXES):
                continue
            kept_dirs.append(name)
        dirnames[:] = kept_dirs
        for name in filenames:
            path = current / name
            if path.suffix.casefold() == ".md":
                paths.append(path)
    return paths


def without_code_fences(text: str) -> str:
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is None:
            kept.append(line)
    return "\n".join(kept)


def clean_target(raw: str) -> str:
    target = raw.replace("\\|", "|").split("|", 1)[0]
    target = target.split("#", 1)[0].split("^", 1)[0]
    return target.strip().lstrip("/")


def key(path: Path) -> str:
    return path.relative_to(ROOT).as_posix().casefold()


def inbound_counts(markdown: list[Path]) -> Counter[str]:
    by_path = {key(path): path for path in markdown}
    by_stem: dict[str, list[Path]] = defaultdict(list)
    for path in markdown:
        by_stem[path.stem.casefold()].append(path)

    counts: Counter[str] = Counter()
    for source in markdown:
        text = source.read_text(encoding="utf-8-sig", errors="replace")
        source_dir = source.parent.relative_to(ROOT).as_posix()
        for raw in WIKILINK_RE.findall(without_code_fences(text)):
            target = clean_target(raw)
            if not target or "${" in target or "<%" in target:
                continue
            normalized = target.replace("\\", "/")
            variants = [normalized]
            if not Path(normalized).suffix:
                variants.append(f"{normalized}.md")
            resolved: list[Path] = []
            for variant in variants:
                for candidate in (
                    variant.casefold(),
                    posixpath.normpath(posixpath.join(source_dir, variant)).casefold(),
                ):
                    if candidate in by_path:
                        resolved.append(by_path[candidate])
            resolved = list(dict.fromkeys(resolved))
            if not resolved and "/" not in normalized and "\\" not in target:
                name = Path(normalized).stem.casefold()
                candidates = by_stem.get(name, [])
                if len(candidates) == 1:
                    resolved = candidates
            for destination in resolved:
                if destination != source:
                    counts[destination.relative_to(ROOT).as_posix()] += 1
    return counts


def has_flag(note: dict[str, object], fragment: str) -> bool:
    return any(fragment in str(flag) for flag in note.get("flags", []))


def impact(note: dict[str, object]) -> int:
    backlinks = int(note.get("backlinks", 0))
    score = int(note.get("score", 0))
    severity = max(0, 60 - score)
    return backlinks * 12 + severity


def note_link(note: dict[str, object]) -> str:
    path = str(note["path"])
    return f"[[{path[:-3] if path.endswith('.md') else path}|{Path(path).stem}]]"


def issue_summary(note: dict[str, object]) -> str:
    flags = [str(flag) for flag in note.get("flags", [])]
    return "；".join(flags[:3]) if flags else "未记录具体问题"


def table(notes: list[dict[str, object]], limit: int) -> list[str]:
    lines = [
        "| 笔记 | 学科 | 分数 | 入链 | 有效字符 | 主要问题 |",
        "|:--|:--|--:|--:|--:|:--|",
    ]
    for note in notes[:limit]:
        lines.append(
            f"| {note_link(note)} | {note['subject']} | {note['score']} | "
            f"{note['backlinks']} | {note['effective_characters']} | {issue_summary(note)} |"
        )
    if not notes:
        lines.append("| — | — | — | — | — | 当前没有命中项 |")
    return lines


def build_report(data: dict[str, object], audit_path: Path, backlinks: Counter[str], limit: int) -> str:
    notes = [dict(note) for note in data["notes"] if note.get("category") == "知识点"]
    for note in notes:
        note["backlinks"] = backlinks.get(str(note["path"]), 0)
        note["impact"] = impact(note)

    failing = [note for note in notes if int(note["score"]) < 60]
    corruption = [
        note
        for note in failing
        if any(
            has_flag(note, fragment)
            for fragment in ("LaTeX转义", "通用模板", "伪公式", "标题疑似错配", "篇内重复")
        )
    ]
    corruption.sort(key=lambda note: (-int(note["impact"]), int(note["score"]), str(note["path"])))

    high_impact = [note for note in failing if int(note["backlinks"]) > 0]
    high_impact.sort(key=lambda note: (-int(note["impact"]), int(note["score"]), str(note["path"])))

    source_repairs = [
        note
        for note in failing
        if has_flag(note, "无可定位来源") and int(note["effective_characters"]) >= 500
    ]
    source_repairs.sort(key=lambda note: (-int(note["backlinks"]), -int(note["score"]), str(note["path"])))

    retire_review = [
        note
        for note in failing
        if int(note["score"]) <= 20
        and int(note["effective_characters"]) < 200
        and int(note["backlinks"]) == 0
    ]
    retire_review.sort(key=lambda note: (int(note["score"]), str(note["path"])))

    subjects: dict[str, list[int]] = defaultdict(list)
    for note in notes:
        subjects[str(note["subject"])].append(int(note["score"]))
    subject_rows = sorted(
        ((subject, len(scores), sum(scores) / len(scores)) for subject, scores in subjects.items()),
        key=lambda row: (row[2], -row[1], row[0]),
    )

    summary = data["summary"]
    lines = [
        "---",
        'type: "index"',
        'topic: "知识质量修复队列"',
        f"created: {date.today().isoformat()}",
        f"updated: {date.today().isoformat()}",
        'status: "active"',
        'flow: "review"',
        'kind: "moc"',
        "tags: [质量治理, 修复队列, 审计]",
        "---",
        "",
        "# 🧯 知识质量修复队列",
        "",
        "> 本页只决定修复顺序，不自动重写或删除知识卡。优先处理被其他笔记依赖的损坏主卡，低价值空壳先进入退役复核。",
        "",
        "## 当前基线",
        "",
        f"- 知识点：**{summary['knowledge_notes']}** 篇；不合格：**{summary['distribution']['<60']}** 篇。",
        f"- 平均分：**{summary['average']}**；中位数：**{summary['median']}**。",
        f"- 无来源：**{summary['no_sources']}**；模板污染：**{summary['cross_template']}**；占位：**{summary['placeholders']}**。",
        f"- 审计数据：`{audit_path.relative_to(ROOT).as_posix()}`。",
        "",
        "## 固定修复顺序",
        "",
        "1. **P0 结构损坏**：先修控制字符、伪公式、错配和实质重复。",
        "2. **P1 高影响主卡**：按入链数量修复，避免大量下游继续依赖坏卡。",
        "3. **P2 来源补全**：正文已有价值的卡，补教材章节、论文 DOI 或权威文档。",
        "4. **P3 退役复核**：低分、短正文、零入链卡，不扩写；先判断删除、合并或隔离。",
        "",
        "## P0 · 结构与语义损坏",
        "",
        *table(corruption, limit),
        "",
        "## P1 · 高影响主卡",
        "",
        *table(high_impact, limit),
        "",
        "## P2 · 有正文但缺来源",
        "",
        *table(source_repairs, limit),
        "",
        "## P3 · 建议退役复核",
        "",
        *table(retire_review, limit),
        "",
        "## 最低均分学科",
        "",
        "| 学科 | 知识点 | 平均分 |",
        "|:--|--:|--:|",
    ]
    lines.extend(f"| {subject} | {count} | {average:.1f} |" for subject, count, average in subject_rows[:10])
    lines.extend(
        [
            "",
            "## 单卡验收标准",
            "",
            "- 删除与主题无关的通用模板、伪公式和跨学科错配段落。",
            "- 给出定义、成立条件、机制或推导、贴题例子、边界/反例。",
            "- 至少补一个可定位来源；书籍必须到章节，论文优先 DOI，软件优先官方文档。",
            "- 修复断链；只连接真正相关的 canonical 主卡。",
            "- 清除 TODO 后重新运行极严审计，不手填分数。",
            "",
            "## 重建命令",
            "",
            "```powershell",
            "python 99-System/tools/audit_knowledge_notes_merciless.py",
            "python 99-System/tools/build_quality_repair_queue.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    audit_path = (args.audit_json or newest_audit_json()).resolve()
    if not audit_path.is_file():
        print(f"审计 JSON 不存在: {audit_path}", file=sys.stderr)
        return 2
    data = json.loads(audit_path.read_text(encoding="utf-8-sig"))
    markdown = active_markdown()
    backlinks = inbound_counts(markdown)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        build_report(data, audit_path, backlinks, max(args.limit, 1)),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "audit": str(audit_path),
                "output": str(output),
                "active_markdown_scanned": len(markdown),
                "resolved_inbound_targets": len(backlinks),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
