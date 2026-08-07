#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, json
from pathlib import Path

VAULT = Path(r"F:\-")
ROOT = Path(r"F:\-\02-Knowledge\🧠 学习系统\12-信号与系统")

# ---------- Build file index over the whole vault ----------
vault_files = {}   # basename -> list of rel paths (from VAULT)
vault_paths = set()
for p in VAULT.rglob("*.md"):
    rel = str(p.relative_to(VAULT)).replace("\\", "/")
    vault_paths.add(rel)
    vault_files.setdefault(p.stem, []).append(rel)

# index within course only
course_files = {}
for p in ROOT.rglob("*.md"):
    rel = str(p.relative_to(VAULT)).replace("\\", "/")
    course_files.setdefault(p.stem, []).append(rel)

def get_fm(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None
    return m.group(1)

def fm_keys(block):
    """Return dict key -> raw value text (handles simple + list values)."""
    res = {}
    lines = block.split("\n")
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        m = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", ln)
        if m:
            key = m.group(1)
            val = m.group(2).strip()
            if val == "" or val.startswith("[") or val.startswith("{"):
                # possibly multi-line list/map
                j = i + 1
                buf = [val] if val else []
                while j < n and (lines[j].startswith("  ") or lines[j].startswith("\t") or lines[j].strip() == ""):
                    if lines[j].strip() != "":
                        buf.append(lines[j].strip())
                    j += 1
                res[key] = "\n".join(buf)
                i = j
            else:
                res[key] = val
                i += 1
        else:
            i += 1
    return res

def has_wikilink(s):
    return "[[" in s

def link_targets(s):
    """Extract all [[...]] targets from a string."""
    out = []
    for m in re.finditer(r"\[\[([^\]]+)\]\]", s):
        out.append(m.group(1))
    return out

def resolve_target(target):
    """Return (status, detail). status in {ok, ambiguous, broken}."""
    # strip alias
    t = target.split("|", 1)[0].strip()
    # strip heading
    t = t.split("#", 1)[0].strip()
    if t == "":
        return ("empty", "")
    if "/" in t:
        # path-based
        cand = t
        if not cand.endswith(".md"):
            cand += ".md"
        rel = cand
        if rel in vault_paths:
            return ("ok", rel)
        # try as relative to ROOT
        rp = (ROOT / cand)
        if rp.exists():
            return ("ok", str(rp.relative_to(VAULT)).replace("\\","/"))
        return ("broken", rel)
    else:
        base = t
        if base in vault_files:
            if len(vault_files[base]) == 1:
                return ("ok", vault_files[base][0])
            return ("ambiguous", str(vault_files[base]))
        return ("broken", base)

# ---------- Walk course files ----------
report = {
    "study_missing_fields": [],
    "stage_mocs": [],
    "broken_links": [],
    "ambiguous_links": [],
    "no_frontmatter": [],
    "duplicate_basenames": [],
    "project_files_root": [],
    "downstream_present": [],
    "plain_string_stage_moc_or_upstream": [],
    "stage_moc_missing_on_card": [],
    "upstream_unresolved": [],
    "course_missing": [],
    "flow_missing": [],
    "kind_missing": [],
    "stray_root_files": [],
}

# note which files live at course root (not in a stage dir and not the known meta files)
meta_root = {
    "🗺️ 信号与系统学习路径.md",
    "📚 教材挂载索引.md",
    "📋 知识点卡清单.md",
    "🧭 开源作业体系-信号与系统.md",
    "学习地图.md",
    "课程复盘.md",
    "信号与系统错题漏洞入口.md",
    "采样定理与混叠.md",
    "傅里叶变换与频谱分析.md",
    "拉普拉斯变换.md",
    "第七阶段：DFT 与 FFT.md",
}

# files whose name starts with 项目- are project files
# detect stage dirs
stage_dirs = [d.name for d in ROOT.iterdir() if d.is_dir() and re.match(r"^\d{2}-", d.name)]

all_cards = []  # (rel, fmkeys, body)
for p in sorted(ROOT.rglob("*.md")):
    rel = str(p.relative_to(VAULT)).replace("\\", "/")
    text = p.read_text(encoding="utf-8", errors="replace")
    block = get_fm(text)
    body = text[text.find("---", 3)+3:] if block is not None else text
    keys = fm_keys(block) if block else {}
    base = p.stem
    is_project = base.startswith("项目-") or "HW" in base and base.startswith("信号与系统")
    is_root = p.parent == ROOT
    # record duplicate basenames
    if len(course_files[base]) > 1:
        report["duplicate_basenames"].append((base, course_files[base]))
    if block is None:
        report["no_frontmatter"].append(rel)
    ftype = keys.get("type", "")
    # Stage MOC detection
    if ftype == "stage":
        report["stage_mocs"].append((rel, keys.get("topic",""), keys.get("phase","")))
    # Study card checks
    if ftype == "study":
        for f in ["course","stage_moc","flow","kind","upstream"]:
            if f not in keys or keys.get(f,"").strip() in ("","[]","{}"):
                if f == "course": report["course_missing"].append(rel)
                if f == "stage_moc": report["stage_moc_missing_on_card"].append(rel)
                if f == "flow": report["flow_missing"].append(rel)
                if f == "kind": report["kind_missing"].append(rel)
        # check stage_moc/upstream are wikilinks
        for f in ["stage_moc","upstream"]:
            v = keys.get(f,"")
            if v and not has_wikilink(v):
                report["plain_string_stage_moc_or_upstream"].append((rel, f, v[:80]))
        # upstream resolution
        v = keys.get("upstream","")
        if v and has_wikilink(v):
            for tgt in link_targets(v):
                st, det = resolve_target(tgt)
                if st != "ok":
                    report["upstream_unresolved"].append((rel, tgt, st, det))
    # downstream present (should be derived, not static, in new cards)
    if "downstream" in keys:
        report["downstream_present"].append(rel)
    # project files at root
    if is_project and is_root:
        report["project_files_root"].append(rel)
    # stray root files (not meta, not project, not HW)
    if is_root and base not in meta_root and not is_project and ftype != "index":
        report["stray_root_files"].append(rel)
    # broken / ambiguous links in body
    for tgt in link_targets(body):
        st, det = resolve_target(tgt)
        if st == "broken":
            report["broken_links"].append((rel, tgt))
        elif st == "ambiguous":
            report["ambiguous_links"].append((rel, tgt, det))
    # also check links in frontmatter values
    if block is not None:
        for tgt in link_targets(block):
            st, det = resolve_target(tgt)
            if st == "broken":
                report["broken_links"].append((rel, tgt))
            elif st == "ambiguous":
                report["ambiguous_links"].append((rel, tgt, det))

# counts
print("="*70)
print("AUDIT SUMMARY — 12-信号与系统")
print("="*70)
print(f"Total .md files in course: {len(list(ROOT.rglob('*.md')))}")
print(f"Stage dirs: {stage_dirs}")
print(f"\n[1] study cards missing `course`: {len(report['course_missing'])}")
print(f"[2] study cards missing `stage_moc`: {len(report['stage_moc_missing_on_card'])}")
print(f"[3] study cards missing `flow`: {len(report['flow_missing'])}")
print(f"[4] study cards missing `kind`: {len(report['kind_missing'])}")
print(f"[5] files with NO frontmatter: {len(report['no_frontmatter'])}")
print(f"[6] stage MOC files found: {len(report['stage_mocs'])}")
print(f"[7] duplicate basenames: {len(report['duplicate_basenames'])}")
print(f"[8] project files at course ROOT: {len(report['project_files_root'])}")
print(f"[9] downstream present (should be derived): {len(report['downstream_present'])}")
print(f"[10] plain-string stage_moc/upstream: {len(report['plain_string_stage_moc_or_upstream'])}")
print(f"[11] upstream unresolved: {len(report['upstream_unresolved'])}")
print(f"[12] BROKEN links: {len(report['broken_links'])}")
print(f"[13] ambiguous links: {len(report['ambiguous_links'])}")
print(f"[14] stray root files: {len(report['stray_root_files'])}")

print("\n--- Stage MOC files (rel, topic, phase) ---")
for x in report["stage_mocs"]:
    print("  ", x)

print("\n--- Duplicate basenames ---")
for b, locs in report["duplicate_basenames"]:
    print("  ", b, "->", locs)

print("\n--- Project files at course ROOT ---")
for x in report["project_files_root"]:
    print("  ", x)

print("\n--- Files with NO frontmatter ---")
for x in report["no_frontmatter"]:
    print("  ", x)

print("\n--- Stray root files ---")
for x in report["stray_root_files"]:
    print("  ", x)

print("\n--- Plain-string stage_moc/upstream (first 20) ---")
for x in report["plain_string_stage_moc_or_upstream"][:20]:
    print("  ", x)

print("\n--- Upstream unresolved (first 20) ---")
for x in report["upstream_unresolved"][:20]:
    print("  ", x)

print("\n--- BROKEN links (first 40) ---")
for x in report["broken_links"][:40]:
    print("  ", x)

print("\n--- Ambiguous links (first 20) ---")
for x in report["ambiguous_links"][:20]:
    print("  ", x)

print("\n--- downstream present ---")
for x in report["downstream_present"]:
    print("  ", x)

# Save full report as JSON for later
with open(r"F:\-\.tmp\audit_signals_report.json","w",encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
print("\nFull report saved to F:\\-\\.tmp\\audit_signals_report.json")
