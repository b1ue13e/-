import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
KB = "F:" + os.sep + "-"
MOCS = [
    KB + "/02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🚀 第四阶段：前沿架构探索.md",
    KB + "/02-Knowledge/🧠 学习系统/05-计算机视觉/03-视觉核心任务/🎯 第三阶段：视觉核心任务.md",
    KB + "/02-Knowledge/🧠 学习系统/05-计算机视觉/05-专业深化与工程落地/🏭 第五阶段：专业深化与工程落地.md",
]
# 表格行内：[[full|card]] -> [[full\|card]]（full 含 / 但无 |）
pat = re.compile(r'(\[\[[^\]\n]+?)\|([^\]\n]+?\]\])')
total = 0
for p in MOCS:
    with open(p, encoding='utf-8') as f:
        lines = f.readlines()
    changed = False
    for i, line in enumerate(lines):
        if not line.lstrip().startswith('|'):
            continue
        new_line = pat.sub(r'\1\\|\2', line)
        if new_line != line:
            lines[i] = new_line
            changed = True
            total += 1
    if changed:
        with open(p, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(os.path.basename(p), "转义", total)
print("总计转义表格行", total)
