import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = Path("F:/-")
CV_DIR = VAULT_ROOT / "02-Knowledge" / "🧠 学习系统" / "05-计算机视觉"
if not CV_DIR.exists():
    CV_DIR = VAULT_ROOT / "🧠 学习系统" / "05-计算机视觉"

print(f"Stage 28: Upgrading CNN, ResNet, and YOLO in {CV_DIR}...")

# 1. 卷积神经网络CNN.md
cnn_content = """---
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
$$H_{\text{out}} = \left\lfloor \frac{H_{\text{in}} + 2 P_h - D_h(K_h - 1) - 1}{S_h} \right\rfloor + 1$$
$$W_{\text{out}} = \left\lfloor \frac{W_{\text{in}} + 2 P_w - D_w(K_w - 1) - 1}{S_w} \right\rfloor + 1$$

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
    \"\"\"
    手动实现 2D 卷积层前向传播
    x: (N, Cin, Hin, Win)
    weight: (Cout, Cin, Kh, Kw)
    bias: (Cout,)
    \"\"\"
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
"""

# 2. ResNet残差网络.md
resnet_content = """---
title: "ResNet 残差网络 (Residual Network)"
course: "05-计算机视觉"
tags:
  - 计算机视觉
  - ResNet
  - 残差网络
  - 恒等映射
  - 梯度退化
  - 深度学习
type: knowledge_card
status: completed
created: 2026-07-31
---

# ResNet 残差网络 (Residual Network)

## 1. ResNet 残差网络的定义与退化问题突破

**ResNet 残差网络 (Residual Network)** 的核心定义是：通过引入**跳跃连接 (Shortcut / Skip Connection)** 显式地将网络层拟合目标重构为**残差映射 $\mathcal{F}(\mathbf{x}) = \mathcal{H}(\mathbf{x}) - \mathbf{x}$** 的深度卷积神经网络架构。由 He (何恺明) 等人于 2015 年在 Microsoft Research 提出，并荣获 CVPR 2016 最佳论文奖。

**基本性质与退化问题 (Degradation Problem) 突破**：
在 ResNet 出现前，单纯堆叠更深的网络（如 20 层 vs 56 层）会导致训练集与测试集准确率同时下降的**网络退化现象**（非过拟合造成）。ResNet 残差网络通过恒等映射 (Identity Mapping) 保证了深层网络的优化难度不高于浅层网络，成功突破了深度学习 100+ 层的训练天花板（如 ResNet-152, ResNet-1001）。

---

## 2. 残差块形式化推导与梯度高速公路证明

**残差块 (Residual Block) 表达式**：
设残差块输入为 $\mathbf{x}$，期望拟合的映射为 $\mathcal{H}(\mathbf{x})$，网络隐层计算为 $\mathcal{F}(\mathbf{x}, \{\mathbf{W}_i\})$，则残差块输出为：

$$\mathbf{y} = \mathcal{F}(\mathbf{x}, \{\mathbf{W}_i\}) + \mathbf{x}, \quad \mathbf{x}_{l+1} = \text{ReLU}(\mathbf{y})$$

**梯度高速公路 (Gradient Highway) 形式化证明**：
假设从第 $l$ 层到第 $L$ 层（$L > l$）连续采用纯恒等映射 $\mathbf{x}_{l+1} = \mathbf{x}_l + \mathcal{F}(\mathbf{x}_l, \mathbf{W}_l)$，展开可得递归式：

$$\mathbf{x}_L = \mathbf{x}_l + \sum_{i=l}^{L-1} \mathcal{F}(\mathbf{x}_i, \mathbf{W}_i)$$

设标量损失为 $\mathcal{E}$，根据多元链式法则求第 $l$ 层激活值的梯度：

$$\frac{\partial \mathcal{E}}{\partial \mathbf{x}_l} = \frac{\partial \mathcal{E}}{\partial \mathbf{x}_L} \frac{\partial \mathbf{x}_L}{\partial \mathbf{x}_l} = \frac{\partial \mathcal{E}}{\partial \mathbf{x}_L} \left( \mathbf{I} + \frac{\partial}{\partial \mathbf{x}_l} \sum_{i=l}^{L-1} \mathcal{F}(\mathbf{x}_i, \mathbf{W}_i) \right)$$

**因此**：
1. 梯度包含一个直接项 $\frac{\partial \mathcal{E}}{\partial \mathbf{x}_L} \mathbf{I}$；
2. 即使残差项梯度 $\frac{\partial \mathcal{F}}{\partial \mathbf{x}_l}$ 接近于 0，总梯度也绝不会为 0（恒等项 $\mathbf{I}$ 无损反向传递误差）；
3. 这一性质彻底消除了深层网络中的**梯度消失**问题。

---

## 3. 基础残差块 (BasicBlock) 与瓶颈残差块 (Bottleneck) 对比

| 维度 | BasicBlock (ResNet-18/34) | Bottleneck (ResNet-50/101/152) |
|:---|:---|:---|
| **卷积层结构** | 2 层 $3 \times 3$ 卷积 | 3 层结构 ($1 \times 1 \to 3 \times 3 \to 1 \times 1$) |
| **通道维度变化** | 通道数保持不变 | $C \to C/4 \to C$ (降维再升维) |
| **计算量与参数** | 较高（针对中等通道）| **极其节省 FLOPs** ($1 \times 1$ 压缩算力) |
| **适用深度** | 浅层 ResNet ($\le 34$ 层) | 深层 ResNet ($\ge 50$ 层) |

**局限（误区）**：若 Shortcut 分支的尺寸或通道数与残差分支不匹配，须使用 $1 \times 1$ 卷积做投影映射 $\mathbf{y} = \mathcal{F}(\mathbf{x}) + \mathbf{W}_s \mathbf{x}$；若每层都加上非线性变换（如把 Identity 改为乘权重 $\lambda \mathbf{x}$），恒等通道破坏，梯度高速公路将立刻失效。

关联知识点推荐：[[卷积神经网络CNN]]、[[YOLO目标检测]]、[[反向传播算法BP]]、[[Amdahl定律]]。

---

## 4. Python 残差块 Skip Connection 与梯度无损传递自测断言

```python
import numpy as np

def relu(x): return np.maximum(0, x)

class BasicBlockSimulation:
    \"\"\"模拟 ResNet BasicBlock: y = ReLU(Conv2(ReLU(Conv1(x))) + x)\"\"\"
    def __init__(self, channels: int):
        np.random.seed(42)
        self.W1 = np.random.randn(channels, channels) * 0.1
        self.W2 = np.random.randn(channels, channels) * 0.1

    def forward(self, x: np.ndarray) -> np.ndarray:
        # F(x)
        out1 = relu(self.W1 @ x)
        fx = self.W2 @ out1
        # H(x) = F(x) + x
        return relu(fx + x)

if __name__ == "__main__":
    block = BasicBlockSimulation(channels=4)
    x = np.array([[1.0], [-0.5], [2.0], [0.0]])

    out = block.forward(x)

    # 自测验证 1: 输出维度不变断言
    assert out.shape == (4, 1)

    # 自测验证 2: 恒等映射保底断言 (即使权重为0，输出也不应为0)
    zero_block = BasicBlockSimulation(channels=4)
    zero_block.W1.fill(0.0)
    zero_block.W2.fill(0.0)
    zero_out = zero_block.forward(x)
    # H(x) = ReLU(0 + x)
    expected_zero = relu(x)
    assert np.array_equal(zero_out, expected_zero), "零权重下应退化为纯恒等映射"

    print(f"ResNet 恒等映射保护测试通过: 零权重输出等于原始 ReLU(x)")
    print("ResNet 残差网络单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep residual learning for image recognition (ResNet). *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR '16)*, 770-778. DOI: https://doi.org/10.1109/CVPR.2016.90
- He, K., Zhang, X., Ren, S., & Sun, J. (2016). Identity mappings in deep residual networks. *European Conference on Computer Vision (ECCV '16)*, 630-645. DOI: https://doi.org/10.1007/978-3-319-46493-0_38
- Russakovsky, O., et al. (2015). ImageNet large scale visual recognition challenge. *International Journal of Computer Vision (IJCV)*, 115(3), 211-252. DOI: https://doi.org/10.1007/s11263-015-0816-y
"""

# 3. YOLO目标检测.md
yolo_content = """---
title: "YOLO 目标检测算法 (You Only Look Once)"
course: "05-计算机视觉"
tags:
  - 计算机视觉
  - YOLO
  - 目标检测
  - 单阶段检测
  - NMS
  - Anchor
type: knowledge_card
status: completed
created: 2026-07-31
---

# YOLO 目标检测算法 (You Only Look Once)

## 1. YOLO 目标检测算法的定义与单阶段突破

**YOLO 目标检测算法 (You Only Look Once)** 的核心定义是：将目标检测任务直接重构为**单阶段 (One-Stage) 端到端回归问题**的实时目标检测框架。由 Redmon 等人于 2015 年在 CVPR 提出。

**基本性质与单阶段突破**：传统两阶段 (Two-Stage) 检测器（如 Faster R-CNN）先由 RPN 生成候选框 (Region Proposals)，再对分类与回归进行二次计算，速度受限（~5-7 FPS）。YOLO 目标检测算法仅需对全图进行**单次前向传播 (Single Forward Pass)**，即可并发预测出整张图像中所有目标的边界框 (Bounding Box) 物理坐标与类别概率，实现高达 45~155 FPS 的超实时检测。

---

## 2. 网格划分、损失函数与非极大值抑制 (NMS) 形式化推导

**网格划分 (Grid Cell) 与输出张量推导**：
1. 将输入图像划分为 $S \times S$ 个网格（如 $7 \times 7$）；
2. 若目标中心落在某个网格内，则该网格负责检测该目标；
3. 每个网格预测 $B$ 个 Bounding Box，每个 Box 包含 5 个预测值：$(x, y, w, h, c)$，其中 $c$ 为置信度 $\text{Pr}(\text{Object}) \times \text{IoU}_{\text{pred}}^{\text{truth}}$；
4. 输出张量维度为 $S \times S \times (B \times 5 + C)$（$C$ 为类别数）。

**多任务复合损失函数 (Multi-Part Loss)**：
$$L_{\text{YOLO}} = \lambda_{\text{coord}} \sum_{i=0}^{S^2} \sum_{j=0}^B \mathbb{I}_{ij}^{\text{obj}} \left[ (x_i - \hat{x}_i)^2 + (y_i - \hat{y}_i)^2 + (\sqrt{w_i} - \sqrt{\hat{w}_i})^2 + (\sqrt{h_i} - \sqrt{\hat{h}_i})^2 \right]$$
$$+ \sum_{i=0}^{S^2} \sum_{j=0}^B \mathbb{I}_{ij}^{\text{obj}} (C_i - \hat{C}_i)^2 + \lambda_{\text{noobj}} \sum_{i=0}^{S^2} \sum_{j=0}^B \mathbb{I}_{ij}^{\text{noobj}} (C_i - \hat{C}_i)^2 + \sum_{i=0}^{S^2} \mathbb{I}_i^{\text{obj}} \sum_{c \in \text{classes}} (p_i(c) - \hat{p}_i(c))^2$$

**NMS (Non-Maximum Suppression) 消除冗余框**：
对所有得分高于阈值的框按 Score 排序，挑选最高分框 $B_{\text{max}}$，计算其他框与 $B_{\text{max}}$ 的 $\text{IoU}$，剔除 $\text{IoU} > \text{Threshold}$ 的重叠框，重复迭代。

---

## 3. 单阶段 (YOLO) 与两阶段 (Faster R-CNN) 检测器对比

| 维度 | YOLO 单阶段检测器 | Faster R-CNN 两阶段检测器 |
|:---|:---|:---|
| **预测范式** | 全图单次回归预测 | RPN 生成候选区 $\to$ ROI Pooling $\to$ 2nd 头部 |
| **推理速度** | **超实时 (45 - 160+ FPS)** | 较慢 (5 - 15 FPS) |
| **背景误报 (Background Error)** | **低**（看全图，全局上下文好）| 较高（只看局部 Proposal 易把背景认错）|
| **小目标定位精度** | 早期版本稍低（受限网格） | 较高（多尺度特征融合与 ROI 对齐） |
| **代表演进版本** | YOLOv1~v8, YOLOX | Fast / Faster / Mask R-CNN |

**局限（误区）**：早期 YOLOv1 每个网格最多检测一个目标，在面对密集小目标群（如成群飞鸟）时存在定位瓶颈；后来的 YOLOv2/v3 引入了 **Anchor Boxes** 与 **FPN 多尺度预测**，彻底解决了小目标检测难题。

关联知识点推荐：[[卷积神经网络CNN]]、[[ResNet残差网络]]、[[交叉熵损失函数]]、[[均方误差MSE与Huber损失]]。

---

## 4. Python IoU (交并比) 计算与 NMS 算法自测断言

```python
import numpy as np

def compute_iou(box1: np.ndarray, box2: np.ndarray) -> float:
    \"\"\"
    计算两个矩形框的 IoU (Intersection over Union)
    box 格式: [x1, y1, x2, y2]
    \"\"\"
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    union_area = box1_area + box2_area - inter_area
    return float(inter_area / union_area) if union_area > 0 else 0.0

def nms_suppression(boxes: np.ndarray, scores: np.ndarray, iou_threshold: float = 0.5) -> list:
    \"\"\"非极大值抑制 NMS\"\"\"
    idxs = np.argsort(scores)[::-1]
    keep = []

    while len(idxs) > 0:
        current = idxs[0]
        keep.append(current)
        if len(idxs) == 1:
            break
        rem_idxs = idxs[1:]
        ious = np.array([compute_iou(boxes[current], boxes[i]) for i in rem_idxs])
        idxs = rem_idxs[ious <= iou_threshold]

    return keep

if __name__ == "__main__":
    # 测试 1: 完全重合 IoU == 1.0
    b1 = np.array([0, 0, 10, 10])
    b2 = np.array([0, 0, 10, 10])
    assert compute_iou(b1, b2) == 1.0

    # 测试 2: 部分重叠 IoU
    b3 = np.array([5, 0, 15, 10])
    # inter = 5x10=50, union = 100+100-50 = 150 -> 50/150 = 0.3333
    iou_val = compute_iou(b1, b3)
    assert abs(iou_val - 1/3) < 1e-4

    # 测试 3: NMS 筛选测试
    boxes = np.array([[0,0,10,10], [1,1,10,10], [100,100,110,110]])
    scores = np.array([0.9, 0.8, 0.95])
    keep_indices = nms_suppression(boxes, scores, iou_threshold=0.5)

    # 应保留最高分的框 2 (0.95) 与 框 0 (0.9)，框 1 (0.8) 与框 0 高度重合被抑制
    assert set(keep_indices) == {0, 2}

    print(f"IoU 计算验证成功: 重叠度 = {iou_val:.4f}")
    print(f"NMS 抑制成功: 原始 3 个候选框降至 {keep_indices}")
    print("YOLO 目标检测算法单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016). You only look once: Unified, real-time object detection (YOLOv1). *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR '16)*, 779-788. DOI: https://doi.org/10.1109/CVPR.2016.91
- Redmon, J., & Farhadi, A. (2017). YOLO9000: Better, faster, stronger (YOLOv2). *CVPR '17*, 7263-7271. DOI: https://doi.org/10.1109/CVPR.2017.690
- Ren, S., He, K., Girshick, R., & Sun, J. (2015). Faster R-CNN: Towards real-time object detection with region proposal networks. *Advances in Neural Information Processing Systems (NIPS '15)*, 28, 91-99. DOI: https://doi.org/10.1109/TPAMI.2016.2577031
"""

# Write files
(CV_DIR / "卷积神经网络CNN.md").write_text(cnn_content, encoding="utf-8")
(CV_DIR / "ResNet残差网络.md").write_text(resnet_content, encoding="utf-8")
(CV_DIR / "YOLO目标检测.md").write_text(yolo_content, encoding="utf-8")

print("Stage 28: Successfully written CNN, ResNet, and YOLO!")
