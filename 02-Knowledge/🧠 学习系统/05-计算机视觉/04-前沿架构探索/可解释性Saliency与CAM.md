---
type: study
course: "05-计算机视觉"
topic: "可解释性：Saliency Map与CAM"
created: 2026-08-05
status: ongoing
difficulty: intermediate
concept: ["可解释性","Saliency Map","CAM","Grad-CAM","模型解释"]
prerequisites: ["卷积神经网络CNN","反向传播"]
related: ["Transformer","迁移学习"]
flow: knowledge
upstream: ["[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/卷积神经网络CNN]]", "[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/反向传播与计算图]]", "[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/Softmax与SVM损失函数]]"]
stage_moc: "[[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🚀 第四阶段：前沿架构探索]]"
kind: concept
source: "CS231n A3讲义"
anki_deck: "05-计算机视觉::04-前沿架构探索"
anki_tags: ["计算机视觉","可解释性","Grad-CAM"]
tags: [学习,计算机视觉,可解释性,SaliencyMap,GradCAM]
---

# 🔷 可解释性：Saliency Map与CAM

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：深度学习长期被诟病为"黑盒"。Saliency Map（Simonyan et al., 2014）是输入梯度法鼻祖；CAM（Zhou et al., 2016）首次实现"不额外标注，CNN 自动定位关键区域"；Grad-CAM（Selvaraju et al., 2017）将 CAM 推广到任意架构，成为工业标配。从医疗 AI 合规到模型调试，不懂这些方法就无法回答"模型凭什么这么判断"。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem**：
> 你的 ResNet 以 95% 准确率通过测试。但部署到医疗影像时，医生说："你说这是恶性肿瘤，依据是肿瘤边界，还是片子右下角的医院 Logo？"模型做决策的依据是什么——是语义区域，还是数据中的虚假相关性（水印、背景、拍摄设备）？没有可解释性，模型的正确是巧合，错误则是深渊——无法修复一个不知道原因的误判。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：可解释性方法从不同粒度揭示 CNN 的内部表征——Saliency Map 通过输入梯度定位关键像素，CAM/Grad-CAM 通过特征图加权定位关键语义区域。这验证了 CNN 确实在底层学边缘、中层学纹理、高层学语义部件，与生物视觉层级抽象一致。
- **实际应用场景**：医疗 AI（Grad-CAM 热力图展示诊断依据）、模型调试（发现"哈士奇 vs 狼"的模型实际在看雪地背景——Ribeiro et al., 2016 的经典案例）、弱监督定位（仅用分类标签自动定位物体）、自动驾驶/金融风控的合规审计。
- **高频考点**：区分 Saliency Map / CAM / Grad-CAM 的计算流程与差异；理解 GAP 在 CAM 中的关键作用；手写 Grad-CAM 的 PyTorch 实现；解释为什么 ReLU 出现在 Grad-CAM 公式中。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[卷积神经网络CNN]]**：理解卷积层、特征图（Feature Map）、全连接层的基本数据流动。
2. **[[反向传播与计算图]]**：核心！Saliency Map 和 Grad-CAM 都用反向传播，但求导对象不再是权重 $W$，而是输入 $\mathbf{X}$ 或特征图 $\mathbf{A}$。
3. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/Softmax与SVM损失函数|Softmax]]**：理解 logit $S_c$ 与 softmax 概率的区别，以及为何可解释性方法通常对 logits 求导（避免 Softmax 饱和导致梯度消失）。

---

## 4. 用直觉语言解释它

> «"这东西其实就像……"»

- **Saliency Map——"哪个像素最要命"**：你想知道模型凭什么判断"这是一只狗"。你用手依次遮住不同区域——遮住狗鼻子时打分暴跌，说明鼻子是关键。Saliency Map 用梯度替换了这个遮挡实验：对每个像素求 $\partial S_c / \partial \mathbf{X}$，梯度大的像素就是模型"盯得最紧"的地方。
- **CAM——"特征图投票"**：CNN 最后卷积层有 512 张特征图，各负责检测不同视觉模式（眼睛、毛发……）。分类头（GAP → FC）给"对判断猫有帮助的特征图"分配大权重。用这些权重对特征图加权求和，合成热力图——模型到底在图的什么地方看到了"猫的证据"。**限制**：必须 GAP → FC 结构（ResNet、GoogLeNet 适用；VGG 不适用）。
- **Grad-CAM——"万能适配器"**：不再依赖分类头权重。对任意层的特征图 $\mathbf{A}^k$ 求梯度 $\partial S_c / \partial A_{ij}^k$，用梯度的空间均值 $\alpha_k^c$ 作为特征图重要性权重。VGG、ResNet、DenseNet、ViT 全部通用。
- **Guided Backprop——"只看正向激励"**：普通反向传播正负梯度掺杂。Guided Backprop 在 ReLU 反向传播时加一道门——只允许"前向激活为正 + 反向梯度为正"的信号通过。结果：只保留对目标类有正向贡献的像素，边缘清晰锐利。常与 Grad-CAM 点乘得 **Guided Grad-CAM**（粗定位 + 细纹理）。

> **一句话本质**：可解释性 = 把 $S_c$ 对"你想知道谁在起作用"的东西求偏导——对 $\mathbf{X}$ 求导得 Saliency Map，对 $\mathbf{A}^k$ 求导并加权得 Grad-CAM。

---

## 5. 正式定义、核心公式、符号解释

### 5.1 Saliency Map（输入梯度法）

$$\text{Saliency}_{ij} = \max_{ch \in \{R,G,B\}} \left| \frac{\partial S_c}{\partial X_{ij,ch}} \right|$$

- **流程**：前向得 $S_c$ → 反向求 $\partial S_c/\partial \mathbf{X}$ → 取绝对值 + 按通道取 max → 归一化。
- **局限**：像素级梯度噪声极大，热力图不平滑，难以勾勒完整物体轮廓。

### 5.2 CAM（Class Activation Mapping）

前提：最后卷积层 → **GAP** → FC。设特征图 $\mathbf{A}^k \in \mathbb{R}^{H' \times W'}$，GAP 后 $f_k = \frac{1}{Z}\sum_{i,j} A_{ij}^k$，分类得分 $S_c = \sum_k w_k^c f_k$。

交换求和顺序得：

$$\text{CAM}^c = \sum_{k=1}^K w_k^c \cdot \mathbf{A}^k$$

- **$w_k^c$**：FC 层第 $(k, c)$ 权重——天然就是第 $k$ 张特征图对类别 $c$ 的重要性。
- **限制**：必须有 GAP，且只用最后一层卷积。

### 5.3 Grad-CAM（梯度加权 CAM）

对任意卷积层输出的 $\mathbf{A}^k$，定义特征图 $k$ 的重要性权重为其梯度的全局均值：

$$\alpha_k^c = \frac{1}{Z} \sum_{i=1}^{H'} \sum_{j=1}^{W'} \frac{\partial S_c}{\partial A_{ij}^k}$$

$$\text{Grad-CAM}^c = \text{ReLU}\left( \sum_{k=1}^K \alpha_k^c \cdot \mathbf{A}^k \right)$$

- **ReLU**：只保留对 $c$ 有**正向贡献**（$\alpha_k^c > 0$）的特征，抑制负贡献区域。
- **推广优势**：无需 GAP，可用于 VGG/ResNet/DenseNet/ViT 等任意架构；可对**任意层**（不仅最后一层）求 Grad-CAM，观察不同抽象层次的可解释性。
- **与 CAM 等价性**：对于 GAP → FC 结构，Grad-CAM 与 CAM 在数学上等价。

### 5.4 Guided Backpropagation

在 ReLU 反向传播中施加双重门控：

$$\frac{\partial L}{\partial x} = \frac{\partial L}{\partial y} \cdot \mathbf{1}_{y > 0} \cdot \mathbf{1}_{\frac{\partial L}{\partial y} > 0}$$

只允许"前向激活为正 **且** 反向梯度为正"的信号通过，滤除负向干扰。与 Grad-CAM 点乘 = **Guided Grad-CAM**：Grad-CAM 提供粗粒度"位置"，Guided Backprop 提供细粒度"边缘纹理"。

### 5.5 符号说明表

| 符号 | 含义 | 维度 | 备注 |
| :--- | :--- | :--- | :--- |
| $\mathbf{X}$ | 输入图像 | $\mathbb{R}^{H \times W \times 3}$ | 原始像素 |
| $S_c$ | 类别 $c$ 的 logit | 标量 | 未经 Softmax |
| $\mathbf{A}^k$ | 第 $k$ 张特征图 | $\mathbb{R}^{H' \times W'}$ | 目标卷积层输出 |
| $K$ | 特征图通道数 | 标量 | 如 ResNet-50 layer4: $K=2048$ |
| $w_k^c$ | CAM 分类权重 | 标量 | GAP → FC 的第 $(k,c)$ 个权重 |
| $\alpha_k^c$ | Grad-CAM 重要性权重 | 标量 | 梯度全局均值 |
| $Z$ | 特征图像素数 | 标量 | $Z = H' \times W'$ |

---

## 6. 推导思路和思想来源

- **Saliency Map 的诞生（Simonyan et al., 2014）**：关键转念——训练时用 $\partial L / \partial W$ 更新权重，那为什么不用 $\partial S_c / \partial \mathbf{X}$ 来"问网络哪些像素最重要"？局限是像素级梯度噪声极大。

- **CAM 的意外之喜（Zhou et al., 2016）**：NIN（Lin et al., 2014）中提出的 GAP 层本是为了替代 Flatten 减少参数，但意外发现 GAP → FC 结构中分类头权重 $w_k^c$ 天然就是特征图的重要性权重——不需要任何额外训练即可生成定位热力图。限制：架构必须 GAP → FC。

- **Grad-CAM 的关键洞察（Selvaraju et al., 2017）**：用**梯度替代权重**。既然 CAM 的 $w_k^c$ 衡量特征图对 $S_c$ 的贡献，那直接用 $\partial S_c / \partial \mathbf{A}^k$ 的空间均值 $\alpha_k^c$ 也能做到同样的事——而且不再需要 GAP。数学上可以证明：当 $S_c$ 对 $A_{ij}^k$ 近似线性时，Grad-CAM 退化为 CAM。

- **Guided Backprop（Springenberg et al., 2015）**：结合 DeconvNet（滤除负激活）和普通反向传播，只传播"双重为正"的信号，生成更干净的像素级可视化。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础（手算 Saliency Map 梯度）

**题目**：极简网络——$2 \times 2$ 灰度图 $\mathbf{X}$ 经 GAP 得 $f = \frac{1}{4}\sum x_{ij}$，$S_c = w \cdot f + b$。求 $\partial S_c / \partial \mathbf{X}$。

**解答**：$\partial S_c / \partial x_{ij} = w/4$。每个像素梯度相同——GAP 压缩了空间信息。**教训**：Saliency Map 的精细度取决于网络对空间分辨率的保持程度。

### 例子 2：中等（Grad-CAM $\alpha_k^c$ 推导验证）

**题目**：$K=2$ 特征图，$\mathbf{A}^1 = \begin{bmatrix}1&0\\3&2\end{bmatrix}$，$\mathbf{A}^2 = \begin{bmatrix}2&1\\0&4\end{bmatrix}$。GAP → FC，$w_1^c=0.8$，$w_2^c=-0.3$。分别用 CAM 和 Grad-CAM 计算。

**解答**：CAM：$\text{CAM}^c = 0.8\mathbf{A}^1 + (-0.3)\mathbf{A}^2 = \begin{bmatrix}0.2&-0.3\\2.4&0.4\end{bmatrix}$。

Grad-CAM：$S_c = 0.8\times1.5 + (-0.3)\times1.75 = 0.675$。$\partial S_c/\partial A_{ij}^1 = 0.8/4=0.2$，$\alpha_1^c=0.2$。同理 $\alpha_2^c=-0.075$。

$\text{ReLU}(0.2\mathbf{A}^1 + (-0.075)\mathbf{A}^2) = \text{ReLU}\begin{bmatrix}0.05&-0.075\\0.6&-0.1\end{bmatrix} = \begin{bmatrix}0.05&0\\0.6&0\end{bmatrix}$

$\alpha_k^c = w_k^c/Z$——CAM 与 Grad-CAM 仅在缩放因子 $1/Z$ 上差一个常量，归一化后等价。ReLU 额外滤除了负贡献。

### 例子 3：实际应用（PyTorch 实现 Grad-CAM）

```python
import torch
import torch.nn.functional as F
import cv2
import numpy as np


class GradCAM:
    """对任意 CNN 的任意目标层生成 Grad-CAM 热力图。"""
    def __init__(self, model, target_layer):
        self.model = model
        self.activations = None
        self.gradients = None
        target_layer.register_forward_hook(self._save_activation)
        target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, module, input, output):
        self.activations = output.detach()

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate(self, input_image, target_class=None):
        """返回热力图 (H', W') ∈ [0, 1]"""
        output = self.model(input_image)
        if target_class is None:
            target_class = output.argmax(dim=1).item()
        self.model.zero_grad()
        output[0, target_class].backward(retain_graph=True)

        gradients = self.gradients[0]               # (K, H', W')
        alpha = gradients.mean(dim=(1, 2))           # (K,)

        activations = self.activations[0]            # (K, H', W')
        for k in range(alpha.shape[0]):
            activations[k] *= alpha[k]
        cam = activations.sum(dim=0)                 # (H', W')
        cam = F.relu(cam)
        cam = (cam - cam.min()) / (cam.max() + 1e-8)
        return cam.detach().cpu().numpy()


def apply_colormap(cam, original_image, alpha=0.5):
    """上采样热力图并叠加到原图。"""
    h, w = original_image.shape[:2]
    cam_resized = cv2.resize(cam, (w, h))
    heatmap = cv2.applyColorMap(np.uint8(255 * cam_resized), cv2.COLORMAP_JET)
    return cv2.addWeighted(original_image, 1 - alpha, heatmap, alpha, 0)


# ===== 使用示例（需取消注释） =====
# model = models.resnet50(pretrained=True).eval()
# grad_cam = GradCAM(model, model.layer4[-1])
# # img_rgb = cv2.cvtColor(cv2.imread("cat.jpg"), cv2.COLOR_BGR2RGB)
# # input_tensor = transform(img_rgb).unsqueeze(0)
# # cam = grad_cam.generate(input_tensor)
# # overlay = apply_colormap(cam, img_rgb)
```

**关键细节**：
1. **Hook 机制**：`forward_hook` 截获激活值，`backward_hook` 截获梯度——非侵入式获取中间层数据。
2. **$\alpha_k^c$ 的计算**：`.mean(dim=(1,2))` 对 $H' \times W'$ 取全局均值，等价于 $\frac{1}{Z}\sum_i\sum_j$。
3. **ReLU**：只保留正向贡献特征，抑制负向区域。
4. **上采样**：热力图分辨率 = 目标层特征图尺寸（如 ResNet-50 layer4 为 $7 \times 7$），需 `cv2.resize` 到原图尺寸。

---

## 8. 常见误区和易混概念

### 误区 1：Saliency Map 和 Grad-CAM 是一回事
- **纠正**：Saliency Map 对**输入像素** $\mathbf{X}$ 求导（像素级，噪声大）；Grad-CAM 对**特征图** $\mathbf{A}^k$ 求导（语义区域级，平滑）。粒度不同。

### 误区 2：Grad-CAM 需要 GAP 层
- **纠正**：Grad-CAM 的核心设计就是**绕开 GAP 限制**，适用于 VGG/ResNet/DenseNet/ViT。需要 GAP 的是 CAM。

### 误区 3：热力图越亮 = 模型越确定
- **纠正**：Grad-CAM 只告诉你模型依赖哪些区域，不告诉你决策是否正确。"哈士奇 vs 狼"案例中，模型在看雪地——热力图照样亮。

### 误区 4：Guided Backprop 比普通反向传播"更准确"
- **纠正**：双重门控是强烈的先验剪枝——更干净但也可能过度滤除负贡献信号。它不"更准确"，而是"更偏向正向"。

### 概念对比表

| 方法 | 对谁求导 | 输出分辨率 | 架构限制 | 典型用途 |
| :--- | :--- | :--- | :--- | :--- |
| Saliency Map | 输入 $\mathbf{X}$ | 原图分辨率 | 无 | 像素级重要性初探 |
| CAM | 不求导（用 FC 权重） | 最后特征图尺寸 | 需 GAP → FC | 弱监督定位 |
| Grad-CAM | 特征图 $\mathbf{A}^k$ | 目标层特征图尺寸 | 无 | 通用语义区域定位 |
| Guided Backprop | 输入 $\mathbf{X}$（双门控） | 原图分辨率 | 需 ReLU | 细粒度边缘纹理 |
| Guided Grad-CAM | 两者点乘 | 原图分辨率 | 无 | 粗定位 + 细纹理 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[卷积神经网络CNN]]：特征图概念是所有 CAM 类方法的基础。
- [[反向传播与计算图]]：Grad-CAM 对中间层索求梯度依赖链式法则。
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/激活函数详解]]：Guided Backprop 的核心是对 ReLU 反向传播的修改。

### 下游延伸
- 注意力可视化：Transformer 的 Self-Attention 自带可解释性——$\text{softmax}(QK^T/\sqrt{d_k})$ 的注意力权重矩阵本身就是一种"CAM"。
- [[ViT]]：ViT 的 Attention Rollout 是 Transformer 版本的可解释性方法。
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/03-视觉核心任务/迁移学习与微调]]：Grad-CAM 验证迁移后模型的关注区域是否合理。

### 横向关联
- **Saliency Map ↔ 对抗样本**：同一数学引擎 $\partial S_c / \partial \mathbf{X}$ 驱动了相反的目标——前者解释模型，后者愚弄模型。
- **CAM ↔ NIN**：GAP 层的设计初衷是减少参数，意外催生了可解释性的"免费午餐"。

---

## 10. 闭卷复现任务

- [ ] 1. 一句话说清可解释性方法的核心数学思想（对谁求什么）。
- [ ] 2. 写出 Saliency Map 的计算流程（前向 → 反向 → 取绝对值 → 归一化）。
- [ ] 3. 写出 CAM 公式，解释为什么需要 GAP 层。
- [ ] 4. 写出 Grad-CAM 的 $\alpha_k^c$ 公式，解释为什么用均值而非极值。
- [ ] 5. 说明 Grad-CAM 相比 CAM 的推广优势（≥2 点）。
- [ ] 6. 解释 Guided Backprop 的双重门控条件。
- [ ] 7. 说出 Guided Grad-CAM 中两个组件的分工。
- [ ] 8. 手写 Grad-CAM 的核心 PyTorch 代码（hook + $\alpha_k^c$ + ReLU）。
- [ ] 9. 解释 ReLU 在 Grad-CAM 公式中的作用。
- [ ] 10. 画出四种方法的对比表（求导对象/分辨率/架构限制）。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | Saliency Map vs Grad-CAM 的求导对象 |
| 2 | 架构理解 | 基础 | CAM 的 GAP 依赖 |
| 3 | 公式运用 | 中等 | $\alpha_k^c$ 的计算方式选择 |
| 4 | 条件判断 | 中等 | ReLU 在 Grad-CAM 中的作用 |
| 5 | 综合分析 | 较难 | Guided Grad-CAM 的分工 |

### 题目与解析

#### 1. Saliency Map 对什么求偏导，Grad-CAM 对什么求偏导？

- A. 两者都对输入 $\mathbf{X}$ 求偏导
- B. Saliency Map 对 $\mathbf{X}$ 求偏导；Grad-CAM 对特征图 $\mathbf{A}^k$ 求偏导
- C. Saliency Map 对 $\mathbf{A}^k$ 求偏导；Grad-CAM 对 $\mathbf{X}$ 求偏导
- D. 两者都对 $\mathbf{A}^k$ 求偏导

> [!question]- 答案解析
> - **答案**：B。这是两者最本质的区别——决定了输出粒度：像素级 vs 语义区域级。

#### 2. CAM 为什么要求最后一层卷积后接 GAP 再接入 FC？

- A. GAP 提高分类准确率
- B. GAP 后才能做反向传播
- C. CAM 公式 $S_c = \sum w_k^c \cdot \text{GAP}(\mathbf{A}^k)$ 依赖 GAP 使 $w_k^c$ 与特征图直接线性对应
- D. 为了减少计算量

> [!question]- 答案解析
> - **答案**：C。没有 GAP，中间 Flatten → FC 的多次非线性变换会让 $w_k^c$ 失去与特征图的直接对应关系。

#### 3. 若将 $\alpha_k^c$ 的均值改为最大值 $\max_{i,j}$，会有什么问题？

- A. 不变，效果一样
- B. 对噪声极度敏感，可能被单个异常像素劫持
- C. 无法反向传播
- D. 热力图全为零

> [!question]- 答案解析
> - **答案**：B。均值代表特征图"整体"贡献，稳健且与 CAM 数学等价；最大值只取最敏感像素，易被噪声劫持。

#### 4. Grad-CAM 中的 ReLU 的作用是？

- A. 仅为了让值非负
- B. 只保留对目标类有正向贡献的特征区域，抑制负贡献
- C. 加速计算
- D. 防止梯度消失

> [!question]- 答案解析
> - **答案**：B。$\alpha_k^c < 0$ 的特征图代表"不是 $c$ 的证据"，ReLU 清零后可让热力图干净聚焦于"是 $c$ 的证据"。

#### 5. Guided Grad-CAM 中两个组件的分工是？

- A. Grad-CAM 细粒度纹理，Guided Backprop 粗粒度位置
- B. Grad-CAM 粗粒度位置（where），Guided Backprop 细粒度纹理（what）
- C. 两者信息相同，点乘只是增强
- D. Grad-CAM 处理正样本，Guided Backprop 处理负样本

> [!question]- 答案解析
> - **答案**：B。Grad-CAM 特征图分辨率低（$7\times7$），上采样后给出平滑热力区域；Guided Backprop 保留像素级高频边缘，提供精细纹理。

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

### 我的推导复现
> 不看上文，尝试写出核心公式或推导主线：

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **归档目录**：`04-前沿架构探索/`（已在此）
- **建议双链**：
  - [[卷积神经网络CNN]] — 特征图概念来源
  - [[反向传播与计算图]] — 梯度索取的数学基础
  - 注意力可视化 — Transformer 可解释性对应方法
  - [[ViT]] — Attention Map 可视化
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/03-视觉核心任务/迁移学习与微调]] — 验证迁移后关注区域
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/激活函数详解]] — Guided Backprop 依赖 ReLU
- **建议标签**：`#学习` `#计算机视觉` `#可解释性` `#SaliencyMap` `#GradCAM` `#CAM`
- **拆分建议**：当前覆盖 Saliency/CAM/Grad-CAM/Guided Backprop 四条线。若挖深可将 SHAP/LIME/Integrated Gradients 等模型无关方法另开卡片；Grad-CAM 的高级扩展（Score-CAM、Ablation-CAM、Transformer 适配版）也可单独成卡。

---
---

## 🔗 知识图谱

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
