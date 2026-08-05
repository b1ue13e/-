import os
import sys
import re
import yaml

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

fm_re = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

def sanitize_line(line):
    if line.strip().startswith('upstream:') or line.strip().startswith('downstream:'):
        key = line.split(':', 1)[0].strip()
        links = re.findall(r'\[\[(.*?)\]\]', line)
        formatted_links = [f'"[[{l}]]"' for l in links]
        return f"{key}: [{', '.join(formatted_links)}]"
        
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

fixed_cnt = 0
active_errs = []

for p in md_files:
    rel_p = os.path.relpath(p, root_dir)
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
    except Exception: continue
    
    m = fm_re.match(content)
    if not m: continue
    
    raw_yaml = m.group(1)
    try:
        yaml.safe_load(raw_yaml)
    except Exception:
        lines = raw_yaml.splitlines()
        fixed_lines = [sanitize_line(l) for l in lines]
        repaired = '\n'.join(fixed_lines)
        
        try:
            yaml.safe_load(repaired)
            new_content = f"---\n{repaired}\n---\n" + content[m.end():]
            with open(p, 'w', encoding='utf-8') as fp:
                fp.write(new_content)
            fixed_cnt += 1
            print(f"✅ Fixed YAML in {rel_p}")
        except Exception as e:
            if '99-System\\tmp' not in rel_p:
                active_errs.append((rel_p, str(e).splitlines()[0]))

print(f"\nFixed {fixed_cnt} files.")
print(f"Remaining active note YAML errors: {len(active_errs)}")
if active_errs:
    for path, err in active_errs:
        print(f"  - [{path}]: {err}")

