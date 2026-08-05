import os
import re

# Find all markdown files under current directory (excluding .git)
all_md = []
for root, dirs, files in os.walk('.'):
    # Skip .git directories
    dirs[:] = [d for d in dirs if d != '.git']
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            all_md.append(path)

# Categorize files
empty_files = []
only_frontmatter = []  # Has frontmatter but no real content after it
placeholder_named = []  # Named with placeholder keywords

for path in all_md:
    try:
        size = os.path.getsize(path)
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Skip plan execution system files (they are templates, not placeholders)
        if '计划执行系统' in path:
            continue
        
        if size == 0:
            empty_files.append(path)
            continue
        
        stripped = content.strip()
        
        # Check if only frontmatter
        if stripped.startswith('---'):
            rest = stripped[3:]
            end_fm = rest.find('---')
            if end_fm != -1:
                after_fm = rest[end_fm+3:].strip()
                # If after frontmatter, content is very minimal
                if len(after_fm) < 50:
                    only_frontmatter.append((path, size, after_fm[:150]))
        
        # Check for placeholder in filename
        basename = os.path.basename(path).lower()
        placeholder_keywords = ['占位', 'placeholder', 'todo', '待补充']
        if any(k in basename for k in placeholder_keywords):
            placeholder_named.append((path, size, stripped[:200]))
            
    except Exception as e:
        pass

print("=== 空文件 (0字节) ===")
for p in empty_files:
    print(f"  {p}")

print(f"\n=== 仅有 frontmatter、无实质内容的文件 ({len(only_frontmatter)}个) ===")
for p, s, after in only_frontmatter:
    print(f"  {s:>5} bytes | {p}")
    if after:
        print(f"    剩余内容: {repr(after)}")

print(f"\n=== 文件名含'占位'等关键词的文件 ({len(placeholder_named)}个) ===")
for p, s, content in placeholder_named:
    print(f"  {s:>5} bytes | {p}")

print(f"\n总计: {len(empty_files)} 空文件, {len(only_frontmatter)} 仅有frontmatter, {len(placeholder_named)} 占位名文件")
print(f"总md文件数: {len(all_md)}")
