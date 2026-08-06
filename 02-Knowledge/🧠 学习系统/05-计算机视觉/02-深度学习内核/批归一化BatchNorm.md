---
type: study
course: "05-计算机视觉"
topic: "批归一化与训练优化 (Batch Normalization)"
created: 2026-08-05
status: ongoing
difficulty: intermediate
concept: ["BatchNorm", "批归一化", "内部协变量偏移", "训练优化", "归一化层"]
prerequisites:
  - "前向传播"
  - "梯度计算"
related:
  - "LayerNorm"
  - "InstanceNorm"
  - "GroupNorm"
  - "ResNet残差网络"
flow: knowledge
upstream: ["[[前向传播]]", "[[反向传播与计算图]]"]
stage_moc: "[[🧠 第二阶段：深度学习内核]]"
kind: concept
source: "CS231n A2; D2L Ch.8"
anki_deck: "05-计算机视觉::02-深度学习内核"
anki_tags:
  - "BatchNorm"
  - "批归一化"
  - "归一化层"
  - "训练优化"
tags: [学习, 计算机视觉, BatchNorm, 批归一化, 归一化层, 训练优化]
---

# 🎯 批归一化与训练优化 (Batch Normalization)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：Batch Normalization（BN，批归一化）由 Sergey Ioffe 和 Christian Szegedy 于 2015 年提出，是深度学习训练工程中最具影响力的技术之一。它通过在每个 mini-batch 内对激活值进行标准化，一举解决了深层网络训练中**内部协变量偏移 (Internal Covariate Shift)**、梯度消失/爆炸、对权重初始化极度敏感三大痛点。BN 使得使用高达 10× 的初始学习率成为可能、大幅降低了对 Dropout 的依赖，并成为 ResNet、DenseNet、EfficientNet 等几乎所有 SOTA 架构的标准层。理解 BN 的前向/反向公式、训练/测试模式差异，是掌握现代深度学习训练管线的必修课。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem（我们遇到了什么麻烦）**：
> 在 BN 出现之前，训练深层神经网络极其困难。核心问题有三：
>
> **① 内部协变量偏移 (Internal Covariate Shift, ICS)**：
> 在训练过程中，由于前面层参数的更新，后面层接收到的输入数据分布会不断变化。这相当于每层都面对一个"不断漂移的靶子"——SGD 本来假设数据分布是平稳的，现在每更新一步前面的参数，后面层的输入分布就变了，导致后面层不得不持续重新适应，训练效率极低。
>
> **② 梯度消失/爆炸**：
> 深层网络中，若激活值分布漂移到饱和区（如 Sigmoid 的两端），梯度趋近于 0，浅层参数完全无法更新；若激活值分布漂移到极大值区域，梯度爆炸让训练发散。在没有 BN 的年代，人们不得不小心翼翼地设计权重初始化方案（如 Xavier/He 初始化）和小得可怜的学习率。
>
> **③ 对超参数极度敏感**：
> 学习率稍大就发散，稍小就收敛极慢；Dropout 强度、权重衰减系数必须精调，换一个数据集就失效——调参成本极高。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：BN 是深度学习从"炼丹"走向"工程化"的关键转折点。它将归一化操作内嵌为网络的可微分层，使得整个训练过程对超参数的选择更加鲁棒。BN + ResNet 残差连接 + Adam 优化器被合称为"深度学习训练三件套"。
- **实际应用场景**：
  - 图像分类（ResNet、VGG、EfficientNet 的标准组件）
  - 目标检测与分割（Faster R-CNN、Mask R-CNN 的 backbone 必备）
  - GAN 训练中稳定生成器与判别器的梯度流
  - 几乎所有基于卷积的视觉任务
- **高频考点/任务**：ICS 问题的定义、BN 前向四步公式、训练/测试模式差异（`running_mean` / `running_var`）、手推 BN 反向传播梯度、LayerNorm vs BatchNorm 的适用场景对比、为什么 BN 在 batch size 很小时失效。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[前向传播|前向传播与全连接层]]**：理解层与层之间的激活值如何流动，$z = Wx + b$ 形式的线性变换。
2. **[[反向传播与计算图|反向传播与链式法则]]**：能够对复合函数逐级求导，理解 $\frac{\partial \mathcal{L}}{\partial x} = \frac{\partial \mathcal{L}}{\partial y} \cdot \frac{\partial y}{\partial x}$ 的递推逻辑。
3. **基本概率统计**：均值 $\mu$、方差 $\sigma^2$、标准化 $z = \frac{x - \mu}{\sigma}$ 的含义。

---

## 4. 用直觉语言解释它

> «"这东西其实就像……"»

- **直觉类比 1 — 流水线质检员**：
  想象工厂流水线，每一道工序（层）的工人（神经元）都在加工零件（激活值）。问题是：上道工序的师傅今天心情好，把零件磨得特别小（均值变小），明天心情不好又磨得特别大（均值变大）。下道工序的工人每天面对尺寸忽大忽小的零件，根本没法稳定地精加工！
  **BN 就是给每道工序后加一个自动校准台**：不管上道工序出来的零件尺寸多离谱，校准台都把它们统一缩放到"均值=0、方差=1"的标准件，再通过两个可学习的旋钮（$\gamma$ 放大缩小、$\beta$ 平移）微调到最适合下道工序的状态。

- **直觉类比 2 — 考试的标准化评分**：
  原始分数（激活值）可能因为题目难度的不同而分布在不同的区间（0-40 或 80-100）。BN 相当于先把所有人的分数 Z-Score 标准化（均值 0，标准差 1），再伸缩平移到一个合理的分数范围。这样后续的"排名决策"（下一层网络的权重）就不会被分数的绝对数值范围干扰。

- **一句话直觉本质**：给每一层网络提供"白化处理后的稳定输入"，让每层只需学习"在这个稳定输入上做什么"，而不必同时适应"输入的漂移"。

---

## 5. 正式定义、核心公式、符号解释

### 5.1 问题形式化

考虑一个 mini-batch $\mathcal{B} = \{x_1, x_2, \ldots, x_m\}$，其中 $x_i \in \mathbb{R}^d$ 是某一层某个神经元在 $m$ 个样本上的激活值。BN 对该 mini-batch 执行如下变换：

$$\text{BN}_{\gamma, \beta}(x_i) = \gamma \cdot \hat{x}_i + \beta$$

### 5.2 前向传播四步公式

#### Step 1：计算 mini-batch 均值

$$\mu_\mathcal{B} = \frac{1}{m} \sum_{i=1}^{m} x_i$$

#### Step 2：计算 mini-batch 方差

$$\sigma_\mathcal{B}^2 = \frac{1}{m} \sum_{i=1}^{m} (x_i - \mu_\mathcal{B})^2$$

#### Step 3：标准化（Z-Score Normalization）

$$\hat{x}_i = \frac{x_i - \mu_\mathcal{B}}{\sqrt{\sigma_\mathcal{B}^2 + \epsilon}}$$

其中 $\epsilon$ 是一个极小常数（如 $10^{-5}$），防止除零。

#### Step 4：缩放与平移（Scale and Shift）

$$y_i = \gamma \cdot \hat{x}_i + \beta$$

其中 $\gamma$（scale）和 $\beta$（shift）是**可学习参数**，与权重 $W$ 一起通过反向传播更新。这一步至关重要：如果标准化后的分布确实就是最优的，网络可以学到 $\gamma = 1, \beta = 0$；如果网络需要不同的分布（如保持非线性），它可以通过调整 $\gamma, \beta$ 来恢复。

### 5.3 训练模式 vs 测试模式

| 模式 | $\mu$ 来源 | $\sigma^2$ 来源 | 关键细节 |
| :--- | :--- | :--- | :--- |
| **训练模式** | 当前 mini-batch 的 $\mu_\mathcal{B}$ | 当前 mini-batch 的 $\sigma_\mathcal{B}^2$ | 同时用指数移动平均 (EMA) 更新全局统计量 |
| **测试/推理模式** | 全局 `running_mean` | 全局 `running_var` | 使用训练阶段累积的无偏估计，不再依赖 batch |

**指数移动平均 (EMA) 更新公式**（训练时每个 batch 执行）：

$$\text{running\_mean} = \alpha \cdot \text{running\_mean} + (1 - \alpha) \cdot \mu_\mathcal{B}$$

$$\text{running\_var} = \alpha \cdot \text{running\_var} + (1 - \alpha) \cdot \sigma_\mathcal{B}^2$$

PyTorch 默认 $\alpha = 0.9$（即 `momentum=0.1`，注意 PyTorch 的 `momentum` 参数对应 $(1-\alpha)$）。

> **为什么测试时不能用 mini-batch 统计量？**
> 推理时可能只有 1 张图（batch_size=1），无法计算有意义的均值和方差；更重要的是，测试时的统计量应反映**整个训练集的全局分布**，而非某个随机 mini-batch 的局部波动。

### 5.4 符号说明表

| 符号 | 含义 | 维度/量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $m$ | mini-batch 大小 | 标量 | 通常 32/64/128 |
| $x_i$ | 第 $i$ 个样本的激活值（某个神经元） | 标量 | 在 CNN 中，BN 按通道独立计算 |
| $\mu_\mathcal{B}$ | mini-batch 均值 | 标量 | $\frac{1}{m}\sum x_i$ |
| $\sigma_\mathcal{B}^2$ | mini-batch 方差 | 标量 | 有偏估计（分母 $m$，非 $m-1$） |
| $\hat{x}_i$ | 标准化后的值 | 标量 | 均值 0、方差 1 |
| $\gamma$ | 可学习缩放参数 | 标量（每通道） | 初始化为 1 |
| $\beta$ | 可学习平移参数 | 标量（每通道） | 初始化为 0 |
| $y_i$ | BN 最终输出 | 标量 | $\gamma \hat{x}_i + \beta$ |
| $\epsilon$ | 数值稳定常数 | $10^{-5}$ | 防止 $\sqrt{\cdot}$ 梯度爆炸 |

---

## 6. 推导思路和思想来源

### 6.1 从 Internal Covariate Shift 到 BN

- **最初困难**：训练深层网络时，前面层参数的微小变化经过多层非线性放大，导致后面层的输入分布剧烈漂移（ICS）。如果使用较大的学习率，这种漂移会使训练发散；使用小学习率则收敛极慢。
- **关键转念**：Ioffe 和 Szegedy 意识到——既然输入数据的白化（whitening）对传统机器学习有益，为什么不把白化嵌入到网络内部，作为每一层或每几层之后的"标准化步骤"？但全数据集的白化计算量过大且不可微，于是提出**在 mini-batch 维度上做近似白化**——这就是 BN 的核心洞见！
- **为什么必须加回 $\gamma$ 和 $\beta$**：如果只是简单地把每层输出强行归一化到均值 0 方差 1，会严重限制网络的表达能力。例如，Sigmoid 激活函数在 0 附近近似线性，但完全失去其非线性饱和区的表达能力。$\gamma$ 和 $\beta$ 恢复了网络的表达能力——让梯度下降自行决定每一层最优的激活值分布。

### 6.2 BN 反向传播梯度推导

> 这是面试高频手推题！以下给出完整链式推导。

设损失函数为 $\mathcal{L}$，已知上游梯度 $\frac{\partial \mathcal{L}}{\partial y_i}$，求 $\frac{\partial \mathcal{L}}{\partial x_i}$、$\frac{\partial \mathcal{L}}{\partial \gamma}$、$\frac{\partial \mathcal{L}}{\partial \beta}$。

**Step 1：$\gamma$ 和 $\beta$ 的梯度**

$$\frac{\partial \mathcal{L}}{\partial \beta} = \sum_{i=1}^{m} \frac{\partial \mathcal{L}}{\partial y_i}$$

$$\frac{\partial \mathcal{L}}{\partial \gamma} = \sum_{i=1}^{m} \frac{\partial \mathcal{L}}{\partial y_i} \cdot \hat{x}_i$$

**Step 2：$\hat{x}_i$ 的梯度**

$$\frac{\partial \mathcal{L}}{\partial \hat{x}_i} = \frac{\partial \mathcal{L}}{\partial y_i} \cdot \gamma$$

**Step 3：$\sigma_\mathcal{B}^2$ 和 $\mu_\mathcal{B}$ 的梯度**（关键步骤，$\hat{x}_i$ 同时依赖 $\mu_\mathcal{B}$ 和 $\sigma_\mathcal{B}^2$）

$$\frac{\partial \mathcal{L}}{\partial \sigma_\mathcal{B}^2} = \sum_{i=1}^{m} \frac{\partial \mathcal{L}}{\partial \hat{x}_i} \cdot (x_i - \mu_\mathcal{B}) \cdot \left(-\frac{1}{2}\right) \cdot (\sigma_\mathcal{B}^2 + \epsilon)^{-3/2}$$

$$\frac{\partial \mathcal{L}}{\partial \mu_\mathcal{B}} = \sum_{i=1}^{m} \frac{\partial \mathcal{L}}{\partial \hat{x}_i} \cdot \frac{-1}{\sqrt{\sigma_\mathcal{B}^2 + \epsilon}} + \frac{\partial \mathcal{L}}{\partial \sigma_\mathcal{B}^2} \cdot \frac{\sum_{i=1}^{m} -2(x_i - \mu_\mathcal{B})}{m}$$

**Step 4：$x_i$ 的梯度**（三个贡献项之和）

$$\frac{\partial \mathcal{L}}{\partial x_i} = \frac{\partial \mathcal{L}}{\partial \hat{x}_i} \cdot \frac{1}{\sqrt{\sigma_\mathcal{B}^2 + \epsilon}} + \frac{\partial \mathcal{L}}{\partial \sigma_\mathcal{B}^2} \cdot \frac{2(x_i - \mu_\mathcal{B})}{m} + \frac{\partial \mathcal{L}}{\partial \mu_\mathcal{B}} \cdot \frac{1}{m}$$

> **直观理解**：$x_i$ 的梯度有三条路径 —— ① 通过 $\hat{x}_i$ 直接影响输出；② 通过影响 $\sigma_\mathcal{B}^2$ 间接影响所有样本的标准化；③ 通过影响 $\mu_\mathcal{B}$ 间接影响所有样本。这体现了 BN 的"全局依赖"特性：每个样本的梯度不仅取决于自己，还依赖于同一 batch 内所有其他样本。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础 — 手算一个小 batch 的 BN 前向传播

假设一个 mini-batch 包含 4 个样本，某个神经元的激活值为：

$$x = [1.0, 3.0, 5.0, 7.0]$$

给定 $\gamma = 2.0$，$\beta = 1.0$，$\epsilon = 0$（简化）。

**Step 1：均值**
$$\mu_\mathcal{B} = \frac{1.0 + 3.0 + 5.0 + 7.0}{4} = 4.0$$

**Step 2：方差**
$$\sigma_\mathcal{B}^2 = \frac{(1-4)^2 + (3-4)^2 + (5-4)^2 + (7-4)^2}{4} = \frac{9 + 1 + 1 + 9}{4} = 5.0$$

**Step 3：标准化**
$$\hat{x} = \left[\frac{1-4}{\sqrt{5}}, \frac{3-4}{\sqrt{5}}, \frac{5-4}{\sqrt{5}}, \frac{7-4}{\sqrt{5}}\right] \approx [-1.3416, -0.4472, 0.4472, 1.3416]$$

验证：$\mu_{\hat{x}} = 0$、$\sigma_{\hat{x}}^2 = 1$ ✓

**Step 4：缩放平移**
$$y = 2.0 \times \hat{x} + 1.0 \approx [-1.683, 0.106, 1.894, 3.683]$$

验证：$\mu_y = 1.0 = \beta$、$\sigma_y^2 = 4.0 = \gamma^2$ ✓

---

### 例子 2：中等 — CNN 中的 BN 维度处理

在卷积神经网络中，BN 按**通道 (channel)** 独立计算。设输入特征图为 $(N, C, H, W) = (2, 3, 4, 4)$：

- 对于通道 $c$，BN 在该通道上所有 $N \times H \times W = 2 \times 4 \times 4 = 32$ 个数值上计算 $\mu_c$ 和 $\sigma_c^2$。
- 每个通道有独立的 $\gamma_c$ 和 $\beta_c$（共 $3$ 对参数）。
- 标准化时，通道 $c$ 的所有 32 个值共享同一组 $(\mu_c, \sigma_c^2, \gamma_c, \beta_c)$。

```python
import torch
import torch.nn as nn

# 模拟 CNN 中的 BN
bn = nn.BatchNorm2d(num_features=3)  # 3 个通道
x = torch.randn(2, 3, 4, 4)          # (N, C, H, W)

y = bn(x)  # 训练模式下的前向传播

print("输入形状:", x.shape)       # [2, 3, 4, 4]
print("输出形状:", y.shape)       # [2, 3, 4, 4]
print("γ 形状:", bn.weight.shape)  # [3]  — 每通道一个
print("β 形状:", bn.bias.shape)    # [3]  — 每通道一个
print("running_mean:", bn.running_mean)  # [3]  — 推理时使用
print("running_var: ", bn.running_var)   # [3]
```

### 例子 3：实际应用 — 完整训练管线中的 BN

```python
import torch
import torch.nn as nn
import torch.optim as optim

# === 定义一个使用 BN 的小型 CNN ===
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(32),          # BN 放在 Conv 之后、激活之前
            nn.ReLU(inplace=True),

            nn.Conv2d(32, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),

            nn.AdaptiveAvgPool2d(1)
        )
        self.classifier = nn.Linear(64, num_classes)

    def forward(self, x):
        feat = self.features(x)
        feat = feat.view(feat.size(0), -1)
        return self.classifier(feat)

model = SimpleCNN()

# === 训练模式 ===
model.train()
x_train = torch.randn(16, 3, 32, 32)
out_train = model(x_train)
print(f"训练模式输出: {out_train.shape}")  # [16, 10]
print(f"训练中 running_mean 在变化: {model.features[1].running_mean[:3]}")

# === 切换到推理模式 ===
model.eval()
with torch.no_grad():
    x_test = torch.randn(1, 3, 32, 32)    # batch_size=1 也没问题！
    out_test = model(x_test)
    print(f"推理模式输出: {out_test.shape}") # [1, 10]

# === 关键提醒：BN 会改变模型行为 ===
# 训练时：model.train() → BN 用 batch 统计量 + 更新 running stats
# 推理时：model.eval()   → BN 用 running stats（冻结）
# 忘记切换模式是新手最常见的 bug！
```

---

## 8. 常见误区和易混概念

### 误区 1：BN 能"完全消除"Internal Covariate Shift

- **错误直觉**："加了 BN 之后，每一层的输入分布就完全固定了。"
- **为什么错**：MIT 2018 年的一项研究（Santurkar et al.）表明，BN 的真正威力**可能不主要来自消除 ICS**，而更来自于它使损失景观（loss landscape）变得更加平滑——梯度更稳定、Lipschitz 常数更小，从而允许更大的学习率。实际上，BN 之后重新注入噪声的实验显示，即使存在 ICS，BN 依然有效。
- **正确理解**：BN 通过"重新参数化"平滑了优化地形，ICS 的消除是附带收益而非唯一机制。

### 误区 2：测试时继续用 batch 统计量就行

- **错误直觉**："测试集也有 batch，直接用测试 batch 的均值和方差就行了。"
- **为什么错**：推理场景可能是 batch_size=1（在线服务），单个样本的方差为 0，除以 0 会崩溃；更重要的是，推理需要**确定性输出**——同一个样本无论放在哪个 batch 里，结果应该一致。使用训练集全局统计量保证了这个确定性。
- **正确做法**：`model.eval()` 后，PyTorch 自动切换为 `running_mean` / `running_var`。

### 误区 3：BN 层放在激活函数之后

- **错误直觉**："先激活再归一化，让激活值更稳定。"
- **为什么错**：原始论文和大量实验表明，**Conv → BN → ReLU** 的顺序效果最好。原因在于：卷积输出通常近似对称分布，在此处标准化效果最佳；而 ReLU 之后的激活值是非负的、稀疏的，分布已经严重偏斜，标准化收益有限。但实践中也有"ReLU → BN"的变体工作（如某些 ResNet 变体），并非绝对禁忌。
- **推荐顺序**：`Conv → BatchNorm → Activation`

### 概念对比表

| 归一化方法 | 归一化维度 | 依赖 batch size？ | 适用场景 | 典型应用 |
| :--- | :--- | :--- | :--- | :--- |
| **Batch Norm** | $(N, H, W)$ 每个通道 | ✅ 强依赖 | 大 batch 的 CV 任务 | ResNet, VGG, GAN |
| **Layer Norm** | $(C, H, W)$ 每个样本 | ❌ 不依赖 | NLP / Transformer | GPT, BERT, LLaMA |
| **Instance Norm** | $(H, W)$ 每个样本每个通道 | ❌ 不依赖 | 风格迁移 | StyleGAN, Pix2Pix |
| **Group Norm** | $(G, H, W)$ 通道分组 | ❌ 不依赖 | 小 batch CV / 分割 | Mask R-CNN, video models |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[前向传播]]：BN 插在层与层之间，理解激活值的流动。
- [[反向传播与计算图|反向传播与链式法则]]：BN 梯度的三路径推导依赖扎实的链式法则功底。
- [[数据增强与正则化|权重正则化]]：BN 自带轻微正则化效果（batch 内噪声），有时可减少 Dropout。

### 下游延伸
- [[🎯 ResNet (残差网络)|ResNet]]：BN + 残差连接共同保障深层梯度流动。
- LayerNorm：Transformer 的自注意力机制中替代 BN 的归一化方案。

### 横向关联
- InstanceNorm ↔ GroupNorm：BN 家族的不同归一化维度选择。
- [[学习率调度策略|学习率调度]]：BN 允许使用更大的初始学习率，但配合学习率衰减效果更佳。
- [[梯度流问题]]：BN 通过对激活值重新缩放，间接稳定了梯度范数。

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话解释 Internal Covariate Shift 是什么。
- [ ] 2. 默写 BN 前向传播的四步公式（$\mu_\mathcal{B}$, $\sigma_\mathcal{B}^2$, $\hat{x}_i$, $y_i$）。
- [ ] 3. 解释 $\gamma$ 和 $\beta$ 为什么不可或缺。
- [ ] 4. 说明训练模式和测试模式的关键差异，及 `running_mean` 的更新公式。
- [ ] 5. 手推 $\frac{\partial \mathcal{L}}{\partial x_i}$ 的三条梯度路径。
- [ ] 6. 解释为什么 BN 在 batch_size 很小时效果变差。
- [ ] 7. 对比 BatchNorm、LayerNorm、InstanceNorm、GroupNorm 的归一化维度。
- [ ] 8. 说出 CNN 中 BN 的推荐插入位置（Conv → BN → ReLU）。
- [ ] 9. 手写 PyTorch 中带 BN 的 CNN 训练/推理切换代码。
- [ ] 10. 说出 BN 为什么自带轻微正则化效果。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | Internal Covariate Shift 的定义 |
| 2 | 模式判断 | 基础 | 训练/测试模式下的 BN 行为差异 |
| 3 | 公式推导 | 中等 | BN 反向传播中 $\partial \mathcal{L} / \partial \gamma$ 的推导 |
| 4 | 维度对比 | 中等 | BatchNorm vs LayerNorm 的归一化维度 |
| 5 | 实践问题 | 较难 | 小 batch size 场景下的归一化策略选择 |

### 题目与解析

#### 1. 关于 Internal Covariate Shift (ICS)，以下说法正确的是？
- A. ICS 指测试集和训练集的分布不一致
- B. ICS 指网络中同一层的输入分布随前层参数更新而不断漂移
- C. ICS 只能通过减小学习率来解决
- D. BN 消除 ICS 是其加速训练的唯一原因

> [!question]- 答案解析
> - **答案**：B
> - **解析**：ICS 描述的是训练过程中，由于前面层参数更新，后面层的输入分布不断变化的现象。A 描述的是 dataset shift / covariate shift（数据集层面），不是内部（internal）的。C 错误，BN 是主要解决方案。D 错误，BN 的作用机制不仅限于消除 ICS，还包括平滑优化地形。
> - **对应章节**：§1。

#### 2. `model.eval()` 对 BatchNorm 层的行为产生什么影响？
- A. BN 层的 $\gamma$ 和 $\beta$ 被冻结
- B. BN 层改用训练期间累积的 `running_mean` 和 `running_var`
- C. BN 层完全跳过，不做任何归一化
- D. BN 层继续使用当前 batch 的统计量，但不更新 running stats

> [!question]- 答案解析
> - **答案**：B
> - **解析**：`model.eval()` 让 BN 层切换到推理模式，使用 EMA 累积的全局均值/方差。A 是混淆项——$\gamma$ 和 $\beta$ 在训练完成后本来就是固定的（不再接收梯度），但冻结它们不是 `eval()` 的行为。C 错误，BN 不能跳过。D 描述的是训练时的行为。
> - **对应章节**：§5.3。

#### 3. 【推导】给定 $\frac{\partial \mathcal{L}}{\partial y_i}$，写出 $\frac{\partial \mathcal{L}}{\partial \gamma}$ 的表达式。
> [!question]- 答案解析
> - **答案**：$\frac{\partial \mathcal{L}}{\partial \gamma} = \sum_{i=1}^{m} \frac{\partial \mathcal{L}}{\partial y_i} \cdot \hat{x}_i$
> - **解析**：因为 $y_i = \gamma \hat{x}_i + \beta$，所以 $\frac{\partial y_i}{\partial \gamma} = \hat{x}_i$，链式法则得 $\frac{\partial \mathcal{L}}{\partial \gamma} = \sum_i \frac{\partial \mathcal{L}}{\partial y_i} \frac{\partial y_i}{\partial \gamma} = \sum_i \frac{\partial \mathcal{L}}{\partial y_i} \hat{x}_i$。注意这里是求和，因为 $\gamma$ 被 batch 内所有样本共享。
> - **对应章节**：§6.2。

#### 4. 对于输入张量 $(N, C, H, W)$，LayerNorm 在哪些维度上计算均值和方差？
- A. 在 $(N, H, W)$ 维度
- B. 在 $(C, H, W)$ 维度
- C. 在 $(N, C)$ 维度
- D. 在 $(H, W)$ 维度

> [!question]- 答案解析
> - **答案**：B
> - **解析**：LayerNorm 对每个样本独立做归一化，在 $(C, H, W)$ 维度上计算均值和方差。BN 在 $(N, H, W)$ 维度（每个通道）。IN 在 $(H, W)$ 维度（每个样本每个通道）。GN 把通道分成 G 组，在 $(G, H, W)$ 维度。
> - **对应章节**：§8 概念对比表。

#### 5. 【实践】目标检测任务中 batch_size 只能设为 2（显存限制），BN 训练不稳定。以下哪项是最合理的替代方案？
- A. 强行把 batch_size 调到 32，使用梯度累积
- B. 用 GroupNorm（GN）替换 BN
- C. 去掉所有归一化层，靠权重初始化保证训练
- D. 把 $\epsilon$ 增大到 0.1

> [!question]- 答案解析
> - **答案**：B
> - **解析**：BN 在小 batch 下统计量不稳定（均值和方差噪声极大），训练效果差甚至发散。GroupNorm 不依赖 batch 维度，天然适合小 batch 场景（如分割、检测的高分辨率输入）。A 可能受显存限制不可行；C 在现代深层网络中几乎不可能成功训练；D 治标不治本，且过大的 $\epsilon$ 会破坏归一化效果。
> - **对应章节**：§8 概念对比表。

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

- **归档目录**：`02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/`
- **建议双链**：
  - [[🧠 第二阶段：深度学习内核|第二阶段：深度学习内核]]
  - [[🎯 ResNet (残差网络)|ResNet残差网络]]
  - LayerNorm
  - GroupNorm
  - [[梯度流问题]]
  - [[数据增强与正则化|权重正则化]]
- **建议标签**：`#学习` `#深度学习` `#计算机视觉` `#BatchNorm` `#批归一化` `#训练优化` `#归一化层`

---
---

## 学完后可以完成

- [[05-计算机视觉-课后作业-03-小型CNN与训练工程|HW03]]：单因素对照 BatchNorm 效果

> 作业入口由 frontmatter `requires` 维护（唯一事实源），下方 Dataview 反向派生当前卡可完成的全部作业。
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
