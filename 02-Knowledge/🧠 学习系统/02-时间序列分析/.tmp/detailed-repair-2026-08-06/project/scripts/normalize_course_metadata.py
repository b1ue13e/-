from __future__ import annotations

import argparse
import pathlib
import re


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
COURSE_ROOT = REPO_ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统" / "02-时间序列分析"
TODAY = "2026-08-06"
LEGACY_TYPES = {"concept", "derivation", "problem-type", "mistake"}


def scalar(value: str) -> str:
    return value.strip().strip('"').strip("'")


def top_level_fields(lines: list[str]) -> dict[str, int]:
    fields: dict[str, int] = {}
    for index, line in enumerate(lines):
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s.*)?$", line)
        if match:
            fields[match.group(1)] = index
    return fields


def value_at(lines: list[str], fields: dict[str, int], key: str) -> str:
    if key not in fields:
        return ""
    return scalar(lines[fields[key]].split(":", 1)[1])


def normalize(path: pathlib.Path) -> tuple[str, list[str]]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return text, []
    try:
        end = lines.index("---", 1)
    except ValueError:
        return text, []

    front = lines[1:end]
    changes: list[str] = []
    fields = top_level_fields(front)
    original_type = value_at(front, fields, "type")

    if original_type in LEGACY_TYPES:
        front[fields["type"]] = "type: study"
        changes.append(f"type {original_type} -> study")
        fields = top_level_fields(front)
    is_study = original_type == "study" or original_type in LEGACY_TYPES

    if is_study:
        if value_at(front, fields, "course") != "时间序列分析":
            if "course" in fields:
                front[fields["course"]] = 'course: "时间序列分析"'
            else:
                front.append('course: "时间序列分析"')
            changes.append("normalize course")
            fields = top_level_fields(front)

        if "topic" not in fields:
            topic = value_at(front, fields, "title") or path.stem
            front.append(f'topic: "{topic}"')
            changes.append("add topic")
            fields = top_level_fields(front)

        if "created" not in fields:
            if "date" in fields:
                front[fields["date"]] = f"created: {value_at(front, fields, 'date')}"
            else:
                front.append(f"created: {TODAY}")
            changes.append("add created")
            fields = top_level_fields(front)

        if value_at(front, fields, "status") in {"learning", "active"}:
            front[fields["status"]] = "status: ongoing"
            changes.append("normalize status")
        elif "status" not in fields:
            front.append("status: ongoing")
            changes.append("add status")
        fields = top_level_fields(front)

        if "flow" not in fields:
            front.append("flow: knowledge")
            changes.append("add flow")
        if "kind" not in fields:
            kind = original_type if original_type in LEGACY_TYPES else "concept"
            front.append(f"kind: {kind}")
            changes.append("add kind")

    fields = top_level_fields(front)
    remove_indexes: set[int] = set()
    for key in ("next", "downstream"):
        if key in fields:
            remove_indexes.add(fields[key])
            changes.append(f"remove {key}")
    for key in ("prerequisites", "related", "upstream"):
        if key in fields and value_at(front, fields, key) in {"[]", "[ ]"}:
            remove_indexes.add(fields[key])
            changes.append(f"remove empty {key}")
    front = [line for index, line in enumerate(front) if index not in remove_indexes]

    normalized = "\n".join(["---", *front, "---", *lines[end + 1 :]]) + "\n"
    return normalized, changes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    changed = 0
    for path in sorted(COURSE_ROOT.rglob("*.md")):
        if ".tmp" in path.parts or ".reasonix" in path.parts:
            continue
        normalized, changes = normalize(path)
        if not changes:
            continue
        changed += 1
        print(f"{path.relative_to(COURSE_ROOT)}: {', '.join(changes)}")
        if args.write:
            path.write_text(normalized, encoding="utf-8")
    print(f"changed_files={changed} mode={'write' if args.write else 'dry-run'}")


if __name__ == "__main__":
    main()
