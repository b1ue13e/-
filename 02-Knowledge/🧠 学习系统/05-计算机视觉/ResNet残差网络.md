---
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

$$\frac{\partial \mathcal{E}}{\partial \mathbf{x}_l} = \frac{\partial \mathcal{E}}{\partial \mathbf{x}_L} \frac{\partial \mathbf{x}_L}{\partial \mathbf{x}_l} = \frac{\partial \mathcal{E}}{\partial \mathbf{x}_L} \left( \mathbf{I} + \frac{\partial}{\partial \mathbf{x}_l} \sum_{i=l}^{L-1} \mathcal{F}(\mathbf{x}_i, \mathbf{W}_i) 
ight)$$

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
    """模拟 ResNet BasicBlock: y = ReLU(Conv2(ReLU(Conv1(x))) + x)"""
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
