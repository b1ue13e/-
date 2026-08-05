import os
import sys
import re
import yaml

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

fm_re = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

def repair_corrupted_line(line):
    # Fix corruptions like `"]]"]]"]]", "`
    if '"]]"]]' in line or ']]"]' in line:
        links = re.findall(r'\[\[(.*?)\]\]', line)
        if links:
            key = line.split(':', 1)[0].strip()
            formatted_links = [f'"[[{l}]]"' for l in links]
            return f"{key}: [{', '.join(formatted_links)}]"
            
    # Fix list items with colons inside strings
    m = re.match(r'^(\s*-\s*)([\"\\\']?\[\[.*?\]\][\"\\\']?):\s*(.*)$', line)
    if m:
        indent_dash = m.group(1)
        link_str = m.group(2).strip('"\'')
        val_str = m.group(3)
        return f'{indent_dash}"{link_str}：{val_str}"'
        
    return line

md_files = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    if any(x in dirpath for x in ['.git', '.obsidian', '.claude']): continue
    for f in filenames:
        if f.endswith('.md'):
            md_files.append(os.path.join(dirpath, f))

fixed_count = 0
still_errs = []

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
        lines = raw_yaml.splitlines()
        fixed_lines = [repair_corrupted_line(l) for l in lines]
        repaired_yaml = '\n'.join(fixed_lines)
        
        try:
            yaml.safe_load(repaired_yaml)
            new_content = f"---\n{repaired_yaml}\n---\n" + content[m.end():]
            with open(p, 'w', encoding='utf-8') as fp:
                fp.write(new_content)
            fixed_count += 1
        except Exception as e:
            still_errs.append((os.path.relpath(p, root_dir), str(e).splitlines()[0]))

print(f"Fixed {fixed_count} corrupted YAML frontmatters.")
print(f"Remaining errors count: {len(still_errs)}")
if still_errs:
    for path, err in still_errs:
        print(f"  - [{path}]: {err}")

