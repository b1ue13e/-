# -*- coding: utf-8 -*-
"""B10: 查看每个旧名的引用明细（文件级），区分课程内/外"""
import os, re, io

VAULT = r'F:\-'
CV_PREFIX = '02-Knowledge/🧠 学习系统/05-计算机视觉'
EXCLUDE_DIRS = {'.workbuddy', '.归档', '.reasonix', '.recovery-hold', '.git', 'node_modules', '__pycache__', '.pytest_cache', '.tmp', '.obsidian'}

RENAME = {
    'SIFT': '计算机视觉-SIFT',
    'SVDCV': '计算机视觉-SVD分解',
    'AlexNet': '计算机视觉-AlexNet',
    'DenseNet': '计算机视觉-DenseNet',
    'GoogLeNet': '计算机视觉-GoogLeNet',
    'MLP': '计算机视觉-MLP',
    'VGGNet': '计算机视觉-VGGNet',
    'DETR': '计算机视觉-DETR',
    'FPN': '计算机视觉-FPN',
    'CLIP': '计算机视觉-CLIP',
    'DeiT': '计算机视觉-DeiT',
    'LoRA': '计算机视觉-LoRA',
    'MAE': '计算机视觉-MAE',
    'SwinTransformer': '计算机视觉-SwinTransformer',
    'ViT': '计算机视觉-ViT',
    'TensorRT': '计算机视觉-TensorRT',
    '🎯 ResNet (残差网络)': '计算机视觉-ResNet',
    '🎯 Diffusion 扩散模型 (DDPM)': '计算机视觉-Diffusion扩散模型',
    '🎯 SimCLR 与对比学习 (Contrastive Learning)': '计算机视觉-SimCLR与对比学习',
    '🎯 VAE 变分自编码器 (Variational Autoencoder)': '计算机视觉-VAE变分自编码器',
    '🎯 NeRF 神经辐射场 (Neural Radiance Fields)': '计算机视觉-NeRF神经辐射场',
    '🎯 相机标定与对极几何 (Epipolar Geometry)': '计算机视觉-相机标定与对极几何',
    '🏗️ 第一阶段：底层基石': '🧭 阶段1-底层基石',
    '🧠 第二阶段：深度学习内核': '🧭 阶段2-深度学习内核',
    '🎯 第三阶段：视觉核心任务': '🧭 阶段3-视觉核心任务',
    '🚀 第四阶段：前沿架构探索': '🧭 阶段4-前沿架构探索',
    '🏭 第五阶段：专业深化与工程落地': '🧭 阶段5-专业深化与工程落地',
}

# 只看这些容易误伤的通用词
CHECK = ['MLP', 'ViT', 'CLIP', 'LoRA', 'MAE', 'FPN', 'ResNet', 'VAE', 'AlexNet', 'SIFT']

def walk_md():
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fn in files:
            if fn.endswith('.md'):
                yield os.path.join(root, fn)

for old in CHECK:
    print(f'===== {old!r} 引用明细 =====')
    for fp in walk_md():
        rel = os.path.relpath(fp, VAULT).replace('\\', '/')
        try:
            with io.open(fp, encoding='utf-8-sig', errors='replace') as f:
                content = f.read()
        except Exception:
            continue
        pat = re.compile(r'\[\[([^\]\n#|]*?/)?' + re.escape(old) + r'(\|[^\]]*?)?\]\]')
        found = pat.findall(content)
        if found:
            tag = 'CV内' if rel.startswith(CV_PREFIX) else 'CV外'
            print(f'  [{tag}] {rel} x{len(found)}')
    print()
