import os
import sys
import re
import yaml

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

fm_re = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

def repair_yaml_str(yaml_str):
    lines = yaml_str.splitlines()
    fixed_lines = []
    
    for line in lines:
        # Fix pattern like:  - "[[something]]": text  or  - [[something]]: text
        # Convert colon after quote/link into Chinese colon ： or valid string
        m = re.match(r'^(\s*-\s*)([\"\\\']?\[\[.*?\]\][\"\\\']?):\s*(.*)$', line)
        if m:
            indent_dash = m.group(1)
            link_part = m.group(2).strip('"\'')
            val_part = m.group(3)
            fixed_lines.append(f'{indent_dash}"{link_part}：{val_part}"')
            continue
            
        # Fix unquoted list items containing colons like: - key: val where - "[[link]]": val
        m2 = re.match(r'^(\s*-\s*\".*?\"):\s*(.*)$', line)
        if m2:
            fixed_lines.append(f'{m2.group(1)}：{m2.group(2)}')
            continue

        # Fix key with unquoted brackets or colons
        m3 = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', line)
        if m3:
            key = m3.group(1)
            val = m3.group(2).strip()
            # If val contains unquoted brackets or colon that breaks YAML
            if val and not (val.startswith('"') or val.startswith("'") or val.startswith('[') or val.startswith('{')):
                if ':' in val or '[' in val or ']' in val or '#' in val or '@' in val:
                    # Sanitize quotes
                    clean_val = val.replace('"', '\\"')
                    fixed_lines.append(f'{key}: "{clean_val}"')
                    continue
                    
        fixed_lines.append(line)
        
    return '\n'.join(fixed_lines)

md_files = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    if any(x in dirpath for x in ['.git', '.obsidian', '.claude']): continue
    for f in filenames:
        if f.endswith('.md'):
            md_files.append(os.path.join(dirpath, f))

fixed_count = 0
remaining_errs = []

for p in md_files:
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
    except Exception: continue
    
    m = fm_re.match(content)
    if not m:
        continue
        
    raw_yaml = m.group(1)
    try:
        yaml.safe_load(raw_yaml)
    except Exception:
        # Repaired version
        repaired = repair_yaml_str(raw_yaml)
        try:
            yaml.safe_load(repaired)
            # Replaced successfully
            new_content = f"---\n{repaired}\n---\n" + content[m.end():]
            with open(p, 'w', encoding='utf-8') as fp:
                fp.write(new_content)
            fixed_count += 1
            print(f"✅ [YAML 自动修补成功] {os.path.relpath(p, root_dir)}")
        except Exception as e2:
            remaining_errs.append((os.path.relpath(p, root_dir), str(e2).splitlines()[0]))

print(f"\n=========================================")
print(f"YAML 修补工具完成：成功修补 {fixed_count} 篇笔记。")
print(f"剩余不可解析 YAML 数量: {len(remaining_errs)}")
print("=========================================")
if remaining_errs:
    for path, err in remaining_errs[:20]:
        print(f"  - [{path}]: {err}")

