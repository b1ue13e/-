import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

# Simple, foolproof replacement:
# Match '02-Knowledge/🧠 学习系统/' ONLY if the preceding 13 chars are NOT '02-Knowledge/' and NOT '02-Knowledge\'
def fix_content(text):
    changed = False
    
    # 1. 02-Knowledge/🧠 学习系统/
    def replace_study(m):
        start = m.start()
        prefix = text[max(0, start-13):start]
        if prefix in ('02-Knowledge/', '02-Knowledge\\'):
            return m.group(0)
        return '02-Knowledge/🧠 学习系统/'
        
    new_text, n1 = re.subn(r'02-Knowledge/🧠 学习系统/', replace_study, text)
    if n1 > 0 and new_text != text:
        changed = True
        text = new_text

    # 2. 99-System/🗓️ 计划执行系统/
    def replace_sprint(m):
        start = m.start()
        prefix = text[max(0, start-10):start]
        if prefix in ('99-System/', '99-System\\'):
            return m.group(0)
        return '99-System/🗓️ 计划执行系统/'

    new_text, n2 = re.subn(r'99-System/🗓️ 计划执行系统/', replace_sprint, text)
    if n2 > 0 and new_text != text:
        changed = True
        text = new_text

    # 3. 02-Knowledge/📚 书库/
    def replace_books(m):
        start = m.start()
        prefix = text[max(0, start-13):start]
        if prefix in ('02-Knowledge/', '02-Knowledge\\'):
            return m.group(0)
        return '02-Knowledge/📚 书库/'

    new_text, n3 = re.subn(r'02-Knowledge/📚 书库/', replace_books, text)
    if n3 > 0 and new_text != text:
        changed = True
        text = new_text

    # 4. 02-Knowledge/📚 论文库/
    def replace_papers(m):
        start = m.start()
        prefix = text[max(0, start-13):start]
        if prefix in ('02-Knowledge/', '02-Knowledge\\'):
            return m.group(0)
        return '02-Knowledge/📚 论文库/'

    new_text, n4 = re.subn(r'02-Knowledge/📚 论文库/', replace_papers, text)
    if n4 > 0 and new_text != text:
        changed = True
        text = new_text

    return text, changed

skip_dirs = {'.git', '.obsidian', '.claude'}
modified_count = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    if any(sd in dirpath for sd in skip_dirs):
        continue
    for f in filenames:
        if f.endswith(('.md', '.py', '.ps1', '.js', '.json', '.base')):
            abs_p = os.path.join(dirpath, f)
            if 'fix_all_vault_paths_sync.py' in f or 'debug_path_fix.py' in f:
                continue
            try:
                with open(abs_p, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
            except Exception:
                continue
                
            new_content, changed = fix_content(content)
            if changed:
                with open(abs_p, 'w', encoding='utf-8') as fp:
                    fp.write(new_content)
                modified_count += 1

print(f"Sync migration completed. Modified {modified_count} files.")

