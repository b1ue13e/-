import os, re, sys
from collections import defaultdict, deque
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
# 短名 -> 完整路径
short = {}
for root, dirs, files in os.walk(KB):
    dirs[:] = [x for x in dirs if x not in SKIP]
    for f in files:
        if f.endswith('.md'):
            short.setdefault(f[:-3], []).append(os.path.join(root, f))
def canon(link):
    t = re.sub(r'\\\|.*$', '', link)
    t = t.split('#')[0].split('|')[0].strip().removesuffix('.md')
    if '/' in t:
        full = t
    else:
        cands = short.get(t, [])
        full = next((os.path.relpath(c, KB).replace('\\', '/') for c in cands if COURSE in c), '')
    return full

# 构建课程卡依赖图
cards = {}  # 短名 -> 完整路径
up_map = {}  # 完整路径 -> [upstream 完整路径]
for p in walk(COURSE):
    with open(p, encoding='utf-8') as f:
        c = f.read()
    if 'type: study' not in c:
        continue
    name = os.path.basename(p)[:-3]
    full = os.path.relpath(p, KB).replace('\\', '/')
    cards[name] = full
    m = re.match(r'^---\n(.*?)\n---', c, re.S)
    fm = m.group(1)
    upm = re.search(r'^upstream:\s*\[(.*?)\]', fm, re.M | re.S)
    ups = []
    if upm:
        for lk in re.findall(r'\[\[([^\]]+)\]\]', upm.group(1)):
            u = canon(lk)
            if u:
                ups.append(u)
    up_map[full] = ups

# 拓扑排序检测环（只考虑课程内卡之间的边）
node_ids = {f: i for i, f in enumerate(cards.values())}
n = len(node_ids)
adj = [[] for _ in range(n)]
indeg = [0] * n
for f, ups in up_map.items():
    if f not in node_ids:
        continue
    for u in ups:
        if u in node_ids:
            adj[node_ids[u]].append(node_ids[f])
            indeg[node_ids[f]] += 1
q = deque([i for i in range(n) if indeg[i] == 0])
visited = 0
while q:
    v = q.popleft()
    visited += 1
    for w in adj[v]:
        indeg[w] -= 1
        if indeg[w] == 0:
            q.append(w)
if visited == n:
    print(f"✅ upstream 图无环（{n} 张卡全部可拓扑排序）")
else:
    print(f"❌ 检测到环！{n - visited} 张卡无法拓扑排序（在环中）：")
    for i in range(n):
        if indeg[i] > 0:
            print("  环中卡:", [k for k, v in node_ids.items() if v == i][0])
