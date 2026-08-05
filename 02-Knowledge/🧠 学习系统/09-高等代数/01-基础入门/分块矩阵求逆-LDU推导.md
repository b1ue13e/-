---
type: study
topic: "推导"
course: "高等代数"
stage: "📐 第一阶段：基础入门"
module: "模块2：矩阵运算与逆矩阵"
created: 2026-04-23
status: ongoing
difficulty: beginner
concept: ["推导"]
prerequisites: ["矩阵分块", "逆矩阵"]
related: ["矩阵分块", "逆矩阵", "矩阵乘法"]
source_textbook: ["高等代数（第5版）", "矩阵力量"]
tags: ["高等代数", "学习"]
---
要把这个复杂的公式“拆解”清楚，我们不能光盯着结果看。 要把这个推导过程看作是一场 **“高维空间的消元游戏”**。

普通的消元法是把数字变成 0，而分块矩阵的推导则是利用**分块消元**，通过构造特殊的三角矩阵，把 $M$ 变成一个容易求逆的对角阵。

---

## 1. 核心思想：分块 LDU 分解

求逆的最快路径是先把矩阵 $M$ 拆成三个简单的矩阵相乘：一个**下三角**、一个**对角**、一个**上三角**。

### 第一步：消除左下角的 $C$

我们想构造一个矩阵，左乘 $M$ 后能让 $C$ 变成 $0$。 利用分块消元，我们给第二行加上第一行的 $-CA^{-1}$ 倍 ：

$$\begin{pmatrix} I & 0 \\ -CA^{-1} & I \end{pmatrix} \begin{pmatrix} A & B \\ C & D \end{pmatrix} = \begin{pmatrix} A & B \\ 0 & D - CA^{-1}B \end{pmatrix}$$

注意，这里出现了**舒尔补 $S = D - CA^{-1}B$**。

### 第二步：消除右上角的 $B$

同理，我们想让右上角也变成 $0$。 我们在右边乘以一个上三角矩阵：

$$\begin{pmatrix} A & B \\ 0 & S \end{pmatrix} \begin{pmatrix} I & -A^{-1}B \\ 0 & I \end{pmatrix} = \begin{pmatrix} A & 0 \\ 0 & S \end{pmatrix}$$

### 整合：LDU 分解公式

把上面两步反过来写，我们就得到了矩阵 $M$ 的完美分解：

$$M = \underbrace{\begin{pmatrix} I & 0 \\ CA^{-1} & I \end{pmatrix}}_{L} \underbrace{\begin{pmatrix} A & 0 \\ 0 & S \end{pmatrix}}_{D_{block}} \underbrace{\begin{pmatrix} I & A^{-1}B \\ 0 & I \end{pmatrix}}_{U}$$

> **金句：分解的本质是剥离关联。$L$ 和 $U$ 负责描述块与块之间的“纠缠”，而 $D$ 则是它们各自独立的灵魂。**

---

## 2. 暴力求逆：反转顺序

根据矩阵求逆的性质 $(XYZ)^{-1} = Z^{-1}Y^{-1}X^{-1}$，我们只需要分别求出这三个简单矩阵的逆，再按相反顺序乘起来：

1. **单位三角阵求逆：** 只需要把消元系数变号。
    
    $$L^{-1} = \begin{pmatrix} I & 0 \\ -CA^{-1} & I \end{pmatrix}, \quad U^{-1} = \begin{pmatrix} I & -A^{-1}B \\ 0 & I \end{pmatrix}$$
    
2. **对角阵求逆：** 直接对子块求逆。
    
    $$D_{block}^{-1} = \begin{pmatrix} A^{-1} & 0 \\ 0 & S^{-1} \end{pmatrix}$$
    

所以：

$$M^{-1} = U^{-1} D_{block}^{-1} L^{-1} = \begin{pmatrix} I & -A^{-1}B \\ 0 & I \end{pmatrix} \begin{pmatrix} A^{-1} & 0 \\ 0 & S^{-1} \end{pmatrix} \begin{pmatrix} I & 0 \\ -CA^{-1} & I \end{pmatrix}$$

---

## 3. 最后的合体：矩阵乘法三步走

现在我们开始手动把这三个矩阵乘回去。

**第一步：先乘后面两个**

$$\begin{pmatrix} A^{-1} & 0 \\ 0 & S^{-1} \end{pmatrix} \begin{pmatrix} I & 0 \\ -CA^{-1} & I \end{pmatrix} = \begin{pmatrix} A^{-1} & 0 \\ -S^{-1}CA^{-1} & S^{-1} \end{pmatrix}$$

**第二步：乘上前面的 $U^{-1}$**

$$\begin{pmatrix} I & -A^{-1}B \\ 0 & I \end{pmatrix} \begin{pmatrix} A^{-1} & 0 \\ -S^{-1}CA^{-1} & S^{-1} \end{pmatrix}$$

计算各分块：

- **左上角：** $I \cdot A^{-1} + (-A^{-1}B) \cdot (-S^{-1}CA^{-1}) = A^{-1} + A^{-1}BS^{-1}CA^{-1}$
    
- **右上角：** $I \cdot 0 + (-A^{-1}B) \cdot S^{-1} = -A^{-1}BS^{-1}$
    
- **左下角：** $0 \cdot A^{-1} + I \cdot (-S^{-1}CA^{-1}) = -S^{-1}CA^{-1}$
    
- **右下角：** $0 \cdot 0 + I \cdot S^{-1} = S^{-1}$
    

**大功告成！** 这就是你在图中看到的那个令人望而生畏的公式。

---

## 4. 为什么这么麻烦？ 它的现实意义

你可能会想：“我用软件直接求逆不就行了？ “但在你的研究领域，这个公式有奇效：

1. **分治计算：** 如果 $A$ 是一个 $10000 \times 10000$ 的对角阵，而 $D$ 很小，直接求整个 $M$ 的逆非常慢。 但用这个公式，你只需要对 $A$ 求逆（对角阵求逆是瞬间的）和对很小的 $S$ 求逆。
    
2. **伍德伯里恒等式（Woodbury Identity）：** 它是很多优化算法和卡尔曼滤波的核心，本质上也是由这个分块求逆公式推导出来的。
    
3. **信息提取：** 在统计学中，左上角的 $A^{-1} + A^{-1}BS^{-1}CA^{-1}$ 实际上告诉了我们：在考虑了变量 $D$ 的影响后，$A$ 的不确定性是如何增加的。