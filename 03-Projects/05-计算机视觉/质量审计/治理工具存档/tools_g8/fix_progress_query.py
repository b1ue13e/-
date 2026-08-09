import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
KB = "F:" + os.sep + "-"
COURSE = KB + os.sep + "02-Knowledge" + os.sep + "🧠 学习系统" + os.sep + "05-计算机视觉"
files = [
    COURSE + "/01-底层基石/🏗️ 第一阶段：底层基石.md",
    COURSE + "/02-深度学习内核/🧠 第二阶段：深度学习内核.md",
    COURSE + "/03-视觉核心任务/🎯 第三阶段：视觉核心任务.md",
    COURSE + "/04-前沿架构探索/🚀 第四阶段：前沿架构探索.md",
    COURSE + "/05-专业深化与工程落地/🏭 第五阶段：专业深化与工程落地.md",
    COURSE + "/🗺️ 计算机视觉学习路径.md",
]
# 把 .where(p => p.status === "completed") 改为计入 completed 或 ongoing
# 学习路径：统计已建卡（completed/ongoing）
old = 'p.status === "completed"'
new = '(p.status === "completed" || p.status === "ongoing")'
for p in files:
    with open(p, encoding='utf-8') as f:
        c = f.read()
    if old in c:
        c = c.replace(old, new)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print("已更新:", os.path.basename(p))
    else:
        print("跳过（无匹配）:", os.path.basename(p))
