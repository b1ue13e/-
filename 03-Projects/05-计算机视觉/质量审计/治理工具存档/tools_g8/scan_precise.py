import re, os, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
KB = "F:" + os.sep + "-"
COURSE = "F:" + os.sep + "-" + os.sep + "02-Knowledge" + os.sep + "🧠 学习系统" + os.sep + "05-计算机视觉"
SKIP = {'.归档', '.reasonix', '.recovery-hold', '.pytest_cache', '__pycache__', '.git', '.obsidian', '.tmp'}

def walk(base):
    for r, d, fs in os.walk(base):
        d[:] = [x for x in d if x not in SKIP]
        for f in fs:
            if f.endswith('.md'):
                yield os.path.join(r, f)

short = {}
for p in walk(KB):
    short.setdefault(os.path.basename(p)[:-3], []).append(p)

def resolv(raw):
    t = re.sub(r'\\\|.*$', '', raw)
    t = t.split('#')[0].split('|')[0].strip()
    if not t:
        return True
    if t.endswith('.md'):
        t = t[:-3]
    if '/' in t:
        return os.path.exists(os.path.join(KB, t + '.md'))
    return t in short

cnt = Counter()
samples = {}
for p in walk(COURSE):
    rel = os.path.relpath(p, COURSE)
    with open(p, encoding='utf-8') as f:
        lines = f.readlines()
    in_f = False
    for i, l in enumerate(lines, 1):
        if re.match(r'^\s*(```|~~~)', l):
            in_f = not in_f
            continue
        if in_f:
            continue
        for m in re.finditer(r'\[\[([^\]]+)\]\]', l):
            raw = m.group(1)
            if not resolv(raw):
                t = re.sub(r'\\\|.*$', '', raw).split('#')[0].split('|')[0].strip()
                cnt[t] += 1
                samples.setdefault(t, []).append(f"{rel}:{i}")

total = sum(cnt.values())
print(f"唯一死链目标: {len(cnt)}, 总引用: {total}")
for t, c in cnt.most_common():
    print(f"{c:4d}  {t}   # 例: {samples[t][0]}")
