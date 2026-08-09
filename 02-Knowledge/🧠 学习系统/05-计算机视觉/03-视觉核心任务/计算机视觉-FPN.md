---
type: study
course: "05-计算机视觉"
topic: "FPN 特征金字塔网络 (Feature Pyramid Network)"
created: 2026-08-06
status: ongoing
difficulty: intermediate
concept: ["FPN", "特征金字塔", "多尺度", "目标检测", "特征融合"]
prerequisites: ["卷积神经网络CNN", "目标检测RCNN与YOLO", "感受野"]
related: ["SwinTransformer", "语义分割与UNet", "IoU与NMS"]
upstream: ["[[目标检测RCNN与YOLO]]"]
flow: knowledge
stage_moc: "[[🧭 阶段3-视觉核心任务]]"
kind: concept
source: "Lin et al. 2017 'Feature Pyramid Networks for Object Detection'; D2L Ch.14"
tags: [学习, 计算机视觉, FPN, 目标检测, 多尺度]
---

# FPN 特征金字塔网络 (Feature Pyramid Network)

> 所属模块：[[🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[🧭 阶段3-视觉核心任务|第三阶段]]
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

> **交错练习**：回到 [[感受野]]。单一特征图（如 C5，stride=32）的有效感受野约 $\sqrt{\text{理论RF}} \approx 22$ 像素。一个 $16\times16$ 的小物体在此层可能只有 1 个像素的响应 → 几乎无法检测。

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

### 4.1 ROI 该分配到哪一层？

多层特征都可用时，必须有一条**唯一分派规则**，否则同一物体会在多层被重复检测。Faster R-CNN + FPN 按 ROI 的**面积**分派：

$$k = \left\lfloor k_0 + \log_2\!\left(\frac{\sqrt{wh}}{224}\right) \right\rfloor$$

其中 $w, h$ 是 ROI 在原图上的宽高，$k_0 = 4$（即 224×224 的 ROI 落在 P4），结果裁剪到 $[2, 5]$ 区间。

| ROI 尺寸 | $\sqrt{wh}$ | $\log_2(\cdot/224)$ | 分配层 |
|:---|:---:|:---:|:---:|
| 56×56 | 56 | $-2$ | P2 |
| 112×112 | 112 | $-1$ | P3 |
| 224×224 | 224 | $0$ | P4 |
| 448×448 | 448 | $+1$ | P5 |

> 直觉：ROI 每放大一倍，就往上挪一层——这样每个 ROI 落在感受野与其尺寸相匹配的特征层上。

---

## 4.2 最小实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class FPN(nn.Module):
    """输入 C2~C5（通道数各异），输出 P2~P5（统一 256 通道）"""
    def __init__(self, in_channels=(256, 512, 1024, 2048), out_channels=256):
        super().__init__()
        # 侧向 1x1：统一通道数
        self.lateral = nn.ModuleList(
            [nn.Conv2d(c, out_channels, kernel_size=1) for c in in_channels]
        )
        # 输出 3x3：消除上采样混叠
        self.smooth = nn.ModuleList(
            [nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1)
             for _ in in_channels]
        )

    def forward(self, feats):           # feats = [C2, C3, C4, C5]
        laterals = [l(c) for l, c in zip(self.lateral, feats)]
        # 自上而下：从最深层开始逐级上采样相加
        for i in range(len(laterals) - 1, 0, -1):
            laterals[i - 1] = laterals[i - 1] + F.interpolate(
                laterals[i], size=laterals[i - 1].shape[-2:], mode="nearest"
            )
        return [s(l) for s, l in zip(self.smooth, laterals)]

# 形状自检：输入 stride 4/8/16/32，输出通道统一为 256
fpn = FPN()
cs = [torch.randn(1, c, s, s) for c, s in zip((256, 512, 1024, 2048), (56, 28, 14, 7))]
for p in fpn(cs):
    print(tuple(p.shape))   # (1,256,56,56) (1,256,28,28) (1,256,14,14) (1,256,7,7)
```

> 注意 `F.interpolate` 用 `size=` 而非 `scale_factor=2`：当特征图边长为奇数时，2× 上采样结果与浅层不一致会直接报形状错误。这是复现 FPN 最高频的坑。

---

## 4.3 适用条件与边界

| 条件 | 说明 |
|:---|:---|
| **适用** | 目标尺度跨度大（同图中既有远处小物体又有近处大物体）的检测/分割任务 |
| **收益有限** | 目标尺度单一（如证件照人脸、固定机位工业质检），此时单层特征已够用，FPN 徒增开销 |
| **代价** | 多层预测头带来额外显存与推理时间；P2 分辨率最高，显存占用往往是 P5 的 16 倍以上 |
| **后续改进** | PANet 增加自下而上的第二条路径补强定位信息；BiFPN 引入可学习的跨层加权融合；RetinaNet 额外构造 P6/P7 覆盖超大物体 |

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
   <details><summary>💡 思路</summary>顺着 ResNet 的 C2–C5 逐级下采样倍数推出各层 stride；再按「stride 越小分辨率越高」判断它更适合哪种尺寸的物体。</details>

2. **(中等)** 为什么 FPN 需要侧向连接 ($1\times1$ 卷积)？不用侧向连接直接上采样会有什么问题？
   <details><summary>💡 思路</summary>先看 C2–C5 的通道数是否一致——上采样后逐元素相加要求什么前提；再想缺了这条通路时，深层语义与浅层细节能否对齐。</details>

3. **(较难)** FPN 如何解决"同一个物体在不同尺度被多次检测"的问题？
   <details><summary>💡 思路</summary>FPN 需要一条把每个 ROI 唯一分派到某一层的规则。想想这条规则应该以 ROI 的什么量为依据（面积还是长宽比），再查对应的分配公式长什么样。</details>

---

## 学完后可以完成

> 下列作业在 `requires` 中引用了本卡，由 Dataview 实时派生（非人工维护反向链接）：

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

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
