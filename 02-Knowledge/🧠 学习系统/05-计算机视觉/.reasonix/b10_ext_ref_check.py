# -*- coding: utf-8 -*-
"""B10: 检查 CV 外文件中 MLP/ResNet/AlexNet/FPN 引用的上下文，判断指向"""
import os, re, io

VAULT = r'F:\-'
FILES = [
    r'02-Knowledge\🧠 学习系统\🎭 深度学习框架\01-深度学习核心\🧠 第二阶段：深度学习内核（模型本质）.md',
    r'02-Knowledge\🧠 学习系统\🎭 深度学习框架\锚框 Anchor Box.md',
]
PATTERNS = {
    'MLP': r'\[\[([^\]\n#|]*?/)?MLP(\|[^\]]*?)?\]\]',
    'ResNet': r'\[\[([^\]\n#|]*?/)?ResNet(\|[^\]]*?)?\]\]',
    'AlexNet': r'\[\[([^\]\n#|]*?/)?AlexNet(\|[^\]]*?)?\]\]',
    'FPN': r'\[\[([^\]\n#|]*?/)?FPN(\|[^\]]*?)?\]\]',
    'ViT': r'\[\[([^\]\n#|]*?/)?ViT(\|[^\]]*?)?\]\]',
}
for fp in FILES:
    full = os.path.join(VAULT, fp)
    if not os.path.exists(full):
        print('MISSING:', fp); continue
    with io.open(full, encoding='utf-8-sig', errors='replace') as f:
        lines = f.read().split('\n')
    print(f'===== {fp} =====')
    for key, pat in PATTERNS.items():
        for i, line in enumerate(lines, 1):
            for m in re.finditer(pat, line):
                # 打印该行上下文
                ctx_start = max(0, i-2)
                ctx_end = min(len(lines), i+1)
                print(f'  [{key} @ L{i}] {" / ".join(l.strip()[:100] for l in lines[ctx_start:ctx_end])}')
    print()
