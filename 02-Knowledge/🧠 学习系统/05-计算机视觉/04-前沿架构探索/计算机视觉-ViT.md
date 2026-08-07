---
type: study
course: "05-计算机视觉"
topic: "Vision Transformer (ViT)"
created: 2026-08-06
status: ongoing
difficulty: advanced
concept: ["ViT", "Vision Transformer", "图像分块", "位置编码", "自注意力"]
prerequisites: ["Transformer与自注意力", "卷积神经网络CNN"]
related: ["SwinTransformer", "MAE", "DeiT", "CLIP"]
upstream: ["[[Transformer与自注意力]]"]
flow: knowledge
stage_moc: "[[🧭 阶段4-前沿架构探索]]"
kind: concept
source: "Dosovitskiy et al. 2021 'An Image is Worth 16x16 Words'; D2L Ch.11"
tags: [学习, 计算机视觉, ViT, Transformer, 前沿架构]
---

# Vision Transformer (ViT)

> 所属模块：[[🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[🧭 阶段4-前沿架构探索|第四阶段]]
> 建议先看：[[Transformer与自注意力]]、[[卷积神经网络CNN]]

---

## 0. 类别：A 类核心概念

ViT 是 2020 年颠覆 CV 的里程碑：**"把图像当作文本序列，直接用 Transformer 处理"**。它终结了 CNN 在视觉领域十年的统治地位。

---

## 1. 直觉：图像 = 16×16 的"单词"

CNN 逐像素滑窗提取特征。ViT 说：**不需要**。把图像切成固定大小的小块 (patch)，每个 patch 当作一个"单词"，扔进标准 Transformer 编码器。

```
图像 (224×224×3)
  → 切成 14×14=196 个 16×16 patch
  → 每个 patch 展平为 768 维向量（线性投影）
  → 加上位置编码（CLS token + 可学习的位置嵌入）
  → 送入标准 Transformer 编码器（12层）
  → CLS token 输出 → 分类头
```

---

## 2. 架构详解

### 2.1 Patch Embedding

$$\mathbf{z}_0 = [\mathbf{x}_{\text{class}}; \mathbf{x}_p^1\mathbf{E}; \mathbf{x}_p^2\mathbf{E}; \ldots; \mathbf{x}_p^N\mathbf{E}] + \mathbf{E}_{\text{pos}}$$

| 符号 | 含义 | 形状 |
|:---|:---|:---|
| $\mathbf{x}_p^i$ | 第 i 个 patch（展平） | $1 \times (P^2 \cdot C)$ |
| $\mathbf{E}$ | 线性投影矩阵 | $(P^2 \cdot C) \times D$ |
| $\mathbf{x}_{\text{class}}$ | 可学习的 CLS token | $1 \times D$ |
| $\mathbf{E}_{\text{pos}}$ | 位置嵌入 | $(N+1) \times D$ |
| $D$ | Transformer 隐藏维度 | ViT-Base: 768 |

**CLS token**：借鉴 BERT，在序列头部添加一个特殊的可学习 token。经过 Transformer 后，其输出作为整张图的表示用于分类。

### 2.2 Transformer 编码器

标准的多层 Transformer（与 NLP 完全相同，**无任何修改**）：

$$\mathbf{z}'_\ell = \text{MSA}(\text{LN}(\mathbf{z}_{\ell-1})) + \mathbf{z}_{\ell-1}$$
$$\mathbf{z}_\ell = \text{MLP}(\text{LN}(\mathbf{z}'_\ell)) + \mathbf{z}'_\ell$$

> ViT 最优雅的地方：**Transformer 架构零改动**。NLP 的 Transformer 直接拿来处理图像。

---

## 3. ViT vs CNN：归纳偏置的对比

| 特性 | CNN | ViT |
|:---|:---|:---|
| **局部性** | 天然（卷积核只看邻域） | 需要大量数据学习 |
| **平移等变性** | 天然（卷积共享权重） | 需位置编码补偿 |
| **全局感受野** | 需深层堆叠 | 第一层就是全局的（自注意力） |
| **数据效率** | 高（强归纳偏置） | 低（弱归纳偏置，需大数据） |
| **预训练需求** | 中等 | **极强**（ImageNet-21K → 才能发挥） |

> **核心矛盾**：CNN 的局部性 + 平移等变性是"先天赋予"的归纳偏置 → 小数据也能学好。ViT 没有这些偏置 → 需要海量数据才能从零学到这些规律。

---

## 4. ViT 的三种规模

| 模型 | 层数 | 隐藏维度 | MLP 维度 | 头数 | 参数量 |
|:---|:---:|:---:|:---:|:---:|:---:|
| ViT-Base | 12 | 768 | 3072 | 12 | 86M |
| ViT-Large | 24 | 1024 | 4096 | 16 | 307M |
| ViT-Huge | 32 | 1280 | 5120 | 16 | 632M |

---

## 5. 代码示例：ViT 的 Patch Embedding

```python
import torch
import torch.nn as nn

class PatchEmbedding(nn.Module):
    """将图像切成 patch 并线性投影"""
    def __init__(self, img_size=224, patch_size=16, in_chans=3, embed_dim=768):
        super().__init__()
        self.n_patches = (img_size // patch_size) ** 2  # 196
        self.proj = nn.Conv2d(in_chans, embed_dim, 
                              kernel_size=patch_size, stride=patch_size)
    
    def forward(self, x):
        # x: (B, 3, 224, 224) → (B, 768, 14, 14)
        x = self.proj(x)
        # → (B, 768, 196) → (B, 196, 768)
        x = x.flatten(2).transpose(1, 2)
        return x

# 验证
patch_embed = PatchEmbedding()
x = torch.randn(4, 3, 224, 224)           # batch=4
tokens = patch_embed(x)
print(f"Tokens shape: {tokens.shape}")     # (4, 196, 768) — 196个"单词"
```

---

## 6. 何时用 ViT？何时用 CNN？

| 场景 | 推荐 | 原因 |
|:---|:---|:---|
| 大数据（>1M 样本） | **ViT** | ViT 的弱归纳偏置在大数据下变优势（更灵活） |
| 小数据（<100K 样本） | **CNN/ResNet** | CNN 的强归纳偏置防止过拟合 |
| 需要密集预测（检测/分割） | **Swin/Hierarchical ViT** | 标准 ViT 输出单尺度特征，不适合密集预测 |
| 推理速度敏感 | **CNN** | ViT 的自注意力 $O(N^2)$ 复杂度（$N$=patch数） |

---

## 7. 与 CNN 的交错练习

> **回顾** [[感受野]]：CNN 第1层感受野=3×3，需要堆叠深度才能覆盖大物体。ViT 第1层通过自注意力直接拥有**全局感受野**——每个 patch 在第一层就能"看到"所有其他 patch。

> **回顾** [[卷积神经网络CNN|CNN]] vs ViT：两者都在学习"从像素提取特征"。CNN 用局部卷积核（局部归纳偏置），ViT 用全局自注意力（弱归纳偏置）。在小数据集上训练时，CNN 通常更优；在大数据集上，ViT 超越 CNN。

---

## 8. 常见误区

- ❌ "ViT 已经完全取代 CNN" — 小数据/密集预测场景 CNN 仍占优势
- ❌ "ViT 和 NLP Transformer 架构不同" — 完全相同，ViT 最优雅之处就是架构零修改
- ❌ "patch 越大越好" — 大 patch 降低序列长度但丢失细粒度信息；16×16 是经验最优

---

## 🧪 自测题

1. **(基础)** ViT 把 224×224 图像切成 16×16 patch 后，序列长度是多少？
   <details><summary>💡 提示</summary>224/16 = 14，14×14 = 196 个 patch。加上 CLS token 共 197 个 token。</details>

2. **(中等)** ViT 在小数据集上不如 CNN，根本原因是什么？
   <details><summary>💡 提示</summary>CNN 的卷积操作自带局部性和平移等变性（强归纳偏置），小数据即可学。ViT 的自注意力无此偏置，需要海量数据才能从零学到局部模式。</details>

3. **(较难)** ViT 的位置编码为什么是"可学习的"而非固定的（如 NLP 中的正弦位置编码）？两者有什么区别？
   <details><summary>💡 提示</summary>图像 patch 之间的空间关系不像文本那样严格有序。可学习的位置编码允许模型自行发现"上下左右"的 2D 空间关系。实验表明 1D 可学习位置编码对图像同样有效。</details>

---

## 🧪 学完本节后可完成的作业

- 配合 [[计算机视觉-SwinTransformer]] 理解层次化 ViT 的设计动机
- 配合 [[计算机视觉-MAE]] 理解 ViT 的自监督预训练范式
---

## 学完后可以完成

- 可作为 HW06 开放项目『ViT 小样本/微调实验』选题

> 该卡无直接课后/阶段作业：以卡内自测题与闭卷复现作为形成性验收；如需综合实践，可挂靠 HW06 开放课程项目或 CAP01。

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
