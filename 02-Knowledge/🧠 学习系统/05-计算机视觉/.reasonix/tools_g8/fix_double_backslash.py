import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
KB = "F:" + os.sep + "-"
COURSE = KB + os.sep + "02-Knowledge" + os.sep + "🧠 学习系统" + os.sep + "05-计算机视觉"
SKIP = {'.归档', '.reasonix', '.recovery-hold', '.pytest_cache', '__pycache__', '.git', '.obsidian', '.tmp'}
WIKI = re.compile(r'\[\[([^\]]+)\]\]')
DOUBLE = re.compile(r'\\\\\|')  # 字面 \\|

def fix_wiki(m):
    return '[[' + DOUBLE.sub(r'\\|', m.group(1)) + ']]'

total = 0
files_changed = 0
for root, dirs, files in os.walk(COURSE):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for f in files:
        if not f.endswith('.md'):
            continue
        p = os.path.join(root, f)
        with open(p, encoding='utf-8') as fh:
            content = fh.read()
        before = content.count('\\\\|')
        if before == 0:
            continue
        new = WIKI.sub(fix_wiki, content)
        after = new.count('\\\\|')
        n = before - after
        if n > 0:
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(new)
            total += n
            files_changed += 1
            print(os.path.relpath(p, COURSE), f"修正 {n}（剩余 {after}）")
print(f"共修正 {total} 处（{files_changed} 文件）")
