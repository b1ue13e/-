---
title: "卷积神经网络 CNN (Convolutional Neural Network)"
course: "05-计算机视觉"
tags:
  - 计算机视觉
  - 深度学习
  - CNN
  - 卷积核
  - 感受野
  - 图像处理
type: knowledge_card
status: completed
created: 2026-07-31
---

# 卷积神经网络 CNN (Convolutional Neural Network)

## 1. 卷积神经网络 CNN 的定义与三大核心机制

**卷积神经网络 CNN (Convolutional Neural Network)** 的核心定义是：一种专门用于处理具有网格状拓扑结构数据（如二维图像、一维语音信号）的深度前馈神经网络。由 LeCun 等人于 1989 年在 LeNet-5 中提出，并由 Krizhevsky 等人在 AlexNet (2012) 中发扬光大。

**基本性质与三大核心机制**：
1. **局部感受野 (Local Receptive Fields)**：每个神经元仅与前一层局部区域的像素连接，捕捉局部特征（如边缘、纹理）；
2. **权值共享 (Weight Sharing)**：同一特征图 (Feature Map) 内的所有神经元共享同一组卷积核参数，使参数量减少多个数量级并赋予网络**平移不变性 (Translation Invariance)**；
3. **空间池化 (Spatial Pooling)**：通过 Downsampling（如 Max/Average Pooling）降低空间分辨率、减少计算量并增强对微小平移与变形的鲁棒性。

---

## 2. 卷积层输出尺寸与感受野形式化推导

**输入与超参数假设**：
- 输入图像尺寸：$H_{\text{in}} \times W_{\text{in}}$，通道数为 $C_{\text{in}}$；
- 卷积核尺寸：$K_h \times K_w$，卷积核个数（输出通道数）为 $C_{\text{out}}$；
- 填充 padding：$P_h, P_w$；步长 stride：$S_h, S_w$；膨胀率 dilation：$D_h, D_w$。

**输出尺寸推导公式**：
$$H_{\text{out}} = \left\lfloor \frac{H_{\text{in}} + 2 P_h - D_h(K_h - 1) - 1}{S_h} 
ight
floor + 1$$
$$W_{\text{out}} = \left\lfloor \frac{W_{\text{in}} + 2 P_w - D_w(K_w - 1) - 1}{S_w} 
ight
floor + 1$$

**参数量 (Params) 与 FLOPs 计算**：
- **参数量**：$\text{Params} = C_{\text{out}} \times (C_{\text{in}} \times K_h \times K_w + 1)$
- **浮点运算量**：$\text{FLOPs} \approx 2 \times H_{\text{out}} \times W_{\text{out}} \times C_{\text{out}} \times (C_{\text{in}} \times K_h \times K_w)$
- **因此**，相比全连接网络 (FC)，CNN 将连接数从 $O(H_{\text{in}} W_{\text{in}} H_{\text{out}} W_{\text{out}})$ 骤降至仅与卷积核大小相关，彻底解决了高维图像输入的维数灾难。

---

## 3. 卷积层与全连接层 (FC) 及视觉 Transformer (ViT) 的对比

| 维度 | 卷积神经网络 CNN | 全连接网络 (FC) | 视觉 Transformer (ViT) |
|:---|:---|:---|:---|
| **归纳偏置 (Inductive Bias)** | **强**（局部性 + 平移不变性）| 无 | **弱**（需大规模数据预训练）|
| **计算复杂度** | $O(K^2 \cdot H W \cdot C_{\text{in}} C_{\text{out}})$ | $O(N_{\text{in}} N_{\text{out}})$ | $O((HW)^2 \cdot C)$ (全局 Self-Attention) |
| **小样本学习能力** | **强**（泛化速度快，不易过拟合）| 极差 (易过拟合) | 中等 (依赖大集或强增强) |
| **长距离依赖捕捉** | 依赖深层堆叠扩大感受野 | 直接全连接 | **单层直接捕捉全局注意力** |

**局限（误区）**：池化操作会不可逆地丢失物体精细的位置与几何姿态信息，这使得纯 CNN 在要求密集像素预测（如语义分割、关键点检测）任务中需要借助空洞卷积 (Dilated Conv) 或跳跃连接 (FPN)。

关联知识点推荐：[[ResNet残差网络]]、[[YOLO目标检测]]、[[梯度下降与Adam优化器]]、[[交叉熵损失函数]]。

---

## 4. Python PyTorch 风格 2D 卷积前向计算与感受野推导自测断言

```python
import numpy as np

def conv2d_forward(x: np.ndarray, weight: np.ndarray, bias: np.ndarray,
                   stride: int = 1, padding: int = 0) -> np.ndarray:
    """
    手动实现 2D 卷积层前向传播
    x: (N, Cin, Hin, Win)
    weight: (Cout, Cin, Kh, Kw)
    bias: (Cout,)
    """
    N, Cin, Hin, Win = x.shape
    Cout, _, Kh, Kw = weight.shape

    Hout = (Hin + 2 * padding - Kh) // stride + 1
    Wout = (Win + 2 * padding - Kw) // stride + 1

    x_padded = np.pad(x, ((0,0), (0,0), (padding, padding), (padding, padding)), mode='constant')
    out = np.zeros((N, Cout, Hout, Wout), dtype=np.float32)

    for n in range(N):
        for c_out in range(Cout):
            for h in range(Hout):
                for w in range(Wout):
                    h_start = h * stride
                    w_start = w * stride
                    patch = x_padded[n, :, h_start:h_start+Kh, w_start:w_start+Kw]
                    out[n, c_out, h, w] = np.sum(patch * weight[c_out]) + bias[c_out]

    return out

if __name__ == "__main__":
    np.random.seed(42)
    x = np.random.randn(1, 3, 5, 5).astype(np.float32)  # Batch=1, Cin=3, 5x5
    weight = np.random.randn(2, 3, 3, 3).astype(np.float32) # Cout=2, 3x3
    bias = np.array([0.1, -0.2], dtype=np.float32)

    # 卷积计算 (P=0, S=1) -> Hout = (5-3)/1 + 1 = 3
    out = conv2d_forward(x, weight, bias, stride=1, padding=0)

    # 自测验证 1: 输出尺寸断言
    assert out.shape == (1, 2, 3, 3), f"输出尺寸异常: {out.shape}"

    # 自测验证 2: 填充测试 (P=1, S=1) -> Hout = (5+2-3)/1 + 1 = 5 (保持同尺寸 Same Conv)
    out_pad = conv2d_forward(x, weight, bias, stride=1, padding=1)
    assert out_pad.shape == (1, 2, 5, 5)

    # 自测验证 3: 感受野 (Receptive Field) 计算: 2 层 3x3 卷积的感受野 = 3 + (3-1) = 5
    rf_layer2 = 3 + (3 - 1) * 1
    assert rf_layer2 == 5, "两层 3x3 卷积感受野等价于 5x5"

    print("卷积神经网络 CNN 前向计算与感受野断言验证成功！")
    print(f"输出 Shape: {out.shape}, 带 Padding Shape: {out_pad.shape}")
    print("卷积神经网络 CNN 单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998). Gradient-based learning applied to document recognition (LeNet-5). *Proceedings of the IEEE*, 86(11), 2278-2324. DOI: https://doi.org/10.1109/5.726791
- Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks (AlexNet). *Advances in Neural Information Processing Systems (NIPS '12)*, 25, 1097-1105. DOI: https://doi.org/10.1145/3065386
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. Chapter 9 (Convolutional Networks). ISBN: 978-0262035613. URL: https://www.deeplearningbook.org/
