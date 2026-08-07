import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
KB = "F:" + os.sep + "-"
B = "02-Knowledge/🧠 学习系统/05-计算机视觉"

# 目标：将 `[[<full>\| [[<full>\|<card>]]` 还原为 `[[<full>\|<card>]]`
MOCS = [
    KB + "/02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🚀 第四阶段：前沿架构探索.md",
    KB + "/02-Knowledge/🧠 学习系统/05-计算机视觉/03-视觉核心任务/🎯 第三阶段：视觉核心任务.md",
    KB + "/02-Knowledge/🧠 学习系统/05-计算机视觉/05-专业深化与工程落地/🏭 第五阶段：专业深化与工程落地.md",
]
pat = re.compile(r'\[\[([^\[\]]+?)\\\| \[\[([^\[\]]+?)\\\|([^\[\]]+?)\]\]')
total = 0
for p in MOCS:
    with open(p, encoding='utf-8') as f:
        content = f.read()
    new = pat.sub(r'[[\1|\3]]', content)
    n = len(re.findall(pat, content))
    if n:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(new)
        total += n
        print(os.path.basename(p), "修复", n, "处")
print("总计修复", total)
