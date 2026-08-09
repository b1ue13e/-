import os, re, unicodedata

VAULT = "f:/-"
COURSE_PREFIXES = (
    "02-Knowledge/🧠 学习系统/11-计算机组成原理/",
    "03-Projects/系统与硬件/11-计算机组成原理/",
)
SKIP_PARTS = {".obsidian", ".recovery-hold", ".trash", ".git", "node_modules"}

def nfc(s):
    return unicodedata.normalize("NFC", s)

name2paths = {}
all_rels = []
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in SKIP_PARTS]
    for fn in files:
        if not fn.endswith(".md"):
            continue
        rel = os.path.relpath(os.path.join(root, fn), VAULT).replace("\\", "/")
        rel = nfc(rel)
        stem = nfc(fn[:-3])
        name2paths.setdefault(stem, []).append(rel)
        all_rels.append(rel)

def resolve(link, cur_rel):
    raw = nfc(link).replace("\\|", "|")
    if "|" in raw:
        raw = raw.split("|", 1)[0]
    if "#" in raw:
        raw = raw.split("#", 1)[0]
    raw = raw.strip()
    if not raw:
        return "anchor", None
    if "/" not in raw:
        lst = name2paths.get(raw, [])
        if not lst:
            return "dead", None
        return ("ok", lst) if len(lst) == 1 else ("ambig", lst)
    target = raw if raw.endswith(".md") else raw + ".md"
    # 1) relative to current file dir
    cand = nfc(os.path.normpath(os.path.join(os.path.dirname(cur_rel), target)).replace("\\", "/"))
    if cand in all_rels:
        return "ok", [cand]
    # 2) vault-root absolute
    if target in all_rels:
        return "ok", [target]
    # 3) suffix shortest-path
    cands = [r for r in all_rels if r.endswith("/" + target)]
    if cands:
        return ("ok", cands) if len(cands) == 1 else ("ambig", cands)
    return "dead", None


LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
dead, ambig = [], []
scanned = 0
for rel in all_rels:
    if not rel.startswith(COURSE_PREFIXES):
        continue
    scanned += 1
    full = os.path.join(VAULT, rel)
    with open(full, encoding="utf-8") as f:
        text = f.read()
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in LINK_RE.finditer(line):
            st, info = resolve(m.group(1), rel)
            if st == "dead":
                dead.append((rel, m.group(1)))
            elif st == "ambig":
                ambig.append((rel, m.group(1), len(info)))

print("SCANNED:", scanned)
print("DEAD:", len(dead))
for r, l in sorted(dead):
    tag = "[AUDIT-HISTORY]" if "/质量审计/" in r else "[ACTIVE]"
    print(f"  {tag} {r}: [[{l}]]")
print("AMBIGUOUS:", len(ambig))
for r, l, n in sorted(ambig):
    print(f"  {r}: [[{l}]] -> {n} files")
