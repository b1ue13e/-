from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = REPO_ROOT / "02-Knowledge" / "🧠 学习系统" / "02-时间序列分析"
PROJECT_ROOT = REPO_ROOT / "03-Projects" / "02-时间序列分析"
EXCLUDED_PARTS = {".git", ".tmp", ".reasonix", ".recovery-hold", ".归档"}
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
ASSIGNMENT_CONTRACT = {
    "LEARNING_GOAL": r"(?m)^## 学习目标",
    "DETAILED_TASK": r"(?m)^## (?:详细任务|任务|里程碑)",
    "DELIVERABLES": r"(?m)^## 提交产物",
    "RUBRIC": r"(?m)^## .*?(?:Rubric|验收)",
    "GUIDANCE": r"(?m)^## .*?(?:引导|提示|自检)",
}


def split_frontmatter(text: str) -> tuple[dict[str, object], str] | None:
    match = re.match(r"\ufeff?---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if match is None:
        return None
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        return None
    return data, match.group(2)


def without_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def wikilinks(text: str) -> list[str]:
    return re.findall(r"\[\[([^\]|]+)", without_code(text))


def clean_target(target: str) -> str:
    return target.split("#", 1)[0].strip().strip('"').rstrip("\\").removesuffix(".md").replace("\\", "/")


def markdown_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*.md") if not EXCLUDED_PARTS.intersection(path.parts)]


def target_candidates(target: str, files: list[Path], by_stem: dict[str, list[Path]]) -> list[Path]:
    cleaned = clean_target(target)
    if not cleaned:
        return []
    if "/" not in cleaned:
        return by_stem.get(cleaned, [])
    normalized = cleaned.lstrip("/")
    matches: list[Path] = []
    for path in files:
        relative = path.relative_to(REPO_ROOT).with_suffix("").as_posix()
        if relative == normalized or relative.endswith("/" + normalized):
            matches.append(path)
    return matches


def main() -> int:
    errors: list[str] = []
    course_files = markdown_files(COURSE_ROOT)
    project_files = markdown_files(PROJECT_ROOT)
    repository_files = markdown_files(REPO_ROOT)
    by_stem: dict[str, list[Path]] = defaultdict(list)
    for path in repository_files:
        by_stem[path.stem].append(path)

    documents: dict[Path, tuple[dict[str, object], str]] = {}
    for path in course_files + project_files:
        parsed = split_frontmatter(path.read_text(encoding="utf-8-sig"))
        if parsed is None:
            errors.append(f"NO_FRONTMATTER {path.relative_to(REPO_ROOT)}")
            continue
        documents[path] = parsed

    stage_documents = {
        path: (data, body)
        for path, (data, body) in documents.items()
        if path.is_relative_to(COURSE_ROOT) and data.get("type") == "index" and data.get("stage_id") is not None
    }
    stage_paths = set(stage_documents)
    study_documents = {
        path: (data, body)
        for path, (data, body) in documents.items()
        if path.is_relative_to(COURSE_ROOT) and data.get("type") == "study"
    }
    study_paths = set(study_documents)

    for path, (data, body) in study_documents.items():
        missing = STUDY_FIELDS - data.keys()
        if missing:
            errors.append(f"STUDY_FIELDS {path.relative_to(REPO_ROOT)} {sorted(missing)}")
        if data.get("course") != "时间序列分析":
            errors.append(f"STUDY_COURSE {path.relative_to(REPO_ROOT)} {data.get('course')}")

        stage_links = wikilinks(str(data.get("stage_moc", "")))
        stage_candidates = target_candidates(stage_links[0], repository_files, by_stem) if len(stage_links) == 1 else []
        if len(stage_candidates) != 1 or stage_candidates[0] not in stage_paths:
            errors.append(f"STAGE_MOC {path.relative_to(REPO_ROOT)} {data.get('stage_moc')}")
        else:
            moc_body = stage_documents[stage_candidates[0]][1]
            listed = {clean_target(target).split("/")[-1] for target in wikilinks(moc_body)}
            if path.stem not in listed:
                errors.append(f"NOT_IN_STAGE_MOC {path.relative_to(REPO_ROOT)} {stage_candidates[0].relative_to(REPO_ROOT)}")

        if "upstream" in data:
            upstream = data["upstream"]
            if not isinstance(upstream, list) or not upstream:
                errors.append(f"UPSTREAM_SHAPE {path.relative_to(REPO_ROOT)} {upstream!r}")
            else:
                for raw in upstream:
                    links = wikilinks(str(raw))
                    candidates = target_candidates(links[0], repository_files, by_stem) if len(links) == 1 else []
                    if len(candidates) != 1 or candidates[0] not in study_paths:
                        errors.append(f"UPSTREAM_TARGET {path.relative_to(REPO_ROOT)} {raw}")
                    elif candidates[0] == path:
                        errors.append(f"SELF_UPSTREAM {path.relative_to(REPO_ROOT)}")

        if "downstream" in data:
            errors.append(f"STATIC_DOWNSTREAM {path.relative_to(REPO_ROOT)}")
        if "## 学完后可以完成" not in body:
            errors.append(f"NO_ASSESSMENT_SECTION {path.relative_to(REPO_ROOT)}")
        if "WHERE contains(upstream, this.file.link)" not in body:
            errors.append(f"NO_DOWNSTREAM_VIEW {path.relative_to(REPO_ROOT)}")
        if "WHERE contains(requires, this.file.link)" not in body:
            errors.append(f"NO_ASSIGNMENT_VIEW {path.relative_to(REPO_ROOT)}")
        if not any(key in data for key in ("source", "sources", "source_url")):
            errors.append(f"NO_SOURCE {path.relative_to(REPO_ROOT)}")
        for key in ("source", "source_url", "license"):
            if data.get(key) == "[待验证]":
                errors.append(f"UNRESOLVED_SOURCE {path.relative_to(REPO_ROOT)} {key}")

    assignment_count = 0
    assignment_ids: set[str] = set()
    for path, (data, body) in documents.items():
        if not path.is_relative_to(PROJECT_ROOT) or data.get("type") != "project":
            continue
        assignment_count += 1
        missing = ASSIGNMENT_FIELDS - data.keys()
        if missing:
            errors.append(f"ASSIGNMENT_FIELDS {path.relative_to(REPO_ROOT)} {sorted(missing)}")
        if data.get("assignment_level") not in {"lesson", "stage", "capstone"}:
            errors.append(f"ASSIGNMENT_LEVEL {path.relative_to(REPO_ROOT)} {data.get('assignment_level')}")
        assignment_id = str(data.get("assignment_id", ""))
        if assignment_id in assignment_ids:
            errors.append(f"DUPLICATE_ASSIGNMENT_ID {assignment_id}")
        assignment_ids.add(assignment_id)

        requires = data.get("requires")
        if not isinstance(requires, list) or not requires:
            errors.append(f"REQUIRES_SHAPE {path.relative_to(REPO_ROOT)} {requires!r}")
        else:
            for raw in requires:
                links = wikilinks(str(raw))
                candidates = target_candidates(links[0], repository_files, by_stem) if len(links) == 1 else []
                if len(candidates) != 1 or candidates[0] not in study_paths:
                    errors.append(f"REQUIRES {path.relative_to(REPO_ROOT)} {raw}")

        for label, pattern in ASSIGNMENT_CONTRACT.items():
            if re.search(pattern, body) is None:
                errors.append(f"ASSIGNMENT_{label} {path.relative_to(REPO_ROOT)}")
        if len(body) < 900:
            errors.append(f"ASSIGNMENT_TOO_SHORT {path.relative_to(REPO_ROOT)} {len(body)}")
        if re.search(r"\bHW\d{2}\b", without_code(body)):
            errors.append(f"LEGACY_HW_REFERENCE {path.relative_to(REPO_ROOT)}")
        if any(label in path.name for label in ("李宏毅式", "4-Tier", "Boss", "阶梯作业")):
            errors.append(f"LEGACY_ASSIGNMENT_NAME {path.relative_to(REPO_ROOT)}")

    for path, (_, body) in documents.items():
        text = path.read_text(encoding="utf-8-sig")
        for target in wikilinks(text):
            candidates = target_candidates(target, repository_files, by_stem)
            if not candidates:
                errors.append(f"WIKILINK {path.relative_to(REPO_ROOT)} {target}")
            elif "/" not in clean_target(target) and len(candidates) > 1:
                errors.append(f"AMBIGUOUS_WIKILINK {path.relative_to(REPO_ROOT)} {target} {len(candidates)}")

    for path, (data, body) in stage_documents.items():
        stage_id = str(data["stage_id"])
        if f'WHERE stage_id = "{stage_id}"' not in body:
            errors.append(f"STAGE_ASSIGNMENT_QUERY {path.relative_to(REPO_ROOT)} {stage_id}")
        if re.search(r'WHERE\s+stage_id\s*=\s*"[^"]+"\s+OR\s+assignment_level\s*=\s*"capstone"', body):
            errors.append(f"CROSS_STAGE_CAPSTONE_QUERY {path.relative_to(REPO_ROOT)}")

    old_active = [
        REPO_ROOT / "03-Projects" / "金融与时序" / "02-时间序列分析",
        REPO_ROOT / "03-Projects" / "课程作业" / "02-时间序列分析",
    ]
    for directory in old_active:
        if directory.exists() and any(directory.glob("*.md")):
            errors.append(f"SECOND_ASSIGNMENT_SOURCE {directory.relative_to(REPO_ROOT)}")

    print(f"study_cards={len(study_documents)}")
    print(f"stage_mocs={len(stage_documents)}")
    print(f"assignments={assignment_count}")
    print(f"errors={len(errors)}")
    for error in errors:
        print(error.encode("unicode_escape").decode("ascii"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
