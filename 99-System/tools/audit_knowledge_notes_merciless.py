from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
from dataclasses import dataclass, field
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path
from statistics import median


VAULT = Path(__file__).resolve().parents[2]
ROOT = VAULT / "02-Knowledge" / "🧠 学习系统"
STAMP = date.today().isoformat()
OUTPUT_DIR = VAULT / "99-System" / "🗄️ 归档" / "知识库审计"
REPORT = OUTPUT_DIR / f"knowledge_notes_merciless_audit_{STAMP}.md"
SCORES = OUTPUT_DIR / f"knowledge_notes_merciless_scores_{STAMP}.csv"
DATA = OUTPUT_DIR / f"knowledge_notes_merciless_scores_{STAMP}.json"

EXCLUDED_TREE_PARTS = {
    ".git", ".obsidian", ".kiro", ".pandoc", ".pytest_cache",
    ".recovery-hold", ".tmp.drivedownload", ".tmp.driveupload",
    "scratch", "__pycache__",
}
AUXILIARY_SUBJECT_PREFIXES = ("18-", "19-", "20-", "21-")
KNOWLEDGE_TYPES = {"study", "concept", "knowledge_card", "study_note", "derivation"}
NON_KNOWLEDGE_TYPES = {
    "index", "moc", "stage", "project", "problem-type", "problem_type",
    "mistake", "question", "journal", "template", "book", "paper", "tool",
    "lab", "lab_manual", "lab-manual", "assignment", "homework",
}

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
URL_RE = re.compile(r"https?://[^\s)>\]]+", re.I)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
CODE_RE = re.compile(r"```([^\n`]*)\n(.*?)```", re.S)
MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.S)
HEADING_RE = re.compile(r"(?m)^#{1,6}\s+(.+?)\s*$")

# A previous batch operation appended the same machine-learning appendix to
# unrelated notes. It is excluded before any scoring.
APPENDIX_MARKERS = (
    "## 💡 直觉心智模型与痛点背景",
    "## 📐 形式化定义与数学推导 (LaTeX)",
    "## 💻 核心代码实现与张量维度追踪 (Shape Tracing)",
    "## 🔗 知识连接与闭卷自测",
    "## 🔗 知识网络与闭卷自查",
    "## ⚠️ 常见误区与对比矩阵",
)
APPENDIX_SIGNATURES = (
    "信息调度过滤器",
    "优化目标定义为最小化经验风险",
    "标准 Python 核心实现，附带严谨的 Tensor Shape Tracing",
    "传统方法在处理高维空间、动态序列或非线性特征映射时存在严重的表达能力瓶颈",
)

PLACEHOLDER_RE = re.compile(
    r"待补(?:全|充)?|TODO|TBD|占位|暂无内容|后续补充|coming soon|未完成|待完善",
    re.I,
)
GENERIC_RISK_PATTERNS = (
    ("通用高维模板", re.compile(r"面对高维数据与复杂非线性关系|维度灾难与优化陷入局部极值")),
    ("通用离散数学模板", re.compile(r"将口头逻辑转化为形式化的语言与严密的证明框架|满足相应离散约束与代数公理")),
    ("通用梯度下降模板", re.compile(r"用局部导数指导全局迭代优化|放弃一步到位，改用泰勒展开一阶近似")),
    ("无意义伪公式", re.compile(r"CoreFormula\s*\(|TextFormula\s*\(|TODOFormula\s*\(", re.I)),
    ("虚假完成度字段", re.compile(r"subagent_audit_score\s*:\s*(?:9(?:\.\d+)?|10(?:\.0+)?)", re.I)),
    ("LaTeX转义/控制字符损坏", re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]|\text\s*\{")),
)


@dataclass
class Note:
    path: Path
    rel: str
    subject: str
    title: str
    topic: str
    raw: str
    body: str
    frontmatter_text: str
    frontmatter: dict[str, str]
    category: str
    appendix_body: str = ""
    appendix_removed: int = 0
    blocks: list[str] = field(default_factory=list)
    block_keys: list[str] = field(default_factory=list)
    effective_body: str = ""
    repeated_removed: int = 0
    repeat_ratio: float = 0.0
    within_repeated_removed: int = 0
    within_repeat_ratio: float = 0.0
    duplicate_group: str = ""
    title_path_similarity: float = 1.0
    links: list[str] = field(default_factory=list)
    valid_links: int = 0
    broken_links: list[str] = field(default_factory=list)
    score: int = 0
    cap: int = 100
    grade: str = ""
    dimensions: dict[str, int] = field(default_factory=dict)
    flags: list[str] = field(default_factory=list)
    fixes: list[str] = field(default_factory=list)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, str]:
    if not text.startswith("---"):
        return {}, "", text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not match:
        return {}, "", text
    raw = match.group(1)
    values: dict[str, str] = {}
    for line in raw.splitlines():
        item = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if item:
            values[item.group(1).lower()] = item.group(2).strip().strip("'\"")
    return values, raw, text[match.end():]


def strip_known_appendix(body: str) -> tuple[str, int]:
    if not any(signature in body for signature in APPENDIX_SIGNATURES):
        return body, 0
    positions = [body.find(marker) for marker in APPENDIX_MARKERS if body.find(marker) >= 0]
    if not positions:
        return body, 0
    cut = min(positions)
    return body[:cut].rstrip(), len(body) - cut


def visible_text(text: str) -> str:
    text = CODE_RE.sub(" ", text)
    text = MATH_RE.sub(" ", text)
    text = re.sub(r"`[^`]+`", " ", text)
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), text)
    text = re.sub(r"(?m)^\s*[-*+>]\s*", "", text)
    text = re.sub(r"(?m)^#{1,6}\s*", "", text)
    text = re.sub(r"[*_~|>#]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def title_anchor(value: str) -> str:
    value = re.sub(r"^[\W_\d]+", "", value, flags=re.UNICODE)
    value = re.sub(r"[（(][^()（）]{1,120}[)）]", "", value)
    value = re.sub(
        r"(?:深度学习笔记|学习笔记|核心笔记|完整笔记|笔记|详解|精读|入门|概述|基础)$",
        "",
        value,
    )
    return re.sub(r"[\s_\-—:：()（）【】\[\]\/]+", "", value).lower()


def normalize_block(block: str, note: Note) -> str:
    text = block.lower()
    substitutions = {
        note.path.stem,
        note.title,
        note.topic,
        note.frontmatter.get("course", ""),
        note.subject,
    }
    for item in sorted((item for item in substitutions if len(item) >= 2), key=len, reverse=True):
        text = text.replace(item.lower(), "<topic>")
    text = re.sub(r"\[\[[^\]]+\]\]", "<link>", text)
    text = re.sub(r"https?://\S+", "<url>", text)
    text = re.sub(r"\d+(?:\.\d+)?", "<num>", text)
    text = re.sub(r"[^\w\u4e00-\u9fff<>]+", "", text)
    return text


def classify(path: Path, fm: dict[str, str], body: str) -> str:
    stem = path.stem.lower()
    relative = path.relative_to(ROOT)
    subject = relative.parts[0] if len(relative.parts) > 1 else "根目录"
    note_type = fm.get("type", "").lower().strip()
    kind = fm.get("kind", "").lower().strip()
    note_role = fm.get("note_role", "").lower().strip()
    declared = " ".join((note_type, kind, note_role, fm.get("flow", ""))).lower()

    # AGENTS.md explicitly declares 18-21 as auxiliary directories. Journals,
    # habit trackers and PARA pages must never leak into the knowledge-card mean.
    if subject.startswith(AUXILIARY_SUBJECT_PREFIXES):
        return "辅助系统"
    if subject == "根目录" or "资源" in subject:
        return "导航/索引" if re.search(r"索引|入口|主页|指南|检查|追踪", path.stem) else "资料/文献"

    if re.search(r"\b(moc|index|map|navigation|hub)\b", declared) or re.search(
        r"(?:\bMOC\b)|学习路径|知识地图|总索引|教材挂载索引|课程挂载索引|导航|入口$|总览|概览|维度$|阶段\d|板块.*层$",
        path.stem,
        re.I,
    ):
        return "导航/索引"

    if note_type in {"problem-type", "problem_type", "mistake", "question"} or kind in {
        "problem-type", "problem_type", "mistake"
    } or note_role in {"problem-type", "problem_type", "mistake"}:
        return "题型/错题"
    if re.search(r"project|exercise|practice|homework|worksheet|review|lab|assignment", declared) or re.search(
        r"项目|实战|练习|题库|作业|复盘|错题|代码实践|课程任务|实验手册|验收",
        path.stem,
    ):
        return "练习/项目"
    if note_type in {"journal", "template"} or re.search(r"plan|daily|weekly|monthly|template|checklist", declared) or re.search(
        r"日计划|周计划|月计划|总规划|清单|模板",
        path.stem,
    ):
        return "计划/模板"
    if note_type in {"book", "paper", "tool"} or re.search(r"resource|book|paper|reference", declared) or re.search(r"教材|书籍|论文|资源", path.stem):
        return "资料/文献"

    if note_type in KNOWLEDGE_TYPES or kind in {"concept", "derivation"} or note_role in {"concept", "derivation"}:
        return "知识点"
    if note_type in NON_KNOWLEDGE_TYPES:
        return "其他非知识点"

    # Legacy notes in numbered subject paths often lack normalized metadata.
    # Include them as knowledge candidates only after all explicit exclusions.
    if re.match(r"^(?:0[1-9]|1[0-7]|2[2-9]|3[0-7])-", subject):
        return "知识点"
    return "知识点"


def iter_markdown_pruned(root: Path):
    """Yield Markdown files without ever descending into excluded trees."""
    for current, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in EXCLUDED_TREE_PARTS]
        current_path = Path(current)
        for filename in files:
            if filename.lower().endswith((".md", ".markdown")):
                yield current_path / filename


def active_markdown_inventory() -> dict[str, int]:
    """Count the user-visible vault while keeping system/recovery noise explicit."""
    counts: Counter[str] = Counter()
    for path in iter_markdown_pruned(VAULT):
        rel = path.relative_to(VAULT)
        top = rel.parts[0] if len(rel.parts) > 1 else "根目录"
        if top == "99-System" and any(part in {"tools", "🗄️ 归档", ".tmp"} for part in rel.parts):
            counts["排除的系统脚本/归档"] += 1
            continue
        counts[top] += 1
    return dict(counts)


def load_notes() -> list[Note]:
    notes: list[Note] = []
    for path in sorted(ROOT.rglob("*.md")):
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        fm, fm_text, body = parse_frontmatter(raw)
        stripped, removed = strip_known_appendix(body)
        title_match = re.search(r"(?m)^#\s+(.+?)\s*$", stripped)
        title = title_match.group(1).strip() if title_match else path.stem
        topic = fm.get("topic") or fm.get("title") or path.stem
        relative = path.relative_to(ROOT)
        subject = relative.parts[0] if len(relative.parts) > 1 else "根目录"
        note = Note(
            path=path,
            rel=path.relative_to(VAULT).as_posix(),
            subject=subject,
            title=title,
            topic=topic,
            raw=raw,
            body=body,
            frontmatter_text=fm_text,
            frontmatter=fm,
            category=classify(path, fm, stripped),
            appendix_body=stripped,
            appendix_removed=removed,
        )
        note.blocks = [block.strip() for block in re.split(r"\n\s*\n", stripped) if block.strip()]
        note.block_keys = [normalize_block(block, note) for block in note.blocks]
        # Frontmatter prerequisites/upstream/downstream are part of the graph too.
        note.links = [target.strip() for target in WIKILINK_RE.findall(stripped + "\n" + fm_text)]
        stem_anchor = title_anchor(path.stem)
        # Compare the filesystem identity with the declared semantic identity.
        # Notes without an H1 often preserve the filename as `title`, which used
        # to hide batch corruption such as filename "创建图结构" + title "嵌入特征".
        declared_title = fm.get("topic") or fm.get("title") or title
        title_key = title_anchor(declared_title)
        if len(stem_anchor) >= 3 and len(title_key) >= 3:
            note.title_path_similarity = SequenceMatcher(None, stem_anchor, title_key).ratio()
        notes.append(note)
    return notes


def remove_cross_file_templates(notes: list[Note]) -> None:
    doc_frequency: Counter[str] = Counter()
    for note in notes:
        doc_frequency.update({key for key in note.block_keys if len(key) >= 100})

    duplicate_hashes: defaultdict[str, list[Note]] = defaultdict(list)
    for note in notes:
        kept: list[tuple[str, str]] = []
        removed = 0
        candidate_chars = 0
        for block, key in zip(note.blocks, note.block_keys):
            if len(key) >= 100:
                candidate_chars += len(block)
            if len(key) >= 100 and doc_frequency[key] >= 8:
                removed += len(block)
            else:
                kept.append((block, key))

        unique_blocks: list[str] = []
        seen_keys: set[str] = set()
        within_removed = 0
        for block, key in kept:
            if len(key) >= 80 and key in seen_keys:
                within_removed += len(block)
                continue
            unique_blocks.append(block)
            if len(key) >= 80:
                seen_keys.add(key)

        note.effective_body = "\n\n".join(unique_blocks)
        # Catch shorter duplicated fragments inside otherwise unique blocks
        # (for example, a table row + navigation paragraph pasted twice).
        line_keys: list[tuple[str, int]] = []
        line_source = CODE_RE.sub("", note.effective_body)
        for line in line_source.splitlines():
            stripped_line = line.strip()
            if not stripped_line or re.fullmatch(r"[-:|\s]+", stripped_line):
                continue
            key = normalize_block(stripped_line, note)
            if len(key) >= 50:
                line_keys.append((key, len(stripped_line)))
        line_counts = Counter(key for key, _ in line_keys)
        line_seen: set[str] = set()
        for key, size in line_keys:
            if key in line_seen and line_counts[key] > 1:
                within_removed += size
            line_seen.add(key)

        note.repeated_removed = removed
        denominator = len(note.appendix_body) or 1
        note.repeat_ratio = removed / denominator
        note.within_repeated_removed = within_removed
        note.within_repeat_ratio = within_removed / denominator

        normalized = re.sub(r"\s+", "", visible_text(note.effective_body)).lower()
        if len(normalized) >= 120:
            duplicate_hashes[hashlib.sha1(normalized.encode()).hexdigest()[:12]].append(note)

    for digest, group in duplicate_hashes.items():
        if len(group) < 2:
            continue
        for note in group:
            note.duplicate_group = f"{digest} ({len(group)}篇)"


def resolve_links(notes: list[Note]) -> None:
    rel_keys: set[str] = set()
    suffixes: set[str] = set()
    stems: defaultdict[str, list[str]] = defaultdict(list)
    active_files = list(iter_markdown_pruned(VAULT))
    for path in active_files:
        rel = path.relative_to(VAULT).as_posix()[:-3].lower()
        rel_keys.add(rel)
        parts = rel.split("/")
        # Precompute every relative tail once. The former per-link linear scan
        # made a full-vault audit quadratic in the number of files and links.
        suffixes.update("/".join(parts[index:]) for index in range(len(parts)))
        stems[path.stem.lower()].append(rel)
    for note in notes:
        for original in note.links:
            target = original.replace("\\", "/").strip().removesuffix(".md").strip("/").lower()
            target = target.removeprefix("./")
            leaf = target.split("/")[-1]
            valid = (
                target in rel_keys
                or target in suffixes
                or target.removeprefix("02-knowledge/") in suffixes
                or leaf in stems
            )
            if valid:
                note.valid_links += 1
            else:
                note.broken_links.append(original)


def keyword_groups(text: str, groups: tuple[tuple[str, ...], ...]) -> int:
    lowered = text.lower()
    return sum(1 for group in groups if any(word.lower() in lowered for word in group))


def grade(score: int) -> str:
    if score >= 90:
        return "A 卓越"
    if score >= 80:
        return "B 良好"
    if score >= 70:
        return "C 合格"
    if score >= 60:
        return "D 勉强"
    return "F 不合格"


def score_note(note: Note) -> None:
    text = note.effective_body
    plain = visible_text(text)
    plain_len = len(plain)
    code = [body for _, body in CODE_RE.findall(text) if body.strip()]
    math = [body for body in MATH_RE.findall(text) if body.strip()]
    headings = HEADING_RE.findall(text)
    # A target such as [[占位-SARIMA模型|SARIMA模型]] is a graph-maintenance
    # problem, not proof that the current note body is itself a placeholder.
    placeholders = PLACEHOLDER_RE.findall(visible_text(text))
    risk_labels = [label for label, pattern in GENERIC_RISK_PATTERNS if pattern.search(note.raw)]
    anchor = title_anchor(note.topic)
    anchor_hits = plain.lower().replace(" ", "").count(anchor) if len(anchor) >= 2 else 0
    title_path_mismatch = (
        note.title_path_similarity < 0.18
        and len(title_anchor(note.path.stem)) >= 4
        and len(title_anchor(note.title)) >= 4
    )

    # 1. Topic grounding and semantic plausibility, 20 points.
    grounding = 3 if plain_len else 0
    grounding += 6 if anchor_hits >= 2 else 3 if anchor_hits == 1 else 0
    grounding += min(5, keyword_groups(text, (
        ("定义", "是指", "definition"),
        ("性质", "定理", "命题", "机制", "原理"),
        ("例如", "例子", "示例", "反例", "案例"),
        ("局限", "边界", "不适用", "误区", "注意"),
        ("区别", "对比", "关系", "vs"),
    )))
    if re.search(r"无意义伪公式", "；".join(risk_labels)):
        grounding -= 12
    elif risk_labels:
        grounding -= min(8, len(risk_labels) * 3)
    if title_path_mismatch:
        grounding -= 8
    grounding = max(0, min(20, grounding))

    # 2. Completeness, 20 points. Effective length excludes recognized padding.
    length_points = 1 if plain_len < 200 else 3 if plain_len < 500 else 6 if plain_len < 900 else 9 if plain_len < 1500 else 12
    coverage = keyword_groups(text, (
        ("定义", "是什么", "概念", "definition"),
        ("为什么", "动机", "背景", "问题", "目标"),
        ("原理", "机制", "过程", "步骤", "算法", "推导"),
        ("例子", "示例", "案例", "例如", "example"),
        ("局限", "边界", "适用", "不适用", "限制"),
    ))
    completeness = min(20, length_points + min(8, coverage * 2))

    # 3. Rigor, 15 points.
    rigor = min(10, keyword_groups(text, (
        ("假设", "条件", "前提"),
        ("定义", "定理", "命题", "性质"),
        ("推导", "证明", "因此", "从而"),
        ("区别", "对比", "vs", "关系"),
        ("误区", "反例", "边界", "局限"),
    )) * 2)
    rigor += 3 if math else 0
    rigor += 2 if re.search(r"(?m)^\|.+\|\s*$", text) and re.search(r"(?m)^\|\s*:?-+", text) else 0
    rigor = min(15, rigor)

    # 4. Evidence, 15 points. Internal links and a generic references heading do not qualify.
    URLs = URL_RE.findall(text)
    dois = DOI_RE.findall(text)
    # A source can be traceable without a URL, but a bare "参考资料" heading is
    # still worth zero. Require an ISBN/arXiv identifier or bibliographic detail.
    bibliographic = re.findall(
        r"(?:ISBN(?:-1[03])?\s*[:：]?\s*[0-9Xx-]{10,17}|arXiv\s*[:：]?\s*\d{4}\.\d{4,5}|"
        r"(?:作者|编者)\s*[:：].{2,40}(?:出版社|出版)|(?:第\s*[一二三四五六七八九十0-9]+\s*章).{0,40}(?:第\s*\d+\s*页|页码))",
        text,
        re.I,
    )
    identifiable = len(URLs) + len(dois) + len(bibliographic)
    evidence = 0 if identifiable == 0 else 5 if identifiable == 1 else 8 if identifiable == 2 else 11
    if identifiable and re.search(r"作者|出版社|出版年份|isbn|et al\.|arxiv|期刊|会议", text, re.I):
        evidence += 2
    if identifiable and re.search(r"页码|章节|chapter\s+\d|section\s+\d", text, re.I):
        evidence += 2
    evidence = min(15, evidence)

    # 5. Examples and independent verification, 10 points.
    verification = 0
    if re.search(r"例子|示例|案例|例如|算例|反例|example", text, re.I):
        verification += 3
    if code:
        verification += 3
        if re.search(r"assert|expected|输出|结果|测试|验证|print\(", "\n".join(code), re.I):
            verification += 2
    if re.search(r"练习|自测|证明|推导|实验|复现", text, re.I):
        verification += 2
    verification = min(10, verification)

    # 6. Knowledge graph, 10 points.
    valid = note.valid_links
    connection = 0 if valid == 0 else 3 if valid == 1 else 5 if valid <= 3 else 7 if valid <= 6 else 9
    if note.links and not note.broken_links:
        connection += 1
    connection = min(10, connection)

    # 7. Structure and maintenance, 10 points.
    structure = 0
    structure += 2 if re.search(r"(?m)^#\s+", text) else 0
    structure += 2 if len(headings) >= 3 else 0
    structure += 2 if note.frontmatter and any(key in note.frontmatter for key in ("type", "topic", "course", "tags")) else 0
    structure += 1 if re.search(r"(?m)^\s*[-*+]\s+", text) else 0
    structure += 1 if re.search(r"(?m)^\|.+\|\s*$", text) else 0
    structure += 2 if not placeholders and not note.broken_links and note.repeat_ratio < 0.3 else 0
    if note.within_repeated_removed:
        structure = max(0, structure - 2)
    structure = min(10, structure)

    note.dimensions = {
        "主题聚焦": grounding,
        "内容完整": completeness,
        "严谨性": rigor,
        "证据来源": evidence,
        "例证验证": verification,
        "知识连接": connection,
        "结构维护": structure,
    }
    raw_score = sum(note.dimensions.values())

    if note.appendix_removed:
        note.flags.append(f"已剔除批量附录{note.appendix_removed}字符")
        note.cap = min(note.cap, 75)
    if note.repeated_removed:
        note.flags.append(f"跨文件高频模板占比{note.repeat_ratio:.0%}")
    if note.within_repeated_removed:
        note.flags.append(f"篇内重复占比{note.within_repeat_ratio:.0%}")
    if risk_labels:
        note.flags.extend(risk_labels)
    if title_path_mismatch:
        note.flags.append(f"文件名与标题疑似错配({note.title_path_similarity:.0%})")
        note.cap = min(note.cap, 35)
    if placeholders:
        note.flags.append(f"占位/TODO {len(placeholders)}处")
        note.cap = min(note.cap, 30)
    if plain_len < 200:
        note.flags.append("去模板后有效正文不足200字")
        note.cap = min(note.cap, 20)
    elif plain_len < 500:
        note.flags.append("去模板后有效正文不足500字")
        note.cap = min(note.cap, 35)
    elif plain_len < 900:
        note.flags.append("去模板后有效正文不足900字")
        note.cap = min(note.cap, 50)
    if note.repeat_ratio >= 0.75:
        note.cap = min(note.cap, 25)
    elif note.repeat_ratio >= 0.5:
        note.cap = min(note.cap, 40)
    elif note.repeat_ratio >= 0.3:
        note.cap = min(note.cap, 55)
    if note.within_repeat_ratio >= 0.25:
        note.cap = min(note.cap, 50)
    elif note.within_repeat_ratio >= 0.10:
        note.cap = min(note.cap, 70)
    if "无意义伪公式" in risk_labels:
        note.cap = min(note.cap, 15)
    if any(label in risk_labels for label in ("通用高维模板", "通用离散数学模板", "通用梯度下降模板")):
        note.cap = min(note.cap, 30)
    elif risk_labels and note.repeat_ratio >= 0.3:
        note.cap = min(note.cap, 30)
    if "虚假完成度字段" in risk_labels:
        note.cap = min(note.cap, 60)
    if "LaTeX转义/控制字符损坏" in risk_labels:
        note.cap = min(note.cap, 45)
    if note.duplicate_group:
        note.flags.append("去模板后正文仍重复")
        note.cap = min(note.cap, 50)
    if note.broken_links:
        note.flags.append(f"断链{len(note.broken_links)}个")
    if evidence == 0:
        note.flags.append("无可定位来源")
        note.cap = min(note.cap, 75)
    if verification < 4:
        note.flags.append("缺少贴题例证/验证")
    if anchor_hits == 0 and len(anchor) >= 2:
        note.flags.append("有效正文缺少主题锚点")

    note.score = min(raw_score, note.cap)
    note.grade = grade(note.score)

    if note.appendix_removed or note.repeat_ratio >= 0.3 or note.within_repeated_removed or risk_labels or title_path_mismatch:
        note.fixes.append("删除通用模板，按本主题重写定义、机制和边界")
    if placeholders or plain_len < 500:
        note.fixes.append("先补齐真实正文，未完成前保持草稿状态")
    if evidence == 0:
        note.fixes.append("补可定位教材章节、论文 DOI 或权威文档")
    if verification < 4:
        note.fixes.append("加入贴题正反例、推导或可复现实验")
    if note.broken_links:
        note.fixes.append("修复或删除断链")
    if "LaTeX转义/控制字符损坏" in risk_labels:
        note.fixes.insert(0, "修复控制字符和损坏的 LaTeX 转义后再复核公式")
    note.fixes = note.fixes[:3]


def percentile(values: list[int], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = (len(ordered) - 1) * p
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = index - lower
    return round(ordered[lower] * (1 - fraction) + ordered[upper] * fraction, 1)


def summarize(notes: list[Note], inventory: dict[str, int]) -> dict:
    targets = [note for note in notes if note.category == "知识点"]
    scores = [note.score for note in targets]
    distribution = Counter(
        "90-100" if score >= 90 else "80-89" if score >= 80 else "70-79" if score >= 70 else "60-69" if score >= 60 else "<60"
        for score in scores
    )
    return {
        "active_note_files": sum(count for key, count in inventory.items() if key != "排除的系统脚本/归档"),
        "active_inventory": inventory,
        "scanned": len(notes),
        "knowledge_notes": len(targets),
        "average": round(sum(scores) / len(scores), 1) if scores else 0,
        "median": round(median(scores), 1) if scores else 0,
        "p25": percentile(scores, 0.25),
        "p75": percentile(scores, 0.75),
        "distribution": dict(distribution),
        "category_counts": dict(Counter(note.category for note in notes)),
        "appendix_polluted": sum(bool(note.appendix_removed) for note in targets),
        "cross_template": sum(note.repeat_ratio >= 0.3 for note in targets),
        "within_file_repetition": sum(bool(note.within_repeated_removed) for note in targets),
        "semantic_risk": sum(any(pattern.search(note.raw) for _, pattern in GENERIC_RISK_PATTERNS) for note in targets),
        "latex_control_corruption": sum(
            bool(dict(GENERIC_RISK_PATTERNS)["LaTeX转义/控制字符损坏"].search(note.raw)) for note in targets
        ),
        "title_path_mismatch": sum(
            note.title_path_similarity < 0.18
            and len(title_anchor(note.path.stem)) >= 4
            and len(title_anchor(note.frontmatter.get("topic") or note.frontmatter.get("title") or note.title)) >= 4
            for note in targets
        ),
        "placeholders": sum(bool(PLACEHOLDER_RE.search(visible_text(note.effective_body))) for note in targets),
        "no_sources": sum(note.dimensions["证据来源"] == 0 for note in targets),
        "broken_notes": sum(bool(note.broken_links) for note in targets),
        "broken_links": sum(len(note.broken_links) for note in targets),
        "duplicates": sum(bool(note.duplicate_group) for note in targets),
    }


def md_link(note: Note) -> str:
    return f"[[{note.rel[:-3]}|{note.path.stem.replace('|', '-') }]]"


def write_csv(notes: list[Note]) -> None:
    fields = [
        "path", "subject", "category", "score", "grade", "cap",
        "主题聚焦", "内容完整", "严谨性", "证据来源", "例证验证", "知识连接", "结构维护",
        "去模板有效正文字符", "原始字符", "剔除批量附录字符", "剔除跨文件模板字符", "跨文件模板占比",
        "剔除篇内重复字符", "篇内重复占比",
        "文件名标题相似度", "有效链接", "断链数", "重复组", "主要问题", "优先修复",
    ]
    with SCORES.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for note in sorted(notes, key=lambda item: (item.category != "知识点", item.score, item.rel)):
            writer.writerow({
                "path": note.rel,
                "subject": note.subject,
                "category": note.category,
                "score": note.score,
                "grade": note.grade,
                "cap": note.cap,
                **note.dimensions,
                "去模板有效正文字符": len(visible_text(note.effective_body)),
                "原始字符": len(note.raw),
                "剔除批量附录字符": note.appendix_removed,
                "剔除跨文件模板字符": note.repeated_removed,
                "跨文件模板占比": f"{note.repeat_ratio:.1%}",
                "剔除篇内重复字符": note.within_repeated_removed,
                "篇内重复占比": f"{note.within_repeat_ratio:.1%}",
                "文件名标题相似度": f"{note.title_path_similarity:.1%}",
                "有效链接": note.valid_links,
                "断链数": len(note.broken_links),
                "重复组": note.duplicate_group,
                "主要问题": "；".join(note.flags),
                "优先修复": "；".join(note.fixes),
            })


def write_json(notes: list[Note], summary: dict) -> None:
    payload = {
        "summary": summary,
        "rubric": {
            "主题聚焦": 20,
            "内容完整": 20,
            "严谨性": 15,
            "证据来源": 15,
            "例证验证": 10,
            "知识连接": 10,
            "结构维护": 10,
        },
        "notes": [
            {
                "path": note.rel,
                "subject": note.subject,
                "category": note.category,
                "score": note.score,
                "grade": note.grade,
                "cap": note.cap,
                "dimensions": note.dimensions,
                "effective_characters": len(visible_text(note.effective_body)),
                "appendix_removed": note.appendix_removed,
                "repeated_removed": note.repeated_removed,
                "repeat_ratio": round(note.repeat_ratio, 4),
                "within_repeated_removed": note.within_repeated_removed,
                "within_repeat_ratio": round(note.within_repeat_ratio, 4),
                "valid_links": note.valid_links,
                "broken_links": note.broken_links,
                "duplicate_group": note.duplicate_group,
                "title_path_similarity": round(note.title_path_similarity, 4),
                "flags": note.flags,
                "fixes": note.fixes,
            }
            for note in sorted(notes, key=lambda item: (item.category != "知识点", item.score, item.rel))
        ],
    }
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_report(notes: list[Note], summary: dict) -> None:
    targets = [note for note in notes if note.category == "知识点"]
    worst = sorted(targets, key=lambda item: (item.score, item.rel))[:60]
    best = sorted(targets, key=lambda item: (-item.score, item.rel))[:20]
    groups: defaultdict[str, list[Note]] = defaultdict(list)
    for note in targets:
        groups[note.subject].append(note)
    subjects = sorted(
        ((sum(note.score for note in group) / len(group), subject, group) for subject, group in groups.items()),
        key=lambda item: item[0],
    )

    lines = [
        "# 知识点笔记全量极严审计",
        "",
        f"> 审计日期：{date.today().isoformat()}。全库纳管范围为用户可见 Markdown；评分主体为 `02-Knowledge/🧠 学习系统/**/*.md`。",
        "> `.git`、`.obsidian`、`.recovery-hold`、临时同步目录、系统脚本与历史归档不纳入；评分前先剔除已知批量附录和跨文件高频复用段落。",
        "",
        "## 总结论",
        "",
        f"- 全库纳管 **{summary['active_note_files']}** 个活跃 Markdown；其中知识学习区逐文件读取 **{summary['scanned']}** 个，严格识别出 **{summary['knowledge_notes']}** 篇知识点笔记。",
        f"- 平均分 **{summary['average']} / 100**，中位数 **{summary['median']}**；P25/P75 为 **{summary['p25']} / {summary['p75']}**。",
        f"- 批量附录污染 **{summary['appendix_polluted']}** 篇；跨文件模板占比不低于 30% 的有 **{summary['cross_template']}** 篇；存在实质篇内重复 **{summary['within_file_repetition']}** 篇；命中通用模板/伪公式等高风险信号 **{summary['semantic_risk']}** 篇，其中 LaTeX 转义/控制字符损坏 **{summary['latex_control_corruption']}** 篇；文件名—标题疑似错配 **{summary['title_path_mismatch']}** 篇。",
        f"- 无可定位来源 **{summary['no_sources']}** 篇；明确占位 **{summary['placeholders']}** 篇；含断链 **{summary['broken_notes']}** 篇，共 **{summary['broken_links']}** 个断链。",
        "- 旧报告所称的 9.59/10 不可信：大量不相关公式、PyTorch 代码和自测模板被重复灌入不同学科，制造了虚假的完整度。",
        "",
        "## 分数分布",
        "",
        "| 分数段 | 数量 | 占比 | 严格解释 |",
        "|:---|---:|---:|:---|",
    ]
    interpretations = {
        "90-100": "A 卓越：接近可长期依赖，仍需人工事实复核",
        "80-89": "B 良好：主体可靠，但存在证据或边界缺口",
        "70-79": "C 合格：可学习使用，不宜无核验引用",
        "60-69": "D 勉强：形式基本齐，知识闭环不足",
        "<60": "F 不合格：模板、错配、占位、缺证据或内容空洞",
    }
    for bucket in ("90-100", "80-89", "70-79", "60-69", "<60"):
        count = summary["distribution"].get(bucket, 0)
        ratio = count / summary["knowledge_notes"] * 100 if summary["knowledge_notes"] else 0
        lines.append(f"| **{bucket}** | {count} | {ratio:.1f}% | {interpretations[bucket]} |")

    lines.extend([
        "",
        "## 评分口径",
        "",
        "| 维度 | 分值 | 严苛要求 |",
        "|:---|---:|:---|",
        "| 主题聚焦 | 20 | 内容必须真的解释标题主题；通用高维/梯度下降话术、伪公式和虚假完成度字段重罚 |",
        "| 内容完整 | 20 | 定义、动机、机制、例子、适用边界形成闭环；按去模板后的有效正文计 |",
        "| 严谨性 | 15 | 有成立条件、定义/定理、推导或因果链、对比和局限 |",
        "| 证据来源 | 15 | 可定位的权威链接、DOI、书籍章节/页码、作者出版信息 |",
        "| 例证验证 | 10 | 贴题正反例、证明、可运行代码及输出、实验或复现 |",
        "| 知识连接 | 10 | 有效双链与完整依赖关系；断链不能算连接质量 |",
        "| 结构维护 | 10 | 可检索元数据、层级清楚、无占位、无模板污染、无断链 |",
        "",
        "### 强制封顶",
        "",
        "- 明确占位/TODO：最高 30 分。",
        "- 去模板后有效正文少于 200/500/900 字：分别最高 20/35/50 分。",
        "- 跨文件高频模板占比达到 75%/50%/30%：分别最高 25/40/55 分。",
        "- 篇内重复占比达到 25%/10%：分别最高 50/70 分；重复段落先剔除再计正文。",
        "- 命中无意义伪公式：最高 15 分；模板高占比且存在主题错配风险：最高 30 分。",
        "- 文件名与正文主标题相似度低于 18%：疑似批量错配，最高 35 分。",
        "- 出现 `subagent_audit_score: 9–10` 等虚假完成度字段：最高 60 分，且该字段本身不加分。",
        "- 出现退格、换页、`\\text` 被写成制表符等 LaTeX 转义损坏：最高 45 分。",
        "",
        "## 全库扫描清单",
        "",
        "| 区域 | Markdown 数 | 处理方式 |",
        "|:---|---:|:---|",
    ])
    for area, count in sorted(summary["active_inventory"].items()):
        treatment = "排除：系统脚本/历史归档" if area == "排除的系统脚本/归档" else "纳管；仅知识点进入评分"
        lines.append(f"| {area} | {count} | {treatment} |")

    lines.extend([
        "",
        "## 文件分类",
        "",
        "| 类型 | 数量 | 是否纳入知识点均分 |",
        "|:---|---:|:---|",
    ])
    for category in ("知识点", "导航/索引", "题型/错题", "练习/项目", "计划/模板", "资料/文献", "辅助系统", "其他非知识点"):
        lines.append(f"| {category} | {summary['category_counts'].get(category, 0)} | {'是' if category == '知识点' else '否'} |")

    lines.extend([
        "",
        "## 各学科排名",
        "",
        "| 学科 | 知识点数 | 平均分 | <60 | 无来源 | 模板污染≥30% |",
        "|:---|---:|---:|---:|---:|---:|",
    ])
    for average, subject, group in subjects:
        lines.append(
            f"| {subject} | {len(group)} | **{average:.1f}** | {sum(note.score < 60 for note in group)} | "
            f"{sum(note.dimensions['证据来源'] == 0 for note in group)} | {sum(note.repeat_ratio >= 0.3 for note in group)} |"
        )

    lines.extend([
        "",
        "## 最差 60 篇知识点",
        "",
        "| # | 笔记 | 学科 | 分数 | 主要问题 | 优先修复 |",
        "|---:|:---|:---|---:|:---|:---|",
    ])
    for index, note in enumerate(worst, 1):
        lines.append(
            f"| {index} | {md_link(note)} | {note.subject} | **{note.score}** | "
            f"{'；'.join(note.flags[:3]) or '深度不足'} | {'；'.join(note.fixes[:2])} |"
        )

    lines.extend([
        "",
        "## 相对最高 20 篇",
        "",
        "> 这是静态规则下的相对高分，不代表公式、事实和代码已逐条通过领域专家核验。",
        "",
        "| # | 笔记 | 学科 | 分数 | 自动规则仍发现的短板 |",
        "|---:|:---|:---|---:|:---|",
    ])
    for index, note in enumerate(best, 1):
        lines.append(
            f"| {index} | {md_link(note)} | {note.subject} | **{note.score}** | "
            f"{'；'.join(note.flags[:3]) or '未发现明显静态缺陷'} |"
        )

    lines.extend([
        "",
        "## 最严厉诊断",
        "",
        "1. **先承认虚假完成度**：带 9.5/10、mastered 或完整章节结构，不等于内容正确。当前最大问题是批量生成造成的‘看起来很完整’。",
        "2. **删除污染再重写**：不要在现有通用模板上继续补字；先删去与主题无关的经验风险公式、PyTorch 张量代码和万能类比。",
        "3. **一主题一主卡**：重复笔记应合并为 canonical 主卡，其他位置只保留有语义的链接，避免多个互相矛盾版本。",
        "4. **补来源和验证**：定义/定理必须落到教材章节或原始论文；算法必须给贴题输入、输出、复杂度和失败案例。",
        "5. **最后才做样式**：Frontmatter、表格、emoji 和长目录是检索工具，不是知识质量本身。",
        "",
        "## 审计边界",
        "",
        "- 本次逐文件读取全部正文并执行静态结构、重复、污染、来源、链接和主题锚定审计。",
        f"- 未联网逐条核验 {summary['knowledge_notes']} 篇知识点内的每个事实和公式；因此高分仍不是事实正确性的担保。",
        "- 对已抽样发现的明显主题错配（如以梯度下降解释向量空间、以抽象二元组解释 Dinic）已通过模板风险规则统一降分。",
        f"- 每篇完整明细：`{SCORES.name}`；机器可读结果：`{DATA.name}`。",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if not ROOT.exists():
        raise SystemExit(f"Knowledge root not found: {ROOT}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    notes = load_notes()
    inventory = active_markdown_inventory()
    remove_cross_file_templates(notes)
    resolve_links(notes)
    for note in notes:
        score_note(note)
    summary = summarize(notes, inventory)
    write_csv(notes)
    write_json(notes, summary)
    write_report(notes, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(REPORT)
    print(SCORES)
    print(DATA)


if __name__ == "__main__":
    main()
