import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

target_files = [
    r'02-Knowledge\🧠 学习系统\12-信号与系统\📓 信号与系统单知识点深度学习模板.md',
    r'99-System\📇 模板\Obsidian单知识点深度学习模板.md',
    r'02-Knowledge\🧠 学习系统\26-实变函数\03-微分与函数空间\微分与函数空间-Lp 与函数空间-L∞.md',
    r'02-Knowledge\🧠 学习系统\26-实变函数\03-微分与函数空间\微分与函数空间-绝对连续与微分-绝对连续.md'
]

for rel_p in target_files:
    abs_p = os.path.join(root_dir, rel_p)
    if not os.path.exists(abs_p):
        continue
    with open(abs_p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Fix Templater placeholders date: {{date}} -> date: "{{date}}"
    new_c = content.replace('date: {{date}}', 'date: "{{date}}"')
    # Fix unescaped backslashes in double-quoted YAML strings like "$L^\infty$"
    new_c = new_c.replace(r'"$L^\infty$空间"', r"'$L^\infty$空间'")
    new_c = new_c.replace(r'"$L^1$空间对偶"', r"'$L^1$空间对偶'")
    
    if new_c != content:
        with open(abs_p, 'w', encoding='utf-8') as f:
            f.write(new_c)
        print(f"✅ Fixed YAML in {rel_p}")

