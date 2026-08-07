"""为 42 张无 upstream 的 study 卡补全 upstream（直接前置，完整路径 wikilink）。

规则（AGENTS.md §3）：
- 正文 §3 有明确前置且可映射到已建卡 -> 填 upstream
- 真正起点（无课程内直接前置，如基础数学/图像表示）-> 保持省略
- 只填直接前置（不多级），可解析
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

KB = "F:" + os.sep + "-"
CV = "02-Knowledge/🧠 学习系统/05-计算机视觉"
def cv(path): return CV + "/" + path

# 卡短名 -> upstream 数组（完整路径 wikilink）
# 依据：各卡正文 §3 前置声明（上一轮扫描结果）
UPSTREAM_MAP = {
    # ---- 01-底层基石 ----
    "SIFT": [cv("01-底层基石/图像滤波"), cv("01-底层基石/图像表示"), cv("01-底层基石/边缘检测")],
    "傅里叶变换CV": [cv("01-底层基石/图像表示"), cv("01-底层基石/线性代数基础CV"), cv("01-底层基石/图像滤波")],
    "几何变换CV": [cv("01-底层基石/线性代数基础CV"), cv("01-底层基石/图像表示")],
    "图像滤波": [cv("01-底层基石/图像表示"), cv("01-底层基石/线性代数基础CV"), cv("01-底层基石/傅里叶变换CV")],
    "边缘检测": [cv("01-底层基石/图像滤波"), cv("01-底层基石/图像表示")],
    # 起点卡（无课程内直接前置，保持省略）：线性代数基础CV / 图像表示 / 梯度下降CV / 概率分布CV
    # 已有 upstream（不重复补）：凸优化CV / 特征分解CV / SVDCV / 贝叶斯CV / MLP / 前向传播 / 计算图 / 梯度流问题 / FPN / ViT / SwinTransformer / MAE / 模型剪枝
    # ---- 02-深度学习内核 ----
    "感知机": [cv("02-深度学习内核/前向传播")],
    "激活函数详解": [cv("02-深度学习内核/感知机"), cv("02-深度学习内核/前向传播")],
    "反向传播与计算图": [cv("02-深度学习内核/前向传播"), cv("02-深度学习内核/计算图")],
    "kNN与线性分类器": [cv("02-深度学习内核/前向传播"), cv("01-底层基石/线性代数基础CV")],
    "Softmax与SVM损失函数": [cv("02-深度学习内核/kNN与线性分类器"), cv("02-深度学习内核/前向传播"), cv("02-深度学习内核/反向传播与计算图")],
    "优化器SGD到Adam": [cv("01-底层基石/梯度下降CV"), cv("02-深度学习内核/反向传播与计算图")],
    "学习率调度策略": [cv("02-深度学习内核/优化器SGD到Adam"), cv("01-底层基石/梯度下降CV")],
    "卷积神经网络CNN": [cv("01-底层基石/图像滤波"), cv("02-深度学习内核/感知机"), cv("02-深度学习内核/前向传播")],
    "感受野": [cv("02-深度学习内核/卷积神经网络CNN")],
    "AlexNet": [cv("02-深度学习内核/卷积神经网络CNN"), cv("02-深度学习内核/激活函数详解")],
    "VGGNet": [cv("02-深度学习内核/卷积神经网络CNN"), cv("02-深度学习内核/AlexNet")],
    "GoogLeNet": [cv("02-深度学习内核/卷积神经网络CNN"), cv("02-深度学习内核/VGGNet"), cv("02-深度学习内核/AlexNet")],
    "🎯 ResNet (残差网络)": [cv("02-深度学习内核/VGGNet"), cv("02-深度学习内核/梯度流问题")],
    "DenseNet": [cv("02-深度学习内核/🎯 ResNet (残差网络)"), cv("02-深度学习内核/卷积神经网络CNN")],
    "批归一化BatchNorm": [cv("02-深度学习内核/前向传播"), cv("02-深度学习内核/反向传播与计算图")],
    "权重初始化策略": [cv("02-深度学习内核/反向传播与计算图"), cv("02-深度学习内核/激活函数详解")],
    "数据增强与正则化": [cv("02-深度学习内核/卷积神经网络CNN"), cv("02-深度学习内核/反向传播与计算图")],
    "图像分类任务与数据管线": [cv("02-深度学习内核/感知机"), cv("02-深度学习内核/kNN与线性分类器")],
    # ---- 03-视觉核心任务 ----
    "IoU与NMS": [cv("03-视觉核心任务/目标检测RCNN与YOLO")],
    "目标检测RCNN与YOLO": [cv("02-深度学习内核/卷积神经网络CNN"), cv("02-深度学习内核/Softmax与SVM损失函数")],
    "语义分割与UNet": [cv("02-深度学习内核/卷积神经网络CNN"), cv("03-视觉核心任务/目标检测RCNN与YOLO")],
    "迁移学习与微调": [cv("02-深度学习内核/卷积神经网络CNN"), cv("02-深度学习内核/Softmax与SVM损失函数"), cv("02-深度学习内核/优化器SGD到Adam")],
    # ---- 04-前沿架构探索 ----
    "Transformer与自注意力": [cv("02-深度学习内核/Softmax与SVM损失函数"), cv("02-深度学习内核/批归一化BatchNorm")],
    "可解释性Saliency与CAM": [cv("02-深度学习内核/卷积神经网络CNN"), cv("02-深度学习内核/反向传播与计算图"), cv("02-深度学习内核/Softmax与SVM损失函数")],
    "生成模型GAN与Diffusion": [cv("02-深度学习内核/卷积神经网络CNN"), cv("02-深度学习内核/反向传播与计算图"), cv("02-深度学习内核/Softmax与SVM损失函数")],
    "🎯 VAE 变分自编码器 (Variational Autoencoder)": [cv("02-深度学习内核/反向传播与计算图"), "02-Knowledge/🧠 学习系统/14-概率图模型/🎯 变分推断 (Variational Inference & ELBO)"],
    "🎯 Diffusion 扩散模型 (DDPM)": [cv("04-前沿架构探索/🎯 VAE 变分自编码器 (Variational Autoencoder)"), cv("04-前沿架构探索/生成模型GAN与Diffusion")],
    "🎯 SimCLR 与对比学习 (Contrastive Learning)": [cv("02-深度学习内核/🎯 ResNet (残差网络)"), cv("02-深度学习内核/Softmax与SVM损失函数")],
    "自监督学习SimCLR与CLIP": [cv("02-深度学习内核/卷积神经网络CNN"), cv("02-深度学习内核/🎯 ResNet (残差网络)")],
    "LoRA": [cv("04-前沿架构探索/Transformer与自注意力"), cv("03-视觉核心任务/迁移学习与微调")],
    # ---- 05-专业深化与工程落地 ----
    "模型量化": [cv("02-深度学习内核/卷积神经网络CNN"), cv("02-深度学习内核/优化器SGD到Adam")],
    "🎯 NeRF 神经辐射场 (Neural Radiance Fields)": [cv("05-专业深化与工程落地/🎯 相机标定与对极几何 (Epipolar Geometry)"), cv("02-深度学习内核/MLP")],
    "🎯 相机标定与对极几何 (Epipolar Geometry)": [cv("01-底层基石/线性代数基础CV"), cv("01-底层基石/几何变换CV")],
}

def main():
    COURSE_DIR = KB + os.sep + "02-Knowledge" + os.sep + "🧠 学习系统" + os.sep + "05-计算机视觉"
    SKIP = {'.归档', '.reasonix', '.recovery-hold', '.pytest_cache', '__pycache__', '.git', '.obsidian', '.tmp'}
    # 建立短名 -> 文件路径索引（验证目标存在）
    short = {}
    for root, dirs, files in os.walk(KB):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for f in files:
            if f.endswith('.md'):
                short.setdefault(f[:-3], []).append(os.path.join(root, f))
    applied = skipped = 0
    for root, dirs, files in os.walk(COURSE_DIR):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for f in files:
            if not f.endswith('.md'):
                continue
            p = os.path.join(root, f)
            name = f[:-3]
            if name not in UPSTREAM_MAP:
                continue
            with open(p, encoding='utf-8') as fh:
                content = fh.read()
            if 'type: study' not in content:
                continue
            if re.search(r'upstream:\s*\[', content):
                # 已有 upstream：若为裸路径则补 [[ ]] 包裹（幂等修复）
                fixed = re.sub(
                    r'upstream:\s*\[(.*?)\]',
                    lambda m: 'upstream: [' + ', '.join(
                        f'"[[{t.strip().strip(chr(34))}]]"' if not t.strip().startswith('[[') else t.strip()
                        for t in m.group(1).split(',')
                    ) + ']',
                    content,
                    count=1,
                    flags=re.S,
                )
                if fixed != content:
                    with open(p, 'w', encoding='utf-8') as fh:
                        fh.write(fixed)
                    print(f"[修正包裹] {name}")
                skipped += 1
                continue
            ups = UPSTREAM_MAP[name]
            # 验证目标存在
            missing = []
            for u in ups:
                t = u.split('/')[-1]
                if t not in short:
                    missing.append(u)
            if missing:
                print(f"[目标缺失] {name}: {missing}")
                continue
            # 在 prerequisites 后插入 upstream（或 stage_moc 前）
            lines = content.split('\n')
            idx = None
            for i, l in enumerate(lines[:30]):
                if re.match(r'^(prerequisites|related|stage_moc|difficulty|concept|created):', l):
                    if l.startswith('stage_moc'):
                        idx = i
                        break
            if idx is None:
                print(f"[插入点未找到] {name}")
                continue
            up_line = 'upstream: [' + ', '.join(f'"[[{u}]]"' for u in ups) + ']'
            lines.insert(idx, up_line)
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write('\n'.join(lines))
            applied += 1
            print(f"[已补] {name}: {len(ups)} 个 upstream")
    print(f"\n补全 {applied} 张，跳过（已有）{skipped} 张")

if __name__ == '__main__':
    main()
