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
for p in sorted(walk(COURSE)):
    rel = os.path.relpath(p, COURSE)
    with open(p, encoding='utf-8') as f:
        c = f.read()
    if 'type: study' not in c or re.search(r'upstream:\s*\[', c):
        continue
    m = re.search(r'## 3\. 学它之前需要哪些前置知识\？(.*?)(?=\n## |\Z)', c, re.S)
    body = m.group(1).strip() if m else ''
    # 提取前置中的 wikilink 与首行文本
    links = re.findall(r'\[\[([^\]]+?)(?:\||\]\])', body)
    first_lines = [l.strip()[:60] for l in body.split('\n') if l.strip()][:3]
    print(f"\n### {rel}")
    if links:
        print(f"  §3 链接: {links[:6]}")
    print(f"  §3 首行: {first_lines}")
