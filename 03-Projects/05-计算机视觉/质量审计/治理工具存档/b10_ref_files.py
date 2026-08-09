# -*- coding: utf-8 -*-
"""B10: 列出全部引用文件分类清单（CV内/CV外），用于替换策略"""
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

ext_files = set()  # CV外的引用文件
cv_files = set()
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for fn in files:
        if not fn.endswith('.md'):
            continue
        fp = os.path.join(root, fn)
        rel = os.path.relpath(fp, VAULT).replace('\\', '/')
        try:
            with io.open(fp, encoding='utf-8-sig', errors='replace') as f:
                content = f.read()
        except Exception:
            continue
        for old in RENAME:
            pat = re.compile(r'\[\[([^\]\n#|]*?/)?' + re.escape(old) + r'(\|[^\]]*?)?\]\]')
            if pat.search(content):
                if rel.startswith(CV_PREFIX):
                    cv_files.add(rel)
                else:
                    ext_files.add(rel)
                break

print(f'=== CV内引用文件 ({len(cv_files)}) ===')
for f in sorted(cv_files):
    print(f'  {f}')
print(f'\n=== CV外引用文件 ({len(ext_files)}) ===')
for f in sorted(ext_files):
    print(f'  {f}')
