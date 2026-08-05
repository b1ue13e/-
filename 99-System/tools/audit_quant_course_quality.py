#!/usr/bin/env python3
"""Fail-fast quality gate for the canonical quant-finance course slice."""
from __future__ import annotations

import ast
import math
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
QUANT = ROOT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"
LEARNING_PATH = QUANT / "🗺️ 量化金融学习路径.md"
BLACK_SCHOLES_PAGE = QUANT / "02-量化核心技能" / "Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model).md"
SKIP_DIRS = {
    ".git",
    ".obsidian",
    ".recovery-hold",
    ".tmp",
    "__pycache__",
    "site-packages",
}
CODE_BLOCK_RE = re.compile(r"```([^\n`]*)\n(.*?)```", re.S)
PYTHON_BLOCK_RE = re.compile(r"```(?:python|py)\s*\n(.*?)```", re.S | re.I)
WIKILINK_RE = re.compile(r"!?\[\[(.*?)\]\]")
BARE_TABLE_ALIAS_RE = re.compile(r"\[\[[^\]\r\n]*?(?<!\\)\|[^\]\r\n]*\]\]")

OFFICIAL_PAGES = [
    QUANT / "00-课程说明与先修诊断.md",
    LEARNING_PATH,
    QUANT / "知识地图" / "🗺️ 量化金融全栈终极框架 (Academic + AFML + HFT).md",
    QUANT / "03-Projects" / "Capstone-统一标的贯穿实战项目.md",
    QUANT / "03-Projects" / "Capstone-AAPL" / "README.md",
    QUANT / "03-Projects" / "HW05-BSM" / "README.md",
    QUANT / "03-Projects" / "Phase2-GARCH" / "README.md",
    QUANT / "03-Projects" / "HW01-CAPM" / "README.md",
    QUANT / "03-Projects" / "HW06-DynamicVaR" / "README.md",
    QUANT / "03-Projects" / "Tree-Model-Baseline" / "README.md",
    QUANT / "知识地图" / "📦 外部实验资产索引.md",
    QUANT / "01-夯实基础" / "收益率与对数收益率.md",
    QUANT / "01-夯实基础" / "OHLCV字段清洗与复权.md",
    QUANT / "01-夯实基础" / "时间索引与频率（量化）.md",
    QUANT / "01-夯实基础" / "Pandas分组聚合与透视表.md",
    QUANT / "01-夯实基础" / "滚动窗口与波动率特征.md",
    QUANT / "01-夯实基础" / "量化金融-Level0-累计交错测验.md",
    QUANT / "02-量化核心技能" / "样本泄漏.md",
    BLACK_SCHOLES_PAGE,
] + [
    QUANT / "知识地图" / "00-每周学习执行卡.md",
    QUANT / "01-夯实基础" / "00-零基础补救-数学统计与Python.md",
    QUANT / "01-夯实基础" / "00-量化金融符号与术语速查.md",
    QUANT / "03-Projects" / "课程质量自查记录.md",
] + sorted((QUANT / "03-Projects" / "开源课程课后习题").glob("*.md"))

PROJECT_FILES = [
    QUANT / "03-Projects" / "Capstone-AAPL" / "requirements.txt",
    QUANT / "03-Projects" / "Capstone-AAPL" / "src" / "phase1_baseline.py",
    QUANT / "03-Projects" / "Capstone-AAPL" / "tests" / "test_phase1_baseline.py",
    QUANT / "03-Projects" / "HW05-BSM" / "requirements.txt",
    QUANT / "03-Projects" / "HW05-BSM" / "src" / "bsm_lab.py",
    QUANT / "03-Projects" / "HW05-BSM" / "tests" / "test_bsm_lab.py",
    QUANT / "03-Projects" / "Phase2-GARCH" / "requirements.txt",
    QUANT / "03-Projects" / "Phase2-GARCH" / "src" / "garch_lab.py",
    QUANT / "03-Projects" / "Phase2-GARCH" / "tests" / "test_garch_lab.py",
    QUANT / "03-Projects" / "HW01-CAPM" / "requirements.txt",
    QUANT / "03-Projects" / "HW01-CAPM" / "src" / "capm_lab.py",
    QUANT / "03-Projects" / "HW01-CAPM" / "tests" / "test_capm_lab.py",
    QUANT / "03-Projects" / "HW06-DynamicVaR" / "requirements.txt",
    QUANT / "03-Projects" / "HW06-DynamicVaR" / "src" / "dynamic_var.py",
    QUANT / "03-Projects" / "HW06-DynamicVaR" / "tests" / "test_dynamic_var.py",
    QUANT / "03-Projects" / "Tree-Model-Baseline" / "requirements.txt",
    QUANT / "03-Projects" / "Tree-Model-Baseline" / "src" / "tree_baseline.py",
    QUANT / "03-Projects" / "Tree-Model-Baseline" / "tests" / "test_tree_baseline.py",
]


def project_test_dirs() -> list[Path]:
    projects_root = QUANT / "03-Projects"
    return sorted({path.parents[1] for path in projects_root.rglob("tests/test_*.py")})


def markdown_files() -> list[Path]:
    paths: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(".md"):
                paths.append(Path(dirpath) / filename)
    return paths


def strip_code_blocks(text: str) -> str:
    return CODE_BLOCK_RE.sub("", normalize_callout_blocks(text))


def audit_table_wikilink_escaping(errors: list[str]) -> None:
    for path in QUANT.rglob("*.md"):
        text = strip_code_blocks(path.read_text(encoding="utf-8-sig"))
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.lstrip().startswith("|") and BARE_TABLE_ALIAS_RE.search(line):
                errors.append(
                    "table wikilink alias must escape its pipe: "
                    f"{path.relative_to(ROOT)}:{line_number}"
                )


def normalize_callout_blocks(text: str) -> str:
    """Remove one Markdown quote prefix so code inside Obsidian callouts is audited."""
    return re.sub(r"(?m)^> ?", "", text)


def build_stem_index(paths: list[Path]) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = defaultdict(list)
    for path in paths:
        index[path.stem].append(path)
    return index


def resolves_link(source: Path, target: str, stems: dict[str, list[Path]]) -> bool:
    target = re.split(r"\\?\|", target, maxsplit=1)[0]
    target = target.split("#", 1)[0].strip().replace("\\", "/")
    if not target or "{{" in target:
        return True

    candidate = Path(*target.split("/"))
    if candidate.suffix.lower() not in {".md", ".pdf", ".py", ".csv", ".json"}:
        candidate = candidate.with_suffix(".md")
    if (source.parent / candidate).exists() or (ROOT / candidate).exists() or (QUANT / candidate).exists():
        return True

    if "/" in target:
        return False

    name = Path(target).name.removesuffix(".md")
    return bool(stems.get(name))


def audit_python_blocks(errors: list[str]) -> None:
    for path in QUANT.rglob("*.md"):
        text = normalize_callout_blocks(path.read_text(encoding="utf-8-sig"))
        for number, block in enumerate(PYTHON_BLOCK_RE.findall(text), start=1):
            try:
                ast.parse(block)
            except SyntaxError as exc:
                errors.append(
                    f"invalid Python block {number} in {path.relative_to(ROOT)}: {exc.msg}"
                )


def audit_official_links(errors: list[str], all_md: list[Path]) -> None:
    stems = build_stem_index(all_md)
    for path in OFFICIAL_PAGES:
        if not path.exists():
            continue
        visible = strip_code_blocks(path.read_text(encoding="utf-8-sig"))
        for match in WIKILINK_RE.finditer(visible):
            if not resolves_link(path, match.group(1), stems):
                errors.append(
                    f"broken official link in {path.relative_to(ROOT)}: {match.group(1)}"
                )


def unresolved_course_links(all_md: list[Path]) -> list[str]:
    stems = build_stem_index(all_md)
    warnings: list[str] = []
    for path in QUANT.rglob("*.md"):
        visible = strip_code_blocks(path.read_text(encoding="utf-8-sig"))
        for match in WIKILINK_RE.finditer(visible):
            if not resolves_link(path, match.group(1), stems):
                warnings.append(
                    f"{path.relative_to(ROOT)}: {match.group(1)}"
                )
    return warnings


def audit_black_scholes_anchor(errors: list[str]) -> None:
    spot, strike, maturity, rate, volatility = 100.0, 110.0, 1.0, 0.05, 0.20
    d1 = (
        math.log(spot / strike)
        + (rate + 0.5 * volatility**2) * maturity
    ) / (volatility * math.sqrt(maturity))
    d2 = d1 - volatility * math.sqrt(maturity)
    if not math.isclose(d2, -0.326551, abs_tol=1e-6):
        errors.append(f"Black-Scholes numerical anchor changed unexpectedly: d2={d2}")

    page = BLACK_SCHOLES_PAGE
    if page.exists() and "-0.326551" not in page.read_text(encoding="utf-8-sig"):
        errors.append("Black-Scholes page is missing the verified d2 anchor -0.326551")


def audit_machine_bound_paths(errors: list[str]) -> None:
    for path in QUANT.rglob("*.md"):
        text = path.read_text(encoding="utf-8-sig")
        if re.search(r"file:///([A-Za-z]:|/Users/|/home/)", text, re.I):
            errors.append(f"machine-bound file URI in {path.relative_to(ROOT)}")
        if re.search(r"(?<![A-Za-z0-9:/])[A-Za-z]:[\\/]", text):
            errors.append(f"machine-bound drive path in {path.relative_to(ROOT)}")


def audit_project_tests(errors: list[str]) -> None:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for project in project_test_dirs():
        if not project.exists():
            continue
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=project,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            check=False,
        )
        if result.returncode != 0:
            output = (result.stdout + result.stderr).strip().replace("\n", " | ")
            errors.append(f"project tests failed in {project.relative_to(ROOT)}: {output}")


def audit_project_layout(errors: list[str]) -> None:
    for project in project_test_dirs():
        required = [project / "README.md", project / "requirements.txt"]
        if not (project / "src").is_dir() or not list((project / "src").glob("*.py")):
            errors.append(f"project has tests but no Python source: {project.relative_to(ROOT)}")
        for path in required:
            if not path.exists():
                errors.append(f"project layout missing {path.relative_to(ROOT)}")


def audit_phase1_test_strength(errors: list[str]) -> None:
    test_path = QUANT / "03-Projects" / "Capstone-AAPL" / "tests" / "test_phase1_baseline.py"
    if not test_path.exists():
        return
    text = test_path.read_text(encoding="utf-8")
    required = [
        "past_first = first.iloc[:cutoff]",
        "self.assertGreater(len(past_first), 0)",
    ]
    for marker in required:
        if marker not in text:
            errors.append(f"Phase 1 truncation test lacks non-empty guard: {marker}")


def audit_teaching_score(errors: list[str]) -> None:
    score_script = ROOT / "99-System" / "tools" / "score_quant_course.py"
    if not score_script.exists():
        errors.append(f"missing teaching score script: {score_script.relative_to(ROOT)}")
        return
    result = subprocess.run(
        [sys.executable, str(score_script), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        check=False,
    )
    if result.returncode != 0:
        output = (result.stdout + result.stderr).strip().replace("\n", " | ")
        errors.append(f"teaching score below threshold: {output}")


def audit_learning_path_contract(errors: list[str]) -> None:
    if not LEARNING_PATH.exists():
        return
    text = LEARNING_PATH.read_text(encoding="utf-8-sig")
    required = [
        "唯一学习入口",
        "![[01-Active Sprint/🚀 Active Sprint#🎯 当前指针]]",
        "## Week 0-9 必修路线",
        "## Week 9 后再选方向",
        "K01-K06",
        "PS01-PS05",
        "实作与解锁",
        "知识地图/00-每周学习执行卡",
    ]
    for marker in required:
        if marker not in text:
            errors.append(f"learning path contract missing marker: {marker}")
    for week in range(10):
        if not re.search(rf"(?m)^\|\s*\*\*{week}\*\*\s*\|", text):
            errors.append(f"learning path missing Week {week} row")

    weekly_path = QUANT / "知识地图" / "00-每周学习执行卡.md"
    if weekly_path.exists():
        weekly_text = weekly_path.read_text(encoding="utf-8-sig")
        for week in range(10):
            if not re.search(rf"(?m)^##\s+Week\s+{week}\b", weekly_text):
                errors.append(f"weekly execution card missing Week {week}")
        if len(re.findall(r"(?m)^### 当周练习$", weekly_text)) != 10:
            errors.append("weekly execution card must contain 10 exercise sections")
        if len(re.findall(r"(?m)^### 通过闸门$", weekly_text)) != 10:
            errors.append("weekly execution card must contain 10 mastery-gate sections")

    navigation_notes = [
        QUANT / "01-夯实基础" / "收益率与对数收益率.md",
        QUANT / "01-夯实基础" / "OHLCV字段清洗与复权.md",
        QUANT / "01-夯实基础" / "时间索引与频率（量化）.md",
        QUANT / "01-夯实基础" / "Pandas分组聚合与透视表.md",
        QUANT / "01-夯实基础" / "滚动窗口与波动率特征.md",
        QUANT / "02-量化核心技能" / "样本泄漏.md",
        QUANT / "02-量化核心技能" / "CAPM 资本资产定价模型.md",
        QUANT / "02-量化核心技能" / "量化金融-波动率-GARCH家族模型.md",
        QUANT / "02-量化核心技能" / "参数法VaR（方差-协方差法）.md",
        BLACK_SCHOLES_PAGE,
        QUANT / "02-量化核心技能" / "树模型基线.md",
    ]
    for path in navigation_notes:
        if path.exists() and "主线导航" not in path.read_text(encoding="utf-8-sig"):
            errors.append(f"core note missing main-path navigation: {path.relative_to(ROOT)}")

    active_sprint = ROOT / "01-Active Sprint" / "🚀 Active Sprint.md"
    canonical_link = "02-Knowledge/🧠 学习系统/03-量化金融/🗺️ 量化金融学习路径"
    if not active_sprint.exists() or canonical_link not in active_sprint.read_text(encoding="utf-8-sig"):
        errors.append("Active Sprint does not point to the canonical quant learning path")

    legacy_target = "03-量化金融/🗺️ 学习路径"
    active_roots = [ROOT / "01-Active Sprint", ROOT / "02-Knowledge", ROOT / "03-Projects"]
    for active_root in active_roots:
        for path in active_root.rglob("*.md"):
            try:
                text = path.read_text(encoding="utf-8-sig")
            except FileNotFoundError:
                continue
            if legacy_target in text:
                errors.append(f"legacy quant learning-path target remains in {path.relative_to(ROOT)}")
                return


def main() -> int:
    errors: list[str] = []
    all_md = markdown_files()
    for path in OFFICIAL_PAGES + PROJECT_FILES:
        if not path.exists():
            errors.append(f"missing required course asset: {path.relative_to(ROOT)}")

    audit_python_blocks(errors)
    audit_table_wikilink_escaping(errors)
    audit_official_links(errors, all_md)
    audit_black_scholes_anchor(errors)
    audit_machine_bound_paths(errors)
    audit_project_layout(errors)
    audit_project_tests(errors)
    audit_phase1_test_strength(errors)
    audit_teaching_score(errors)
    audit_learning_path_contract(errors)
    link_warnings = unresolved_course_links(all_md)
    if link_warnings:
        preview = " | ".join(link_warnings[:5])
        errors.append(
            f"unresolved course links must be zero; found {len(link_warnings)}: {preview}"
        )

    for path in OFFICIAL_PAGES:
        if not path.exists():
            continue
        text = strip_code_blocks(path.read_text(encoding="utf-8-sig"))
        h1_count = len(re.findall(r"(?m)^#\s+", text))
        if h1_count != 1:
            errors.append(f"official page must contain exactly one H1: {path.relative_to(ROOT)}")

    if errors:
        print(f"Quant course quality gate failed with {len(errors)} issue(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Quant course quality gate passed: required assets, project tests, official links, "
        "all course links, table wikilink escaping, Python syntax, H1 structure, machine paths, "
        "Black-Scholes anchor, and teaching score are valid."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
