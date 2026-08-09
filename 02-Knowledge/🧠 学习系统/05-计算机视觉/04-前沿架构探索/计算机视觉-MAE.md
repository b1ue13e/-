---
type: study
course: "05-计算机视觉"
topic: "MAE 掩码自编码器 (Masked Autoencoder)"
created: 2026-08-06
status: ongoing
difficulty: advanced
concept: ["MAE", "掩码自编码器", "自监督学习", "ViT", "预训练"]
prerequisites: ["ViT", "自监督学习SimCLR与CLIP"]
related: ["BEiT", "iBOT", "SimCLR"]
upstream: ["[[计算机视觉-ViT]]"]
flow: knowledge
stage_moc: "[[🧭 阶段4-前沿架构探索]]"
kind: concept
source: "He et al. 2022 'Masked Autoencoders Are Scalable Vision Learners'"
tags: [学习, 计算机视觉, MAE, 自监督, ViT]
---

# MAE 掩码自编码器 (Masked Autoencoder)

> 所属模块：[[🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[🧭 阶段4-前沿架构探索|第四阶段]]
> 建议先看：[[计算机视觉-ViT]]、[[自监督学习SimCLR与CLIP]]

---

## 0. 类别：A 类核心概念

MAE 是 Kaiming He (ResNet 作者) 提出的 ViT 自监督预训练方法。核心思想极其简单：**随机遮住 75% 的图像 patch，让模型从可见的 25% 重建整张图**。

---

## 1. 直觉：看图猜谜

遮住一只猫 75% 的身体，你能猜出它是猫吗？能——因为有足够的上下文线索（耳朵尖、毛色、背景）。

MAE 让 ViT 做同样的事：遮掉大部分 patch → 编码器只看可见 patch → 解码器重建所有 patch → 用重建误差训练。**这让 ViT 学到图像的高级语义表示**，无需人工标注。

---

## 2. 架构

```
输入图像 (75% patch 被遮)
    ↓
编码器 (ViT)：仅处理可见的 25% patch → 大幅节省计算
    ↓
解码器 (轻量 Transformer)：接收编码特征 + 被遮 patch 的占位符
    ↓
输出：重建完整图像（逐像素 MSE Loss）
```

**关键设计**：
- **非对称架构**：编码器重（ViT-Large），解码器轻（8层小型Transformer）
- **高掩码率 75%**：迫使模型学习全局语义（只看 25% 的 patch 必须理解整体结构）
- **编码器不处理被遮 patch**：省计算（训练快 3×+）

---

## 3. 为什么 75% 掩码率是关键？

| 掩码率 | 效果 | 原因 |
|:---|:---|:---|
| 50% | 下游性能较差 | 任务太简单，模型可以"插值"而非"理解" |
| **75%** | **最优** | 迫使学习全局语义，训练加速 3× |
| 90% | 性能下降 | 可见信息太少，重建太难 |

> **交错练习**：回顾 [[自监督学习SimCLR与CLIP|SimCLR 对比学习]]。SimCLR 通过"同一图像的不同增强应相似"来学习。MAE 通过"从部分重建整体"来学习。两种完全不同的自监督范式。

---

## 4. 与 BERT 的关系

MAE 是 NLP 中 **BERT 的视觉版**：
- BERT：遮住 15% 的单词 → 预测被遮单词
- MAE：遮住 75% 的 patch → 重建被遮 patch
- 区别：图像信息密度远低于文本（图像有大量冗余），所以掩码率可以更高（75% vs 15%）

---

## 5. 代码理念

```python
# MAE 前向传播的简化逻辑
def mae_forward(imgs, mask_ratio=0.75):
    N, L = patches.shape[0], patches.shape[1]  # L = 196 patches
    
    # 随机选择 25% 的 patch 保留
    ids_keep = random.sample(range(L), int(L * (1 - mask_ratio)))
    ids_mask = [i for i in range(L) if i not in ids_keep]
    
    # 编码：仅处理可见 patch
    visible = patches[:, ids_keep]      # (N, 49, 768)
    encoded = vit_encoder(visible)      # 仅 49 个 token，快！
    
    # 解码：重建所有 patch
    all_tokens = merge(encoded, mask_tokens, ids_keep, ids_mask)
    reconstructed = light_decoder(all_tokens)  # (N, 196, 768)
    
    # Loss：仅在被遮 patch 上计算 MSE
    loss = mse_loss(reconstructed[:, ids_mask], original_patches[:, ids_mask])
    return loss
```

---

## 5.5 BEiT 与 iBOT：掩码预训练的另两条路线

MAE 用"像素回归"重建被掩 patch；**BEiT**（Bao et al., 2021）与 **iBOT**（Zhou et al., 2021）走"离散 token 预测"路线，与 BERT 的 masked language modeling 更接近：

- **BEiT**：先用一个预训练好的 **dVAE**（离散 VAE，如 8192 个码字）把每个 patch 编码为离散 token；预训练时遮住 patch，用 ViT 预测其 dVAE token——分类任务（判别式重建）而非回归；
- **iBOT**：把 BEiT 的 tokenizer 换成**在线自蒸馏**（教师网络产生 token 软标签），并加入 [CLS] token 的全局对比损失，同时做 patch 级与图像级自监督，在 ImageNet 线性探针与微调上刷新 SOTA；
- **共同点**：用**离散表示**作为预测目标 → 学到的特征更适合下游判别任务；而 MAE 的像素回归目标信息密度低，特征偏向低频结构。

**选择**：MAE 实现简单、易复现（无需 tokenizer）；BEiT/iBOT 特征质量更高但依赖额外 tokenizer/教师网络，工程复杂度高。

## 6. 常见误区

- ❌ "MAE 和 Autoencoder 一样" — 传统 AE 压缩再解压；MAE 是掩码预测（更像 BERT）
- ❌ "掩码率越高越好" — 75% 是最优点，90% 性能下降
- ❌ "MAE 只能在 ViT 上用" — 原理上也可用于 CNN，但 ViT 的非局部性更适合

---

## 🧪 自测题

1. **(基础)** MAE 的典型掩码率是多少？为什么这么高？
   <details><summary>💡 思路</summary>从「任务难度」角度想：图像相邻像素高度冗余，掩码率低时模型能否靠邻域插值蒙混过关？再查论文实际采用的比例。</details>

2. **(中等)** MAE 的编码器为什么不处理被遮住的 patch？
   <details><summary>💡 思路</summary>数一数若编码器跳过被遮 token，参与计算的序列长度会缩短多少；再想被遮 token 本身携带多少信息、重建工作该由哪个模块承担。</details>

3. **(较难)** MAE 和 SimCLR 作为两种自监督范式，哪种更适合下游密集预测任务（检测/分割）？为什么？
   <details><summary>💡 思路</summary>先分别问：MAE 的预训练任务要求模型输出什么粒度的信息？SimCLR 的对比目标又是在什么粒度上做区分（整图还是局部）？再想检测/分割需要的是哪种粒度的表征，据此判断并说明理由。</details>

---

## 🔀 学完本节后的横向连接

- 配合 [[计算机视觉-ViT]] 理解为什么 MAE 特别适合 ViT 预训练
---

## 学完后可以完成

> 下列作业在 `requires` 中引用了本卡，由 Dataview 实时派生（非人工维护反向链接）：

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

本卡另以前置「🧪 自测题」与闭卷复现作为形成性验收。

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
