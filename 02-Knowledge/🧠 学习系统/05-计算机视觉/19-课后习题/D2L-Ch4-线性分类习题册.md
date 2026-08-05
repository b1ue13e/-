---
type: project
topic: "D2L Ch.4 线性分类课后习题"
created: 2026-08-05
status: active
flow: project
tags: [计算机视觉, 课后习题, D2L, 线性分类]
---

# 📐 D2L Ch.4 线性神经网络分类（Linear Neural Networks for Classification）课后习题册

> 基于 [Dive into Deep Learning (D2L)](https://d2l.ai/chapter_linear-classification/index.html) 第4章（CC BY-SA 4.0），共8道习题。
> 覆盖：Softmax公式推导、交叉熵损失计算、线性分类器决策边界、one-hot编码、数值稳定性（log-sum-exp trick）、softmax回归从零实现思路、Fashion-MNIST分类实验设计。
> 每道题标注考查知识点与对应知识卡，形成「学→练→测」闭环。

---

## 🗺️ 知识地图

| 题号 | 题目 | 考查知识点 | 对应知识卡 | 难度 |
|:---:|:---|:---|:---|:---:|
| 1 | Softmax从得分到概率：公式推导与性质验证 | Softmax函数定义、指数归一化、概率性质 | [[Softmax与SVM损失函数]]、[[线性代数基础CV]] | ⭐⭐ |
| 2 | 交叉熵损失的手算与梯度推导 | 交叉熵公式、one-hot、梯度$p_j - \mathbb{1}[j=y_i]$ | [[Softmax与SVM损失函数]]、[[梯度计算]] | ⭐⭐⭐ |
| 3 | 线性分类器的决策边界：几何直觉与代数推导 | 打分函数、超平面方程、线性可分的充要条件 | [[kNN与线性分类器]]、[[线性代数基础CV]] | ⭐⭐ |
| 4 | One-Hot编码与交叉熵的信息论视角 | one-hot编码、交叉熵$H(\mathbf{y},\mathbf{p})$、KL散度 | [[Softmax与SVM损失函数]] | ⭐ |
| 5 | Log-Sum-Exp与数值稳定性：为什么Softmax会溢出 | 指数溢出、log-sum-exp trick、代码实现 | [[Softmax与SVM损失函数]]、[[梯度计算]] | ⭐⭐⭐ |
| 6 | Softmax回归从零实现：模块设计与训练循环 | 数据管线、前向传播、损失计算、参数更新 | [[Softmax与SVM损失函数]]、[[前向传播]]、[[梯度下降CV]] | ⭐⭐⭐ |
| 7 | Fashion-MNIST分类实验：从数据到模型评估 | 数据集加载、超参数调优、混淆矩阵、消融实验 | [[图像分类任务与数据管线]]、[[kNN与线性分类器]] | ⭐⭐⭐ |
| 8 | 线性分类与非线性分类：边界、局限与突破 | 线性可分性、XOR问题、非线性特征变换 | [[kNN与线性分类器]]、[[激活函数CV]] | ⭐ |

---

## 习题

---

### 习题 1 · Softmax从得分到概率：公式推导与性质验证

> 📘 **考查**：Softmax函数定义与概率性质 | 🏷️ **对应卡**：[[Softmax与SVM损失函数]] [[线性代数基础CV]]
> 📖 **D2L参考**：Ch.4.1 Softmax Regression

**题目**：Softmax函数是连接"原始得分"与"概率分布"的桥梁。对于一个$C$类分类问题，给定得分向量 $\mathbf{s} = [s_1, s_2, \dots, s_C]^\top \in \mathbb{R}^C$，Softmax函数定义为：

$$p_j = \text{softmax}(\mathbf{s})_j = \frac{e^{s_j}}{\sum_{k=1}^{C} e^{s_k}}$$

**(a)** 证明：对任意 $\mathbf{s}$，Softmax输出 $\mathbf{p}$ 构成一个合法的概率分布：即 $\forall j, p_j \in (0, 1)$ 且 $\sum_{j=1}^{C} p_j = 1$。

**(b)** 平移不变性证明：对任意标量 $c \in \mathbb{R}$，证明 $\text{softmax}(\mathbf{s} + c\mathbf{1}) = \text{softmax}(\mathbf{s})$，其中 $\mathbf{1} = [1, 1, \dots, 1]^\top$。解释这一性质为何对数值稳定性至关重要。

**(c)** 给定得分 $\mathbf{s} = [2.0, 1.0, 0.5]$（$C=3$），手算Softmax输出概率 $\mathbf{p}$（保留3位小数）。哪个类别被预测？

**(d)** 若将得分整体放大10倍（$\mathbf{s}' = [20, 10, 5]$），Softmax输出有何变化？这揭示了什么特性？

---

<details>
<summary><b>📝 参考答案要点</b></summary>

**(a)** 合法概率分布：
- $p_j > 0$：因为 $e^{s_j} > 0$（指数函数恒正），分子分母均为正数 → $p_j > 0$。
- $p_j < 1$：因为分母 $\sum_k e^{s_k} > e^{s_j}$（除非只有一类），所以 $p_j < 1$。
- $\sum_j p_j = \frac{\sum_j e^{s_j}}{\sum_k e^{s_k}} = 1$（分子分母相同）。

**(b)** 平移不变性：
$$\text{softmax}(\mathbf{s} + c\mathbf{1})_j = \frac{e^{s_j + c}}{\sum_k e^{s_k + c}} = \frac{e^{c} \cdot e^{s_j}}{e^{c} \cdot \sum_k e^{s_k}} = \frac{e^{s_j}}{\sum_k e^{s_k}}$$

因子 $e^c$ 从分子分母中同时约掉。这就是log-sum-exp数值稳定技巧的数学基础：我们可以将所有得分减去最大值（$c = -\max_k s_k$），保证指数参数 $\le 0$，避免 $e^{\text{大正数}}$ 溢出为 `inf`。

**(c)** 手算：
- $e^{2.0} = 7.389$，$e^{1.0} = 2.718$，$e^{0.5} = 1.649$
- $\sum e^{s_k} = 7.389 + 2.718 + 1.649 = 11.756$
- $\mathbf{p} = [7.389/11.756,\; 2.718/11.756,\; 1.649/11.756] = [0.629,\; 0.231,\; 0.140]$
- 预测：类别1（$p_1 = 0.629$ 最高）。

**(d)** 放大效应：
- $e^{20} \approx 4.85 \times 10^8$，$e^{10} \approx 2.20 \times 10^4$，$e^5 \approx 148$
- $\mathbf{p}' \approx [1.000,\; 0.000,\; 0.000]$
- 得分的整体放大使Softmax分布变得**极其尖锐**（接近one-hot），这揭示了Softmax的"自信度"依赖于得分之间的**绝对差值**而非相对比例，也是知识蒸馏中温度参数 $T$ 反向操作的动机。

> 🔗 **对比**：这就是为什么训练良好的模型Softmax输出往往接近 one-hot（高度自信），而未经校准的"概率"并不是真正的 $P(y|\mathbf{x})$。

</details>

---

### 习题 2 · 交叉熵损失的手算与梯度推导

> 📘 **考查**：交叉熵公式推导 | 🏷️ **对应卡**：[[Softmax与SVM损失函数]] [[梯度计算]]
> 📖 **D2L参考**：Ch.4.1 Softmax Regression, Ch.4.3 The Base Classification Model

**题目**：对于一个样本 $(\mathbf{x}, y)$，给定得分 $\mathbf{s} = f(\mathbf{x}; \mathbf{W}, \mathbf{b})$，Softmax + 交叉熵的损失定义为：

$$L = -\ln p_{y} = -\ln\left(\frac{e^{s_{y}}}{\sum_{k=1}^{C} e^{s_k}}\right) = -s_{y} + \ln\sum_{k=1}^{C} e^{s_k}$$

**(a)** 写出交叉熵损失的**信息论定义** $H(\mathbf{y}, \mathbf{p}) = -\sum_{j=1}^{C} y_j \ln p_j$，解释为什么在one-hot标签下这个定义等价于 $-\ln p_{y}$。

**(b)** 核心推导：证明Softmax + 交叉熵对得分 $s_j$ 的梯度为：

$$\frac{\partial L}{\partial s_j} = p_j - \mathbb{1}[j = y]$$

请分两种情况（$j = y$ 和 $j \neq y$）完成推导。提示：将损失写为 $L = -s_y + \ln Z$，其中 $Z = \sum_k e^{s_k}$，先求 $\frac{\partial \ln Z}{\partial s_j}$。

**(c)** 验证梯度之和为零：证明 $\sum_{j=1}^{C} \frac{\partial L}{\partial s_j} = 0$。这个性质对SGD更新有什么隐含意义？

**(d)** 给定 $\mathbf{s} = [2.0, 1.0, 0.5]$，$y = 1$（类别1是正确答案），用习题1的 $\mathbf{p}$ 和上面推导的梯度公式计算 $\frac{\partial L}{\partial s_1}$、$\frac{\partial L}{\partial s_2}$、$\frac{\partial L}{\partial s_3}$。

---

<details>
<summary><b>📝 参考答案要点</b></summary>

**(a)** one-hot下等价性：
- 交叉熵 $H(\mathbf{y}, \mathbf{p}) = -\sum_{j=1}^{C} y_j \ln p_j$
- $\mathbf{y}$ 是one-hot编码：$y_{y}=1$，其余 $y_j = 0$（$j \neq y$）
- 因此 $H(\mathbf{y}, \mathbf{p}) = -1 \cdot \ln p_y - \sum_{j \neq y} 0 \cdot \ln p_j = -\ln p_y$

**(b)** 梯度推导：

将损失写为 $L = -s_y + \ln Z$，其中 $Z = \sum_{k=1}^{C} e^{s_k}$。

首先计算公共项：$\frac{\partial}{\partial s_j} \ln Z = \frac{1}{Z} \cdot \frac{\partial Z}{\partial s_j} = \frac{e^{s_j}}{Z} = p_j$

**情况1**：$j = y$（对正确类得分求导）
$$\frac{\partial L}{\partial s_y} = -\frac{\partial s_y}{\partial s_y} + \frac{\partial \ln Z}{\partial s_y} = -1 + p_y = p_y - 1$$

**情况2**：$j \neq y$（对错误类得分求导）
$$\frac{\partial L}{\partial s_j} = -0 + \frac{\partial \ln Z}{\partial s_j} = p_j = p_j - 0$$

**统一**：$\frac{\partial L}{\partial s_j} = p_j - \mathbb{1}[j = y]$

> 💡 直觉解读：正确类的梯度为负（$p_y - 1 < 0$，推动 $s_y$ 增大），错误类的梯度为正（$p_j > 0$，推动 $s_j$ 减小）。这个**优雅简洁的梯度形式**是Softmax+CE被广泛使用的核心原因之一。

**(c)** 梯度之和为零：
$$\sum_{j=1}^{C} \frac{\partial L}{\partial s_j} = \sum_{j=1}^{C} (p_j - \mathbb{1}[j=y]) = \left(\sum_{j=1}^{C} p_j\right) - 1 = 1 - 1 = 0$$

**隐含意义**：梯度分量之和为零意味着在梯度下降更新中，某些得分上升的量恰好等于另一些得分下降的量——更新的总"能量"守恒，优化过程稳定。这在数值上也是一种自我调节。

**(d)** 数值计算（$\mathbf{p} = [0.629, 0.231, 0.140]$，$y=1$）：
- $\frac{\partial L}{\partial s_1} = p_1 - 1 = 0.629 - 1 = -0.371$
- $\frac{\partial L}{\partial s_2} = p_2 - 0 = 0.231$
- $\frac{\partial L}{\partial s_3} = p_3 - 0 = 0.140$

验证：$-0.371 + 0.231 + 0.140 = 0$ ✓

</details>

---

### 习题 3 · 线性分类器的决策边界：几何直觉与代数推导

> 📘 **考查**：线性分类器决策边界的代数推导与几何直觉 | 🏷️ **对应卡**：[[kNN与线性分类器]] [[线性代数基础CV]]
> 📖 **D2L参考**：Ch.4.1 Softmax Regression

**题目**：线性分类器对每个类别 $j$ 输出一个得分 $s_j = \mathbf{w}_j^\top \mathbf{x} + b_j$（或统一写为 $\mathbf{s} = \mathbf{W}\mathbf{x} + \mathbf{b}$），预测结果为 $\hat{y} = \arg\max_j s_j$。

**(a)** 两个类别 $j$ 和 $k$ 之间的决策边界由 $s_j = s_k$ 定义。推导该决策边界的方程，证明它是 $\mathbf{x}$ 空间中的一个**超平面**（hyperplane），并写出其法向量。

**(b)** 考虑二分类问题（$C=2$），输入 $\mathbf{x} \in \mathbb{R}^2$（二维平面），分类器参数为：
$$\mathbf{w}_1 = [1, 0],\; b_1 = 0;\quad \mathbf{w}_2 = [0, 1],\; b_2 = -1$$

写出决策边界方程，画出两类区域。点 $(2, 0)$、$(0, 2)$、$(2, 2)$ 分别被分到哪一类？

**(c)** 以下二维数据集哪些是**线性可分**的？哪些不是？简述判断理由。
- A：`○(0,0), ○(0,1), ×(1,0), ×(1,1)`（两个类沿对角线分开）
- B：`○(0,0), ×(0,1), ×(1,0), ○(1,1)`（XOR问题）
- C：`○(0,0), ○(0,1), ○(0,2), ×(2,0), ×(2,1), ×(2,2)`（两个竖排）

**(d)** 对于(b)中线性不可分的数据集，如果允许你先对输入做一个非线性变换 $\phi(\mathbf{x}) = [x_1, x_2, x_1 x_2]^\top$（引入乘积特征），然后用线性分类器 $\mathbf{s} = \mathbf{W}\phi(\mathbf{x}) + \mathbf{b}$ 在这个三维特征空间中分类，能否变为可分的？简要说明。

---

<details>
<summary><b>📝 参考答案要点</b></summary>

**(a)** 决策边界的超平面性质：

由 $s_j = s_k$ 得：
$$\mathbf{w}_j^\top \mathbf{x} + b_j = \mathbf{w}_k^\top \mathbf{x} + b_k$$
$$(\mathbf{w}_j - \mathbf{w}_k)^\top \mathbf{x} + (b_j - b_k) = 0$$

这是 $\mathbf{x}$ 的**线性方程**，形式为 $\mathbf{n}^\top \mathbf{x} + d = 0$，其中：
- **法向量** $\mathbf{n} = \mathbf{w}_j - \mathbf{w}_k$（指向从类别 $k$ 到类别 $j$ 的方向）
- **偏移量** $d = b_j - b_k$

在二维是直线，三维是平面，高维是超平面。这是"线性"分类器名字的由来——决策边界只能是线性的。

**(b)** 具体计算：
- $s_1 = 1 \cdot x_1 + 0 \cdot x_2 + 0 = x_1$
- $s_2 = 0 \cdot x_1 + 1 \cdot x_2 - 1 = x_2 - 1$
- 决策边界：$x_1 = x_2 - 1$，即 $x_1 - x_2 + 1 = 0$（一条直线）

分类结果：
- $(2, 0)$：$s_1=2$，$s_2=-1$ → 类别1
- $(0, 2)$：$s_1=0$，$s_2=1$ → 类别2
- $(2, 2)$：$s_1=2$，$s_2=1$ → 类别1

**(c)** 线性可分性判断：
- **A**：○在左下，×在右上 → 直线 $x_1 + x_2 = 1$ 可以分开 → **线性可分**。
- **B**（XOR）：对角线上同类的两个点被异类的两个点夹在中间 → 不存在一条直线能分开 → **线性不可分**。这是历史上导致感知机"第一次AI寒冬"的经典反例。
- **C**：两类分别在 $x_1=0$ 和 $x_1=2$ 两条竖直线上 → 直线 $x_1=1$ 可分开 → **线性可分**。

**(d)** 引入乘积特征后的可分性：

在原空间 $\mathbb{R}^2$ 中XOR不可分。变换到 $\phi(\mathbf{x}) = [x_1, x_2, x_1 x_2]^\top$ 后：
- $\phi(0,0) = [0, 0, 0]$，$\phi(1,1) = [1, 1, 1]$（类别○）
- $\phi(0,1) = [0, 1, 0]$，$\phi(1,0) = [1, 0, 0]$（类别×）

在三维空间中，可以用平面 $2(x_1 + x_2) - 4x_1 x_2 - 1 = 0$ 将两类分开。**关键启示**：线性不可分的数据可以通过**非线性特征变换**变为可分——这是核方法（kernel methods）和深度学习中隐藏层的基本思想。但手动设计好的 $\phi(\cdot)$ 很难，神经网络通过数据来学习 $\phi(\cdot)$。

</details>

---

### 习题 4 · One-Hot编码与交叉熵的信息论视角

> 📘 **考查**：One-hot编码的数学本质与交叉熵的信息论含义 | 🏷️ **对应卡**：[[Softmax与SVM损失函数]]
> 📖 **D2L参考**：Ch.4.1 Softmax Regression

**题目**：在分类问题中，真实标签 $y \in \{1, 2, \dots, C\}$ 通常被编码为**one-hot向量** $\mathbf{y} = [y_1, y_2, \dots, y_C]^\top$，其中 $y_{y}=1$，其余为0。

**(a)** 写出one-hot编码的数学定义：$y_j = \mathbb{1}[j = y]$。这是一个合法的概率分布吗？为什么？

**(b)** 在Softmax回归中，损失函数是交叉熵 $L = -\sum_{j=1}^{C} y_j \ln p_j$。如果将标签改为**标签平滑**（Label Smoothing）：$\tilde{y}_j = (1-\epsilon) y_j + \frac{\epsilon}{C}$（其中 $\epsilon \in (0, 1)$ 是一个小值，如0.1），交叉熵损失变为 $L_{\text{LS}} = -\sum_{j=1}^{C} \tilde{y}_j \ln p_j$。

计算当 $\epsilon = 0.1$，$C=3$，$y=1$，$\mathbf{p} = [0.7, 0.2, 0.1]$ 时：
- 原始交叉熵 $L$
- 标签平滑后的交叉熵 $L_{\text{LS}}$
两者差多少？为什么标签平滑能缓解过拟合？

**(c)** 交叉熵 $H(\mathbf{y}, \mathbf{p})$、熵 $H(\mathbf{y})$、KL散度 $D_{KL}(\mathbf{y} \| \mathbf{p})$ 三者之间的关系是什么？证明最小化交叉熵等价于最小化KL散度（当真实分布固定时）。

**(d)** 当模型完全错误时（$p_y \to 0^+$），$L = -\ln p_y \to +\infty$；当模型完全正确时（$p_y \to 1^-$），$L \to 0^+$。Softmax+CE下是否可能达到**绝对零损失**？为什么？

---

<details>
<summary><b>📝 参考答案要点</b></summary>

**(a)** One-hot是合法概率分布：
- $y_j = \mathbb{1}[j = y]$
- 非负性：$\forall j, y_j \in \{0, 1\} \ge 0$ ✓
- 归一性：$\sum_{j=1}^{C} y_j = 1$（只有一个位置是1）✓
- 它是一个**退化的**（degenerate）概率分布——确定性分布，所有概率质量集中在正确类上。

这个"退化"性质就是Softmax+CE"永不满足"的根源：模型被要求去逼近一个它永远无法完美匹配的分布（除非 $p_y = 1.0$，这要求 $s_y = +\infty$）。

**(b)** 数值计算：

原始 $L = -\ln 0.7 = 0.357$

标签平滑后的 $\tilde{\mathbf{y}}$：
- $\tilde{y}_1 = (1-0.1) \times 1 + 0.1/3 = 0.9 + 0.033 = 0.933$
- $\tilde{y}_2 = 0 + 0.033 = 0.033$
- $\tilde{y}_3 = 0 + 0.033 = 0.033$

$L_{\text{LS}} = -(0.933 \ln 0.7 + 0.033 \ln 0.2 + 0.033 \ln 0.1)$
$= -(0.933 \times (-0.357) + 0.033 \times (-1.609) + 0.033 \times (-2.303))$
$= -(-0.333 - 0.053 - 0.076) = 0.462$

差值 $L_{\text{LS}} - L = 0.462 - 0.357 = 0.105$。

**缓解过拟合的原因**：
- 原始one-hot要求模型对正确类输出1.0（概率质量全部集中），这鼓励模型极端自信，容易过度拟合噪声。
- 标签平滑说："正确答案大概率是1，但也有$\epsilon$的可能是其他类"——这让模型不再追求$p_y \to 1$的极端，从而学到更平滑、更泛化的决策边界。
- 另外，标签平滑约束了正确类的logit不会无限增长，起到隐性正则化作用。

**(c)** 三者关系：

$$H(\mathbf{y}, \mathbf{p}) = H(\mathbf{y}) + D_{KL}(\mathbf{y} \| \mathbf{p})$$

其中 $H(\mathbf{y}) = -\sum_j y_j \ln y_j$（真实分布的熵），$D_{KL}(\mathbf{y} \| \mathbf{p}) = \sum_j y_j \ln \frac{y_j}{p_j}$。

**等价性证明**：对于固定的 $\mathbf{y}$，$H(\mathbf{y})$ 是常数。因此：
$$\arg\min_{\mathbf{p}} H(\mathbf{y}, \mathbf{p}) = \arg\min_{\mathbf{p}} [H(\mathbf{y}) + D_{KL}(\mathbf{y} \| \mathbf{p})] = \arg\min_{\mathbf{p}} D_{KL}(\mathbf{y} \| \mathbf{p})$$

所以**最小化交叉熵 = 最小化KL散度**，即让预测分布 $\mathbf{p}$ 尽可能接近真实分布 $\mathbf{y}$。

**(d)** 绝对零损失不可达：

$L = 0 \iff p_y = 1 \iff \frac{e^{s_y}}{\sum_k e^{s_k}} = 1 \iff \forall k \neq y, \frac{e^{s_k}}{e^{s_y}} = 0$

这要求 $\forall k \neq y, s_k \to -\infty$，且 $s_y$ 有限——在有限精度的实际训练中不可能，理论上也需要无限步优化。因此 **Softmax+CE 的零损失是不可达的理想极限**，模型永远有训练信号——这就是它比SVM Hinge Loss更常用的原因之一。

</details>

---

### 习题 5 · Log-Sum-Exp与数值稳定性：为什么Softmax会溢出

> 📘 **考查**：指数溢出的数值分析、log-sum-exp trick实现 | 🏷️ **对应卡**：[[Softmax与SVM损失函数]] [[梯度计算]]
> 📖 **D2L参考**：Ch.4.4 Softmax Regression Implementation from Scratch

**题目**：在实际计算Softmax+交叉熵时，直接计算 $e^{s_j}$ 极易溢出。float32的最大可表示值约为 $3.4 \times 10^{38}$，当 $s_j > 89$ 时 $e^{s_j}$ 就可能超过此范围。

**(a)** 为什么只减去最大值不够？已知标准技巧是 $\text{softmax}(\mathbf{s})_j = \frac{e^{s_j - s_{\max}}}{\sum_k e^{s_k - s_{\max}}}$，其中 $s_{\max} = \max_k s_k$。这个变换保证 $s_j - s_{\max} \le 0$，因此 $e^{s_j - s_{\max}} \in (0, 1]$，不再溢出。但交叉熵损失还需要取 $\ln$——如果我们用上面的稳定Softmax先算 $\mathbf{p}$，再算 $-\ln p_y$，会发生什么问题？

**(b)** 写出**一次性**计算Softmax交叉熵损失的数值稳定公式（不显式计算 $\mathbf{p}$），即直接计算：

$$L = -s_y + s_{\max} + \ln\sum_{k=1}^{C} e^{s_k - s_{\max}}$$

推导这个公式（从 $L = -\ln(e^{s_y}/\sum_k e^{s_k})$ 出发），并说明为什么它比"先softmax后log"更稳定。

**(c)** 实现一个函数 `softmax_cross_entropy_stable(scores, labels)`，接受得分矩阵 $\mathbf{S} \in \mathbb{R}^{N \times C}$（$N$ 个样本）和标签向量 $\mathbf{y} \in \mathbb{R}^{N}$（整数索引，非one-hot），返回逐样本损失向量。要求：
- 使用log-sum-exp技巧
- 向量化（无Python显式循环遍历样本）
- 返回 $(L_1, L_2, \dots, L_N)$

用NumPy或PyTorch写出伪代码。

**(d)** 如果得分中有一个值是 `NaN`（例如因为某次参数更新导致的），损失函数会发生什么？如何在代码中检测并优雅处理这种情况？

---

<details>
<summary><b>📝 参考答案要点</b></summary>

**(a)** "先Softmax后Log"的风险：

```python
# ❌ 不稳定的两步法
p = stable_softmax(s)   # p 的元素在 (0,1]，看似安全
L = -np.log(p[y])       # 但当 p[y] 接近 0 时 log(1e-38) = -87 还好
                        # 真正的问题是：如果所有 s_j 都很小，
                        # p[y] 可能已是 denormalized float，
                        # log 会给出 -inf
```

更关键的是，**两步法浪费计算**：先算完整 $\mathbf{p}$（$C$ 个值），再从里面取一个；一步法直接算 $-\ln p_y$，避免了中间的全概率向量。

**(b)** 公式推导：

$$L = -\ln\frac{e^{s_y}}{\sum_k e^{s_k}} = -\left(s_y - \ln\sum_k e^{s_k}\right) = -s_y + \ln\sum_k e^{s_k}$$

引入 $s_{\max}$：
$$\ln\sum_k e^{s_k} = \ln\left(e^{s_{\max}} \sum_k e^{s_k - s_{\max}}\right) = s_{\max} + \ln\sum_k e^{s_k - s_{\max}}$$

代入得：
$$L = -s_y + s_{\max} + \ln\sum_k e^{s_k - s_{\max}}$$

**更稳定的原因**：
- $e^{s_k - s_{\max}} \in (0, 1]$，$\sum_k$ 范围在 $[1, C]$，再取 $\ln$ 范围在 $[0, \ln C]$——全程在 float32 安全区内。
- $s_{\max} - s_y$ 也是有限值（不失一般性的减法）。
- 整个过程没有极小数取log的风险。

**(c)** 向量化实现：

```python
import numpy as np

def softmax_cross_entropy_stable(S, y):
    """
    S: (N, C) 得分矩阵
    y: (N,)   整数标签
    返回: (N,) 逐样本损失
    """
    N = S.shape[0]
    # 1. 每行减去最大值（log-sum-exp trick）
    s_max = S.max(axis=1, keepdims=True)          # (N, 1)
    S_shifted = S - s_max                          # (N, C)

    # 2. 计算 log-sum-exp
    log_sum_exp = np.log(np.sum(np.exp(S_shifted), axis=1))  # (N,)

    # 3. 损失 = -s_y + s_max + log-sum-exp
    s_correct = S[np.arange(N), y]                 # (N,) 正确类得分
    loss = -s_correct + s_max.squeeze() + log_sum_exp

    return loss
```

```python
# PyTorch 等价版
import torch
import torch.nn.functional as F

def softmax_ce_stable_torch(S, y):
    # PyTorch 的 cross_entropy 内部已使用 log-sum-exp
    return F.cross_entropy(S, y, reduction='none')
```

> 🔧 工程要点：PyTorch的 `F.cross_entropy` 在内部已做了log-sum-exp + NLL的稳定计算，**无需在模型输出层加Softmax**。

**(d)** NaN检测与处理：

```python
def safe_cross_entropy(S, y):
    if np.isnan(S).any() or np.isinf(S).any():
        # 诊断信息
        nan_count = np.isnan(S).sum()
        inf_count = np.isinf(S).sum()
        print(f"⚠️ 检测到异常值：{nan_count} 个 NaN, {inf_count} 个 Inf")
        # 梯度裁剪/权重衰减失效/学习率过大 是常见原因
        # 当前batch可返回大loss + 跳过参数更新
        return np.full(len(y), 1e3)  # 大loss标记异常
    return softmax_cross_entropy_stable(S, y)
```

**排查路线**：NaN的常见来源包括：(1) 学习率过大导致参数爆炸，(2) 未使用log-sum-exp导致Softmax溢出，(3) 数据本身含NaN，(4) 除零操作。应逐层加 `assert not np.isnan(x).any()` 定位问题源头。

</details>

---

### 习题 6 · Softmax回归从零实现：模块设计与训练循环

> 📘 **考查**：Softmax回归的完整实现思路 | 🏷️ **对应卡**：[[Softmax与SVM损失函数]] [[前向传播]] [[梯度下降CV]]
> 📖 **D2L参考**：Ch.4.4 Softmax Regression Implementation from Scratch

**题目**：设计一个从零实现的Softmax回归训练框架（仅用NumPy），不使用自动求导。

**(a)** 写出Softmax回归模型需要实现的**核心模块清单**（数据加载、模型定义、损失函数、优化器），说明每个模块的输入输出和关键设计决策。

**(b)** 以**模型模块**为例，写出参数初始化（$\mathbf{W} \in \mathbb{R}^{D \times C}$，$\mathbf{b} \in \mathbb{R}^{C}$）、前向传播（得分+Softmax）的NumPy伪代码。初始化的标准差应该是多少？为什么？

**(c)** 训练循环的伪代码应包括哪些关键步骤？写清楚每个batch内的操作序列：数据加载 → 前向 → 损失 → 梯度 → 更新 → 评估。标注每个步骤涉及的**矩阵维度变化**。

**(d)** 在一次完整训练后，你会如何在测试集上评估模型性能？写出计算准确率（accuracy）和top-k准确率的伪代码，并说明在Fashion-MNIST（10类均衡）上随机猜测的准确率基线是多少。

---

<details>
<summary><b>📝 参考答案要点</b></summary>

**(a)** 核心模块清单：

| 模块 | 输入 | 输出 | 关键设计决策 |
|:---|:---|:---|:---|
| **数据加载** `DataLoader` | 原始数据 $(N, D)$，标签 $(N,)$ | Mini-batch $(B, D)$，$(B,)$ | batch_size=256；shuffle=True（每个epoch前打乱）；归一化到[0,1] |
| **模型** `SoftmaxRegression` | $(B, D)$ 输入 | $(B, C)$ 概率 | $W \in \mathbb{R}^{D \times C}$（注意维度！）；偏置初始化为0；权重用$\mathcal{N}(0, 0.01)$ |
| **损失函数** `CrossEntropyLoss` | $(B, C)$ 概率 + $(B,)$ 标签 | 标量loss | 使用log-sum-exp稳定计算；平均（除以B）而非求和 |
| **优化器** `SGD` | 参数 + 梯度 | 更新后的参数 | lr=0.1；可选momentum；可选weight_decay（L2正则化） |

**(b)** 参数初始化与前向传播：

```python
import numpy as np

class SoftmaxRegression:
    def __init__(self, input_dim, num_classes, std=0.01):
        # 小随机数初始化：避免对称性，保持初始loss接近ln(C)
        self.W = np.random.randn(input_dim, num_classes) * std
        self.b = np.zeros((1, num_classes))  # 偏置初始化为0是安全的

    def forward(self, X):
        """
        X: (B, D) 输入batch
        返回: probs (B, C) Softmax概率
        """
        scores = X @ self.W + self.b           # (B, D) @ (D, C) = (B, C)
        # log-sum-exp 稳定Softmax
        scores_shifted = scores - scores.max(axis=1, keepdims=True)
        exp_scores = np.exp(scores_shifted)
        probs = exp_scores / exp_scores.sum(axis=1, keepdims=True)
        return probs
```

**标准差为何是0.01**：对于Softmax回归（线性模型+凸损失），初始权重不需要严格满足Xavier/He条件（因为没有多层堆叠导致梯度消失/爆炸的问题）。常用 $\mathcal{N}(0, 0.01)$ 使初始得分接近0——此时Softmax输出接近均匀分布 $p_j \approx 1/C$，初始交叉熵损失约为 $\ln C$（$C=10$ 时约为2.3）。这是合理的"无知"起点。

**(c)** 训练循环（含维度标注）：

```python
def train_epoch(model, dataloader, lr=0.1, reg=0.0):
    total_loss, total_correct, total_samples = 0.0, 0, 0

    for X_batch, y_batch in dataloader:
        # X_batch: (B, D)  y_batch: (B,)
        B = X_batch.shape[0]

        # ─── 1. 前向传播 ───
        probs = model.forward(X_batch)          # (B, C)

        # ─── 2. 损失计算（log-sum-exp稳定）───
        # 注意：实际中先算scores再用stable CE loss
        # 这里简化展示梯度计算
        loss = -np.log(probs[np.arange(B), y_batch] + 1e-8).mean()
        if reg > 0:
            loss += reg * np.sum(model.W ** 2)
        total_loss += loss * B

        # ─── 3. 反向传播（手动计算梯度）───
        dS = probs.copy()                        # (B, C)
        dS[np.arange(B), y_batch] -= 1           # ∂L/∂S = p_j - 𝟙[j=y]
        dS /= B                                  # 平均化

        dW = X_batch.T @ dS                      # (D, B) @ (B, C) = (D, C)
        db = dS.sum(axis=0, keepdims=True)       # (1, C)

        if reg > 0:
            dW += 2 * reg * model.W              # L2正则化梯度

        # ─── 4. 参数更新 ───
        model.W -= lr * dW                       # (D, C)
        model.b -= lr * db                       # (1, C)

        # ─── 5. 准确率统计 ───
        preds = probs.argmax(axis=1)             # (B,)
        total_correct += (preds == y_batch).sum()
        total_samples += B

    return total_loss / total_samples, total_correct / total_samples
```

> 🔑 维度变化链：$(B,D) \xrightarrow{\times W} (B,C) \xrightarrow{\text{softmax}} (B,C) \xrightarrow{\text{loss}} ()$ 标量。

**(d)** 评估与基线：

```python
def evaluate(model, X_test, y_test, batch_size=256):
    total_correct, total_correct_top5, total = 0, 0, 0
    for i in range(0, len(X_test), batch_size):
        X_batch = X_test[i:i+batch_size]
        y_batch = y_test[i:i+batch_size]
        probs = model.forward(X_batch)           # (B, C)
        preds = probs.argmax(axis=1)
        total_correct += (preds == y_batch).sum()
        # top-5: 取每行最大的5个索引
        top5 = np.argsort(-probs, axis=1)[:, :5]
        total_correct_top5 += np.any(top5 == y_batch[:, None], axis=1).sum()
        total += len(y_batch)
    return total_correct / total, total_correct_top5 / total
```

**基线**：Fashion-MNIST有10个均衡类别，随机猜测的准确率基线是 **10%**。Softmax回归通常能达到约 **85-87%** 的测试准确率（取决于训练epoch数），这比随机猜测好得多但仍远低于CNN（~93%+），体现了线性模型的表达力局限。

</details>

---

### 习题 7 · Fashion-MNIST分类实验：从数据到模型评估

> 📘 **考查**：完整分类实验设计、超参数调优、结果分析 | 🏷️ **对应卡**：[[图像分类任务与数据管线]] [[kNN与线性分类器]]
> 📖 **D2L参考**：Ch.4.2 The Image Classification Dataset, Ch.4.5 Concise Implementation

**题目**：你需要在Fashion-MNIST（$28 \times 28$ 灰度图，10类衣物）上完成Softmax回归实验。数据集包含60,000训练样本和10,000测试样本。

**(a)** **数据预处理**：写出数据管线的完整流程。原始像素值范围是 $[0, 255]$（uint8），如何处理？是否需要归一化？为什么？应该划分验证集吗？如需要，怎么划？

**(b)** **超参数搜索**：设计一个简单的网格搜索（grid search）方案，对学习率 `lr` ∈ {0.01, 0.05, 0.1, 0.5} 和 batch_size ∈ {32, 128, 256} 进行搜索。写出实验配置的关键要素：每个组合训练多少epoch？用什么指标选择最优超参数？如何避免数据泄露？

**(c)** **结果分析**：假设你的Softmax回归模型在训练集上准确率为88%，测试集上为85%。
- 这是什么现象？是否有问题？
- 如果再训练更多epoch，训练准确率升到95%但测试准确率降到83%，这是为什么？该怎么办？
- 画出**混淆矩阵**（confusion matrix）后，发现模型最常把"Shirt"（衬衫, class 6）误分为"T-shirt/top"（T恤, class 0），这说明了什么？如何改进？

**(d)** **与kNN对比**：如果改用kNN分类器（$k=5$，L2距离）在同样的Fashion-MNIST上测试，预期结果（训练/测试的准确率和速度）会有什么不同？解释原因。

---

<details>
<summary><b>📝 参考答案要点</b></summary>

**(a)** 数据预处理流程：

```python
# 1. 读取原始数据（uint8, [0, 255]）
X_train_raw, y_train = ...  # (60000, 784)
X_test_raw, y_test = ...    # (10000, 784)

# 2. 类型转换 + 归一化
X_train = X_train_raw.astype(np.float32) / 255.0  # → [0, 1]
X_test = X_test_raw.astype(np.float32) / 255.0

# 3. (可选) 验证集划分：从训练集中划出最后5000或随机10%
# 方法A：固定划分（可复现）
X_val, y_val = X_train[-5000:], y_train[-5000:]
X_train, y_train = X_train[:-5000], y_train[:-5000]

# 方法B：随机划分
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, test_size=0.1, random_state=42
)
```

**为什么要归一化？** (1) 数值稳定性：原始像素值255会让初始得分 $s = Wx + b$ 的范围过大，导致Softmax溢出或梯度异常。(2) 优化效率：不同特征量纲统一后，SGD在所有方向上步长一致，收敛更快。(3) Softmax回归中，若不归一化，初始loss会非常大。

**需要验证集吗？** 强烈建议。没有验证集就无法客观地选择超参数（如学习率、正则化系数），在测试集上调参会造成数据泄露。标准做法：训练集→训练+验证，测试集仅用于最终报告。

**(b)** 网格搜索方案：

```python
learning_rates = [0.01, 0.05, 0.1, 0.5]
batch_sizes = [32, 128, 256]
num_epochs = 50  # 固定，或 early stopping

best_val_acc = 0
best_config = None

for lr in learning_rates:
    for bs in batch_sizes:
        # 初始化模型（固定随机种子保证可比性）
        model = SoftmaxRegression(input_dim=784, num_classes=10)

        for epoch in range(num_epochs):
            # 训练一个epoch...
            train_loss, train_acc = train_epoch(model, train_loader, lr=lr)
            val_acc = evaluate(model, X_val, y_val)

        # 用验证集最优准确率选择超参数
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_config = (lr, bs)

# 最后在测试集上报告 best_config 的结果（仅一次！）
```

**关键要素**：
- **指标**：用**验证集准确率**（而非训练集）选择最优配置。
- **避免数据泄露**：测试集在超参数搜索阶段**完全不接触**，只在最终选好超参数后，用测试集评估一次并报告。
- **固定随机种子**：确保不同超参数组合的可比性。
- **可选改进**：加early stopping（验证loss连续N个epoch不降则停）。

**(c)** 结果分析：

**训练88% vs 测试85%**：差距3个百分点属于**期望范围**——模型在训练数据上略优于未见数据是完全正常的。这不代表严重过拟合。

**训练95% vs 测试83%**：差距12个百分点 → **明确过拟合**。模型开始记忆训练集的噪声和特例，泛化能力下降。

**应对措施**：
1. **L2正则化**（weight decay）：给损失加上 $\lambda \|W\|_2^2$，约束权重不要过大
2. **早停（early stopping）**：在验证准确率不再上升时停止训练
3. **数据增强**：对Fashion-MNIST可做随机水平翻转（注意：左右鞋不能翻转！）、小幅度平移、旋转
4. **减小模型容量**或**增大训练集**（这里容量已是最小，主要靠正则化）

**混淆矩阵分析**："Shirt" ↔ "T-shirt/top" 高混淆率说明两者在像素空间中确实高度相似——它们都是上半身穿着的衣物，在28×28低分辨率下轮廓极为接近。这是**语义相似导致的数据固有模糊性**，而非模型缺陷。改进方向：(1) 收集更多标注样本，(2) 使用CNN提取局部纹理/领口等判别性特征，(3) 类别合并或层级分类。

**(d)** kNN对比（预期）：

| 维度 | Softmax回归 | kNN (k=5, L2) |
|:---|:---|:---|
| **训练时间** | 需若干epoch的迭代优化 | **几乎为零**（惰性学习，只存数据） |
| **测试时间** | **极快**（一次矩阵乘法 $784 \times 10$） | 极慢（每个测试样本需与60,000训练样本算距离） |
| **测试准确率（预期）** | ~85-87% | ~85%（kNN在像素空间的L2距离效果类似，但维数灾难影响有限于784维） |
| **存储开销** | **极小**（$784 \times 10$ 参数 ≈ 31KB） | 极大（存全部60,000×784 ≈ 188MB） |
| **决策边界** | 线性超平面（全局光滑） | 任意复杂（紧贴数据，局部投票） |

本质差异：Softmax回归把知识"压缩"进参数，kNN把知识"存储"在数据中。前者适合部署，后者适合理论理解和小规模原型。

</details>

---

### 习题 8 · 线性分类与非线性分类：边界、局限与突破

> 📘 **考查**：线性可分的概念边界，从线性到非线性的过渡 | 🏷️ **对应卡**：[[kNN与线性分类器]] [[激活函数CV]]
> 📖 **D2L参考**：Ch.4.1 Softmax Regression, Ch.4.6 Generalization in Classification

**题目**：线性分类器（包括Softmax回归）的决策边界只能是超平面，这从根本上限制了它的表达能力。

**(a)** 经典反例：**XOR问题**。四个二维点：$A(0,0), B(0,1), C(1,0), D(1,1)$。假设 $A$ 和 $D$ 属于类别○，$B$ 和 $C$ 属于类别×。严格证明：**不存在**任何线性分类器（任意 $\mathbf{w}, b$）能将这四个点正确分类。提示：假设存在这样的分类器，导出矛盾。

**(b)** 如果允许你在Softmax回归之前先加一个**隐藏层** $\mathbf{h} = \text{ReLU}(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)})$（即变成两层网络），直观解释为什么XOR变得可以分了。你能构造一组具体的 $\mathbf{W}^{(1)}$ 和 $\mathbf{b}^{(1)}$（用2个隐藏神经元），将XOR的四个点映射到隐藏空间中的新坐标，使得在隐藏空间中它们变得线性可分吗？

**(c)** 在D2L第4章的Fashion-MNIST实验中，Softmax回归的测试准确率天花板大约是85-87%。是什么图像特征导致剩下的13-15%无法被线性模型正确分类？列举至少三种具体的失败模式（failure modes），并解释为什么需要深度非线性模型来解决。

**(d)** **哲学题**：有人说"Softmax回归的线性本质不是bug，而是feature——它迫使可解释性和效率"。你同意吗？写一段50-100字的评述，从**可解释性、效率、表达能力**三个维度给出你的观点。

---

<details>
<summary><b>📝 参考答案要点</b></summary>

**(a)** XOR线性不可分的严格证明（反证法）：

假设存在 $\mathbf{w} = (w_1, w_2)$ 和 $b$，使得分类器 $\text{sign}(w_1 x_1 + w_2 x_2 + b)$ 正确分类所有四个点。

设分类规则为 $w_1 x_1 + w_2 x_2 + b > 0$ 预测类别○（若 $<0$ 同理，反号即可）。

- $A(0,0)$ 是○ → $b > 0$  … (1)
- $D(1,1)$ 是○ → $w_1 + w_2 + b > 0$  … (2)
- $B(0,1)$ 是× → $w_2 + b \le 0$  … (3)
- $C(1,0)$ 是× → $w_1 + b \le 0$  … (4)

由(3): $w_2 + b \le 0 \Rightarrow w_2 \le -b$
由(4): $w_1 + b \le 0 \Rightarrow w_1 \le -b$

相加：$w_1 + w_2 \le -2b$  … (5)

由(2): $w_1 + w_2 > -b$  … (6)

联立(5)(6)：$-b < w_1 + w_2 \le -2b \Rightarrow -b < -2b \Rightarrow b < 0$

但(1)断言 $b > 0$。**矛盾！** 因此不存在这样的线性分类器。∎

**(b)** 隐藏层解决XOR：

使用2个隐藏神经元，$\text{ReLU}$ 激活：

$$\mathbf{W}^{(1)} = \begin{bmatrix} 1 & 1 \\ -1 & -1 \end{bmatrix},\quad \mathbf{b}^{(1)} = \begin{bmatrix} -0.5 \\ 1.5 \end{bmatrix}$$

- $A(0,0)$：$\mathbf{h} = [\text{ReLU}(-0.5), \text{ReLU}(1.5)] = [0, 1.5]$
- $B(0,1)$：$\mathbf{h} = [\text{ReLU}(0.5), \text{ReLU}(0.5)] = [0.5, 0.5]$
- $C(1,0)$：$\mathbf{h} = [\text{ReLU}(0.5), \text{ReLU}(0.5)] = [0.5, 0.5]$
- $D(1,1)$：$\mathbf{h} = [\text{ReLU}(1.5), \text{ReLU}(-0.5)] = [1.5, 0]$

在隐藏空间中：○类 $A$ 和 $D$ 分别位于 $[0, 1.5]$ 和 $[1.5, 0]$，×类 $B$ 和 $C$ 都位于 $[0.5, 0.5]$。可以用 $h_1 + h_2 > 1.0$ 的决策线分开——**线性可分了！**

> 💡 本质：隐藏层将原始空间中线性不可分的点，通过非线性变换"弯折"到新的特征空间，使它们变得线性可分。这就是深度学习"逐层提取特征"的最简原型。

**(c)** Fashion-MNIST上线性模型的失败模式：

1. **类内形变（intra-class variation）**：同一类"连衣裙"可能有长袖、无袖、A字摆、紧身等完全不同的像素轮廓。线性模型只能学一个"平均模板"，无法处理多模态分布。

2. **姿态和视角变化**：同一件"外套"的正面照和侧面照在像素空间中可以相差很大，但仍然是同一类。线性模型对所有像素一视同仁，缺乏平移/旋转不变性。

3. **局部细节 vs 全局轮廓混淆**："衬衫"和"T恤"的区别在于领口形状（一个局部特征），但像素级全局模板会将大部分像素分配给无关区域（背景、下摆），判别性细节被平均淹没。

**为什么深度非线性模型有效**：CNN的卷积层可以检测**局部特征**（边缘→纹理→领口形状→衣领→整件衣服），池化层提供平移不变性，ReLU非线性使得特征可以按"是否存在某模式"而非"某模式的像素值是多少"来响应。多层堆叠逐步将像素空间"展开"为语义可分空间。

**(d)** 评述参考：

> "我部分同意。线性模型的优势在于其决策边界的透明性——$\mathbf{W}$ 矩阵可直接可视化为模板、单个权重可解释为特征重要性，这在医疗和法律等需要可解释性的领域至关重要；同时推理极快（一次矩阵乘法），适合边缘部署。然而，当面对自然图像的语义复杂度时，'可解释'的代价是'表达力严重不足'——为了那13%的准确率差距，接受非线性带来的'黑箱'是必要的权衡。好的工程实践是用线性模型做baseline和特征重要性分析，用深度模型追求性能。"

</details>

---

## 🔗 习题→知识卡映射速查

| 习题 | 对应知识卡 |
|:---|:---|
| 习题1：Softmax公式推导 | [[Softmax与SVM损失函数]] [[线性代数基础CV]] |
| 习题2：交叉熵梯度推导 | [[Softmax与SVM损失函数]] [[梯度计算]] |
| 习题3：决策边界推导 | [[kNN与线性分类器]] [[线性代数基础CV]] |
| 习题4：One-Hot与信息论 | [[Softmax与SVM损失函数]] |
| 习题5：Log-Sum-Exp稳定性 | [[Softmax与SVM损失函数]] [[梯度计算]] |
| 习题6：从零实现思路 | [[Softmax与SVM损失函数]] [[前向传播]] [[梯度下降CV]] |
| 习题7：Fashion-MNIST实验 | [[图像分类任务与数据管线]] [[kNN与线性分类器]] |
| 习题8：线性 vs 非线性 | [[kNN与线性分类器]] [[激活函数CV]] |

---

## 📐 使用建议

1. **最小完成路径**：习题 1 → 2 → 3 → 8 覆盖线性分类核心理解（Softmax、交叉熵梯度、决策边界、线性局限）
2. **强化数学推导**：习题 2 + 5 是面经高频题——Softmax梯度推导和log-sum-exp技巧
3. **工程实战辅助**：习题 6 建议配合 [[../18-实战作业说明书/🎓 HW01 - CIFAR-10 kNN 与 Softmax 基线正式作业说明书\|HW01]] 一起完成，习题 7 对应D2L Ch.4.2的实际coding部分
4. **查漏补缺**：习题 4（信息论视角）+ 习题 8（哲学思考）用于检验对分类问题的整体理解深度

---

*基于 D2L Ch.4（CC BY-SA 4.0）编写 | 最后更新 2026-08-05*
