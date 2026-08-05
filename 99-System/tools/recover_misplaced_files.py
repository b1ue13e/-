#!/usr/bin/env python3
"""Restore flattened vault files using recovery metadata and frontmatter.

The recovery source is never modified. Existing destination files are copied to
the run backup before replacement, and every operation is written to JSON.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import defaultdict
from datetime import datetime
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SYSTEM = ROOT / "02-Knowledge" / "🧠 学习系统"
HISTORY_SYSTEM = ROOT / ".recovery-hold" / "02-Knowledge" / "🧠 学习系统"
FLAT_PROJECT_DIR = ROOT / "03-Projects" / "李宏毅机器学习实战作业"
RUN_ID = "2026-07-31-location-restore"
BACKUP = ROOT / ".recovery-hold" / RUN_ID
LOG_PATH = ROOT / "99-System" / "🗄️ 归档" / "迁移日志" / f"{RUN_ID}.json"

COURSE_ALIASES = {
    "时间序列分析": "02-时间序列分析",
    "量化金融": "03-量化金融",
    "“量化金融”": "03-量化金融",
    "03-量化金融": "03-量化金融",
    "机器学习": "17-机器学习",
    "17-机器学习": "17-机器学习",
    "05-计算机视觉": "05-计算机视觉",
    "08-NLP全栈": "08-NLP全栈",
    "13-强化学习": "13-强化学习",
    "30-应用回归分析": "30-应用回归分析",
}

ALREADY_RESTORED = {
    "18-题库学习",
    "19-习惯追踪",
    "20-PARA知识管理",
    "21-周期笔记",
    "23-图神经网络",
    "27-泛函分析",
    "29-运筹学",
    "31-属性数据分析",
    "32-非参数统计",
    "34-偏微分方程",
    "35-数值分析",
    "37-复变函数",
}


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    if not text.startswith("---"):
        return {}
    match = re.match(r"^---\s*\n(.*?)\n---", text, flags=re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        field = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if field:
            result[field.group(1)] = field.group(2).strip(" \"'[]")
    return result


def normalize_course(value: str) -> str | None:
    if not value:
        return None
    if value in COURSE_ALIASES:
        return COURSE_ALIASES[value]
    for alias, course in COURSE_ALIASES.items():
        if alias in value:
            return course
    match = re.search(r"(\d{2}-[^/]+)", value)
    return match.group(1) if match else None


@lru_cache(maxsize=None)
def file_index(directory: Path) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = defaultdict(list)
    if directory.exists():
        for path in directory.rglob("*.md"):
            index[path.name].append(path)
    return index


def backup_path(path: Path, category: str) -> Path:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        relative = Path(path.name)
    return BACKUP / category / relative


def copy_backup(path: Path, category: str, dry_run: bool) -> Path:
    destination = backup_path(path, category)
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    return destination


def move_with_backup(
    source: Path,
    destination: Path,
    log: list[dict[str, str]],
    dry_run: bool,
) -> None:
    if source.resolve() == destination.resolve():
        return
    source_backup = copy_backup(source, "sources", dry_run)
    replaced_backup = None
    if destination.exists():
        replaced_backup = copy_backup(destination, "replaced-targets", dry_run)
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
    log.append(
        {
            "action": "move",
            "source": str(source.relative_to(ROOT)),
            "destination": str(destination.relative_to(ROOT)),
            "source_backup": str(source_backup.relative_to(ROOT)),
            "replaced_backup": (
                str(replaced_backup.relative_to(ROOT)) if replaced_backup else ""
            ),
        }
    )


def restore_unique_knowledge_paths(
    log: list[dict[str, str]], dry_run: bool
) -> list[dict[str, str]]:
    ambiguous: list[dict[str, str]] = []
    for course_dir in sorted(path for path in SYSTEM.iterdir() if path.is_dir()):
        if course_dir.name in ALREADY_RESTORED:
            continue
        history_dir = HISTORY_SYSTEM / course_dir.name
        if not history_dir.exists():
            continue
        history_index = file_index(history_dir)
        for current in sorted(course_dir.glob("*.md")):
            candidates = history_index.get(current.name, [])
            if len(candidates) > 1:
                ambiguous.append(
                    {
                        "file": str(current.relative_to(ROOT)),
                        "candidates": [str(item.relative_to(ROOT)) for item in candidates],
                    }
                )
                continue
            if len(candidates) != 1:
                continue
            relative = candidates[0].relative_to(history_dir)
            if relative.parent == Path("."):
                continue
            move_with_backup(current, course_dir / relative, log, dry_run)
    return ambiguous


def historical_destination(path: Path, course: str | None) -> Path | None:
    if course:
        history_dir = HISTORY_SYSTEM / course
        candidates = file_index(history_dir).get(path.name, [])
        if len(candidates) == 1:
            return SYSTEM / course / candidates[0].relative_to(history_dir)

    candidates = file_index(HISTORY_SYSTEM).get(path.name, [])
    if len(candidates) != 1:
        return None
    return SYSTEM / candidates[0].relative_to(HISTORY_SYSTEM)


def route_flat_project_file(path: Path) -> Path:
    metadata = read_frontmatter(path)
    note_type = metadata.get("type", "")
    kind = metadata.get("kind", "")
    course = normalize_course(metadata.get("course", ""))

    if path.name == "AGENTS.md.md":
        return ROOT / "AGENTS.md"
    if path.name == "🏠 个人知识系统主页.md":
        return ROOT / "🏠 主页.md"
    if path.name == "🚀 Active Sprint.md":
        return ROOT / "01-Active Sprint" / path.name
    if path.name == "33 门课程开源自学与验收总索引.md":
        return ROOT / "02-Knowledge" / "MOC" / "33门课程开源自学与验收总索引.md"
    if kind == "audit" or "审计-2026" in path.name or "挂载建议-2026" in path.name:
        return ROOT / "04-Review" / path.name
    if path.name.startswith("recovered_"):
        return ROOT / "00-Inbox" / "恢复待确认" / "量化金融" / path.name
    if path.name.startswith("HW17：Qlib"):
        return ROOT / "03-Projects" / "金融与时序" / "03-量化金融" / path.name

    historical = historical_destination(path, course)
    if historical:
        return historical

    if note_type == "homework" and course:
        return SYSTEM / course / "18-实战作业说明书" / path.name
    if note_type == "problem-type" and course:
        problem_dir = SYSTEM / course / "30-题型笔记"
        return problem_dir / path.name
    if course:
        return SYSTEM / course / path.name
    if note_type in {"index", "MOC", "stage", "study", "concept"}:
        return ROOT / "00-Inbox" / "恢复待确认" / "未识别课程" / path.name
    return ROOT / "00-Inbox" / "恢复待确认" / "未分类" / path.name


def restore_flat_project_directory(
    log: list[dict[str, str]], dry_run: bool
) -> None:
    if not FLAT_PROJECT_DIR.exists():
        return
    for path in sorted(FLAT_PROJECT_DIR.glob("*.md")):
        move_with_backup(path, route_flat_project_file(path), log, dry_run)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="perform file moves")
    args = parser.parse_args()
    dry_run = not args.apply

    log: list[dict[str, str]] = []
    ambiguous = restore_unique_knowledge_paths(log, dry_run)
    restore_flat_project_directory(log, dry_run)
    report = {
        "run_id": RUN_ID,
        "mode": "dry-run" if dry_run else "apply",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "operation_count": len(log),
        "ambiguous_count": len(ambiguous),
        "operations": log,
        "ambiguous": ambiguous,
    }
    if not dry_run:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        LOG_PATH.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps({key: report[key] for key in report if key != "operations" and key != "ambiguous"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
