---
type: study
course: "05-计算机视觉"
topic: "IoU 与 NMS (交并比与非极大值抑制)"
created: 2026-08-06
status: ongoing
difficulty: intermediate
concept: ["IoU", "NMS", "目标检测", "边界框", "后处理"]
prerequisites: ["目标检测RCNN与YOLO"]
related: ["FPN", "FocalLoss", "FasterRCNN"]
flow: knowledge
upstream: ["[[目标检测RCNN与YOLO]]"]
stage_moc: "[[🧭 阶段3-视觉核心任务]]"
kind: concept
source: "CS231n Lecture 11; D2L Ch.14"
tags: [学习, 计算机视觉, 目标检测, IoU, NMS]
---

# IoU 与 NMS (交并比与非极大值抑制)

> 所属模块：[[🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[🧭 阶段3-视觉核心任务|第三阶段：视觉核心任务]]
> 建议先看：[[目标检测RCNN与YOLO]]

---

## 0. 学习边界

- **类别**：**A 类（核心概念）** — IoU 和 NMS 是目标检测的"度量衡"和"筛子"。无论 R-CNN 还是 YOLO，都离不开这两个操作。

---

## 1. IoU：交并比

### 定义

两个边界框 A 和 B 的 IoU：

$$\text{IoU}(A, B) = \frac{|A \cap B|}{|A \cup B|}$$

- 值域：$[0, 1]$
- **IoU = 1**：完全重叠
- **IoU = 0**：完全不重叠
- 常用阈值：**IoU ≥ 0.5** 视为正检测（PASCAL VOC 标准）

### 计算

```python
def compute_iou(boxA, boxB):
    # box format: (x1, y1, x2, y2)
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    
    inter_area = max(0, xB - xA) * max(0, yB - yA)
    areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    
    return inter_area / (areaA + areaB - inter_area + 1e-6)

# 验证示例
box1 = [10, 20, 50, 60]   # (10,20) → (50,60), 面积=1600
box2 = [30, 40, 70, 80]   # (30,40) → (70,80), 面积=1600
# 交集：(30,40)→(50,60), 面积=400
# 预期 IoU = 400 / (1600+1600-400) = 400/2800 ≈ 0.143
print(f"IoU = {compute_iou(box1, box2):.3f}")  # 预期 0.143

box3 = [10, 20, 50, 60]   # 与 box1 完全相同
print(f"IoU(identical) = {compute_iou(box1, box3):.3f}")  # 预期 1.000
```

### IoU 的局限与改进

标准 IoU 有两个致命缺陷：

1. **无重叠时始终为 0**，无法区分"完全不重叠"和"差一点就重叠"
2. **不反映重叠方式**：中心对齐 vs 边角擦过，IoU 可能相同

| 改进版本 | 额外度量 | 公式思路 | 何时用 |
|:---|:---|:---|:---|
| **GIoU** | 最小闭包面积 | $\text{IoU} - \frac{\|C - (A \cup B)\|}{\|C\|}$ | 通用改进，解决无重叠问题 |
| **DIoU** | 中心点距离 | $\text{IoU} - \frac{\rho^2(b_A, b_B)}{c^2}$ | 需要更快收敛的边界框回归 |
| **CIoU** | + 长宽比 | DIoU + $\alpha v$（长宽比一致性） | 精确的边界框回归 Loss |

> **实践建议**：边界框回归 Loss 用 CIoU Loss（YOLOv4/v5 默认），评估仍用标准 IoU（与论文可比）。

---

## 2. NMS：非极大值抑制

### 问题

检测器对同一个物体可能输出多个重叠的边界框（不同 anchor/尺度的重复检测）。每个框有置信度 score。

### 算法

```
输入：框列表 boxes（按 score 降序排序），IoU 阈值 τ
输出：保留的框列表

1. 选 score 最高框 M，加入保留列表
2. 计算 M 与其余框的 IoU
3. 移除 IoU ≥ τ 的框（认为它们是 M 的重复）
4. 重复 1-3 直到没有框剩余
```

### 代码

```python
def nms(boxes, scores, iou_threshold=0.5):
    order = scores.argsort()[::-1]  # 按 score 降序
    keep = []
    while len(order) > 0:
        i = order[0]
        keep.append(i)
        if len(order) == 1:
            break
        ious = np.array([compute_iou(boxes[i], boxes[j]) for j in order[1:]])
        order = order[1:][ious < iou_threshold]
    return keep
```

---

## 3. mAP 中的 IoU 角色

**mAP (mean Average Precision)** 是检测的核心指标：

1. 对每个预测框，与所有 GT 框计算 IoU
2. **IoU ≥ 0.5 → TP**（真正例）；否则 → FP（假正例）
3. 绘制 PR 曲线，计算 AP
4. 对所有类别 AP 取平均 → mAP

**COCO 更严格**：计算 mAP@[0.5:0.95]，即 IoU 阈值从 0.5 到 0.95 步进 0.05 的平均。

---

## 4. NMS 的变体

### Greedy NMS（标准）
直接删除 IoU ≥ τ 的框。简单高效，但会误删密集场景中重叠的不同物体。

### Soft-NMS

不直接删除，而是用**衰减函数**降低重叠框的 score：

$$s_j = s_j \cdot f(\text{IoU}(M, b_j))$$

两种衰减函数：

| 衰减函数 | 公式 | 特点 |
|:---|:---|:---|
| **线性** | $f(x) = 1 - x$（$x \geq \tau$） | 简单，但高于阈值的框被直接置零 |
| **高斯** | $f(x) = e^{-x^2/\sigma}$ | 平滑衰减，重叠越严重 score 越低 |

```python
def soft_nms(boxes, scores, iou_threshold=0.5, sigma=0.5, method='gaussian'):
    """Soft-NMS 简化实现"""
    order = scores.argsort()[::-1]
    keep = []
    while len(order) > 0:
        i = order[0]
        keep.append(i)
        if len(order) == 1:
            break
        ious = np.array([compute_iou(boxes[i], boxes[j]) for j in order[1:]])
        if method == 'linear':
            weights = np.where(ious >= iou_threshold, 1 - ious, 1.0)
        else:  # gaussian
            weights = np.exp(-(ious ** 2) / sigma)
        scores[order[1:]] *= weights
        # 移除 score 过低的框
        order = order[1:][scores[order[1:]] > 0.001]
    return keep
```

### 方法对比

| 方法 | 特点 | 适用场景 |
|:---|:---|:---|
| **Greedy NMS** | 标准算法，简单高效 | 物体稀疏的场景 |
| **Soft-NMS** | 保留密集场景中重叠物体 | 行人检测、拥挤场景 |
| **Class-Agnostic NMS** | 不考虑类别，所有框一起做 | 类别数少时使用 |
| **Class-Aware NMS** | 每个类别独立 NMS | **推荐默认**，避免跨类误删 |

---

## 5. 常见误区与失败模式

| 问题 | 原因 | 修复 |
|:---|:---|:---|
| NMS 阈值过低删除了正确检测 | τ 太小（如 0.3） | 提高到 0.5-0.7；或用 Soft-NMS |
| 密集场景漏检 | 同类物体靠太近，Greedy NMS 误删 | 用 Soft-NMS 或降低 τ |
| "同一个物体被多次检测"（即使 NMS 后） | NMS 未覆盖所有类别，跨类重复 | 确认使用 Class-Aware NMS |
| mAP 虚高 | 评估用 IoU@0.5 太松 | 用 COCO mAP@[0.5:0.95] 更严格 |
| 边界框回归 Loss 不收敛 | 用标准 IoU Loss，无重叠时梯度为 0 | 改用 GIoU/DIoU/CIoU Loss |

### 常见误区

- ❌ "NMS 阈值设得越低越好" — 太低会把不同物体的框也删掉，导致召回率下降
- ❌ "IoU = 0.5 就是好检测" — COCO 标准更严（mAP@0.75 通常远低于 mAP@0.5）
- ❌ "NMS 可以替代更好的检测头设计" — 端到端方法（如 DETR 用匈牙利匹配）试图消除 NMS
- ❌ "用更大的 IoU 阈值训练会让模型更好" — 太高的阈值（如 0.9）让正样本太少，训练不稳定

---

## 🧪 自测题

1. **(基础)** 两个完全不重叠的框，IoU 是多少？NMS 中 IoU 阈值设为 0.5 意味着什么？
   <details><summary>💡 思路</summary>先按 IoU 定义算交集面积为 0 时的取值；再想阈值 $\tau$ 在 NMS 中的判定语义——它决定了「多大重叠算同一个物体」。</details>

2. **(中等)** NMS 的 IoU 阈值设得太低会有什么问题？设得太高呢？
   <details><summary>💡 思路</summary>分别设想两个极端：$\tau \to 0$ 与 $\tau \to 1$ 时 NMS 会保留多少框，再判断各自抬高的是假阳性还是假阴性。</details>

3. **(中等)** Soft-NMS 相比 Greedy NMS 的核心改进是什么？在什么场景下改善最显著？
   <details><summary>💡 思路</summary>对比两者对「被抑制框」的处理动作（直接删除 vs 平滑降分）；再想哪类场景下同类物体本身就高度重叠，删除策略会误伤。</details>

4. **(较难)** 为什么标准 IoU 不适合直接作为边界框回归的 Loss 函数？GIoU 如何解决这个问题？
   <details><summary>💡 思路</summary>先考察当 IoU=0 时，损失关于框坐标的导数是多少；再看 GIoU 额外引入的最小闭包项在两框不重叠时是否仍随距离变化。</details>


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

