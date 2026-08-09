# -*- coding: utf-8 -*-
"""B10 前置检查：跨课程同名冲突 + 新名唯一性"""
import os, collections

VAULT = r'F:\-'
EXCLUDE_DIRS = {'.workbuddy', '.归档', '.reasonix', '.recovery-hold', '.git', 'node_modules', '__pycache__', '.pytest_cache', '.tmp', '.obsidian'}

names = collections.defaultdict(list)
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for fn in files:
        if fn.endswith('.md'):
            base = os.path.splitext(fn)[0]
            rel = os.path.relpath(os.path.join(root, fn), VAULT).replace('\\', '/')
            names[base].append(rel)

targets = ['SIFT', 'SVDCV', 'AlexNet', 'DenseNet', 'GoogLeNet', 'MLP', 'VGGNet', 'DETR', 'FPN',
           'CLIP', 'DeiT', 'LoRA', 'MAE', 'SwinTransformer', 'ViT', 'TensorRT',
           'ResNet', 'Diffusion', 'SimCLR', 'VAE', 'NeRF', '相机标定']

print('=== 旧名在全库的同名冲突检查（含子串匹配，保守） ===')
hit = 0
for t in targets:
    for base, files in names.items():
        if base == t or base.startswith(t) or t in base:
            others = [f for f in files if not f.startswith('02-Knowledge/🧠 学习系统/05-计算机视觉')]
            if others:
                hit += 1
                print(f'  冲突候选 base={base!r} (目标词 {t!r}):')
                for f in files:
                    mark = ' [CV课程]' if f.startswith('02-Knowledge/🧠 学习系统/05-计算机视觉') else ' [其他课程]'
                    print(f'      {f}{mark}')
if hit == 0:
    print('  无冲突')

print()
print('=== 新名唯一性检查 ===')
new_names = ['计算机视觉-SIFT', '计算机视觉-SVD分解', '计算机视觉-AlexNet', '计算机视觉-DenseNet',
             '计算机视觉-GoogLeNet', '计算机视觉-MLP', '计算机视觉-VGGNet', '计算机视觉-DETR',
             '计算机视觉-FPN', '计算机视觉-CLIP', '计算机视觉-DeiT', '计算机视觉-LoRA',
             '计算机视觉-MAE', '计算机视觉-SwinTransformer', '计算机视觉-ViT', '计算机视觉-TensorRT',
             '计算机视觉-ResNet', '计算机视觉-Diffusion扩散模型', '计算机视觉-SimCLR与对比学习',
             '计算机视觉-VAE变分自编码器', '计算机视觉-NeRF神经辐射场', '计算机视觉-相机标定与对极几何',
             '🧭 阶段1-底层基石', '🧭 阶段2-深度学习内核', '🧭 阶段3-视觉核心任务',
             '🧭 阶段4-前沿架构探索', '🧭 阶段5-专业深化与工程落地']
for n in new_names:
    if n in names:
        print(f'  新名 {n!r} 已存在! {names[n]}')
    else:
        print(f'  OK {n!r} 唯一')

print()
print('=== CV课程内现有 计算机视觉- 前缀卡（避免重复） ===')
for base, files in names.items():
    if base.startswith('计算机视觉-'):
        for f in files:
            print(f'  {f}')
