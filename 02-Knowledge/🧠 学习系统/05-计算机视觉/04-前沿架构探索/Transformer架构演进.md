---
type: study
topic: "Transformer 架构演进（PVT/ConvNeXt/CoAtNet）"
course: "05-计算机视觉"
created: 2026-08-06
status: completed
difficulty: intermediate
concept: ["PVT", "ConvNeXt", "CoAtNet", "CNN-Transformer 融合", "金字塔结构"]
prerequisites: ["ViT", "Swin", "CNN 基础"]
related: ["Transformer与自注意力", "ViT", "SwinTransformer", "DeiT"]
upstream: ["[[ViT]]", "[[SwinTransformer]]", "[[卷积神经网络CNN]]"]
flow: knowledge
stage_moc: "[[🚀 第四阶段：前沿架构探索]]"
kind: concept
source: "PVT（Wang et al. 2021）；ConvNeXt（Liu et al. 2022）；CoAtNet（Dai et al. 2021）"
accessed: 2026-08-06
license: "论文公开可访问（arXiv），本地为原创教学说明"
tags: [学习, 计算机视觉, Transformer, 架构演进]
---

# Transformer 架构演进（PVT / ConvNeXt / CoAtNet）

## 0. 学习边界

**B 类专题（架构演进主线）**。ViT 证明了纯 Transformer 能做视觉，但"怎么把 Transformer 用得更高效、更适合密集预测"经历了三轮演进：**金字塔化**（PVT，处理多尺度）、**CNN 现代化**（ConvNeXt，反向证明卷积没死）、**融合**（CoAtNet，全局+局部结合）。本卡合并 MOC 中 PVT / CNN+Transformer / ConvNeXt / CoAtNet 四个规划项——它们是"视觉骨干演进"同一主题的四个节点。

## 1. 这个知识点解决什么问题？

- ViT 是固定分辨率、无多尺度的（像一个大网格），检测/分割需要**多尺度特征**（如 FPN）；
- ViT 的二次复杂度 $O(N^2)$ 限制了高分辨率输入；
- 纯 CNN 和纯 Transformer 各有短板：CNN 局部归纳偏置强但看不了全局，Transformer 全局强但缺归纳偏置、数据效率低。

## 2. 为什么它重要？它有什么用？

- 现代视觉骨干（backbone）几乎都在"卷积+注意力"谱系上做选择；
- PVT 是检测/分割任务的高效骨干（替代 ResNet 的常见选项）；
- ConvNeXt 证明"把 CNN 按 Transformer 的设计原则现代化"后两者性能相当——理解它避免"Transformer 绝对优于 CNN"的误解。

## 3. 学它之前需要哪些前置知识？

- ViT 与 Swin：[[ViT]]、[[SwinTransformer]]；
- 注意力：[[Transformer与自注意力]]；
- CNN 基础：[[卷积神经网络CNN]]。

## 4. 用直觉语言解释它

ViT 像一张"大网兜"——一次看全图，但格子固定、铺不开多尺度。PVT 把网兜改成**金字塔**：先粗后细地逐层缩小分辨率，同时保留多尺度——就像 CNN 的 ResNet 结构但内部换成注意力。ConvNeXt 走相反路线：把 ResNet 逐项改造（换 patchify、深度可分离卷积、更大的核、GELU、LayerNorm……）直到它长得像"没有注意力的 Swin"——结果性能追平 Swin。CoAtNet 则直接**分层混搭**：浅层用卷积（快、抓局部），深层用注意力（看全局），各取所长。

## 5. 正式定义、核心公式、符号解释

### 5.1 三种演进路线对比

| 路线 | 代表 | 核心设计 | 针对问题 |
|:---|:---|:---|:---|
| 金字塔化 | PVT | 4 阶段金字塔 + 空间缩减注意力（SRA） | ViT 无多尺度、复杂度高 |
| CNN 现代化 | ConvNeXt | 把 ResNet 改造成"类 Swin"的纯卷积 | 证明归纳偏置与设计的价值 |
| 卷积+注意力融合 | CoAtNet | 浅层卷积 + 深层注意力 + 相对位置编码 | 全局-局部权衡、数据效率 |

### 5.2 PVT 的空间缩减注意力（SRA）

把注意力中的 K、V 先做空间降采样再参与注意力，复杂度从 $O((HW)^2)$ 降为 $O((HW) \cdot (HW/R^2))$：

$$\text{SRA}(Q, K, V) = \text{Softmax}\left(\frac{Q K_r^\top}{\sqrt{d}}\right) V_r, \qquad K_r = \text{Reshape}(K, R),\; V_r = \text{Reshape}(V, R)$$

$R$ 是缩减率（每阶段不同）。配合 4 阶段金字塔（stride 4/8/16/32），直接对接 FPN 做密集预测。

### 5.3 ConvNeXt 的现代化配方（从 ResNet 到 ConvNeXt 的 7 步）

1. 训练策略现代化（AdamW、数据增强）；
2. 深度可分离卷积（depthwise conv，等价于"卷积版注意力"的 token mixing）；
3. 反瓶颈结构（通道先扩再缩，$3\times3 \to 1\times1 \times4 \to 1\times1$）；
4. 更大的卷积核（$7\times7$）；
5. 激活换 GELU、归一化换 LayerNorm；
6. 下采样分离（patchify stem + 独立 downsample 层）；
7. 精简各阶段块数（3-3-9-3）。

结论：**架构层面的设计原则（token mixing 与 channel mixing 分离）比"卷积 vs 注意力"本身更重要**。

### 5.4 CoAtNet：卷积 + 注意力的分层融合

网络分 5 个阶段：stem（卷积）+ 前两阶段用卷积块 + 后两阶段用注意力块，配合相对位置编码（将注意力变为"卷积+全局"的连续插值）：

$$\text{Attn} = \text{Softmax}\left(\frac{QK^\top}{\sqrt{d}} + \text{relative\_pos}\right)$$

关键洞察：**浅层适合卷积**（像素级局部信息、计算高效），**深层适合注意力**（语义级全局关联）——融合后数据效率与容量兼得。

## 6. 例子：基础 → 中等 → 实际应用

### 例子 1：基础——复杂度对比

```python
# 输入 224×224，patch 16 → 序列长度 N = 14×14 = 196
# ViT 全局注意力: O(N²) = O(196²) ≈ 3.8 万
# PVT SRA (R=8):   O(N · N/64) ≈ 600     （快 ~64 倍）
# ConvNeXt:        O(N · k²)（k=7）≈ 1 万   （局部，线性复杂度）
# 高分辨率 1024×1024 时 ViT 的 N 变 4096，N² 爆炸；PVT/ConvNeXt 依然可行
```

### 例子 2：中等——深度可分离卷积（ConvNeXt 的 token mixing）

```python
import torch
import torch.nn as nn

# depthwise conv = 每个通道独立空间混合（类似 attention 的 token 交互）
class DepthwiseSeparable(nn.Module):
    def __init__(self, dim, kernel_size=7):
        super().__init__()
        self.dw = nn.Conv2d(dim, dim, kernel_size, padding=kernel_size//2, groups=dim)
        self.pw = nn.Conv2d(dim, dim, 1)   # pointwise = 通道混合
    def forward(self, x):
        return self.pw(self.dw(x))         # 空间混合 → 通道混合

x = torch.randn(1, 96, 56, 56)
print(DepthwiseSeparable(96)(x).shape)     # (1, 96, 56, 56)，参数只有 96*7*7 + 96*96
```

### 例子 3：应用——骨干选型（检测/分割任务）

```python
# 伪代码：MMDetection 中 backbone 选择
# ResNet-50:  强基线，部署友好，Faster R-CNN 经典组合
# Swin-T:     ImageNet 预训练优势大，检测/分割 SOTA（多尺度窗口）
# PVT:        金字塔直接喂 FPN，训练快，适合高分辨率输入
# ConvNeXt:   若已有 ResNet 训练经验，现代化改造迁移成本低
# 选型依据：预训练可用性 > 推理硬件 > 任务多尺度需求
```

## 7. 常见误区和易混概念

| 误区 | 正确理解 |
|:---|:---|
| "Transformer 全面碾压 CNN" | ConvNeXt 证明现代化 CNN 性能相当；两者是设计空间的连续谱 |
| "PVT 就是 Swin" | PVT 用全局注意力+空间缩减，Swin 用窗口注意力+移动窗口，多尺度实现不同 |
| "ConvNeXt 是纯手工设计" | 它的每步改造都由明确的"对齐 Swin 设计原则"驱动 |
| "CoAtNet 浅层用注意力更好" | 浅层像素级注意力计算浪费且缺归纳偏置，卷积更合适 |
| "架构演进已经结束" | Mamba/混合架构仍活跃，但本卡三类范式至今是主干 |

## 8. 检索练习

1. ViT 用在检测任务上有哪两个主要困难？PVT 如何解决？#自测题/基础
2. depthwise conv 与 attention 的"token mixing"有何相似与不同？#自测题/中等
3. ConvNeXt 现代化的核心设计原则是什么？#自测题/中等
4. CoAtNet 为什么浅层用卷积、深层用注意力？#自测题/较难

## 9. 闭卷复现任务

1. 写出 SRA 的公式并说明 $R$ 的作用；
2. 画出 ConvNeXt 一个 block 的结构（depthwise → LayerNorm → pointwise）；
3. 用 PyTorch 实现 DepthwiseSeparable（例子 2）并验证输出形状与参数量；
4. 画一张"ResNet → ViT → Swin/PVT → ConvNeXt/CoAtNet"的演进时间线。

## 🔗 知识图谱

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

## 10. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

> 衔接：理解骨干选型后，可在 HW06 开放项目中对比 ResNet-50 与 Swin-T 作为 backbone 的检测/分割效果。

---

## 通过标准
- [ ] 能对比三条演进路线（金字塔/CNN 现代化/融合）的动机与代表
- [ ] 能写出 SRA 公式并解释复杂度收益
- [ ] 能说出 ConvNeXt 现代化的核心设计原则
- [ ] 能解释 CoAtNet 分层融合的理由

