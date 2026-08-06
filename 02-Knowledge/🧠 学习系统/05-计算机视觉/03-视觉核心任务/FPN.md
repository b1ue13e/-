---
type: study
course: "05-计算机视觉"
topic: "FPN 特征金字塔网络 (Feature Pyramid Network)"
created: 2026-08-06
status: planned
difficulty: intermediate
concept: ["FPN", "特征金字塔", "多尺度", "目标检测", "特征融合"]
prerequisites: ["卷积神经网络CNN", "目标检测RCNN与YOLO", "感受野"]
related: ["SwinTransformer", "语义分割与UNet", "IoU与NMS"]
upstream: ["[[02-Knowledge/🧠 学习系统/05-计算机视觉/03-视觉核心任务/目标检测RCNN与YOLO]]"]
flow: knowledge
stage_moc: "[[02-Knowledge/🧠 学习系统/05-计算机视觉/03-视觉核心任务/🎯 第三阶段：视觉核心任务]]"
kind: concept
source: "Lin et al. 2017 'Feature Pyramid Networks for Object Detection'; D2L Ch.14"
tags: [学习, 计算机视觉, FPN, 目标检测, 多尺度]
---

# FPN 特征金字塔网络 (Feature Pyramid Network)

> 所属模块：[[02-Knowledge/🧠 学习系统/05-计算机视觉/🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[02-Knowledge/🧠 学习系统/05-计算机视觉/03-视觉核心任务/🎯 第三阶段：视觉核心任务|第三阶段]]
> 建议先看：[[卷积神经网络CNN]]、[[目标检测RCNN与YOLO]]

---

## 0. 类别：A 类核心概念

FPN 是目标检测的"标配"——几乎所有现代检测器（Faster R-CNN、RetinaNet、Mask R-CNN）都使用 FPN。它优雅地解决了**单一尺度特征无法同时检测大小物体**的问题。

---

## 1. 直觉：同时拥有"望远镜"和"显微镜"

CNN 的特点：浅层高分辨率 → 适合小物体；深层低分辨率 → 适合大物体。

**FPN 的核心思想**：把深层的**强语义**信息通过自上而下的路径**融合**到浅层，让每一层特征既有高分辨率又有强语义。

```
CNN Backbone (自下而上):
  C5 (stride=32) ─────────────────────→ P5 (检测大物体)
    ↓ 上采样×2 + 侧向连接
  C4 (stride=16) ─────────────────────→ P4 (检测中大物体)
    ↓ 上采样×2 + 侧向连接
  C3 (stride=8)  ─────────────────────→ P3 (检测中小物体)
    ↓ 上采样×2 + 侧向连接
  C2 (stride=4)  ─────────────────────→ P2 (检测小物体)
```

---

## 2. 侧向连接 (Lateral Connection)

$$P_\ell = \text{Conv}_{3\times3}(\text{Conv}_{1\times1}(C_\ell) + \text{Upsample}(P_{\ell+1}))$$

| 操作 | 作用 |
|:---|:---|
| $\text{Conv}_{1\times1}(C_\ell)$ | 统一通道数（如全部 256） |
| $\text{Upsample}(P_{\ell+1})$ | 深层特征上采样 2×（最近邻） |
| $+$ | 逐元素相加（融合深层语义） |
| $\text{Conv}_{3\times3}$ | 消除上采样混叠伪影 |

---

## 3. 为什么需要 FPN？— 感受野视角

> **交错练习**：回到 [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/感受野|感受野]]。单一特征图（如 C5，stride=32）的有效感受野约 $\sqrt{\text{理论RF}} \approx 22$ 像素。一个 $16\times16$ 的小物体在此层可能只有 1 个像素的响应 → 几乎无法检测。

| 特征层 | stride | 典型感受野 | 适合物体尺寸 |
|:---|:---:|:---|:---|
| P2 | 4 | ~50 | 小物体 (<32×32) |
| P3 | 8 | ~120 | 中小物体 |
| P4 | 16 | ~250 | 中物体 |
| P5 | 32 | ~480 | 大物体 (>96×96) |

> FPN 让检测器在每个尺度上都有合适感受野的特征可用。

---

## 4. FPN 在主流检测器中的应用

| 检测器 | FPN 用法 |
|:---|:---|
| **Faster R-CNN + FPN** | RPN 在每层独立生成 anchor，ROI Pooling 根据物体大小选择特征层 |
| **RetinaNet** | 每层直接预测分类+回归（one-stage + FPN） |
| **Mask R-CNN** | FPN + ROI Align → 检测+分割 |
| **YOLOv3+** | 类似 FPN 的多尺度预测（3 个尺度） |

---

## 5. FPN vs U-Net vs DeepLab

| 架构 | 融合方式 | 用途 |
|:---|:---|:---|
| **FPN** | 自上而下 + 侧向连接（逐元素相加） | **目标检测** |
| **U-Net** | 编码-解码 + 跳跃连接（通道拼接） | **语义分割** |
| **DeepLab** | 空洞空间金字塔池化 (ASPP) | **语义分割** |

---

## 6. 常见误区

- ❌ "FPN 只是上采样" — 侧向连接的 $1\times1$ 卷积 + $3\times3$ 卷积才是关键
- ❌ "FPN 和 U-Net 一样" — FPN 用逐元素相加，U-Net 用通道拼接；FPN 面向检测，U-Net 面向分割

---

## 🧪 自测题

1. **(基础)** FPN 的 P2 层 stride 是多少？主要检测什么尺寸的物体？
   <details><summary>💡 提示</summary>stride=4，检测小物体 (<32×32)。</details>

2. **(中等)** 为什么 FPN 需要侧向连接 ($1\times1$ 卷积)？不用侧向连接直接上采样会有什么问题？
   <details><summary>💡 提示</summary>$C_\ell$ 的通道数可能不同（ResNet: 256/512/1024/2048）。$1\times1$ 卷积统一为 256。无侧向连接意味着深层语义无法与浅层细节对齐。</details>

3. **(较难)** FPN 如何解决"同一个物体在不同尺度被多次检测"的问题？
   <details><summary>💡 提示</summary>Faster R-CNN + FPN 根据 ROI 的尺寸 ($w,h$) 选择性分配：$k = k_0 + \log_2(\sqrt{wh}/224)$。小 ROI → 浅层 P2/P3，大 ROI → 深层 P4/P5。</details>

---
---

## 学完后可以完成

- [[03-Projects/05-计算机视觉/阶段作业/05-计算机视觉-阶段作业-03-目标检测PascalVOC|HW05]]：理解多尺度特征融合在检测中的作用

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
