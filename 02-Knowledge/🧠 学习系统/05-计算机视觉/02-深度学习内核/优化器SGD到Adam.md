---
type: study
course: "05-计算机视觉"
topic: "优化器：从SGD到AdamW"
created: 2026-08-06
status: ongoing
difficulty: intermediate
concept: ["优化器", "SGD", "Momentum", "Adam", "AdamW"]
prerequisites:
  - "梯度下降CV"
  - "反向传播与计算图"
related:
  - "学习率调度"
  - "批归一化BatchNorm"
  - "权重正则化"
flow: knowledge
upstream: ["[[梯度下降CV]]", "[[反向传播与计算图]]"]
stage_moc: "[[🧠 第二阶段：深度学习内核]]"
kind: concept
source: "D2L Ch.12; CS231n L3"
anki_deck: "05-计算机视觉::02-深度学习内核"
anki_tags:
  - "计算机视觉"
  - "优化器"
  - "Adam"
  - "SGD"
tags: [学习, 计算机视觉, 优化器, SGD, Adam, Momentum]
---

# 🎯 优化器：从SGD到AdamW

> 所属路径：[[🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 所属阶段：[[🧠 第二阶段：深度学习内核|🧠 第二阶段：深度学习内核（模型本质）]]
> 教材入口：[[02-Knowledge/🧠 学习系统/05-计算机视觉/📚 教材挂载索引|教材挂载索引]]
> 核心源：D2L Ch.12; CS231n L3

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：优化器的选择直接决定模型能否收敛、收敛速度、以及最终泛化性能。从 2012 年的朴素 SGD 到 2024 年 CV 领域的标配 AdamW，优化器的发展史就是深度学习从"手工血汗调参"走向"自动稳定训练"的缩影。理解 SGD → Momentum → NAG → AdaGrad → RMSprop → Adam → AdamW 的演进逻辑，你就能看懂每一代优化器"修了前一代的什么 bug"，从而在实际工作中做出正确的选择——而不是跟风用 Adam 或盲目坚守 SGD。CS231n 在 L3 专门用一整节讲优化器，D2L 以 Ch.12 完整展开。**不理解优化器家族的设计哲学，调参永远靠运气。**

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem（我们遇到了什么麻烦）**：

朴素 SGD（Stochastic Gradient Descent）虽然简单，但在实际训练深层网络时暴露出三大致命缺陷：

**① 峡谷震荡（Ravine Oscillation）**：
损失函数的地形往往不是各向同性的碗状，而是狭长的"峡谷"——在某些方向上曲率很大（陡壁），另一些方向上曲率很小（平坦谷底）。SGD 沿梯度方向更新时，在陡壁方向上反复震荡、大幅跨越，在谷底方向上却挪动得极其缓慢，就像醉汉在峡谷中 Z 字形摇摆却始终走不到谷底。

**② 鞍点停滞（Saddle-Point Stagnation）**：
高维空间中鞍点远比局部极小值常见得多。在鞍点处，梯度接近零（但不为零），SGD 的更新步长变得极小，训练几乎"卡住"。Hessian 矩阵中有正有负的特征值让梯度方向犹豫不决——往某些方向走损失下降，另一些方向走损失上升，SGD 缺乏"冲出鞍点"的惯性机制。

**③ 统一学习率的僵化**：
SGD 对所有参数使用同一个全局学习率。但不同层的参数对损失的敏感度可能差数个数量级——Embedding 层可能只需微小调整，全连接层的某些权重可能需要大步更新。当参数空间的曲率在不同维度上差异悬殊（病态 Hessian），统一学习率要么在敏感方向上发散，要么在平坦方向上爬行。

**优化器家族**通过三种思路逐一击破：**动量**（惯性冲出峡谷和鞍点）、**自适应学习率**（每个参数有自己的步长）、**解耦权重衰减**（正则化不受自适应机制污染）。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：优化器是梯度下降的"驾驶系统"。如果说反向传播是地图（告诉你往哪走），优化器就是方向盘和油门（决定每一步的步长和方向修正）。优化器 + 学习率调度 + 权重初始化，三者构成训练工程的"铁三角"。
- **实际应用场景**：
  - **图像分类/检测/分割**：CV 任务首选 AdamW（ResNet、ViT、SwinT 的 PyTorch 官方实现几乎全用 AdamW）
  - **NLP 大模型训练**：Transformer 家族（BERT、GPT、LLaMA）标配 Adam/AdamW
  - **GAN 训练**：生成器/判别器常用 Adam（β₁=0.5 的变体以稳定对抗训练）
  - **追求极致精度**：ImageNet 刷榜场景常用 SGD + Momentum + 精心调度的学习率（cosine annealing）+ 长时间训练
  - **强化学习**：PPO、SAC 等算法内部用 Adam 更新策略/价值网络
- **高频考点/任务**：
  - SGD + Momentum 的指数移动平均公式与衰减因子 β 的作用
  - Nesterov 与经典 Momentum 的"前瞻"差异
  - AdaGrad 的累积梯度平方为什么导致学习率单调递减至零
  - RMSprop 如何通过 EMA 修正 AdaGrad 的致命缺陷
  - Adam 的偏差校正公式 $\hat{m}_t = m_t / (1 - \beta_1^t)$ 及其必要性
  - AdamW 为什么将权重衰减从 Adam 的自适应矩阵中解耦出来
  - 优化器选择决策表（什么场景用什么优化器）

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[梯度下降CV|梯度下降与优化基础]]**：理解批量梯度下降（GD）→ 随机梯度下降（SGD）→ 小批量 SGD 的演进，掌握 $\theta_{t+1} = \theta_t - \eta \nabla J(\theta_t)$ 的更新公式及学习率 η 的含义。
2. **[[反向传播与计算图]]**：理解梯度 $\nabla J(\theta_t)$ 如何通过链式法则逐层回传——优化器"消费"的梯度由反向传播"生产"。
3. **指数移动平均（EMA）的直觉**：$v_t = \beta v_{t-1} + (1 - \beta) g_t$ 的含义——近期的值权重更大、远期的值权重指数衰减。这是 Momentum、RMSprop、Adam 的共同数学基础。
4. **基本微积分**：偏导数、链式法则、Hessian 矩阵的概念（至少听说过曲率）。

---

## 4. 用直觉语言解释它

> «"这东西其实就像……"»

- **直觉类比 1 — Momentum = 滚下山的铁球**：
  朴素 SGD 像一个没有重量的乒乓球：每一步只看当前位置的坡度，风吹一下就飘了，在峡谷壁上疯狂弹跳。Momentum 给球加上了质量——它记住之前的运动方向，保持"惯性"。在峡谷的两壁之间，惯性抵消了震荡（左右摇摆被平均掉），在谷底方向惯性叠加让下降越来越快。在鞍点处，即使当前梯度为零，惯性也能推着球冲过去。

- **直觉类比 2 — Nesterov = "先看一步再迈腿"**：
  普通 Momentum 先按惯性往前走，到了新位置再看梯度修正。Nesterov 更聪明：先按惯性往前滑半步，在那个"前瞻位置"计算梯度，再综合修正。就像你下楼梯时不会闭着眼迈步——你会先看下一级台阶在哪，然后调整落脚点。

- **直觉类比 3 — AdaGrad/RMSprop = 为每个参数定制"学习率鞋"**：
  SGD 给所有人穿同一尺码的鞋，在陡坡上脚疼（震荡）、在平地上走不动（步长太小）。AdaGrad 观察每个参数的历史梯度：历史梯度大的参数（陡坡）自动减小步长、历史梯度小的参数（平地）自动增大步长。但它有个致命 bug——"历史"是累加的，鞋子越来越紧，最后走不动了。RMSprop 修复了这一点：用指数移动平均只记住"近期"的梯度大小，让鞋子有弹性。

- **直觉类比 4 — Adam = Momentum + RMSprop 的婚姻**：
  Adam 同时拥有"惯性"（一阶动量 $m_t$，决定方向）和"自适应步长"（二阶动量 $v_t$，调整每参数步长），就像一辆既有巡航控制（惯性）又有自适应悬挂（每轮独立调阻尼）的越野车。

- **直觉类比 5 — AdamW = 把"减重"从"调悬挂"里拆出来**：
  Adam 的权重衰减（正则化）被卷入了自适应学习率的计算中，导致衰减效果被污染——在梯度大的参数上衰减反而变小。AdamW 的做法简单而深刻：**分开两个控制回路**——自适应学习率只管梯度方向/步长，权重衰减直接减在参数上（$w \leftarrow w - \eta \lambda w$）。就像减肥（权重衰减）和调整步伐（自适应学习率）应该是两件独立的事。

---

## 5. 正式定义、核心公式、符号解释

### 5.1 通用框架：随机梯度下降（SGD）

设损失函数为 $\mathcal{L}(\theta)$，参数为 $\theta \in \mathbb{R}^d$，在 mini-batch $\mathcal{B}_t$ 上计算梯度 $g_t = \frac{1}{|\mathcal{B}_t|} \sum_{x \in \mathcal{B}_t} \nabla_\theta \mathcal{L}(x, \theta_t)$。SGD 更新公式：

$$\theta_{t+1} = \theta_t - \eta \cdot g_t$$

### 5.2 SGD + Momentum

引入速度（velocity）$v_t$ 作为梯度的一阶指数移动平均：

$$v_t = \beta \cdot v_{t-1} + (1 - \beta) \cdot g_t$$
$$\theta_{t+1} = \theta_t - \eta \cdot v_t$$

- $\beta \in [0, 1)$：动量衰减因子，常用 $\beta = 0.9$。$\beta = 0$ 退化为朴素 SGD。
- $v_t$ 的等效展开：$v_t = (1-\beta) \sum_{i=0}^{t} \beta^{t-i} g_i$，近期梯度权重更大。

> **为什么能抑制峡谷震荡？** 震荡方向的梯度正负交替，在 EMA 中被相互抵消（$v \approx 0$）；下降方向的梯度始终同号，在 EMA 中被持续放大。动量"平均掉了噪声，累积了信号"。

### 5.3 Nesterov Accelerated Gradient (NAG)

NAG 不是在当前位置 $\theta_t$ 计算梯度，而是先沿惯性方向走半步，在"前瞻位置" $\theta_t - \eta \beta v_{t-1}$ 处计算梯度：

$$g_t^{\text{NAG}} = \nabla_\theta \mathcal{L}\big(\theta_t - \eta \beta v_{t-1}\big)$$
$$v_t = \beta \cdot v_{t-1} + (1 - \beta) \cdot g_t^{\text{NAG}}$$
$$\theta_{t+1} = \theta_t - \eta \cdot v_t$$

> **直觉**：相当于"先看看你即将到达的地方有多陡，再决定这一步迈多大"。在凸优化中，NAG 的理论收敛速度比标准 Momentum 更快（$O(1/t^2)$ vs $O(1/t)$）。

### 5.4 AdaGrad

为每个参数维度 $i$ 独立维护历史梯度平方的累加和 $G_{t, i}$：

$$G_{t, i} = G_{t-1, i} + g_{t, i}^2$$
$$\theta_{t+1, i} = \theta_{t, i} - \frac{\eta}{\sqrt{G_{t, i} + \epsilon}} \cdot g_{t, i}$$

- $\epsilon$：数值稳定常数（通常 $10^{-8}$），防止除零。
- **致命缺陷**：$G_{t, i}$ 单调递增，分母 $\sqrt{G_{t, i} + \epsilon}$ 无限增大，学习率最终趋于零——训练还没结束，参数已经不更新了。因此在深度学习中极少直接使用 AdaGrad。

### 5.5 RMSprop

将 AdaGrad 的历史累加改为梯度平方的**指数移动平均**，用 $\beta_2$ 控制"记忆长度"：

$$v_t = \beta_2 \cdot v_{t-1} + (1 - \beta_2) \cdot g_t^2$$
$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{v_t} + \epsilon} \cdot g_t$$

- $\beta_2$：二阶动量衰减因子，Hinton 建议 $\beta_2 = 0.9$（在 Coursera 课程中提出）。
- 与 AdaGrad 的关键区别：$v_t$ 不再单调递增，"历史"会指数遗忘——近期的梯度大小影响更大，远期的梯度逐渐淡出。

### 5.6 Adam（Kingma & Ba, 2015）

Adam 同时维护一阶动量 $m_t$（方向）和二阶动量 $v_t$（自适应步长）：

$$m_t = \beta_1 \cdot m_{t-1} + (1 - \beta_1) \cdot g_t$$
$$v_t = \beta_2 \cdot v_{t-1} + (1 - \beta_2) \cdot g_t^2$$

**偏差校正**：在 $t$ 较小时，$m_t$ 和 $v_t$ 初始化于零导致估计严重偏低。校正因子 $(1 - \beta^t)$ 将估计拉升到无偏水平：

$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}$$

最终更新：

$$\theta_{t+1} = \theta_t - \eta \cdot \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}$$

默认超参数：$\beta_1 = 0.9$，$\beta_2 = 0.999$，$\epsilon = 10^{-8}$，$\eta = 0.001$。

> **偏差校正为什么必要？** 在 $t=1$ 时，$m_1 = (1-\beta_1)g_1 = 0.1 g_1$，而非我们期望的 $g_1$。未经校正的更新步长仅是应有的 $10\%$，训练初期几乎停滞。$\hat{m}_1 = m_1/(1-0.9) = g_1$，校正完美还原。

### 5.7 AdamW（Loshchilov & Hutter, 2019）

核心洞见：**权重衰减（L2 正则化）不应与自适应学习率耦合**。

在 Adam 的标准实现中，L2 正则化通过修改梯度实现：

$$g_t^{\text{Adam+L2}} = g_t + \lambda \theta_t$$

但这导致 $\lambda \theta_t$ 被传入 $m_t$ 和 $v_t$，最终更新变为：
$$\theta_{t+1} = \theta_t - \eta \cdot \frac{\hat{m}_t + \lambda \hat{\theta}_t / \sqrt{\hat{v}_t}}{\sqrt{\hat{v}_t} + \epsilon}$$

——权重衰减的强度被 $\sqrt{\hat{v}_t}$ "扭曲"了：梯度大的参数（$\sqrt{\hat{v}_t}$ 大）受到的衰减反而更少，这与正则化的初衷相悖。

**AdamW 的解耦方案**：将权重衰减独立应用于参数本身，不经过 $m_t$/$v_t$ 的自适应机制：

$$m_t = \beta_1 \cdot m_{t-1} + (1 - \beta_1) \cdot g_t$$
$$v_t = \beta_2 \cdot v_{t-1} + (1 - \beta_2) \cdot g_t^2$$
$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}$$
$$\theta_{t+1} = \theta_t - \eta \cdot \left( \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} + \lambda \theta_t \right)$$

最后一个括号中的 $\lambda \theta_t$ 是关键——它是"脱钩"的权重衰减项，不经过自适应矩阵缩放。$\lambda$ 通常设为 $0.01 \sim 0.1$。

> **为什么解耦很重要？** 实验表明 AdamW 在 CV（尤其 ViT/ConvNeXt）上比 Adam+L2 显著提升泛化性，并且 $\eta$ 和 $\lambda$ 可以独立调参——不再相互纠缠。AdamW 是现代 CV 训练的默认选择。

### 5.8 符号说明总表

| 符号 | 含义 | 典型值 | 解释 |
| :--- | :--- | :--- | :--- |
| $\theta_t$ | 第 $t$ 步的参数向量 | — | 所有权重和偏置展平 |
| $g_t$ | 第 $t$ 步的随机梯度 | — | 在 mini-batch 上计算 |
| $\eta$ | 学习率 | 0.001 | SGD 常用 0.01，Adam 常用 0.001 |
| $\beta$ / $\beta_1$ | 一阶动量衰减因子 | 0.9 | "惯性"的记忆长度 |
| $\beta_2$ | 二阶动量衰减因子 | 0.999 | 梯度平方的 EMA 系数 |
| $m_t$ | 一阶动量（梯度 EMA） | — | 决定方向 |
| $v_t$ | 二阶动量（梯度平方 EMA） | — | 决定自适应步长 |
| $\hat{m}_t, \hat{v}_t$ | 偏差校正后的动量 | — | $t$ 小时拉回无偏估计 |
| $\epsilon$ | 数值稳定常数 | $10^{-8}$ | 防止除零 |
| $\lambda$ | 权重衰减系数 | 0.01~0.1 | AdamW 中独立于自适应机制 |

---

## 6. 推导思路和思想来源

### 6.1 SGD → Momentum：物理直觉到数学公式

- **最初困难**：Hinton 等人在 1980s 训练早期神经网络时发现，SGD 在狭长峡谷中震荡严重，学习率一调大就发散，一调小就停滞。
- **关键转念**：Polyak (1964) 的 Heavy-Ball Method 从物理中汲取灵感——将参数更新类比为有质量的球在山坡上滚动，速度 $v_t$ 不仅依赖当前推力（梯度），还保留前一时刻的速度（惯性）。数学上，这就是一阶梯度 EMA。
- **为什么 EMA 而不是简单平均**：EMA 只用一个标量 $\beta$ 和上一时刻的 $v_{t-1}$ 就能表征加权历史，无需存储所有历史梯度。$\beta$ 越接近 1，记忆越长、惯性越大，但也越迟钝；$\beta$ 越小，反应越快，但震荡抑制减弱。

### 6.2 AdaGrad → RMSprop：从"历史包袱"到"滑动窗口"

- **AdaGrad 的初衷**（Duchi et al., 2011）：为每个参数独立调整学习率——频繁更新的参数（大梯度平方累积）步长自动缩小，稀疏更新的参数（小累积）步长保持较大。这对稀疏特征（NLP 词向量）极其有效。
- **灾难性遗忘问题**：$G_t = \sum_{i=1}^t g_i^2$ 单调递增，分母 $\sqrt{G_t}$ 无界增长。在训练深度网络时，$10^4$ 步之后学习率已衰减到几乎为零——深度网络不是稀疏特征，所有参数都在持续更新。
- **RMSprop 的矫正**（Hinton, 2012）：用 EMA 替代累加和。$\beta_2=0.9$ 时，$v_t$ 的有效窗口约为 $1/(1-\beta_2) = 10$ 步——只记住最近 ~10 步的梯度规模，历史被"遗忘"。这给了每个参数持续的适应性而不被过去禁锢。

### 6.3 Adam → AdamW：一个被忽视 5 年的正则化 Bug

- **Adam 的成功**（Kingma & Ba, 2015）：将 Momentum 和 RMSprop 结合，加上偏差校正，成为深度学习默认优化器。但实践中人们发现 Adam 的泛化性有时不如精心调参的 SGD + Momentum。
- **Loshchilov & Hutter 的洞见（2019）**：问题不在 Adam 的核心算法，而在**L2 正则化的实现方式**。传统框架（包括 PyTorch 早期 `Adam(weight_decay=...)`）将正则化耦合到梯度中——$\lambda \theta$ 进入 $m_t$ 和 $v_t$ 后，在梯度大的方向上衰减反而被抑制。解耦后，权重衰减直接作用在参数上，不再受自适应机制的"污染"。
- **实验验证**：AdamW 在 CIFAR-10/100、ImageNet 上一致优于 Adam+L2，且对 $\lambda$ 的敏感性大幅降低——超参搜索更容易。此论文（"Decoupled Weight Decay Regularization"）获 ICLR 2019 接收，PyTorch 自 1.2 起将 `AdamW` 设为独立类。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础 — 手算同一函数在 SGD/Momentum/Adam 下的 5 步迭代

考虑一个简单的二维二次函数（模拟峡谷地形，一个方向曲率大、一个方向曲率小）：

$$\mathcal{L}(x, y) = \frac{1}{2}\left( 10x^2 + y^2 \right)$$

初始点 $(x_0, y_0) = (3.0, 3.0)$，最优解为 $(0, 0)$。梯度：$\nabla \mathcal{L} = (10x, y)$。

设 $\eta = 0.1$，$\beta = 0.9$（Momentum），$\beta_1 = 0.9, \beta_2 = 0.999$（Adam），$\epsilon = 10^{-8}$。

#### 朴素 SGD（5 步）：

| 步 | $x_t$ | $y_t$ | $g_x = 10x$ | $g_y = y$ | $x_{t+1}=x_t-0.1g_x$ | $y_{t+1}=y_t-0.1g_y$ | $\mathcal{L}$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | 3.0000 | 3.0000 | 30.0000 | 3.0000 | 0.0000 | 2.7000 | 49.5000 |
| 1 | 0.0000 | 2.7000 | 0.0000 | 2.7000 | 0.0000 | 2.4300 | 3.6450 |
| 2 | 0.0000 | 2.4300 | 0.0000 | 2.4300 | 0.0000 | 2.1870 | 2.9525 |
| 3 | 0.0000 | 2.1870 | 0.0000 | 2.1870 | 0.0000 | 1.9683 | 1.9374 |
| 4 | 0.0000 | 1.9683 | 0.0000 | 1.9683 | 0.0000 | 1.7715 | 1.5698 |
| 5 | 0.0000 | 1.7715 | — | — | — | — | — |

> **观察**：SGD 第一步就在 $x$ 方向"过冲"到了对面的零点（$3.0 - 0.1\times 30 = 0$），恰好跨过了最优解。但 $y$ 方向每步仅缩减 $10\%$，$y$ 振荡缓慢下降。损失虽有下降但极慢——原因就是 $x$ 方向曲率（10）远大于 $y$ 方向（1），统一学习率无法兼顾。

#### SGD + Momentum（$\beta=0.9$，5 步）：

$v_x$ 和 $v_y$ 初始化为 0。

| 步 | $x_t$ | $y_t$ | $g_x$ | $g_y$ | $v_x$ | $v_y$ | $x_{t+1}$ | $y_{t+1}$ | $\mathcal{L}$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | 3.0000 | 3.0000 | 30.0 | 3.0 | 3.0000 | 0.3000 | 2.7000 | 2.9700 | 40.8605 |
| 1 | 2.7000 | 2.9700 | 27.0 | 2.97 | 5.4000 | 0.5670 | 2.1600 | 2.9133 | 27.5713 |
| 2 | 2.1600 | 2.9133 | 21.6 | 2.91 | 7.0200 | 0.8016 | 1.4580 | 2.8331 | 16.2407 |
| 3 | 1.4580 | 2.8331 | 14.58 | 2.83 | 7.7760 | 1.0047 | 0.6804 | 2.7326 | 7.9733 |
| 4 | 0.6804 | 2.7326 | 6.804 | 2.73 | 7.6788 | 1.1775 | -0.0875 | 2.6149 | 3.7383 |
| 5 | -0.0875 | 2.6149 | — | — | — | — | — | — | — |

> **观察**：Momentum 在 $x$ 方向由于梯度方向一致，惯性累加、收敛远超 SGD——第 5 步 $x$ 已接近零点。但 $y$ 方向上由于动量同样在累积，震荡的幅度反而比纯 SGD 更大——这是 Momentum 的 trade-off：信号方向加速，噪声方向也可能被放大。

#### Adam（$\beta_1=0.9, \beta_2=0.999$，5 步）：

| 步 | $x_t$ | $y_t$ | $m_x$ | $m_y$ | $v_x$ | $v_y$ | $\hat{x}_{t+1}$ | $\hat{y}_{t+1}$ | $\mathcal{L}$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | 3.0000 | 3.0000 | 3.0000 | 0.3000 | 0.9000 | 0.0090 | 2.6837 | 2.6837 | 40.8605* |
| 1 | 2.6837 | 2.6837 | 5.4684 | 0.5384 | 1.6180 | 0.0162 | 2.0364 | 2.4153 | 26.9434* |
| 2 | 2.0364 | 2.4153 | 7.3521 | 0.7115 | 2.1967 | 0.0218 | 1.1714 | 2.1877 | 14.7873* |
| 3 | 1.1714 | 2.1877 | 8.4266 | 0.8465 | 2.6360 | 0.0263 | 0.2334 | 2.0057 | 6.6840* |
| 4 | 0.2334 | 2.0057 | 8.7027 | 0.9474 | 2.9592 | 0.0299 | -0.5665 | 1.8548 | 2.9885* |
| 5 | -0.5665 | 1.8548 | — | — | — | — | — | — | — |

> *注：Adam 的精确值依赖于 $\epsilon$ 和逐步偏差校正，以上为近似计算。核心观察：$x$ 方向的大梯度被 $\sqrt{v_x}$ 压制（自适应步长缩小），$y$ 方向的小梯度被 $\sqrt{v_y}$ 放大——两个方向的收敛速度被"拉平"。与 SGD 不同，Adam 不会在 $x$ 方向一步跨过零点，而是稳步推进。

**关键对比总结**：
- **SGD**：$x$ 一步过冲到零点，$y$ 方向蜗牛爬行 —— 严重受制于方向曲率差异。
- **Momentum**：$x$ 方向加速收敛（惯性叠加），$y$ 震荡更大——惯性帮了"趋势"方向但也放大了"噪声"方向。
- **Adam**：$x$ 大梯度被压制（分母大），$y$ 小梯度被放大（分母小）——两个方向收敛趋于平衡，无需手动调每维度学习率。

---

### 例子 2：中等 — PyTorch 中不同优化器的收敛曲线对比

```python
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np

# === 造一个病态二次函数（峡谷地形） ===
def loss_fn(theta):
    """ f(x, y) = 0.5 * (10*x^2 + y^2)，模拟峡谷 """
    return 0.5 * (10 * theta[:, 0]**2 + theta[:, 1]**2)

# === 训练函数 ===
def train_one_epoch(opt_class, lr, n_steps=200, **kwargs):
    theta = torch.tensor([[3.0, 3.0]], requires_grad=True)
    optimizer = opt_class([theta], lr=lr, **kwargs)
    path = [theta.detach().clone().numpy().flatten()]

    for _ in range(n_steps):
        optimizer.zero_grad()
        loss = loss_fn(theta)
        loss.backward()
        optimizer.step()
        path.append(theta.detach().clone().numpy().flatten())
    return np.array(path)

# === 运行所有优化器 ===
paths = {
    "SGD (lr=0.1)":          train_one_epoch(optim.SGD,  lr=0.1),
    "Momentum (lr=0.1, β=0.9)": train_one_epoch(optim.SGD,  lr=0.1, momentum=0.9),
    "NAG (lr=0.1, β=0.9)":    train_one_epoch(optim.SGD,  lr=0.1, momentum=0.9, nesterov=True),
    "RMSprop (lr=0.1)":       train_one_epoch(optim.RMSprop, lr=0.1),
    "Adam (lr=0.1)":          train_one_epoch(optim.Adam, lr=0.1),
    "AdamW (lr=0.1)":         train_one_epoch(optim.AdamW, lr=0.1, weight_decay=0.01),
}

# === 绘制收敛路径（等高线 + 轨迹） ===
x = np.linspace(-4, 4, 200)
y = np.linspace(-4, 4, 200)
X, Y = np.meshgrid(x, y)
Z = 0.5 * (10 * X**2 + Y**2)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for ax, (name, path) in zip(axes, paths.items()):
    ax.contour(X, Y, Z, levels=30, cmap='viridis', alpha=0.6)
    ax.plot(path[:, 0], path[:, 1], 'r.-', markersize=3, linewidth=1.2)
    ax.plot(0, 0, 'g*', markersize=12)                   # 最优解
    ax.plot(path[0, 0], path[0, 1], 'bo', markersize=8)  # 起点
    ax.set_title(name, fontsize=11)
    ax.set_xlabel('x (高曲率)')
    ax.set_ylabel('y (低曲率)')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')

plt.suptitle('不同优化器在峡谷函数 $f(x,y)=5x^2+0.5y^2$ 上的收敛路径（200步）', fontsize=14)
plt.tight_layout()
plt.savefig('optimizer_comparison.png', dpi=150)
plt.show()

# === 打印最终损失 ===
print("\n最终损失对比（200步后）：")
for name, path in paths.items():
    final = torch.tensor(path[-1:])
    print(f"  {name:30s}: loss = {loss_fn(final).item():.6f}")
```

**预期结果**（在峡谷函数上运行 200 步）：
- **SGD**：路径剧烈 Z 字形震荡，收敛最慢。
- **Momentum**：震荡幅度减小，收敛显著加快。
- **NAG**：路径更平滑，比普通 Momentum 更早趋向最优解。
- **RMSprop**：每个方向自适应步长，路径像"直线"走向目标——x 方向步长被自动压缩。
- **Adam**：兼具惯性与自适应，收敛最快、路径最平滑。
- **AdamW**：在此简单函数上与 Adam 几乎一致（无正则化需求时两者等价）。

---

### 例子 3：实际应用 — CIFAR-10 上完整训练对比

```python
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

# === 数据准备 ===
transform_train = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

trainset = torchvision.datasets.CIFAR10(
    root='./data', train=True, download=True, transform=transform_train)
trainloader = DataLoader(trainset, batch_size=128, shuffle=True, num_workers=2)

# === 小型 ResNet（简化版） ===
class TinyResNet(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.net = nn.Sequential(
            # 初始卷积
            nn.Conv2d(3, 64, 3, padding=1, bias=False),
            nn.BatchNorm2d(64), nn.ReLU(inplace=True),
            # 两个残差块
            self._make_block(64, 64, stride=1),
            self._make_block(64, 128, stride=2),
            nn.AdaptiveAvgPool2d(1),
        )
        self.fc = nn.Linear(128, num_classes)

    def _make_block(self, in_c, out_c, stride):
        return nn.Sequential(
            nn.Conv2d(in_c, out_c, 3, stride, 1, bias=False),
            nn.BatchNorm2d(out_c), nn.ReLU(inplace=True),
            nn.Conv2d(out_c, out_c, 3, 1, 1, bias=False),
            nn.BatchNorm2d(out_c), nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.fc(self.net(x).squeeze(-1).squeeze(-1))

# === 训练函数 ===
def train_model(name, opt_class, lr, epochs=30, **kwargs):
    model = TinyResNet().cuda()
    criterion = nn.CrossEntropyLoss()
    optimizer = opt_class(model.parameters(), lr=lr, **kwargs)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    history = {'train_loss': [], 'train_acc': []}
    for epoch in range(epochs):
        model.train()
        total_loss, correct, total = 0.0, 0, 0
        for inputs, targets in trainloader:
            inputs, targets = inputs.cuda(), targets.cuda()
            optimizer.zero_grad()
            loss = criterion(model(inputs), targets)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            _, pred = model(inputs).max(1)
            correct += pred.eq(targets).sum().item()
            total += targets.size(0)
        scheduler.step()
        history['train_loss'].append(total_loss / len(trainloader))
        history['train_acc'].append(100. * correct / total)
        print(f"[{name}] Epoch {epoch+1:2d}/{epochs} | "
              f"Loss: {history['train_loss'][-1]:.4f} | "
              f"Acc: {history['train_acc'][-1]:.2f}%")
    return history

# === 跑 4 个优化器对比 ===
results = {}
results["SGD+Momentum"] = train_model("SGD+M", optim.SGD,  lr=0.1, momentum=0.9, weight_decay=5e-4)
results["Adam"]         = train_model("Adam",   optim.Adam, lr=0.001)
results["AdamW"]        = train_model("AdamW",  optim.AdamW, lr=0.001, weight_decay=0.05)
results["RMSprop"]      = train_model("RMSprop", optim.RMSprop, lr=0.001, weight_decay=5e-4)
```

**预期结果（CIFAR-10, 30 epochs）**：

| 优化器 | 最终 Train Acc | 学习率 | 备注 |
| :--- | :---: | :---: | :--- |
| SGD + Momentum (lr=0.1, wd=5e-4) | ~94% | 需精调 | 对 lr 极其敏感，lr=0.01 只有 ~88% |
| Adam (lr=0.001) | ~92% | 默认即可 | 收敛快但泛化略逊 |
| AdamW (lr=0.001, wd=0.05) | **~95%** | 默认即可 | **最优，CV 首选** |
| RMSprop (lr=0.001, wd=5e-4) | ~91% | 默认即可 | 作为 Adam 的前身，略逊 |

**关键启示**：
- AdamW 在默认设置下就能接近或超越精调后的 SGD+Momentum——对工程效率是巨大提升。
- Adam 不加 weight_decay 时泛化略逊，因为缺少正则化——但若加入 weight_decay（Adam+L2 风格），泛化改善有限且不稳定。AdamW 解耦后才真正释放 weight_decay 的威力。

---

## 8. 常见误区和易混概念

### 误区 1：Adam 总是比 SGD 好

- **错误直觉**："Adam 是最先进的，所有场景都用 Adam 就行。"
- **为什么错**：Adam 的自适应学习率在训练初期收敛极快，但在训练的后期——当梯度变得很小且噪声主导时——Adam 的二阶动量 $v_t$ 可能累积噪声而非信号，导致"自适应步长不稳定"。Wilson et al. (2017) 的著名论文"*The Marginal Value of Adaptive Gradient Methods in Machine Learning*"指出，在 ImageNet 上 SGD+Momentum 精心调参后，泛化误差可比 Adam 低 1-2%。Adam 是"快而稳"，SGD 是"慢而准"——取决于你的优先目标。
- **正确理解**：CV 领域 AdamW 已解决大部分泛化问题；但在极端追求 SOTA 的 ImageNet 竞赛场景，SGD+Momentum+Cosine Annealing LR 仍是强有力选择。

### 误区 2：Nesterov 只是 Momentum 的变体，区别可忽略

- **错误直觉**："NAG 和 Momentum 差不多，用哪个无所谓。"
- **为什么错**：NAG 的"前瞻"在曲率突然变化的地形上显著优于标准 Momentum——它提前"感知"到前方陡坡，提前减速，避免冲过头。在 RNN/LSTM 的训练中（损失地形极端崎岖），NAG 常比标准 Momentum 快 20-30% 收敛。PyTorch 中只需设置 `nesterov=True` 即可启用——零成本收益。
- **正确实践**：使用 SGD+Momentum 时，默认开启 `nesterov=True`。

### 误区 3：AdamW 的 weight_decay 和 Adam 的 weight_decay 参数是一回事

- **错误直觉**："PyTorch 中 `Adam(weight_decay=...)` 和 `AdamW(weight_decay=...)` 效果一样。"
- **为什么错**：这是 AdamW 论文要纠正的核心误解！`Adam(weight_decay=0.01)` 是在梯度上加上 $0.01\theta$，再送入 $m_t$/$v_t$——这不是真正的"权重衰减"，而是"L2 正则化被自适应污染"的版本。`AdamW(weight_decay=0.01)` 则是直接在参数上执行 $\theta \leftarrow \theta - \eta \cdot 0.01 \cdot \theta$——与自适应机制解耦。两者的优化轨迹在训练后期显著分化。
- **正确实践**：训练 CV 模型时，优先使用 `optim.AdamW` 并显式设置 `weight_decay`（通常 0.01~0.1）。

### 误区 4：Adam 的 β 参数调不调都一样

- **错误直觉**："$\beta_1=0.9, \beta_2=0.999$ 是论文默认值，不需要动。"
- **为什么不完全对**：默认值在大多数场景下确实有效，但有两个值得微调的场景：
  - **GAN 训练**：常用 $\beta_1=0.5$（降低一阶惯性以更快响应判别器/生成器的快速切换）。
  - **小 batch / 高噪声梯度**：可适当增大 $\beta_2$ 到 0.9999 以增加二阶 EMA 窗口长度，平滑噪声。
- **正确理解**：默认值是优秀的起点，但在极端场景下有调整空间。

### 概念对比表

| 特性 | SGD | SGD+Momentum | NAG | AdaGrad | RMSprop | Adam | AdamW |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 一阶惯性 | ❌ | ✅ | ✅ (前瞻) | ❌ | ❌ | ✅ | ✅ |
| 自适应学习率 | ❌ | ❌ | ❌ | ✅ (累加) | ✅ (EMA) | ✅ | ✅ |
| 偏差校正 | — | — | — | — | — | ✅ | ✅ |
| 权重衰减解耦 | — | — | — | — | — | ❌ | ✅ |
| 建议 LR (CV) | 0.01 | 0.01 | 0.01 | 0.01 | 0.001 | 0.001 | 0.001 |
| 收敛速度 | 慢 | 中 | 中快 | 中（会停止） | 快 | 很快 | 很快 |
| 泛化性能 | 高（精调） | 高 | 高 | 中 | 中高 | 中高 | **高** |
| CV 首选度 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | **⭐⭐⭐⭐⭐** |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[梯度下降CV|梯度下降与优化基础]]：SGD 的数学定义和批量/随机 trade-off。
- [[反向传播与计算图]]：`loss.backward()` 产出的梯度是优化器的输入。

### 下游延伸
- [[LoRA]]：LoRA 的优化器选择（通常 AdamW）直接影响微调效果。
- [[学习率调度策略|学习率调度]]：优化器和学习率调度是"油门"和"驾驶模式"的关系——CosineAnnealingLR + AdamW 是现代 CV 标配。

### 横向关联
- [[批归一化BatchNorm|BatchNorm]]：BN 平滑损失地形后，Adam 的自适应优势更加明显——BN + AdamW 是黄金搭档。
- [[数据增强与正则化|权重正则化]]：AdamW 的"解耦"思想改变了整个正则化的实现方式——不再通过修改梯度注入，而是独立衰减。
- 混合精度训练：Adam 的二阶动量 $v_t$ 在 FP16 下容易下溢，PyTorch AMP 自动用 FP32 维护优化器状态——这是工程实践中必须知道的细节。

---

## 10. 闭卷复现任务

- [ ] 1. 用三段话解释：SGD 在峡谷地形中为什么震荡，Momentum 如何解决，以及 Momentum 的潜在代价是什么。
- [ ] 2. 默写 Momentum、RMSprop、Adam 的核心更新公式（可以不用偏差校正）。
- [ ] 3. 解释 NAG 与标准 Momentum 的唯一区别，并画出两者的"先滑再修正" vs "先看再滑"的示意图。
- [ ] 4. 写出 Adam 的偏差校正公式，解释为什么 $t=1$ 时未经校正的 $m_1$ 只有实际梯度的 $10\%$。
- [ ] 5. 用自己的话解释：为什么 AdaGrad 在深度学习中不可用，RMSprop 如何修正它。
- [ ] 6. 写出 AdamW 的更新公式中解耦权重衰减的关键项，解释它与 Adam+L2 的本质区别。
- [ ] 7. 在纸上手算：$\mathcal{L}(x,y)=5x^2+0.5y^2$，起点 $(3,3)$，用 SGD (lr=0.1) 和 Momentum (β=0.9) 各迭代 3 步，列出每一步的 $(x,y)$ 坐标。
- [ ] 8. 写出 PyTorch 中创建以下优化器的代码：SGD+Momentum+NAG、Adam、AdamW。
- [ ] 9. 回答优化器选择决策问题：CV 分类任务、NLP Transformer、GAN、Reinforcement Learning 分别首选什么优化器？
- [ ] 10. 解释为什么 Adam 和 AdamW 在 `weight_decay=0` 时行为完全一致。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | Momentum 与 NAG 的"前瞻"差异 |
| 2 | 公式推导 | 中等 | Adam 偏差校正的 $t=1$ 特例计算 |
| 3 | 问题诊断 | 中等 | AdaGrad 训练后期停滞的原因 |
| 4 | 公式书写 | 较难 | AdamW 解耦权重衰减的完整更新式 |
| 5 | 实践决策 | 较难 | 不同场景下的优化器选择与超参数建议 |

### 题目与解析

#### 1. Nesterov Accelerated Gradient (NAG) 与标准 Momentum 的核心区别是？
- A. NAG 使用 $\beta_2$ 做二阶动量，Momentum 只用一阶
- B. NAG 在"前瞻位置" $\theta_t - \eta\beta v_{t-1}$ 处计算梯度，而非当前位置
- C. NAG 的学习率在训练过程中自动衰减
- D. NAG 对每个参数使用独立的学习率

> [!question]- 答案解析
> - **答案**：B
> - **解析**：NAG 的核心创新在于"先看再跳"——先沿当前速度方向滑半步，在那个前瞻位置计算梯度，再综合修正。A 混淆了 NAG 和 Adam；C 描述的是 AdaGrad 的副作用或学习率调度；D 描述的是自适应方法（AdaGrad/RMSprop/Adam）。
> - **对应章节**：§5.3。

#### 2. 在 Adam 的第一步更新中（$t=1$），若 $g_1 = 10$，未经校正的 $m_1$ 和校正后的 $\hat{m}_1$ 分别是多少？设 $\beta_1 = 0.9$。
- A. $m_1 = 10, \hat{m}_1 = 10$
- B. $m_1 = 1, \hat{m}_1 = 10$
- C. $m_1 = 9, \hat{m}_1 = 10$
- D. $m_1 = 1, \hat{m}_1 = 1$

> [!question]- 答案解析
> - **答案**：B
> - **解析**：$m_0 = 0$，所以 $m_1 = \beta_1 \cdot 0 + (1 - 0.9) \cdot 10 = 1$。$\hat{m}_1 = m_1 / (1 - 0.9^1) = 1 / 0.1 = 10$。校正正好将 1 拉回 10。若不加校正，Adam 的第一步更新幅度仅为预期的 10%，训练初期几乎停滞。
> - **对应章节**：§5.6。

#### 3. 用 AdaGrad 训练一个深度网络 1000 步后，训练几乎完全停滞。最可能的原因是？
- A. 网络陷入了局部极小值
- B. $G_t = \sum_{i=1}^t g_i^2$ 无限累积导致 $\eta / \sqrt{G_t + \epsilon}$ 趋近于 0
- C. $\beta_2 = 0.999$ 过大导致二阶动量记忆过长
- D. 梯度爆炸导致参数更新发散

> [!question]- 答案解析
> - **答案**：B
> - **解析**：这是 AdaGrad 的核心缺陷——$G_t$ 是历史梯度平方的累加和，单调递增、永不清零。每步 $G_t$ 都在变大，分母 $\sqrt{G_t}$ 无界增长，学习率最终衰减至零。A 可能在 SGD 中发生，但"完全停滞"是 AdaGrad 的典型特征。C 混淆了 Adam。D 描述的是发散，而非停滞。
> - **对应章节**：§5.4-5.5。

#### 4. 【推导】写出 AdamW 中同时包含自适应更新和解耦权重衰减的完整一步参数更新公式，并标注哪一项是"解耦"的关键。

> [!question]- 答案解析
> - **答案**：
>   $$\theta_{t+1} = \theta_t - \eta \cdot \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} \quad\underbrace{- \eta \lambda \theta_t}_{\text{解耦的权重衰减}}$$
>   解耦关键：$\lambda \theta_t$ 独立于 $\hat{m}_t$ 和 $\hat{v}_t$，不经过自适应矩阵缩放。对比 Adam+L2 的写法：$\theta_{t+1} = \theta_t - \eta \cdot \frac{\hat{m}_t + \lambda \theta_t / \sqrt{\hat{v}_t}}{\sqrt{\hat{v}_t} + \epsilon}$，其中 $\lambda \theta_t$ 被 $\sqrt{\hat{v}_t}$ "污染"了。
> - **对应章节**：§5.7。

#### 5. 【实践】以下哪些场景的优化器选择是合理的？
- A. 用 ResNet-50 在 ImageNet 上追求 SOTA → 使用 SGD + Momentum (β=0.9) + CosineAnnealingLR + 精细调参
- B. 用 ViT-Base 在 CIFAR-100 上快速实验 → 使用 AdamW (lr=1e-3, wd=0.05)
- C. 训练一个 GAN 的生成器 → 使用 Adam (β₁=0.5, lr=2e-4)
- D. 以上都是合理的

> [!question]- 答案解析
> - **答案**：D
> - **解析**：A 是 ImageNet 竞赛的经典方案——SGD+Momentum 精调后可获得最优泛化性。B 是现代 CV 的标准方案——AdamW 快速稳定且泛化好。C 是 GAN 训练的标准选择——Adam 的 β₁=0.5 降低惯性以匹配对抗训练的快速动力学切换。三种场景各有最优解，没有"一招鲜"。
> - **对应章节**：§8 概念对比表 + §2 实际应用场景。

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

### 我的推导复现
> 不看上文，尝试默写 Momentum、RMSprop、Adam、AdamW 的核心更新公式：

### 我的对比表
> 不看上文，画出优化器演进路线图：
> SGD → ______ → ______ → ______ → ______ → ______ → ______
> 并标注每一步"修了前一步的什么 bug"

### 我的决策树
> 不看上文，写出：CV 分类、NLP Transformer、GAN、小 batch 目标检测 分别首选什么优化器？

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
  - [[🧠 第二阶段：深度学习内核|第二阶段：深度学习内核]]
  - [[梯度下降CV|梯度下降与优化基础]]
  - [[反向传播与计算图]]
  - [[学习率调度策略|学习率调度]]
  - [[批归一化BatchNorm|BatchNorm]]
  - [[数据增强与正则化|权重正则化]]
  - 混合精度训练
- **建议标签**：`#学习` `#计算机视觉` `#优化器` `#SGD` `#Adam` `#AdamW` `#Momentum` `#训练优化`

---
---

## 学完后可以完成

- [[05-计算机视觉-课后作业-03-小型CNN与训练工程|HW03]]：单因素对照优化器

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
