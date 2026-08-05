import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

# Paths to replace: (pattern_regex, replacement_str)
replacements = [
    (re.compile(r'(?<!02-Knowledge/)02-Knowledge/🧠 学习系统/'), '02-Knowledge/🧠 学习系统/'),
    (re.compile(r'(?<!99-System/)99-System/🗓️ 计划执行系统/'), '99-System/🗓️ 计划执行系统/'),
    (re.compile(r'(?<!02-Knowledge/)02-Knowledge/📚 书库/'), '02-Knowledge/📚 书库/'),
    (re.compile(r'(?<!02-Knowledge/)02-Knowledge/📚 论文库/'), '02-Knowledge/📚 论文库/'),
]

# Skip .git, .obsidian, .claude, etc.
skip_dirs = {'.git', '.obsidian', '.claude'}

modified_files = 0
total_replacements = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    if any(sd in dirpath for sd in skip_dirs):
        continue
        
    for f in filenames:
        if f.endswith(('.md', '.py', '.ps1', '.js', '.json', '.base')):
            abs_p = os.path.join(dirpath, f)
            rel_p = os.path.relpath(abs_p, root_dir)
            
            # Don't modify batch_fix_vault_paths.py itself
            if 'batch_fix_vault_paths.py' in f:
                continue
                
            try:
                with open(abs_p, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
            except Exception:
                continue
                
            new_content = content
            file_changed = False
            
            for pat, rep in replacements:
                if pat.search(new_content):
                    new_content, count = pat.subn(rep, new_content)
                    total_replacements += count
                    file_changed = True
                    
            if file_changed:
                with open(abs_p, 'w', encoding='utf-8') as fp:
                    fp.write(new_content)
                modified_files += 1

print(f"✅ Vault path batch migration completed.")
print(f"Modified Files: {modified_files}")
print(f"Total Path Replacements: {total_replacements}")

