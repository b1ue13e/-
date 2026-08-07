import os
import sys
import re
import yaml

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

# 1. Search Dataview queries with unprefixed paths (without trailing slash requirement)
# E.g. '02-Knowledge/🧠 学习系统' or '99-System/🗓️ 计划执行系统' or '02-Knowledge/📚 书库' or '02-Knowledge/📚 论文库' not preceded by '02-Knowledge/' or '99-System/'
pattern_dv = re.compile(r'(?<!02-Knowledge/)(?<!02-Knowledge\\)(?<!99-System/)(?<!99-System\\)(02-Knowledge/🧠 学习系统|99-System/🗓️ 计划执行系统|02-Knowledge/📚 书库|02-Knowledge/📚 论文库)')

dv_files = set()
dv_matches_cnt = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    if any(x in dirpath for x in ['.git', '.obsidian', '.claude']): continue
    for f in filenames:
        if f.endswith(('.md', '.py', '.js', '.json')):
            p = os.path.join(dirpath, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
            except Exception: continue
            
            matches = pattern_dv.findall(content)
            if matches:
                dv_files.add(os.path.relpath(p, root_dir))
                dv_matches_cnt += len(matches)

print(f"=== Dataview/Path Scan (without slash req) ===")
print(f"Total unprefixed path occurrences: {dv_matches_cnt} in {len(dv_files)} files")
for p in list(dv_files)[:15]:
    print(f"  - {p}")

# 2. Check Git index lock
index_lock = os.path.join(root_dir, r'.git\index.lock')
print(f"\n=== Git Index Lock ===")
print(f".git/index.lock exists: {os.path.exists(index_lock)}")

