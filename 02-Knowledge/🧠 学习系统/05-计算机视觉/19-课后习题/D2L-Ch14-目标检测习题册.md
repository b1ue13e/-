---
type: project
topic: "D2L Ch.14 目标检测课后习题"
created: 2026-08-05
status: active
flow: project
kind: problem-type
source: "D2L Chapter 14: Object Detection and Bounding Boxes"
source_url: "https://d2l.ai/chapter_computer-vision/object-detection-and-bounding-boxes.html"
license: "CC BY-SA 4.0"
tags: [计算机视觉, 课后习题, D2L, 目标检测, 语义分割]
---

# D2L Ch.14 目标检测课后习题

> **来源改编**：基于 [Dive into Deep Learning (D2L) Ch.14 Object Detection and Bounding Boxes](https://d2l.ai/chapter_computer-vision/object-detection-and-bounding-boxes.html)（CC BY-SA 4.0）各节 Exercises 重述、扩展与参数替换。涵盖 IoU 计算、锚框生成、NMS、SSD 多尺度设计、YOLO 网格预测、FCN 全卷积化、U-Net 跳跃连接、语义分割评估指标八大模块。

## 对应知识卡

- [[目标检测RCNN与YOLO]]
- [[语义分割与UNet]]
- [[卷积神经网络CNN]]
- [[迁移学习与微调]]
- [[数据增强与正则化]]

## 作答协议

每题先写「**作答前信心：__/100**」，完成后写「**作答后信心：__/100**」。手算题写出完整推导过程；代码题保留输入、输出和断言（assert）。错题记录错因并在 24h / 72h / 7d 重测。

---

### 题 1（计算题）：IoU（交并比）手算

IoU（Intersection over Union）是目标检测中最基础的定位精度评估指标，也用于 NMS 的抑制判定和锚框匹配。

给定两个边界框（均以左上-右下坐标 $(x_1, y_1, x_2, y_2)$ 表示，坐标系原点在左上角，$x$ 向右、$y$ 向下为正）：

- **框 A**：$(30, 50, 210, 230)$
- **框 B**：$(90, 120, 270, 260)$

- (a) 在纸上画出两个框的位置示意图，标注坐标轴方向和关键坐标值。
- (b) 写出 IoU 的通用公式：$\text{IoU}(A, B) = \dfrac{|\text{Area}_{\text{overlap}}|}{|\text{Area}_{\text{union}}|}$。然后**手算**：
  - 框 A 的面积
  - 框 B 的面积
  - 交集矩形的左上/右下坐标（用 $\max$/$\min$ 表达）
  - 交集面积（若两框不相交则交集为 0）
  - 并集面积（提示：$\text{Area}_A + \text{Area}_B - \text{Area}_{\text{overlap}}$）
  - 最终 IoU 值（保留三位小数）
- (c) 验证你的计算：设框 A 和框 B **恰好不相交**（A 的 $x_2 = \text{B}的 x_1$，即边界相切），此时 IoU 应为多少？为什么这种"相切"情况在实际目标检测中也可能被视为无效匹配？
- (d) 在目标检测训练中，IoU 阈值通常设为 0.5 来判定锚框是否为正样本。讨论：阈值设为 0.5 的含义是什么？如果阈值提高到 0.7 或降低到 0.3，分别会对训练的正负样本分布产生什么影响？

> [!hint]- 提示 1
> 交集左上角 $x_{\text{inter},1} = \max(x_{A,1}, x_{B,1})$，$y_{\text{inter},1} = \max(y_{A,1}, y_{B,1})$；交集右下角 $x_{\text{inter},2} = \min(x_{A,2}, x_{B,2})$，$y_{\text{inter},2} = \min(y_{A,2}, y_{B,2})$。交集宽 $w_{\text{inter}} = \max(0, x_{\text{inter},2} - x_{\text{inter},1})$，高同理。
> [!hint]- 提示 2
> 框 A 面积：$(210 - 30) \times (230 - 50) = 180 \times 180 = 32{,}400$；框 B 面积：$(270 - 90) \times (260 - 120) = 180 \times 140 = 25{,}200$。
> [!hint]- 提示 3
> 交集坐标：$x_1 = \max(30, 90) = 90$，$y_1 = \max(50, 120) = 120$，$x_2 = \min(210, 270) = 210$，$y_2 = \min(230, 260) = 230$。交集 = $(210 - 90) \times (230 - 120) = 120 \times 110 = 13{,}200$。
> [!hint]- 提示 4
> 阈值提高 → 正样本更少且质量更高（定位更精确），但可能导致正样本过少而训练不稳定；阈值降低 → 正样本更多但包含大量低质量匹配，定位精度下降。
> [!success]- 答案锚点
> (b) 框 A 面积 = $(210 - 30) \times (230 - 50) = 180 \times 180 = 32{,}400$；框 B 面积 = $(270 - 90) \times (260 - 120) = 180 \times 140 = 25{,}200$；交集 = $(210 - 90) \times (230 - 120) = 120 \times 110 = 13{,}200$；并集 = $32{,}400 + 25{,}200 - 13{,}200 = 44{,}400$；$\text{IoU} = 13{,}200 / 44{,}400 \approx 0.297$。(c) 边界相切时交集面积 = 0（线接触面积为零），IoU = 0。相切在离散像素中对应的交集区域可能为 0 或仅 1 像素宽，实际上没有"重叠区域"，因此应被视为无效匹配。(d) IoU ≥ 0.5 表示两个框的重叠面积超过并集的一半，视觉上已大致定位到同一物体。阈值 0.7：正样本极度稀缺，可能导致大量锚框被标为负样本 → 正负样本严重失衡 → 训练困难，但最终定位精度可能更高。阈值 0.3：正样本大量增加，但许多低质量匹配被视为正样本 → 模型学会容忍不精确的定位 → 推理时边界框回归质量下降。

---

### 题 2（设计题）：锚框（Anchor Box）的生成逻辑

锚框是 SSD 和 Faster R-CNN 的核心组件，在每个特征图位置预先定义一组不同尺度和宽高比的参考框。

假设输入图像尺寸为 $H \times W = 480 \times 640$，特征图尺寸为 $h \times w = 30 \times 40$（对应 stride $s = 16$）。在特征图的每个空间位置 $(i, j)$（$i \in [0, h), j \in [0, w)$），生成 $k = 6$ 个锚框，参数为：

- **尺度**（scale，相对于输入图像的边长比例）：$s_1 = 0.25,\ s_2 = 0.50$
- **宽高比**（aspect ratio）：$r \in \{1/2,\ 1,\ 2\}$
- 对每个尺度，分别与三种宽高比组合，共 $2 \times 3 = 6$ 个锚框

- (a) 写出特征图位置 $(i, j)$ 映射回输入图像中心坐标的公式（使用 stride $s$，设锚框中心与特征图像素中心对齐）。计算 $(i, j) = (15, 20)$ 时锚框中心在原图上的坐标 $(c_x, c_y)$。
- (b) 给定尺度 $s_k$ 和宽高比 $r_t$，推导锚框的**宽度** $w_{kt}$ 和**高度** $h_{kt}$ 的计算公式（以原图像素为单位）。为什么公式是 $w = s_k \cdot W \cdot \sqrt{r}$ 和 $h = s_k \cdot H / \sqrt{r}$（或等价地 $w = s_k \cdot \sqrt{r} \cdot \sqrt{HW}$）？解释 $\sqrt{r}$ 因子的作用。
- (c) 计算中心点 $(320, 240)$（图像正中心）处所有 6 个锚框的具体 $(x_{\min}, y_{\min}, x_{\max}, y_{\max})$ 坐标（取整数）。以 $s_1 = 0.25, r = 2$ 为例写出完整推导。
- (d) 如果输入图像中需要检测的物体尺度范围是 $[16 \times 16,\ 256 \times 256]$（像素），当前锚框设计方案能否覆盖？如果不能覆盖，应如何调整 scale 或添加额外的特征图层？

> [!hint]- 提示 1
> 特征图 $(i, j)$ → 图像中心坐标：$c_x = (j + 0.5) \times s$，$c_y = (i + 0.5) \times s$（像素中心对齐）。对 $(15, 20)$：$c_x = (20 + 0.5) \times 16 = 328$，$c_y = (15 + 0.5) \times 16 = 248$。
> [!hint]- 提示 2
> 锚框面积 = $(s_k \cdot W) \times (s_k \cdot H)$ 的缩放版本，保持宽高比 $r = w/h$：由 $w \cdot h = s_k^2 \cdot W \cdot H$ 和 $w/h = r$ → $w = s_k \cdot \sqrt{r \cdot W \cdot H}$，$h = s_k \cdot \sqrt{W \cdot H / r}$。或等价地 $w = s_k \cdot W \cdot \sqrt{r}$，$h = s_k \cdot H / \sqrt{r}$（当 $W=H$ 时两者等价，$W \neq H$ 时需注意具体实现的选择）。
> [!hint]- 提示 3
> 以 $(c_x, c_y) = (320, 240)$，$s_1 = 0.25$，$r = 2$：$w = 0.25 \times 640 \times \sqrt{2} \approx 160 \times 1.414 \approx 226$，$h = 0.25 \times 480 / \sqrt{2} \approx 120 / 1.414 \approx 85$。框坐标：$(320 - 113, 240 - 42, 320 + 113, 240 + 42) \approx (207, 198, 433, 282)$。
> [!hint]- 提示 4
> $s_1=0.25$ 对应锚框尺寸约 $160 \times 120$（$r=1$），最小锚框（$r=1/2$）约 $113 \times 170$，均远大于 $16\times16$；$s_2=0.50$ 对应约 $320 \times 240$。需要更小的 scale（如 0.05, 0.10）或使用 stride 更小的浅层特征图（如 stride=4 或 8）。
> [!success]- 答案锚点
> (a) $c_x = (j + 0.5) \times s$，$c_y = (i + 0.5) \times s$。$(15, 20)$：$c_x = 20.5 \times 16 = 328$，$c_y = 15.5 \times 16 = 248$。(b) 锚框面积 $= s_k^2 \cdot W \cdot H$（确保尺度 $s_k$ 使锚框边长约为图像的 $s_k$ 比例）。结合 $w/h = r$ → $w = s_k \cdot \sqrt{r \cdot WH}$，$h = s_k \cdot \sqrt{WH / r}$。$\sqrt{r}$ 保证在保持面积不变的前提下调整宽高比。(c) 6 个锚框（中心 $(320, 240)$）：

| $s$ | $r$ | $w$ | $h$ | $(x_{\min}, y_{\min}, x_{\max}, y_{\max})$ |
|:---|:---|:---|:---|:---|
| 0.25 | 1/2 | $\approx 113$ | $\approx 226$ | (263, 127, 377, 353) |
| 0.25 | 1 | 160 | 120 | (240, 180, 400, 300) |
| 0.25 | 2 | $\approx 226$ | $\approx 85$ | (207, 198, 433, 282) |
| 0.50 | 1/2 | $\approx 226$ | $\approx 453$ | (207, 14, 433, 467) |
| 0.50 | 1 | 320 | 240 | (160, 120, 480, 360) |
| 0.50 | 2 | $\approx 453$ | $\approx 170$ | (94, 155, 546, 325) |

(d) 当前方案最小锚框约 $113 \times 226$ 或 $160 \times 120$，无法覆盖 $16 \times 16$ 的小物体。解决方案：① 添加更小的 scale（如 $s_0=0.05, s_1=0.10$）；② 使用更浅层的高分辨率特征图（如 stride=4 的特征图），为每层分配不同的 scale 范围——这正是 SSD 多尺度预测的核心思想。

---

### 题 3（算法题）：非极大值抑制（NMS）算法伪代码与复杂度

NMS（Non-Maximum Suppression）是目标检测后处理的标准步骤：从大量重叠的预测框中筛选出"最可信且不冗余"的最终检测结果。

- (a) 写出 NMS 的**完整伪代码**，输入为预测框列表 $\mathcal{B} = \{(x_1, y_1, x_2, y_2, \text{score})\}$ 和 IoU 阈值 $\tau$，输出为筛选后的框列表。伪代码应包含：按 score 降序排序、逐个取出最高分框、计算与其他框的 IoU、抑制 IoU > $\tau$ 的框、循环直到处理完所有框。使用清晰的缩进和循环/条件语句。
- (b) 分析 NMS 的**时间复杂度**（假设框数为 $N$，IoU 计算为 $O(1)$），给出最坏情况下的复杂度并解释之。是否存在比朴素 NMS 更高效的方法？
- (c) NMS 的一个已知问题是：当两个**不同类别的物体**高度重叠时（如"人骑自行车"中的人和车），NMS 会错误地抑制其中一个。如何改进 NMS 以处理多类别检测？（提示：per-class NMS vs class-agnostic NMS）
- (d) **Soft-NMS** 是对传统 NMS 的改进。解释 Soft-NMS 的核心思想——不是直接删除高重叠框，而是降低其置信度分数。写出 Soft-NMS 的分数衰减公式（线性衰减和高斯衰减两种），并讨论 Soft-NMS 相比传统 NMS 在什么场景下收益最大。

> [!hint]- 提示 1
> NMS 伪代码框架：
> ```
> Input: B = [(box, score)], IoU threshold τ
> Output: D (kept boxes)
> D ← []
> while B not empty:
>     m ← argmax scores in B
>     M ← B[m]; remove M from B; D.append(M)
>     for each b in B:
>         if IoU(M, b) > τ: remove b from B
> return D
> ```
> [!hint]- 提示 2
> 朴素 NMS：排序 $O(N\log N)$，worst case 每次只删一个框 → 共 $N$ 轮循环，每轮扫描剩余 $O(N)$ 框 → $O(N^2)$。加速方法：按空间分桶（如将图像分成网格，只比较同格/邻格内的框）→ 期望复杂度 $O(N\log N)$；GPU 加速的 batched NMS（如 torchvision.ops.nms）。
> [!hint]- 提示 3
> 多类别情况应使用 **per-class NMS**：先按类别分组，每个类别内部独立做 NMS — 不同类别的框不会互相抑制。
> [!hint]- 提示 4
> Soft-NMS 线性衰减：$s_i = s_i \cdot (1 - \text{IoU}(M, b_i))$ 当 $\text{IoU} > \tau$；高斯衰减：$s_i = s_i \cdot \exp(-\frac{\text{IoU}(M, b_i)^2}{\sigma})$。std NMS 是 $\sigma \to 0$ 的特例。
> [!success]- 答案锚点
> (a) 伪代码：
> ```
> def nms(boxes, scores, iou_threshold):
>     # boxes: (N, 4) [x1, y1, x2, y2], scores: (N,)
>     order = argsort(scores, descending=True)
>     keep = []
>     while len(order) > 0:
>         idx = order[0]           # 当前最高分
>         keep.append(idx)
>         if len(order) == 1: break
>         # 计算当前框与其余所有框的 IoU
>         ious = compute_iou(boxes[idx], boxes[order[1:]])
>         # 保留 IoU <= threshold 的框
>         mask = ious <= iou_threshold
>         order = order[1:][mask]
>     return keep
> ```
> (b) 排序 $O(N\log N)$。最坏情况：所有框互不重叠 → 每次 while 迭代只移除当前最高分框（1 个），循环 $N$ 次，每次计算与剩余 $O(N)$ 框的 IoU → $O(N^2)$。平均情况（框分布均匀且阈值合理）：每次抑制大量框，接近 $O(N\log N)$。高效方法：空间哈希/网格分桶、GPU 上的 batched IoU 矩阵计算 + 逐行抑制。(c) 使用 **per-class NMS**：先将预测框按类别分组（$\text{cls}_1, \text{cls}_2, \dots$），每组独立运行 NMS。这样"人"类别的框不会抑制"自行车"类别的框，重叠的不同类物体共存。(d) Soft-NMS 不删除框，而是对高重叠框**降权**：线性 $s_i \leftarrow s_i \cdot (1 - \text{IoU})$（$\text{IoU} > \tau$），高斯 $s_i \leftarrow s_i \cdot \exp(-\text{IoU}^2 / \sigma)$。优势场景：高度拥挤的物体（人群、车辆密集场景），标准 NMS 直接删除重叠框导致漏检 → Soft-NMS 通过降权保留这些框，后续可通过二次阈值过滤恢复部分检测。在 COCO 上 Soft-NMS 可提升 mAP 约 1-2%，对 AP@0.7 等严格 IoU 阈值的指标提升更明显。

---

### 题 4（分析题）：SSD 的多尺度特征图设计原理

SSD（Single Shot MultiBox Detector）的核心创新是**在多个不同分辨率的特征图上同时进行检测**，每个特征图层负责检测不同尺度的物体。

- (a) 画出 SSD-300（以 VGG-16 为 backbone）的完整架构示意图。标出用于检测的六个特征图层的名称、空间尺寸（$H \times W$）、stride、以及每层分配的默认锚框 scale 范围。说明为什么需要多尺度特征图而不是仅在最后一层做检测。
- (b) SSD 的锚框 scale 按公式 $s_k = s_{\min} + \frac{s_{\max} - s_{\min}}{m - 1}(k - 1)$（$k \in [1, m]$，$m=6$）分配到各层。通常 $s_{\min}=0.2$，$s_{\max}=0.9$。计算六个特征图层分别对应的 $s_k$ 值，并解释这个**线性递增**的 scale 分配策略是否合理——为什么深层（小特征图）应该用更大的 scale？
- (c) SSD 在每个特征图位置预测 4 个边界框偏移量 $(\Delta x, \Delta y, \Delta w, \Delta h)$ 和 $C$ 个类别分数（含背景类）。对于 Conv4_3 层（$38 \times 38$），每个位置有 4 个锚框；对于 Conv11_2 层（$1 \times 1$），每个位置也有 4 个锚框。计算这两层分别产生多少个预测框，并计算 SSD-300 总共产生多少个预测框。
- (d) SSD 的**浅层特征图**（如 Conv4_3，stride=8）语义信息弱但分辨率高，适合检测小物体；**深层特征图**（如 Conv11_2，stride=300）语义强但分辨率低，适合检测大物体。这种"分工"存在什么根本性问题？FPN 是如何解决该问题的？用"语义鸿沟"（semantic gap）概念解释。

> [!hint]- 提示 1
> SSD-300 六层特征图：Conv4_3 (38×38, stride=8), Conv7/FC7 (19×19, stride=16), Conv8_2 (10×10, stride=32), Conv9_2 (5×5, stride=64), Conv10_2 (3×3, stride=100), Conv11_2 (1×1, stride=300)。
> [!hint]- 提示 2
> $s_k$ 计算（$m=6$）：$s_1 = 0.2 + (0.9 - 0.2)/(5) \times 0 = 0.2$，$s_2 = 0.2 + 0.14 \times 1 = 0.34$，$s_3 = 0.48$，$s_4 = 0.62$，$s_5 = 0.76$，$s_6 = 0.9$。深层特征图的每个像素对应原图更大区域（感受野大），自然适合检测大物体，因此用大 scale。
> [!hint]- 提示 3
> Conv4_3: $38 \times 38 \times 4 = 5{,}776$ 框。Conv11_2: $1 \times 1 \times 4 = 4$ 框。SSD-300 总框数：Conv4_3 (38²×4=5776) + Conv7 (19²×6=2166) + Conv8_2 (10²×6=600) + Conv9_2 (5²×6=150) + Conv10_2 (3²×4=36) + Conv11_2 (1²×4=4) = 8732。
> [!hint]- 提示 4
> 语义鸿沟：Conv4_3 仅经过约 10 层卷积 → 特征仍是低级纹理/边缘，缺乏"这是猫还是狗"的语义判别力 → 虽能看到小物体但认不准。Conv11_2 经过全网络的深度语义 → 但分辨率太低，对小物体连"看到"都做不到。FPN 通过自上而下路径 + 横向连接，将深层强语义"回传"到浅层高分辨率特征图。
> [!success]- 答案锚点
> (a) 架构：VGG-16 backbone（至 Conv5_3/pool5）→ 额外卷积层（Conv6/7, Conv8_2, Conv9_2, Conv10_2, Conv11_2）。用于检测的六层：(1) Conv4_3 (38×38, s=8), (2) Conv7 (19×19, s=16), (3) Conv8_2 (10×10, s=32), (4) Conv9_2 (5×5, s=64), (5) Conv10_2 (3×3, s=100), (6) Conv11_2 (1×1, s=300)。只在最后一层检测 → 单一感受野尺度 → 小物体在深层特征图上可能只有 1 像素甚至消失 → 漏检严重。多尺度层确保每个物体在至少一个合适的尺度层上被检出。(b) $s_1$=0.20, $s_2$=0.34, $s_3$=0.48, $s_4$=0.62, $s_5$=0.76, $s_6$=0.90。线性递增合理：深层 stride 大 → 特征图像素对应原图更大区域 → 自然应分配更大锚框；浅层 stride 小 → 像素对应小区域 → 小锚框。(c) Conv4_3：$38^2 \times 4 = 5{,}776$；Conv11_2：$1^2 \times 4 = 4$。SSD-300 总预测框 = $38^2 \times 4 + 19^2 \times 6 + 10^2 \times 6 + 5^2 \times 6 + 3^2 \times 4 + 1^2 \times 4 = 5{,}776 + 2{,}166 + 600 + 150 + 36 + 4 = 8{,}732$。(d) 根本问题：浅层特征"看到但认不准"（语义弱），深层特征"认得准但看不到"（分辨率低）→ 小物体检测效果差。FPN 通过**自上而下路径**（深层特征上采样）与**横向连接**（$1\times1$ 卷积对齐通道后逐元素相加），将深层强语义注入浅层高分辨率特征 → 每一层都同时拥有高分辨率和强语义，弥合了"语义鸿沟" → 小物体 mAP 显著提升（COCO AP@S +3~5%）。

---

### 题 5（设计题）：YOLO 的网格预测与边界框回归

YOLO（You Only Look Once）将目标检测建模为单个回归问题：将输入图像划分为 $S \times S$ 网格，每个网格单元（grid cell）直接预测边界框和类别概率。

- (a) 描述 YOLO v1 的前向预测流程：输入图像 $448 \times 448 \times 3$ → 经过 24 层卷积 + 2 层 FC → 输出张量 $7 \times 7 \times 30$。解释输出张量中 $30$ 个通道的含义——对每个 grid cell，这 30 个值分别代表什么？（提示：$B=2$ 个边界框，$C=20$ 个类别（Pascal VOC））
- (b) 对于每个 grid cell，YOLO 预测的边界框参数为 $(x, y, w, h, \text{confidence})$。解释 $(x, y)$ 为什么是**相对于 grid cell 左上角的偏移量**（取值范围 $[0, 1]$），而 $(w, h)$ 是**相对于整张图像的宽高比例**（取值范围 $[0, 1]$）。如果某个 grid cell（位于第 3 行第 5 列）预测的框参数为 $(x, y, w, h) = (0.6, 0.3, 0.15, 0.20)$，将其转换为原图像素坐标（图像尺寸 $448 \times 448$）。
- (c) YOLO 的置信度分数定义为 $\text{confidence} = \text{Pr}(\text{Object}) \times \text{IoU}_{\text{pred}}^{\text{truth}}$，而测试时的类别特定置信度为 $\text{Pr}(\text{Class}_i | \text{Object}) \times \text{Pr}(\text{Object}) \times \text{IoU}_{\text{pred}}^{\text{truth}}$。解释这三项各自的含义，以及为什么测试时要把它们乘在一起。
- (d) YOLO v1 的一个显著缺陷是对**密集小物体**（如鸟群、人群）的检测效果差。从网格划分机制（每个 grid cell 只预测 2 个框且最多属于 1 个类别）的角度，解释为什么密集小物体会导致大量漏检。YOLO v2/v3 做了哪些改进来缓解此问题？

> [!hint]- 提示 1
> 30 个通道 = $B \times 5 + C = 2 \times 5 + 20 = 30$。每个 grid cell 的 30 维向量：前 5 维（框 1: x, y, w, h, conf），中 5 维（框 2: x, y, w, h, conf），后 20 维（各类别的条件概率 $\text{Pr}(\text{Class}_i|\text{Object})$，注意这个概率是 per-cell 而非 per-box 的）。
> [!hint]- 提示 2
> grid cell 在 $(3, 5)$ 即行=3、列=5，cell 左上角在原图坐标为 $(5 \times 64, 3 \times 64) = (320, 192)$。$(x, y) = (0.6, 0.3)$ 表示框中心在 cell 内偏移 $(0.6 \times 64, 0.3 \times 64) = (38.4, 19.2)$ → 在原图坐标为 $(320 + 38.4, 192 + 19.2) = (358.4, 211.2)$。$w = 0.15 \times 448 = 67.2$，$h = 0.20 \times 448 = 89.6$。框坐标：$(358.4 - 33.6, 211.2 - 44.8, 358.4 + 33.6, 211.2 + 44.8) = (324.8, 166.4, 392.0, 256.0)$。
> [!hint]- 提示 3
> $\text{Pr}(\text{Object})$ 是 grid cell 包含物体的概率（二分类：有/无物体中心落在此 cell），$\text{IoU}_{\text{pred}}^{\text{truth}}$ 是预测框与真值框的重叠度（定位精度），$\text{Pr}(\text{Class}_i|\text{Object})$ 是在有物体的条件下来自类别 $i$ 的概率。测试时相乘得到"这个框属于类别 $i$ 且定位准确的联合置信度"。
> [!hint]- 提示 4
> YOLO v1 每个 grid cell 只预测 2 个框 + 1 组类别概率 → 如果 cell 内包含 > 2 个物体中心，必然漏检。$7\times7$ 网格粗（每个 cell 64×64 像素）→ 小物体密集时多个物体中心落入同一 cell。YOLO v2 引入锚框机制（每个 cell 可预测多个不同形状的框）并增加分辨率；YOLO v3 使用三个尺度的特征图（类似 FPN）→ 多尺度检测 + 每层更多锚框。
> [!success]- 答案锚点
> (a) 输出 $7 \times 7 \times 30$：$S=7$ 网格，每 cell 30 维 = $B \times 5 + C = 2 \times 5 + 20$。维度分解：[0:5] 第 1 个框的 $(x, y, w, h, \text{conf})$，[5:10] 第 2 个框的 $(x, y, w, h, \text{conf})$，[10:30] 20 个类别的 $\text{Pr}(\text{Class}_i | \text{Object})$（per-cell，两个框共享）。(b) $(x, y)$ 是相对 cell 左上角的归一化偏移（除以 cell 边长 64），$(w, h)$ 是相对整图尺寸的归一化值。$(3, 5)$ cell → 左上角 $(320, 192)$，cell 边长 $448/7=64$。$x=0.6 \to 320+0.6\times64=358.4$，$y=0.3 \to 192+0.3\times64=211.2$，$w=0.15\times448=67.2$，$h=0.20\times448=89.6$。左上 $(358.4-33.6, 211.2-44.8) = (324.8, 166.4)$，右下 $(358.4+33.6, 211.2+44.8) = (392.0, 256.0)$。(c) $\text{Pr}(\text{Object})$（objectness）：cell 中是否有物体中心；$\text{IoU}_{\text{pred}}^{\text{truth}}$：预测框的定位精度；$\text{Pr}(\text{Class}_i|\text{Object})$：给定有物体，它属于类别 $i$ 的概率。测试时三者相乘 = 类别特定的置信度 $\text{Pr}(\text{Class}_i) \times \text{IoU}$ — 既考虑分类正确性也考虑定位精度，用于后续 NMS 排序。(d) YOLO v1 的局限：① $7\times7$ 粗网格 → 每个 cell 覆盖 $64\times64$ 区域 → 密集小物体（如鸟群中每只鸟可能仅 $16\times16$）多个物体中心落入同一 cell → cell 只能输出 2 个框和 1 组类别 → 最多检测到 2 个同类别物体；② 空间约束：每个 cell 最多预测 $B=2$ 个框（且它们共享类别预测）→ 超过 2 个物体则必然漏检。YOLO v2 改进：引入锚框（每个 cell 用 k=5 个锚框预测更多物体）、高分辨率输入、passthrough 层融合细粒度特征。YOLO v3 改进：三尺度特征图预测（类似 FPN）→ 每个尺度独立检测不同大小的物体 → 总预测框数大幅增加，密集小物体检测能力显著提升。

---

### 题 6（架构题）：FCN 的全卷积化改造

全卷积网络（Fully Convolutional Network, FCN）是语义分割的里程碑：将分类 CNN（如 VGG-16）改造为端到端的像素级分类器。

- (a) 解释"全卷积化"的具体含义：VGG-16 的最后三层是 FC-4096 → FC-4096 → FC-1000。如何将它们转换为卷积层？写出转换后每层的卷积核尺寸、输入/输出通道数和输出空间尺寸（假设输入特征图为 $7 \times 7 \times 512$）。转换后的网络对输入尺寸有什么新的灵活性？
- (b) FCN 的核心挑战：经过 backbone 的下采样（5 次 pooling，每次 stride=2），特征图分辨率降为输入的 $1/32$。为了得到与输入同分辨率的预测图，FCN 使用**转置卷积**（Transposed Convolution，又称 deconvolution）进行上采样。解释转置卷积与普通卷积（双线性插值上采样 + 卷积）的关系，给出一个 $2\times2$ 输入经 $3\times3$ 转置卷积（stride=2, padding=1）得到 $4\times4$ 输出的具体数值示例（使用固定权重，如全 1 核）。
- (c) FCN-32s、FCN-16s、FCN-8s 是 FCN 的三种变体（数字表示最终预测图相对于原图的下采样倍数）。解释三者的架构差异以及为什么 FCN-8s 的分割精度显著高于 FCN-32s。"跳跃连接"（skip connection）在 FCN 中具体如何实现？
- (d) FCN 的输出是每个像素的 $C$ 类 softmax 概率。写出**逐像素交叉熵损失**（per-pixel cross-entropy loss）的公式：给定真值标签图 $\mathbf{Y} \in \{1, \dots, C\}^{H \times W}$ 和预测 logits $\mathbf{Z} \in \mathbb{R}^{C \times H \times W}$，损失 $\mathcal{L}$ 如何计算？如果图像中 90% 的像素是背景类，这种损失函数会有什么问题？

> [!hint]- 提示 1
> FC 层 → 卷积层转换：FC-4096（输入 $7\times7\times512=25088$）→ $7\times7$ 卷积（kernel=7, in=512, out=4096, pad=0）— 输出 $1\times1\times4096$。FC-4096 → $1\times1$ 卷积（in=4096, out=4096）。FC-1000 → $1\times1$ 卷积（in=4096, out=1000）。转换后网络可接受任意尺寸输入 → 输出为 $C \times H' \times W'$ 的热力图。
> [!hint]- 提示 2
> 转置卷积是普通卷积的"反向"操作：如果普通卷积将 $4\times4$ 映射到 $2\times2$（kernel=3, stride=2, pad=1），那么同样参数的转置卷积将 $2\times2$ 映射回 $4\times4$（通过插入零和卷积）。本质上等价于：先对输入插零上采样（在每两个元素间插 stride-1 个零），再做普通卷积。
> [!hint]- 提示 3
> FCN-32s：pool5 特征图 $1/32$ 分辨率 → 直接 32× 上采样到原图 → 粗糙边界。FCN-16s：pool5 先 2× 上采样 + pool4 特征相加 → 再 16× 上采样 → 中等精细度。FCN-8s：pool5 2× → + pool4 → 2× → + pool3 → 8× 上采样 → 最精细。跳跃连接将较浅层的高分辨率特征与深层上采样特征相加，补充空间细节。
> [!hint]- 提示 4
> $\mathcal{L} = -\frac{1}{HW} \sum_{i=1}^{H} \sum_{j=1}^{W} \log \text{softmax}(\mathbf{Z}_{:, i, j})_{Y_{i,j}}$。类别极度不平衡时，模型倾向于将所有像素预测为背景 → 背景 loss 主导 → 前景物体分割效果差 → 需加权损失或 focal loss。
> [!success]- 答案锚点
> (a) 转换：① FC-4096（输入 $7\times7\times512$）→ Conv2d(in=512, out=4096, kernel=7, stride=1, pad=0) → 输出 $1\times1\times4096$；② FC-4096 → Conv2d(in=4096, out=4096, kernel=1) → 输出 $1\times1\times4096$；③ FC-1000 → Conv2d(in=4096, out=num_classes, kernel=1) → 输出 $1\times1\times C$。全卷积化后网络可接受任意尺寸输入 → 输出变为空间热力图（$C \times h \times w$），而非单个类别向量。(b) 转置卷积 = 对输入进行插零上采样（在行列间各插入 stride-1=1 个零）→ 普通卷积。具体步骤：$2\times2$ 输入在行列间插零 → $3\times3$（元素 + 零交替），与 $3\times3$ 全 1 核卷积（stride=1, pad=1）→ $4\times4$ 输出。若输入为 $\begin{pmatrix}1&2\\3&4\end{pmatrix}$，插零后 $\begin{pmatrix}1&0&2\\0&0&0\\3&0&4\end{pmatrix}$，与全 1 核卷积 → 输出各位置为邻域和。(c) FCN-32s：pool5（$1/32$）→ $1\times1$ 卷积预测 → 32× 双线性插值上采样 → 输出。FCN-16s：pool5 2× 上采样 + pool4（$1/16$）经 $1\times1$ 卷积后的特征 → 融合后 16× 上采样。FCN-8s：在 FCN-16s 基础上再融合 pool3（$1/8$）→ 8× 上采样。跳跃连接将浅层高分辨率池化层输出通过 $1\times1$ 卷积降维后与上采样特征逐元素相加 → 补充空间定位细节。FCN-8s 因融合了更多浅层空间信息，边界更清晰。(d) $\mathcal{L} = \frac{1}{HW} \sum_{i,j} \text{CrossEntropy}(\mathbf{Z}_{:,i,j}, Y_{i,j}) = -\frac{1}{HW} \sum_{i,j} \log \frac{\exp(Z_{Y_{i,j}, i, j})}{\sum_{c=1}^{C} \exp(Z_{c,i,j})}$。类别不平衡问题：背景像素占 90% → loss 被背景主导 → 模型学会"全输出背景"即可获得低 loss → 前景分割失败。解决方案：① 按类别频率加权损失（$\alpha_{\text{fg}} \gg \alpha_{\text{bg}}$）；② 用 Dice Loss 或 Focal Loss 替代 CE；③ 在训练时采样平衡的 mini-batch（如每 batch 保证前景像素 ≥ 25%）。

---

### 题 7（对比分析题）：U-Net 跳跃连接的作用——为什么比 FCN 效果好

U-Net 在生物医学图像分割中取得了卓越性能，其"U 形"对称架构和跳跃连接是其标志性设计。

- (a) 画出 U-Net 的完整架构图（标注各层的空间尺寸和通道数变化）。解释 "U 形"设计的直觉：左侧的**收缩路径**（contracting path / encoder）和右侧的**扩张路径**（expanding path / decoder）分别起到什么作用？
- (b) U-Net 的跳跃连接与 FCN 的跳跃连接（FCN-8s 中 pool3+pool4 的融合）在**实现方式**上有本质区别。U-Net 使用的是**通道维拼接**（concatenation）而非**逐元素相加**（element-wise addition）。比较这两种融合方式：
  - 参数量和计算开销
  - 信息保留的完整性
  - 对梯度流动的影响
  - 各自更适合什么场景
- (c) 从**信息瓶颈**（information bottleneck）的角度分析：FCN 的 encoder 将输入图像逐层压缩为一个 $1/32$ 分辨率的语义特征向量，然后通过上采样恢复分辨率。为什么这个过程会丢失大量**空间定位信息**（如精细边界、小物体的精确位置）？U-Net 的跳跃连接如何"绕开"这个瓶颈？
- (d) U-Net 原始论文中使用了一种特殊的损失函数——**带边界权重的交叉熵**（weighted cross-entropy with border weight map），对细胞之间的边界像素赋予更高权重。解释这种权重图的计算方式（基于形态学距离变换），以及为什么对细胞分割特别重要。

> [!hint]- 提示 1
> U-Net 架构（典型输入 $572\times572$）：Encoder 每级 = 两个 $3\times3$ Conv（无 padding，所以尺寸逐步缩小）→ $2\times2$ MaxPool；Decoder 每级 = $2\times2$ 上采样 → 与对应 Encoder 级特征 concat → 两个 $3\times3$ Conv。通道数：64 → 128 → 256 → 512 → 1024（bottleneck）→ 512 → 256 → 128 → 64 → 输出 2（二分类）。
> [!hint]- 提示 2
> Concatenation vs Addition：Concat 保留了两个来源的完整信息 → 后续卷积可学习如何选择性融合 → 信息无损但参数多；Addition 假设两个特征图的语义在相同通道上对齐 → 参数少但可能信息被平均/淹没。FCN 用 addition 是因为 pool 特征经 $1\times1$ 降维后语义较接近；U-Net 用 concat 是因为 encoder 特征是低级纹理、decoder 特征是高级语义 → 差异大不宜直接相加。
> [!hint]- 提示 3
> 信息瓶颈：encoder 的池化层将 $H \times W$ 逐次减半 → 在 bottleneck 处空间尺寸仅 $1/32$ 或 $1/16$ → 每个像素需"编码"原图 $32\times32$ 区域的所有信息 → 精细的空间位置信息（如"边界在哪个像素之间"）被不可逆地丢弃。
> [!hint]- 提示 4
> 边界权重图：$w(\mathbf{x}) = w_c(\mathbf{x}) + w_0 \cdot \exp\left(-\frac{(d_1(\mathbf{x}) + d_2(\mathbf{x}))^2}{2\sigma^2}\right)$，其中 $d_1$ 和 $d_2$ 是像素 $\mathbf{x}$ 到最近细胞边界和次近细胞边界的距离。目的：迫使网络"关注"细胞之间的狭窄间隙，避免将相邻接触的细胞合并为一个。
> [!success]- 答案锚点
> (a) 收缩路径（左侧）：逐级提取特征 + 下采样（最大池化）→ 扩大感受野、提取语义层次。扩张路径（右侧）：逐级上采样 + 恢复空间分辨率 → 将语义信息"投射"回高分辨率。U 形对称设计使得每个分辨率层级的 encoder 特征都能直接传递给对应 decoder 层。(b) 对比：

| 维度 | Concat（U-Net） | Addition（FCN） |
|:---|:---|:---|
| 参数 | 更多（后续卷积输入通道翻倍） | 更少（通道数不变） |
| 信息完整性 | 无损保留两个源的全部信息 | 可能信息被平均/覆盖（若两个源语义不对齐） |
| 梯度流动 | 两条独立梯度路径 | 梯度在加法处汇合再分配 |
| 适用场景 | 低级+高级特征差异大时（U-Net encoder 浅层 vs decoder） | 语义相近的特征融合（FCN pool 层经 $1\times1$ 投影后语义较一致） |

(c) FCN encoder 的下采样过程中，每个池化层将空间分辨率减半 → bottleneck 处每个特征向量需"概括"原图 $32\times32$ 区域 → 这种有损压缩丢弃了精细的空间坐标信息（如边界像素的确切位置）→ 上采样只能"猜测"这些丢失的细节（依赖转置卷积学到的模糊模式）。U-Net 的跳跃连接**绕开了 bottleneck**：encoder 浅层的高分辨率特征通过 concat 直接传递给同分辨率的 decoder 层 → decoder 既拥有深层的强语义（通过上采样），又拥有浅层的精确空间位置 → 恢复的边界更清晰。(d) 权重图：$w(\mathbf{x}) = w_c(\mathbf{x}) + w_0 \cdot \exp(-(d_1 + d_2)^2 / 2\sigma^2)$。$w_c$ 平衡类别频率；$d_1, d_2$ 是到最近和次近细胞边界的距离。两个相邻细胞的接触处 → $d_1 \approx d_2 \approx 0$ → 权重极大 → 网络被迫在这些难分的"间隙"区域付出更多注意力 → 防止将两个紧贴的细胞分割为同一个连通域。这对细胞计数、形态分析等下游任务至关重要。

---

### 题 8（计算题）：语义分割评估指标——mIoU 与 Dice 系数

语义分割模型的评估远比分类复杂：需要逐像素比较预测与真值，且需处理类别不平衡。

- (a) 写出**混淆矩阵**（Confusion Matrix）在语义分割中的定义：对于 $C$ 个类别（含背景），混淆矩阵 $\mathbf{M} \in \mathbb{N}^{C \times C}$ 的元素 $M_{ij}$ 表示什么？用一句话定义 True Positive（TP）、False Positive（FP）、False Negative（FN）在语义分割中的含义。
- (b) 给出 **IoU（Jaccard Index）** 对于单类别 $c$ 的计算公式：$\text{IoU}_c = \dfrac{\text{TP}_c}{\text{TP}_c + \text{FP}_c + \text{FN}_c}$。然后定义 **mIoU（mean IoU）**：$\text{mIoU} = \dfrac{1}{C} \sum_{c=1}^{C} \text{IoU}_c$。

  给定以下 3 类分割的混淆矩阵（类别：背景=0、猫=1、狗=2，真值为行、预测为列）：

  | 真值\预测 | 背景 (0) | 猫 (1) | 狗 (2) |
  |:---|:---:|:---:|:---:|
  | 背景 (0) | 850,000 | 5,000 | 8,000 |
  | 猫 (1) | 2,000 | 65,000 | 3,000 |
  | 狗 (2) | 4,000 | 6,000 | 57,000 |

  计算：① 每个类别的 IoU；② mIoU（保留四位小数）；③ 为什么背景类的 IoU 通常比前景类高很多？这对 mIoU 作为评估指标有什么影响？

- (c) **Dice 系数**（F1-score 的变体）是医学图像分割中常用的指标。写出 Dice 系数的公式：$\text{Dice}_c = \dfrac{2 \cdot \text{TP}_c}{2 \cdot \text{TP}_c + \text{FP}_c + \text{FN}_c} = \dfrac{2 |X \cap Y|}{|X| + |Y|}$。推导 Dice 与 IoU 的数学关系：证明 $\text{Dice} = \dfrac{2 \cdot \text{IoU}}{1 + \text{IoU}}$。如果 $\text{IoU} = 0.6$，对应的 Dice 值是多少？
- (d) **像素精度**（Pixel Accuracy）和 mIoU 是两种不同的全局指标。用题 (b) 的混淆矩阵计算像素精度（$\sum_c M_{cc} / \sum_{i,j} M_{ij}$），并解释为什么像素精度在类别极度不平衡时会给出"虚高"的评估结果——即使模型把所有像素都预测为背景类，像素精度仍然很高。为什么 mIoU 能更好地反映模型在少数类上的表现？

> [!hint]- 提示 1
> 混淆矩阵：$M_{ij}$ = 真值为类别 $i$ 但被预测为类别 $j$ 的像素数。对类别 $c$：$\text{TP}_c = M_{cc}$，$\text{FP}_c = \sum_{i \neq c} M_{ic}$（列和减去对角），$\text{FN}_c = \sum_{j \neq c} M_{cj}$（行和减去对角）。
> [!hint]- 提示 2
> 背景 IoU：$\text{TP}_0 = 850{,}000$，$\text{FP}_0 = 2{,}000 + 4{,}000 = 6{,}000$，$\text{FN}_0 = 5{,}000 + 8{,}000 = 13{,}000$ → $\text{IoU}_0 = 850{,}000 / (850{,}000 + 6{,}000 + 13{,}000) \approx 0.9781$。
> [!hint]- 提示 3
> 猫 IoU：$\text{TP}_1 = 65{,}000$，$\text{FP}_1 = 5{,}000 + 6{,}000 = 11{,}000$，$\text{FN}_1 = 2{,}000 + 3{,}000 = 5{,}000$ → $\text{IoU}_1 = 65{,}000 / (65{,}000 + 11{,}000 + 5{,}000) \approx 0.8025$。狗 IoU：$\text{TP}_2 = 57{,}000$，$\text{FP}_2 = 8{,}000 + 3{,}000 = 11{,}000$，$\text{FN}_2 = 4{,}000 + 6{,}000 = 10{,}000$ → $\text{IoU}_2 = 57{,}000 / (57{,}000 + 11{,}000 + 10{,}000) \approx 0.7308$。mIoU = (0.9781 + 0.8025 + 0.7308) / 3 ≈ 0.8371。
> [!hint]- 提示 4
> 像素精度 = (850k + 65k + 57k) / (850k + 5k + 8k + 2k + 65k + 3k + 4k + 6k + 57k) = 972k / 1M = 0.972。Dice 与 IoU 关系：从 $\text{Dice} = 2\text{TP}/(2\text{TP}+\text{FP}+\text{FN})$ 和 $\text{IoU} = \text{TP}/(\text{TP}+\text{FP}+\text{FN})$，令 $S = \text{FP}+\text{FN}$ → $\text{Dice} = 2\text{TP}/(2\text{TP}+S)$，$\text{IoU} = \text{TP}/(\text{TP}+S)$ → 消去 $S$ 得 $\text{Dice} = 2\text{IoU}/(1+\text{IoU})$。
> [!success]- 答案锚点
> (a) $M_{ij}$ = 真值为类别 $i$ 但被预测为类别 $j$ 的像素总数。TP：真值为 $c$ 且预测为 $c$ 的像素；FP：真值非 $c$ 但预测为 $c$ 的像素；FN：真值为 $c$ 但预测非 $c$ 的像素。(b) ① 各 IoU：

- $\text{IoU}_{\text{bg}} = 850{,}000 / (850{,}000 + 6{,}000 + 13{,}000) = 850{,}000 / 869{,}000 \approx 0.9781$
- $\text{IoU}_{\text{cat}} = 65{,}000 / (65{,}000 + 11{,}000 + 5{,}000) = 65{,}000 / 81{,}000 \approx 0.8025$
- $\text{IoU}_{\text{dog}} = 57{,}000 / (57{,}000 + 11{,}000 + 10{,}000) = 57{,}000 / 78{,}000 \approx 0.7308$

② $\text{mIoU} = (0.9781 + 0.8025 + 0.7308) / 3 \approx 0.8371$。③ 背景像素占比极大（~86%），模型只要"倾向预测背景"即可获得很高的背景 TP 且 FP/FN 低。这对 mIoU 的影响：背景类 IoU 拉高了 mIoU 均值，可能掩盖前景类的分割质量问题。改进方法：计算 **mIoU without background**（仅前景类的均值）或使用频率加权 IoU（FW-IoU）。

(c) 推导：令 $S = \text{FP} + \text{FN}$，$\text{IoU} = \frac{\text{TP}}{\text{TP} + S}$，则 $S = \frac{\text{TP}}{\text{IoU}} - \text{TP}$。代入 Dice：$\text{Dice} = \frac{2\text{TP}}{2\text{TP} + S} = \frac{2\text{TP}}{2\text{TP} + \frac{\text{TP}}{\text{IoU}} - \text{TP}} = \frac{2\text{TP}}{\text{TP} + \frac{\text{TP}}{\text{IoU}}} = \frac{2}{1 + 1/\text{IoU}} = \frac{2\text{IoU}}{1 + \text{IoU}}$。当 $\text{IoU}=0.6$：$\text{Dice} = 2 \times 0.6 / 1.6 = 0.75$。Dice 始终 $\geq$ IoU（当 IoU=0 时 Dice=0；IoU=1 时 Dice=1）。

(d) 像素精度 = $(850{,}000 + 65{,}000 + 57{,}000) / 1{,}000{,}000 = 972{,}000 / 1{,}000{,}000 = 0.972$。虚高原因：如果模型把全部像素预测为背景 → TP$_{\text{bg}}$ = 863,000（背景总像素），TP$_{\text{cat}}$ = TP$_{\text{dog}}$ = 0 → 像素精度 = 863,000/1,000,000 = 86.3% — 看起来还不错，但实际上猫和狗完全没检测到。mIoU 在这种情况下：猫 IoU = 0，狗 IoU = 0，背景 IoU ≈ 0.86 → mIoU ≈ 0.29，真实反映了模型在少数类上的失败。因此 mIoU 对类别不平衡更敏感，是更诚实的评估指标。

---

## 错因与重测

| 题号 | 错因 | 作答前信心 | 补救页 | 24h | 72h | 7d | 作答后信心 |
|:---|:---|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 2 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 3 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 4 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 5 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 6 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 7 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |
| 8 | 概念 / 运算 / 粗心 / — | | | ☐ | ☐ | ☐ | |

---

## 外部原题索引

| D2L 节 | 原 Exercises 链接 | 改编题号 |
|:---|:---|:---:|
| 14.3 Object Detection and Bounding Boxes | [bounding-box.html#exercises](https://d2l.ai/chapter_computer-vision/bounding-box.html#exercises) | 题1, 题2 |
| 14.4 Anchor Boxes | [anchor.html#exercises](https://d2l.ai/chapter_computer-vision/anchor.html#exercises) | 题2 |
| 14.5 Multiscale Object Detection | [multiscale-object-detection.html#exercises](https://d2l.ai/chapter_computer-vision/multiscale-object-detection.html#exercises) | 题4 |
| 14.7 Single Shot Multibox Detection (SSD) | [ssd.html#exercises](https://d2l.ai/chapter_computer-vision/ssd.html#exercises) | 题3, 题4, 题5 |
| 14.8 Region-based CNNs (R-CNNs) | [rcnn.html#exercises](https://d2l.ai/chapter_computer-vision/rcnn.html#exercises) | 题3 |
| 14.9 Semantic Segmentation and the Dataset | [semantic-segmentation-and-dataset.html#exercises](https://d2l.ai/chapter_computer-vision/semantic-segmentation-and-dataset.html#exercises) | 题8 |
| 14.10 Transposed Convolution | [transposed-conv.html#exercises](https://d2l.ai/chapter_computer-vision/transposed-conv.html#exercises) | 题6 |
| 14.11 Fully Convolutional Networks | [fcn.html#exercises](https://d2l.ai/chapter_computer-vision/fcn.html#exercises) | 题6 |
| 14.12 Neural Style Transfer | —（本节偏生成，未编入本册） | — |
| 14.13 Image Classification (CIFAR-10) on Kaggle | —（竞赛实战，未编入本册） | — |
| —（跨节综合） | 锚框生成 + NMS + 多尺度检测 综合 | 题1-5 |
| —（跨节综合） | 语义分割：FCN + U-Net + 评估指标 综合 | 题6-8 |
