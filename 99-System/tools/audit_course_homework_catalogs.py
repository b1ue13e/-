"""Audit complete official-link and local-extension homework catalogs."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from build_course_homework_catalogs import CATALOGS, all_units, capstone_path


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT / "03-Projects" / "课程作业"
STUDY_ROOT = ROOT / "02-Knowledge" / "🧠 学习系统"
INDEX_PATH = PROJECT_ROOT / "33门课程完整作业包索引.md"
EXPECTED_OFFICIAL = 273
EXPECTED_LOCAL = 132
EXPECTED_UNITS = 405
PLACEHOLDER_PATTERN = re.compile(r"\b(?:TODO|TBD)\b|待补|待完善", re.I)
REQUIRED_TERMS = {
    "01": ("网络统计", "节点嵌入", "链路预测", "推荐系统", "GNN"),
    "05": ("kNN", "Softmax", "CNN", "Transformer", "Diffusion", "CLIP"),
    "08": ("Word Vectors", "反向传播", "依存分析", "Transformers", "LLM"),
    "10": ("哈希", "堆", "平衡搜索树", "图搜索", "动态规划"),
    "13": ("Value Iteration", "Q-Learning", "Policy Gradient", "Actor-Critic", "模型式强化学习"),
    "14": ("变量消元", "采样", "参数学习", "结构学习", "因果图"),
    "17": ("ML2021 HW01", "ML2021 HW15", "ML2023 HW01", "ML2023 HW15", "本地扩展"),
    "23": ("GCN", "GraphSAGE", "异构图", "图级表示", "图学习项目"),
    "36": ("MinHash/LSH", "推荐系统", "PageRank", "倒排索引", "检索评测"),
}


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) != 3:
        return {}, text
    data = yaml.safe_load(parts[1])
    return (data if isinstance(data, dict) else {}), text


def wiki_target(raw: str) -> Path:
    target = raw.split("|", 1)[0].split("#", 1)[0].replace("\\", "/")
    path = ROOT / target
    return path if path.suffix else path.with_suffix(".md")


def main() -> int:
    errors: list[str] = []
    if len(CATALOGS) != 33:
        errors.append(f"catalog manifest course count={len(CATALOGS)}, expected=33")
    official_total = sum(len(item.official) for item in CATALOGS)
    local_total = sum(len(item.local_topics) for item in CATALOGS)
    unit_total = sum(len(all_units(item)) for item in CATALOGS)
    if official_total != EXPECTED_OFFICIAL:
        errors.append(f"official total={official_total}, expected={EXPECTED_OFFICIAL}")
    if local_total != EXPECTED_LOCAL:
        errors.append(f"local total={local_total}, expected={EXPECTED_LOCAL}")
    if unit_total != EXPECTED_UNITS:
        errors.append(f"unit total={unit_total}, expected={EXPECTED_UNITS}")

    index_data, index_text = parse_frontmatter(INDEX_PATH) if INDEX_PATH.exists() else ({}, "")
    for field, expected in {
        "course_count": 33,
        "official_assignment_count": EXPECTED_OFFICIAL,
        "local_extension_count": EXPECTED_LOCAL,
        "assignment_unit_count": EXPECTED_UNITS,
    }.items():
        if index_data.get(field) != expected:
            errors.append(f"central index {field}={index_data.get(field)!r}, expected={expected}")
    if len(re.findall(r"(?m)^\|\s*(?:0[1-9]|1[0-7]|2[2-9]|3[0-7])\s*\|", index_text)) != 33:
        errors.append("central index does not contain 33 course rows")

    passed = 0
    for catalog in CATALOGS:
        label = f"{catalog.code}-{catalog.course}"
        path = PROJECT_ROOT / label / "课程作业总表.md"
        local_errors: list[str] = []
        if not path.exists():
            local_errors.append("missing catalog")
        else:
            data, text = parse_frontmatter(path)
            units = all_units(catalog)
            expected = {
                "type": "index",
                "kind": "moc",
                "flow": "project",
                "course": catalog.course,
                "official_assignment_count": len(catalog.official),
                "local_extension_count": len(catalog.local_topics),
                "assignment_unit_count": len(units),
                "source_policy": "link-only-by-default",
                "solution_visibility": "private",
            }
            for field, value in expected.items():
                if data.get(field) != value:
                    local_errors.append(f"{field}={data.get(field)!r}, expected={value!r}")

            section_ids = re.findall(r"(?m)^###\s+((?:OF|LOCAL)-[^ ·]+)\s+·", text)
            expected_ids = [unit.unit_id for unit in units]
            if section_ids != expected_ids:
                local_errors.append("execution-card IDs do not exactly match manifest order")
            if len(set(section_ids)) != len(section_ids):
                local_errors.append("duplicate execution-card ID")
            for unit in units:
                if unit.title not in text:
                    local_errors.append(f"missing unit title: {unit.title}")
                if f"[{unit.source}]({unit.url})" not in text:
                    local_errors.append(f"missing source link for {unit.unit_id}")
            for name, url, policy in catalog.materials:
                if f"[{name}]({url})" not in text or f"`{policy}`" not in text:
                    local_errors.append(f"missing material/policy: {name}")
            for term in REQUIRED_TERMS.get(catalog.code, ()):
                if term not in text:
                    local_errors.append(f"missing required topic: {term}")
            if PLACEHOLDER_PATTERN.search(text):
                local_errors.append("contains TODO/TBD placeholder")
            if "不复制官方题干、Starter 压缩包或参考解答" not in text and catalog.official:
                local_errors.append("missing official-content copy boundary")

            capstone = ROOT / capstone_path(catalog)
            capstone = capstone if capstone.suffix else capstone.with_suffix(".md")
            if not capstone.exists():
                local_errors.append("capstone link target missing")
            if f"[[{capstone_path(catalog)}]]" not in text:
                local_errors.append("catalog does not link canonical capstone")

            resource = STUDY_ROOT / label / "📚 教材挂载索引.md"
            resource_text = resource.read_text(encoding="utf-8") if resource.exists() else ""
            match = re.search(
                r"(?s)<!-- complete-homework-catalog:start -->(.*?)"
                r"<!-- complete-homework-catalog:end -->",
                resource_text,
            )
            if not match:
                local_errors.append("course resource index missing complete-catalog block")
            else:
                links = re.findall(r"\[\[([^\]]+)\]\]", match.group(1))
                if len(links) != 1:
                    local_errors.append(f"catalog block links={len(links)}, expected=1")
                elif wiki_target(links[0]).resolve() != path.resolve():
                    local_errors.append("catalog block points to wrong file")

            relative = path.relative_to(ROOT).with_suffix("").as_posix()
            if f"[[{relative}|" not in index_text:
                local_errors.append("central index missing catalog link")

        if local_errors:
            print(f"FAIL\t{label}\t问题={len(local_errors)}")
            errors.extend(f"{label}\t{item}" for item in local_errors)
        else:
            passed += 1
            print(
                f"PASS\t{label}\tofficial={len(catalog.official)}\t"
                f"local={len(catalog.local_topics)}\tunits={len(all_units(catalog))}"
            )

    print(
        f"TOTAL\t课程={len(CATALOGS)}\t通过={passed}\t课程内官方入口条目={official_total}\t"
        f"本地扩展={local_total}\t单元={unit_total}"
    )
    if errors:
        for error in errors:
            print(f"ERROR\t{error}")
        return 1
    print("RESULT\t33/33 完整作业包通过；官方材料保持 link-only，作业编目不代表已完成。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
