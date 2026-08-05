import sys
import os
import glob
import re
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

root_dir = r'f:\-'
scan_dirs = ['00-Inbox', '01-Active Sprint', '02-Knowledge', '03-Projects', '04-Review']

md_files = []
for sd in scan_dirs:
    full_sd = os.path.join(root_dir, sd)
    if os.path.exists(full_sd):
        for dirpath, dirnames, filenames in os.walk(full_sd):
            for f in filenames:
                if f.endswith('.md'):
                    md_files.append(os.path.join(dirpath, f))

# Standardize titles/concepts
def get_canonical_concept(title_str):
    t = title_str.lower()
    t = re.sub(r'[\.md\s\-_\(\)（）]', '', t)
    # Common mappings
    t = re.sub(r'算法$', '', t)
    t = re.sub(r'优化器$', '', t)
    t = re.sub(r'模型$', '', t)
    t = re.sub(r'定义$', '', t)
    t = re.sub(r'基础$', '', t)
    t = re.sub(r'实现$', '', t)
    t = re.sub(r'概述$', '', t)
    return t

canonical_map = defaultdict(list)
full_title_map = defaultdict(list)

for p in md_files:
    fname = os.path.basename(p)
    rel_path = os.path.relpath(p, root_dir)
    
    if fname in ['🗺️ 学习路径.md', '阶段1：基础理论.md', '阶段2：进阶应用.md', '阶段3：前沿拓展.md', '📚 教材挂载索引.md']:
        continue
    if fname.startswith('占位-'):
        continue

    # Path classification
    path_match = re.search(r'02-Knowledge/🧠 学习系统\\([^\\]+)', rel_path)
    path_name = path_match.group(1) if path_match else rel_path.split('\\')[0]

    title = os.path.splitext(fname)[0]
    full_title_map[title.lower()].append((rel_path, path_name))
    
    canon = get_canonical_concept(title)
    if len(canon) >= 2:
        canonical_map[canon].append((rel_path, path_name, fname))

print("=== EXACT DUPLICATE TITLES ===")
for title, list_info in full_title_map.items():
    if len(list_info) > 1:
        paths = set(x[1] for x in list_info)
        print(f"\nTitle: {title} (Across {len(paths)} locations)")
        for rel_path, path_name in list_info:
            print(f"  - [{path_name}] {rel_path}")

print("\n=== SEMANTIC / CANONICAL CONCEPT DUPLICATES ACROSS DIFFERENT LEARNING PATHS ===")
for canon, list_info in canonical_map.items():
    paths = set(x[1] for x in list_info)
    if len(paths) > 1: # Spans multiple learning paths
        # Check if titles are different or same
        fnames = set(x[2] for x in list_info)
        print(f"\nConcept Cluster: '{canon}' (Files: {', '.join(fnames)})")
        for rel_path, path_name, fname in list_info:
            print(f"  - [{path_name}] {rel_path}")

