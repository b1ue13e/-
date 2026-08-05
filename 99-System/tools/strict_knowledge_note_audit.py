from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from statistics import median


VAULT = Path(__file__).resolve().parents[2]
KNOWLEDGE_ROOT = VAULT / "02-Knowledge" / "🧠 学习系统"
OUTPUT_DIR = VAULT / "99-System" / "🗄️ 归档" / "知识库审计"
REPORT_PATH = OUTPUT_DIR / "knowledge_notes_rigorous_audit_2026-07-31.md"
CSV_PATH = OUTPUT_DIR / "knowledge_notes_rigorous_scores_2026-07-31.csv"
JSON_PATH = OUTPUT_DIR / "knowledge_notes_rigorous_scores_2026-07-31.json"

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
URL_RE = re.compile(r"https?://[^\s)>\]]+", re.I)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
HEADING_RE = re.compile(r"(?m)^#{1,6}\s+(.+?)\s*$")
CODE_RE = re.compile(r"```([^\n`]*)\n(.*?)```", re.S)
MATH_BLOCK_RE = re.compile(r"\$\$(.+?)\$\$", re.S)

# These exact sections were batch-appended to the vault. The phrases and examples
# are topic-independent, so counting them as note substance would reward padding.
INJECTED_SECTION_MARKERS = (
    "## 💡 直觉心智模型与痛点背景",
    "## 📐 形式化定义与数学推导 (LaTeX)",
    "## 💻 核心代码实现与张量维度追踪 (Shape Tracing)",
    "## 🔗 知识连接与闭卷自测",
    "## ⚠️ 常见误区与对比矩阵",
)
INJECTION_SIGNATURES = (
    "信息调度过滤器",
    "传统方法在处理高维空间、动态序列或非线性特征映射时存在严重的表达能力瓶颈",
    "优化目标定义为最小化经验风险",
    "标准 Python 核心实现，附带严谨的 Tensor Shape Tracing",
    "请在不查阅资料的前提下，尝试回答以下问题",
)
PLACEHOLDER_PATTERNS = (
    r"待补全", r"待补充", r"TODO", r"TBD", r"占位", r"暂无内容",
    r"后续补充", r"coming soon", r"未完成",
)


@dataclass
class Note:
    path: Path
    rel: str
    subject: str
    title: str
    raw: str
    frontmatter: dict[str, str]
    body: str
    clean_body: str
    note_type: str
    injection_removed_chars: int
    paragraphs: list[str] = field(default_factory=list)
    repeat_ratio: float = 0.0
    duplicate_group: str = ""
    links: list[str] = field(default_factory=list)
    valid_links: int = 0
    broken_links: list[str] = field(default_factory=list)
    score: int = 0
    grade: str = ""
    cap: int = 100
    dimensions: dict[str, int] = field(default_factory=dict)
    flags: list[str] = field(default_factory=list)
    fixes: list[str] = field(default_factory=list)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not match:
        return {}, text
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if item:
            data[item.group(1).lower()] = item.group(2).strip().strip("'\"")
    return data, text[match.end():]


def remove_injected_padding(body: str) -> tuple[str, int]:
    positions = [body.find(marker) for marker in INJECTED_SECTION_MARKERS]
    positions = [position for position in positions if position >= 0]
    has_signature = any(signature in body for signature in INJECTION_SIGNATURES)
    if not positions or not has_signature:
        return body, 0
    cut = min(positions)
    return body[:cut].rstrip(), len(body) - cut


def visible_text(text: str) -> str:
    text = CODE_RE.sub(" ", text)
    text = re.sub(r"\$\$.+?\$\$", " ", text, flags=re.S)
    text = re.sub(r"`[^`]+`", " ", text)
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), text)
    text = re.sub(r"(?m)^\s*[-*+>]\s*", "", text)
    text = re.sub(r"(?m)^#{1,6}\s*", "", text)
    text = re.sub(r"[*_~|>#]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_paragraph(paragraph: str, title: str) -> str:
    text = paragraph.lower().replace(title.lower(), "<title>")
    text = re.sub(r"\[\[[^\]]+\]\]", "<link>", text)
    text = re.sub(r"https?://\S+", "<url>", text)
    text = re.sub(r"\d+(?:\.\d+)?", "<num>", text)
    text = re.sub(r"[^\w\u4e00-\u9fff<>]+", "", text)
    return text


def extract_paragraphs(text: str, title: str) -> list[str]:
    result = []
    for block in re.split(r"\n\s*\n", text):
        normalized = normalize_paragraph(block, title)
        if len(normalized) >= 80:
            result.append(normalized)
    return result


def classify_note(path: Path, frontmatter: dict[str, str], body: str) -> str:
    name = path.stem
    declared = " ".join(frontmatter.get(k, "") for k in ("type", "kind", "tags")).lower()
    if re.search(r"moc|index|索引|地图", declared) or re.search(r"学习路径|知识地图|总索引|入口|导航$|维度$|板块", name):
        return "导航/索引"
    if re.search(r"错题|复盘|实践|项目|练习|题库|清单|计划|模板", name):
        return "练习/工作台"
    if any(re.search(pattern, body, re.I) for pattern in PLACEHOLDER_PATTERNS):
        return "占位稿"
    return "知识点"


def load_notes() -> list[Note]:
    notes = []
    for path in sorted(KNOWLEDGE_ROOT.rglob("*.md")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        frontmatter, body = parse_frontmatter(raw)
        clean, removed = remove_injected_padding(body)
        rel_path = path.relative_to(VAULT).as_posix()
        relative_parts = path.relative_to(KNOWLEDGE_ROOT).parts
        subject = relative_parts[0] if len(relative_parts) > 1 else "根目录"
        title_match = re.search(r"(?m)^#\s+(.+?)\s*$", clean)
        title = title_match.group(1).strip() if title_match else path.stem
        note = Note(
            path=path,
            rel=rel_path,
            subject=subject,
            title=title,
            raw=raw,
            frontmatter=frontmatter,
            body=body,
            clean_body=clean,
            note_type=classify_note(path, frontmatter, clean),
            injection_removed_chars=removed,
        )
        note.paragraphs = extract_paragraphs(clean, path.stem)
        note.links = [target.strip() for target in WIKILINK_RE.findall(clean)]
        notes.append(note)
    return notes


def resolve_links(notes: list[Note]) -> None:
    rel_keys: set[str] = set()
    stems: defaultdict[str, list[str]] = defaultdict(list)
    suffixes: set[str] = set()
    for note in notes:
        rel_no_ext = note.rel[:-3].lower()
        rel_keys.add(rel_no_ext)
        suffixes.add(rel_no_ext.removeprefix("02-knowledge/"))
        suffixes.add(rel_no_ext.removeprefix("02-knowledge/🧠 学习系统/"))
        stems[note.path.stem.lower()].append(rel_no_ext)

    for note in notes:
        for original_target in note.links:
            target = original_target.replace("\\", "/").strip().removesuffix(".md").lower()
            target = target.removeprefix("./").strip("/")
            valid = (
                target in rel_keys
                or target in suffixes
                or target.removeprefix("02-knowledge/") in suffixes
                or target.split("/")[-1] in stems
                or any(key.endswith("/" + target) for key in rel_keys)
            )
            if valid:
                note.valid_links += 1
            else:
                note.broken_links.append(original_target)


def analyze_repetition(notes: list[Note]) -> None:
    paragraph_docs: Counter[str] = Counter()
    for note in notes:
        paragraph_docs.update(set(note.paragraphs))

    skeleton_groups: defaultdict[str, list[Note]] = defaultdict(list)
    for note in notes:
        repeated_chars = sum(len(p) for p in note.paragraphs if paragraph_docs[p] >= 10)
        all_chars = sum(len(p) for p in note.paragraphs)
        note.repeat_ratio = repeated_chars / all_chars if all_chars else 0.0
        skeleton = "|".join(note.paragraphs)
        if skeleton:
            digest = hashlib.sha1(skeleton.encode("utf-8")).hexdigest()[:10]
            skeleton_groups[digest].append(note)

    for digest, group in skeleton_groups.items():
        if len(group) < 2:
            continue
        for note in group:
            note.duplicate_group = f"{digest} ({len(group)}篇)"


def count_keyword_groups(text: str, groups: tuple[tuple[str, ...], ...]) -> int:
    return sum(1 for group in groups if any(word.lower() in text.lower() for word in group))


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
    text = note.clean_body
    plain = visible_text(text)
    plain_len = len(plain)
    headings = HEADING_RE.findall(text)
    urls = URL_RE.findall(text)
    dois = DOI_RE.findall(text)
    code_blocks = [body for lang, body in CODE_RE.findall(text) if body.strip()]
    math_blocks = [item for item in MATH_BLOCK_RE.findall(text) if item.strip()]
    placeholder_hits = sum(bool(re.search(pattern, text, re.I)) for pattern in PLACEHOLDER_PATTERNS)

    # 1. Substance and completeness, 25 points.
    length_score = 2 if plain_len < 200 else 5 if plain_len < 500 else 9 if plain_len < 900 else 13 if plain_len < 1500 else 16
    coverage_groups = (
        ("定义", "是什么", "概念", "definition"),
        ("为什么", "动机", "背景", "问题", "目标"),
        ("原理", "机制", "过程", "步骤", "算法", "推导"),
        ("例子", "示例", "案例", "例如", "example"),
        ("局限", "边界", "适用", "不适用", "限制"),
    )
    substance = min(25, length_score + min(9, count_keyword_groups(text, coverage_groups) * 2))

    # 2. Rigor and precision, 20 points. Math/code are evidence, not universal requirements.
    rigor_groups = (
        ("假设", "条件", "前提"),
        ("定义", "定理", "命题", "性质"),
        ("推导", "证明", "因此", "由于", "从而"),
        ("区别", "对比", "vs", "关系"),
        ("误区", "反例", "边界", "局限", "注意"),
    )
    rigor = min(15, count_keyword_groups(text, rigor_groups) * 3)
    if math_blocks:
        rigor += 3
    if re.search(r"(?m)^\|.+\|\s*$", text) and re.search(r"(?m)^\|\s*:?-+", text):
        rigor += 2
    rigor = min(20, rigor)

    # 3. Evidence and sources, 15 points.
    source_heading = bool(re.search(r"参考|来源|文献|bibliograph|reference", text, re.I))
    identifiable_citations = len(urls) + len(dois)
    evidence = 0
    if identifiable_citations == 1:
        evidence = 6
    elif identifiable_citations == 2:
        evidence = 9
    elif identifiable_citations >= 3:
        evidence = 12
    elif source_heading:
        evidence = 2
    if re.search(r"作者|出版社|出版|et al\.|arxiv|doi|isbn|期刊|会议", text, re.I):
        evidence += 3
    evidence = min(15, evidence)

    # 4. Examples and verifiability, 15 points.
    verification = 0
    if code_blocks:
        verification += 5
        if re.search(r"assert|print\(|expected|输出|结果|测试", "\n".join(code_blocks), re.I):
            verification += 3
    if re.search(r"例子|示例|案例|例如|算例|example", text, re.I):
        verification += 4
    if re.search(r"练习|自测|问题|验证|复现|实验", text, re.I):
        verification += 3
    verification = min(15, verification)

    # 5. Knowledge graph quality, 10 points.
    valid = note.valid_links
    connection = 0 if valid == 0 else 3 if valid == 1 else 5 if valid <= 3 else 7 if valid <= 6 else 9
    if note.links and not note.broken_links:
        connection += 1
    connection = min(10, connection)

    # 6. Structure and retrieval, 10 points.
    structure = 0
    if re.search(r"(?m)^#\s+", text):
        structure += 2
    if len(headings) >= 3:
        structure += 2
    if note.frontmatter:
        structure += 1
        if any(key in note.frontmatter for key in ("tags", "course", "topic", "type")):
            structure += 1
    if re.search(r"(?m)^\s*[-*+]\s+", text):
        structure += 1
    if re.search(r"(?m)^\|.+\|\s*$", text):
        structure += 1
    empty_heading_count = sum(
        1 for match in re.finditer(r"(?m)^(#{2,6})\s+.+$", text)
        if not text[match.end():].lstrip("\n").strip() or re.match(r"^#{1,6}\s+", text[match.end():].lstrip("\n"))
    )
    if empty_heading_count == 0:
        structure += 2
    structure = min(10, structure)

    # 7. Maintenance health, 5 points.
    health = 5
    if placeholder_hits:
        health -= 2
    if note.broken_links:
        health -= min(2, len(note.broken_links))
    if note.repeat_ratio >= 0.5 or note.duplicate_group:
        health -= 2
    health = max(0, health)

    note.dimensions = {
        "内容完整性": substance,
        "严谨性": rigor,
        "证据来源": evidence,
        "例证验证": verification,
        "知识连接": connection,
        "结构检索": structure,
        "维护健康": health,
    }
    raw_score = sum(note.dimensions.values())

    if note.injection_removed_chars:
        note.flags.append(f"批量注水{note.injection_removed_chars}字符")
    if placeholder_hits:
        note.flags.append("存在占位/TODO")
        note.cap = min(note.cap, 35)
    if plain_len < 200:
        note.flags.append("有效正文不足200字")
        note.cap = min(note.cap, 25)
    elif plain_len < 500:
        note.flags.append("有效正文不足500字")
        note.cap = min(note.cap, 45)
    if note.repeat_ratio >= 0.5:
        note.flags.append(f"高频模板段占比{note.repeat_ratio:.0%}")
        note.cap = min(note.cap, 55)
    if note.duplicate_group:
        note.flags.append("内容骨架重复")
        note.cap = min(note.cap, 60)
    if note.broken_links:
        note.flags.append(f"断链{len(note.broken_links)}个")
    if evidence <= 2:
        note.flags.append("无可核验来源")
    if not code_blocks and not re.search(r"例子|示例|案例|算例|证明|推导", text):
        note.flags.append("无例证/推导")

    note.score = min(raw_score, note.cap)
    note.grade = grade(note.score)

    if placeholder_hits or plain_len < 500:
        note.fixes.append("先完成真实正文，删除占位骨架")
    if note.injection_removed_chars:
        note.fixes.append("删除与主题无关的批量通用段落")
    if evidence <= 2:
        note.fixes.append("补充可定位的书籍章节、论文 DOI 或权威链接")
    if verification < 7:
        note.fixes.append("加入贴合主题的例题、反例、推导或可运行验证")
    if note.broken_links:
        note.fixes.append("修复断链")
    if rigor < 9:
        note.fixes.append("补充定义、成立条件、边界与易错点")
    note.fixes = note.fixes[:3]


def summarize(notes: list[Note]) -> dict:
    knowledge_notes = [note for note in notes if note.note_type == "知识点"]
    scores = [note.score for note in knowledge_notes]
    all_scores = [note.score for note in notes]
    distribution = Counter(
        "90-100" if score >= 90 else "80-89" if score >= 80 else "70-79" if score >= 70 else "60-69" if score >= 60 else "<60"
        for score in scores
    )
    return {
        "scanned": len(notes),
        "knowledge_notes": len(knowledge_notes),
        "average": round(sum(scores) / len(scores), 1) if scores else 0,
        "median": round(median(scores), 1) if scores else 0,
        "all_average": round(sum(all_scores) / len(all_scores), 1) if all_scores else 0,
        "distribution": dict(distribution),
        "injected": sum(bool(note.injection_removed_chars) for note in notes),
        "placeholders": sum(note.note_type == "占位稿" for note in notes),
        "broken_notes": sum(bool(note.broken_links) for note in notes),
        "broken_links": sum(len(note.broken_links) for note in notes),
        "no_sources": sum(note.dimensions["证据来源"] <= 2 for note in knowledge_notes),
        "duplicate_skeletons": sum(bool(note.duplicate_group) for note in notes),
        "type_counts": dict(Counter(note.note_type for note in notes)),
    }


def write_csv(notes: list[Note]) -> None:
    columns = [
        "path", "subject", "type", "score", "grade", "cap",
        "内容完整性", "严谨性", "证据来源", "例证验证", "知识连接", "结构检索", "维护健康",
        "有效正文字符", "原始字符", "移除注水字符", "有效链接", "断链数", "重复段落占比",
        "重复组", "问题", "优先修复",
    ]
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for note in sorted(notes, key=lambda item: (item.score, item.rel)):
            writer.writerow({
                "path": note.rel,
                "subject": note.subject,
                "type": note.note_type,
                "score": note.score,
                "grade": note.grade,
                "cap": note.cap,
                **note.dimensions,
                "有效正文字符": len(visible_text(note.clean_body)),
                "原始字符": len(note.raw),
                "移除注水字符": note.injection_removed_chars,
                "有效链接": note.valid_links,
                "断链数": len(note.broken_links),
                "重复段落占比": f"{note.repeat_ratio:.1%}",
                "重复组": note.duplicate_group,
                "问题": "；".join(note.flags),
                "优先修复": "；".join(note.fixes),
            })


def md_link(note: Note) -> str:
    target = note.rel[:-3]
    label = note.path.stem.replace("|", "-")
    return f"[[{target}|{label}]]"


def write_report(notes: list[Note], summary: dict) -> None:
    knowledge = [note for note in notes if note.note_type == "知识点"]
    worst = sorted(knowledge, key=lambda item: (item.score, item.rel))[:50]
    best = sorted(knowledge, key=lambda item: (-item.score, item.rel))[:20]
    subject_rows = []
    grouped: defaultdict[str, list[Note]] = defaultdict(list)
    for note in knowledge:
        grouped[note.subject].append(note)
    for subject, group in grouped.items():
        subject_rows.append((sum(note.score for note in group) / len(group), subject, group))
    subject_rows.sort()

    lines = [
        "# 知识点笔记全量严苛审计（去模板注水版）",
        "",
        f"> 审计日期：{date.today().isoformat()}。扫描范围：`02-Knowledge/🧠 学习系统/**/*.md`。",
        "> 评分对象是去除可识别批量通用段落后的真实内容，不因字数、代码围栏或固定模板自动给高分。",
        "",
        "## 结论",
        "",
        f"- 扫描文件：**{summary['scanned']}** 篇；其中严格识别为知识点笔记 **{summary['knowledge_notes']}** 篇。",
        f"- 知识点平均分：**{summary['average']} / 100**；中位数：**{summary['median']}**。全目录平均分：**{summary['all_average']}**。",
        f"- 识别到批量无关内容：**{summary['injected']}** 篇；占位稿：**{summary['placeholders']}** 篇。",
        f"- 无可核验来源的知识点：**{summary['no_sources']}** 篇；含断链文件：**{summary['broken_notes']}** 篇，共 **{summary['broken_links']}** 个断链。",
        f"- 内容骨架重复：**{summary['duplicate_skeletons']}** 篇。旧报告中的 9.59/10 不能成立，它主要奖励了批量补入的相同公式、代码和自测模板。",
        "",
        "## 评级分布（知识点）",
        "",
        "| 分数段 | 数量 | 占比 | 严格解释 |",
        "|:---|---:|---:|:---|",
    ]
    labels = {
        "90-100": "A 卓越：可作为长期可信知识资产",
        "80-89": "B 良好：少量证据或边界缺口",
        "70-79": "C 合格：能用，但不可直接依赖",
        "60-69": "D 勉强：结构存在，知识闭环不足",
        "<60": "F 不合格：占位、注水、缺证据或内容空洞",
    }
    for bucket in ("90-100", "80-89", "70-79", "60-69", "<60"):
        count = summary["distribution"].get(bucket, 0)
        ratio = count / summary["knowledge_notes"] * 100 if summary["knowledge_notes"] else 0
        lines.append(f"| **{bucket}** | {count} | {ratio:.1f}% | {labels[bucket]} |")

    lines.extend([
        "",
        "## 评分标准",
        "",
        "| 维度 | 分值 | 严格要求 |",
        "|:---|---:|:---|",
        "| 内容完整性 | 25 | 定义、动机、机制、例子、适用边界形成闭环；字数只作为最低证据 |",
        "| 严谨性 | 20 | 明确概念、成立条件、因果/推导、对比、局限；数学和代码按主题需要，不是一刀切 |",
        "| 证据来源 | 15 | 可定位的权威链接、DOI、书籍章节、作者/出版信息；只有‘参考资料’标题不得高分 |",
        "| 例证验证 | 15 | 贴合主题的例题、反例、推导、实验、输出或测试 |",
        "| 知识连接 | 10 | 有效双链及其完整性；断链扣维护分 |",
        "| 结构检索 | 10 | 标题层级、元数据、列表/表格、无空章节 |",
        "| 维护健康 | 5 | 无 TODO/占位、无高频模板、无重复骨架、无断链 |",
        "",
        "### 强制封顶",
        "",
        "- 明示占位/TODO：最高 35 分。",
        "- 去注水后有效正文少于 200 字：最高 25 分；少于 500 字：最高 45 分。",
        "- 高频模板段占正文一半以上：最高 55 分；内容骨架重复：最高 60 分。",
        "",
        "## 文件类型盘点",
        "",
        "| 类型 | 数量 | 说明 |",
        "|:---|---:|:---|",
    ])
    type_notes = {
        "知识点": "主评分对象",
        "导航/索引": "不是知识点正文，仍计入全目录健康度",
        "练习/工作台": "按可执行性与真实内容扫描",
        "占位稿": "明确未完成，严格封顶",
    }
    for kind in ("知识点", "导航/索引", "练习/工作台", "占位稿"):
        lines.append(f"| {kind} | {summary['type_counts'].get(kind, 0)} | {type_notes[kind]} |")

    lines.extend([
        "",
        "## 各学科排名（知识点）",
        "",
        "| 学科 | 数量 | 平均分 | <60 | 无可核验来源 | 注水篇数 |",
        "|:---|---:|---:|---:|---:|---:|",
    ])
    for avg, subject, group in subject_rows:
        lines.append(
            f"| {subject} | {len(group)} | **{avg:.1f}** | "
            f"{sum(n.score < 60 for n in group)} | {sum(n.dimensions['证据来源'] <= 2 for n in group)} | "
            f"{sum(bool(n.injection_removed_chars) for n in group)} |"
        )

    lines.extend([
        "",
        "## 最差 50 篇知识点",
        "",
        "| # | 笔记 | 学科 | 分数 | 主要问题 | 优先修复 |",
        "|---:|:---|:---|---:|:---|:---|",
    ])
    for index, note in enumerate(worst, 1):
        lines.append(
            f"| {index} | {md_link(note)} | {note.subject} | **{note.score}** | "
            f"{'；'.join(note.flags[:3]) or '内容深度不足'} | {'；'.join(note.fixes[:2])} |"
        )

    lines.extend([
        "",
        "## 最高 20 篇知识点",
        "",
        "> 高分只表示相对当前规则更完整，未逐条外部事实核验，不等于事实零错误。",
        "",
        "| # | 笔记 | 学科 | 分数 | 主要短板 |",
        "|---:|:---|:---|---:|:---|",
    ])
    for index, note in enumerate(best, 1):
        lines.append(
            f"| {index} | {md_link(note)} | {note.subject} | **{note.score}** | "
            f"{'；'.join(note.flags[:2]) or '未发现自动规则可识别的重大短板'} |"
        )

    issue_counts = Counter(flag.split("个")[0] if flag.startswith("断链") else re.sub(r"\d+字符|\d+%", "", flag) for note in notes for flag in note.flags)
    lines.extend([
        "",
        "## 全库优先整改顺序",
        "",
        "1. **先停止模板化增肥**：批量通用公式、伪代码、‘信息调度过滤器’类比与主题无关，应删除而不是继续扩写。",
        "2. **清空占位债务**：占位稿先做保留/删除决策，再补真实定义、机制、例子和边界。",
        "3. **补证据链**：优先给核心概念增加可定位来源，不接受只有‘参考资料’标题或泛称教材。",
        "4. **补可验证内容**：数学主题给推导/反例，工程主题给最小运行例和输出，概念主题给正反例与适用边界。",
        "5. **修复断链与重复**：断链影响检索；重复骨架应合并为一篇主笔记，其他位置保留链接。",
        "",
        "## 自动审计边界",
        "",
        "- 本次是全量静态审计，逐文件读取并评分，但未对 2604 篇中的每一条知识陈述联网查证。",
        "- 自动规则可以可靠发现占位、模板注水、来源缺失、结构问题、重复和断链；不能替代领域专家对公式与事实的逐句校核。",
        f"- 全量逐文件明细见 `{CSV_PATH.name}`；机器可读结果见 `{JSON_PATH.name}`。",
        "",
        "## 问题计数（辅助）",
        "",
    ])
    for issue, count in issue_counts.most_common(12):
        lines.append(f"- {issue}：{count} 篇")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_json(notes: list[Note], summary: dict) -> None:
    payload = {
        "summary": summary,
        "rubric": {
            "内容完整性": 25,
            "严谨性": 20,
            "证据来源": 15,
            "例证验证": 15,
            "知识连接": 10,
            "结构检索": 10,
            "维护健康": 5,
        },
        "notes": [
            {
                "path": note.rel,
                "subject": note.subject,
                "type": note.note_type,
                "score": note.score,
                "grade": note.grade,
                "cap": note.cap,
                "dimensions": note.dimensions,
                "valid_links": note.valid_links,
                "broken_links": note.broken_links,
                "repeat_ratio": round(note.repeat_ratio, 4),
                "duplicate_group": note.duplicate_group,
                "injection_removed_chars": note.injection_removed_chars,
                "flags": note.flags,
                "fixes": note.fixes,
            }
            for note in sorted(notes, key=lambda item: (item.score, item.rel))
        ],
    }
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    if not KNOWLEDGE_ROOT.exists():
        raise SystemExit(f"Knowledge root does not exist: {KNOWLEDGE_ROOT}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    notes = load_notes()
    resolve_links(notes)
    analyze_repetition(notes)
    for note in notes:
        score_note(note)
    summary = summarize(notes)
    write_csv(notes)
    write_json(notes, summary)
    write_report(notes, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(REPORT_PATH)
    print(CSV_PATH)
    print(JSON_PATH)


if __name__ == "__main__":
    main()
