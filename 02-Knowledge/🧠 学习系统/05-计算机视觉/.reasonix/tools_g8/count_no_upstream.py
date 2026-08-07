import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
KB = "F:" + os.sep + "-"
COURSE = KB + os.sep + "02-Knowledge" + os.sep + "🧠 学习系统" + os.sep + "05-计算机视觉"
SKIP = {'.归档', '.reasonix', '.recovery-hold', '.pytest_cache', '__pycache__', '.git', '.obsidian', '.tmp'}
def walk(base):
    for r, d, fs in os.walk(base):
        d[:] = [x for x in d if x not in SKIP]
        for f in fs:
            if f.endswith('.md'):
                yield os.path.join(r, f)
no_up = []
total = 0
for p in walk(COURSE):
    rel = os.path.relpath(p, COURSE)
    with open(p, encoding='utf-8') as f:
        c = f.read()
    if 'type: study' not in c:
        continue
    total += 1
    # 提取 frontmatter（--- 之间）
    m = re.match(r'^---\n(.*?)\n---', c, re.S)
    fm = m.group(1) if m else ''
    has_up = bool(re.search(r'^upstream:', fm, re.M))
    if not has_up:
        no_up.append(rel)
print(f"study 卡总数: {total}")
print(f"真正无 upstream 的卡 ({len(no_up)}):")
for x in no_up:
    print("  " + x)
