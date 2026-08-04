---
title: "计算机视觉-题型-ResNet与YOLO目标检测手撕阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "计算机视觉作业"
course: "05-计算机视觉"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["计算机视觉", "ResNet", "YOLO"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/17-机器学习/🗺️ 机器学习学习路径|机器学习]]"]
related: ["[[机器学习-题型-李宏毅式分类与深层模型阶梯作业]]"]
upstream: ["[[🗺️ 计算机视觉学习路径]]"]
downstream: []
tags: [学习, 05-计算机视觉, 作业, 实战, 阶梯作业]
aliases: ["CS231n-HW03-ResNetYOLO作业"]
---

# 计算机视觉 - HW03：ResNet 与 YOLO 目标检测手撕阶梯作业

> 🎯 **作业目标**：手写 kNN/Softmax、从零实现带有残差连接的 ResNet-50，并构建简易 YOLO 目标检测模型。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-cv/hw03_resnet_yolo.ipynb`
- **开源标杆仓库**：[Michigan EECS 498-007 / CS231n](https://eecs498-007-welcome.github.io/)
- **核心依赖**：`torch`, `torchvision`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 CIFAR-10 / mAP | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | CIFAR-10 Acc ≥ 60.0% | 手写 kNN 与 Softmax Classifier 处理 CIFAR-10。 |
| 🟡 **L2 - Medium Baseline** | Acc ≥ 78.0% | **手写 Im2col 卷积优化**：实现 2 层 CNN 的 Forward 与 Backward 梯度推导。 |
| 🔴 **L3 - Strong Baseline** | **手撕 ResNet-50 & FPN** | 用 PyTorch 从零构建包含 Residual Bottleneck Block 的 ResNet-50 架构。 |
| 👑 **L4 - Boss Baseline** | mAP@0.5 ≥ 65.0% | 从零手写 YOLOv3 / YOLOv5 Anchor-based 目标检测 Head 与 IoU/NMS 非极大值抑制。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import torch

def test_resnet_block_residual_connection():
    from cv_models import ResidualBlock
    block = ResidualBlock(in_channels=64, out_channels=64)
    x = torch.randn(4, 64, 32, 32)
    out = block(x)
    
    assert out.shape == (4, 64, 32, 32)
    assert not torch.allclose(out, x), "残差块输出不得与原始输入完全相同（需经卷积与 ReLU）"
```

---

## 🃏 Anki 卡片

- Q: 为什么 ResNet 的 Residual Block ($y = F(x) + x$) 能够解决超深层网络（如 100+ 层）梯度消失的问题？
- A: 在反向传播求导时，$\frac{\partial y}{\partial x} = \frac{\partial F(x)}{\partial x} + 1$。即使 $F(x)$ 的梯度接近于 0，恒等映射常数 1 也能确保上层梯度无损耗地直通底层。
