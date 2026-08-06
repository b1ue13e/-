"""Audit the canonical formal assignment pack for all 33 learning paths."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
STUDY_ROOT = ROOT / "02-Knowledge" / "🧠 学习系统"
PROJECT_ROOT = ROOT / "03-Projects" / "课程作业"
INDEX_PATH = PROJECT_ROOT / "33门课程正式作业索引.md"
QLIB_PATH = (
    ROOT
    / "03-Projects"
    / "金融与时序"
    / "03-量化金融"
    / "HW17：Qlib 因子研究与成本敏感回测.md"
)
COURSE_PATTERN = re.compile(r"^(0[1-9]|1[0-7]|2[2-9]|3[0-7])-(.+)$")
FORMAL_COURSE_DIRS = {
    "01-社交网络挖掘", "02-时间序列分析", "03-量化金融", "04-离散数学",
    "05-计算机视觉", "06-常微分方程", "07-最优化方法", "08-NLP全栈",
    "09-高等代数", "10-数据结构与算法", "11-计算机组成原理", "12-信号与系统",
    "13-强化学习", "14-概率图模型", "15-控制与机器人学", "16-多元统计",
    "17-机器学习", "22-概率论与数理统计", "23-图神经网络", "24-随机过程",
    "25-测度论", "26-实变函数", "27-泛函分析", "28-数学分析",
    "29-运筹学", "30-应用回归分析", "31-属性数据分析", "32-非参数统计",
    "33-贝叶斯统计", "34-偏微分方程", "35-数值分析",
    "36-数据挖掘与信息检索", "37-复变函数",
}
REQUIRED_FIELDS = (
    "course",
    "source_url",
    "source_course",
    "source_version",
    "license",
    "mirror_policy",
    "adaptation",
    "dataset_version",
    "starter_code",
    "tests",
    "baseline",
    "acceptance_test",
    "compute_budget",
    "solution_visibility",
)
REQUIRED_SECTION_PATTERNS = {
    "任务": r"(?m)^##\s+\d+\.\s+任务",
    "来源": r"(?m)^##\s+\d+\.\s+来源",
    "测试": r"(?m)^##\s+\d+\.\s+(?:验收|最小)测试",
    "Rubric": r"(?m)^##\s+\d+\.\s+.*Rubric",
    "提交物": r"(?m)^##\s+\d+\.\s+提交物",
    "失败条件": r"(?m)^##\s+\d+\.\s+失败条件",
    "当前状态": r"(?m)^##\s+\d+\.\s+当前状态",
}
PLACEHOLDER_PATTERN = re.compile(r"\b(?:TODO|TBD)\b|待补|待完善", re.I)


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8-sig", errors="strict").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) != 3:
        return {}, text
    data = yaml.safe_load(parts[1])
    return (data if isinstance(data, dict) else {}), text


def wiki_target(link: str) -> Path:
    target = link.split("|", 1)[0].split("#", 1)[0].replace("\\", "/")
    path = ROOT / target
    return path if path.suffix else path.with_suffix(".md")


def rubric_sum(text: str) -> int | None:
    match = re.search(r"(?ms)^##\s+\d+\.\s+.*Rubric.*?\n(.*?)(?=^##\s|\Z)", text)
    if not match:
        return None
    total = 0
    found = False
    for line in match.group(1).splitlines():
        if not line.startswith("|") or "总计" in line:
            continue
        cells = [cell.strip().strip("*") for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2 or not re.fullmatch(r"\d+", cells[1]):
            continue
        total += int(cells[1])
        found = True
    return total if found else None


def course_roots() -> list[tuple[str, str, Path]]:
    rows: list[tuple[str, str, Path]] = []
    for path in STUDY_ROOT.iterdir():
        if not path.is_dir() or path.name not in FORMAL_COURSE_DIRS:
            continue
        match = COURSE_PATTERN.match(path.name)
        if match:
            rows.append((match.group(1), match.group(2), path))
    return sorted(rows)


def assignment_for(code: str, course: str) -> tuple[Path | None, list[str]]:
    if code == "03":
        return QLIB_PATH, []
    course_dir = PROJECT_ROOT / f"{code}-{course}"
    files = sorted(course_dir.glob("项目-*.md")) if course_dir.exists() else []
    errors: list[str] = []
    if len(files) != 1:
        errors.append(f"正式目录应有且仅有 1 份作业，实际={len(files)}")
    return (files[0] if len(files) == 1 else None), errors


def main() -> int:
    errors: list[str] = []
    courses = course_roots()
    if len(courses) != 33:
        errors.append(f"正式课程数量应为 33，实际={len(courses)}")

    index_text = INDEX_PATH.read_text(encoding="utf-8") if INDEX_PATH.exists() else ""
    index_rows = re.findall(r"(?m)^\|\s*(\d{2})\s*\|", index_text)
    if len(index_rows) != 33 or len(set(index_rows)) != 33:
        errors.append(f"正式作业索引应有 33 个唯一课程行，实际={len(index_rows)}")

    passed = 0
    for code, course, course_root in courses:
        label = f"{code}-{course}"
        path, assignment_errors = assignment_for(code, course)
        local_errors = list(assignment_errors)
        if path is None or not path.exists():
            local_errors.append("正式作业文件不存在")
        else:
            data, text = parse_frontmatter(path)
            expected = {
                "type": "project",
                "kind": "project",
                "flow": "project",
                "project_type": "homework",
                "asset_eligibility": "eligible",
                "course": course,
            }
            for field, value in expected.items():
                if data.get(field) != value:
                    local_errors.append(f"{field} 应为 {value!r}，实际={data.get(field)!r}")
            for field in REQUIRED_FIELDS:
                if data.get(field) in (None, ""):
                    local_errors.append(f"缺少资格字段 {field}")
            if data.get("mirror_policy") not in {"link-only", "local-clone", "fork"}:
                local_errors.append("mirror_policy 枚举无效")
            if data.get("solution_visibility") not in {"private", "summary-only"}:
                local_errors.append("solution_visibility 枚举无效")
            if not str(data.get("source_url", "")).startswith(("https://", "http://")):
                local_errors.append("source_url 不是 HTTP(S) 地址")
            for section, pattern in REQUIRED_SECTION_PATTERNS.items():
                if not re.search(pattern, text):
                    local_errors.append(f"缺少章节：{section}")
            score = rubric_sum(text)
            if score != 100:
                local_errors.append(f"Rubric 合计应为 100，实际={score}")
            if PLACEHOLDER_PATTERN.search(text):
                local_errors.append("包含 TODO/TBD/待补类占位词")

            resource_path = course_root / "📚 教材挂载索引.md"
            resource_text = (
                resource_path.read_text(encoding="utf-8") if resource_path.exists() else ""
            )
            block_match = re.search(
                r"(?s)<!-- formal-homework:start -->(.*?)<!-- formal-homework:end -->",
                resource_text,
            )
            if not block_match:
                local_errors.append("教材挂载索引缺少正式作业入口")
            else:
                links = re.findall(r"\[\[([^\]]+)\]\]", block_match.group(1))
                if len(links) != 1:
                    local_errors.append(f"正式作业入口应有 1 个双链，实际={len(links)}")
                elif wiki_target(links[0]).resolve() != path.resolve():
                    local_errors.append("教材挂载索引指向的不是本课程 canonical 作业")

            relative_target = path.relative_to(ROOT).with_suffix("").as_posix()
            if f"[[{relative_target}|" not in index_text:
                local_errors.append("33 门课程正式作业索引缺少 canonical 链接")

        if local_errors:
            for error in local_errors:
                errors.append(f"{label}\t{error}")
            print(f"FAIL\t{label}\t问题={len(local_errors)}")
        else:
            passed += 1
            print(f"PASS\t{label}\teligible=1\trubric=100")

    print(f"TOTAL\t课程={len(courses)}\t通过={passed}\t失败={len(courses) - passed}")
    if errors:
        print("\n".join(f"ERROR\t{error}" for error in errors))
        return 1
    print("RESULT\t33/33 门课程均有一份 canonical 正式作业；规格合格不代表已经执行。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
