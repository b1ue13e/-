# -*- coding: utf-8 -*-
import os, re

VAULT = r"F:\-"
COURSE = r"F:\-\02-Knowledge\🧠 学习系统\17-机器学习"
REPORT = r"F:\-\03-Projects\17-机器学习\质量审计\课程严苛审计.md"

SKIP_DIRS = {'.obsidian', '.trash', '.git', 'node_modules', '.workbuddy-ai', '.recovery-hold'}

def rel(p):
    return os.path.relpath(p, VAULT).replace(os.sep, '/')

# 1. Build index over the dirs actually referenced by course link targets
INDEX_ROOTS = [
    os.path.join(VAULT, '02-Knowledge'),
    os.path.join(VAULT, '03-Projects'),
    os.path.join(VAULT, '📚 书库'),
]
COURSE_REL = rel(COURSE)  # '02-Knowledge/🧠 学习系统/17-机器学习'
md_files = []
for idx_root in INDEX_ROOTS:
    if not os.path.isdir(idx_root):
        continue
    for root, dirs, files in os.walk(idx_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.lower().endswith('.md'):
                md_files.append(os.path.join(root, f))

def head_lines(full, n=40):
    try:
        with open(full, encoding='utf-8', errors='replace') as fh:
            return ''.join([next(fh) for _ in range(n)])
    except Exception:
        return ''

basename_map = {}   # basename -> [relpath,...]
alias_map = {}      # alias -> relpath
relpath_set = set()
for full in md_files:
    r = rel(full)
    relpath_set.add(r)
    base = os.path.splitext(os.path.basename(full))[0]
    basename_map.setdefault(base, []).append(r)
    try:
        text = head_lines(full, 40)
    except Exception:
        continue
    fm = None
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            fm = text[3:end]
    if fm:
        # inline aliases [a, b]
        m = re.search(r'aliases\s*:\s*\[(.*?)\]', fm, re.S)
        if m:
            for a in re.findall(r'["\'](.*?)["\']', m.group(1)):
                alias_map.setdefault(a, r)
        # yaml list aliases
        m = re.search(r'aliases\s*:\s*\n((?:\s*-\s*.+\n)+)', fm)
        if m:
            for a in re.findall(r'-\s*["\']?(.*?)["\']?\s*$', m.group(1), re.M):
                if a:
                    alias_map.setdefault(a, r)

def resolve_link(target):
    """Return relpath if resolvable else None."""
    # unescape Obsidian escaped pipe (\| -> |), used inside markdown tables
    t = target.replace('\\|', '|')
    t = t.split('|')[0].split('#')[0].strip()
    if not t:
        return None
    # path link
    if '/' in t:
        cands = []
        cands.append(t if t.endswith('.md') else t + '.md')
        cands.append(t)
        cands.append(COURSE_REL + '/' + (t if t.endswith('.md') else t + '.md'))
        cands.append(COURSE_REL + '/' + t)
        for c in cands:
            if c in relpath_set:
                return c
        # fallback: basename at that course subpath
        b = os.path.splitext(os.path.basename(t))[0]
        if b in basename_map:
            return basename_map[b][0]
        return None
    if t in basename_map:
        return basename_map[t][0]
    if t in alias_map:
        return alias_map[t]
    if t.endswith('.md'):
        b = t[:-3]
        if b in basename_map:
            return basename_map[b][0]
    return None

# 2. Course-specific audit
bom = []
dual_fm = []
broken = []
missing_flow_kind = []
hw_hist_label = []
hist_label_filename = []
planned_shells = []     # (rel, charcount, has_content)
static_downstream = []

LINK_RE = re.compile(r'\[\[([^\]]+)\]\]')
MDLINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
HIST_LABEL_RE = re.compile(r'【.*?】|〔.*?〕|〈.*?〉|\〈.*?\〉')  # book-title style legacy marks

course_files = []
for root, dirs, files in os.walk(COURSE):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if f.lower().endswith('.md'):
            course_files.append(os.path.join(root, f))

for full in course_files:
    r = rel(full)
    raw = open(full, encoding='utf-8')
    if raw.read(1) == '\ufeff':
        bom.append(r)
    raw.seek(0)
    text = raw.read()
    raw.close()

    # dual frontmatter detection: count genuine YAML blocks (--- ... ---)
    # delimited by standalone '---' lines; a block is YAML if it contains a
    # 'key:' line. Content horizontal rules (---) produce non-YAML blocks.
    lines = text.split('\n')[:120]
    dash_idx = [i for i, ln in enumerate(lines) if ln.strip() == '---']
    yaml_blocks = 0
    for k in range(0, len(dash_idx) - 1, 2):
        a, b = dash_idx[k], dash_idx[k+1]
        block = '\n'.join(lines[a+1:b])
        if re.search(r'^\s*\w[\w-]*\s*:', block, re.M):
            yaml_blocks += 1
    if yaml_blocks >= 2:
        dual_fm.append((r, yaml_blocks))

    # frontmatter parse
    fm = None
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            fm = text[3:end]

    ftype = None
    flow = None
    kind = None
    status = None
    assignment_format = None
    if fm:
        m = re.search(r'^type\s*:\s*(.+)$', fm, re.M)
        if m: ftype = m.group(1).strip()
        m = re.search(r'^flow\s*:\s*(.+)$', fm, re.M)
        if m: flow = m.group(1).strip()
        m = re.search(r'^kind\s*:\s*(.+)$', fm, re.M)
        if m: kind = m.group(1).strip()
        m = re.search(r'^status\s*:\s*(.+)$', fm, re.M)
        if m: status = m.group(1).strip()
        m = re.search(r'^assignment_format\s*:\s*(.+)$', fm, re.M)
        if m: assignment_format = m.group(1).strip()

    # missing flow/kind for study cards
    if ftype == 'study' and (not flow or not kind):
        missing_flow_kind.append((r, flow, kind))

    # homework historical label in assignment_format or H1/filename
    if ftype == 'homework':
        if assignment_format and HIST_LABEL_RE.search(assignment_format):
            hw_hist_label.append((r, 'assignment_format', assignment_format))
        # H1
        m = re.search(r'^#\s+(.+)$', text, re.M)
        if m and HIST_LABEL_RE.search(m.group(1)):
            hw_hist_label.append((r, 'H1', m.group(1)))

    # historical labels in filename or H1 for all course files
    if HIST_LABEL_RE.search(os.path.basename(full)):
        hist_label_filename.append((r, 'filename'))
    m = re.search(r'^#\s+(.+)$', text, re.M)
    if m and HIST_LABEL_RE.search(m.group(1)) and ftype != 'homework':
        hist_label_filename.append((r, 'H1', m.group(1)))

    # planned status shells
    if status == 'planned':
        body = text
        if fm:
            body = text[end+4:] if end != -1 else text
        charcount = len(body.strip())
        planned_shells.append((r, charcount))

    # link resolution
    for lm in LINK_RE.finditer(text):
        tgt = lm.group(1)
        # skip image embeds ![[...]]
        if text[lm.start()-1:lm.start()] == '!':
            continue
        if resolve_link(tgt) is None:
            broken.append((r, tgt))
    for mm in MDLINK_RE.finditer(text):
        tgt = mm.group(1)
        if tgt.startswith('http') or tgt.startswith('mailto'):
            continue
        if tgt.startswith('/'):
            tgt = tgt[1:]
        if resolve_link(tgt) is None:
            broken.append((r, tgt))

# 3. Specific checks
prereq_moc = r"02-Knowledge/🧠 学习系统/17-机器学习/00-前置知识/🧭 机器学习-前置知识.md"
prereq_moc_exists = prereq_moc in relpath_set
prereq_moc_referenced = []
for full in course_files:
    t = open(full, encoding='utf-8').read()
    if '机器学习-前置知识' in t or '00-前置知识' in t:
        prereq_moc_referenced.append(rel(full))

authored = {}
for name in ['DQN', 'K-means++', '高斯混合模型', 'SMOTE', '曼哈顿距离']:
    cands = basename_map.get(name, [])
    for c in cands:
        if c.startswith('02-Knowledge/🧠 学习系统/17-机器学习'):
            full = os.path.join(VAULT, *c.split('/'))
            txt = open(full, encoding='utf-8').read()
            sm = re.search(r'^status\s*:\s*(.+)$', txt, re.M)
            st = sm.group(1).strip() if sm else None
            authored[name] = (c, st, len(txt))

# 4. Report
print("=== COMPLIANCE AUDIT (post-fix verification) ===")
print(f"Vault md files indexed: {len(md_files)}")
print(f"Course files scanned:   {len(course_files)}")
print()
print(f"[BOM] count: {len(bom)}  -> {bom}")
print(f"[Dual FM] count: {len(dual_fm)} -> {dual_fm}")
print(f"[Broken links] count: {len(broken)}")
for b in broken[:50]:
    print("   ", b)
print(f"[Missing flow/kind (study)] count: {len(missing_flow_kind)} -> {missing_flow_kind}")
print(f"[Homework hist-label] count: {len(hw_hist_label)} -> {hw_hist_label}")
print(f"[Hist-label filename/H1] count: {len(hist_label_filename)} -> {hist_label_filename}")
print(f"[Planned status cards] count: {len(planned_shells)}")
for p in planned_shells:
    print("   ", p)
print()
print(f"[Prereq MOC exists]: {prereq_moc_exists}  ({prereq_moc})")
print(f"[Prereq MOC referenced by]: {prereq_moc_referenced}")
print()
print("[Authored placeholder cards status]:")
for name,(c,st,ln) in authored.items():
    print(f"   {name}: status={st} chars={ln} path={c}")
print()
print("=== END ===")
