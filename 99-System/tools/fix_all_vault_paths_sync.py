import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

targets = [
    (re.compile(r'(?<!02-Knowledge/)(?<!02-Knowledge\\)🧠 学习系统'), '02-Knowledge/🧠 学习系统'),
    (re.compile(r'(?<!99-System/)(?<!99-System\\)🗓️ 计划执行系统'), '99-System/🗓️ 计划执行系统'),
    (re.compile(r'(?<!02-Knowledge/)(?<!02-Knowledge\\)📚 书库'), '02-Knowledge/📚 书库'),
    (re.compile(r'(?<!02-Knowledge/)(?<!02-Knowledge\\)📚 论文库'), '02-Knowledge/📚 论文库'),
]

skip_dirs = {'.git', '.obsidian', '.claude', 'tmp', 'exports', '.recovery-hold'}
skip_files = {'fix_all_vault_paths_sync.py', 'verify_vault_integrity.py', 'AGENTS.md'}

modified_files = 0
total_replacements = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith('.')]
    for f in filenames:
        if f in skip_files or not f.endswith(('.md', '.py', '.ps1', '.js', '.json', '.base')):
            continue
            
        abs_p = os.path.join(dirpath, f)
        try:
            with open(abs_p, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
        except Exception:
            continue
            
        new_content = content
        file_changed = False
        
        for pat, rep in targets:
            if pat.search(new_content):
                new_content, count = pat.subn(rep, new_content)
                total_replacements += count
                file_changed = True
                
        if file_changed:
            with open(abs_p, 'w', encoding='utf-8') as fp:
                fp.write(new_content)
            modified_files += 1

print(f"✅ Full vault path migration complete.")
print(f"Modified Files: {modified_files}")
print(f"Total Replacements: {total_replacements}")
