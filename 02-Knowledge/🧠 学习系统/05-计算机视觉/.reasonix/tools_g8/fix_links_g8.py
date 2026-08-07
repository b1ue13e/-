#!/usr/bin/env python3
"""G8 链接欠债修复脚本：05-计算机视觉 课程范围（v2）。

规则：
1. ESCAPE: \\| -> \| （表格转义规范，所有文件）
2. RELPATH: 相对课程路径前缀/../ 前缀 -> 完整仓库根路径
3. RENAME:  旧目标名 -> 新目标（完整仓库根路径），保留别名
4. UNLINK:  计划性概念 -> 去链接保留文字（别名优先）
5. MOC 表格中状态 ⬜ 且笔记列目标不可解析 -> 笔记列改为 `—`（纯文本）
6. 其余不可解析目标保持不变并计入遗留统计

用法: python fix_links_g8.py [--apply]   # 默认 dry-run
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

KB = "F:" + os.sep + "-"
COURSE = KB + os.sep + "02-Knowledge" + os.sep + "🧠 学习系统" + os.sep + "05-计算机视觉"
CV = "02-Knowledge/🧠 学习系统/05-计算机视觉"
SKIP = {'.归档', '.reasonix', '.recovery-hold', '.pytest_cache', '__pycache__', '.git', '.obsidian', '.tmp'}

WIKI = re.compile(r'\[\[([^\]]+)\]\]')

# 短名索引（活动文件）
SHORT = {}
def build_index():
    for root, dirs, files in os.walk(KB):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for f in files:
            if f.endswith('.md'):
                SHORT.setdefault(f[:-3], []).append(os.path.join(root, f))

def resolve(target):
    t = target.split('#')[0].split('|')[0].strip()
    if not t:
        return True
    if t.endswith('.md'):
        t = t[:-3]
    if '/' in t:
        return os.path.exists(os.path.join(KB, t + '.md'))
    return t in SHORT

def cv(path):
    return CV + "/" + path

RELPATH = {
    "00-前置知识/": cv("00-前置知识/"),
    "01-底层基石/": cv("01-底层基石/"),
    "02-深度学习内核/": cv("02-深度学习内核/"),
    "03-视觉核心任务/": cv("03-视觉核心任务/"),
    "04-前沿架构探索/": cv("04-前沿架构探索/"),
    "05-专业深化与工程落地/": cv("05-专业深化与工程落地/"),
}
DOTDOT = {
    "../🗺️ 计算机视觉学习路径": CV + "/🗺️ 计算机视觉学习路径",
    "../📚 教材挂载索引": CV + "/📚 教材挂载索引",
    "../00-前置知识/": cv("00-前置知识/"),
    "../01-底层基石/": cv("01-底层基石/"),
    "../02-深度学习内核/": cv("02-深度学习内核/"),
    "../03-视觉核心任务/": cv("03-视觉核心任务/"),
    "../04-前沿架构探索/": cv("04-前沿架构探索/"),
    "../05-专业深化与工程落地/": cv("05-专业深化与工程落地/"),
}

RENAME = {
    "01-底层基石/🏗️ 第一阶段：底层基石": cv("01-底层基石/🏗️ 第一阶段：底层基石"),
    "02-深度学习内核/🧠 第二阶段：深度学习内核": cv("02-深度学习内核/🧠 第二阶段：深度学习内核"),
    "03-视觉核心任务/🎯 第三阶段：视觉核心任务": cv("03-视觉核心任务/🎯 第三阶段：视觉核心任务"),
    "04-前沿架构探索/🚀 第四阶段：前沿架构探索": cv("04-前沿架构探索/🚀 第四阶段：前沿架构探索"),
    "05-专业深化与工程落地/🏭 第五阶段：专业深化与工程落地": cv("05-专业深化与工程落地/🏭 第五阶段：专业深化与工程落地"),
    "00-前置知识/🧭 阶段0-前置知识": cv("00-前置知识/🧭 阶段0-前置知识"),
    "相机标定与对极几何": cv("05-专业深化与工程落地/🎯 相机标定与对极几何 (Epipolar Geometry)"),
    "NeRF 神经辐射场": cv("05-专业深化与工程落地/🎯 NeRF 神经辐射场 (Neural Radiance Fields)"),
    "ResNet残差网络": cv("02-深度学习内核/🎯 ResNet (残差网络)"),
    "ResNet": cv("02-深度学习内核/🎯 ResNet (残差网络)"),
    "BatchNorm": cv("02-深度学习内核/批归一化BatchNorm"),
    "Dropout": cv("02-深度学习内核/数据增强与正则化"),
    "Softmax分类器": cv("02-深度学习内核/Softmax与SVM损失函数"),
    "线性分类器与Softmax损失": cv("02-深度学习内核/Softmax与SVM损失函数"),
    "Softmax 与交叉熵损失": cv("02-深度学习内核/Softmax与SVM损失函数"),
    "Softmax与交叉熵损失": cv("02-深度学习内核/Softmax与SVM损失函数"),
    "交叉熵损失": cv("02-深度学习内核/Softmax与SVM损失函数"),
    "多类支持向量机损失": cv("02-深度学习内核/Softmax与SVM损失函数"),
    "k最近邻(kNN)": cv("02-深度学习内核/kNN与线性分类器"),
    "kNN 与线性分类器": cv("02-深度学习内核/kNN与线性分类器"),
    "最优化与梯度下降": cv("02-深度学习内核/优化器SGD到Adam"),
    "优化器对比 (SGD vs Adam vs RMSprop)": cv("02-深度学习内核/优化器SGD到Adam"),
    "反向传播算法 (Backpropagation)": cv("02-深度学习内核/反向传播与计算图"),
    "🎯 反向传播算法 (Backpropagation)": cv("02-深度学习内核/反向传播与计算图"),
    "反向传播": cv("02-深度学习内核/反向传播与计算图"),
    "梯度计算": cv("02-深度学习内核/反向传播与计算图"),
    "链式法则": cv("02-深度学习内核/反向传播与计算图"),
    "LRScheduler": cv("02-深度学习内核/学习率调度策略"),
    "学习率调度与超参": cv("02-深度学习内核/学习率调度策略"),
    "权重正则化": cv("02-深度学习内核/数据增强与正则化"),
    "标签平滑": cv("02-深度学习内核/数据增强与正则化"),
    "数据增强与预处理": cv("02-深度学习内核/数据增强与正则化"),
    "迁移学习CV": cv("03-视觉核心任务/迁移学习与微调"),
    "迁移学习": cv("03-视觉核心任务/迁移学习与微调"),
    "微调策略": cv("03-视觉核心任务/迁移学习与微调"),
    "图像分类数据管线": cv("02-深度学习内核/图像分类任务与数据管线"),
    "CNN": cv("02-深度学习内核/卷积神经网络CNN"),
    "CNN/卷积神经网络": cv("02-深度学习内核/卷积神经网络CNN"),
    "VAE": cv("04-前沿架构探索/🎯 VAE 变分自编码器 (Variational Autoencoder)"),
    "VAE 变分自编码器": cv("04-前沿架构探索/🎯 VAE 变分自编码器 (Variational Autoencoder)"),
    "GAN": cv("04-前沿架构探索/生成模型GAN与Diffusion"),
    "Diffusion 扩散模型": cv("04-前沿架构探索/🎯 Diffusion 扩散模型 (DDPM)"),
    "CLIP": cv("04-前沿架构探索/自监督学习SimCLR与CLIP"),
    "SimCLR": cv("04-前沿架构探索/🎯 SimCLR 与对比学习 (Contrastive Learning)"),
    "GoogLeNet (Inception)": cv("02-深度学习内核/GoogLeNet"),
    "FocalLoss": cv("03-视觉核心任务/目标检测RCNN与YOLO"),
    "FasterRCNN": cv("03-视觉核心任务/目标检测RCNN与YOLO"),
    "FastRCNN": cv("03-视觉核心任务/目标检测RCNN与YOLO"),
    "RCNN": cv("03-视觉核心任务/目标检测RCNN与YOLO"),
    "YOLO目标检测": cv("03-视觉核心任务/目标检测RCNN与YOLO"),
    "SSD": cv("03-视觉核心任务/目标检测RCNN与YOLO"),
    "RetinaNet": cv("03-视觉核心任务/目标检测RCNN与YOLO"),
    "FCOS": cv("03-视觉核心任务/目标检测RCNN与YOLO"),
    "DETR": cv("03-视觉核心任务/目标检测RCNN与YOLO"),
    "MaskRCNN": cv("03-视觉核心任务/目标检测RCNN与YOLO"),
    "FCN": cv("03-视觉核心任务/语义分割与UNet"),
    "DeepLab": cv("03-视觉核心任务/语义分割与UNet"),
    "MaskRCNN分割": cv("03-视觉核心任务/语义分割与UNet"),
    "全景分割定义": cv("03-视觉核心任务/语义分割与UNet"),
    "DiceLoss": cv("03-视觉核心任务/语义分割与UNet"),
    "UNet": cv("03-视觉核心任务/语义分割与UNet"),
    "位置编码": cv("04-前沿架构探索/Transformer与自注意力"),
    "SelfAttention": cv("04-前沿架构探索/Transformer与自注意力"),
    "MultiHeadAttention": cv("04-前沿架构探索/Transformer与自注意力"),
    "残差连接": cv("04-前沿架构探索/Transformer与自注意力"),
    "LayerNorm": cv("02-深度学习内核/批归一化BatchNorm"),
    "InstanceNorm": cv("02-深度学习内核/批归一化BatchNorm"),
    "GroupNorm": cv("02-深度学习内核/批归一化BatchNorm"),
    "激活函数CV": cv("02-深度学习内核/激活函数详解"),
    "凸优化基础": cv("01-底层基石/凸优化CV"),
    "批归一化 BatchNorm": cv("02-深度学习内核/批归一化BatchNorm"),
    "02-Knowledge/🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型/Transformer注意力": "02-Knowledge/🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型/08-NLP全栈-Transformer架构",
    "02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/反向传播算法": "02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/机器学习-反向传播算法",
    "14-概率图模型/变分推断": "02-Knowledge/🧠 学习系统/14-概率图模型/🎯 变分推断 (Variational Inference & ELBO)",
    "15-控制与机器人学/SLAM": "02-Knowledge/🧠 学习系统/15-控制与机器人学/10-状态估计/SLAM基础",
    "09-高等代数/01-基础/齐次坐标与投影变换": "02-Knowledge/🧠 学习系统/15-控制与机器人学/02-机器人学基础模型/齐次坐标",
    "09-高等代数/01-基础/叉积与反对称矩阵": "02-Knowledge/🧠 学习系统/15-控制与机器人学/02-机器人学基础模型/齐次变换矩阵",
    "24-随机过程/01-基础/马尔可夫链": "02-Knowledge/🧠 学习系统/24-随机过程/02-马尔可夫与泊松过程/马尔可夫与泊松过程-应用入口-1",
    "05-计算机视觉/01-经典视觉/边缘与特征检测": cv("01-底层基石/边缘检测"),
    "05-计算机视觉/02-深度学习内核/SimCLR与对比学习": cv("04-前沿架构探索/🎯 SimCLR 与对比学习 (Contrastive Learning)"),
    "05-计算机视觉/02-深度学习内核/Diffusion 扩散模型": cv("04-前沿架构探索/🎯 Diffusion 扩散模型 (DDPM)"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/ResNet": cv("02-深度学习内核/🎯 ResNet (残差网络)"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/ResNet残差网络": cv("02-深度学习内核/🎯 ResNet (残差网络)"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/BatchNorm": cv("02-深度学习内核/批归一化BatchNorm"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/Dropout": cv("02-深度学习内核/数据增强与正则化"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/LRScheduler": cv("02-深度学习内核/学习率调度策略"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/权重正则化": cv("02-深度学习内核/数据增强与正则化"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/梯度计算": cv("02-深度学习内核/反向传播与计算图"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/交叉熵损失": cv("02-深度学习内核/Softmax与SVM损失函数"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/LayerNorm": cv("02-深度学习内核/批归一化BatchNorm"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/InstanceNorm": cv("02-深度学习内核/批归一化BatchNorm"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/GroupNorm": cv("02-深度学习内核/批归一化BatchNorm"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/CLIP": cv("04-前沿架构探索/自监督学习SimCLR与CLIP"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/GAN": cv("04-前沿架构探索/生成模型GAN与Diffusion"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/MoCo": cv("04-前沿架构探索/自监督学习SimCLR与CLIP"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/03-视觉核心任务/度量学习": cv("03-视觉核心任务/迁移学习与微调"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/05-专业深化与工程落地/目标跟踪": cv("05-专业深化与工程落地/🎯 相机标定与对极几何 (Epipolar Geometry)"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/NumPy矩阵CV": cv("01-底层基石/线性代数基础CV"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/HOG": cv("01-底层基石/SIFT"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/采样量化": cv("01-底层基石/图像表示"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/频域滤波": cv("01-底层基石/傅里叶变换CV"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/形态学": cv("01-底层基石/图像滤波"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/直方图处理": cv("01-底层基石/图像滤波"),
    "05-计算机视觉/02-深度学习内核/3DGS": cv("05-专业深化与工程落地/🎯 NeRF 神经辐射场 (Neural Radiance Fields)"),
    "05-计算机视觉/02-深度学习内核/单应性矩阵": cv("05-专业深化与工程落地/🎯 相机标定与对极几何 (Epipolar Geometry)"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/参数量计算": cv("02-深度学习内核/卷积神经网络CNN"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/ConvNeXt": cv("02-深度学习内核/卷积神经网络CNN"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/CSPNet": cv("02-深度学习内核/DenseNet"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/EfficientNet": cv("02-深度学习内核/DenseNet"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/MobileNet": cv("02-深度学习内核/DenseNet"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/GoogLeNet/Inception": cv("02-深度学习内核/GoogLeNet"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/.归档/空壳文件/GoogLeNet": cv("02-深度学习内核/GoogLeNet"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/混合精度": cv("02-深度学习内核/优化器SGD到Adam"),
    "17-机器学习/03-正则优化/VAE 变分自编码器": cv("04-前沿架构探索/🎯 VAE 变分自编码器 (Variational Autoencoder)"),
    "🎓 HW01 - CIFAR-10 kNN 与 Softmax 基线正式作业说明书": "03-Projects/05-计算机视觉/课后作业/05-计算机视觉-课后作业-01-kNN与Softmax线性分类",
    # 上一轮 RELPATH 抢占产生的坏目标（完整路径形式）反向修复
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/机器学习-反向传播算法": "02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/机器学习-反向传播算法",
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-Knowledge/🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型/08-NLP全栈-Transformer架构": "02-Knowledge/🧠 学习系统/08-NLP全栈/04-Transformer与预训练模型/08-NLP全栈-Transformer架构",
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/LatentDiffusion": cv("04-前沿架构探索/🎯 Diffusion 扩散模型 (DDPM)"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/Diffusion 扩散模型": cv("04-前沿架构探索/🎯 Diffusion 扩散模型 (DDPM)"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/SimCLR与对比学习": cv("04-前沿架构探索/🎯 SimCLR 与对比学习 (Contrastive Learning)"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/3DGS": cv("05-专业深化与工程落地/🎯 NeRF 神经辐射场 (Neural Radiance Fields)"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/单应性矩阵": cv("05-专业深化与工程落地/🎯 相机标定与对极几何 (Epipolar Geometry)"),
    "02-Knowledge/🧠 学习系统/05-计算机视觉/01-经典视觉/边缘与特征检测": cv("01-底层基石/边缘检测"),
    # 书库（实际为书籍笔记 .md，无 PDF）
    "02-Knowledge/📚 书库/书籍资源/Mathematics for Machine Learning (Marc Peter Deisenroth, A. Aldo Faisal etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf": "02-Knowledge/📚 书库/书籍笔记/Mathematics for Machine Learning",
    "02-Knowledge/📚 书库/书籍资源/Hands-on Machine Learning with Scikit-Learn, Keras, and TensorFlow (Aurélien Géron) (z-library.sk, 1lib.sk, z-lib.sk).pdf": "02-Knowledge/📚 书库/书籍笔记/Hands-on Machine Learning",
    # 马尔可夫链 -> 24-随机过程 阶段入口
    "马尔可夫链": "02-Knowledge/🧠 学习系统/24-随机过程/02-马尔可夫与泊松过程/马尔可夫与泊松过程-应用入口-1",
    # NLP 全栈学习路径实际文件名
    "02-Knowledge/🧠 学习系统/08-NLP全栈/🗺️ NLP全栈学习路径": "02-Knowledge/🧠 学习系统/08-NLP全栈/🗺️ 08-NLP全栈学习路径",
}

UNLINK = {
    "ORB", "SURF", "HOG", "LBP", "图像匹配", "三维重建与SfM", "视觉SLAM",
    "频域滤波", "小波变换CV", "采样量化", "直方图处理", "颜色模型", "图像质量",
    "OpenCV读写", "NumPy基础", "NumPy数组CV", "NumPy矩阵CV", "向量化CV", "线性变换CV",
    "形态学", "几何增强", "颜色增强", "Mixup", "CutMix", "AutoAugment", "DropConnect",
    "MSE损失", "注意力可视化", "矩阵乘法与广播", "训练循环", "Python基础",
    "PyTorch Dataset与DataLoader", "数据管线", "损失函数基础", "信息论基础",
    "正则化技术", "贝叶斯深度学习", "生成模型VAE", "扩散模型DDPM", "梯度下降与优化基础",
    "高中数学", "微积分基础", "知识蒸馏", "细粒度分类", "难例挖掘",
    "StyleGAN", "CycleGAN", "ControlNet", "StableDiffusion", "MoCo", "BYOL",
    "BLIP", "LLaVA", "ALIGN", "DeiT", "PVT", "CNNTransformer混合", "ConvNeXt",
    "CoAtNet", "SimSiam", "BEiT", "iBOT", "自监督预训练", "自监督特征",
    "Diffusion", "TextualInversion", "3DGS", "LatentDiffusion", "单应性矩阵",
    "光流估计", "动作识别", "视频分割", "立体视觉", "点云处理", "NeRF",
    "GaussianSplatting", "TensorRT", "ONNXRuntime", "OpenVINO", "移动端推理",
    "部署蒸馏", "部署NAS", "模型服务", "模型版本", "模型监控", "ABA测试",
    "BEV感知", "多传感器融合", "车道线检测", "Occupancy", "病灶检测", "器官分割",
    "病理分析", "联邦学习医疗", "缺陷检测", "工业OCR", "视觉测量",
    "MLECV", "EM算法CV", "拉格朗日CV", "牛顿法CV", "广播机制CV", "颜色空间",
    "OpenCV绘图", "项目-Panorama", "项目-HDR", "项目-图像搜索", "LeNet",
    "MobileNet", "ShuffleNet", "EfficientNet", "GhostNet", "参数量计算",
    "多尺度特征", "通道注意力", "PyTorchDataset", "DataLoader", "PyTorchModule",
    "PyTorchOptimizer", "自定义算子", "DDP", "混合精度", "模型保存", "TensorBoard",
    "PyTorch项目结构", "配置管理", "实验跟踪", "模型版本管理", "项目-CIFAR10",
    "项目-CNN可视化", "项目-风格迁移", "分类经典网络", "长尾分布", "YOLOv3",
    "YOLOv8", "CenterNet", "多尺度检测", "PSPNet", "YOLACT", "SOLO",
    "PanopticFPN", "OpenPose", "HRNet", "SimpleBaseline", "单目3D姿态", "多视角姿态",
    "项目-自定义检测", "项目-医学分割", "项目-姿态估计",
    "牛顿法与二阶优化",
}


def parse_link(raw):
    """返回 (target, alias, sep)。sep 为 '\\\\|' / '\\|' / '|' / None。"""
    if '\\\\|' in raw:
        target, _, alias = raw.partition('\\\\|')
        return target.strip(), alias, '\\\\|'
    if '\\|' in raw:
        target, _, alias = raw.partition('\\|')
        return target.strip(), alias, '\\|'
    if '|' in raw:
        target, _, alias = raw.partition('|')
        return target.strip(), alias, '|'
    return raw.strip(), None, None


def main():
    apply = '--apply' in sys.argv
    build_index()
    total_changes = 0
    unlink_count = 0
    leftover = {}   # target -> 次数（未处理死链）
    table_fixed = 0
    for p in sorted(walk_md(COURSE)):
        rel = os.path.relpath(p, COURSE)
        with open(p, encoding='utf-8') as f:
            lines = f.readlines()
        changed = []
        in_fence = False
        for i, line in enumerate(lines):
            # 代码围栏跳过（避免代码中的 [[x]] 被误判为 wikilink）
            if re.match(r'^\s*(```|~~~)', line):
                in_fence = not in_fence
                new_line = line
                if new_line != lines[i]:
                    changed.append((i + 1, lines[i].rstrip('\n'), new_line.rstrip('\n')))
                continue
            new_line = line
            if in_fence:
                continue
            # 5. MOC 表格中 ⬜ 行：笔记列不可解析 -> 纯文本
            is_moc = any(k in rel for k in ('阶段', 'MOC', '路径', '挂载'))
            in_table = line.lstrip().startswith('|')
            if in_table and '⬜' in line:
                for m in WIKI.finditer(line):
                    raw = m.group(1)
                    target, alias, _ = parse_link(raw)
                    t_clean = target.split('#')[0].removesuffix('.md')
                    if not resolve(t_clean):
                        cell = m.group(0)
                        new_line = new_line.replace(cell, '—')
                        table_fixed += 1
            for m in WIKI.finditer(new_line):
                raw = m.group(1)
                target, alias, sep = parse_link(raw)
                t_clean = target.split('#')[0].strip().removesuffix('.md')
                if resolve(t_clean):
                    # 已解析：分隔符规范化（\\| 或 \| 归一为 |；表格内保留 \|）
                    if sep == '\\\\|' or sep == '\\|':
                        sep2 = '\\|' if in_table else '|'
                        new_line = new_line.replace('[[' + raw + ']]',
                                                    '[[' + target + sep2 + alias + ']]')
                        total_changes += 1
                    continue
                # 相对路径规范化
                new_target = None
                if t_clean.startswith('../'):
                    for pref, full in DOTDOT.items():
                        if t_clean == pref.rstrip('/'):
                            new_target = full
                            break
                        if t_clean.startswith(pref):
                            new_target = full + t_clean[len(pref):]
                            break
                if new_target is None:
                    for pref, full in RELPATH.items():
                        if t_clean.startswith(pref):
                            new_target = full + t_clean[len(pref):]
                            break
                if new_target is None and t_clean in RENAME:
                    new_target = RENAME[t_clean]
                if new_target is None and t_clean in UNLINK:
                    # 去链接：保留文字
                    text = alias if alias is not None else t_clean.split('#')[0]
                    new_line = new_line.replace('[[' + raw + ']]', text)
                    unlink_count += 1
                    continue
                if new_target is None:
                    leftover[t_clean] = leftover.get(t_clean, 0) + 1
                    continue
                # 组装：表格内保留 \|，表格外用 |
                sep2 = '\\|' if in_table else '|'
                body = new_target + ('#' + target.split('#')[1] if '#' in target else '')
                if alias is not None:
                    body += sep2 + alias
                new_line = new_line.replace('[[' + raw + ']]', '[[' + body + ']]')
                total_changes += 1
            if new_line != line:
                changed.append((i + 1, line.rstrip('\n'), new_line.rstrip('\n')))
                lines[i] = new_line
        if changed:
            print(f"\n=== {rel} ({len(changed)} 行)")
            for ln, old, new in changed:
                print(f"  L{ln}  {old.strip()[:100]}")
                print(f"     -> {new.strip()[:100]}")
        if apply:
            with open(p, 'w', encoding='utf-8') as f:
                f.writelines(lines)
    print(f"\n[{'APPLIED' if apply else 'DRY-RUN'}] 替换 {total_changes} 处，去链接 {unlink_count} 处，表格规划行 {table_fixed} 处")
    if leftover:
        print(f"\n!! 遗留未处理死链目标 {len(leftover)} 个:")
        for t, c in sorted(leftover.items(), key=lambda x: -x[1]):
            print(f"   {c:3d}  {t}")


def walk_md(base):
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for f in files:
            if f.endswith('.md'):
                yield os.path.join(root, f)


if __name__ == '__main__':
    main()
