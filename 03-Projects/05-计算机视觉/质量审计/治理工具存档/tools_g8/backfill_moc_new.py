import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
KB = "F:" + os.sep + "-"
B = "02-Knowledge/🧠 学习系统/05-计算机视觉"

# 概念行关键字 -> (卡短名, 完整路径)
BACKFILL = {
    # 阶段3：DETR / 知识蒸馏
    "DETR": ("DETR", B + "/03-视觉核心任务/DETR"),
    "模型蒸馏": ("知识蒸馏", B + "/03-视觉核心任务/知识蒸馏"),
    # 阶段4：DeiT / CLIP
    "DeiT": ("DeiT", B + "/04-前沿架构探索/DeiT"),
    "CLIP": ("CLIP", B + "/04-前沿架构探索/CLIP"),
    # 阶段5：TensorRT / 目标跟踪
    "TensorRT": ("TensorRT", B + "/05-专业深化与工程落地/TensorRT"),
    "目标跟踪": ("目标跟踪", B + "/05-专业深化与工程落地/目标跟踪"),
}

MOCS = [
    KB + "/02-Knowledge/🧠 学习系统/05-计算机视觉/03-视觉核心任务/🎯 第三阶段：视觉核心任务.md",
    KB + "/02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🚀 第四阶段：前沿架构探索.md",
    KB + "/02-Knowledge/🧠 学习系统/05-计算机视觉/05-专业深化与工程落地/🏭 第五阶段：专业深化与工程落地.md",
]

total = 0
for p in MOCS:
    with open(p, encoding='utf-8') as f:
        lines = f.readlines()
    changed = False
    for i, line in enumerate(lines):
        if not line.lstrip().startswith('|') or '⬜' not in line:
            continue
        for kw, (card, full) in BACKFILL.items():
            if '**' + kw + '**' in line:
                # 状态 ⬜ -> ✅
                new_line = line.replace('⬜', '✅')
                # 笔记列（最后一个非空 cell）-> 完整路径链接
                cells = new_line.split('|')
                for j in range(len(cells) - 1, 0, -1):
                    if cells[j].strip():
                        cells[j] = ' [[' + full + '\\|' + card + ']] '
                        break
                new_line = '|'.join(cells)
                if new_line != line:
                    lines[i] = new_line
                    changed = True
                    total += 1
                    print(f"{os.path.basename(p)} L{i+1}: {kw} ⬜→✅ 回填 {card}")
                break
    if changed:
        with open(p, 'w', encoding='utf-8') as f:
            f.writelines(lines)
print(f"回填 {total} 行")
