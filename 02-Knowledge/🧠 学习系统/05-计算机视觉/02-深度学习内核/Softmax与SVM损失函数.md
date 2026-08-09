---
type: study
course: "05-计算机视觉"
topic: "Softmax与SVM损失函数"
created: 2026-08-05
status: ongoing
difficulty: intermediate
concept:
  - "损失函数"
  - "SVM损失函数"
  - "Softmax"
  - "交叉熵"
  - "梯度推导"
prerequisites:
  - "线性分类器"
  - "向量微分"
related:
  - "交叉熵损失"
  - "梯度下降优化"
flow: knowledge
upstream: ["[[kNN与线性分类器]]", "[[前向传播]]", "[[反向传播与计算图]]"]
stage_moc: "[[🧭 阶段2-深度学习内核]]"
kind: concept
source: "CS231n A1; D2L Ch.4"
anki_deck: "05-计算机视觉::02-深度学习内核"
anki_tags:
  - "Softmax"
  - "SVM"
  - "损失函数"
  - "交叉熵"
  - "梯度推导"
tags: [学习, 计算机视觉, Softmax, SVM, 交叉熵, 损失函数, 梯度推导]
---

# 🎯 Softmax 与 SVM 损失函数

---

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：损失函数（Loss Function）是监督学习的"指挥棒"——它用**一个标量值**告诉模型"你错得有多离谱"。Softmax + Cross-Entropy 和 Multiclass SVM Loss（Hinge Loss）是多类分类中**最根本的两种损失函数范式**，所有现代分类模型（ResNet、ViT、GPT 的下游分类头）都在这两类损失中二选一。两者的区别不仅是公式不同，更体现了对"正确"的根本哲学分歧：Softmax 要你**永远不满足**（概率永不完美），SVM 只要求你**过线即可**（只要正确类比其他类高出一个 margin）。不理解它们的梯度形式，就无法理解反向传播的起点——所有深度网络的参数更新，都是从损失函数的梯度**出发**的。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 在线性分类器中，对于一张猫的图片，我们得到了三个得分：`s = [3.2, 5.1, -1.7]`（分别对应猫、狗、船）。模型"说出"狗得分最高（5.1），但我们知道正确答案是猫。
>
> 现在的问题是：**怎么用数学语言量化"模型说错了"这件事？** 并且这个量化结果还必须是**可导的**（以便后面用梯度下降来修正参数）。
>
> 我们需要的损失函数必须满足三条硬性要求：
> 1. **当预测正确时，损失应该很小（或为零）**；
> 2. **当预测错误时，损失应该很大**；
> 3. **损失对模型参数必须处处可导**（或几乎处处，以便优化）。
>
> SVM Loss 和 Softmax/Cross-Entropy 正是解决这个问题的两大经典方案。它们都接受一个得分向量 $\mathbf{s} = f(\mathbf{x}; \mathbf{W})$，返回一个标量损失 $L$，且对 $\mathbf{s}$（进而对 $\mathbf{W}$）可导。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：损失函数是监督学习三要素（模型、损失、优化器）的核心枢纽。没有损失函数，就没有"好"与"坏"的客观标准，优化器（SGD/Adam）将无从下手。损失函数的选择直接决定了模型最终学到什么样的决策边界。
- **实际应用场景**：
  - **Softmax + Cross-Entropy**：ImageNet 分类、CIFAR-10/100、NLP 语言模型的下一个 token 预测、几乎所有现代多类分类任务。PyTorch 中 `nn.CrossEntropyLoss()` 是默认选项。
  - **Multiclass SVM Loss（Hinge Loss）**：CS231n 作业 A1 必手写实现、一些对"margin"有明确需求的场景（如某些度量学习任务）。
- **高频考点/任务**：手写 SVM Loss 和 Softmax Loss 的 Python 向量化实现（CS231n A1 核心作业）、推导 Softmax 对得分的梯度 $\frac{\partial L}{\partial s_j}$、对比两者的优化行为差异、解释"为什么 Softmax + Cross-Entropy 配合 Sigmoid 可以消除输出层梯度饱和"。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **线性分类器**：理解得分函数 $s_j = \mathbf{w}_j^T \mathbf{x} + b_j$，知道什么是得分向量 $\mathbf{s} \in \mathbb{R}^C$（$C$ 个类别的原始得分）。
2. **[[反向传播与计算图|梯度与偏导数基础]]**：知道 $\frac{\partial}{\partial x}\ln x = \frac{1}{x}$，链式法则的基本用法，以及梯度向量 $\nabla_{\mathbf{s}} L$ 的含义。
3. **[[反向传播与计算图|链式法则]]**（建议同步）：理解 $\frac{\partial L}{\partial \mathbf{W}} = \frac{\partial L}{\partial \mathbf{s}} \cdot \frac{\partial \mathbf{s}}{\partial \mathbf{W}}$ 的分层求导思路。

---

## 4. 用直觉语言解释它

> «"这东西其实就像……"»

### SVM Loss（Hinge Loss）的直觉
> 想象一场赛跑，有 $C$ 个选手（类别）。**正确答案（正确类）只要比第二名（最高错误类）领先一个安全距离 $\Delta$（margin）就够了**。一旦领先超过 $\Delta$，裁判就不再惩罚——"你已经赢了，不用再拉开更大差距"。只有那些没能甩开对手、甚至被对手反超的情况，才会产生损失。

- **为什么不追求更大领先？** 因为 Hinge Loss 的设计哲学是"够用就好"（once the margin is satisfied, the loss is zero）。这带来一个有趣的属性：模型不会花力气去"刷分"——只要正确类比所有错误类高出 $\Delta$，损失就为零，梯度也停止流动。

### Softmax / Cross-Entropy 的直觉
> 不再是赛跑，而是**概率分配游戏**。Softmax 把得分向量 $\mathbf{s}$ 转化为一个概率分布 $\mathbf{p}$（所有 $p_i \ge 0$ 且 $\sum p_i = 1$）。交叉熵损失衡量的是"真实分布 $\mathbf{y}$（one-hot）与预测分布 $\mathbf{p}$ 之间的差异"。
>
> 关键在于：**由于 Softmax 的指数归一化，正确类的概率永远不可能等于 1.0（除非正确类得分是 $+\infty$）**。这意味着模型永远有改进的动力——即使正确类得分已经远超其他类，Softmax 仍然会督促模型"再高一点、再高一点"，迫使正确类的概率趋近于 1。这就是 Softmax "永不满足"的特性。

### 两者哲学对比
| | SVM Loss (Hinge) | Softmax + Cross-Entropy |
|:---|:---|:---|
| **核心哲学** | "过线即止"——margin 满足就停 | "永不满足"——永远追求更纯的概率 |
| **对得分尺度敏感？** | 在 margin 区域内敏感；超出后不敏感 | **始终敏感**——得分整体放大/缩小会改变损失 |
| **零损失条件** | $s_{y_i} - s_j \ge \Delta$ 对所有 $j \ne y_i$ | 仅有 $p_{y_i}=1$（需要 $s_{y_i}=+\infty$，不可能） |
| **梯度消失条件** | margin 满足时梯度为零 | **永不为零**（除理论极限） |

---

## 5. 正式定义、核心公式、符号解释

### 5.1 通用设定

给定一个训练样本 $(\mathbf{x}_i, y_i)$：
- $\mathbf{x}_i$：输入图像（如一张 32×32×3 的猫图）
- $y_i$：正确类别标签（整数，$y_i \in \{1, 2, \dots, C\}$）
- $C$：类别总数
- $\mathbf{s} = f(\mathbf{x}_i; \mathbf{W}) \in \mathbb{R}^C$：模型输出的得分向量
- $s_j$：第 $j$ 类的得分

### 5.2 Multiclass SVM Loss（多类支持向量机损失 / Hinge Loss）

$$\boxed{L_i = \sum_{j \neq y_i} \max(0,\; s_j - s_{y_i} + \Delta)}$$

其中：
- $s_{y_i}$：正确类的得分
- $\Delta$：**安全边际（margin）**，是一个超参数，通常设为 $\Delta = 1$
- $\max(0, \cdot)$：Hinge 函数——只有当 $s_j - s_{y_i} + \Delta > 0$（即错误类比正确类+margin 还高）时才产生损失

**向量化形式**：
$$L_i = \sum_{j \neq y_i} \max(0,\; \mathbf{s} - s_{y_i} + \Delta)_{j}$$

整个训练集的损失是各样本损失的平均：$L = \frac{1}{N} \sum_{i=1}^{N} L_i$

> **关键理解**：阈值条件 $s_{y_i} \ge s_j + \Delta$，即正确类得分应比**每一个**错误类高出至少 $\Delta$。

### 5.3 Softmax 分类器与交叉熵损失（Cross-Entropy Loss）

Softmax 函数将得分向量 $\mathbf{s}$ 转化为概率分布：

$$\boxed{p_j = \frac{e^{s_j}}{\sum_{k=1}^{C} e^{s_k}}}$$

其中 $p_j$ 可解释为模型认为样本属于第 $j$ 类的**估计概率**。显然 $\sum_j p_j = 1$，$p_j \in (0, 1)$。

**交叉熵损失**衡量预测分布 $\mathbf{p}$ 与真实分布 $\mathbf{y}$（one-hot）的差异：

$$\boxed{L_i = -\ln p_{y_i} = -\ln\left(\frac{e^{s_{y_i}}}{\sum_{k=1}^{C} e^{s_k}}\right) = -s_{y_i} + \ln\sum_{k=1}^{C} e^{s_k}}$$

最后一个等式是对数性质推导得出，也是数值计算中最常用的形式（Log-Sum-Exp 技巧）：

$$L_i = \ln\sum_{k=1}^{C} e^{s_k} - s_{y_i}$$

**信息论视角**：交叉熵 $H(\mathbf{y}, \mathbf{p}) = -\sum_j y_j \ln p_j$。由于 $\mathbf{y}$ 是 one-hot，只有 $y_{y_i}=1$，其余为零，所以简化为 $-\ln p_{y_i}$。

### 5.4 符号说明表

| 符号 | 含义 | 维度 | 备注 |
|:---|:---|:---|:---|
| $\mathbf{s}$ | 一个样本的得分向量 | $\mathbb{R}^C$ | 线性分类器输出 |
| $s_j$ | 第 $j$ 类的得分 | 标量 | |
| $s_{y_i}$ | 正确类的得分 | 标量 | 下标 $y_i$ 是正确类别索引 |
| $\Delta$ | SVM 的安全边际 | 标量 | 默认 $\Delta = 1.0$ |
| $p_j$ | Softmax 预测概率 | 标量 | $p_j = e^{s_j}/\sum_k e^{s_k}$ |
| $p_{y_i}$ | 正确类的预测概率 | 标量 | 越接近 1 越理想 |
| $L_i$ | 单个样本的损失 | 标量 | 最终 Loss 是 $N$ 个 $L_i$ 的均值 |
| $N$ | 训练集样本数 | 标量 | |

### 5.5 正则化

以上公式只定义了 **data loss**。实践中，完整损失还需加上 **regularization loss**：

$$L = \underbrace{\frac{1}{N} \sum_{i=1}^{N} L_i}_{\text{data loss}} + \underbrace{\lambda R(\mathbf{W})}_{\text{regularization}}$$

最常见的 $R(\mathbf{W})$ 是 L2 正则化：$R(\mathbf{W}) = \sum_k \sum_l W_{k,l}^2$（所有权重的平方和）。正则化的作用是防止模型通过"放大所有权重"来 trivially 降低 Softmax 损失。

---

## 6. 推导思路和思想来源

### 6.1 SVM Loss 的设计思路

**最初困难**：如何鼓励正确类得分高于错误类，同时又不指定"高多少"的精确数值？

**关键转念**：借鉴二分类 SVM 的 **Hinge Loss** 思想——只惩罚那些"没超过 margin"的错误，对"已经超过 margin 很多"的正确不再奖励。这保持了稀疏性：不需要每个错误类都贡献梯度，只有"危险"的错误类才被更新。

**推导主线**：
1. 对每个错误类 $j \neq y_i$，定义其"违规程度"为 $s_j - s_{y_i} + \Delta$。
2. 若违规程度 $\le 0$（即 $s_{y_i} \ge s_j + \Delta$），则该错误类不贡献损失。
3. 若违规程度 $> 0$，则该错误类贡献 $s_j - s_{y_i} + \Delta$ 的损失。
4. 对所有错误类的违规程度求和，得到 $L_i$。

### 6.2 Softmax 的推导思路

**最初困难**：如何从无界的得分向量 $\mathbf{s}$ 得到一个合法的概率分布？

**关键转念**：使用 **指数函数** $e^{s_j}$ 将得分映射到 $(0, +\infty)$，再除以总和归一化。指数函数有三个关键优点：
- **单调性**：得分越高 → 概率越大。
- **非负性**：$e^x > 0$ 保证概率始终为正。
- **凸性**：使得 $-\ln(\text{softmax})$ 是凸函数，保证优化有唯一全局最优（在线性模型下）。

**交叉熵的信息论根源**：
- 熵 $H(p) = -\sum p \ln p$ 衡量分布的不确定性
- 交叉熵 $H(p, q) = -\sum p \ln q$ 衡量用分布 $q$ 近似分布 $p$ 的"代价"
- KL 散度 $D_{KL}(p \| q) = H(p, q) - H(p)$ 衡量两个分布的差异
- 最小化交叉熵等价于最小化 KL 散度（因为 $H(p)$ 对真实分布是常数）

### 6.3 Log-Sum-Exp 数值稳定技巧

直接计算 $e^{s_j}$ 容易溢出（如 $s_j = 1000$ 时）。数值稳定做法是减去最大值：

$$\ln\sum_{k} e^{s_k} = \ln\left(e^{s_{\max}} \sum_k e^{s_k - s_{\max}}\right) = s_{\max} + \ln\sum_k e^{s_k - s_{\max}}$$

其中 $s_{\max} = \max_k s_k$。这保证了指数参数最大为 0，不会溢出。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算 — 同一得分向量，两种损失

**题目**：设三分类问题（猫=0, 狗=1, 船=2），某样本真实类别是猫（$y_i = 0$），得分向量为：

$$\mathbf{s} = [3.2,\; 5.1,\; -1.7]$$

分别计算 SVM Loss（$\Delta = 1$）和 Softmax / Cross-Entropy Loss。

#### SVM Loss 手算

正确类得分 $s_{y_i} = s_0 = 3.2$。

- 对 $j=1$（狗）：$\max(0, 5.1 - 3.2 + 1) = \max(0, 2.9) = 2.9$
- 对 $j=2$（船）：$\max(0, -1.7 - 3.2 + 1) = \max(0, -3.9) = 0$

$$L_{\text{SVM}} = 2.9 + 0 = 2.9$$

> 🤔 注意：模型预测得分最高的是狗（5.1），正确答案是猫（3.2），模型判断错误，SVM 给出了 2.9 的惩罚。

#### Softmax / Cross-Entropy 手算

1. **指数化**：
   - $e^{3.2} \approx 24.53$
   - $e^{5.1} \approx 164.02$
   - $e^{-1.7} \approx 0.18$

2. **求和**：$\sum_k e^{s_k} \approx 24.53 + 164.02 + 0.18 = 188.73$

3. **概率**：
   - $p_0 = 24.53 / 188.73 \approx 0.130$（正确类概率仅 13%）
   - $p_1 = 164.02 / 188.73 \approx 0.869$
   - $p_2 = 0.18 / 188.73 \approx 0.001$

4. **交叉熵损失**：$L_{\text{CE}} = -\ln(0.130) \approx -\ln 0.130 \approx 2.04$

> 解读：模型把 87% 的概率错给了狗，正确类的概率只有 13%，交叉熵损失为 2.04。

---

### 例子 2：中等例子 — 得分轻微变化时两种损失的敏感度对比

**题目**：对同一个三分类问题，比较以下三组得分向量下的 SVM Loss 和 Softmax Loss（$\Delta=1$，真实类别 $y_i=0$）：

| 情况 | 得分 $\mathbf{s}$ | SVM Loss | Softmax Loss | 备注 |
|:---|:---|:---|:---|:---|
| A（全对且大幅领先） | `[10, 2, 2]` | 0 | 0.0003 | SVM 早停 |
| B（对但仅微弱领先）| `[10, 9, 9]` | 0 | 0.31 | SVM 仍为 0！ |
| C（错得极离谱） | `[10, 14, 15]` | 9 | 4.31 | 两者都很大 |

**关键洞察 — 对情况 B 的分析**：

- $s = [10, 9, 9]$，正确类 $s_0=10$。
- **SVM**：对所有 $j$，$\max(0, 9 - 10 + 1) = \max(0, 0) = 0$。**损失为 0，梯度也为 0**——SVM 认为"足够了，不训了"。
- **Softmax**：$p_0 = e^{10}/(e^{10}+e^{9}+e^{9}) = e^{10}/(e^{10}+2e^9) = e/(e+2) \approx 2.718/(4.718) \approx 0.576$。
  $L = -\ln(0.576) \approx 0.55$。**损失不为 0，仍会继续优化**——Softmax 说"虽然对了，但概率只有 58%，不够，继续学！"

这就是 Softmax 更常用的核心原因之一：**它始终提供非零梯度，推动模型学到更自信、更锐利的决策边界**。

---

### 例子 3：实际应用 — PyTorch 中的两种损失

```python
import torch
import torch.nn as nn

# --- 设定：批次大小 B=3，类别数 C=4 ---
# 得分矩阵 (3个样本, 4个类别的得分)
scores = torch.tensor([
    [3.2, 5.1, -1.7, 0.3],   # 样本1: 真实类=0(猫)
    [1.1, 2.2, 3.3, 0.5],    # 样本2: 真实类=2
    [-0.5, 0.8, 1.2, 2.0],   # 样本3: 真实类=3
])
labels = torch.tensor([0, 2, 3])  # 真实标签

# --- 方式一：CrossEntropyLoss（内置 Softmax + log + NLL）---
# 注意：nn.CrossEntropyLoss 的输入是原始得分(raw logits)，不是概率！
criterion_ce = nn.CrossEntropyLoss()
loss_ce = criterion_ce(scores, labels)
print(f"CrossEntropyLoss: {loss_ce.item():.4f}")

# --- 方式二：手动 Softmax + NLL ---
log_probs = torch.log_softmax(scores, dim=1)       # 等价于 log(softmax)
loss_nll = nn.NLLLoss()(log_probs, labels)          # 取正确类的负 log 概率
print(f"手动 NLL Loss:    {loss_nll.item():.4f}")   # 应与上面一致

# --- 方式三：手写 Multiclass SVM Loss（Hinge Loss）---
def svm_loss(scores, labels, delta=1.0):
    """
    scores: (N, C) 得分矩阵
    labels: (N,)   正确类别索引
    """
    N = scores.shape[0]
    correct_scores = scores[range(N), labels]  # (N,) 正确类的得分

    # 计算每个错误类的 margin: s_j - s_{y_i} + delta
    margins = scores - correct_scores.unsqueeze(1) + delta  # (N, C)

    # 把正确类位置的 margin 设为 0（不参与求和）
    margins[range(N), labels] = 0

    # Hinge: max(0, margin)
    loss_per_sample = torch.clamp(margins, min=0).sum(dim=1)  # (N,)
    return loss_per_sample.mean()

loss_svm = svm_loss(scores, labels, delta=1.0)
print(f"SVM Hinge Loss:   {loss_svm.item():.4f}")
```

> **关键工程注意**：`nn.CrossEntropyLoss()` 已经在内部做了 Softmax，**不要**在模型输出层再加 `nn.Softmax()` 后再传入，否则会 double-softmax 导致错误。

---

## 8. 常见误区和易混概念

### 误区 1：SVM Loss 里的 $\Delta$ 越大越好

- **错误直觉**："margin 越大，模型越安全，所以设大一点更好。"
- **为什么错**：$\Delta$ 只是缩放因子。在线性分类器中，如果把所有权重同时放大 $k$ 倍，得分也放大 $k$ 倍，margin 条件 $s_{y_i} \ge s_j + \Delta$ 变为 $k s_{y_i} \ge k s_j + \Delta$，这**不等价于** $s_{y_i} \ge s_j + \Delta/k$。但在有 L2 正则化的情况下，$\Delta$ 和正则化系数 $\lambda$ 之间存在**联动关系**：放大 $\Delta$ 和缩小 $\lambda$ 的效果类似。因此实践中通常固定 $\Delta = 1$，通过调 $\lambda$ 来控制 margin 的效果。
- **正确做法**：$\Delta = 1$ 是安全的默认值，无需调整。真正需要调的是学习率和正则化强度。

### 误区 2：Softmax 输出的就是真正的"概率"

- **错误直觉**："$p_j = 0.87$ 说明模型 87% 确信这是狗。"
- **为什么有偏差**：Softmax 输出的是**模型在参数分布下的估计置信度**，而非校准良好的真实概率。现代深度网络（尤其是大模型）往往**过度自信**（overconfident）——Softmax 输出 0.999，但实际准确率远低于此。需要用**温度缩放（Temperature Scaling）**或**标签平滑（Label Smoothing）**来校准。
- **正确理解**：Softmax 输出叫"预测置信度"可以，但不要与"真实后验概率 $P(y|\mathbf{x})$"等同。

### 误区 3：CrossEntropyLoss 接受概率输入

- **错误直觉**：`nn.CrossEntropyLoss()` 名字里有 Cross Entropy，应该接受概率吧？
- **为什么错**：PyTorch 的 `nn.CrossEntropyLoss` 设计为接受**原始 logits（未归一化得分）**，内部自动完成 `log_softmax` + `NLLLoss` 的组合。如果传来已经 softmax 过的值，会导致 softmax-of-softmax 和 log-of-softmax，完全错误。
- **正确做法**：模型最后一层不要加 Sigmoid 或 Softmax（除非使用 `nn.BCEWithLogitsLoss`），让损失函数内部处理。

### 概念对比表

| 概念 | 损失公式（单样本） | 梯度 $\partial L / \partial s_j$ | 零损失条件 | 典型场景 |
|:---|:---|:---|:---|:---|
| **SVM Hinge Loss** | $\sum_{j \neq y_i} \max(0, s_j - s_{y_i} + \Delta)$ | 见 §6 推导 | $s_{y_i} \ge s_j + \Delta,\forall j \neq y_i$ | CS231n 教学、某些度量学习 |
| **Cross-Entropy Loss** | $-\ln\left(\frac{e^{s_{y_i}}}{\sum_k e^{s_k}}\right)$ | $p_j - 𝟙[j=y_i]$ | 不可达（理论极限 $p_{y_i}=1$） | 几乎所有现代分类任务 |
| **Binary Cross-Entropy** | $-y\ln\hat{y} - (1-y)\ln(1-\hat{y})$ | — | $\hat{y}=y$ | 二分类 / 多标签分类 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- 线性分类器：理解得分函数 $\mathbf{s} = \mathbf{W}\mathbf{x} + \mathbf{b}$ 的来龙去脉。
- [[反向传播与计算图|梯度与偏导数基础]]：掌握 $\frac{\partial}{\partial s_j}$ 的基本运算法则。
- [[反向传播与计算图|链式法则]]：$\frac{\partial L}{\partial \mathbf{W}} = \frac{\partial L}{\partial \mathbf{s}} \cdot \frac{\partial \mathbf{s}}{\partial \mathbf{W}}$ 的分层求导。

### 下游延伸
- [[反向传播与计算图|反向传播算法]]：损失函数 $\to$ 输出层误差信号 $\delta^{(L)}$ 是整个反向传播的起点。
- PyTorch 优化器：loss 计算完成后，`loss.backward()` 触发梯度计算，optimizer 执行参数更新。
- 交叉熵损失（工程视角）：深入 `nn.CrossEntropyLoss` 的源码实现与数值稳定技巧。
- [[目标检测RCNN与YOLO|Focal Loss]]：对 Cross-Entropy 的改进——通过 $(1-p_t)^\gamma$ 因子降低易分类样本的权重，解决类别极度不平衡问题。
- [[数据增强与正则化|标签平滑]]：将 one-hot 目标 $\mathbf{y}$ 软化为 $\mathbf{y}' = (1-\epsilon)\mathbf{y} + \epsilon/C$，缓解 Softmax 过度自信。

### 横向关联
- MSE 损失 ↔ Softmax/CE：为什么分类不用 MSE？（因为 MSE + Softmax 在输出层会产生梯度饱和，收敛极慢）
- [[数据增强与正则化|权重正则化]] ↔ 损失函数：L2 正则化在 SVM 和 Softmax 中的数学形式与调参策略。

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清楚 SVM Loss 和 Softmax Loss 分别解决什么问题。
- [ ] 2. 用直觉语言解释两者的核心哲学差异（"过线即止" vs "永不满足"）。
- [ ] 3. 写出 Multiclass SVM Loss 的完整公式，解释每个符号。
- [ ] 4. 写出 Softmax 函数和 Cross-Entropy Loss 的完整公式。
- [ ] 5. 给定得分向量 `[3.2, 5.1, -1.7]`，手算两种损失值。
- [ ] 6. 推导 Softmax/CE 对得分 $s_j$ 的梯度：$\frac{\partial L}{\partial s_j} = p_j - 𝟙[j=y_i]$。
- [ ] 7. 推导 SVM Loss 对得分 $s_j$ 的梯度形式。
- [ ] 8. 解释为什么 Softmax 比 SVM 更常用（至少三条原因）。
- [ ] 9. 写出 Log-Sum-Exp 数值稳定技巧的公式并解释原理。
- [ ] 10. 说出 `nn.CrossEntropyLoss()` 的输入应该是 logits 还是概率。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
|:---|:---|:---|:---|
| 1 | 概念辨析 | 基础 | SVM vs Softmax 的哲学差异 |
| 2 | 手算 | 基础 | 给定得分向量计算两种损失 |
| 3 | 公式推导 | 中等 | Softmax/CE 梯度的推导过程 |
| 4 | 条件判断 | 中等 | 为什么分类不用 MSE 损失 |
| 5 | 综合分析 | 较难 | 温度参数对 Softmax 分布的影响 |

### 题目与解析

#### 1. 关于 Multiclass SVM Loss（Hinge Loss）的说法，**错误**的是？
- A. 当正确类的得分比所有错误类高出至少 $\Delta$ 时，损失为 0
- B. 增大 $\Delta$ 的值等价于缩小正则化系数 $\lambda$
- C. Hinge Loss 的梯度在某些区间为零，具有稀疏性
- D. 当模型完全错误时（$s_j \gg s_{y_i}$），SVM Loss 会趋于无穷大

> [!question]- 答案解析
> - **答案**：D
> - **解析**：即使模型完全错误，SVM Loss 也是**线性增长**（$s_j - s_{y_i} + \Delta$），不会趋于无穷大。正是因为"错的再离谱也只线性惩罚"的特性，SVM Loss 对极端异常值比 Softmax/CE 更不敏感（Softmax 的指数函数会指数级放大极端错误）。A、B、C 均为正确表述。
> - **易错原因**：直觉上觉得"错了就该狠狠惩罚"，忘了 Hinge 是线性函数。
> - **Obsidian 标签建议**：`#自测题/概念`

#### 2. 给定得分 $\mathbf{s} = [2.0, 4.0, 1.0]$（$y_i=0$，$\Delta=1$），SVM Loss = ？

> [!question]- 答案解析
> - **答案**：$L_{\text{SVM}} = \max(0, 4.0 - 2.0 + 1) + \max(0, 1.0 - 2.0 + 1) = 3.0 + 0 = 3.0$
> - **解析**：逐一检查每个错误类。$j=1$ 时 $4.0-2.0+1=3>0$，贡献 3.0；$j=2$ 时 $1.0-2.0+1=0$，贡献 0。合计 3.0。

#### 3. 【推导】请证明 Softmax + Cross-Entropy 对得分 $s_j$ 的梯度为 $\frac{\partial L}{\partial s_j} = p_j - 𝟙[j=y_i]$。

> [!question]- 答案解析
> - **答案**：设 $L = -\ln p_{y_i}$，其中 $p_k = e^{s_k} / \sum_t e^{s_t} = e^{s_k} / Z$。
>
>   **情况 1**：$j = y_i$（对正确类得分求导）
>   $$\frac{\partial L}{\partial s_{y_i}} = -\frac{\partial}{\partial s_{y_i}}\left(s_{y_i} - \ln Z\right) = -\left(1 - \frac{1}{Z} \cdot \frac{\partial Z}{\partial s_{y_i}}\right)$$
>   因为 $\frac{\partial Z}{\partial s_{y_i}} = e^{s_{y_i}}$，所以 $\frac{\partial L}{\partial s_{y_i}} = -1 + \frac{e^{s_{y_i}}}{Z} = p_{y_i} - 1$。
>
>   **情况 2**：$j \neq y_i$（对错误类得分求导）
>   $$\frac{\partial L}{\partial s_j} = -\frac{\partial}{\partial s_j}\left(s_{y_i} - \ln Z\right) = \frac{1}{Z} \cdot e^{s_j} = p_j$$
>
>   **统一形式**：$\frac{\partial L}{\partial s_j} = p_j - 𝟙[j = y_i]$
>
>   **直觉解读**：对于正确类，梯度为 $p_{y_i} - 1$（负值，增加正确类得分）；对于错误类，梯度为 $p_j$（正值，降低错误类得分）。且 $\sum_j \frac{\partial L}{\partial s_j} = (\sum_j p_j) - 1 = 0$，梯度之和为零。
> - **对应误区**：这个优雅的梯度形式也是 Softmax/CE 流行的关键原因——计算极其简单！

#### 4. 为什么分类问题用 MSE（均方误差）损失效果很差？（结合梯度分析）

> [!question]- 答案解析
> - **答案**：MSE 损失为 $L = \frac{1}{2}\sum_j (p_j - y_j)^2$。
>   - **梯度饱和问题**：$\frac{\partial L}{\partial s_j} = (p_j - y_j) \cdot p_j(1-p_j)$（或类似的 sigmoid 导数项）。当 $p_j$ 接近 0 或 1 时，导数 $p_j(1-p_j) \approx 0$，梯度几乎消失，训练极其缓慢。
>   - **对比 CE**：CE 的梯度是 $p_j - y_j$，**干净地消去了 Softmax 导数的饱和因子**（见上题的推导中，$\frac{\partial \ln p}{\partial s}$ 恰好约掉了 $\frac{\partial p}{\partial s}$ 中的饱和项）。这使得即使 $p_{y_i}$ 已经接近 1，梯度仍线性地传递误差信号，训练持续高效。
>   - **凸性差异**：MSE + Softmax 的组合在参数空间中是非凸的（有多个局部极小值），而 CE + Softmax（在线性模型上）保持凸性。

#### 5. 【综合分析】在 Softmax 中引入温度参数 $T$：$p_j = \frac{e^{s_j/T}}{\sum_k e^{s_k/T}}$。当 $T \to 0^+$ 和 $T \to +\infty$ 时，概率分布分别趋于什么？这对知识蒸馏有什么启示？

> [!question]- 答案解析
> - **答案**：
>   - **$T \to 0^+$**：Softmax 趋于 **argmax**——最大得分对应的类概率趋近于 1，其他类趋近于 0。分布变得极其尖锐（hard target）。
>   - **$T \to +\infty$**：$e^{s_j/T} \approx e^0 = 1$，所有类概率趋近于 $1/C$。分布退化为均匀分布（最大熵）。
>   - **知识蒸馏启示**：Hinton 在 Distilling the Knowledge in a Neural Network (2015) 中提出，用高温度 $T > 1$ 软化教师网络的输出分布，使**错误类的相对概率差异被放大**（"暗知识"被显露出来），学生网络可以从这些软标签中学到比 one-hot 硬标签更丰富的类间相似性结构。蒸馏时教师和学生使用相同的高温度 $T$，推理时学生恢复 $T=1$。
> - **Obsidian 标签建议**：`#自测题/知识蒸馏` `#自测题/综合分析`

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释 SVM Loss 和 Softmax/CE 的核心差异：

### 我的推导复现
> 不看上文，尝试：
> 1. 写出两种损失的完整公式
> 2. 推导 Softmax/CE 对 $s_j$ 的梯度 $\frac{\partial L}{\partial s_j} = p_j - 𝟙[j=y_i]$
> 3. 推导 SVM Loss 对 $s_j$ 的梯度

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/`
- **建议双链**：
  - 线性分类器
  - [[反向传播与计算图|梯度计算基础]]
  - [[反向传播与计算图|反向传播算法]]
  - 交叉熵损失（工程视角）
  - [[目标检测RCNN与YOLO|Focal Loss]]
  - [[数据增强与正则化|标签平滑]]
  - MSE 损失
  - [[数据增强与正则化|权重正则化]]
- **建议标签**：`#学习` `#深度学习` `#计算机视觉` `#Softmax` `#SVM` `#交叉熵` `#损失函数` `#梯度推导` `#CS231n`
- **拆分建议**：属于 A 类核心概念主体卡。如后续补充 SVM Loss 梯度推导或 Log-Sum-Exp 的数值分析，可独立为子卡（难度 advanced），用双链从本卡 §6 链接出去。SVM Loss 的 vectorized 实现（Python 手写 + 梯度检查）作为实战作业 HW01 的一部分，在作业说明书 [[05-计算机视觉-课后作业-01-kNN与Softmax线性分类|HW01]] 中完成。

---

*创建于：2026-07-27*
*来源：CS231n Assignment 1; 《动手学深度学习》D2L Ch.4*

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

