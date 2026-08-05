#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimize the Obsidian learning system into the five-note-role structure.

Scope:
- Works inside "02-Knowledge/🧠 学习系统" plus the five root note templates.
- Does not move existing stage concept cards.
- Rewrites only legacy scaffold study cards into AI-initial concept drafts.
- Creates/updates MOC, concept-entry, derivation, problem-type, and mistake-entry pages.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import yaml


ROOT = Path("02-Knowledge/🧠 学习系统")
TODAY = date.today().isoformat()

FIVE_DIRS = ["00-MOC地图", "10-概念笔记", "20-推导笔记", "30-题型笔记", "40-错题漏洞"]
ROOT_TEMPLATES = {
    "moc": Path("🧭 MOC地图笔记模板.md"),
    "concept": Path("📓 概念笔记模板.md"),
    "derivation": Path("📐 推导笔记模板.md"),
    "problem_type": Path("📝 题型笔记模板.md"),
    "mistake": Path("🧯 错题漏洞笔记模板.md"),
}

CORE_COURSE_RE = re.compile(r"^(?:0[1-9]|1[0-7]|2[2-9]|3[0-7])-")
NUMBERED_DIR_RE = re.compile(r"^\d{2}-")
FRONTMATTER_RE = re.compile(r"^\ufeff?---\s*\n(.*?)\n---\s*\n?", re.S)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")
OLD_SCAFFOLD_RE = re.compile(
    r"## 为什么学|## 教材定位|## 必须掌握|## 关键问题|## 练习与输出|## 完成标准|## 最小例子\s*\n- 场景："
)
EMPTY_SHELL_RE = re.compile(r"^>\s*$|^-\s*$|\[\[ \]\]", re.M)
DATAVIEW_FENCE_RE = re.compile(r"```dataview(?:js)?")


def configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str, dry_run: bool, changes: Counter[str]) -> None:
    old = read_text(path) if path.exists() else None
    if old == text:
        return
    changes["files_changed"] += 1
    if old is None:
        changes["files_created"] += 1
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str, bool]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text, False
    raw = match.group(1)
    body = text[match.end() :]
    try:
        data = yaml.safe_load(raw) or {}
        if not isinstance(data, dict):
            data = {}
    except yaml.YAMLError:
        data = {}
    return data, body, True


def dump_frontmatter(data: dict[str, Any]) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False).strip()


def render_note(data: dict[str, Any], body: str) -> str:
    return f"---\n{dump_frontmatter(data)}\n---\n\n{body.strip()}\n"


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        return [stripped]
    return [str(value).strip()]


def yaml_inline_list(items: list[str]) -> str:
    return "[" + ", ".join(str(i) for i in items) + "]"


def course_name(course_dir: Path) -> str:
    return course_dir.name.split("-", 1)[1] if "-" in course_dir.name else course_dir.name


def clean_title(value: str) -> str:
    value = Path(value).stem
    value = re.sub(r"^[^\w\u4e00-\u9fff]+", "", value).strip()
    return value or "未命名"


def display_title_from_meta(path: Path, fm: dict[str, Any], body: str = "") -> str:
    raw = str(fm.get("topic") or "")
    if not raw:
        heading = HEADING_RE.search(body)
        raw = heading.group(2) if heading else path.stem
    raw = clean_title(raw)
    parts = [p.strip() for p in raw.split("-") if p.strip()]
    if len(parts) >= 3:
        return parts[-1]
    return raw


def safe_filename(name: str, suffix: str = ".md") -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\n\r\t]', "-", name).strip().strip(".")
    cleaned = re.sub(r"\s+", " ", cleaned)
    if len(cleaned) > 80:
        cleaned = cleaned[:80].rstrip()
    return (cleaned or "未命名") + suffix


def wiki(name: str) -> str:
    return f"[[{Path(name).stem}]]"


def find_markdown(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if p.is_file())


def find_course_dirs(core_only: bool = False) -> list[Path]:
    dirs = [p for p in ROOT.iterdir() if p.is_dir() and NUMBERED_DIR_RE.match(p.name)]
    if core_only:
        dirs = [p for p in dirs if CORE_COURSE_RE.match(p.name)]
    return sorted(dirs, key=lambda p: p.name)


def find_stage_heading(stage_dir: Path) -> str:
    stage_files = []
    for path in sorted(stage_dir.glob("*.md")):
        fm, body, _ = parse_frontmatter(read_text(path))
        if fm.get("type") == "stage":
            stage_files.append((path, body))
    if stage_files:
        heading = HEADING_RE.search(stage_files[0][1])
        if heading:
            return clean_title(heading.group(2))
    return clean_title(stage_dir.name.split("-", 1)[1] if "-" in stage_dir.name else stage_dir.name)


def stage_heading_by_dir(course_dir: Path) -> dict[Path, str]:
    result: dict[Path, str] = {}
    for child in sorted(course_dir.iterdir()):
        if child.is_dir() and NUMBERED_DIR_RE.match(child.name):
            result[child] = find_stage_heading(child)
    return result


def infer_stage(path: Path, fm: dict[str, Any], stage_map: dict[Path, str]) -> str:
    value = str(fm.get("stage") or "").strip()
    if value:
        return value
    for stage_dir, heading in stage_map.items():
        try:
            path.relative_to(stage_dir)
            return heading
        except ValueError:
            pass
    return ""


def infer_module(path: Path, fm: dict[str, Any]) -> str:
    value = str(fm.get("module") or "").strip()
    if value:
        return value
    parent = path.parent.name
    if NUMBERED_DIR_RE.match(parent):
        return clean_title(parent.split("-", 1)[1])
    return ""


@dataclass
class NoteInfo:
    path: Path
    fm: dict[str, Any]
    body: str
    title: str
    course: str
    stage: str
    module: str
    role: str


@dataclass
class CourseInfo:
    dir: Path
    name: str
    stage_map: dict[Path, str]
    notes: list[NoteInfo] = field(default_factory=list)


def collect_course_info(course_dir: Path) -> CourseInfo:
    cname = course_name(course_dir)
    smap = stage_heading_by_dir(course_dir)
    info = CourseInfo(course_dir, cname, smap)
    for path in find_markdown(course_dir):
        fm, body, has_fm = parse_frontmatter(read_text(path))
        if not has_fm:
            continue
        title = display_title_from_meta(path, fm, body)
        stage = infer_stage(path, fm, smap)
        module = infer_module(path, fm)
        role = str(fm.get("note_role") or "").strip()
        info.notes.append(NoteInfo(path, fm, body, title, str(fm.get("course") or cname), stage, module, role))
    return info


def is_study_concept_candidate(note: NoteInfo) -> bool:
    if note.fm.get("type") != "study" or note.fm.get("template"):
        return False
    parts = set(note.path.parts)
    if {"20-推导笔记", "30-题型笔记", "40-错题漏洞"} & parts:
        return False
    return True


def legacy_scaffold(text: str) -> bool:
    return bool(OLD_SCAFFOLD_RE.search(text))


def has_human_content(body: str) -> bool:
    if legacy_scaffold(body):
        return False
    stripped = re.sub(r"---.*?---", "", body, flags=re.S).strip()
    return len(stripped) > 500 and not EMPTY_SHELL_RE.search(stripped[:1200])


def format_source(fm: dict[str, Any]) -> str:
    books = as_list(fm.get("source_textbook"))
    sections = as_list(fm.get("source_sections"))
    if books and sections:
        return "；".join(books[:2]) + " / " + "；".join(sections[:2])
    if books:
        return "；".join(books[:2])
    if sections:
        return "；".join(sections[:2])
    return "当前课程阶段材料"


COURSE_ACTIONS = {
    "社交网络挖掘": "把节点、边、社群和传播过程转成可计算的网络指标或任务",
    "时间序列分析": "描述随时间变化的数据结构、依赖关系和预测规则",
    "量化金融": "把收益、风险、交易信号和组合约束转成可检验的量化判断",
    "离散数学": "处理集合、关系、图、递推和证明中的离散结构",
    "计算机视觉": "把图像或视频中的视觉信号转成特征、几何关系或识别结果",
    "常微分方程": "把连续变化过程写成状态、导数和解的关系",
    "最优化方法": "把目标函数、约束和迭代规则转成求解流程",
    "NLP全栈": "把文本、语义、序列和模型训练转成可实现的语言处理任务",
    "高等代数": "分析向量空间、线性变换、矩阵和多项式结构",
    "数据结构与算法": "把数据组织方式和计算步骤转成复杂度可控的程序过程",
    "计算机组成原理": "解释指令、存储、流水线和硬件执行之间的关系",
    "信号与系统": "把信号、系统响应和频域表示转成可分析的输入输出关系",
    "强化学习": "把状态、动作、奖励和策略更新转成序贯决策问题",
    "概率图模型": "用图结构表达随机变量之间的条件依赖和推断任务",
    "控制与机器人学": "把机器人状态、运动约束和控制输入写成可求解的模型",
    "多元统计": "分析多个变量之间的协方差结构、降维关系和统计推断",
    "机器学习": "把数据、假设空间、损失函数和泛化误差转成可训练模型",
    "概率论与数理统计": "描述随机现象、样本信息和统计推断规则",
    "图神经网络": "把图结构数据与神经网络表示学习结合起来",
    "随机过程": "描述随时间演化的随机变量族及其极限行为",
    "测度论": "用集合函数、可测性和积分统一概率与分析的基础语言",
    "实变函数": "研究实数空间上的函数、极限、积分和收敛性质",
    "泛函分析": "研究函数空间中的线性算子、范数和拓扑结构",
    "数学分析": "建立极限、连续、微分、积分和级数的严格分析框架",
    "运筹学": "把资源配置、网络流、排队和决策问题转成优化模型",
    "应用回归分析": "用回归模型解释变量关系、预测结果并诊断模型假设",
    "属性数据分析": "处理分类变量、列联表和广义线性模型中的推断问题",
    "非参数统计": "在少分布假设下用秩、核、重抽样等方法做推断",
    "贝叶斯统计": "用先验、似然和后验更新不确定性",
    "偏微分方程": "描述多变量连续系统中的局部变化与边界条件",
    "数值分析": "把连续数学问题转成误差可控的离散算法",
    "数据挖掘与信息检索": "从大规模数据和文本集合中提取模式、排序和检索结果",
    "复变函数": "研究复平面上解析函数、积分和级数展开的结构",
}


TOPIC_KIND_PATTERNS = [
    (r"定理|引理|法则|不等式|性质|条件", "定理/性质", "给出一组条件下必然成立的结论"),
    (r"算法|搜索|排序|规划|训练|采样|更新|优化器", "算法/流程", "规定从输入到输出的一组可执行步骤"),
    (r"模型|网络|结构|架构|机制|系统", "模型/结构", "描述对象由哪些变量、部件或关系组成"),
    (r"检验|test|Test|p值|显著性", "检验方法", "把假设、样本和拒绝规则连接起来"),
    (r"估计|估计量|回归|拟合|预测", "估计/预测方法", "从样本信息得到参数、函数或未来结果"),
    (r"矩阵|向量|空间|变换|投影|特征值", "线性代数对象", "刻画线性关系、坐标变化或结构分解"),
    (r"分布|过程|随机|概率", "概率对象", "描述随机变量或随机系统的取值规律"),
    (r"方程|公式|递推|积分|微分|极限", "公式/方程", "把变量之间的约束关系写成可推导形式"),
    (r"指标|比率|距离|损失|误差|风险|收益", "指标/度量", "把表现、差异或代价压缩成可比较数值"),
    (r"轮|坐标|图|树|堆|表|链|栈|队列", "结构对象", "描述对象的组成、连接方式和可执行操作"),
]


def course_action(course: str) -> str:
    return COURSE_ACTIONS.get(course, f"处理「{course}」中的对象、模型和判断问题")


def topic_kind(title: str) -> tuple[str, str]:
    for pattern, kind, mechanism in TOPIC_KIND_PATTERNS:
        if re.search(pattern, title):
            return kind, mechanism
    return "概念/方法", "把问题对象、适用条件和输出结论组织成稳定框架"


def relation_text(items: list[str], empty: str) -> str:
    if items:
        return "、".join(wiki(x) for x in items[:6])
    return empty


def concept_body(note: NoteInfo) -> str:
    prereqs = as_list(note.fm.get("prerequisites"))
    related = as_list(note.fm.get("related"))
    source = format_source(note.fm)
    prereq_text = "、".join(prereqs[:3]) if prereqs else "本阶段的基础定义、符号和例题"
    related_text = "、".join(related[:4]) if related else "同一模块中的相邻概念"
    module = note.module or note.stage or note.course
    stage = note.stage or "当前阶段"
    title = note.title
    kind, mechanism = topic_kind(title)
    action = course_action(note.course)

    return f"""# {title}

## 一句话定义
> {title} 是「{note.course}」中用于{action}的{kind}；放在「{module}」里，它的作用是{mechanism}。

## 它解决什么问题
- 把「{module}」里的问题从口头描述转成可检查的对象、条件和输出。
- 回答三个做题入口问题：什么时候能用「{title}」？输入是什么？结论如何解释？
- 把前置知识「{prereq_text}」接到「{related_text}」，避免只按文件夹顺序记忆。

## 核心内容

### 工作对象
「{title}」主要处理「{module}」中的{kind}问题。学习时先写清：
- 对象：题目或项目里真正被讨论的变量、结构、样本、状态或过程。
- 条件：哪些假设、约束、输入格式或前置概念必须成立。
- 输出：最后需要得到定义、数值、模型、判断、证明还是解释。

### 使用方式
1. 先把题目关键词定位到「{stage}」和「{module}」。
2. 用「{title}」识别对象、条件和输出，不急着套公式。
3. 若题目要求计算，就写出最小公式或算法步骤；若题目要求解释，就说明它和「{related_text}」的区别。

### 典型例子
> 最小例子：给定一个来自「{module}」的对象，先判断它是否满足「{title}」的适用条件；若满足，就按“对象 -> 条件 -> 输出”的顺序写出定义、计算步骤或解释结论。

### 常见误区
- 只背「{title}」这个名字，却说不清它解决的具体问题。
- 把「{title}」和「{related_text}」混为一谈，导致做题时选错工具。
- 忽略适用条件，直接套公式、流程或结论。
- 只记录教材位置，不记录能闭卷复现的最小例子。

## 和其他笔记的关系
- 前置：{relation_text(prereqs, "本卡暂无显式前置双链，先从本阶段基础概念进入")}
- 相关：{relation_text(related, "本卡暂无显式相关双链，可从同阶段 MOC 继续扩展")}
- 来源定位：{source}

## 我自己的补充
- 最小例子：
- 易错边界：
- 应用输出：
"""


def ensure_note_role_and_metadata(note: NoteInfo, course: CourseInfo, changes: Counter[str], dry_run: bool) -> None:
    if note.fm.get("type") != "study" or note.fm.get("template"):
        return
    fm = dict(note.fm)
    path_parts = set(note.path.parts)
    role = str(fm.get("note_role") or "").strip()
    inferred = "concept"
    if "20-推导笔记" in path_parts:
        inferred = "derivation"
    elif "30-题型笔记" in path_parts:
        inferred = "problem_type"
    elif "40-错题漏洞" in path_parts:
        inferred = "mistake"
    if not role:
        fm["note_role"] = inferred
    if not fm.get("course"):
        fm["course"] = course.name
    if not fm.get("stage"):
        stage = infer_stage(note.path, fm, course.stage_map)
        if stage:
            fm["stage"] = stage
    if not fm.get("module"):
        module = infer_module(note.path, fm)
        if module and "笔记" not in module:
            fm["module"] = module
    if fm != note.fm:
        write_text(note.path, render_note(fm, note.body), dry_run, changes)


def rewrite_legacy_concept(note: NoteInfo, changes: Counter[str], dry_run: bool) -> None:
    text = read_text(note.path)
    if not legacy_scaffold(text):
        return
    if note.fm.get("type") != "study" or note.fm.get("template"):
        return
    if note.fm.get("note_role") in {"derivation", "problem_type", "mistake"}:
        return
    fm = dict(note.fm)
    fm["type"] = "study"
    fm["note_role"] = "concept"
    fm["draft_quality"] = "ai_initial"
    fm["status"] = fm.get("status") or "ongoing"
    if not fm.get("course"):
        fm["course"] = note.course
    if not fm.get("stage") and note.stage:
        fm["stage"] = note.stage
    if not fm.get("module") and note.module:
        fm["module"] = note.module
    write_text(note.path, render_note(fm, concept_body(note)), dry_run, changes)
    changes["legacy_cards_rewritten"] += 1


GENERATED_CONCEPT_MARKERS = (
    "核心概念或方法",
    "初稿：可以把",
    "本阶段前置概念",
    "待补前置链接",
    "待补相关链接",
)


def refresh_generated_concept(note: NoteInfo, changes: Counter[str], dry_run: bool) -> None:
    if note.fm.get("type") != "study" or note.fm.get("template"):
        return
    if note.fm.get("note_role") != "concept" or note.fm.get("draft_quality") != "ai_initial":
        return
    if not any(marker in note.body for marker in GENERATED_CONCEPT_MARKERS):
        return
    write_text(note.path, render_note(note.fm, concept_body(note)), dry_run, changes)
    changes["generated_concepts_refreshed"] += 1


def project_body(note: NoteInfo) -> str:
    title = note.title
    course = note.course
    module = note.module or note.stage or course
    related = as_list(note.fm.get("related"))
    related_text = "、".join(wiki(x) for x in related[:5]) if related else "待补相关链接"
    return f"""# {title}

## 项目目标
> 用一个可交付的小项目，把「{module}」中的关键概念落到数据、代码、实验、展示或申请材料里。

## 它解决什么问题
- 把「{course}」里的抽象知识转化为可展示的作品或复盘材料。
- 明确项目输入、方法、输出和验收标准，避免只停留在学习计划。
- 为后续简历、论文、课程作业或作品集沉淀证据。

## 核心任务
1. 明确项目问题：要回答什么、服务什么场景。
2. 选择方法路线：用哪些概念、模型、算法或工具。
3. 形成最小交付：代码、图表、报告、演示或复盘。
4. 记录风险：数据不足、假设过强、评价指标不清或复现困难。

## 最小交付
- 项目一句话说明：
- 输入数据 / 材料：
- 核心方法：
- 输出形式：
- 验收标准：

## 关联
- 相关概念：{related_text}
- 课程入口：[[{course} MOC]]
"""


def rewrite_legacy_project(note: NoteInfo, changes: Counter[str], dry_run: bool) -> None:
    text = read_text(note.path)
    if not legacy_scaffold(text):
        return
    if note.fm.get("type") != "project" or note.fm.get("template"):
        return
    fm = dict(note.fm)
    fm["draft_quality"] = "ai_initial"
    fm["status"] = fm.get("status") or "ongoing"
    if not fm.get("course") and note.course:
        fm["course"] = note.course
    write_text(note.path, render_note(fm, project_body(note)), dry_run, changes)
    changes["legacy_projects_rewritten"] += 1


def root_template_content(kind: str) -> str:
    templates = {
        "moc": """---
type: index
note_role: moc
cssclasses:
  - atlas-page
  - atlas-index
template: true
topic: "MOC地图笔记模板"
course:
created: 2026-06-24
status: active
tags: [MOC, 索引]
---

# MOC地图笔记模板

## 概念地图
- [[ ]]

## 推导地图
- [[ ]]

## 题型地图
- [[ ]]

## 错题 / 漏洞
- [[ ]]

## 输出与应用
- [[ ]]
""",
        "concept": """---
type: study
note_role: concept
cssclasses:
  - atlas-page
  - atlas-study
template: true
topic:
course:
stage:
module:
created: 2026-06-24
status: ongoing
difficulty: intermediate
concept: []
prerequisites: []
related: []
tags: [学习]
---

# {{title}}

## 一句话定义
> 用 1-3 句话说清这个概念是什么。不要写学习任务，直接写知识本身。

## 它解决什么问题
- 

## 核心内容

### 正式定义
> 

### 使用条件 / 判断方法
> 

### 典型例子
> 

### 常见误区
- 

## 和其他笔记的关系
- 前置：[[ ]]
- 相关：[[ ]]
- 题型：[[ ]]

## 我自己的补充
- 原题 / 案例：
- 我卡住的地方：
- 下次闭卷复写：
""",
        "derivation": """---
type: study
note_role: derivation
cssclasses:
  - atlas-page
  - atlas-study
template: true
topic:
course:
stage:
source_concept:
created: 2026-06-24
status: ongoing
difficulty: intermediate
concept: []
prerequisites: []
related: []
tags: [学习, 推导]
---

# {{title}}

## 推导目标
> 要证明什么？最后要得到哪一个公式、结论或分布？

## 关键假设
1. 

## 推导步骤

### 步骤 1：
> 

为什么这一步成立：

### 步骤 2：
> 

为什么这一步成立：

### 步骤 3：
> 

为什么这一步成立：

## 我容易卡住的地方
- 

## 最小复现
- 起点：
- 关键变形：
- 终点：

## 关联
- 概念主卡：[[ ]]
- 题型笔记：[[ ]]
- 错题漏洞：[[ ]]
""",
        "problem_type": """---
type: study
note_role: problem_type
cssclasses:
  - atlas-page
  - atlas-study
template: true
topic:
course:
stage:
source_concept:
created: 2026-06-24
status: ongoing
difficulty: intermediate
concept: []
prerequisites: []
related: []
linked_questions: []
tags: [学习, 题型]
---

# {{title}}

## 题型识别
> 看到什么条件、问法或关键词，就应该想到这类题？

## 解题套路
1. 

## 题型 1
- 识别信号：
- 标准步骤：
- 易错点：
- 关联题目：[[ ]]

## 题型 2
- 识别信号：
- 标准步骤：
- 易错点：
- 关联题目：[[ ]]

## 关联概念
- [[ ]]

## 我的补题区
- 原题链接：
- 我卡住的步骤：
- 下次看到同类题的触发词：
""",
        "mistake": """---
type: study
note_role: mistake
cssclasses:
  - atlas-page
  - atlas-study
template: true
topic: "错题漏洞笔记模板"
course:
stage:
source_concept:
created: 2026-06-24
status: ongoing
difficulty: intermediate
concept: []
prerequisites: []
related: []
review_status: open
tags: [学习, 错题, 漏洞]
---

# 错题漏洞笔记模板

## 原题 / 来源
> 

## 我的错误答案
> 

## 错因
> 

## 正解
> 

## 修复动作
- [ ] 回看概念主卡
- [ ] 做一道同型题
- [ ] 一周后闭卷复现

## 关联
- 概念：[[ ]]
- 题型：[[ ]]
- 单题卡：[[ ]]

## 复习状态
| 日期 | 结果 | 下一步 |
|:---|:---|:---|
| 2026-06-24 | open |  |
""",
    }
    return templates[kind].strip() + "\n"


def update_root_templates(dry_run: bool, changes: Counter[str]) -> None:
    for kind, path in ROOT_TEMPLATES.items():
        write_text(path, root_template_content(kind), dry_run, changes)


def concept_notes(course: CourseInfo) -> list[NoteInfo]:
    notes = [n for n in course.notes if is_study_concept_candidate(n)]
    return sorted(notes, key=lambda n: (n.stage, n.module, n.title))


def grouped_concepts(course: CourseInfo) -> dict[str, dict[str, list[NoteInfo]]]:
    groups: dict[str, dict[str, list[NoteInfo]]] = defaultdict(lambda: defaultdict(list))
    for note in concept_notes(course):
        stage = note.stage or "未分阶段"
        module = note.module or "未分模块"
        groups[stage][module].append(note)
    return groups


def derivation_notes(course: CourseInfo) -> list[Path]:
    root = course.dir / "20-推导笔记"
    return sorted(root.glob("*.md")) if root.exists() else []


def problem_type_notes(course: CourseInfo) -> list[Path]:
    root = course.dir / "30-题型笔记"
    return sorted(root.glob("*.md")) if root.exists() else []


def moc_body(course: CourseInfo) -> str:
    groups = grouped_concepts(course)
    lines = [f"# {course.name} MOC", "", "## 概念地图"]
    for stage, modules in groups.items():
        lines += ["", f"### {stage}"]
        for module, notes in modules.items():
            lines += ["", f"#### {module}"]
            for note in notes:
                lines.append(f"- [[{note.path.stem}]]")
    lines += ["", "## 推导地图"]
    derivs = derivation_notes(course)
    if derivs:
        lines += [f"- [[{p.stem}]]" for p in derivs]
    else:
        lines.append("- (待补)")
    lines += ["", "## 题型地图"]
    problems = problem_type_notes(course)
    if problems:
        lines += [f"- [[{p.stem}]]" for p in problems]
    else:
        lines.append("- (待补)")
    lines += ["", "## 错题 / 漏洞", f"- [[{course.name}错题漏洞入口]]"]
    return "\n".join(lines) + "\n"


def index_frontmatter(topic: str, course: str, tags: list[str]) -> dict[str, Any]:
    return {
        "type": "index",
        "note_role": "moc",
        "cssclasses": ["atlas-page", "atlas-index"],
        "topic": topic,
        "course": course,
        "created": TODAY,
        "status": "active",
        "tags": tags,
    }


def create_course_moc(course: CourseInfo, dry_run: bool, changes: Counter[str]) -> None:
    path = course.dir / "00-MOC地图" / f"{course.name} MOC.md"
    fm = index_frontmatter(f"{course.name} MOC", course.name, ["MOC", course.name, "索引"])
    write_text(path, render_note(fm, moc_body(course)), dry_run, changes)


def concept_entry_body(course: CourseInfo) -> str:
    groups = grouped_concepts(course)
    lines = [
        f"# {course.name}概念笔记入口",
        "",
        "## 当前原则",
        f"- 现有概念主卡保留在阶段目录中，不做物理迁移。",
        f"- 本入口只负责把阶段概念卡接入五类笔记结构。",
        f"- 总地图：[[{course.name} MOC]]",
        "",
        "## 阶段概念卡",
    ]
    for stage, modules in groups.items():
        lines += ["", f"### {stage}"]
        for module, notes in modules.items():
            sample = notes[:8]
            lines += ["", f"#### {module}"]
            lines += [f"- [[{note.path.stem}]]" for note in sample]
            if len(notes) > len(sample):
                lines.append(f"- ... 其余 {len(notes) - len(sample)} 张见 [[{course.name} MOC]]")
    lines += ["", "## 后续独立概念卡", "- 高频复用或跨阶段概念可以后续从阶段目录抽出到本目录。"]
    return "\n".join(lines) + "\n"


def create_concept_entry(course: CourseInfo, dry_run: bool, changes: Counter[str]) -> None:
    path = course.dir / "10-概念笔记" / f"{course.name}概念笔记入口.md"
    fm = index_frontmatter(f"{course.name}概念笔记入口", course.name, ["MOC", course.name, "概念笔记"])
    write_text(path, render_note(fm, concept_entry_body(course)), dry_run, changes)


DERIVATION_KEYWORDS = [
    "推导",
    "证明",
    "公式",
    "定理",
    "方程",
    "分布",
    "梯度",
    "矩阵",
    "算法",
    "收敛",
    "判据",
    "模型",
    "损失",
]


def select_derivation_candidates(course: CourseInfo, count: int = 2) -> list[NoteInfo]:
    notes = concept_notes(course)
    scored = []
    for idx, note in enumerate(notes):
        title = note.title
        score = sum(3 for kw in DERIVATION_KEYWORDS if kw.lower() in title.lower() or kw in note.module)
        score += max(0, 5 - idx / 50)
        scored.append((score, idx, note))
    selected: list[NoteInfo] = []
    seen_stage: set[str] = set()
    for _, _, note in sorted(scored, key=lambda x: (-x[0], x[1])):
        if len(selected) >= count:
            break
        if note.stage in seen_stage and len(seen_stage) < count and len(notes) > count:
            continue
        selected.append(note)
        seen_stage.add(note.stage)
    for note in notes:
        if len(selected) >= count:
            break
        if note not in selected:
            selected.append(note)
    return selected[:count]


def derivation_body(course: CourseInfo, note: NoteInfo) -> str:
    prereqs = as_list(note.fm.get("prerequisites"))
    related = as_list(note.fm.get("related"))
    prereq_text = "、".join(prereqs[:3]) if prereqs else "相关定义和基本符号"
    related_links = "、".join(wiki(x) for x in related[:5]) if related else "待补相关链接"
    return f"""# {note.title}推导

## 推导目标
说明「{note.title}」从定义、条件到结论的最小推导链条，并把它放回「{course.name}」的「{note.module or note.stage}」主线中。

## 关键假设
1. 已经掌握：{prereq_text}。
2. 问题对象属于「{note.module or note.stage}」讨论范围。
3. 目标是得到可用于判断、计算或解释的结论，而不是只背术语。

## 推导步骤

### 步骤 1：明确对象和符号
把题目中的对象写成清楚的输入、条件和输出。对「{note.title}」来说，输入通常来自「{note.stage or course.name}」中的具体对象或数据结构。

为什么这一步成立：推导的第一步不是套公式，而是确认对象满足该概念的适用条件。

### 步骤 2：代入核心定义
把「{note.title}」的核心定义或判别规则写出来，并检查哪些条件来自前置知识「{prereq_text}」。

为什么这一步成立：定义决定了后续能做哪些变形、比较或计算。

### 步骤 3：得到结论并解释边界
根据定义推出结论，再说明它和「{note.module or note.stage}」中的相邻概念有什么区别。

为什么这一步成立：推导的终点必须能回答原问题，而不是停在形式变形上。

## 我容易卡住的地方
- 忘记先检查适用条件，直接套用「{note.title}」。
- 把「{note.title}」和相邻概念混用。
- 只写结果，不解释每一步为什么允许这样变形。

## 最小复现
- 起点：写出「{note.title}」的对象和条件。
- 关键变形：代入定义或判别规则。
- 终点：得到结论，并说清它的适用边界。

## 关联
- 概念主卡：[[{note.path.stem}]]
- 相关概念：{related_links}
"""


def derivation_frontmatter(course: CourseInfo, note: NoteInfo) -> dict[str, Any]:
    return {
        "type": "study",
        "note_role": "derivation",
        "cssclasses": ["atlas-page", "atlas-study"],
        "topic": f"{note.title}推导",
        "course": course.name,
        "stage": note.stage,
        "source_concept": note.path.stem,
        "created": TODAY,
        "status": "ongoing",
        "difficulty": note.fm.get("difficulty") or "intermediate",
        "concept": [note.title, "推导"],
        "prerequisites": as_list(note.fm.get("prerequisites")),
        "related": [note.path.stem] + as_list(note.fm.get("related"))[:4],
        "draft_quality": "ai_initial",
        "tags": ["学习", "推导", course.name],
    }


def create_derivations(course: CourseInfo, dry_run: bool, changes: Counter[str]) -> None:
    existing = derivation_notes(course)
    needed = max(0, 2 - len(existing))
    if needed == 0:
        return
    used = {p.stem for p in existing}
    for note in select_derivation_candidates(course, needed + len(existing)):
        if needed <= 0:
            break
        stem = safe_filename(f"{note.title}推导", "").rstrip(".")
        if stem in used:
            continue
        path = course.dir / "20-推导笔记" / safe_filename(stem)
        write_text(path, render_note(derivation_frontmatter(course, note), derivation_body(course, note)), dry_run, changes)
        used.add(stem)
        needed -= 1


def module_candidates(course: CourseInfo) -> list[tuple[str, list[NoteInfo]]]:
    by_module: dict[str, list[NoteInfo]] = defaultdict(list)
    for note in concept_notes(course):
        key = note.module or note.stage or "核心主线"
        by_module[key].append(note)
    ranked = sorted(by_module.items(), key=lambda item: (-len(item[1]), item[0]))
    return ranked


def problem_type_body(course: CourseInfo, module: str, notes: list[NoteInfo]) -> str:
    links = [n.path.stem for n in notes[:6]]
    link_text = "\n".join(f"- [[{x}]]" for x in links) if links else "- 待补概念链接"
    return f"""# {module}常见题型

## 题型识别
看到题目要求定义、比较、计算、判断或解释「{module}」相关对象时，先回到本题型笔记，确认它属于概念辨析、过程计算、结构判断还是应用解释。

## 解题套路
1. 确认题目给出的对象、条件和目标。
2. 选择「{module}」中最相关的概念卡。
3. 写出定义或判别规则，再代入题目条件。
4. 给出结论，并补一句适用边界或易错点。

## 题型 1：概念辨析题
- 识别信号：题目问“是什么、区别是什么、为什么成立”。
- 标准步骤：写定义；列关键条件；和相邻概念做对照。
- 易错点：只背术语，不说明边界。

## 题型 2：计算 / 推导题
- 识别信号：题目给具体对象，要求算指标、推出结论或验证条件。
- 标准步骤：列输入；代入公式或流程；检查单位、维度、自由度、边界条件。
- 易错点：忽略前提条件，直接套用结果。

## 题型 3：应用解释题
- 识别信号：题目给案例、代码输出、实验结果或项目场景。
- 标准步骤：先翻译成课程语言；再定位到概念卡；最后解释结果含义和局限。
- 易错点：只描述现象，不说它和「{module}」的哪条主线相连。

## 关联概念
{link_text}

## 我的补题区
- 原题链接：待从真实做题中回填。
- 我卡住的步骤：待回填。
- 下次看到同类题的触发词：{module}、定义、判断、计算、解释、比较。
"""


def problem_frontmatter(course: CourseInfo, module: str, notes: list[NoteInfo]) -> dict[str, Any]:
    concepts = [n.title for n in notes[:3]]
    related = [n.path.stem for n in notes[:6]]
    return {
        "type": "study",
        "note_role": "problem_type",
        "cssclasses": ["atlas-page", "atlas-study"],
        "topic": f"{module}常见题型",
        "course": course.name,
        "stage": notes[0].stage if notes else "",
        "source_concept": related[0] if related else "",
        "created": TODAY,
        "status": "ongoing",
        "difficulty": "intermediate",
        "concept": concepts or [module],
        "prerequisites": [],
        "related": related,
        "linked_questions": [],
        "draft_quality": "ai_initial",
        "tags": ["学习", "题型", course.name],
    }


def create_problem_types(course: CourseInfo, dry_run: bool, changes: Counter[str]) -> None:
    existing = problem_type_notes(course)
    needed = max(0, 5 - len(existing))
    if needed == 0:
        return
    used = {p.stem for p in existing}
    for module, notes in module_candidates(course):
        if needed <= 0:
            break
        stem = safe_filename(f"{module}常见题型", "").rstrip(".")
        if stem in used:
            continue
        path = course.dir / "30-题型笔记" / safe_filename(stem)
        write_text(path, render_note(problem_frontmatter(course, module, notes), problem_type_body(course, module, notes)), dry_run, changes)
        used.add(stem)
        needed -= 1


def mistake_entry_body(course: CourseInfo) -> str:
    problems = problem_type_notes(course)
    problem_links = "\n".join(f"- [[{p.stem}]]" for p in problems[:8]) if problems else "- 待补题型笔记"
    return f"""# {course.name}错题漏洞入口

## 使用规则
- 这里只记录真实做题、听课或复盘中暴露出的错误。
- 不批量伪造错题；每张错题都必须有原题或来源。
- 每张错题至少写清：原题 / 我的错误答案 / 错因 / 正解 / 关联概念 / 复习状态。

## 错题清单

```dataview
TABLE status, review_status, source_concept
FROM "02-Knowledge/🧠 学习系统/{course.dir.name}/40-错题漏洞"
WHERE type = "study" AND note_role = "mistake"
SORT file.mtime DESC
```

## 关联题型
{problem_links}
"""


def create_mistake_entry(course: CourseInfo, dry_run: bool, changes: Counter[str]) -> None:
    path = course.dir / "40-错题漏洞" / f"{course.name}错题漏洞入口.md"
    fm = index_frontmatter(f"{course.name}错题漏洞入口", course.name, ["MOC", "错题", course.name])
    write_text(path, render_note(fm, mistake_entry_body(course)), dry_run, changes)


def ensure_five_dirs(course: CourseInfo, dry_run: bool, changes: Counter[str]) -> None:
    for dirname in FIVE_DIRS:
        path = course.dir / dirname
        if not path.exists():
            changes["dirs_created"] += 1
            if not dry_run:
                path.mkdir(parents=True, exist_ok=True)


def update_course_structure(course: CourseInfo, dry_run: bool, changes: Counter[str]) -> None:
    ensure_five_dirs(course, dry_run, changes)
    create_derivations(course, dry_run, changes)
    create_problem_types(course, dry_run, changes)
    # Refresh info after generated derivations/problem types so MOC sees them.
    refreshed = collect_course_info(course.dir)
    create_moc = create_course_moc(refreshed, dry_run, changes)
    create_concept_entry(refreshed, dry_run, changes)
    create_mistake_entry(refreshed, dry_run, changes)


def progress_block(course: str, stage: str) -> str:
    course_escaped = course.replace("\\", "\\\\").replace('"', '\\"')
    stage_escaped = stage.replace("\\", "\\\\").replace('"', '\\"')
    return f"""```dataviewjs
const notes = dv.pages('"02-Knowledge/🧠 学习系统"')
  .where(p => p.type === "study"
    && !p.template
    && (p.note_role ?? "concept") === "concept"
    && p.course === "{course_escaped}"
    && p.stage === "{stage_escaped}");
const completed = notes.where(p => p.status === "completed").length;
const total = notes.length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**阶段进度: ${{progress}}%** (${{completed}}/${{total}} 概念卡)`);
```"""


def update_stage_progress(course: CourseInfo, dry_run: bool, changes: Counter[str]) -> None:
    for stage_dir, stage_title in course.stage_map.items():
        for path in sorted(stage_dir.glob("*.md")):
            text = read_text(path)
            fm, body, has_fm = parse_frontmatter(text)
            if not has_fm or fm.get("type") != "stage":
                continue
            lines = text.splitlines()
            changed = False
            i = 0
            while i < len(lines):
                if lines[i].startswith("##") and "阶段进度" in lines[i]:
                    j = i + 1
                    while j < len(lines) and not lines[j].strip().startswith("```dataviewjs"):
                        j += 1
                    if j < len(lines):
                        k = j + 1
                        while k < len(lines) and not lines[k].strip().startswith("```"):
                            k += 1
                        if k < len(lines):
                            block = progress_block(course.name, stage_title).splitlines()
                            lines = lines[:j] + block + lines[k + 1 :]
                            changed = True
                    else:
                        block = [""] + progress_block(course.name, stage_title).splitlines()
                        lines = lines[: i + 1] + block + lines[i + 1 :]
                        changed = True
                    break
                i += 1
            if changed:
                write_text(path, "\n".join(lines).rstrip() + "\n", dry_run, changes)


def update_concept_index(dry_run: bool, changes: Counter[str]) -> None:
    path = ROOT / "🔍 概念自动索引.md"
    if not path.exists():
        return
    text = read_text(path)
    old = 'p.type === "study" && !p.template && inStudyScope(p) && !isStageLikeName(p.file.name)'
    new = 'p.type === "study" && !p.template && p.note_role !== "moc" && inStudyScope(p) && !isStageLikeName(p.file.name)'
    text = text.replace(old, new)
    write_text(path, text, dry_run, changes)


def update_review_list(dry_run: bool, changes: Counter[str]) -> None:
    path = ROOT / "🔄 复习清单.md"
    if not path.exists():
        return
    text = read_text(path)
    marker = "<!-- five-role-review:start -->"
    end = "<!-- five-role-review:end -->"
    block = f"""
{marker}

## 错题 / 漏洞回填

```dataviewjs
const mistakes = dv.pages('"02-Knowledge/🧠 学习系统"')
  .where(p => p.type === "study" && p.note_role === "mistake" && !p.template)
  .sort(p => p.file.mtime, 'desc')
  .limit(30);
dv.table(["错题", "课程", "状态", "复习状态"], mistakes.map(p => [p.file.link, p.course ?? "", p.status ?? "", p.review_status ?? "open"]));
```

## AI 初稿复核

```dataviewjs
const drafts = dv.pages('"02-Knowledge/🧠 学习系统"')
  .where(p => p.type === "study" && p.draft_quality === "ai_initial" && !p.template)
  .sort(p => p.file.mtime, 'desc')
  .limit(50);
dv.table(["初稿", "课程", "阶段", "角色"], drafts.map(p => [p.file.link, p.course ?? "", p.stage ?? "", p.note_role ?? "concept"]));
```

{end}
""".strip()
    pattern = re.compile(re.escape(marker) + r".*?" + re.escape(end), re.S)
    if pattern.search(text):
        text = pattern.sub(block, text)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    write_text(path, text, dry_run, changes)


def update_auto_index_guide(dry_run: bool, changes: Counter[str]) -> None:
    path = ROOT / "📋 自动化索引使用指南.md"
    if not path.exists():
        return
    text = read_text(path)
    marker = "<!-- five-role-optimization:start -->"
    end = "<!-- five-role-optimization:end -->"
    block = f"""
{marker}

## 五类笔记优化规则

- `type` 继续表示系统类型，`note_role` 表示学习沉淀角色。
- 概念索引排除 `template: true` 和 `note_role: moc` 页面。
- 阶段进度优先按 `course + stage + note_role` 统计概念卡，不依赖文件是否移动。
- `draft_quality: ai_initial` 表示该卡是 AI 初稿，需要后续通过做题、闭卷复现或项目应用校准。
- 错题/漏洞笔记只记录真实错误，不批量伪造。

{end}
""".strip()
    pattern = re.compile(re.escape(marker) + r".*?" + re.escape(end), re.S)
    if pattern.search(text):
        text = pattern.sub(block, text)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    write_text(path, text, dry_run, changes)


def dataview_anomalies(files: list[Path]) -> int:
    bad = 0
    bad_fence_re = re.compile(r"(?m)^``dataview(?:js)?\s*$")
    for path in files:
        text = read_text(path)
        if text.count("```") % 2 != 0:
            bad += 1
        if bad_fence_re.search(text):
            bad += 1
    return bad


def audit() -> dict[str, Any]:
    all_files = find_markdown(ROOT)
    courses = [collect_course_info(p) for p in find_course_dirs(core_only=True)]
    base_by_course = {c.dir.name: {p.stem for p in find_markdown(c.dir)} for c in courses}
    rows = []
    old = 0
    empty = 0
    note_roles = 0
    type_study = 0
    generated_moc_missing = 0

    for path in all_files:
        text = read_text(path)
        if OLD_SCAFFOLD_RE.search(text):
            old += 1
        if EMPTY_SHELL_RE.search(text):
            empty += 1
        fm, _, has_fm = parse_frontmatter(text)
        if has_fm and fm.get("type") == "study":
            type_study += 1
            if fm.get("note_role"):
                note_roles += 1

    for course in courses:
        dir_state = {d: (course.dir / d).exists() for d in FIVE_DIRS}
        moc_path = course.dir / "00-MOC地图" / f"{course.name} MOC.md"
        moc_missing = 0
        if moc_path.exists():
            text = read_text(moc_path)
            for match in WIKILINK_RE.finditer(text):
                target = Path(match.group(1)).stem
                if target not in base_by_course[course.dir.name]:
                    moc_missing += 1
        generated_moc_missing += moc_missing
        rows.append(
            {
                "course": course.dir.name,
                "dirs_complete": all(dir_state.values()),
                "missing_dirs": [d for d, ok in dir_state.items() if not ok],
                "moc_missing": moc_missing,
                "derivations": len(derivation_notes(course)),
                "problem_types": len(problem_type_notes(course)),
            }
        )
    return {
        "markdown_files": len(all_files),
        "core_courses": len(courses),
        "complete_five_dirs": sum(1 for r in rows if r["dirs_complete"]),
        "old_scaffold_files": old,
        "empty_shell_like_files": empty,
        "type_study": type_study,
        "study_with_note_role": note_roles,
        "generated_moc_missing_links": generated_moc_missing,
        "dataview_anomalies": dataview_anomalies(all_files),
        "rows": rows,
    }


def audit_report(data: dict[str, Any]) -> str:
    lines = [
        "---",
        "type: index",
        "topic: \"五类笔记优化审计\"",
        f"created: {TODAY}",
        "status: active",
        "tags: [审计, 学习系统, 五类笔记]",
        "---",
        "",
        "# 五类笔记优化审计",
        "",
        "## 总览",
        f"- Markdown 文件数：{data['markdown_files']}",
        f"- 核心学科数：{data['core_courses']}",
        f"- 五类目录完整学科：{data['complete_five_dirs']}/{data['core_courses']}",
        f"- 旧空壳文件数：{data['old_scaffold_files']}",
        f"- 空占位痕迹文件数：{data['empty_shell_like_files']}",
        f"- study note_role 覆盖：{data['study_with_note_role']}/{data['type_study']}",
        f"- 生成 MOC 缺失链接数：{data['generated_moc_missing_links']}",
        f"- Dataview 代码块异常：{data['dataview_anomalies']}",
        "",
        "## 学科明细",
        "",
        "| 学科 | 五类目录 | 缺失目录 | MOC缺失链接 | 推导 | 题型 |",
        "|:---|:---:|:---|---:|---:|---:|",
    ]
    for row in data["rows"]:
        missing = "、".join(row["missing_dirs"]) if row["missing_dirs"] else "-"
        lines.append(
            f"| {row['course']} | {'✅' if row['dirs_complete'] else '⚠️'} | {missing} | {row['moc_missing']} | {row['derivations']} | {row['problem_types']} |"
        )
    return "\n".join(lines) + "\n"


def write_audit_report(dry_run: bool, changes: Counter[str]) -> None:
    data = audit()
    path = ROOT / "📊 五类笔记优化审计.md"
    write_text(path, audit_report(data), dry_run, changes)


def apply_all(dry_run: bool) -> Counter[str]:
    changes: Counter[str] = Counter()
    update_root_templates(dry_run, changes)
    core_dirs = find_course_dirs(core_only=True)
    courses = [collect_course_info(p) for p in core_dirs]

    for course in courses:
        ensure_five_dirs(course, dry_run, changes)

    # First pass: normalize metadata and rewrite legacy cards.
    for course in courses:
        for note in course.notes:
            ensure_note_role_and_metadata(note, course, changes, dry_run)

    # Include auxiliary study notes for old scaffold rewriting and note_role coverage.
    for course_dir in find_course_dirs(core_only=False):
        if CORE_COURSE_RE.match(course_dir.name):
            continue
        course = collect_course_info(course_dir)
        for note in course.notes:
            ensure_note_role_and_metadata(note, course, changes, dry_run)

    # Recollect after metadata edits.
    for course_dir in find_course_dirs(core_only=False):
        course = collect_course_info(course_dir)
        for note in course.notes:
            rewrite_legacy_concept(note, changes, dry_run)
            rewrite_legacy_project(note, changes, dry_run)
            refresh_generated_concept(note, changes, dry_run)

    # Recollect after old card rewrites before generating MOCs/links.
    for course_dir in core_dirs:
        course = collect_course_info(course_dir)
        update_course_structure(course, dry_run, changes)
        update_stage_progress(course, dry_run, changes)

    update_concept_index(dry_run, changes)
    update_review_list(dry_run, changes)
    update_auto_index_guide(dry_run, changes)
    write_audit_report(dry_run, changes)
    return changes


def print_audit(data: dict[str, Any]) -> None:
    print(
        f"markdown={data['markdown_files']} core_courses={data['core_courses']} "
        f"complete_five_dirs={data['complete_five_dirs']}/{data['core_courses']}"
    )
    print(
        f"old_scaffold={data['old_scaffold_files']} empty_shell={data['empty_shell_like_files']} "
        f"study_note_role={data['study_with_note_role']}/{data['type_study']} "
        f"moc_missing={data['generated_moc_missing_links']} dataview_anomalies={data['dataview_anomalies']}"
    )
    incomplete = [r for r in data["rows"] if not r["dirs_complete"] or r["moc_missing"]]
    if incomplete:
        print("incomplete_or_missing:")
        for row in incomplete[:20]:
            print(row)


def main() -> int:
    configure_utf8_stdio()
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files.")
    parser.add_argument("--audit", action="store_true", help="Only print audit summary.")
    args = parser.parse_args()

    if args.audit:
        print_audit(audit())
        return 0

    changes = apply_all(dry_run=args.dry_run)
    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(f"{mode}: " + ", ".join(f"{k}={v}" for k, v in sorted(changes.items())))
    print_audit(audit())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
