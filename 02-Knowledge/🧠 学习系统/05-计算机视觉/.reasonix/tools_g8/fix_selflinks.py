import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
KB = "F:" + os.sep + "-"
COURSE = KB + os.sep + "02-Knowledge" + os.sep + "🧠 学习系统" + os.sep + "05-计算机视觉"
SKIP = {'.归档', '.reasonix', '.recovery-hold', '.pytest_cache', '__pycache__', '.git', '.obsidian', '.tmp'}
WIKI = re.compile(r'\[\[([^\]]+)\]\]')

def walk_md(base):
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for f in files:
            if f.endswith('.md'):
                yield os.path.join(root, f)

# 全库短名索引（用于解析）
SHORT = {}
for root, dirs, files in os.walk(KB):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for f in files:
        if f.endswith('.md'):
            SHORT.setdefault(f[:-3], []).append(os.path.join(root, f))

def file_fullname(p):
    """返回该文件作为链接目标的标准完整路径（无 .md）"""
    rel = os.path.relpath(p, KB).replace('\\', '/')[:-3]
    return rel

total_fixed = 0
for p in walk_md(COURSE):
    self_target = file_fullname(p)
    rel = os.path.relpath(p, COURSE)
    with open(p, encoding='utf-8') as f:
        lines = f.readlines()
    changed = []
    for i, line in enumerate(lines):
        new_line = line
        for m in WIKI.finditer(line):
            raw = m.group(1)
            # 解析 target（处理 \| 转义与 | 分隔）
            t = re.sub(r'\\\|.*$', '', raw)
            t = t.split('#')[0].split('|')[0].strip().removesuffix('.md')
            if t == self_target:
                # 自链接 → 去链接保留文字（别名优先）
                alias = None
                if '\\|' in raw:
                    alias = raw.split('\\|', 1)[1]
                elif '|' in raw:
                    alias = raw.split('|', 1)[1]
                text = alias if alias else t.split('/')[-1]
                new_line = new_line.replace('[[' + raw + ']]', text)
                total_fixed += 1
        if new_line != line:
            changed.append((i + 1, line.rstrip('\n'), new_line.rstrip('\n')))
            lines[i] = new_line
    if changed:
        print(f"\n=== {rel} ({len(changed)} 行)")
        for ln, old, new in changed[:6]:
            print(f"  L{ln} {old.strip()[:80]}")
            print(f"     -> {new.strip()[:80]}")
        with open(p, 'w', encoding='utf-8') as f:
            f.writelines(lines)
print(f"\n清理自链接 {total_fixed} 处")
