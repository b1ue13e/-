import os, sys, re, csv
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = Path(r"F:\-")
OUTPUT_CSV = VAULT_ROOT / "knowledge_notes_harsh_scores_2026-07-31.csv"
EXCLUDED_DIRS = {".git", ".obsidian", ".trash", "templates", "📇 模板", "🗄️ 归档", "tools", "scratch"}

CODE_RE = re.compile(r"```([a-zA-Z0-9_+-]*)\n(.*?)```", re.S)
MATH_RE = re.compile(r"\$\$(.*?)\$\$|\$(.*?)\$", re.S)
HEADING_RE = re.compile(r"(?m)^#{1,6}\s+(.+)$")
LINK_RE = re.compile(r"\[\[([^\]\|]+)(?:\|[^\]]+)?\]\]")
URL_RE = re.compile(r"https?://[^\s><\"'\(\)]+")
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")

def parse_frontmatter(text: str):
    if not text.startswith("---"): return {}, text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not match: return {}, text
    fm = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip().lower()] = v.strip().strip("\"'")
    return fm, text[match.end():]

def visible_text(text: str) -> str:
    text = CODE_RE.sub(" ", text)
    text = re.sub(r"---.*?---", " ", text, flags=re.S)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\[\[([^\]\|]+)(?:\|[^\]]+)?\]\]", r"\1", text)
    text = re.sub(r"[#*`>|~_\-\[\]\(\)\$]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def keyword_groups(text: str, groups: tuple) -> int:
    score = 0
    t_lower = text.lower()
    for g in groups:
        if any(k.lower() in t_lower for k in g):
            score += 1
    return score

def audit_file(p: Path, link_target_set: set) -> dict:
    try:
        raw = p.read_text(encoding="utf-8", errors="ignore")
    except Exception: return None
    fm, body = parse_frontmatter(raw)
    title = fm.get("title") or p.stem
    topic = fm.get("topic") or title
    rel = p.relative_to(VAULT_ROOT).as_posix()
    
    plain = visible_text(body)
    plain_len = len(plain)
    code = [b for _, b in CODE_RE.findall(body) if b.strip()]
    math_m = MATH_RE.findall(body)
    math = [m[0] or m[1] for m in math_m if (m[0] or m[1]).strip()]

    anchor = re.sub(r"[\s_\-—:：()（）【】\[\]\/]+", "", topic).lower()
    anchor_hits = plain.lower().replace(" ", "").count(anchor) if len(anchor) >= 2 else 0

    grounding = 3 if plain_len else 0
    grounding += 6 if anchor_hits >= 2 else 3 if anchor_hits == 1 else 0
    grounding += min(5, keyword_groups(body, (
        ("定义", "是指", "definition"),
        ("性质", "定理", "命题", "机制", "原理"),
        ("例如", "例子", "示例", "反例", "案例"),
        ("局限", "边界", "不适用", "误区", "注意"),
        ("区别", "对比", "关系", "vs"),
    )))
    grounding = min(20, grounding)

    length_points = 1 if plain_len < 200 else 3 if plain_len < 500 else 6 if plain_len < 900 else 9 if plain_len < 1500 else 12
    coverage = keyword_groups(body, (
        ("定义", "是什么", "概念", "definition"),
        ("为什么", "动机", "背景", "问题", "目标"),
        ("原理", "机制", "过程", "步骤", "算法", "推导"),
        ("例子", "示例", "案例", "例如", "example"),
        ("局限", "边界", "适用", "不适用", "限制"),
    ))
    completeness = min(20, length_points + min(8, coverage * 2))

    rigor = min(10, keyword_groups(body, (
        ("假设", "条件", "前提"),
        ("定义", "定理", "命题", "性质"),
        ("推导", "证明", "因此", "从而"),
        ("区别", "对比", "vs", "关系"),
        ("误区", "反例", "边界", "局限"),
    )) * 2)
    rigor += 3 if math else 0
    rigor += 2 if re.search(r"(?m)^\|.+\|\s*$", body) and re.search(r"(?m)^\|\s*:?-+", body) else 0
    rigor = min(15, rigor)

    URLs = URL_RE.findall(body)
    dois = DOI_RE.findall(body)
    identifiable = len(URLs) + len(dois)
    evidence = 0 if identifiable == 0 else 5 if identifiable == 1 else 8 if identifiable == 2 else 11
    if identifiable and re.search(r"作者|出版社|出版年份|isbn|et al\.|arxiv|期刊|会议", body, re.I): evidence += 2
    if identifiable and re.search(r"页码|章节|chapter\s+\d|section\s+\d", body, re.I): evidence += 2
    evidence = min(15, evidence)

    verification = 0
    if re.search(r"例子|示例|案例|例如|算例|反例|example", body, re.I): verification += 3
    if code:
        verification += 3
        if re.search(r"assert|expected|输出|结果|测试|验证|print\(", "\n".join(code), re.I): verification += 2
    if re.search(r"练习|自测|证明|推导|实验|复现", body, re.I): verification += 2
    verification = min(10, verification)

    links = LINK_RE.findall(body)
    valid_l = [l for l in links if l.lower() in link_target_set]
    connection = 0 if len(valid_l) == 0 else 3 if len(valid_l) == 1 else 5 if len(valid_l) <= 3 else 7 if len(valid_l) <= 6 else 9
    if links and len(valid_l) == len(links): connection += 1
    connection = min(10, connection)

    structure = 0
    if HEADING_RE.search(body): structure += 4
    if re.search(r"(?m)^\|.+\|\s*$", body): structure += 4
    if fm and any(k in fm for k in ("type", "topic", "course", "tags")): structure += 2
    structure = min(10, structure)

    raw_score = grounding + completeness + rigor + evidence + verification + connection + structure
    cap = 100
    if plain_len < 300: cap = 45
    elif plain_len < 600: cap = 65
    elif plain_len < 900: cap = 80
    final_score = min(raw_score, cap)

    grade = "B 良好" if final_score >= 80 else "C 合格" if final_score >= 70 else "D 勉强" if final_score >= 60 else "F 不合格"

    return {
        "path": rel, "name": p.name, "score": final_score, "grade": grade, "cap": cap,
        "len": plain_len, "grounding": grounding, "completeness": completeness,
        "rigor": rigor, "evidence": evidence, "verification": verification,
        "connection": connection, "structure": structure
    }

def main():
    link_targets = set()
    md_files = []
    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for f in files:
            if f.endswith(".md"):
                p = Path(root) / f
                link_targets.add(p.stem.lower())
                md_files.append(p)

    results = []
    for p in md_files:
        res = audit_file(p, link_targets)
        if res: results.append(res)

    print(f"Scanned {len(results)} files.")

    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["path", "score", "grade", "cap", "去模板有效正文字符", "主题聚焦", "内容完整", "严谨性", "证据来源", "例证验证", "知识连接", "结构维护", "主要问题"])
        for r in results:
            w.writerow([r["path"], r["score"], r["grade"], r["cap"], r["len"], r["grounding"], r["completeness"], r["rigor"], r["evidence"], r["verification"], r["connection"], r["structure"], ""])

if __name__ == "__main__":
    main()
