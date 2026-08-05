import sys
import os
import glob
import re
import hashlib
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

root_dir = r'f:\-'

# Paths to scan (active knowledge areas)
scan_dirs = ['00-Inbox', '01-Active Sprint', '02-Knowledge', '03-Projects', '04-Review']

md_files = []
for sd in scan_dirs:
    full_sd = os.path.join(root_dir, sd)
    if os.path.exists(full_sd):
        for dirpath, dirnames, filenames in os.walk(full_sd):
            for f in filenames:
                if f.endswith('.md'):
                    md_files.append(os.path.join(dirpath, f))

print(f"Total Active MD files scanned in {scan_dirs}: {len(md_files)}")

# 1. Exact Filenames Duplicates across active dirs
name_map = defaultdict(list)

# 2. Topic/Title Duplicates
topic_map = defaultdict(list)

# 3. Core Concept duplicates (e.g., Adam, GCN, PCA, SVM, 梯度下降, 状态转移矩阵, etc.)
concept_extracted_map = defaultdict(list)

# 4. Granularity rule violations (e.g. XXX-概念, XXX-性质, XXX-检验, XXX-公式)
granularity_splits = defaultdict(list)

fm_topic_re = re.compile(r'^topic:\s*[\"\\\']?(.*?)[\"\\\']?\s*$', re.MULTILINE)
fm_concept_re = re.compile(r'^concept:\s*\[(.*?)\]', re.MULTILINE)
h1_re = re.compile(r'^#\s+(.*)$', re.MULTILINE)

def clean_concept_name(name):
    # strip extensions, sub-topic prefixes like "深度学习-优化器-Adam" -> "Adam"
    base = os.path.splitext(name)[0]
    base = re.sub(r'^\d+[\s\-_]*', '', base) # remove leading numbers
    parts = re.split(r'[\-_]', base)
    return parts[-1].strip()

for p in md_files:
    fname = os.path.basename(p)
    rel_path = os.path.relpath(p, root_dir)
    
    # Ignore roadmap index files
    if fname in ['🗺️ 学习路径.md', '阶段1：基础理论.md', '阶段2：进阶应用.md', '阶段3：前沿拓展.md', '📚 教材挂载索引.md']:
        continue
        
    name_map[fname.lower()].append(rel_path)
    
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        continue
        
    # Topic
    m_topic = fm_topic_re.search(content)
    topic_val = m_topic.group(1).strip() if m_topic else None
    if not topic_val:
        m_h1 = h1_re.search(content)
        topic_val = m_h1.group(1).strip() if m_h1 else None
        
    if topic_val and len(topic_val) > 1:
        topic_map[topic_val.strip().lower()].append((rel_path, fname))
        
    # Extracted core concept
    core_c = clean_concept_name(fname)
    if len(core_c) >= 2:
        concept_extracted_map[core_c.lower()].append(rel_path)
        
    # Granularity check (e.g. 概念-主题卡/ or splitting like XXX直观, XXX统计性质)
    m_gran = re.search(r'(.+?)(直观理解|统计性质|检验|重要性|定义|推导|实现|算法)$', fname.replace('.md', ''))
    if m_gran:
        stem = m_gran.group(1)
        granularity_splits[stem].append(rel_path)

print("\n" + "="*60)
print("【维度 1】物理级完全同名笔记 (同名 md 文件分布在不同路径)")
print("="*60)
dup_names = {k: v for k, v in name_map.items() if len(v) > 1}
print(f"找到 {len(dup_names)} 组活跃物理同名文件：")
for k, v in list(dup_names.items()):
    print(f"\n📄 文件名: {k}")
    for path in v:
        print(f"  - {path}")

print("\n" + "="*60)
print("【维度 2】语义级相同主题/标题笔记 (Topic / H1 完全相同)")
print("="*60)
dup_topics = {k: v for k, v in topic_map.items() if len(v) > 1}
print(f"找到 {len(dup_topics)} 组活跃主题/标题完全一致的笔记：")
for k, v in list(dup_topics.items())[:25]:
    print(f"\n📌 主题: \"{k}\"")
    for rel_path, fname in v:
        print(f"  - [{fname}] ({rel_path})")

print("\n" + "="*60)
print("【维度 3】跨路径重复的核心知识点/概念 (跨学科路径重复)")
print("="*60)
cross_path_dups = {}
for concept, paths in concept_extracted_map.items():
    if len(paths) > 1:
        # Check if they span different learning paths
        learning_paths = set()
        for pt in paths:
            m = re.search(r'(\d{2}-[^\\]+)', pt)
            if m:
                learning_paths.add(m.group(1))
        if len(learning_paths) > 1:
            cross_path_dups[concept] = paths

print(f"找到 {len(cross_path_dups)} 个跨学习路径重复出现的核心知识概念：")
for concept, paths in list(cross_path_dups.items())[:30]:
    print(f"\n🧠 核心概念: {concept}")
    for pt in paths:
        print(f"  - {pt}")

print("\n" + "="*60)
print("【维度 4】违反“主题卡优先”粒度规则的细分碎片笔记 (同一概念拆成多个微卡)")
print("="*60)
gran_dups = {k: v for k, v in granularity_splits.items() if len(v) > 1}
print(f"找到 {len(gran_dups)} 组被过度拆分的碎片笔记：")
for stem, paths in list(gran_dups.items())[:20]:
    print(f"\n🧩 概念主干: {stem}")
    for pt in paths:
        print(f"  - {pt}")

