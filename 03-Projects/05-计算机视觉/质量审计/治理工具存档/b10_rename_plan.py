# -*- coding: utf-8 -*-
"""B10: G18 命名体系修复 —— 规划重命名映射 + 全库引用扫描（只读 dry-run）"""
import os, re, io, json, collections

VAULT = r'F:\-'
COURSE = r'02-Knowledge\🧠 学习系统\05-计算机视觉'
PROJ = r'03-Projects\05-计算机视觉'
EXCLUDE_DIRS = {'.workbuddy', '.归档', '.reasonix', '.recovery-hold', '.git', 'node_modules', '__pycache__', '.pytest_cache', '.tmp', '.obsidian'}

# 重命名映射：旧文件名(不含.md) -> 新文件名
RENAME = {
    # ---- 17 个纯英文缩写卡 -> 加"计算机视觉-"前缀 ----
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
    # ---- 6 个括号文件名 -> 规范化 ----
    '🎯 ResNet (残差网络)': '计算机视觉-ResNet',
    '🎯 Diffusion 扩散模型 (DDPM)': '计算机视觉-Diffusion扩散模型',
    '🎯 SimCLR 与对比学习 (Contrastive Learning)': '计算机视觉-SimCLR与对比学习',
    '🎯 VAE 变分自编码器 (Variational Autoencoder)': '计算机视觉-VAE变分自编码器',
    '🎯 NeRF 神经辐射场 (Neural Radiance Fields)': '计算机视觉-NeRF神经辐射场',
    '🎯 相机标定与对极几何 (Epipolar Geometry)': '计算机视觉-相机标定与对极几何',
    # ---- 5 个阶段 MOC -> 统一 "🧭 阶段N-阶段名" ----
    '🏗️ 第一阶段：底层基石': '🧭 阶段1-底层基石',
    '🧠 第二阶段：深度学习内核': '🧭 阶段2-深度学习内核',
    '🎯 第三阶段：视觉核心任务': '🧭 阶段3-视觉核心任务',
    '🚀 第四阶段：前沿架构探索': '🧭 阶段4-前沿架构探索',
    '🏭 第五阶段：专业深化与工程落地': '🧭 阶段5-专业深化与工程落地',
}

def walk_md():
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fn in files:
            if fn.endswith('.md'):
                yield os.path.join(root, fn)

# 1) 收集全库所有 .md 中出现的旧名引用（wikilink 形式 [[旧名]] 或 [[路径/旧名|别名]]）
refs = collections.defaultdict(list)  # old_name -> [(file, count)]
files_with_name = {}  # 旧名 -> 实际文件路径

for fp in walk_md():
    rel = os.path.relpath(fp, VAULT).replace('\\', '/')
    base = os.path.splitext(os.path.basename(fp))[0]
    if base in RENAME:
        files_with_name[base] = rel
    try:
        with io.open(fp, encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print('读取失败:', fp, e); continue
    for old in RENAME:
        # wikilink 引用：[[old]]、[[old|alias]]、[[path/old|alias]]、[[path/old]]
        # 注意避免匹配 old 作为其他名字的子串（用边界）
        pat = re.compile(r'\[\[([^\]\n#|]*?/)?' + re.escape(old) + r'(\|[^\]]*?)?\]\]')
        found = pat.findall(content)
        if found:
            refs[old].append((rel, len(found)))

print('==== 旧名 -> 新名 映射 ====')
for old, new in RENAME.items():
    print(f'  {old!r} -> {new!r}')

print()
print('==== 全库引用分布（每个旧名的引用文件数与总数） ====')
total_refs = 0
for old, new in RENAME.items():
    n_files = len(refs[old])
    n_total = sum(c for _, c in refs[old])
    total_refs += n_total
    print(f'  {old!r}: {n_total} 处引用 / {n_files} 个文件')

print(f'\n全库引用总数: {total_refs}')

print()
print('==== 文件位置核对 ====')
for old in RENAME:
    if old in files_with_name:
        print(f'  OK  {old!r} -> {files_with_name[old]}')
    else:
        print(f'  MISSING! {old!r} 未找到实际文件')

# 2) 检查是否有文件本身存在但不在 RENAME（防止漏掉）
print()
print('==== 课程目录内全部文件（含扩展名） ====')
course_root = os.path.join(VAULT, COURSE)
for root, dirs, files in os.walk(course_root):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for fn in files:
        rel = os.path.relpath(os.path.join(root, fn), VAULT).replace('\\', '/')
        print(f'  {rel}')
