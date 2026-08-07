from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = REPO_ROOT / "02-Knowledge" / "🧠 学习系统" / "02-时间序列分析"
PROJECT_ROOT = REPO_ROOT / "03-Projects" / "02-时间序列分析"
EXCLUDED_PARTS = {".git", ".tmp", ".reasonix", ".recovery-hold"}
STUDY_FIELDS = {"type", "topic", "course", "created", "status", "stage_moc", "flow", "kind"}
ASSIGNMENT_FIELDS = {
    "type",
    "project_type",
    "course",
    "assignment_id",
    "assignment_level",
    "assignment_format",
    "stage_id",
    "requires",
    "source_type",
    "created",
    "status",
    "flow",
}


def split_frontmatter(text: str) -> tuple[str, str] | None:
    match = re.match(r"\ufeff?---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    return match.groups() if match else None


def scalar_fields(frontmatter: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if match:
            fields[match.group(1)] = (match.group(2) or "").strip().strip('"').strip("'")
    return fields


def without_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def wikilinks(text: str) -> list[str]:
    return re.findall(r"\[\[([^\]|]+)", without_code(text))


def markdown_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*.md") if not EXCLUDED_PARTS.intersection(path.parts)]


def main() -> int:
    errors: list[str] = []
    course_files = markdown_files(COURSE_ROOT)
    project_files = markdown_files(PROJECT_ROOT)
    repository_files = markdown_files(REPO_ROOT)
    basenames = {path.stem for path in repository_files}

    stages = {path.stem for path in course_files if path.name.startswith("🧭 阶段")}
    study_count = 0
    for path in course_files:
        text = path.read_text(encoding="utf-8-sig")
        parts = split_frontmatter(text)
        if parts is None:
            errors.append(f"NO_FRONTMATTER {path.relative_to(REPO_ROOT)}")
            continue
        frontmatter, body = parts
        fields = scalar_fields(frontmatter)
        if fields.get("type") == "study":
            study_count += 1
            missing = STUDY_FIELDS - fields.keys()
            if missing:
                errors.append(f"STUDY_FIELDS {path.relative_to(REPO_ROOT)} {sorted(missing)}")
            if fields.get("course") != "时间序列分析":
                errors.append(f"STUDY_COURSE {path.relative_to(REPO_ROOT)} {fields.get('course')}")
            stage_match = re.search(r"\[\[([^\]|]+)", fields.get("stage_moc", ""))
            if not stage_match or stage_match.group(1).split("/")[-1] not in stages:
                errors.append(f"STAGE_MOC {path.relative_to(REPO_ROOT)} {fields.get('stage_moc')}")
            if "downstream" in fields:
                errors.append(f"STATIC_DOWNSTREAM {path.relative_to(REPO_ROOT)}")
            if "WHERE contains(upstream, this.file.link)" not in body:
                errors.append(f"NO_DOWNSTREAM_VIEW {path.relative_to(REPO_ROOT)}")
            if "WHERE contains(requires, this.file.link)" not in body:
                errors.append(f"NO_ASSIGNMENT_VIEW {path.relative_to(REPO_ROOT)}")
            if not any(key in fields for key in ("source", "sources", "source_url")):
                errors.append(f"NO_SOURCE {path.relative_to(REPO_ROOT)}")

    assignment_count = 0
    assignment_ids: set[str] = set()
    for path in project_files:
        text = path.read_text(encoding="utf-8-sig")
        parts = split_frontmatter(text)
        if parts is None:
            errors.append(f"NO_FRONTMATTER {path.relative_to(REPO_ROOT)}")
            continue
        frontmatter, _ = parts
        fields = scalar_fields(frontmatter)
        if fields.get("type") != "project":
            continue
        assignment_count += 1
        missing = ASSIGNMENT_FIELDS - fields.keys()
        if missing:
            errors.append(f"ASSIGNMENT_FIELDS {path.relative_to(REPO_ROOT)} {sorted(missing)}")
        if fields.get("assignment_level") not in {"lesson", "stage", "capstone"}:
            errors.append(f"ASSIGNMENT_LEVEL {path.relative_to(REPO_ROOT)} {fields.get('assignment_level')}")
        assignment_id = fields.get("assignment_id", "")
        if assignment_id in assignment_ids:
            errors.append(f"DUPLICATE_ASSIGNMENT_ID {assignment_id}")
        assignment_ids.add(assignment_id)
        for target in wikilinks(fields.get("requires", "")):
            if target.split("/")[-1] not in basenames:
                errors.append(f"REQUIRES {path.relative_to(REPO_ROOT)} {target}")
        if any(label in path.name for label in ("李宏毅式", "4-Tier", "Boss", "阶梯作业")):
            errors.append(f"LEGACY_ASSIGNMENT_NAME {path.relative_to(REPO_ROOT)}")

    for path in course_files + project_files:
        text = path.read_text(encoding="utf-8-sig")
        for target in wikilinks(text):
            target = target.split("#", 1)[0].strip().strip('"')
            if target and target.split("/")[-1].removesuffix(".md") not in basenames:
                errors.append(f"WIKILINK {path.relative_to(REPO_ROOT)} {target}")

    old_active = [
        REPO_ROOT / "03-Projects" / "金融与时序" / "02-时间序列分析",
        REPO_ROOT / "03-Projects" / "课程作业" / "02-时间序列分析",
    ]
    for directory in old_active:
        if directory.exists() and any(directory.glob("*.md")):
            errors.append(f"SECOND_ASSIGNMENT_SOURCE {directory.relative_to(REPO_ROOT)}")

    print(f"study_cards={study_count}")
    print(f"assignments={assignment_count}")
    print(f"errors={len(errors)}")
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
