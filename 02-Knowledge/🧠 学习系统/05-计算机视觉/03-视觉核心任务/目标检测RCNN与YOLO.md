---
type: study
course: "05-计算机视觉"
topic: "目标检测基础：R-CNN与YOLO"
created: 2026-08-05
status: ongoing
difficulty: intermediate
concept: ["目标检测","R-CNN","YOLO","IoU","NMS","mAP"]
prerequisites: ["卷积神经网络CNN","Softmax分类器"]
related: ["FPN","SSD","FasterRCNN","语义分割"]
flow: knowledge
stage_moc: "[[03-视觉核心任务/🎯 第三阶段：视觉核心任务]]"
kind: concept
source: "D2L Ch.14; CS231n A3"
anki_deck: "05-计算机视觉::03-视觉核心任务"
anki_tags: ["计算机视觉","目标检测","RCNN","YOLO"]
tags: [学习,计算机视觉,目标检测,RCNN,YOLO]
---

# 目标检测基础：R-CNN与YOLO

> 所属模块：[[../🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[02-Knowledge/🧠 学习系统/05-计算机视觉/03-视觉核心任务/🎯 第三阶段：视觉核心任务|返回阶段页]]
> 建议先看：[[卷积神经网络CNN]]、[[Softmax分类器]]
> 辅助教材：`《动手学深度学习》Ch.14`、`CS231n Assignment 3`

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心范式，必须深挖）**。
- **判断理由**：目标检测是计算机视觉中兼具理论深度与工程价值的核心任务——从自动驾驶的障碍物感知到安防监控的人脸锁定，都依赖检测算法。R-CNN 系列奠定了 Two-Stage 的精度标杆，YOLO 系列开创了 One-Stage 的实时范式——理解二者演进逻辑就等于掌握了检测领域半部发展史。IoU/NMS/mAP 三大工具是任何检测任务的"标配"，漏掉任何一个都无法独立评估和调试检测模型。

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：图像分类只能回答"图里有什么"（一张图一个标签），但真实世界需要同时回答"哪里有东西、有什么东西、每个东西的精确边界在哪里"。自动驾驶需要知道前方 3 辆车各自在哪、是什么；安防需要锁定画面中每个行人的精确包围框。

目标检测核心问题：

> **给定一张输入图像，如何同时输出所有目标实例的类别标签和精确的边界框 (Bounding Box) 坐标？**

它比分类难在四个维度：
1. **数量未知**：图中目标数不固定（0～N 个），输出维度必须动态变化。
2. **定位 + 分类耦合**：每个预测须同时给出"类别"和"位置"，二者相互依赖——位置不准则分类上下文错误。
3. **尺度变化极端**：同一张图可能同时出现占画面 80% 的大目标与仅 10 像素的小目标。
4. **重叠与遮挡**：密集场景下多个目标互相遮挡，需要区分单个实例。

## 2. 为什么它重要？它有什么用？

- **连接大图景**：目标检测是分类（回答"是什么"）向定位（回答"在哪里+是什么"）的演化第一站，向上推动实例分割（Mask R-CNN）、目标跟踪、多目标跟踪（MOT）等任务；向下依赖 CNN backbone、特征金字塔（FPN）等基础设施。
- **实际应用**：自动驾驶（车辆/行人/交通标志检测）、安防监控（人脸检测、异常行为定位）、医疗影像（病灶/结节检测与定位）、零售（货架商品识别与计数）、遥感（舰船/建筑物检测）。
- **高频题型**：R-CNN → Fast → Faster 演进解决了什么瓶颈；YOLO 网格预测与 RPN 的本质区别；IoU 定义与计算；NMS 算法步骤与代码；mAP 含义及计算流程；Two-Stage vs One-Stage 精度/速度 trade-off 分析。

## 3. 学它之前需要哪些前置知识？

1. **卷积神经网络 CNN**：理解 backbone 特征提取——浅层捕获边缘/纹理，深层捕获语义部件，这是 RPN 和 YOLO 共享的视觉前端。
2. **Softmax 分类器与交叉熵损失**：检测的分类子任务（类别预测）依赖 Softmax 输出。
3. **边界框回归基础**：理解 $(x, y, w, h)$ 或 $(x_1, y_1, x_2, y_2)$ 坐标表示，以及回归损失（Smooth L1 / MSE）的基本概念。
4. **SGD 与损失函数**：理解多任务损失联合优化（分类损失 + 回归损失加权求和）。

## 4. 用直觉语言解释它

> "图像分类像是在机场广播'张三旅客请注意'——你只听到一个人名。目标检测则像全景雷达扫描：屏幕上同时闪烁 15 个光点，每个光点标注了它是什么（飞机/鸟/无人机）和精确坐标。"

- **Two-Stage（R-CNN 系列）直觉**：先"圈地"再"审问"——第一阶段用某种方式在图上圈出几千个"嫌疑区域"（可能有物体的地方），第二阶段对每个区域仔细分类和精修边界。像海关安检：先快速扫描包裹可疑区，再对可疑区开箱细查。**精度高但慢**。
- **One-Stage（YOLO）直觉**：一眼看清整张图——把图分成 $S \times S$ 网格，每个格子同时预测"这里有没有目标中心、目标是什么、边界框多大"。不需要中间"圈地"步骤。像老练的雷达操作员：看屏幕一眼就知道每个光点是什么、在哪。**快但早期精度稍低**。
- **IoU 直觉**：两个框的"重叠程度"，从 0（完全不重叠）到 1（完全重合）。检测中 0.5 的 IoU 约等于"框住了目标大半"。
- **NMS 直觉**：同一个目标上可能叠着十几个高度重叠的预测框——NMS 保留得分最高的那个，删除所有与它重叠过多的"山寨框"。
- **一句话本质**：目标检测 = 在全图上同时求解"有哪些东西、每个东西在哪"这两个耦合问题——Two-Stage 分步解耦求解，One-Stage 一步联合求解。

## 5. 正式定义、核心公式、符号解释

### 5.1 目标检测 vs 图像分类的形式化区别

| 维度 | 图像分类 | 目标检测 |
|:---|:---|:---|
| 输出 | 单一标签 $y \in \{1,\dots,C\}$ | 可变长集合 $\{(c_k, \mathbf{b}_k)\}_{k=1}^{K}$，$K$ 未知 |
| 标签结构 | 标量 | 类别 $c_k$ + 四元组 $\mathbf{b}_k = (x, y, w, h)$ |
| 评估 | Accuracy | mAP（综合考虑分类正确 + 定位精度） |
| 输出维度 | 固定（$C$） | 动态（取决于图中目标数） |

### 5.2 Two-Stage 检测器：R-CNN → Fast R-CNN → Faster R-CNN

#### R-CNN（2014）——朴素两阶段

**流程**：
1. **Selective Search**：基于颜色/纹理/尺寸相似度，在输入图上生成 ~2000 个类别无关的候选区域 (Region Proposals)。
2. **CNN 特征提取**：每个候选区域 warp 到固定尺寸（227×227），分别送入 CNN（AlexNet）提取 4096 维特征向量。
3. **SVM 分类 + 边界框回归**：每个区域的特征送类别特定 SVM 打分，同时用岭回归精修边界框。

**致命缺陷**：
- 每张图 ~2000 次 CNN 前向传播 → 极慢（GPU 下 ~13s/图）。
- 训练多阶段分离：CNN 预训练 → SVM 训练 → 回归器训练，无法端到端。
- Selective Search 固定不可学习。

#### Fast R-CNN（2015）——共享卷积 + RoI Pooling

**核心改进**：
1. **全图单次 CNN**：整张图只过一遍 CNN → 得到共享特征图，候选区域映射到特征图上裁剪对应区域。
2. **RoI Pooling**：将任意尺寸的候选区域特征统一池化到固定 $H \times W$（如 $7 \times 7$），使全连接层可接受变尺寸输入。
3. **多任务联合损失**（端到端训练）：
   $$L(p, u, t^u, v) = L_{\text{cls}}(p, u) + \lambda \cdot \mathbb{I}[u \ge 1] \cdot L_{\text{loc}}(t^u, v)$$
   其中 $L_{\text{cls}}$ 为 Softmax 交叉熵（$C+1$ 类，含背景），$L_{\text{loc}}$ 为 Smooth L1 损失。

**速度**：~3s/图（仍受 Selective Search 瓶颈制约）。

**Smooth L1 损失**（比 L2 对离群点更鲁棒）：
$$\text{smooth}_{L_1}(x) = \begin{cases} 0.5x^2 & \text{if } |x| < 1 \\ |x| - 0.5 & \text{otherwise} \end{cases}$$

#### Faster R-CNN（2015）——RPN 实现全网络化

**核心突破**：用可学习的**区域提议网络 (Region Proposal Network, RPN)** 取代固定算法 Selective Search，首次实现检测全流程端到端训练。

**RPN 设计**：
1. 在共享特征图上滑动 $n \times n$ 窗口（$n=3$），每个位置生成 $k$ 个 **Anchor Boxes**（预设不同尺度和长宽比的参考框）。
2. 每个 Anchor 预测两个输出：
   - **二分类**：该 Anchor 是否包含目标（Objectness Score）。
   - **回归**：Anchor 相对于真实框的偏移量 $(t_x, t_y, t_w, t_h)$。

**Anchor 偏移编码**：
$$t_x = \frac{x - x_a}{w_a},\quad t_y = \frac{y - y_a}{h_a},\quad t_w = \log\frac{w}{w_a},\quad t_h = \log\frac{h}{h_a}$$

其中 $(x_a, y_a, w_a, h_a)$ 为 Anchor 坐标，$(x, y, w, h)$ 为真实框坐标。

**RPN 训练**：正样本（IoU > 0.7 或最高 IoU 的 Anchor）vs 负样本（IoU < 0.3），保持正负比 1:1，每 batch 256 个 Anchor。

**Faster R-CNN 总损失**：
$$L = L_{\text{RPN\_cls}} + L_{\text{RPN\_reg}} + L_{\text{FastRCNN\_cls}} + L_{\text{FastRCNN\_reg}}$$

### 5.3 One-Stage 检测器：YOLO（You Only Look Once）

**核心思想**：将检测重构为**全图单次回归问题**——无需 RPN、无需 RoI Pooling，直接在输出特征图上预测边界框和类别。

#### YOLOv1 网格预测

1. 将输入图划分为 $S \times S$ 网格（如 $7 \times 7$）。
2. 若目标中心落在某网格内，该网格"负责"检测该目标。
3. 每个网格预测 $B$ 个边界框（$B=2$），每框含 5 个值：$(x, y, w, h, c)$，其中 $c = \text{Pr}(\text{Object}) \times \text{IoU}_{\text{pred}}^{\text{truth}}$（置信度）。
4. 输出张量维度：$S \times S \times (B \cdot 5 + C)$，其中 $C$ 为类别数（VOC 上 $C=20$ → 输出 $7 \times 7 \times 30$）。

**YOLO 多任务复合损失**：
$$L = \lambda_{\text{coord}} \sum_{i=0}^{S^2} \sum_{j=0}^B \mathbb{I}_{ij}^{\text{obj}} \left[(x_i - \hat{x}_i)^2 + (y_i - \hat{y}_i)^2\right]$$
$$+ \lambda_{\text{coord}} \sum_{i=0}^{S^2} \sum_{j=0}^B \mathbb{I}_{ij}^{\text{obj}} \left[(\sqrt{w_i} - \sqrt{\hat{w}_i})^2 + (\sqrt{h_i} - \sqrt{\hat{h}_i})^2\right]$$
$$+ \sum_{i=0}^{S^2} \sum_{j=0}^B \mathbb{I}_{ij}^{\text{obj}} (C_i - \hat{C}_i)^2 + \lambda_{\text{noobj}} \sum_{i=0}^{S^2} \sum_{j=0}^B \mathbb{I}_{ij}^{\text{noobj}} (C_i - \hat{C}_i)^2$$
$$+ \sum_{i=0}^{S^2} \mathbb{I}_i^{\text{obj}} \sum_{c \in \text{classes}} (p_i(c) - \hat{p}_i(c))^2$$

其中 $\lambda_{\text{coord}} = 5$（放大定位损失权重），$\lambda_{\text{noobj}} = 0.5$（减小无目标网格的置信度惩罚）。$\sqrt{w}, \sqrt{h}$ 使用平方根缓解大框对小偏差不敏感的问题。

#### YOLO 后续演进要点

| 版本 | 核心改进 | 关键贡献 |
|:---|:---|:---|
| YOLOv2/v3 | 引入 Anchor Boxes + FPN 多尺度预测 | 解决小目标漏检，mAP 从 63.4 跃升至 57.9 (COCO) |
| YOLOv5/v8 | 工程优化（CSPNet、CIoU Loss、数据增强） | 工业落地标准方案 |

### 5.4 IoU（交并比）定义与计算

**定义**：两个边界框 $A$ 和 $B$ 的交集面积与并集面积之比。

$$\text{IoU}(A, B) = \frac{|A \cap B|}{|A \cup B|} = \frac{|A \cap B|}{|A| + |B| - |A \cap B|}$$

**性质**：
- 取值范围 $[0, 1]$，值越大重叠度越高。
- IoU = 1 表示完全重合，IoU = 0 表示无交集。
- 检测中常用 IoU > 0.5 作为"正确检测"阈值（TP 的条件）。

### 5.5 NMS（非极大值抑制）算法

**目的**：同一目标上多个高度重叠的预测框中，只保留置信度最高的那个，剔除冗余。

**标准 NMS 流程**：

```
输入：边界框列表 B = [b1, ..., bN]，置信度分数 S = [s1, ..., sN]，IoU 阈值 τ
输出：保留的框索引列表 keep

1. 按 S 降序排序 B
2. keep = []
3. while B 非空:
   a. 取出 B[0]（当前最高分框），加入 keep
   b. 计算 B[0] 与 B 中其余所有框的 IoU
   c. 删除所有 IoU > τ 的框
   d. B = 剩余框（不包含 B[0]）
4. return keep
```

**Soft-NMS**（改进变体）：不直接删除高 IoU 框，而是降低其分数 $s_i = s_i \cdot e^{-\text{IoU}(M, b_i)^2 / \sigma}$，对密集场景更友好。

### 5.6 mAP（mean Average Precision）评估指标

**Precision-Recall 基础**：对于给定 IoU 阈值（如 0.5）和置信度阈值，定义：
- **TP**：预测框与真实框 IoU ≥ 阈值，且类别正确。
- **FP**：预测框与任何真实框 IoU < 阈值，或类别错误。
- **FN**：未被任何预测框匹配的真实框。

$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}, \quad \text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$

**AP 计算（VOC 2007 11-point 插值法）**：对 Recall $\in [0, 0.1, \dots, 1.0]$ 的 11 个等分点，取该点右侧最大 Precision 的均值：
$$\text{AP} = \frac{1}{11} \sum_{r \in \{0, 0.1, \dots, 1\}} \max_{\tilde{r} \ge r} P(\tilde{r})$$

**mAP**：所有类别 AP 的平均值。COCO 进一步在多个 IoU 阈值（0.50～0.95，步长 0.05）下取均值，记为 mAP@[.50:.95]。

**COCO 风格关键指标**：

| 指标 | 含义 |
|:---|:---|
| $\text{mAP}^{@0.5}$ | IoU=0.5 时的 mAP（宽松匹配） |
| $\text{mAP}^{@0.75}$ | IoU=0.75 时的 mAP（严格匹配） |
| $\text{mAP}_S, \text{mAP}_M, \text{mAP}_L$ | 小/中/大目标各自 mAP |

### 5.7 符号说明表

| 符号 | 含义 | 典型值 |
|:---|:---|:---|
| $S \times S$ | YOLO 网格尺寸 | $7\times7$ (YOLOv1) |
| $B$ | 每网格预测框数 | 2 (YOLOv1), 3 (YOLOv3 per scale) |
| $C$ | 类别数 | VOC: 20, COCO: 80 |
| $k$ | RPN Anchor 数 per location | 9 (3 scales × 3 ratios) |
| $\lambda_{\text{coord}}$ | 定位损失权重 | 5 (YOLOv1) |
| $\lambda_{\text{noobj}}$ | 无目标置信度损失权重 | 0.5 (YOLOv1) |
| $t_x, t_y, t_w, t_h$ | Anchor 偏移编码 | 见 5.2 节公式 |
| $\tau_{\text{nms}}$ | NMS IoU 阈值 | 0.5（常用） |
| $\tau_{\text{iou}}$ | 正样本 IoU 阈值 | 0.5 (TP 判定) |

## 6. 推导思路和思想来源

### R-CNN 系列演进的思想链

- **最初困难（R-CNN 前）**：滑动窗口 + 图像金字塔暴力穷举 → 每张图上百万个窗口，每个都要过 CNN → 完全不现实。
- **R-CNN 的关键"转念"——Girshick et al. (2014)**：将检测解耦为"提议 + 验证"——先用廉价算法（Selective Search）生成 ~2000 个高召回候选区，再用 CNN 精细验证。将计算量从百万级压缩到千级。
- **Fast R-CNN 的飞跃——Girshick (2015)**：意识到 ~2000 个候选区共享同一张图的底层特征，不应重复卷积。提出全图单次 CNN + RoI Pooling 的特征共享策略，检测速度提升 ~100 倍。
- **Faster R-CNN 的终局——Ren et al. (2015)**：发现 Selective Search 成为新瓶颈（占时 > 90%），且不可学习。反问：能否用神经网络本身生成候选区？提出 RPN + Anchor 机制，使"提议"也成为可训练的网络模块，首次实现检测全流程端到端训练。

**推导主线**：分类器复用 → 特征图共享 → 提议网络化 → 全流程端到端。每一步消除一个瓶颈。

### YOLO 的思想来源

- **Faster R-CNN 的结构遗留问题**：尽管全流程可训练，Two-Stage 仍需先跑 RPN 再跑检测头——本质仍是"串行"推断。
- **Redmon et al. (2015) 的"转念"**：能否像人类一样"一眼看清"——不生成中间候选，直接从像素映射到框和类别？将检测重构为纯回归问题。
- **直觉来源**：OverFeat (2013) 证明全卷积网络可直接输出空间定位。YOLO 将这一思想推至最极端：全图 → 全输出，无任何显式提议步骤。
- **YOLOv2/v3 的补丁**：初始 YOLO 网格粗糙导致小目标漏检 → 引入 Anchor 和多尺度预测，但依然保持单阶段整体性。

**核心哲学分歧**：Two-Stage 认为检测必须"先粗筛再精判"（精度优先）；One-Stage 认为检测可以"一步到位"（速度优先）。后来 RetinaNet (2017) 证明 One-Stage 也能达到 Two-Stage 精度，分歧焦点转向类别不平衡（Focal Loss）。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础（手算 IoU）

**题目**：框 A = [0, 0, 10, 10]（左上角 (0,0)，右下角 (10,10)），框 B = [5, 0, 15, 10]。计算 IoU。

**手算过程**：
1. 交集：$x_1 = \max(0, 5) = 5$, $y_1 = \max(0, 0) = 0$, $x_2 = \min(10, 15) = 10$, $y_2 = \min(10, 10) = 10$。交集面积 $= (10-5) \times (10-0) = 5 \times 10 = 50$。
2. $A$ 面积 $= 10 \times 10 = 100$。
3. $B$ 面积 $= (15-5) \times (10-0) = 10 \times 10 = 100$。
4. 并集 $= 100 + 100 - 50 = 150$。
5. $\text{IoU} = \frac{50}{150} = \frac{1}{3} \approx 0.333$。

**验证**：两框右半重叠，左半 $A$ 独有。$A$ 的 50% 被 $B$ 覆盖，$B$ 的 50% 被 $A$ 覆盖 → 1/3 结果合理。

### 例子 2：中等（检测器选择决策树）

**场景**：你有 10000 张图片，需检测其中 3 类物体。要求：
- 场景 A：实时视频流，≥ 30 FPS，精度可适当让步。
- 场景 B：离线批量分析医学影像，精度最优，速度无所谓。
- 场景 C：嵌入式设备（树莓派），算力极度受限。

**解题**：
- **场景 A** → **YOLOv5s/v8n** 等 One-Stage 轻量模型。Faster R-CNN 在 GPU 上也只能 5-7 FPS，远不达标。
- **场景 B** → **Faster R-CNN + FPN**（Two-Stage）。小病灶需要高定位精度，Faster R-CNN 的 RoI 精修机制优于 YOLO 的粗粒度网格。
- **场景 C** → **YOLOv5n / NanoDet** 等超轻量 One-Stage 模型 + INT8 量化。Two-Stage 在树莓派上推理超 10s/图。

### 例子 3：实际应用（PyTorch 完整 IoU + NMS 实现）

```python
import numpy as np

# ---- 1. IoU 计算 ----
def compute_iou(box1: np.ndarray, box2: np.ndarray) -> float:
    """计算两个 [x1, y1, x2, y2] 框的 IoU"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = area1 + area2 - inter_area

    return float(inter_area / union_area) if union_area > 0 else 0.0

# ---- 2. NMS 实现 ----
def nms(boxes: np.ndarray, scores: np.ndarray,
        iou_threshold: float = 0.5) -> np.ndarray:
    """返回保留框的索引"""
    order = np.argsort(scores)[::-1]  # 降序排列
    keep = []

    while len(order) > 0:
        current = order[0]
        keep.append(current)
        if len(order) == 1:
            break
        # 计算 current 与剩余框的 IoU
        rest = order[1:]
        ious = np.array([compute_iou(boxes[current], boxes[i])
                         for i in rest])
        # 保留 IoU ≤ threshold 的框
        order = rest[ious <= iou_threshold]

    return np.array(keep, dtype=int)

# ---- 3. 自测断言 ----
if __name__ == "__main__":
    # 测试 IoU
    b1 = np.array([0, 0, 10, 10])
    b2 = np.array([5, 0, 15, 10])
    iou_val = compute_iou(b1, b2)
    assert abs(iou_val - 1/3) < 1e-4, f"IoU error: {iou_val}"
    print(f"✓ IoU 计算正确: {iou_val:.4f} (= 1/3)")

    # 完全重合 → IoU = 1
    assert compute_iou(b1, b1) == 1.0

    # 无交集 → IoU = 0
    b3 = np.array([20, 20, 30, 30])
    assert compute_iou(b1, b3) == 0.0

    # 测试 NMS
    boxes = np.array([[0, 0, 10, 10],   # 框 0
                      [1, 1, 10, 10],   # 框 1 (与框0高度重叠)
                      [100, 100, 110, 110]])  # 框 2 (独立)
    scores = np.array([0.9, 0.8, 0.95])
    keep = nms(boxes, scores, iou_threshold=0.5)
    # 期望: 保留框 2 (最高分 0.95) 和框 0 (框1被抑制)
    assert set(keep) == {0, 2}, f"NMS error: kept {keep}"
    print(f"✓ NMS 正确: 3个框 → 保留 {keep} (抑制了框1)")

    print("全部断言通过！")
```

- **实际价值**：此 IoU + NMS 实现是任何检测后处理的核心组件，预训练模型（如 torchvision 的 Faster R-CNN）输出的原始框必须经 NMS 去重才能使用。

## 8. 常见误区和易混概念

### 误区 1：YOLO 比 Faster R-CNN "先进"，因为它更新

- **错误直觉**："YOLOv8 比 Faster R-CNN 新，所以一定更好。"
- **为什么错**：这是**范式选择**问题而非年代问题——Faster R-CNN 代表的 Two-Stage 在精度要求极高的场景（医疗、遥感）仍是主流；YOLO 代表 One-Stage 在实时/嵌入场景占优。选型取决于任务约束，不是出版年份。
- **正确理解**：Two-Stage 适合"精度优先"，One-Stage 适合"速度优先"。

### 误区 2：IoU > 0.5 就算检测正确，所以 0.5 的阈值是"金标准"

- **错误直觉**：IoU = 0.5 是唯一正确的匹配阈值。
- **为什么错**：0.5 是 PASCAL VOC 的历史约定。COCO 挑战赛使用 $\text{mAP}^{@[.50:.95]}$ 多阈值平均，覆盖从粗到细的全部定位精度。任务不同阈值不同——自动驾驶要求 IoU ≥ 0.7（框不准后果严重），医学影像可能放宽至 0.3（病灶边缘模糊）。
- **正确理解**：IoU 阈值是任务定义的一部分，没有普适"正确值"。

### 误区 3：Anchor 越多检测效果越好

- **错误直觉**：RPN 中设 9 个 Anchor/位置，那 20 个不是更好？
- **为什么错**：Anchor 增加带来正负样本比恶化、计算量线性增长。Faster R-CNN 中 9 Anchor 已是经验最优——更多 Anchor 在 COCO 上几乎不涨点。
- **正确理解**：Anchor 本质是"先验形状猜想"——覆盖常见长宽比即可，过多造成冗余。Anchor-Free 方法（FCOS、CenterNet）甚至完全取消 Anchor。

### 概念对比表

| 维度 | R-CNN (2014) | Fast R-CNN (2015) | Faster R-CNN (2015) | YOLOv1 (2015) |
|:---|:---|:---|:---|:---|
| **提议生成** | Selective Search | Selective Search | **RPN**（可学习） | 无（网格隐式提议） |
| **CNN 前传次数** | ~2000 次/图 | 1 次/图 | 1 次/图 | 1 次/图 |
| **训练方式** | 多阶段分离 | 端到端（除 SS） | 端到端 | 端到端 |
| **推理速度** | ~13s/图 (GPU) | ~3s/图 | ~0.2s/图 (5 FPS) | ~0.02s/图 (45 FPS) |
| **VOC 2007 mAP** | 58.5% | 70.0% | 73.2% | 63.4% |
| **定位精度（小目标）** | 较高 | 高 | **最高** | 早期较差 |
| **核心瓶颈** | 重复 CNN 计算 | Selective Search | Two-Stage 串行 | 网格粗粒度 |

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[卷积神经网络CNN]]：所有检测器的 backbone 特征提取基底。
- [[Softmax分类器]]：检测分类子任务的标准输出层。
- [[ResNet残差网络]]：Faster R-CNN 和 YOLOv3+ 最常用 backbone。
- [[感受野]]：理解 Anchor 设计和大目标/小目标检测差异的理论基础。

### 下游延伸
- [[FasterRCNN]]：RPN 机制、Anchor 设计、RoI Align 的深度专题。
- [[YOLO目标检测]]：YOLOv1-v8 各版本演进、损失函数变体完整分析。
- [[FCOS]]：Anchor-Free 检测器——去除 Anchor 先验的最新范式。
- [[DETR]]：Transformer 检测器——用集合预测替代 NMS 的新思路。

### 横向关联
- [[SSD]]：另一经典 One-Stage 检测器，多尺度特征图上做密集 Anchor 预测。
- [[FPN]]（特征金字塔网络）：多尺度特征融合，Faster R-CNN 和 YOLOv3+ 共用基础设施。
- [[RetinaNet]]：用 Focal Loss 解决 One-Stage 正负样本极度不平衡，使 One-Stage 精度追平 Two-Stage。
- [[MaskRCNN]]：Faster R-CNN + 分割分支，检测向实例分割的直接延伸。

### 工具链
- [[IoU与NMS]]：交并比专题（GIoU、DIoU、CIoU 等改进变体）。
- [[IoU与NMS]]：非极大值抑制专题（Soft-NMS、Matrix NMS 等）。
- [[难例挖掘]]：在线难例挖掘 (OHEM) 与 Focal Loss 的联系。

### 应用场景
自动驾驶感知、安防监控、医学影像病灶检测、零售商品识别、遥感目标定位。

## 10. 闭卷复现任务

- [ ] 一句话区分图像分类和目标检测的核心差异。
- [ ] 画出 Two-Stage 检测器通用流程框图（提议 → 特征 → 分类+回归）。
- [ ] R-CNN → Fast R-CNN → Faster R-CNN 每步解决了什么瓶颈？
- [ ] 写出 RPN 的 Anchor 偏移编码公式：$t_x, t_y, t_w, t_h$。
- [ ] YOLO 网格预测：给定 $7\times7$ 网格、2 框/格、20 类，写出输出张量维度。
- [ ] 写出 IoU 公式，手算 $A=[0,0,10,10]$, $B=[5,0,15,10]$ 的 IoU。
- [ ] 写出 NMS 伪代码（5-8 行）。
- [ ] 解释 mAP 中 Precision-Recall 曲线构建方法及 11-point 插值。
- [ ] 对比 Faster R-CNN 和 YOLOv1 在 VOC 2007 上的精度（mAP）和速度（FPS）。
- [ ] 判断：自动驾驶场景（实时 + 高定位精度）→ 选 Two-Stage 还是 One-Stage？为什么？

## 11. 自测题：5 道

1. **基础**：R-CNN 为什么慢？Fast R-CNN 用一个什么关键操作解决了它？ #自测题/基础
   > [!question]- 答案解析
   > R-CNN 对每个候选区域独立跑 CNN（~2000 次/图），大量重复计算；Fast R-CNN 改为全图仅一次 CNN + RoI Pooling，候选区域在共享特征图上裁剪，速度提升 ~100 倍。

2. **基础**：Faster R-CNN 相对于 Fast R-CNN 的核心创新是什么？RPN 输出哪两项？ #自测题/基础
   > [!question]- 答案解析
   > 用可学习的 RPN（区域提议网络）取代固定的 Selective Search 算法。RPN 每个 Anchor 输出：(1) Objectness Score（前景/背景二分类）；(2) 边界框回归偏移 $(t_x, t_y, t_w, t_h)$。这一创新使检测全流程首次端到端可训练。

3. **中等**：给定 YOLOv1 损失函数中 $\lambda_{\text{coord}} = 5$, $\lambda_{\text{noobj}} = 0.5$，为什么定位损失权重要大于置信度损失？为什么对 $w, h$ 使用平方根？ #自测题/中等
   > [!question]- 答案解析
   > 定位权重放大：每张图大多数网格不含目标，若定位损失与置信度损失等权，模型会倾向把所有框置信度预测为 0 来迅速降低损失，忽略定位学习。平方根变换：大框的 $w, h$ 偏差容忍度应高于小框——同样偏移 5 像素，对大框（100px）几乎无影响，对小框（10px）影响剧烈。平方根压缩大框的偏差幅度。

4. **中等**：两张图的检测结果如下——图 1：TP=8, FP=2, FN=2；图 2：TP=15, FP=5, FN=5。在相同 Recall=0.8 处，两图 Precision 分别是多少？这个结果说明了 Precision-Recall trade-off 的什么特点？ #自测题/中等
   > [!question]- 答案解析
   > 图 1：$\text{Precision} = 8/(8+2) = 0.80$, $\text{Recall}=8/(8+2)=0.80$；图 2：$\text{Precision}=15/(15+5)=0.75$, $\text{Recall}=15/(15+5)=0.75$。在相同 Recall 下 Precision 可能不同——这是因为 FP 和 FN 分布不同。PR 曲线不是函数映射，而是由模型置信度阈值扫出的轨迹。

5. **较难**：Two-Stage 检测器（Faster R-CNN）天然比 One-Stage（YOLOv1）精度高——这是"结构决定论"对吗？用 Focal Loss / RetinaNet 的视角分析这个论述。 #自测题/较难
   > [!question]- 答案解析
   > 不完全对。Faster R-CNN 精度优势很大程度上来自 RPN 对正负 Anchor 的 1:1 采样——有效抑制了类别不平衡（一张图数十万 Anchor 中 >99% 是背景）。YOLOv1 的精度劣势部分源于正负样本极端不平衡（绝大多数网格不含目标却参与损失计算），而非 One-Stage 结构本身"注定低精度"。RetinaNet (2017) 引入 Focal Loss 自动降低"容易分类正确"的负样本 Loss 权重，使 One-Stage 在 COCO 上首次超越 Two-Stage——证明精度差距本质是**训练不平衡问题**而非结构限制。

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，写出 R-CNN → Fast → Faster 三步演进每步的核心瓶颈和解决方案。

### 我的推导复现
> 从 IoU 定义出发，手推 $A=[0,0,10,10]$, $B=[3,3,8,8]$ 的 IoU = ?

### 我的错误与卡点
- [ ] IoU 计算忘处理无交集（负面积） → 用 `max(0, x2-x1) * max(0, y2-y1)`。
- [ ] NMS 中未按分数排序 → 必须先降序排序，否则低分框可能保留。
- [ ] mAP 与 Accuracy 混淆 → mAP 综合定位精度和分类正确，Accuracy 只看分类。
- [ ] YOLO 输出维度算错 → 维度公式：$S \times S \times (B \cdot 5 + C)$，不是 $S \times S \times C$。
- [ ] Two-Stage 误以为 RPN 和检测头交替运行 → 实际上是共享特征图，RPN 先跑、Proposal 筛选后再过 RoI Pooling。

### 失败后的回流
- 演进脉络混淆 → 第 5.2 节对比表；IoU/NMS → 第 7 节代码；mAP → 第 5.6 节。
- 检测器选型迷茫 → 第 8 节概念对比表 + 第 7 节例子 2。

### 下次复习日期
- [ ] 明天  [ ] 3 天后  [ ] 7 天后  [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`05-计算机视觉/03-视觉核心任务/`
- **关联已有笔记**：[[RCNN]]、[[FastRCNN]]、[[FasterRCNN]]、[[YOLO目标检测]]、[[IoU与NMS]]、[[IoU与NMS]]
- **建议标签**：`#学习` `#计算机视觉` `#目标检测` `#RCNN` `#YOLO`
- **拆分建议**：此卡定位为"目标检测基础总览"，覆盖从问题定义到评估指标的完整入门链。已有独立深入卡（RCNN.md、FastRCNN.md、FasterRCNN.md、YOLO目标检测.md、IoU.md、NMS.md）可在本卡基础上做专题深挖。若需深入了解 Anchor-Free、DETR 等新范式，建新卡并设本卡为上游。
- **双链优先**：上游 → [[卷积神经网络CNN]]、[[Softmax分类器]]；下游 → [[FasterRCNN]]、[[YOLO目标检测]]、[[FCOS]]；横向 → [[FPN]]、[[SSD]]、[[RetinaNet]]、[[IoU与NMS]]、[[IoU与NMS]]。

## 🃏 Anki 卡片

- 目标检测与图像分类的核心区别？::分类输出单标签（图里有什么）；检测输出可变长集合（每个目标的类别 + 边界框坐标），需同时回答"哪里"和"是什么"。
- R-CNN 三个致命缺陷？::① ~2000 次独立 CNN 前传极慢；② 训练多阶段分离无法端到端；③ Selective Search 固定不可学习。
- Fast R-CNN 两个核心改进？::① 全图单次 CNN + RoI Pooling 特征共享；② 多任务联合损失实现端到端训练（除 Selective Search）。
- Faster R-CNN 核心创新？::用可学习的 RPN（区域提议网络）+ Anchor 机制取代 Selective Search，首次实现检测全流程端到端训练。
- RPN 每个 Anchor 输出哪两项？::① Objectness Score（前景/背景二分类）；② 边界框回归偏移量 $(t_x, t_y, t_w, t_h)$。
- YOLO 的核心思想？::将检测重构为全图单次回归问题——在 $S \times S$ 网格上直接预测每个网格的边界框、置信度和类别概率，无需显式提议步骤。
- IoU 的定义公式？::$\text{IoU}(A, B) = \frac{|A \cap B|}{|A \cup B|} = \frac{|A \cap B|}{|A| + |B| - |A \cap B|}$，值域 [0,1]。
- NMS 算法三个关键步骤？::① 按置信度降序排列所有框；② 取出最高分框加入保留集；③ 剔除与该框 IoU 超过阈值的所有框，重复 ②–③ 直至列表为空。
- mAP 中的 AP 如何计算（VOC 11-point）？::对 Recall 的 11 个等分点 [0, 0.1, ..., 1.0]，取每个点右侧最大 Precision 的值，求 11 个值的算术平均。
- COCO mAP@[.50:.95] 的含义？::在 IoU 阈值 0.50～0.95 范围内（步长 0.05，共 10 个阈值）分别计算 mAP，再取平均——覆盖从宽松到严格的全范围定位精度。
- Faster R-CNN vs YOLOv1 在 VOC 2007 上的精度/速度？::Faster R-CNN: mAP 73.2%, ~5 FPS; YOLOv1: mAP 63.4%, ~45 FPS。Two-Stage 精度高但慢，One-Stage 速度快但早期精度低。
- Two-Stage 和 One-Stage 的本质区别？::Two-Stage 先提议候选区再分类+回归（分步串行，精度优先）；One-Stage 直接在特征图上回归框和类别（一步到位，速度优先）。
- YOLOv1 输出张量维度（$S=7, B=2, C=20$）？::$7 \times 7 \times (2 \times 5 + 20) = 7 \times 7 \times 30$，其中每个网格预测 2 个框（每框 5 个值）和 20 类概率。
- Smooth L1 损失相比 L2 的优势？::对离群点梯度不爆炸——$|x|<1$ 时等价 L2（平滑），$|x|\ge 1$ 时梯度恒为 1（鲁棒），使训练更稳定。

---

## 🧪 学完本节后可完成的作业

- 可直接完成 [[03-Projects/课程作业/05-计算机视觉/课后作业/🎓 HW05 - Pascal VOC 最小目标检测工程包正式作业说明书|HW05]]
- 可直接完成 [[03-Projects/课程作业/05-计算机视觉/阶段作业/05-计算机视觉-阶段作业-ResNet与YOLO目标检测|阶段作业：ResNet与YOLO]] L4 YOLO 检测头
- 配合 [[03-Projects/课程作业/05-计算机视觉/课后习题/D2L-Ch14-目标检测习题册|D2L-Ch14 习题册]]

---
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
