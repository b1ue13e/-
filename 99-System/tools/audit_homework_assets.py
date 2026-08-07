"""Audit whether legacy project/homework notes qualify as executable assignments.

This audit does not delete or rewrite learning notes. It only applies the
eligibility gate defined by the 33-course homework governance project.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
STUDY_ROOT = ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统"
FORMAL_PROJECT_ROOT = ROOT / "03-Projects" / "课程作业"
COURSE_PATTERN = re.compile(r"^(?:0[1-9]|1[0-7]|2[2-9]|3[0-7])-")
NON_FORMAL_DIRS = {"04-前沿架构探索", "05-专业深化与工程落地"}
HW_PATTERN = re.compile(r"^HW\d+", re.I)
REQUIRED_FIELDS = (
    "source_url",
    "source_course",
    "source_version",
    "license",
    "adaptation",
    "dataset_version",
    "starter_code",
    "tests",
    "baseline",
    "acceptance_test",
    "compute_budget",
    "solution_visibility",
)
ALLOWED_SOLUTION_VISIBILITY = {"private", "summary-only"}


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) != 3:
        return {}
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def is_candidate(path: Path, data: dict, course_dir: Path) -> bool:
    relative = path.relative_to(course_dir)
    return any(
        (
            path.stem.startswith("项目-"),
            HW_PATTERN.match(path.stem) is not None,
            any("项目" in part for part in relative.parts[:-1]),
            data.get("project_type") == "homework",
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--details",
        action="store_true",
        help="print each ineligible file and its missing fields",
    )
    args = parser.parse_args()

    totals = Counter()
    detail_rows: list[tuple[str, Path, list[str]]] = []

    for course_dir in sorted(STUDY_ROOT.iterdir()):
        if (
            not course_dir.is_dir()
            or not COURSE_PATTERN.match(course_dir.name)
            or course_dir.name in NON_FORMAL_DIRS
        ):
            continue
        course = Counter()
        roots = [course_dir]
        formal_dir = FORMAL_PROJECT_ROOT / course_dir.name
        if formal_dir.exists():
            roots.append(formal_dir)
        paths = [path for root in roots for path in root.rglob("*.md")]
        for path in paths:
            data = parse_frontmatter(path)
            candidate_root = formal_dir if formal_dir in path.parents else course_dir
            if not is_candidate(path, data, candidate_root):
                continue
            course["candidate"] += 1
            missing = [
                field
                for field in REQUIRED_FIELDS
                if field not in data or data.get(field) in (None, "")
            ]
            visibility = data.get("solution_visibility")
            if visibility and visibility not in ALLOWED_SOLUTION_VISIBILITY:
                missing.append("solution_visibility:private|summary-only")
            if missing:
                course["ineligible"] += 1
                if data.get("asset_eligibility") != "reference-only":
                    course["unmarked"] += 1
                detail_rows.append((course_dir.name, path, missing))
            else:
                course["eligible"] += 1
                if data.get("asset_eligibility") != "eligible":
                    course["unmarked"] += 1
        if course["candidate"]:
            totals.update(course)
            print(
                f"{course_dir.name}\t候选={course['candidate']}\t"
                f"合格={course['eligible']}\t隔离={course['ineligible']}\t"
                f"未标记={course['unmarked']}"
            )

    print(
        f"TOTAL\t候选={totals['candidate']}\t"
        f"合格={totals['eligible']}\t隔离={totals['ineligible']}\t"
        f"未标记={totals['unmarked']}"
    )
    print(
        "RULE\t缺少任一资格字段的旧项目仅作 reference，"
        "不得进入 Active Sprint、作业清单或评分。"
    )
    if args.details:
        for course, path, missing in detail_rows:
            relative = path.relative_to(ROOT).as_posix()
            print(f"INELIGIBLE\t{course}\t{relative}\t缺少={','.join(missing)}")
    if totals["unmarked"]:
        print("ERROR\t存在未写入 asset_eligibility: reference-only 的不合格资产")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
