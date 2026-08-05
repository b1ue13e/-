#!/usr/bin/env python3
"""Restore project cards that an earlier migration put under 通用项目."""

from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / ".recovery-hold" / "03-Projects" / "通用项目"
PROJECTS = ROOT / "03-Projects"
RUN_ID = "2026-07-31-generic-project-restore"
BACKUP = ROOT / ".recovery-hold" / RUN_ID / "replaced-targets"
LOG_PATH = ROOT / "99-System" / "🗄️ 归档" / "迁移日志" / f"{RUN_ID}.json"

COURSE_TO_TRACK = {
    "01-社交网络挖掘": "机器学习与AI应用",
    "02-时间序列分析": "金融与时序",
    "03-量化金融": "金融与时序",
    "04-离散数学": "数学底座",
    "05-计算机视觉": "机器学习与AI应用",
    "06-常微分方程": "数学底座",
    "07-最优化方法": "金融与时序",
    "08-NLP全栈": "机器学习与AI应用",
    "11-计算机组成原理": "系统与硬件",
    "12-信号与系统": "系统与硬件",
    "13-强化学习": "机器学习与AI应用",
    "14-概率图模型": "机器学习与AI应用",
    "15-控制与机器人学": "系统与硬件",
}

MANUAL_COURSES = {
    "项目-Breakout.md": "13-强化学习",
    "项目-CartPoleDQN.md": "13-强化学习",
    "项目-悬崖对比.md": "13-强化学习",
    "项目-迷宫QL.md": "13-强化学习",
    "项目-CIFAR10.md": "05-计算机视觉",
    "项目-CNN可视化.md": "05-计算机视觉",
    "项目-风格迁移.md": "05-计算机视觉",
    "项目-信号分解.md": "12-信号与系统",
    "项目-信号绘制.md": "12-信号与系统",
    "项目-性质判断.md": "04-离散数学",
    "项目-文本统计.md": "08-NLP全栈",
    "项目-正则提取.md": "08-NLP全栈",
    "项目-简单搜索.md": "08-NLP全栈",
}


def load_core_tracks() -> dict[str, str]:
    candidates = [
        ROOT / "update_46_projects.py",
        ROOT / "99-System" / "tools" / "update_46_projects.py",
    ]
    for script in candidates:
        if not script.exists():
            continue
        tree = ast.parse(script.read_text(encoding="utf-8-sig"))
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if not any(
                isinstance(target, ast.Name) and target.id == "CORE_46_PROJECTS"
                for target in node.targets
            ):
                continue
            paths = ast.literal_eval(node.value)
            return {Path(value).name: Path(value).parts[1] for value in paths}
    raise FileNotFoundError("Could not locate CORE_46_PROJECTS")


def infer_course(text: str, name: str) -> str | None:
    match = re.search(
        r"(?:02-Knowledge/)?🧠 学习系统[/\\](\d{2}-[^/\\|\]\r\n]+)",
        text,
    )
    if match:
        return match.group(1).strip()
    return MANUAL_COURSES.get(name)


def repair_frontmatter(text: str, track: str, course: str) -> str:
    if text.startswith("---type:"):
        text = "---\n" + text[3:]
    if not text.startswith("---\n"):
        text = "---\ntype: project\n---\n" + text

    closing = text.find("\n---", 4)
    if closing < 0:
        return text
    head = text[4:closing]
    body = text[closing + 4 :]

    def set_field(block: str, field: str, value: str) -> str:
        pattern = rf"(?m)^{re.escape(field)}:\s*.*$"
        replacement = f'{field}: "{value}"'
        if re.search(pattern, block):
            return re.sub(pattern, replacement, block)
        return block.rstrip() + "\n" + replacement

    head = set_field(head, "type", "project")
    head = set_field(head, "flow", "project")
    head = set_field(head, "kind", "project")
    head = set_field(head, "track", track)
    head = set_field(head, "course", course)
    return f"---\n{head.strip()}\n---\n{body.lstrip()}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    dry_run = not args.apply
    core_tracks = load_core_tracks()

    operations: list[dict[str, str]] = []
    unresolved: list[str] = []
    distribution: Counter[str] = Counter()

    for source in sorted(SOURCE.rglob("*.md")):
        text = source.read_text(encoding="utf-8-sig", errors="replace")
        if source.name in core_tracks:
            track = core_tracks[source.name]
            course = "通用与跨学科"
            destination = PROJECTS / track / source.name
        else:
            course = infer_course(text, source.name)
            if not course or course not in COURSE_TO_TRACK:
                unresolved.append(str(source.relative_to(ROOT)))
                continue
            track = COURSE_TO_TRACK[course]
            destination = PROJECTS / track / course / source.name

        distribution[f"{track}/{course}"] += 1
        replaced_backup = ""
        if destination.exists():
            backup = BACKUP / destination.relative_to(ROOT)
            replaced_backup = str(backup.relative_to(ROOT))
            if not dry_run:
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(destination, backup)

        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                repair_frontmatter(text, track, course), encoding="utf-8", newline="\n"
            )

        operations.append(
            {
                "action": "restore-copy",
                "source": str(source.relative_to(ROOT)),
                "destination": str(destination.relative_to(ROOT)),
                "replaced_backup": replaced_backup,
            }
        )

    report = {
        "run_id": RUN_ID,
        "mode": "dry-run" if dry_run else "apply",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "operation_count": len(operations),
        "unresolved_count": len(unresolved),
        "replacement_count": sum(bool(item["replaced_backup"]) for item in operations),
        "distribution": dict(distribution),
        "operations": operations,
        "unresolved": unresolved,
    }
    if not dry_run:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        LOG_PATH.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(
        json.dumps(
            {key: value for key, value in report.items() if key not in {"operations"}},
            ensure_ascii=False,
        )
    )
    return 0 if not unresolved else 2


if __name__ == "__main__":
    raise SystemExit(main())
