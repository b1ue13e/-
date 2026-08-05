"""Audit the 33 formal course execution routes in the Obsidian vault."""

from __future__ import annotations

import re
import sys
import os
from difflib import SequenceMatcher
from pathlib import Path

import yaml


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
COURSES = {
    "01-社交网络挖掘": "🗺️ 社交网络挖掘学习路径.md",
    "02-时间序列分析": "🗺️ 时间序列分析学习路径.md",
    "03-量化金融": "🗺️ 量化金融学习路径.md",
    "04-离散数学": "🗺️ 离散数学学习路径.md",
    "05-计算机视觉": "🗺️ 计算机视觉学习路径.md",
    "06-常微分方程": "🗺️ 常微分方程学习路径.md",
    "07-最优化方法": "🗺️ 最优化方法学习路径.md",
    "08-NLP全栈": "🗺️ NLP全栈学习路径.md",
    "09-高等代数": "🗺️ 高等代数学习路径.md",
    "10-数据结构与算法": "🗺️ 数据结构与算法学习路径.md",
    "11-计算机组成原理": "🗺️ 计算机组成原理学习路径.md",
    "12-信号与系统": "🗺️ 信号与系统学习路径.md",
    "13-强化学习": "🗺️ 强化学习学习路径.md",
    "14-概率图模型": "🗺️ 概率图模型学习路径.md",
    "15-控制与机器人学": "🗺️ 控制与机器人学学习路径.md",
    "16-多元统计": "🗺️ 多元统计学习路径.md",
    "17-机器学习": "🗺️ 机器学习学习路径.md",
    "22-概率论与数理统计": "🗺️ 概率论与数理统计学习路径.md",
    "23-图神经网络": "🗺️ 图神经网络学习路径.md",
    "24-随机过程": "🗺️ 随机过程学习路径.md",
    "25-测度论": "🗺️ 测度论学习路径.md",
    "26-实变函数": "🗺️ 实变函数学习路径.md",
    "27-泛函分析": "🗺️ 泛函分析学习路径.md",
    "28-数学分析": "🗺️ 数学分析学习路径.md",
    "29-运筹学": "🗺️ 运筹学学习路径.md",
    "30-应用回归分析": "🗺️ 应用回归分析学习路径.md",
    "31-属性数据分析": "🗺️ 属性数据分析学习路径.md",
    "32-非参数统计": "🗺️ 非参数统计学习路径.md",
    "33-贝叶斯统计": "🗺️ 贝叶斯统计学习路径.md",
    "34-偏微分方程": "🗺️ 偏微分方程学习路径.md",
    "35-数值分析": "🗺️ 数值分析学习路径.md",
    "36-数据挖掘与信息检索": "🗺️ 数据挖掘与信息检索学习路径.md",
    "37-复变函数": "🗺️ 复变函数学习路径.md",
}
EXPECTED_SPINES = {
    "01-社交网络挖掘": "https://web.stanford.edu/class/cs224w/",
    "02-时间序列分析": "https://online.stat.psu.edu/stat510/",
    "03-量化金融": "https://lucylabs.gatech.edu/ml4t/",
    "04-离散数学": "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/",
    "05-计算机视觉": "https://cs231n.stanford.edu/2025/assignments.html",
    "06-常微分方程": "https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/assignments/",
    "07-最优化方法": "https://see.stanford.edu/Course/EE364A",
    "08-NLP全栈": "https://web.stanford.edu/class/cs224n/",
    "09-高等代数": "https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/",
    "10-数据结构与算法": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
    "11-计算机组成原理": "https://www.nand2tetris.org/",
    "12-信号与系统": "https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/",
    "13-强化学习": "https://inst.eecs.berkeley.edu/~cs188/su25/projects/",
    "14-概率图模型": "https://cs.stanford.edu/~ermon/cs228/index.html",
    "15-控制与机器人学": "https://github.com/NxRLab/ModernRobotics",
    "16-多元统计": "https://online.stat.psu.edu/stat505/",
    "17-机器学习": "https://github.com/ga642381/ML2021-Spring",
    "22-概率论与数理统计": "https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/",
    "23-图神经网络": "https://web.stanford.edu/class/cs224w/",
    "24-随机过程": "https://ocw.mit.edu/courses/6-011-signals-systems-and-inference-spring-2018/resources/assignments/",
    "25-测度论": "https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/pages/lecture-notes-and-readings/",
    "26-实变函数": "https://ocw.mit.edu/courses/18-100c-real-analysis-fall-2012/pages/assignments/",
    "27-泛函分析": "https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2009/pages/assignments/",
    "28-数学分析": "https://ocw.mit.edu/courses/18-100a-real-analysis-fall-2020/",
    "29-运筹学": "https://ocw.mit.edu/courses/15-053-optimization-methods-in-management-science-spring-2013/pages/assignments/",
    "30-应用回归分析": "https://online.stat.psu.edu/stat462/",
    "31-属性数据分析": "https://online.stat.psu.edu/stat504/",
    "32-非参数统计": "https://online.stat.psu.edu/stat415/",
    "33-贝叶斯统计": "https://github.com/rmcelreath/stat_rethinking_2024",
    "34-偏微分方程": "https://ocw.mit.edu/courses/18-152-introduction-to-partial-differential-equations-fall-2005/pages/assignments/",
    "35-数值分析": "https://ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/resources/problem-sets/",
    "36-数据挖掘与信息检索": "https://web.stanford.edu/class/cs246/",
    "37-复变函数": "https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/resources/problem-set-solutions/",
}
REQUIRED_SUPPORT_URLS = {
    "01-社交网络挖掘": ["https://github.com/networkx/networkx"],
    "02-时间序列分析": ["https://github.com/statsmodels/statsmodels"],
    "03-量化金融": [
        "https://github.com/microsoft/qlib",
        "https://github.com/AI4Finance-Foundation/FinRL",
        "https://quantecon.org/",
    ],
    "05-计算机视觉": ["https://github.com/d2l-ai/d2l-en"],
    "07-最优化方法": ["https://www.cvxpy.org/examples/"],
    "08-NLP全栈": ["https://github.com/huggingface/course"],
    "10-数据结构与算法": ["https://github.com/OpenDSA/OpenDSA"],
    "13-强化学习": [
        "https://rail.eecs.berkeley.edu/deeprlcourse-fa23/",
        "https://github.com/openai/spinningup",
    ],
    "14-概率图模型": ["https://github.com/pgmpy/pgmpy"],
    "15-控制与机器人学": [
        "https://github.com/python-control/python-control",
        "https://github.com/AtsushiSakai/PythonRobotics",
    ],
    "16-多元统计": ["https://github.com/intro-stat-learning/ISLP_labs"],
    "17-机器学习": ["https://speech.ee.ntu.edu.tw/~hylee/ml/2023-spring.php"],
    "22-概率论与数理统计": ["https://github.com/AllenDowney/ThinkStats2"],
    "23-图神经网络": ["https://github.com/pyg-team/pytorch_geometric"],
    "24-随机过程": ["https://github.com/QuantEcon/lecture-python.myst"],
    "25-测度论": ["https://measure.axler.net/"],
    "26-实变函数": ["https://github.com/jirilebl/ra"],
    "29-运筹学": ["https://github.com/google/or-tools"],
    "30-应用回归分析": ["https://github.com/intro-stat-learning/ISLP_labs"],
    "31-属性数据分析": ["https://github.com/friendly/psy6136"],
    "32-非参数统计": ["https://github.com/OpenIntroStat/ims"],
    "33-贝叶斯统计": ["https://github.com/pymc-devs/pymc-examples"],
    "34-偏微分方程": ["https://github.com/iitrabhi/fenics-workshop"],
    "36-数据挖掘与信息检索": [
        "https://web.stanford.edu/class/cs276/",
        "https://github.com/castorini/pyserini",
    ],
    "37-复变函数": ["https://github.com/complex-analysis/complex-analysis.github.io"],
}
STUDY_ROOT = ROOT / "02-Knowledge" / "🧠 学习系统"
EXECUTION_HEADING = "## 🧭 开源自学执行方案"
REQUIRED_TERMS = ("Spine", "Lab", "Capstone", "Rubric", "许可证", "镜像", "失败")
FORBIDDEN_PATTERNS = {
    "placeholder": re.compile(r"\b(?:TODO|XXX|TBD)\b|待补(?:充|写)", re.I),
    "universal-sharpe": re.compile(r"(?:Sharpe|夏普)[^\n]{0,40}(?:>|≥)\s*\d", re.I),
    "universal-pbo": re.compile(r"PBO[^\n]{0,30}(?:<|≤)\s*(?:0\.1|10\s*%)", re.I),
}


def frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError("missing frontmatter")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError("unterminated frontmatter")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data, text


def main() -> int:
    errors: list[str] = []
    rows: list[tuple[str, str]] = []
    execution_sections: dict[str, str] = {}
    course_statuses: dict[str, str] = {}

    if len(COURSES) != 33:
        errors.append(f"course manifest has {len(COURSES)} entries instead of 33")
    if set(EXPECTED_SPINES) != set(COURSES):
        errors.append("expected Spine manifest does not match the 33-course manifest")

    central_path = ROOT / "02-Knowledge" / "MOC" / "33门课程开源自学与验收总索引.md"
    try:
        central_data, central_text = frontmatter(central_path)
        for key, expected in {
            "type": "index",
            "kind": "moc",
            "flow": "knowledge",
            "status": "active",
        }.items():
            if central_data.get(key) != expected:
                errors.append(f"central MOC: {key} != {expected}")
    except Exception as exc:
        central_text = ""
        errors.append(f"central MOC: {exc}")

    governance_files = {
        "source audit": ROOT / "03-Projects" / "33门课程作业来源审计总表.md",
        "legacy asset audit": ROOT
        / "03-Projects"
        / "旧项目与作业资产资格审计-2026-07-28.md",
        "umbrella project": ROOT / "03-Projects" / "项目-33门课程开源作业体系升级.md",
        "project hub": ROOT / "03-Projects" / "03-🛠️ Projects.md",
        "resource hub": ROOT / "🗂️ 资源总索引.md",
        "home": ROOT / "🏠 主页.md",
        "research report": ROOT
        / "99-System"
        / "🗄️ 归档"
        / "33门课程开源自学项目调研-2026-07-27.md",
    }
    governance_texts: dict[str, str] = {}
    for label, path in governance_files.items():
        try:
            _, governance_texts[label] = frontmatter(path)
        except Exception as exc:
            errors.append(f"{label}: {exc}")
    source_rows = re.findall(
        r"(?m)^\|\s*(?:0[1-9]|1[0-7]|2[2-9]|3[0-7])\s*\|",
        governance_texts.get("source audit", ""),
    )
    if len(source_rows) != 33:
        errors.append(f"source audit contains {len(source_rows)} course rows instead of 33")
    source_audit_text = governance_texts.get("source audit", "")
    for course, expected_url in EXPECTED_SPINES.items():
        if expected_url not in source_audit_text:
            errors.append(f"source audit missing attachment-v2 Spine URL for {course}")
    if "progress: 100%" not in governance_texts.get("umbrella project", ""):
        errors.append("umbrella project is not marked 100%")
    legacy_text = governance_texts.get("legacy asset audit", "")
    for expected in ("**210**", "**1**", "**209**", "reference-only"):
        if expected not in legacy_text:
            errors.append(f"legacy asset audit missing summary marker: {expected}")
    if not (ROOT / "99-System" / "tools" / "audit_homework_assets.py").exists():
        errors.append("legacy homework eligibility audit tool is missing")

    for course, learning_name in COURSES.items():
        course_dir = STUDY_ROOT / course
        resource_path = course_dir / "📚 教材挂载索引.md"
        learning_path = course_dir / learning_name
        course_errors: list[str] = []

        for path, label in ((resource_path, "resource"), (learning_path, "learning path")):
            if not path.exists():
                course_errors.append(f"missing {label}: {path.relative_to(ROOT)}")

        if not course_errors:
            try:
                data, resource_text = frontmatter(resource_path)
                for key, expected in {
                    "type": "index",
                    "kind": "moc",
                    "flow": "knowledge",
                }.items():
                    if data.get(key) != expected:
                        course_errors.append(f"resource {key} != {expected}")
                if str(data.get("updated")) != "2026-07-28":
                    course_errors.append("resource updated != 2026-07-28")
                if data.get("status") not in {"active", "planned"}:
                    course_errors.append("resource status must be active or planned")
                else:
                    course_statuses[course] = data["status"]
                if data.get("resource_policy_version") != "attachment-v2-2026-07-28":
                    course_errors.append("resource_policy_version is not attachment-v2-2026-07-28")
                if data.get("spine_url") != EXPECTED_SPINES[course]:
                    course_errors.append(
                        f"spine_url is {data.get('spine_url')!r}, expected {EXPECTED_SPINES[course]}"
                    )
                if data.get("spine_mirror_policy") != "link-only":
                    course_errors.append("spine_mirror_policy must be link-only")

                if resource_text.count(EXECUTION_HEADING) != 1:
                    course_errors.append("execution heading count is not 1")
                    section = ""
                else:
                    section = resource_text.split(EXECUTION_HEADING, 1)[1]
                    execution_sections[course] = section
                if len(section) < 1_200:
                    course_errors.append(f"execution section is too short: {len(section)} chars")
                if "https://" not in section:
                    course_errors.append("execution section has no external source URL")
                for term in REQUIRED_TERMS:
                    if term not in section:
                        course_errors.append(f"execution section missing term: {term}")
                spine_lines = []
                for line in section.splitlines():
                    stripped = line.lstrip()
                    if re.match(r"^-\s+\*\*Spine\b", stripped):
                        spine_lines.append(line)
                    elif stripped.startswith("|"):
                        cells = [
                            cell.strip().replace("*", "")
                            for cell in stripped.strip().strip("|").split("|")
                        ]
                        if cells and cells[0] == "Spine":
                            spine_lines.append(line)
                if len(spine_lines) != 1:
                    course_errors.append(
                        f"execution section has {len(spine_lines)} Spine declarations, expected 1"
                    )
                elif EXPECTED_SPINES[course] not in spine_lines[0]:
                    course_errors.append("Spine declaration does not use the attachment-v2 URL")
                for support_url in REQUIRED_SUPPORT_URLS.get(course, []):
                    if support_url not in section:
                        course_errors.append(f"execution section missing support URL: {support_url}")
                for label, pattern in FORBIDDEN_PATTERNS.items():
                    if pattern.search(section):
                        course_errors.append(f"execution section contains {label}")

                stage_rows = []
                in_stage_table = False
                for line in section.splitlines():
                    if line.lstrip().startswith("|"):
                        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                        if cells and cells[0] in {"阶段", "层级", "阶段/层级"}:
                            in_stage_table = True
                            continue
                        if in_stage_table and not re.search(r":?-{3,}", line):
                            stage_rows.append(cells)
                    elif in_stage_table and line.strip():
                        break
                if not 3 <= len(stage_rows) <= 4:
                    course_errors.append(
                        f"stage-experiment table has {len(stage_rows)} data rows, expected 3-4"
                    )

                rubric_match = re.search(
                    r"### [^\n]*Rubric[^\n]*\n(.*?)(?=\n### |\Z)", section, re.S | re.I
                )
                if not rubric_match:
                    course_errors.append("execution section has no Rubric block")
                else:
                    scores: list[int] = []
                    for line in rubric_match.group(1).splitlines():
                        if not line.lstrip().startswith("|") or re.search(r":?-{3,}", line):
                            continue
                        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                        if len(cells) < 2:
                            continue
                        if cells[0].replace("*", "") in {"总计", "合计"}:
                            continue
                        score = re.fullmatch(r"(?:\*\*)?(\d{1,3})(?:%|分)?(?:\*\*)?", cells[1])
                        if score:
                            scores.append(int(score.group(1)))
                    if sum(scores) != 100:
                        course_errors.append(f"Rubric score sum is {sum(scores)}, expected 100")

                for evidence_term in ("最小证据", "强验证", "失败条件"):
                    if evidence_term not in section:
                        course_errors.append(f"execution section missing {evidence_term}")
            except Exception as exc:
                course_errors.append(f"resource YAML/read error: {exc}")

            try:
                _, learning_text = frontmatter(learning_path)
                expected_link = (
                    f"[[02-Knowledge/🧠 学习系统/{course}/📚 教材挂载索引"
                    f"#🧭 开源自学执行方案"
                )
                if expected_link not in learning_text:
                    course_errors.append("canonical learning path lacks explicit execution link")
            except Exception as exc:
                course_errors.append(f"learning path YAML/read error: {exc}")

            central_link = (
                f"[[02-Knowledge/🧠 学习系统/{course}/📚 教材挂载索引"
                f"#🧭 开源自学执行方案"
            )
            if central_link not in central_text:
                course_errors.append("central MOC lacks explicit execution link")

        if course_errors:
            rows.append((course, "FAIL"))
            errors.extend(f"{course}: {item}" for item in course_errors)
        else:
            rows.append((course, "PASS"))

    sprint_sources: list[Path] = []
    markdown_paths: list[Path] = []
    for current, dirs, files in os.walk(ROOT, topdown=True):
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in {".git", "deep-fill-backup", "node_modules"}
        ]
        markdown_paths.extend(
            Path(current) / name for name in files if name.lower().endswith(".md")
        )
    for path in markdown_paths:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        head = text.split("---", 2)[1] if text.startswith("---") and text.count("---") >= 2 else ""
        if re.search(r"(?m)^sprint:\s*current\s*$", head) and re.search(
            r"(?m)^source_of_truth:\s*true\s*$", head
        ):
            sprint_sources.append(path)
    if len(sprint_sources) != 1:
        errors.append(f"current source_of_truth count is {len(sprint_sources)}, expected 1")

    active_courses = [course for course, status in course_statuses.items() if status == "active"]
    planned_courses = [course for course, status in course_statuses.items() if status == "planned"]
    if active_courses != ["03-量化金融"]:
        errors.append(f"active course indexes are {active_courses}, expected only 03-量化金融")
    if len(planned_courses) != 32:
        errors.append(f"planned course index count is {len(planned_courses)}, expected 32")

    maturity_counts = {"A": 0, "B": 0, "C": 0}
    for line in central_text.splitlines():
        if not re.match(r"^\|\s*(?:0[1-9]|1[0-7]|2[2-9]|3[0-7])\s*\|", line):
            continue
        cells = [cell.strip().replace("*", "") for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[3] in maturity_counts:
            maturity_counts[cells[3]] += 1
    if maturity_counts != {"A": 27, "B": 5, "C": 1}:
        errors.append(f"central maturity counts are {maturity_counts}, expected A27/B5/C1")

    # Attachment-v2 explicitly distinguishes ML2021's 15 official assignments
    # from the local RAG/Agent extension.
    ml_root = STUDY_ROOT / "17-机器学习"
    hw16_path = ml_root / "李宏毅课程与作业" / "HW16-GenAI-RAG与Agent大模型实战.md"
    try:
        hw16_data, hw16_text = frontmatter(hw16_path)
        if hw16_data.get("adaptation") != "original":
            errors.append("ML local extension adaptation must be original")
        if hw16_data.get("official_homework") is not False:
            errors.append("ML local extension official_homework must be false")
        if "不是 ML2021 官方作业" not in hw16_text:
            errors.append("ML local extension lacks explicit non-official disclosure")
    except Exception as exc:
        errors.append(f"ML local extension: {exc}")
    for name in (
        "🎓 李宏毅机器学习与生成式AI全套课程与作业解构.md",
        "🎯 机器学习阶段解锁与作业通关路线图.md",
    ):
        try:
            text = (ml_root / name).read_text(encoding="utf-8")
            if "15 个" not in text or "本地扩展" not in text:
                errors.append(f"{name}: missing 15-official plus local-extension boundary")
        except OSError as exc:
            errors.append(f"{name}: {exc}")

    # Old quant templates must not reintroduce context-free universal pass lines.
    quant_root = STUDY_ROOT / "03-量化金融"
    forbidden_quant_phrases = (
        "扣除交易摩擦与滑点后，样本外 (OOS) 夏普比率 $> 1.8$ 或评估指标提升 20% 以上",
        "实盘级抗过拟合能力，过拟合概率 $\\text{PBO} < 10\\%$",
        "通过 PBO 审计且过拟合概率 $\\text{PBO} < 10\\%$",
        "实现 OOS Sharpe $> 2.2$ 且最大撤回 $< 12\\%$",
        "只有当 $PBO < 0.10$（即过拟合概率低于 10%）",
        "通常 Sharpe > 1 被认为可接受",
        "通常 $S > 1$ 较好",
    )
    for path in quant_root.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for phrase in forbidden_quant_phrases:
            if phrase in text:
                errors.append(
                    f"quant universal threshold remains: {path.relative_to(ROOT).as_posix()}"
                )

    courses_with_sections = sorted(execution_sections)
    max_similarity = (None, None, 0.0)
    for index, left in enumerate(courses_with_sections):
        for right in courses_with_sections[index + 1 :]:
            ratio = SequenceMatcher(
                None, execution_sections[left], execution_sections[right]
            ).ratio()
            if ratio > max_similarity[2]:
                max_similarity = (left, right, ratio)
            if ratio >= 0.88:
                errors.append(
                    f"execution sections may be templated duplicates: {left} vs {right} ({ratio:.3f})"
                )

    for course, status in rows:
        print(f"{status}\t{course}")
    print(f"COURSES={len(rows)}")
    if max_similarity[0] is not None:
        print(
            "MAX_SECTION_SIMILARITY="
            f"{max_similarity[2]:.3f} ({max_similarity[0]} vs {max_similarity[1]})"
        )
    print(f"SPRINT_SOURCE_OF_TRUTH={len(sprint_sources)}")
    for path in sprint_sources:
        print(f"  {path.relative_to(ROOT).as_posix()}")

    if errors:
        print("\nERRORS")
        for error in errors:
            print(f"- {error}")
        return 1
    print("\nALL_COURSE_EXECUTION_ROUTES_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
