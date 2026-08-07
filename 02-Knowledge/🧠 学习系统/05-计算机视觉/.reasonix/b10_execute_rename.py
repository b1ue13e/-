# -*- coding: utf-8 -*-
"""B10: G18 命名体系修复执行脚本（dry-run / apply 双模式）
- 重命名 28 个文件（git mv）
- 全库 .md 引用替换（wikilink，含表格 \\| 转义、路径前缀；跳过代码围栏）
"""
import os, re, io, sys, subprocess, json

MODE = sys.argv[1] if len(sys.argv) > 1 else 'dryrun'  # dryrun | apply
VAULT = r'F:\-'
CV_DIR = r'02-Knowledge\🧠 学习系统\05-计算机视觉'
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

def split_link_body(body):
    """解析 [[body]] 内部: [路径/]名字[|别名] 或 [路径/]名字[\|别名](表格转义)
    注意：先分离别名（避免别名含 / 被误判为路径），再处理路径前缀。"""
    # 先找分隔符：优先 \\|（表格转义），其次 |（普通别名）
    m = re.match(r'^(.*?)(\\\||\|)(.*)$', body)
    if m and m.group(1):
        name_part = m.group(1)
        alias = m.group(2) + m.group(3)
    else:
        name_part = body
        alias = ''
    # 再处理路径前缀
    prefix = ''
    name = name_part
    if '/' in name_part:
        prefix, name = name_part.rsplit('/', 1)
        prefix += '/'
    return prefix, name, alias

def replace_in_text(content):
    """替换文本中所有指向旧名的 wikilink；跳过代码围栏"""
    out_lines = []
    in_fence = False
    for line in content.split('\n'):
        if line.strip().startswith('```'):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue
        def repl(m):
            inner = m.group(0)[2:-2]  # 去掉 [[ ]]
            prefix, name, alias = split_link_body(inner)
            if name in RENAME:
                return '[[' + prefix + RENAME[name] + alias + ']]'
            return m.group(0)
        newline = re.sub(r'\[\[[^\[\]]+?\]\]', repl, line)
        out_lines.append(newline)
    return '\n'.join(out_lines)

def git_mv(old_path, new_path):
    rel_old = os.path.relpath(old_path, VAULT).replace('\\', '/')
    rel_new = os.path.relpath(new_path, VAULT).replace('\\', '/')
    r = subprocess.run(['git', 'mv', rel_old, rel_new], cwd=VAULT, capture_output=True, text=True)
    return r.returncode == 0, r.stderr.strip()

# ---- 1) 文件重命名 ----
print(f'==== 文件重命名 ({MODE}) ====')
renamed = 0
for root, dirs, files in os.walk(os.path.join(VAULT, CV_DIR)):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for fn in files:
        if not fn.endswith('.md'):
            continue
        base = fn[:-3]
        if base in RENAME:
            old_path = os.path.join(root, fn)
            new_path = os.path.join(root, RENAME[base] + '.md')
            if MODE == 'apply':
                ok, err = git_mv(old_path, new_path)
                if not ok:
                    print(f'  [FAIL] {base!r} -> {RENAME[base]!r}: {err}')
                    continue
            renamed += 1
            print(f'  [{"OK" if MODE=="apply" else "PLAN"}] {base!r} -> {RENAME[base]!r}')
print(f'共重命名 {renamed} 个文件')

# ---- 2) 全库引用替换 ----
print(f'\n==== 全库引用替换 ({MODE}) ====')
total_files_changed = 0
total_refs = 0
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for fn in files:
        if not fn.endswith('.md'):
            continue
        fp = os.path.join(root, fn)
        rel = os.path.relpath(fp, VAULT).replace('\\', '/')
        with io.open(fp, encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
        new_content = replace_in_text(content)
        if new_content != content:
            # 统计替换数
            old_cnt = 0
            for old in RENAME:
                old_cnt += len(re.findall(re.escape(old), content))
            total_files_changed += 1
            total_refs += old_cnt
            if MODE == 'apply':
                with io.open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            print(f'  [{MODE}] {rel} (~{old_cnt} 处)')
print(f'\n共修改 {total_files_changed} 个文件，约 {total_refs} 处引用')
