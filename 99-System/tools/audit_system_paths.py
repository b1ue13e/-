import os
import sys
import re
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

old_paths = [
    '02-Knowledge/🧠 学习系统/',
    '99-System/🗓️ 计划执行系统/',
    '02-Knowledge/📚 书库/',
    '02-Knowledge/📚 论文库/'
]

file_matches = defaultdict(int)
file_lists = defaultdict(list)
dv_file_matches = defaultdict(list)

# Regex for Dataview queries like dv.pages('"02-Knowledge/🧠 学习系统/..."') or FROM "02-Knowledge/🧠 学习系统/..."
dv_re = re.compile(r'(dv\.pages\(|FROM\s+|table\s+|list\s+|task\s+).*?(02-Knowledge/🧠 学习系统|99-System/🗓️ 计划执行系统|02-Knowledge/📚 书库|02-Knowledge/📚 论文库)', re.IGNORECASE)

md_files = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    if any(x in dirpath for x in ['.git', '.obsidian', '.claude']):
        continue
    for f in filenames:
        if f.endswith(('.md', '.py', '.ps1', '.js', '.json')):
            md_files.append(os.path.join(dirpath, f))

print(f"Total target text files scanned: {len(md_files)}")

for p in md_files:
    rel_p = os.path.relpath(p, root_dir)
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        continue
        
    for op in old_paths:
        # Match unprefixed occurrences: NOT preceded by 02-Knowledge/ or 99-System/
        pattern = re.compile(rf'(?<!02-Knowledge/)(?<!99-System/){re.escape(op)}')
        matches = pattern.findall(content)
        if matches:
            file_matches[op] += len(matches)
            file_lists[op].append(rel_p)
            
    # Check Dataview specifically
    if 'dataview' in content.lower() or 'dv.pages' in content or '```dataview' in content:
        for op in old_paths:
            pattern = re.compile(rf'(?<!02-Knowledge/)(?<!99-System/){re.escape(op)}')
            if pattern.search(content):
                dv_file_matches[op].append(rel_p)

print("\n=========================================")
print("1. 未修饰旧路径在文件中的出现次数统计")
print("=========================================")
for op, count in file_matches.items():
    print(f"  {op:<15}: {count:5d} 次 (涉及 {len(file_lists[op])} 个文件)")

print("\n=========================================")
print("2. 含有未修饰旧路径的 Dataview 查询文件统计")
print("=========================================")
for op, flist in dv_file_matches.items():
    print(f"\n路径 [{op}] 影响的 Dataview 文件 ({len(flist)} 个):")
    for fpath in flist[:10]:
        print(f"  - {fpath}")

