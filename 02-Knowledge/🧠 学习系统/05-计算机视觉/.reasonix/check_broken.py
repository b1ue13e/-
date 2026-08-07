# -*- coding: utf-8 -*-
"""检查课程内断链（重命名后验证）"""
import os, re, io

VAULT = r'F:\-'
EXCLUDE = {'.workbuddy', '.归档', '.reasonix', '.recovery-hold', '.git', 'node_modules', '__pycache__', '.pytest_cache', '.tmp', '.obsidian'}

all_paths = set()
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE]
    for fn in files:
        if fn.endswith('.md'):
            rel = os.path.relpath(os.path.join(root, fn), VAULT).replace('\\', '/')
            all_paths.add(rel[:-3])

name_to_path = {}
for p in all_paths:
    base = p.split('/')[-1]
    name_to_path.setdefault(base, []).append(p)

cv_root = os.path.join(VAULT, '02-Knowledge', '🧠 学习系统', '05-计算机视觉')
cv_prefix = '02-Knowledge/🧠 学习系统/05-计算机视觉/'

broken = []
checked = 0
for root, dirs, files in os.walk(cv_root):
    dirs[:] = [d for d in dirs if d not in EXCLUDE]
    for fn in files:
        if not fn.endswith('.md'):
            continue
        fp = os.path.join(root, fn)
        rel = os.path.relpath(fp, VAULT).replace('\\', '/')
        with io.open(fp, encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
        checked += 1
        in_fence = False
        for line in content.split('\n'):
            if line.strip().startswith('```'):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for m in re.finditer(r'\[\[([^\[\]\n]+?)\]\]', line):
                target_full = m.group(1)
                # 表格转义 \\| 视为分隔符；普通 | 也是分隔符
                t = target_full.replace('\\|', '|').split('|')[0].strip()
                if not t:
                    continue
                if '/' in t:
                    p = t[:-3] if t.endswith('.md') else t
                    if p not in all_paths:
                        broken.append((rel, target_full, 'path'))
                else:
                    cands = name_to_path.get(t, [])
                    if not cands:
                        broken.append((rel, target_full, 'short-missing'))
                    elif len(cands) > 1 and not any(c.startswith(cv_prefix) for c in cands):
                        broken.append((rel, target_full, 'short-ambiguous'))

print(f'检查 {checked} 个文件')
cv_broken = [b for b in broken if '05-计算机视觉' in b[1] or b[2] == 'short-missing']
print(f'课程相关断链: {len(cv_broken)}')
seen = set()
for rel, t, typ in cv_broken:
    key = (rel, t)
    if key in seen:
        continue
    seen.add(key)
    print(f'  [{typ}] {rel}: {t}')
