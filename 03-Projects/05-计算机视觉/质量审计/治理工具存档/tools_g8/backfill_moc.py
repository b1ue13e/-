import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
KB = "F:" + os.sep + "-"
CV = os.path.join(KB, "02-Knowledge", "🧠 学习系统", "05-计算机视觉").replace("\\", "/")

# 概念行关键字 -> (已建卡短名, 完整路径-仓库根相对)
B = "02-Knowledge/🧠 学习系统/05-计算机视觉"
BACKFILL = {
    "Self-Attention": ("Transformer与自注意力", B + "/04-前沿架构探索/Transformer与自注意力"),
    "SimCLR": ("🎯 SimCLR 与对比学习 (Contrastive Learning)", B + "/04-前沿架构探索/🎯 SimCLR 与对比学习 (Contrastive Learning)"),
    "VAE": ("🎯 VAE 变分自编码器 (Variational Autoencoder)", B + "/04-前沿架构探索/🎯 VAE 变分自编码器 (Variational Autoencoder)"),
    "GAN": ("生成模型GAN与Diffusion", B + "/04-前沿架构探索/生成模型GAN与Diffusion"),
    "Diffusion": ("🎯 Diffusion 扩散模型 (DDPM)", B + "/04-前沿架构探索/🎯 Diffusion 扩散模型 (DDPM)"),
    "R-CNN": ("目标检测RCNN与YOLO", B + "/03-视觉核心任务/目标检测RCNN与YOLO"),
    "Fast R-CNN": ("目标检测RCNN与YOLO", B + "/03-视觉核心任务/目标检测RCNN与YOLO"),
    "Faster R-CNN": ("目标检测RCNN与YOLO", B + "/03-视觉核心任务/目标检测RCNN与YOLO"),
    "YOLOv1-v3": ("目标检测RCNN与YOLO", B + "/03-视觉核心任务/目标检测RCNN与YOLO"),
    "YOLOv4/v5/v8": ("目标检测RCNN与YOLO", B + "/03-视觉核心任务/目标检测RCNN与YOLO"),
    "NeRF": ("🎯 NeRF 神经辐射场 (Neural Radiance Fields)", B + "/05-专业深化与工程落地/🎯 NeRF 神经辐射场 (Neural Radiance Fields)"),
}

MOCS = [
    CV + "/04-前沿架构探索/🚀 第四阶段：前沿架构探索.md",
    CV + "/03-视觉核心任务/🎯 第三阶段：视觉核心任务.md",
    CV + "/05-专业深化与工程落地/🏭 第五阶段：专业深化与工程落地.md",
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
            # 匹配表格行中的 **关键词** 单元格
            if '**' + kw + '**' in line:
                # 状态列 ⬜ -> ✅，笔记列 '—' -> 完整路径链接
                new_line = line.replace('⬜', '✅').replace('| — |', '| [[' + full + '\\|' + card + ']] |')
                # 笔记列可能不是最后一个：确保只替换笔记列占位
                # 解析列：以 | 分割
                cells = new_line.split('|')
                # cells[0] 为空（行首 | 前），cells[-1] 为空（行尾 | 后）
                # 找笔记列 = 最后一个非空 cell
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
