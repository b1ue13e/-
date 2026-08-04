---
title: "YOLO 目标检测算法 (You Only Look Once)"
course: "05-计算机视觉"
tags:
  - 计算机视觉
  - YOLO
  - 目标检测
  - 单阶段检测
  - NMS
  - Anchor
type: knowledge_card
status: completed
created: 2026-07-31
---

# YOLO 目标检测算法 (You Only Look Once)

## 1. YOLO 目标检测算法的定义与单阶段突破

**YOLO 目标检测算法 (You Only Look Once)** 的核心定义是：将目标检测任务直接重构为**单阶段 (One-Stage) 端到端回归问题**的实时目标检测框架。YOLO 目标检测算法由 Redmon 等人于 2015 年在 CVPR 提出。

**基本性质与单阶段突破**：传统两阶段 (Two-Stage) 检测器（如 Faster R-CNN）先由 RPN 生成候选框 (Region Proposals)，再对分类与回归进行二次计算，速度受限（~5-7 FPS）。YOLO 目标检测算法仅需对全图进行**单次前向传播 (Single Forward Pass)**，即可并发预测出整张图像中所有目标的边界框 (Bounding Box) 物理坐标与类别概率，实现高达 45~155 FPS 的超实时检测。

---

## 2. 网格划分、损失函数与非极大值抑制 (NMS) 形式化推导

**网格划分 (Grid Cell) 与输出张量推导**：
1. 将输入图像划分为 $S \times S$ 个网格（如 $7 \times 7$）；
2. 若目标中心落在某个网格内，则该网格负责检测该目标；
3. 每个网格预测 $B$ 个 Bounding Box，每个 Box 包含 5 个预测值：$(x, y, w, h, c)$，其中 $c$ 为置信度 $\text{Pr}(\text{Object}) \times \text{IoU}_{\text{pred}}^{\text{truth}}$；
4. 输出张量维度为 $S \times S \times (B \times 5 + C)$（$C$ 为类别数）。

**多任务复合损失函数 (Multi-Part Loss)**：
$$L_{\text{YOLO}} = \lambda_{\text{coord}} \sum_{i=0}^{S^2} \sum_{j=0}^B \mathbb{I}_{ij}^{\text{obj}} \left[ (x_i - \hat{x}_i)^2 + (y_i - \hat{y}_i)^2 + (\sqrt{w_i} - \sqrt{\hat{w}_i})^2 + (\sqrt{h_i} - \sqrt{\hat{h}_i})^2 \right]$$
$$+ \sum_{i=0}^{S^2} \sum_{j=0}^B \mathbb{I}_{ij}^{\text{obj}} (C_i - \hat{C}_i)^2 + \lambda_{\text{noobj}} \sum_{i=0}^{S^2} \sum_{j=0}^B \mathbb{I}_{ij}^{\text{noobj}} (C_i - \hat{C}_i)^2 + \sum_{i=0}^{S^2} \mathbb{I}_i^{\text{obj}} \sum_{c \in \text{classes}} (p_i(c) - \hat{p}_i(c))^2$$

**NMS (Non-Maximum Suppression) 消除冗余框**：
对所有得分高于阈值的框按 Score 排序，挑选最高分框 $B_{\text{max}}$，计算其他框与 $B_{\text{max}}$ 的 $\text{IoU}$，剔除 $\text{IoU} > \text{Threshold}$ 的重叠框，重复迭代。

---

## 3. 单阶段 (YOLO) 与两阶段 (Faster R-CNN) 检测器对比

| 维度 | YOLO 单阶段检测器 | Faster R-CNN 两阶段检测器 |
|:---|:---|:---|
| **预测范式** | 全图单次回归预测 | RPN 生成候选区 $\to$ ROI Pooling $\to$ 2nd 头部 |
| **推理速度** | **超实时 (45 - 160+ FPS)** | 较慢 (5 - 15 FPS) |
| **背景误报 (Background Error)** | **低**（看全图，全局上下文好）| 较高（只看局部 Proposal 易把背景认错）|
| **小目标定位精度** | 早期版本稍低（受限网格） | 较高（多尺度特征融合与 ROI 对齐） |
| **代表演进版本** | YOLOv1~v8, YOLOX | Fast / Faster / Mask R-CNN |

**局限（误区）**：早期 YOLOv1 每个网格最多检测一个目标，在面对密集小目标群（如成群飞鸟）时存在定位瓶颈；后来的 YOLOv2/v3 引入了 **Anchor Boxes** 与 **FPN 多尺度预测**，彻底解决了小目标检测难题。

关联知识点推荐：[[卷积神经网络CNN]]、[[ResNet残差网络]]、[[交叉熵损失函数]]、[[均方误差MSE与Huber损失]]。

---

## 4. Python IoU (交并比) 计算与 NMS 算法自测断言

```python
import numpy as np

def compute_iou(box1: np.ndarray, box2: np.ndarray) -> float:
    """计算两个矩形框的 IoU"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    union_area = box1_area + box2_area - inter_area
    return float(inter_area / union_area) if union_area > 0 else 0.0

def nms_suppression(boxes: np.ndarray, scores: np.ndarray, iou_threshold: float = 0.5) -> list:
    """非极大值抑制 NMS"""
    idxs = np.argsort(scores)[::-1]
    keep = []

    while len(idxs) > 0:
        current = idxs[0]
        keep.append(current)
        if len(idxs) == 1:
            break
        rem_idxs = idxs[1:]
        ious = np.array([compute_iou(boxes[current], boxes[i]) for i in rem_idxs])
        idxs = rem_idxs[ious <= iou_threshold]

    return keep

if __name__ == "__main__":
    b1 = np.array([0, 0, 10, 10])
    b2 = np.array([0, 0, 10, 10])
    assert compute_iou(b1, b2) == 1.0

    b3 = np.array([5, 0, 15, 10])
    iou_val = compute_iou(b1, b3)
    assert abs(iou_val - 1/3) < 1e-4

    boxes = np.array([[0,0,10,10], [1,1,10,10], [100,100,110,110]])
    scores = np.array([0.9, 0.8, 0.95])
    keep_indices = nms_suppression(boxes, scores, iou_threshold=0.5)
    assert set(keep_indices) == {0, 2}

    print(f"YOLO 目标检测算法 IoU 验证成功: 重叠度 = {iou_val:.4f}")
    print(f"YOLO 目标检测算法 NMS 抑制成功: 原始 3 个候选框降至 {keep_indices}")
    print("YOLO 目标检测算法单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016). You only look once: Unified, real-time object detection (YOLOv1). *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR '16)*, 779-788. DOI: https://doi.org/10.1109/CVPR.2016.91 URL: https://arxiv.org/abs/1506.02640
- Redmon, J., & Farhadi, A. (2017). YOLO9000: Better, faster, stronger (YOLOv2). *IEEE CVPR '17*, 7263-7271. DOI: https://doi.org/10.1109/CVPR.2017.690 URL: https://arxiv.org/abs/1612.08242
- Redmon, J., & Farhadi, A. (2018). YOLOv3: An incremental improvement. *arXiv preprint arXiv:1804.02767*. URL: https://arxiv.org/abs/1804.02767
- Ren, S., He, K., Girshick, R., & Sun, J. (2015). Faster R-CNN: Towards real-time object detection with region proposal networks. *IEEE TPAMI*, 39(6), 1137-1149. DOI: https://doi.org/10.1109/TPAMI.2016.2577031
