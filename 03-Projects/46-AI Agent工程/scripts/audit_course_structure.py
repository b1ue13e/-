"""Structural audit for the AI Agent engineering course."""

from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if (PROJECT_ROOT.parent / "knowledge").is_dir():
    REPO_ROOT = PROJECT_ROOT.parent
    KNOWLEDGE_ROOT = REPO_ROOT / "knowledge"
    MARKDOWN_ROOTS = (KNOWLEDGE_ROOT, PROJECT_ROOT)
    SNAPSHOT_MODE = True
else:
    REPO_ROOT = PROJECT_ROOT.parents[1]
    KNOWLEDGE_ROOT = REPO_ROOT / "02-Knowledge/🧠 学习系统/46-AI Agent工程"
    MARKDOWN_ROOTS = (REPO_ROOT / "02-Knowledge", REPO_ROOT / "03-Projects")
    SNAPSHOT_MODE = False
ASSIGNMENT_DIRS = {
    "课后作业": "lesson",
    "阶段作业": "stage",
    "大作业": "capstone",
}
START_CARD = "AI-Agent-前置-消息JSON异常与单元测试"
STUDY_FIELDS = {
    "type",
    "topic",
    "course",
    "created",
    "status",
    "difficulty",
    "concept",
    "prerequisites",
    "related",
    "stage_moc",
    "flow",
    "kind",
    "source",
    "source_urls",
    "accessed",
    "license",
}
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
}
WIKILINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
STAGE_ORDER = {f"{stage:02d}": stage for stage in range(7)}
EXCLUDED_PARTS = {".recovery-hold", ".归档", ".reasonix", ".tmp", "__pycache__"}
FORBIDDEN_NAMES = {"李宏毅式", "李宏毅-CMU模式", "4-Tier", "Boss Baseline", "阶梯作业"}


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].lstrip("\ufeff") != "---":
        return {}
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            return fields
        match = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return {}


def duplicate_frontmatter_keys(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].lstrip("\ufeff") != "---":
        return []
    seen: set[str] = set()
    duplicates: set[str] = set()
    for line in lines[1:]:
        if line == "---":
            break
        match = re.match(r"^([A-Za-z_]+):\s*", line)
        if not match:
            continue
        key = match.group(1)
        if key in seen:
            duplicates.add(key)
        seen.add(key)
    return sorted(duplicates)


def parse_list(value: str) -> list[str]:
    try:
        parsed = ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []
    return parsed if isinstance(parsed, list) else []


def link_target(value: str) -> str | None:
    match = WIKILINK_PATTERN.search(value)
    return match.group(1) if match else None


def scalar(value: str) -> str:
    return value.strip().strip("\"'")


def active_markdown(base: Path) -> list[Path]:
    return [
        path
        for path in base.rglob("*.md")
        if not EXCLUDED_PARTS.intersection(path.parts)
    ]


def h1_count(text: str) -> int:
    count = 0
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith("# "):
            count += 1
    return count


def without_fenced_code(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return "\n".join(lines)


def main() -> int:
    errors: list[str] = []
    root_markdown = sorted(KNOWLEDGE_ROOT.glob("*.md"))
    allowed_root = {"🗺️ AI-Agent工程-学习路径.md", "📚 教材挂载索引.md"}
    actual_root = {path.name for path in root_markdown}
    if actual_root != allowed_root:
        errors.append(f"课程根目录 Markdown 应为 {sorted(allowed_root)}，实际为 {sorted(actual_root)}")

    study_files = sorted(KNOWLEDGE_ROOT.glob("[0-9][0-9]-*/AI-Agent-*.md"))
    stage_mocs = sorted(KNOWLEDGE_ROOT.glob("[0-9][0-9]-*/🧭 *.md"))
    if len(study_files) != 19:
        errors.append(f"知识卡应为 19 张，实际为 {len(study_files)}")
    if len(stage_mocs) != 7:
        errors.append(f"阶段 MOC 应为 7 个，实际为 {len(stage_mocs)}")

    current_markdown = active_markdown(KNOWLEDGE_ROOT) + active_markdown(PROJECT_ROOT)
    current_set = set(current_markdown)
    all_markdown = [path for root in MARKDOWN_ROOTS for path in active_markdown(root)]
    by_stem: dict[str, list[Path]] = defaultdict(list)
    normalized_paths: dict[Path, str] = {}
    for path in all_markdown:
        by_stem[path.stem].append(path)
        normalized_paths[path] = path.relative_to(REPO_ROOT).with_suffix("").as_posix()

    for path in current_markdown:
        text = path.read_text(encoding="utf-8")
        link_text = without_fenced_code(text)
        duplicate_keys = duplicate_frontmatter_keys(path)
        if duplicate_keys:
            errors.append(f"{path.name} 的 frontmatter 含重复字段: {duplicate_keys}")
        if h1_count(text) != 1:
            errors.append(f"{path.name} 应恰有一个代码围栏外 H1")
        h1 = next((line for line in text.splitlines() if line.startswith("# ")), "")
        if any(label in path.name or label in h1 for label in FORBIDDEN_NAMES):
            errors.append(f"{path.name} 的文件名或 H1 含禁用历史标签")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.startswith("|") and re.search(r"\[\[[^\]]*(?<!\\)\|[^\]]*\]\]", line):
                errors.append(f"{path.name}:{line_number} 表格 wikilink 别名未转义")
        for raw_target in WIKILINK_PATTERN.findall(link_text):
            target = raw_target.rstrip("\\").replace("\\|", "|")
            if "/" not in target:
                candidates = by_stem.get(target, [])
                local_candidates = [candidate for candidate in candidates if candidate in current_set]
                if len(local_candidates) == 1:
                    candidates = local_candidates
            else:
                normalized_target = target.strip("/")
                if normalized_target.startswith("02-Knowledge/") or normalized_target.startswith("03-Projects/"):
                    normalized_target = normalized_target
                else:
                    normalized_target = normalized_target.replace("02-Knowledge/🧠 学习系统/", "")
                candidates = [
                    candidate
                    for candidate, normalized in normalized_paths.items()
                    if normalized == normalized_target
                    or normalized.endswith(f"/{normalized_target}")
                ]
            if not candidates:
                if SNAPSHOT_MODE:
                    continue
                errors.append(f"{path.name} 的 wikilink 不可解析: {target}")
            elif len(candidates) > 1 and "/" not in target:
                errors.append(f"{path.name} 的 wikilink 存在同名歧义: {target}")

    known_by_name = {path.stem: path for path in study_files + stage_mocs + root_markdown}
    upstream_graph: dict[str, list[str]] = defaultdict(list)
    card_stage: dict[str, str] = {}
    card_stage_number: dict[str, int] = {}

    for path in study_files:
        text = path.read_text(encoding="utf-8")
        fields = parse_frontmatter(path)
        missing = STUDY_FIELDS - fields.keys()
        if missing:
            errors.append(f"{path.name} 缺字段: {sorted(missing)}")
        if path.stem == START_CARD:
            if "upstream" in fields:
                errors.append(f"{path.name} 是课程真正起点，不得保留 upstream 字段")
        elif "upstream" not in fields:
            errors.append(f"{path.name} 缺直接前置字段 upstream")
        elif not parse_list(fields["upstream"]):
            errors.append(f"{path.name} 的 upstream 不得为空数组或普通字符串")
        if "downstream" in fields:
            errors.append(f"{path.name} 不得静态维护 downstream")
        if "contains(upstream, this.file.link)" not in text:
            errors.append(f"{path.name} 缺直接后续派生查询")
        if "contains(requires, this.file.link)" not in text:
            errors.append(f"{path.name} 缺作业派生查询")
        if "## 🧪 学完本节后可完成的作业" not in text:
            errors.append(f"{path.name} 缺作业验收标题")

        stage_target = link_target(fields.get("stage_moc", ""))
        if not stage_target or stage_target not in known_by_name:
            errors.append(f"{path.name} 的 stage_moc 不可解析: {fields.get('stage_moc')}")
        else:
            card_stage[path.stem] = stage_target
            card_stage_number[path.stem] = int(path.parent.name[:2])
            if f"[[{path.stem}]]" not in known_by_name[stage_target].read_text(encoding="utf-8"):
                errors.append(f"{stage_target} 未收录 {path.stem}")

        for value in parse_list(fields.get("upstream", "[]")):
            target = link_target(value)
            if not target or target not in known_by_name:
                errors.append(f"{path.name} 的 upstream 不可解析: {value}")
            else:
                upstream_graph[path.stem].append(target)

    state: dict[str, int] = {}

    def visit(node: str) -> None:
        if state.get(node) == 1:
            errors.append(f"upstream 图存在环: {node}")
            return
        if state.get(node) == 2:
            return
        state[node] = 1
        for dependency in upstream_graph[node]:
            visit(dependency)
        state[node] = 2

    for node in list(upstream_graph):
        visit(node)

    coverage: dict[str, int] = defaultdict(int)
    assignment_count = 0
    for directory, expected_level in ASSIGNMENT_DIRS.items():
        for path in sorted((PROJECT_ROOT / directory).glob("*.md")):
            assignment_count += 1
            fields = parse_frontmatter(path)
            missing = ASSIGNMENT_FIELDS - fields.keys()
            if missing:
                errors.append(f"{path.name} 缺字段: {sorted(missing)}")
            if scalar(fields.get("course", "")) != "AI Agent工程":
                errors.append(f"{path.name} 的 course 错误: {fields.get('course')}")
            level = fields.get("assignment_level", "")
            if level != expected_level:
                errors.append(f"{path.name} assignment_level={level}，目录要求 {expected_level}")
            assignment_stage = STAGE_ORDER.get(scalar(fields.get("stage_id", "")))
            if assignment_stage is None:
                errors.append(f"{path.name} 的 stage_id 非法: {fields.get('stage_id')}")
            for value in parse_list(fields.get("requires", "[]")):
                target = link_target(value)
                if not target or target not in known_by_name or target not in card_stage:
                    errors.append(f"{path.name} 的 requires 不可解析为知识卡: {value}")
                else:
                    coverage[target] += 1
                    if assignment_stage is not None and card_stage_number[target] > assignment_stage:
                        errors.append(
                            f"{path.name} 在阶段 {assignment_stage} 要求尚未教授的 {target}"
                        )

    if assignment_count != 11:
        errors.append(f"规范作业应为 11 份，实际为 {assignment_count}")
    uncovered = sorted(path.stem for path in study_files if coverage[path.stem] == 0)
    if uncovered:
        errors.append(f"知识卡未被任何作业 requires 覆盖: {uncovered}")

    legacy_dirs = ["guided-labs", "local-acceptance", "作业映射", "课后习题"]
    for directory in legacy_dirs:
        if (PROJECT_ROOT / directory).exists():
            errors.append(f"旧目录仍在活动区: {directory}")

    if errors:
        print("COURSE STRUCTURE AUDIT: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("COURSE STRUCTURE AUDIT: PASSED")
    print(f"- knowledge cards: {len(study_files)}")
    print(f"- stage MOCs: {len(stage_mocs)}")
    print(f"- assignments: {assignment_count}")
    print(f"- covered cards: {len(coverage)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
