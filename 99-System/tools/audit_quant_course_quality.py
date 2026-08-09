#!/usr/bin/env python3
"""Contract audit for the reconstructed quantitative-finance course."""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError:  # pragma: no cover - the local runtime includes PyYAML
    yaml = None


ROOT = Path(__file__).resolve().parents[2]
COURSE = ROOT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"
PROJECT = ROOT / "03-Projects" / "金融与时序" / "03-量化金融"
STAGES = ["00-前置知识", "01-夯实基础", "02-量化核心技能", "03-研究验证与稳健性", "04-深入精通"]
ASSIGNMENT_TIERS = ["课后作业", "阶段作业", "大作业"]
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
LEGACY_TERMS = ("李宏毅式", "李宏毅-CMU模式", "4-Tier", "Boss Baseline", "阶梯作业", "[支线任务]")
RESIDUE_TERMS = LEGACY_TERMS + (
    "## 13. 给 Obsidian 的归档建议",
    "请帮我建立知识网络",
    "注意：不要只列链接",
    "刷怪通关",
    "专题实战任务",
    "7.5 实战模块",
)
MARKETING_TERMS = ("先判断它值不值得深挖", "终极", "天花板", "镇山之宝", "真金白银", "梭哈")
MARKETING_TERMS += (
    "A+ 类", "A 类", "S 类", "大错特错", "懂编程的韭菜", "绝对基石", "唯一经过严格数学证明",
    "印钞机", "拍脑袋", "稳如老狗", "唯一绝对", "绝对正确", "降维打击", "致命毒药",
    "生死红线", "唯一严谨", "暴力计算法", "顶级投行", "原地翻倍", "杀手锏", "无风险赚",
    "保命符", "只有傻瓜", "亏光所有本金", "量化界的圣杯", "世界首富的密码", "实盘直接破产",
    "回测圣杯", "首要元凶", "立刻爆仓", "工业界极其常用",
    "唯一基础", "绝对看不懂", "量化名人堂", "市场实践厮杀出来",
)
HTTP_URL_RE = re.compile(r"^https?://[^\s。]+$")
TRUE_STARTS = {
    "量化金融-先修诊断与分流",
}
STAGE_ASSIGNMENT_LINKS = {
    "01-夯实基础": "QF-ST01",
    "02-量化核心技能": "QF-ST02",
    "03-研究验证与稳健性": "QF-ST03",
    "04-深入精通": "QF-ST04",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def frontmatter(text: str) -> dict:
    if not text.startswith("---") or text.count("---") < 2:
        return {}
    raw = text.split("---", 2)[1]
    if yaml is None:
        return {line.split(":", 1)[0].strip(): line.split(":", 1)[1].strip() for line in raw.splitlines() if ":" in line}
    try:
        value = yaml.safe_load(raw)
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


def formal_cards() -> list[Path]:
    cards: list[Path] = []
    for stage in STAGES:
        for path in (COURSE / stage).glob("*.md"):
            if not path.name.startswith("🧭") and frontmatter(read(path)).get("type") == "study":
                cards.append(path)
    return cards


def assignment_specs() -> list[Path]:
    return [path for tier in ASSIGNMENT_TIERS for path in (PROJECT / tier).glob("*.md")]


def core_study_card_names() -> set[str]:
    """Resolve numbered stage-MOC entries and keep only canonical study cards."""
    by_stem = {path.stem: path for path in COURSE.rglob("*.md") if ".归档" not in path.parts}
    names: set[str] = set()
    for stage in STAGES:
        mocs = list((COURSE / stage).glob("🧭*.md"))
        if len(mocs) != 1:
            continue
        for raw in re.findall(r"^\d+\. \[\[([^\]|]+)", read(mocs[0]), re.MULTILINE):
            name = Path(raw).name
            path = by_stem.get(name)
            if path is not None and frontmatter(read(path)).get("type") == "study":
                names.add(name)
    return names


def clean_link(raw: str) -> str:
    return raw.replace("\\|", "|").split("|", 1)[0].split("#", 1)[0].strip()


def collect_targets(paths: list[Path]) -> tuple[set[str], set[str]]:
    stems = {path.stem for path in paths}
    aliases: set[str] = set()
    for path in paths:
        value = frontmatter(read(path)).get("aliases", [])
        if isinstance(value, str):
            aliases.add(value)
        elif isinstance(value, list):
            aliases.update(str(item) for item in value)
    return stems, aliases


def link_resolves(source: Path, raw: str, all_md: list[Path], stems: set[str], aliases: set[str]) -> bool:
    target = clean_link(raw)
    if not target or target.startswith("http") or "${" in target or "<%" in target:
        return True
    candidate = Path(*target.replace("\\", "/").split("/"))
    if candidate.suffix.lower() != ".md":
        candidate = candidate.with_suffix(".md")
    if (source.parent / candidate).exists() or (ROOT / candidate).exists():
        return True
    return "/" not in target and (Path(target).stem in stems or target in aliases)


def main() -> int:
    errors: list[str] = []
    if not COURSE.exists() or not PROJECT.exists():
        print("course/project roots are missing")
        return 1

    scoped_roots = [COURSE, PROJECT, ROOT / "02-Knowledge" / "MOC"]
    all_md = [
        path
        for scoped_root in scoped_roots
        for path in scoped_root.rglob("*.md")
        if ".recovery-hold" not in path.parts and ".归档" not in path.parts
    ]
    formal = formal_cards()
    stems, aliases = collect_targets(all_md)

    active_course_files = [
        path for path in COURSE.rglob("*.md")
        if ".归档" not in path.parts and ".recovery-hold" not in path.parts
    ]
    for path in active_course_files:
        body = read(path)
        for term in RESIDUE_TERMS:
            if term in body:
                errors.append(f"legacy/template residue {term!r}: {path.relative_to(ROOT)}")
        if re.search(r"\bHW\d+\b", body, re.IGNORECASE):
            errors.append(f"active course page retains legacy HW identity: {path.relative_to(ROOT)}")
        if "\\n\\n" in body:
            errors.append(f"active course page contains escaped newline residue: {path.relative_to(ROOT)}")

    root_md = list(COURSE.glob("*.md"))
    if {path.name for path in root_md} != {"🗺️ 量化金融学习路径.md", "📚 教材挂载索引.md"}:
        errors.append("course root must contain only the learning path and source index")
    if (COURSE / "知识地图").exists():
        errors.append("duplicate navigation directory remains: 知识地图")

    route_text = read(COURSE / "🗺️ 量化金融学习路径.md")
    if "正式路线为 16 周" not in route_text:
        errors.append("learning path must state the delivered 16-week route")
    for unsupported_scope in ("16+4", "第 17–20 周", "4 周进阶"):
        if unsupported_scope in route_text:
            errors.append(f"learning path still advertises undelivered scope: {unsupported_scope}")
    if not (COURSE / "04-深入精通" / "🧭 阶段4-微观结构与执行.md").is_file():
        errors.append("canonical stage-4 MOC is missing")

    for stage in STAGES:
        directory = COURSE / stage
        mocs = list(directory.glob("🧭*.md"))
        if len(mocs) != 1:
            errors.append(f"{stage} must contain exactly one stage MOC")
            continue
        moc_text = read(mocs[0])
        if "## 阶段验收与作业" not in moc_text:
            errors.append(f"{mocs[0].relative_to(ROOT)} missing stage assessment")
        if "## 核心学习顺序" not in moc_text and "## 核心学习顺序（第 14–16 周）" not in moc_text:
            errors.append(f"{mocs[0].relative_to(ROOT)} missing ordered core list")
        assignment_id = STAGE_ASSIGNMENT_LINKS.get(stage)
        if assignment_id and not re.search(rf"\[\[[^\]]+\|{assignment_id}(?:\s|\])", moc_text):
            errors.append(f"{mocs[0].relative_to(ROOT)} lacks clickable {assignment_id} entry")

    required_study_fields = ("type", "topic", "course", "status", "stage_moc", "flow", "kind", "assessment_exempt")
    for path in formal:
        text = read(path)
        fm = frontmatter(text)
        missing = [field for field in required_study_fields if field not in fm]
        if missing:
            errors.append(f"{path.relative_to(ROOT)} missing fields: {', '.join(missing)}")
        if fm.get("type") != "study" or fm.get("assessment_exempt") is True:
            errors.append(f"formal study card has invalid type/exemption: {path.relative_to(ROOT)}")
        source_url = str(fm.get("source_url", "")).strip()
        if not source_url or source_url == "[待验证]":
            errors.append(f"formal study card missing verified source_url: {path.relative_to(ROOT)}")
        elif source_url.startswith(("http://", "https://")):
            if not HTTP_URL_RE.fullmatch(source_url):
                errors.append(f"formal study card source_url is not a pure URL: {path.relative_to(ROOT)}")
        elif not (ROOT / source_url).is_file():
            errors.append(f"formal study card local source_url does not exist: {path.relative_to(ROOT)}")
        if "[待验证]" in str(fm.get("source", "")):
            errors.append(f"formal study card source remains unverified: {path.relative_to(ROOT)}")
        upstream = fm.get("upstream", [])
        upstream = [upstream] if isinstance(upstream, str) else upstream
        if not upstream and path.stem not in TRUE_STARTS:
            errors.append(f"non-start study card lacks upstream: {path.relative_to(ROOT)}")
        current_names = {path.stem}
        aliases_value = fm.get("aliases", [])
        if isinstance(aliases_value, str):
            current_names.add(aliases_value)
        elif isinstance(aliases_value, list):
            current_names.update(str(item) for item in aliases_value)
        for raw in upstream or []:
            target = clean_link(str(raw).strip("[]"))
            if Path(target).stem in current_names:
                errors.append(f"self-referential upstream: {path.relative_to(ROOT)} -> {target}")
        if "downstream:" in text:
            errors.append(f"static downstream field remains: {path.relative_to(ROOT)}")
        if re.search(r"(?m)^(?:#{1,6}\s*)?(?:上游依赖|下游延伸)\s*$", text):
            errors.append(f"static relationship section remains: {path.relative_to(ROOT)}")
        if re.search(r"(?:上一张|下一张|Capstone-AAPL|(?:\*\*|\|)Week\s*\d)", text, re.IGNORECASE):
            errors.append(f"stale card-level sequence or capstone identity remains: {path.relative_to(ROOT)}")
        if len(re.findall(r"^## 0\.", text, re.MULTILINE)) > 1 or "<!-- 自动合并自：" in text:
            errors.append(f"duplicated merged teaching body remains: {path.relative_to(ROOT)}")
        if "## 学完后可以完成" not in text:
            errors.append(f"formal study card missing derived assessment block: {path.relative_to(ROOT)}")
        if any(term in text for term in MARKETING_TERMS):
            errors.append(f"template/marketing wording remains: {path.relative_to(ROOT)}")
        link_text = FENCED_CODE_RE.sub("", text)
        for raw in WIKILINK_RE.findall(link_text):
            if not link_resolves(path, raw, all_md, stems, aliases):
                errors.append(f"broken link: {path.relative_to(ROOT)} -> {clean_link(raw)}")

    specs = assignment_specs()
    expected_ids = {*(f"QF-L{i:02d}" for i in range(1, 10)), *(f"QF-ST{i:02d}" for i in range(1, 5)), "QF-CAPSTONE-QLIB"}
    actual_ids = set()
    assessed_names: set[str] = set()
    detail_blocks: list[str] = []
    for path in specs:
        fm = frontmatter(read(path))
        spec_text = read(path)
        actual_ids.add(str(fm.get("assignment_id", "")))
        requires = fm.get("requires", [])
        requires = [requires] if isinstance(requires, str) else requires
        for raw in requires or []:
            match = WIKILINK_RE.fullmatch(str(raw))
            if match:
                assessed_names.add(Path(clean_link(match.group(1))).name)
        for field in ("type", "project_type", "course", "assignment_id", "assignment_level", "assignment_format", "stage_id", "requires", "source_type", "source_url", "license"):
            if field not in fm:
                errors.append(f"assignment missing {field}: {path.relative_to(ROOT)}")
        detail_match = re.search(r"^## 题目细化\s*$\n(?P<body>.*?)(?=^## |\Z)", spec_text, re.MULTILINE | re.DOTALL)
        task_pattern = r"^(?:[-*]\s+[QS]1\b|###\s+[QS]1(?:\s|$))"
        if not detail_match or not re.search(task_pattern, detail_match.group("body"), re.MULTILINE):
            errors.append(f"assignment lacks numbered specific tasks: {path.relative_to(ROOT)}")
        else:
            detail_blocks.append(detail_match.group("body").strip())
        if fm.get("assignment_level") == "lesson":
            for field in (
                "source_locator", "official_assignment_url", "official_assignment_scope", "accessed",
                "answer_policy", "estimated_hours", "fixture_path",
            ):
                if field not in fm:
                    errors.append(f"lesson assignment missing {field}: {path.relative_to(ROOT)}")
            if fm.get("source_type") != "local_integration_task":
                errors.append(f"lesson assignment must disclose local integration identity: {path.relative_to(ROOT)}")
            if "starter_path" in fm:
                errors.append(f"lesson assignment retains conflicting starter_path: {path.relative_to(ROOT)}")
            hours = re.fullmatch(r"(\d+)-(\d+)", str(fm.get("estimated_hours", "")))
            if not hours or int(hours.group(2)) > 5:
                errors.append(f"lesson assignment exceeds five-hour scope: {path.relative_to(ROOT)}")
            for heading in ("固定输入", "公开验收断言", "失败诊断", "官方原题加练", "来源与答案边界"):
                if not re.search(rf"^## {heading}\s*$", spec_text, re.MULTILINE):
                    errors.append(f"lesson assignment missing {heading}: {path.relative_to(ROOT)}")
            if detail_match:
                lesson_tasks = re.findall(r"^###\s+Q([1-4])(?:\s|$)", detail_match.group("body"), re.MULTILINE)
                if lesson_tasks != ["1", "2", "3", "4"]:
                    errors.append(f"lesson assignment must define ordered Q1-Q4: {path.relative_to(ROOT)}")
                for term in ("投影矩阵", "Cook 距离", "转移矩阵", "指数分布", "PCA", "Vasicek"):
                    if term in detail_match.group("body"):
                        errors.append(f"lesson assignment contains hidden prerequisite {term}: {path.relative_to(ROOT)}")
            if re.search(r"\bHW\d+\b", spec_text, re.IGNORECASE):
                errors.append(f"lesson assignment retains legacy HW identity: {path.relative_to(ROOT)}")
        for raw in re.findall(r"\[\[([^\]]+)\]\]", spec_text):
            if not link_resolves(path, raw, all_md, stems, aliases):
                errors.append(f"broken assignment link: {path.relative_to(ROOT)} -> {clean_link(raw)}")
    if actual_ids != expected_ids:
        errors.append(f"assignment IDs do not match canonical set: {sorted(actual_ids)}")
    if len(detail_blocks) != len(set(detail_blocks)):
        errors.append("assignment detail blocks contain duplicated templates")
    core_names = core_study_card_names()
    if len(core_names) != 43:
        errors.append(f"expected 43 core study cards from stage MOCs, found {len(core_names)}")
    missing_assessment = sorted(core_names - assessed_names)
    if missing_assessment:
        errors.append(f"core study cards without canonical assignment coverage: {missing_assessment}")
    if (PROJECT / "real_assignment_packages").exists():
        errors.append("second assignment source remains: real_assignment_packages")
    if not (PROJECT / "Qlib因子研究" / "environment-qlib.yml").is_file():
        errors.append("Qlib capstone environment lock is missing")

    package_root = PROJECT / "scripts" / "assignments"
    manifests = sorted(package_root.rglob("package_manifest.json"))
    expected_package_ids = {
        "QF-ST01-BASELINE", "QF-ST02-EVT", "QF-ST03-BARS", "QF-ST03-HRP",
        "QF-ST03-RMT", "QF-ST03-PBO", "QF-ST04-AC", "QF-ST04-QUEUE",
        "QF-CAPSTONE-QLIB",
    }
    package_ids: set[str] = set()
    with tempfile.TemporaryDirectory(prefix="quant-course-audit-") as output_root:
        for manifest_path in manifests:
            try:
                manifest = json.loads(read(manifest_path))
            except (json.JSONDecodeError, OSError) as exc:
                errors.append(f"invalid package manifest {manifest_path.relative_to(ROOT)}: {exc}")
                continue
            package_id = str(manifest.get("id", ""))
            package_ids.add(package_id)
            if re.search(r"\bhw\d+\b", str(manifest_path), re.IGNORECASE):
                errors.append(f"active package path retains legacy HW identity: {manifest_path.relative_to(ROOT)}")
            smoke_dir = PROJECT / str(manifest.get("smoke_data_dir", ""))
            runner = manifest_path.parent / "starter" / "run.py"
            if not smoke_dir.is_dir() or not runner.is_file():
                errors.append(f"package lacks smoke data or runner: {manifest_path.relative_to(ROOT)}")
                continue
            missing_files = [name for name in manifest.get("real_files", []) if not (smoke_dir / name).is_file()]
            if missing_files:
                errors.append(f"package smoke fixture incomplete {package_id}: {missing_files}")
                continue
            completed = subprocess.run(
                [
                    sys.executable, str(runner), "--input-dir", str(smoke_dir),
                    "--output-dir", str(Path(output_root) / str(manifest.get("slug", package_id))),
                ],
                cwd=runner.parent,
                text=True,
                capture_output=True,
                check=False,
                timeout=120,
            )
            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout).strip().splitlines()[-1:]
                errors.append(f"package runner failed {package_id}: {' '.join(detail)}")
                continue
            summary_path = Path(output_root) / str(manifest.get("slug", package_id)) / "results" / "summary.json"
            if not summary_path.is_file():
                errors.append(f"package runner produced no summary: {package_id}")
                continue
            summary = json.loads(read(summary_path))
            if package_id == "QF-CAPSTONE-QLIB":
                contract = summary.get("contract_summary", {})
                if contract.get("contract_status") != "contract_template_ready":
                    errors.append("Qlib template preflight did not reach contract_template_ready")
                if contract.get("provider_status") != "placeholder":
                    errors.append("Qlib smoke must disclose its placeholder provider")
                if contract.get("qlib_execution_status") != "blocked_on_provider" or contract.get("qlib_execution_passed") is not False:
                    errors.append("Qlib contract preflight falsely claims a Qlib execution pass")
    if package_ids != expected_package_ids:
        errors.append(f"active package IDs do not match canonical set: {sorted(package_ids)}")

    for path in (COURSE / "🗺️ 量化金融学习路径.md", COURSE / "📚 教材挂载索引.md", PROJECT / "🧭 课程作业总索引.md"):
        if not path.exists():
            errors.append(f"missing canonical page: {path.relative_to(ROOT)}")

    for path in (ROOT / "02-Knowledge" / "MOC" / "开放教材主线注册表.md", ROOT / "02-Knowledge" / "MOC" / "📚 33门课程教材与作业挂载总地图.md"):
        if path.exists() and "量化金融" not in read(path):
            errors.append(f"global registry lost quant-finance entry: {path.relative_to(ROOT)}")

    for path in (ROOT / "03-Projects" / "金融与时序" / "03-量化金融" / "scripts").rglob("*.py") if (PROJECT / "scripts").exists() else []:
        try:
            ast.parse(read(path), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"invalid Python support script {path.relative_to(ROOT)}: {exc.msg}")

    if errors:
        print(f"Quant course quality gate failed with {len(errors)} issue(s):")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "Quant course quality gate passed: "
        f"{len(formal)} formal study cards, {len(specs)} canonical assignments, "
        f"{len(manifests)} executable packages, sources, links, and route contracts are valid."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
