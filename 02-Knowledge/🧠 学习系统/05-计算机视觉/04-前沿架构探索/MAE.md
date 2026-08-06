---
type: study
course: "05-计算机视觉"
topic: "MAE 掩码自编码器 (Masked Autoencoder)"
created: 2026-08-06
status: planned
difficulty: advanced
concept: ["MAE", "掩码自编码器", "自监督学习", "ViT", "预训练"]
prerequisites: ["ViT", "自监督学习SimCLR与CLIP"]
related: ["BEiT", "iBOT", "SimCLR"]
upstream: ["[[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/ViT]]"]
flow: knowledge
stage_moc: "[[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🚀 第四阶段：前沿架构探索]]"
kind: concept
source: "He et al. 2022 'Masked Autoencoders Are Scalable Vision Learners'"
tags: [学习, 计算机视觉, MAE, 自监督, ViT]
---

# MAE 掩码自编码器 (Masked Autoencoder)

> 所属模块：[[02-Knowledge/🧠 学习系统/05-计算机视觉/🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🚀 第四阶段：前沿架构探索|第四阶段]]
> 建议先看：[[ViT]]、[[自监督学习SimCLR与CLIP]]

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

> **交错练习**：回顾 [[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/自监督学习SimCLR与CLIP|SimCLR 对比学习]]。SimCLR 通过"同一图像的不同增强应相似"来学习。MAE 通过"从部分重建整体"来学习。两种完全不同的自监督范式。

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

## 6. 常见误区

- ❌ "MAE 和 Autoencoder 一样" — 传统 AE 压缩再解压；MAE 是掩码预测（更像 BERT）
- ❌ "掩码率越高越好" — 75% 是最优点，90% 性能下降
- ❌ "MAE 只能在 ViT 上用" — 原理上也可用于 CNN，但 ViT 的非局部性更适合

---

## 🧪 自测题

1. **(基础)** MAE 的典型掩码率是多少？为什么这么高？
   <details><summary>💡 提示</summary>75%。图像有大量空间冗余，低掩码率（如15%）太简单，模型只需"插值"邻域像素即可重建。</details>

2. **(中等)** MAE 的编码器为什么不处理被遮住的 patch？
   <details><summary>💡 提示</summary>省计算（处理 token 减少 75%）。被遮 patch 没有信息，处理它们是浪费。解码器才需要重建它们。</details>

3. **(较难)** MAE 和 SimCLR 作为两种自监督范式，哪种更适合下游密集预测任务（检测/分割）？为什么？
   <details><💡 提示</summary>MAE 更适合。MAE 迫使模型理解全局结构（从部分重建整体），学到的是空间语义；SimCLR 学到的是实例级判别特征。</details>

---

## 🧪 学完本节后可完成的作业

- 配合 [[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/ViT|ViT]] 理解为什么 MAE 特别适合 ViT 预训练
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
