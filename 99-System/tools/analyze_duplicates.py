import sys
import os
import glob
import re
import hashlib
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

root_dir = r'f:\-'
md_files = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    if any(x in dirpath for x in ['.git', '.obsidian', '.claude', '.claudian', '.tmp.drive']):
        continue
    for f in filenames:
        if f.endswith('.md'):
            md_files.append(os.path.join(dirpath, f))

print(f"Total MD files scanned: {len(md_files)}")

name_map = defaultdict(list)
topic_map = defaultdict(list)
concept_map = defaultdict(list)
hash_map = defaultdict(list)

fm_topic_re = re.compile(r'^topic:\s*[\"\\\']?(.*?)[\"\\\']?\s*$', re.MULTILINE)
fm_concept_re = re.compile(r'^concept:\s*\[(.*?)\]', re.MULTILINE)
h1_re = re.compile(r'^#\s+(.*)$', re.MULTILINE)

system_indexes = {
    'readme.md', '🗺️ 学习路径.md', '阶段1：基础理论.md', '阶段2：进阶应用.md', 
    '阶段3：前沿拓展.md', '00-📥 inbox.md', '01-🚀 active sprint.md',
    '03-🛠️ projects.md', '04-🔁 review.md', '🏠 主页.md'
}

for p in md_files:
    fname = os.path.basename(p)
    rel_path = os.path.relpath(p, root_dir)
    name_map[fname.lower()].append(rel_path)
    
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        continue
    
    clean_text = content.strip()
    if len(clean_text) > 50:
        # Ignore frontmatter timestamps or minor whitespace differences
        text_body = re.sub(r'---.*?---', '', clean_text, flags=re.DOTALL).strip()
        chash = hashlib.md5(text_body.encode('utf-8')).hexdigest()
        hash_map[chash].append(rel_path)
    
    # Topic
    m_topic = fm_topic_re.search(content)
    topic_val = m_topic.group(1).strip() if m_topic else None
    if not topic_val:
        m_h1 = h1_re.search(content)
        topic_val = m_h1.group(1).strip() if m_h1 else None
        
    if topic_val and len(topic_val) > 1 and fname.lower() not in system_indexes:
        topic_map[topic_val.lower()].append((rel_path, fname))

    # Concepts
    m_concept = fm_concept_re.search(content)
    if m_concept:
        raw_c = m_concept.group(1)
        concepts = [c.strip().strip('"\'') for c in raw_c.split(',') if c.strip()]
        for c in concepts:
            if c:
                concept_map[c.lower()].append(rel_path)

print("\n=========================================")
print("1. 完全相同内容的文件 (MD5 包含 Frontmatter 后的正文解耦)")
print("=========================================")
exact_content_dups = {k: v for k, v in hash_map.items() if len(v) > 1}
print(f"找到 {len(exact_content_dups)} 组完全相同内容的文件:")
for k, v in list(exact_content_dups.items())[:20]:
    print(f"\n[组 hash: {k[:8]}]")
    for path in v:
        print(f"  - {path}")

print("\n=========================================")
print("2. 跨目录同名笔记 (Duplicate Filenames)")
print("=========================================")
dup_names = {k: v for k, v in name_map.items() if len(v) > 1 and k not in system_indexes}
print(f"找到 {len(dup_names)} 个非系统索引的同名文件:")
for k, v in list(dup_names.items())[:30]:
    print(f"\n文件名: {k}")
    for path in v:
        print(f"  - {path}")

print("\n=========================================")
print("3. 主题/Topic 完全相同的笔记")
print("=========================================")
dup_topics = {k: v for k, v in topic_map.items() if len(v) > 1}
print(f"找到 {len(dup_topics)} 组 Topic/H1 相同但文件名或路径不同的笔记:")
for k, v in list(dup_topics.items())[:30]:
    print(f"\n主题: \"{k}\"")
    for rel_path, fname in v:
        print(f"  - [{fname}] 在 {rel_path}")

