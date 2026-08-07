# -*- coding: utf-8 -*-
"""B11: 重复卡组内容重叠度检测"""
import re, io, os

BASE = r'F:\-\02-Knowledge\🧠 学习系统\05-计算机视觉'

GROUPS = {
    '计算图组': ['02-深度学习内核/计算图.md', '02-深度学习内核/反向传播与计算图.md'],
    'SimCLR组': ['04-前沿架构探索/自监督学习SimCLR与CLIP.md', '04-前沿架构探索/计算机视觉-SimCLR与对比学习.md', '04-前沿架构探索/计算机视觉-CLIP.md'],
    '生成模型组': ['04-前沿架构探索/生成模型GAN与Diffusion.md', '04-前沿架构探索/计算机视觉-Diffusion扩散模型.md', '04-前沿架构探索/计算机视觉-VAE变分自编码器.md'],
    'Transformer组': ['04-前沿架构探索/Transformer与自注意力.md', '04-前沿架构探索/Transformer架构演进.md'],
}

def tokenize(path):
    with io.open(os.path.join(BASE, path), encoding='utf-8-sig', errors='replace') as f:
        content = f.read()
    # 去掉 markdown 语法，取中文+英文词
    text = re.sub(r'[#*`|\[\]()\-—=\n\r\t>]', ' ', content)
    # 中文二元组 + 英文单词
    tokens = set()
    for m in re.findall(r'[\u4e00-\u9fff]{2,4}', text):
        tokens.add(m)
    for m in re.findall(r'[A-Za-z]{3,}', text):
        tokens.add(m.lower())
    return tokens, len(text)

for gname, paths in GROUPS.items():
    print(f'===== {gname} =====')
    tok_data = []
    for p in paths:
        tokens, size = tokenize(p)
        tok_data.append((p, tokens, size))
        print(f'  {p}: 词汇量 {len(tokens)}, 文本量 {size}')
    # 两两重叠
    for i in range(len(tok_data)):
        for j in range(i+1, len(tok_data)):
            p1, t1, s1 = tok_data[i]
            p2, t2, s2 = tok_data[j]
            inter = len(t1 & t2)
            union = len(t1 | t2)
            jaccard = inter / union if union else 0
            # 覆盖率：p1 词汇在 p2 中的比例
            cov12 = len(t1 & t2) / len(t1) if t1 else 0
            cov21 = len(t1 & t2) / len(t2) if t2 else 0
            print(f'  Jaccard={jaccard:.2f} | {os.path.basename(p1)} 词被 {os.path.basename(p2)} 覆盖 {cov12:.2f} | 反向 {cov21:.2f}')
    print()
