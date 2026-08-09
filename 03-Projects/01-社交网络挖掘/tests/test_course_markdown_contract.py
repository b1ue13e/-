from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


VAULT_ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = VAULT_ROOT / "02-Knowledge" / "🧠 学习系统" / "01-社交网络挖掘"
PROJECT_ROOT = VAULT_ROOT / "03-Projects" / "01-社交网络挖掘"


def _document(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^\ufeff?---\r?\n(.*?)\r?\n---", text, re.DOTALL)
    assert match, f"missing frontmatter: {path}"
    metadata = yaml.safe_load(match.group(1))
    assert isinstance(metadata, dict), f"frontmatter is not a mapping: {path}"
    return metadata, text


def _wikilinks(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [link for item in value for link in _wikilinks(item)]
    if not isinstance(value, str):
        return []
    return [
        link.split("#", 1)[0].split("|", 1)[0].rsplit("/", 1)[-1]
        for link in re.findall(r"\[\[([^\]]+)\]\]", value)
    ]


def _study_cards() -> list[Path]:
    return [
        path
        for path in COURSE_ROOT.rglob("*.md")
        if _document(path)[0].get("type") == "study"
    ]


def _assignment_files() -> list[Path]:
    files = []
    for path in PROJECT_ROOT.rglob("*.md"):
        if not path.read_text(encoding="utf-8").startswith("---"):
            continue
        metadata, _ = _document(path)
        if metadata.get("type") == "project" and metadata.get("project_type") == "homework":
            files.append(path)
    return files


def test_card_relations_sources_and_derived_views() -> None:
    cards = _study_cards()
    by_name: dict[str, list[Path]] = {}
    for path in cards:
        by_name.setdefault(path.stem, []).append(path)
    assert len(cards) == 31
    assert all(len(paths) == 1 for paths in by_name.values())

    for path in cards:
        metadata, text = _document(path)
        assert metadata.get("course") == "社交网络挖掘"
        assert metadata.get("status") in {"planned", "ongoing", "completed"}
        assert metadata.get("source")
        assert str(metadata.get("source_url", "")).startswith("https://")
        assert metadata.get("license")
        assert "downstream" not in metadata

        stage_links = _wikilinks(metadata.get("stage_moc"))
        assert len(stage_links) == 1, f"invalid stage_moc: {path}"
        stage_targets = list(COURSE_ROOT.rglob(f"{stage_links[0]}.md"))
        assert len(stage_targets) == 1, f"unresolved or ambiguous stage_moc: {path}"

        upstream = _wikilinks(metadata.get("upstream"))
        if path.name == "数学与Python前置诊断.md":
            assert not upstream
        else:
            assert upstream, f"missing upstream: {path}"
            assert all(name in by_name for name in upstream), f"unresolved upstream: {path}"

        assert "## 学完后可以完成" in text
        assert "contains(requires, this.file.link)" in text


def test_upstream_graph_is_acyclic() -> None:
    cards = _study_cards()
    graph = {
        path.stem: _wikilinks(_document(path)[0].get("upstream"))
        for path in cards
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visited:
            return
        assert node not in visiting, f"upstream cycle at {node}"
        visiting.add(node)
        for parent in graph[node]:
            visit(parent)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)


def test_assignment_contract_and_resolved_knowledge_links() -> None:
    assignments = _assignment_files()
    expected_directory = {"lesson": "课后作业", "stage": "阶段作业", "capstone": "大作业"}
    expected_counts = {"lesson": 1, "stage": 6, "capstone": 1}
    actual_counts = {level: 0 for level in expected_counts}
    card_names = {path.stem for path in _study_cards()}
    covered: set[str] = set()

    assert len(assignments) == 8
    for path in assignments:
        metadata, text = _document(path)
        level = metadata.get("assignment_level")
        assert level in expected_directory
        actual_counts[level] += 1
        assert path.parent.name == expected_directory[level]
        assert metadata.get("assignment_format")
        assert metadata.get("stage_id")
        assert metadata.get("source_type") in {
            "official_assignment",
            "open_textbook_exercise",
            "open_source_project_task",
            "local_integration_task",
        }
        requires = _wikilinks(metadata.get("requires"))
        assert requires, f"empty requires: {path}"
        assert all(name in card_names for name in requires), f"unresolved requires: {path}"
        covered.update(requires)
        for heading in ("提交产物", "Rubric", "自检"):
            assert heading in text, f"missing {heading}: {path}"

    assert actual_counts == expected_counts
    assert card_names <= covered


def test_single_assignment_source_and_removed_legacy_names() -> None:
    indexes = list(PROJECT_ROOT.rglob("🧭 课程作业总索引.md"))
    assert indexes == [PROJECT_ROOT / "🧭 课程作业总索引.md"]
    stale_names = {
        "PageRank-HITS-PPR与Spam-Farm",
        "community_edges.csv",
        "propagation_edges.csv",
    }
    for root in (COURSE_ROOT, PROJECT_ROOT):
        for path in root.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            assert not any(name in text for name in stale_names), f"stale reference: {path}"

    lesson_files = sorted((PROJECT_ROOT / "课后作业").glob("*.md"))
    assert [path.name for path in lesson_files] == [
        "社交网络挖掘-课后作业-00-前置诊断与环境自检.md"
    ]


def test_every_card_python_example_executes() -> None:
    block_pattern = re.compile(r"^```(?:python|py)\s*\n(.*?)^```\s*$", re.DOTALL | re.MULTILINE)
    executed = 0
    for path in _study_cards():
        text = path.read_text(encoding="utf-8")
        blocks = block_pattern.findall(text)
        assert blocks, f"missing runnable Python example: {path}"
        for index, code in enumerate(blocks, start=1):
            namespace = {"__name__": f"card_{path.stem}_{index}"}
            exec(compile(code, f"{path}::block-{index}", "exec"), namespace)
            executed += 1
    assert executed >= len(_study_cards())
