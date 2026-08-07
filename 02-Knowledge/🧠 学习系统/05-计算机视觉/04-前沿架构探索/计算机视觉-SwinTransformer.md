---
type: study
course: "05-计算机视觉"
topic: "Swin Transformer"
created: 2026-08-06
status: ongoing
difficulty: advanced
concept: ["Swin Transformer", "窗口注意力", "层次化", "移位窗口", "多尺度"]
prerequisites: ["ViT", "Transformer与自注意力"]
related: ["FPN", "目标检测RCNN与YOLO", "语义分割与UNet"]
upstream: ["[[计算机视觉-ViT]]"]
flow: knowledge
stage_moc: "[[🧭 阶段4-前沿架构探索]]"
kind: concept
source: "Liu et al. 2021 'Swin Transformer: Hierarchical Vision Transformer using Shifted Windows'; ICCV 2021 Best Paper"
tags: [学习, 计算机视觉, Swin Transformer, ViT, 检测, 分割]
---

# Swin Transformer

> 所属模块：[[🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[🧭 阶段4-前沿架构探索|第四阶段]]
> 建议先看：[[计算机视觉-ViT]]、[[Transformer与自注意力]]

---

## 0. 类别：A 类核心概念

Swin Transformer (ICCV 2021 Best Paper) 解决了 ViT 的两大痛点：**计算复杂度**和**多尺度特征缺失**。它是第一个在检测/分割上全面超越 CNN 的纯 Transformer 架构。

---

## 1. 直觉：把注意力限制在窗口内，然后"移动"窗口

ViT 的问题：全局自注意力 → $O(N^2)$ 复杂度（$N$=patch数），224×224 图像有 196 个 patch 还能接受，但 800×1333 的检测输入有成千上万个 patch → 计算爆炸。

**Swin 的核心思想**：
1. **窗口注意力 (W-MSA)**：只在局部窗口内做自注意力（$7 \times 7$ 窗口），复杂度降为 $O(N)$
2. **移位窗口 (SW-MSA)**：相邻层之间窗口偏移 3 个像素，让信息跨窗口流动
3. **层次化结构**：像 CNN 一样逐步下采样（patch merging），产出多尺度特征

```
Stage 1: H/4 × W/4  (类似 CNN 的浅层高分辨率特征)
Stage 2: H/8 × W/8  (下采样)
Stage 3: H/16 × H/16
Stage 4: H/32 × W/32 (类似 CNN 的深层低分辨率特征)
```

---

## 2. 窗口注意力的数学

标准 ViT 自注意力复杂度：$O(N^2 \cdot D)$

Swin 窗口注意力复杂度：$O(M^2 \cdot N \cdot D)$

其中 $M=7$（窗口大小，远小于 $N$），所以实际是**线性复杂度**。

### 移位窗口机制

```
Layer l:   ┌───┬───┐    标准窗口分区
           │ A │ B │
           ├───┼───┤
           │ C │ D │
           └───┴───┘

Layer l+1: ┌─┬─┬─┐     窗口偏移 (shift=3)
           │A│B│ │     信息跨窗口交互
           ├─┼─┼─┤
           │C│D│ │
           └─┴─┴─┘
```

通过**循环移位 + 注意力掩码**避免窗口数增加（保持4个窗口的效率）。

---

## 3. ViT vs Swin：工程对比

| 特性 | ViT | Swin Transformer |
|:---|:---|:---|
| 注意力范围 | 全局（$O(N^2)$） | 局部窗口（$O(N)$） |
| 特征金字塔 | ❌ 单尺度 | ✅ 4级层次化 |
| 检测/分割 | ❌ 需额外改造 | ✅ 原生支持 |
| 推理速度 | 大图慢 | 快（线性复杂度） |
| 最佳场景 | 分类（ImageNet） | **检测/分割（COCO/ADE20K）** |

> **交错练习**：回到 [[感受野]]。CNN 用 stride 下采样 + 空洞卷积处理多尺度。Swin 用 **patch merging**（拼接相邻 2×2 patch 再线性投影）实现下采样，等效于 CNN 的 stride-2 但保留了 Transformer 的表达能力。

---

## 4. Patch Merging：Transformer 版下采样

```python
# Patch Merging 的等效实现
# 输入: (H, W, C) → 输出: (H/2, W/2, 2C)
x = feature_map  # (56, 56, 96)
# 取 2×2 邻域
x0 = x[0::2, 0::2]  # 左上
x1 = x[1::2, 0::2]  # 左下
x2 = x[0::2, 1::2]  # 右上
x3 = x[1::2, 1::2]  # 右下
x = torch.cat([x0,x1,x2,x3], dim=-1)  # (28, 28, 384)
x = nn.Linear(384, 192)(x)            # (28, 28, 192)
```

---

## 5. Swin 变体

| 模型 | 通道数 C | 各Stage层数 | 参数量 |
|:---|:---|:---|:---:|
| Swin-T (Tiny) | 96 | {2,2,6,2} | 28M |
| Swin-S (Small) | 96 | {2,2,18,2} | 50M |
| Swin-B (Base) | 128 | {2,2,18,2} | 88M |
| Swin-L (Large) | 192 | {2,2,18,2} | 197M |

---

## 6. 常见误区

- ❌ "Swin 就是带窗口的 ViT" — 层次化金字塔结构才是 Swin 的真正创新
- ❌ "窗口注意力会丢失全局信息" — 移位窗口实现了跨窗口通信，深层仍有全局感受野
- ❌ "Swin 已经是最优架构" — ConvNeXt 证明现代化 CNN 仍可与 Swin 竞争

---

## 🧪 自测题

1. **(基础)** Swin Transformer 的窗口大小通常是多大？为什么用这个值？
   <details><summary>💡 提示</summary>$7 \times 7$。经验值——太小损失效率，太大回归 $O(N^2)$。7×7 在局部性和效率间取得平衡。</details>

2. **(中等)** Swin 的移位窗口解决了什么问题？如果只用固定窗口会怎样？
   <details><summary>💡 提示</summary>固定窗口限制了不同窗口间 patch 的交互。移位窗口让相邻层的窗口边界偏移，使信息可以跨窗口流动，最终所有位置都能间接交互。</details>

3. **(较难)** Swin 如何做到在检测/分割任务上超越 CNN？与 ViT 相比的架构优势在哪里？
   <details><summary>💡 提示</summary>CNN 的 success 源于层次化多尺度特征（FPN 的基础）。ViT 丢失了这一点。Swin 恢复了层次化结构→可以无缝接入 FPN→直接用于密集预测任务。</details>

---

## 🧪 学完本节后可完成的作业

- 配合 [[目标检测RCNN与YOLO|目标检测]] 理解 Swin 如何作为检测 backbone 替代 ResNet
- 配合 [[计算机视觉-MAE]] 理解 Swin 的自监督预训练
---

## 学完后可以完成

- 可作为 HW06 开放项目『Swin 层次化架构实验』选题

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
