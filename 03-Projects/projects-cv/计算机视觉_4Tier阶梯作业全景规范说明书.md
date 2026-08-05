---
title: "计算机视觉 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "计算机视觉 4-Tier 阶梯作业规范"
course: "计算机视觉"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [计算机视觉, 4Tier作业, 阶梯作业, 编程实战, PyTest, CS231n]
---

# 👁️ 计算机视觉 4-Tier 阶梯作业全景规范说明书 (Stanford CS231n & D2L 范式)

> 本说明书为 **05-计算机视觉** 路径（基于 Stanford CS231n 与 D2L Vision）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ torchvision / OpenCV 调包 / kNN 与线性分类器 / 评估指标计算
🟡 L2 - Medium Baseline   │ 数据增强 (Mixup/CutMix) / Cosine 学习率 / 特征图可视化
🔴 L3 - Strong Baseline   │ [核心] 不调用高级深度学习库，从零手撕 Conv2d / MaxPool / Softmax / Self-Attention 算子
👑 L4 - Boss Baseline     │ 边缘部署 (TensorRT / ONNX) / 扩散模型 (DDPM) / 视觉大模型 (CLIP / SAM)
```

---

## 🎯 计算机视觉阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 图像分类与线性分类器 (kNN, Linear SVM, Softmax)
- **开源溯源**：Stanford CS231n Assignment 1
- 🟢 **L1**: 在 CIFAR-10 数据集上运行 kNN 算法与 Linear SVM。
- 🟡 **L2**: 计算 L1 / L2 距离矩阵并可视化 nearest neighbors 图像。
- 🔴 **L3 (手撕核心)**：**从零手撕 Softmax 分类器损失函数与梯度推导 (仅使用 NumPy)**：
  $$ L_i = -\log\left(\frac{e^{f_{y_i}}}{\sum_j e^{f_j}}\right), \quad \frac{\partial L_i}{\partial f_k} = p_k - \mathbf{1}(y_i = k) $$
- 👑 **L4**: 证明 Cross-Entropy Loss 与 Softmax 组合时梯度的简洁性。

### 2. HW02 - 多层感知机与前向/反向传播 (Two-Layer Neural Network)
- **开源溯源**：Stanford CS231n Assignment 1
- 🟢 **L1**: 使用 PyTorch `nn.Module` 构建 2 层 MLP 分类 CIFAR-10。
- 🟡 **L2**: 引入 ReLU 激活函数、He/Kaiming 初始化与 L2 权重衰减。
- 🔴 **L3 (手撕核心)**：**手撕 2 层神经网络前向传播、链式法则反向传播 (Backpropagation) 梯度计算**。
- 👑 **L4**: 实现 Batch Normalization 层的前向与反向梯度推导。

### 3. HW03 - 卷积神经网络与算子手撕 (Convolutional Neural Networks)
- **开源溯源**：Stanford CS231n Assignment 2
- 🟢 **L1**: 使用 torchvision 标准 ResNet-18 跑通分类。
- 🟡 **L2**: 引入 CutMix / Mixup 数据增强与 Cosine Annealing 学习率调度。
- 🔴 **L3 (手撕核心)**：**基于 NumPy im2col 高效算法，从零手撕 Conv2d 前向/反向传播与 Max Pooling 算子**。
- 👑 **L4**: 模型量化 (Int8 Quantization) 与模型剪枝 (Pruning)。

### 4. HW04 - 目标检测与 Anchor 匹配 (Object Detection: Faster R-CNN & YOLO)
- **开源溯源**：Stanford CS231n / D2L Detection
- 🟢 **L1**: 调用 torchvision `fasterrcnn_resnet50_fpn` 在 Pascal VOC 上检测目标。
- 🟡 **L2**: 计算 IoU (Intersection over Union) 与 NMS (Non-Maximum Suppression) 非极大值抑制。
- 🔴 **L3 (手撕核心)**：**手撕 Anchor Box 生成算法与 IoU 重叠度矩阵计算引擎**。
- 👑 **L4**: 实现 FPN (Feature Pyramid Network) 多尺度特征融合。

### 5. HW05 - 语义分割与 U-Net (Semantic Segmentation & U-Net)
- **开源溯源**：Stanford CS231n / D2L Segmentation
- 🟢 **L1**: 在 Cityscapes 数据集上运行基础 FCN (Fully Convolutional Network)。
- 🟡 **L2**: 计算 Mean IoU (mIoU) 与 Dice Coefficient。
- 🔴 **L3 (手撕核心)**：**手撕 U-Net 编码器-解码器跳跃连接 (Skip Connections) 与转置卷积 (Transposed Conv) 计算**。
- 👑 **L4**: 实现 Mask R-CNN 实例分割。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-cv/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-cv/tests/test_hw01_softmax.py
pytest 03-Projects/projects-cv/tests/test_hw03_conv2d.py
```
