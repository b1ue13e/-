import os
import sys
import re
import yaml

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'
fm_re = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

yaml_errors = []

for dirpath, dirnames, filenames in os.walk(root_dir):
    dirnames[:] = [d for d in dirnames if d not in ['.git', '.obsidian', '.claude', 'tmp', 'exports', '书籍资源'] and not d.startswith('.')]
    for f in filenames:
        if f.endswith('.md'):
            p = os.path.join(dirpath, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
            except Exception:
                continue
            m = fm_re.match(content)
            if m:
                raw = m.group(1)
                try:
                    yaml.safe_load(raw)
                except Exception as e:
                    yaml_errors.append((p, raw, str(e)))

print(f"Found {len(yaml_errors)} YAML parsing errors:")
for p, raw, err in yaml_errors:
    print(f"\nFile: {os.path.relpath(p, root_dir)}")
    print(f"Error: {err.splitlines()[0]}")
    # Attempt simple auto-fixes
    lines = raw.splitlines()
    fixed_lines = []
    for line in lines:
        # Quote unquoted colons inside strings or list items
        if ':' in line and not line.strip().startswith('#'):
            parts = line.split(':', 1)
            key = parts[0]
            val = parts[1].strip()
            if val and not (val.startswith('"') or val.startswith("'") or val.startswith('[') or val.startswith('{')):
                if any(c in val for c in [':', '[', ']', '#', '@']):
                    clean_val = val.replace('"', '\\"')
                    line = f'{key}: "{clean_val}"'
        fixed_lines.append(line)
    fixed_yaml = '\n'.join(fixed_lines)
    try:
        yaml.safe_load(fixed_yaml)
        new_content = f"---\n{fixed_yaml}\n---\n" + content[m.end():]
        with open(p, 'w', encoding='utf-8') as fp:
            fp.write(new_content)
        print(f"  ===> FIXED SUCCESSFULLY!")
    except Exception as e2:
        print(f"  ===> Manual fix needed: {e2.splitlines()[0]}")
