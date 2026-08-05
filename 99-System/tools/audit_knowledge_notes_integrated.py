#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge Notes Harsh Audit Evaluator (Integrated)
Strictly audits knowledge cards against evidence, verification, grounding, rigor, and structure.
"""

from __future__ import annotations

import csv
import json
import math
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = Path(r"F:\-")
SCAN_ROOT = VAULT_ROOT / "02-Knowledge" / "🧠 学习系统"
OUTPUT_DIR = VAULT_ROOT / "99-System" / "🗄️ 归档" / "知识库审计"
OUTPUT_MD = OUTPUT_DIR / "knowledge_notes_integrated_audit_2026-07-31.md"
OUTPUT_CSV = OUTPUT_DIR / "knowledge_notes_integrated_scores_2026-07-31.csv"
OUTPUT_JSON = OUTPUT_DIR / "knowledge_notes_integrated_scores_2026-07-31.json"

EXCLUDED_PATH_PARTS = {
    ".git", ".obsidian", ".obsidian.disabled", ".recovery-hold", ".trash",
    ".pytest_cache", ".tmp.drivedownload", ".tmp.driveupload", "99-System",
    "templates", "📇 模板", "🗄️ 归档", "tools", "scratch"
}

MARKDOWN_EXTS = {".md", ".markdown"}

CODE_RE = re.compile(r"```([a-zA-Z0-9_+-]*)\n(.*?)```", re.S)
MATH_RE = re.compile(r"\$\$(.*?)\$\$|\$(.*?)\$", re.S)
HEADING_RE = re.compile(r"(?m)^#{1,6}\s+(.+)$")
LINK_RE = re.compile(r"\[\[([^\]\|]+)(?:\|[^\]]+)?\]\]")
URL_RE = re.compile(r"https?://[^\s><\"'\(\)]+")
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")

GENERIC_RISK_PATTERNS = (
    ("通用高维模板", re.compile(r"面对高维数据与复杂非线性关系|维度灾难与优化陷入局部极值")),
    ("通用离散数学模板", re.compile(r"将口头逻辑转化为形式化的语言与严密的证明框架|满足相应离散约束与代数公理")),
    ("通用梯度下降模板", re.compile(r"用局部导数指导全局迭代优化|放弃一步到位，改用泰勒展开一阶近似")),
    ("无意义伪公式", re.compile(r"CoreFormula\s*\(|TextFormula\s*\(|TODOFormula\s*\(", re.I)),
    ("虚假完成度字段", re.compile(r"subagent_audit_score\s*:\s*(?:9(?:\.\d+)?|10(?:\.0+)?)", re.I)),
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
    duplicate_group: str = ""
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
    raw_fm = match.group(1)
    body = text[match.end():]
    fm = {}
    for line in raw_fm.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip().lower()] = v.strip().strip("\"'")
    return fm, raw_fm, body

def split_appendix(text: str) -> tuple[str, str, int]:
    pattern = re.compile(r"(?m)^#+\s*(?:附录|通用解题模板|通用范式|通用例题|标准模板|通用卡片模板|知识树与索引|常见误区与避坑指南)\b")
    match = pattern.search(text)
    if not match:
        return text, "", 0
    idx = match.start()
    return text[:idx], text[idx:], len(text) - idx

def visible_text(text: str) -> str:
    text = CODE_RE.sub(" ", text)
    text = re.sub(r"---.*?---", " ", text, flags=re.S)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\[\[([^\]\|]+)(?:\|[^\]]+)?\]\]", r"\1", text)
    text = re.sub(r"[#*`>|~_\-\[\]\(\)\$]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def title_anchor(value: str) -> str:
    value = re.sub(r"^[\W_\d]+", "", value, flags=re.UNICODE)
    value = re.sub(r"(?:深度学习笔记|学习笔记|核心笔记|完整笔记|笔记|详解|精读|入门|概述|基础)$", "", value)
    return re.sub(r"[\s_\-—:：()（）【】\[\]\/]+", "", value).lower()

def keyword_groups(text: str, groups: tuple[tuple[str, ...], ...]) -> int:
    score = 0
    t_lower = text.lower()
    for g in groups:
        if any(k.lower() in t_lower for k in g):
            score += 1
    return score

def classify_note(path: Path, fm: dict[str, str], body: str) -> str:
    type_val = fm.get("type", "").lower()
    rel = path.relative_to(VAULT_ROOT).as_posix()
    if type_val in {"study", "knowledge_card", "concept", "study_note"} or "02-Knowledge" in rel or "🧠 学习系统" in rel:
        return "知识卡"
    if type_val == "paper" or "论文库" in rel: return "论文"
    if type_val == "book" or "书库" in rel: return "书籍"
    if type_val in {"problem", "problem_type", "mistake", "project"} or "18-题库学习" in rel: return "题库/项目"
    return "计划/模板"

def score_note(note: Note) -> None:
    text = note.effective_body
    plain = visible_text(text)
    plain_len = len(plain)
    code = [body for _, body in CODE_RE.findall(text) if body.strip()]
    math_matches = MATH_RE.findall(text)
    math = [m[0] or m[1] for m in math_matches if (m[0] or m[1]).strip()]
    
    risk_labels = [label for label, pattern in GENERIC_RISK_PATTERNS if pattern.search(note.raw)]
    anchor = title_anchor(note.topic)
    anchor_hits = plain.lower().replace(" ", "").count(anchor) if len(anchor) >= 2 else 0

    grounding = 3 if plain_len else 0
    grounding += 6 if anchor_hits >= 2 else 3 if anchor_hits == 1 else 0
    grounding += min(5, keyword_groups(text, (
        ("定义", "是指", "definition"),
        ("性质", "定理", "命题", "机制", "原理"),
        ("例如", "例子", "示例", "反例", "案例"),
        ("局限", "边界", "不适用", "误区", "注意"),
        ("区别", "对比", "关系", "vs"),
    )))
    if re.search(r"无意义伪公式", "；".join(risk_labels)): grounding -= 12
    elif risk_labels: grounding -= min(8, len(risk_labels) * 3)
    grounding = max(0, min(20, grounding))

    length_points = 1 if plain_len < 200 else 3 if plain_len < 500 else 6 if plain_len < 900 else 9 if plain_len < 1500 else 12
    coverage = keyword_groups(text, (
        ("定义", "是什么", "概念", "definition"),
        ("为什么", "动机", "背景", "问题", "目标"),
        ("原理", "机制", "过程", "步骤", "算法", "推导"),
        ("例子", "示例", "案例", "例如", "example"),
        ("局限", "边界", "适用", "不适用", "限制"),
    ))
    completeness = min(20, length_points + min(8, coverage * 2))

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

    URLs = URL_RE.findall(text)
    dois = DOI_RE.findall(text)
    identifiable = len(URLs) + len(dois)
    evidence = 0 if identifiable == 0 else 5 if identifiable == 1 else 8 if identifiable == 2 else 11
    if identifiable and re.search(r"作者|出版社|出版年份|isbn|et al\.|arxiv|期刊|会议", text, re.I): evidence += 2
    if identifiable and re.search(r"页码|章节|chapter\s+\d|section\s+\d", text, re.I): evidence += 2
    evidence = min(15, evidence)

    verification = 0
    if re.search(r"例子|示例|案例|例如|算例|反例|example", text, re.I): verification += 3
    if code:
        verification += 3
        if re.search(r"assert|expected|输出|结果|测试|验证|print\(", "\n".join(code), re.I): verification += 2
    if re.search(r"练习|自测|证明|推导|实验|复现", text, re.I): verification += 2
    verification = min(10, verification)

    valid = note.valid_links
    connection = 0 if valid == 0 else 3 if valid == 1 else 5 if valid <= 3 else 7 if valid <= 6 else 9
    if note.links and not note.broken_links: connection += 1
    connection = min(10, connection)

    structure = 0
    if HEADING_RE.search(text): structure += 4
    if re.search(r"(?m)^\|.+\|\s*$", text): structure += 4
    if note.frontmatter and any(k in note.frontmatter for k in ("type", "topic", "course", "tags")): structure += 2
    structure = min(10, structure)

    raw_score = grounding + completeness + rigor + evidence + verification + connection + structure

    cap = 100
    if plain_len < 300: cap = min(cap, 45)
    elif plain_len < 600: cap = min(cap, 65)
    elif plain_len < 900: cap = min(cap, 80)
    if "无意义伪公式" in risk_labels: cap = min(cap, 15)

    final_score = min(raw_score, cap)
    note.score = final_score
    note.cap = cap
    note.dimensions = {
        "主题聚焦": grounding, "内容完整": completeness, "严谨性": rigor,
        "证据来源": evidence, "例证验证": verification, "知识连接": connection, "结构维护": structure
    }

    if final_score >= 80: note.grade = "B 良好"
    elif final_score >= 70: note.grade = "C 合格"
    elif final_score >= 60: note.grade = "D 勉强"
    else: note.grade = "F 不合格"

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    notes: list[Note] = []
    link_target_map = {}

    for root, dirs, files in os.walk(SCAN_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_PATH_PARTS]
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in MARKDOWN_EXTS:
                link_target_map[p.stem.lower()] = p
                try:
                    raw = p.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                fm, raw_fm, body = parse_frontmatter(raw)
                eff_body, app_body, app_len = split_appendix(body)
                title = fm.get("title") or p.stem
                topic = fm.get("topic") or title
                cat = classify_note(p, fm, body)
                rel = p.relative_to(VAULT_ROOT).as_posix()
                subj = rel.split("/")[0]
                
                links = LINK_RE.findall(eff_body)
                valid_l = [l for l in links if l.lower() in link_target_map or (VAULT_ROOT / f"{l}.md").exists()]
                broken_l = [l for l in links if l not in valid_l]

                n = Note(
                    path=p, rel=rel, subject=subj, title=title, topic=topic,
                    raw=raw, body=body, frontmatter_text=raw_fm, frontmatter=fm,
                    category=cat, appendix_body=app_body, appendix_removed=app_len,
                    effective_body=eff_body, links=links, valid_links=len(valid_l), broken_links=broken_l
                )
                score_note(n)
                notes.append(n)

    b_count = sum(1 for n in notes if n.score >= 80)
    c_count = sum(1 for n in notes if 70 <= n.score < 80)
    d_count = sum(1 for n in notes if 60 <= n.score < 70)
    f_count = sum(1 for n in notes if n.score < 60)
    avg_score = sum(n.score for n in notes) / len(notes) if notes else 0.0

    out_json = {
        "scanned": len(notes),
        "knowledge_notes": len(notes),
        "average": round(avg_score, 1),
        "distribution": {"<60": f_count, "60-69": d_count, "70-79": c_count, "80-89": b_count}
    }
    OUTPUT_JSON.write_text(json.dumps(out_json, ensure_ascii=False, indent=2), encoding="utf-8")

    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "score", "grade", "cap", "去模板有效正文字符", "主题聚焦", "内容完整", "严谨性", "证据来源", "例证验证", "知识连接", "结构维护", "主要问题"])
        for n in notes:
            writer.writerow([
                n.rel, n.score, n.grade, n.cap, len(visible_text(n.effective_body)),
                n.dimensions["主题聚焦"], n.dimensions["内容完整"], n.dimensions["严谨性"],
                n.dimensions["证据来源"], n.dimensions["例证验证"], n.dimensions["知识连接"], n.dimensions["结构维护"],
                ";".join(n.flags)
            ])

    print(json.dumps(out_json, indent=2))
    print(OUTPUT_MD)
    print(OUTPUT_CSV)
    print(OUTPUT_JSON)

if __name__ == "__main__":
    main()
