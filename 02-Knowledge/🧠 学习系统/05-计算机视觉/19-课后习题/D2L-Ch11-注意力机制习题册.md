---
type: project
topic: "D2L Ch.11 注意力机制课后习题"
created: 2026-08-05
status: active
flow: project
tags: [计算机视觉, 课后习题, D2L, Transformer, 注意力]
---

# 🧠 D2L-Ch11 注意力机制习题册

> 基于 [Dive into Deep Learning (D2L) Ch.11 Attention Mechanisms and Transformers](https://d2l.ai/chapter_attention-mechanisms-and-transformers/index.html)（CC BY-SA 4.0），共 6 道习题。
> 每道题标注考查知识点、难度和对应笔记，形成「学→练→测」闭环。

---

## 📋 题目总览

| 题号 | 类型 | 难度 | 考查知识点 | 前置知识卡 |
|:---:|:---|:---:|:---|:---|
| 1 | 概念 + 类比 | ⭐⭐ 中等 | 注意力机制的 Q/K/V 类比、注意力汇聚的加权平均 | [[Transformer与自注意力]], [[Softmax与交叉熵损失]] |
| 2 | 公式推导 | ⭐⭐⭐ 较难 | Scaled Dot-Product Attention 中 $\sqrt{d_k}$ 的方差归一化作用 | [[Transformer与自注意力]], [[线性代数基础CV]] |
| 3 | 手算 + 推导 | ⭐⭐ 中等 | Multi-Head Attention 的维度拆分、参数矩阵形状、参数量计算 | [[Transformer与自注意力]], [[线性代数基础CV]] |
| 4 | 对比分析 | ⭐⭐ 中等 | 自注意力（Self-Attention）vs 交叉注意力（Cross-Attention）的 Q/K/V 来源差异及应用场景 | [[Transformer与自注意力]] |
| 5 | 推导 + 设计 | ⭐⭐⭐ 较难 | Positional Encoding 的必要性、正弦位置编码公式、相对位置线性表达性质 | [[Transformer与自注意力]], [[线性代数基础CV]] |
| 6 | 流程推导 | ⭐⭐ 中等 | Transformer Encoder 完整前向流程（Embedding → PE → MHA → Add&Norm → FFN → Add&Norm） | [[Transformer与自注意力]], [[反向传播与计算图]], [[Softmax与交叉熵损失]] |

---

## 📝 习题与解析

---

### 习题 1：注意力机制的 Q/K/V 类比与注意力汇聚

> **难度**：⭐⭐ 中等　|　**类型**：概念 + 类比

#### 题目

（1）注意力机制常被类比为**数据库查询**（Database Query）。请完成下表，将注意力机制中的三个核心组件与数据库查询概念对应，并说明每个组件的**语义角色**：

| 注意力组件 | 数据库查询对应 | 数学形式（以向量表示） | 语义角色（一句话） |
|:---|:---|:---|:---|
| Query $\mathbf{q}$ | ① | $\mathbf{q} \in \mathbb{R}^{d_k}$ | ② |
| Key $\mathbf{k}_i$ | ③ | $\mathbf{k}_i \in \mathbb{R}^{d_k}$ | ④ |
| Value $\mathbf{v}_i$ | ⑤ | $\mathbf{v}_i \in \mathbb{R}^{d_v}$ | ⑥ |

（2）写出**注意力汇聚**（Attention Pooling）的加权平均公式：

$$\text{Attention}(\mathbf{q}, \{(\mathbf{k}_i, \mathbf{v}_i)\}_{i=1}^n) = \sum_{i=1}^n \alpha_i \,\mathbf{v}_i$$

其中 $\alpha_i$ 为注意力权重。请给出 $\alpha_i$ 通过 softmax 计算的具体表达式（包含打分函数 $a(\mathbf{q}, \mathbf{k}_i)$），并解释**为什么用 softmax 而非简单归一化**（提示：从梯度、可微性和"聚焦"效果三个角度回答）。

（3）**直观理解**：假设你正在读一篇论文，你想找到关于"Transformer"的信息。在这个场景中：
- Query 是什么？
- Key 是什么？
- Value 是什么？
- 注意力权重 $\alpha_i$ 的物理含义是什么？

#### 前置知识

- Softmax 函数：$\text{softmax}(\mathbf{z})_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$
- 加权平均：$\sum \alpha_i \mathbf{v}_i$，$\sum \alpha_i = 1$，$\alpha_i \ge 0$
- 向量点积作为相似度度量

---

> [!question]- **习题 1 答案解析**

**（1）Q/K/V 与数据库查询对照**

| 注意力组件 | 数据库查询对应 | 数学形式 | 语义角色（一句话） |
|:---|:---|:---|:---|
| Query $\mathbf{q}$ | ① **查询条件**（如 `WHERE topic = "Transformer"`） | $\mathbf{q} \in \mathbb{R}^{d_k}$ | ② **"我想要找什么"**——当前时刻的需求/意图 |
| Key $\mathbf{k}_i$ | ③ **索引键**（数据库中每条记录的索引字段） | $\mathbf{k}_i \in \mathbb{R}^{d_k}$ | ④ **"我有什么可以匹配"**——每个候选内容的特征标签 |
| Value $\mathbf{v}_i$ | ⑤ **记录内容**（数据库中索引指向的实际数据行） | $\mathbf{v}_i \in \mathbb{R}^{d_v}$ | ⑥ **"匹配后提取什么"**——每个候选位置实际承载的信息 |

关键点：$\mathbf{q}$ 和 $\mathbf{k}_i$ 必须在同一空间（均为 $\mathbb{R}^{d_k}$）才能计算相似度；$\mathbf{v}_i$ 可以和 $\mathbf{k}_i$ 不同维度（$d_v \neq d_k$）——因为"匹配"和"提取"是解耦的。

**（2）注意力汇聚公式**

$$\alpha_i = \text{softmax}\big(a(\mathbf{q}, \mathbf{k}_i)\big) = \frac{\exp\big(a(\mathbf{q}, \mathbf{k}_i)\big)}{\sum_{j=1}^n \exp\big(a(\mathbf{q}, \mathbf{k}_j)\big)}$$

其中打分函数 $a(\mathbf{q}, \mathbf{k}_i)$ 常用：
- **加性注意力**（Additive）：$a(\mathbf{q}, \mathbf{k}) = \mathbf{w}_v^\top \tanh(\mathbf{W}_q\mathbf{q} + \mathbf{W}_k\mathbf{k})$
- **缩放点积**（Scaled Dot-Product）：$a(\mathbf{q}, \mathbf{k}) = \frac{\mathbf{q}^\top \mathbf{k}}{\sqrt{d_k}}$

**为什么用 softmax？**

| 角度 | 解释 |
|:---|:---|
| **梯度** | Softmax 输出处处可导，反向传播梯度流畅；简单的 hard-max（选最大）或阈值截断会导致梯度为零。 |
| **可微性** | 整个注意力汇聚 $\sum \alpha_i \mathbf{v}_i$ 可端到端训练——softmax 使离散的"选择"操作变为连续的"软寻址"。 |
| **"聚焦"效果** | Softmax 的指数函数 $e^z$ 放大了打分差异——高分项被指数放大后权重接近 1，低分项被压缩至接近 0，实现了**软注意力**（soft attention）的聚焦效果，同时理论上仍能给所有位置非零权重（保持梯度通路）。 |

**（3）阅读论文的直观场景**

- **Query**：你脑中的问题——"我想了解 Transformer 的注意力机制"（当前需求）。
- **Key**：论文中每个段落/句子的主题标签——"这段讲 CNN"、"这段讲 Transformer 架构"、"这段讲实验结果"。
- **Value**：每个段落的实际内容（文字、公式、图表）。
- **$\alpha_i$ 的物理含义**：你对每个段落的"相关度评分"——讲 Transformer 的段落得到高分（$\alpha \to 1$），讲 CNN 的段落得到低分（$\alpha \to 0$）。最终你读到的"综合信息"是各段落的加权平均——注意力机制让你不是逐字读完，而是**先扫一遍（计算 Key 相似度），再重点读相关部分（按权重聚合 Value）**。

---

### 习题 2：Scaled Dot-Product Attention 中 $\sqrt{d_k}$ 的作用

> **难度**：⭐⭐⭐ 较难　|　**类型**：公式推导

#### 题目

Scaled Dot-Product Attention 的公式为：

$$\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\!\left(\frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{d_k}}\right)\mathbf{V}$$

其中 $\mathbf{Q} \in \mathbb{R}^{n \times d_k}$，$\mathbf{K} \in \mathbb{R}^{m \times d_k}$，$\mathbf{V} \in \mathbb{R}^{m \times d_v}$。

（1）**不加缩放时的问题**：假设 $\mathbf{q}$ 和 $\mathbf{k}$ 的每个分量独立同分布，均值为 0、方差为 1。推导点积 $\mathbf{q}^\top \mathbf{k} = \sum_{j=1}^{d_k} q_j k_j$ 的均值和方差。

（2）当 $d_k$ 较大时（如 $d_k = 64$ 或 $512$），点积的方差导致什么后果？请从 **softmax 的饱和行为**角度分析：方差过大 → softmax 输出趋向什么 → 梯度如何变化？结合 softmax 的雅可比矩阵 $\frac{\partial \alpha_i}{\partial z_j} = \alpha_i(\delta_{ij} - \alpha_j)$ 说明。

（3）除以 $\sqrt{d_k}$ 后，点积的方差变为多少？这一缩放如何使 softmax 保持在非饱和区域？

（4）**延伸思考**：为什么不除以 $d_k$ 而是 $\sqrt{d_k}$？如果 $d_k = 1$，该缩放是否仍有意义？

#### 前置知识

- 独立随机变量之和的方差：$\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y)$（$X, Y$ 独立）
- 独立随机变量之积的方差：$\text{Var}(XY) = \text{Var}(X)\text{Var}(Y) + \text{Var}(X)\mathbb{E}[Y]^2 + \text{Var}(Y)\mathbb{E}[X]^2$
- Softmax 性质：当输入分量差异极大时，输出趋近 one-hot
- 梯度消失：softmax 饱和时 $\frac{\partial \alpha_i}{\partial z_j} \to 0$

---

> [!question]- **习题 2 答案解析**

**（1）点积的均值与方差**

设 $\mathbb{E}[q_j] = \mathbb{E}[k_j] = 0$，$\text{Var}(q_j) = \text{Var}(k_j) = 1$，且 $q_j$ 与 $k_j$ 独立。

- **均值**：

$$\mathbb{E}[\mathbf{q}^\top \mathbf{k}] = \mathbb{E}\!\left[\sum_{j=1}^{d_k} q_j k_j\right] = \sum_{j=1}^{d_k} \underbrace{\mathbb{E}[q_j]}_{=0} \cdot \underbrace{\mathbb{E}[k_j]}_{=0} = 0$$

- **方差**：每个乘积 $q_j k_j$ 的方差：

$$\text{Var}(q_j k_j) = \text{Var}(q_j)\text{Var}(k_j) + \text{Var}(q_j)\underbrace{\mathbb{E}[k_j]^2}_{=0} + \text{Var}(k_j)\underbrace{\mathbb{E}[q_j]^2}_{=0} = 1 \cdot 1 = 1$$

各分量独立，$d_k$ 个乘积之和的方差：

$$\text{Var}(\mathbf{q}^\top \mathbf{k}) = \sum_{j=1}^{d_k} \text{Var}(q_j k_j) = d_k$$

故 $\mathbf{q}^\top \mathbf{k}$ 的**标准差**为 $\sqrt{d_k}$，随维度增大而增大。

**（2）大方差导致的 softmax 饱和问题**

当 $d_k$ 较大（如 512），$\mathbf{q}^\top \mathbf{k}$ 的分布范围约 $\pm 3 \cdot \sqrt{512} \approx \pm 68$。

- 在 softmax 中，极端值经 $\exp(\cdot)$ 放大：$\exp(68) \approx 3.4 \times 10^{29}$，而 $\exp(-68) \approx 2.9 \times 10^{-30}$。
- 结果：softmax 输出**趋近 one-hot**——最大分量 $\alpha_{\max} \approx 1$，其余 $\alpha_i \approx 0$。

**梯度消失**：softmax 雅可比为

$$\frac{\partial \alpha_i}{\partial z_j} = \alpha_i(\delta_{ij} - \alpha_j)$$

- 当 $\alpha_{\max} \approx 1$、其余 $\alpha_i \approx 0$：
  - 最大分量：$\frac{\partial \alpha_{\max}}{\partial z_{\max}} = \alpha_{\max}(1 - \alpha_{\max}) \approx 1 \cdot 0 = 0$（饱和）
  - 其他分量：$\frac{\partial \alpha_i}{\partial z_i} = \alpha_i(1 - \alpha_i) \approx 0$（本身 $\alpha_i \approx 0$）
  - 交叉项：$\frac{\partial \alpha_i}{\partial z_{\max}} = -\alpha_i \alpha_{\max} \approx 0$

→ **几乎所有梯度趋近 0**，反向传播无法有效更新参数，训练停滞。

**（3）$\sqrt{d_k}$ 缩放的归一化效果**

缩放后的点积：

$$\text{Var}\!\left(\frac{\mathbf{q}^\top \mathbf{k}}{\sqrt{d_k}}\right) = \frac{\text{Var}(\mathbf{q}^\top \mathbf{k})}{d_k} = \frac{d_k}{d_k} = 1$$

标准差归 1，缩放后的点积分布在 $\pm 3$ 左右 → softmax 输入不太极端 → 输出远离 one-hot（更平滑，熵更高）→ 梯度保持健康。这就是 **Scaled** Dot-Product Attention 中 "Scaled" 的来源。

**（4）延伸思考**

- **为什么是 $\sqrt{d_k}$ 而非 $d_k$？** 方差 $\propto d_k$，标准差 $\propto \sqrt{d_k}$。要抵消标准差的影响，应除以 $\sqrt{d_k}$。除以 $d_k$ 会**过度缩放**——方差降至 $1/d_k$，softmax 输入过小导致输出趋近均匀分布，注意力机制失去"选择性聚焦"的能力。
- **$d_k = 1$ 时**：$\text{Var} = 1$，$\sqrt{1} = 1$，缩放前后无差别——所以缩放在小维度下可有可无，但在实际 Transformer（$d_k = 64$）中至关重要。

---

### 习题 3：Multi-Head Attention 的维度拆分与参数量推导

> **难度**：⭐⭐ 中等　|　**类型**：手算 + 推导

#### 题目

Multi-Head Attention 的公式为：

$$\text{MultiHead}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h)\mathbf{W}^O$$

$$\text{head}_i = \text{Attention}(\mathbf{Q}\mathbf{W}_i^Q, \mathbf{K}\mathbf{W}_i^K, \mathbf{V}\mathbf{W}_i^V)$$

标准的 Transformer Base 配置：$d_{\text{model}} = 512$，$h = 8$，$d_k = d_v = d_{\text{model}} / h = 64$。

（1）**维度拆分**：填写以下投影矩阵的形状表。

| 投影矩阵 | 输入维度 | 输出维度 | 矩阵形状 |
|:---|:---:|:---:|:---|
| $\mathbf{W}_i^Q$ | $d_{\text{model}}$ | $d_k$ | ① |
| $\mathbf{W}_i^K$ | $d_{\text{model}}$ | $d_k$ | ② |
| $\mathbf{W}_i^V$ | $d_{\text{model}}$ | $d_v$ | ③ |
| $\mathbf{W}^O$（输出投影） | ④ | $d_{\text{model}}$ | ⑤ |

（2）**参数量计算**：计算 Multi-Head Attention 中四个投影矩阵的**总参数量**（不含偏置）。证明该参数量 **与 $h$ 无关**（即只要 $d_k = d_{\text{model}}/h$，$h=1$ 和 $h=8$ 的投影参数量相同）。

（3）**为什么多头优于单头？** 既然参数量相同，用 $h=8$ 个 $d_k=64$ 的小头比用 $h=1$ 个 $d_k=512$ 的大头好在哪？从以下两个角度解释：

- (a) **子空间多样性**：不同 head 可以关注不同类型的依赖关系。举一个 NLP 句子为例。
- (b) **计算效率**：虽然参数量相同，但多头如何利用并行性？

（4）**手算验证**：给定一个简化场景——$d_{\text{model}} = 4$，$h = 2$，$d_k = d_v = 2$，序列长度 $n = 3$。写出 $\text{head}_1$ 和 $\text{head}_2$ 各自的 $\mathbf{Q}_1, \mathbf{K}_1, \mathbf{V}_1$ 维度，以及 Concat 后经 $\mathbf{W}^O$ 投影的最终输出维度。

#### 前置知识

- 矩阵乘法维度规则：$(m \times n) \times (n \times p) = (m \times p)$
- 向量拼接：$\text{Concat}$ 在最后一维
- 参数量 = 输入维度 $\times$ 输出维度（无偏置时）

---

> [!question]- **习题 3 答案解析**

**（1）维度拆分表**

| 投影矩阵 | 输入维度 | 输出维度 | 矩阵形状 |
|:---|:---:|:---:|:---|
| $\mathbf{W}_i^Q$ | $d_{\text{model}} = 512$ | $d_k = 64$ | ① $512 \times 64$ |
| $\mathbf{W}_i^K$ | $d_{\text{model}} = 512$ | $d_k = 64$ | ② $512 \times 64$ |
| $\mathbf{W}_i^V$ | $d_{\text{model}} = 512$ | $d_v = 64$ | ③ $512 \times 64$ |
| $\mathbf{W}^O$（输出投影） | ④ $h \cdot d_v = 8 \times 64 = 512$ | $d_{\text{model}} = 512$ | ⑤ $512 \times 512$ |

关键点：$\mathbf{W}^O$ 的输入是 $h$ 个 head 输出的拼接，维度 $h \cdot d_v = d_{\text{model}}$，恰好等于 $d_{\text{model}}$，这是一致性设计。

**（2）参数量计算**

- 每个 head 的三个投影：$3 \times (d_{\text{model}} \times d_k) = 3 \times 512 \times 64 = 98{,}304$
- $h=8$ 个 head 合计：$8 \times 98{,}304 = 786{,}432$
- 输出投影 $\mathbf{W}^O$：$512 \times 512 = 262{,}144$
- **总参数量**：$786{,}432 + 262{,}144 = 1{,}048{,}576 \approx 1.05\text{M}$

**与 $h$ 无关**的证明：

$$\text{总参数} = h \cdot 3 \cdot d_{\text{model}} \cdot \frac{d_{\text{model}}}{h} + d_{\text{model}} \cdot d_{\text{model}} = 3 \cdot d_{\text{model}}^2 + d_{\text{model}}^2 = 4 \cdot d_{\text{model}}^2$$

$h$ 在 $d_k = d_{\text{model}}/h$ 的约束下被消去 → 无论 $h=1$（单头 $d_k=512$）还是 $h=8$（多头 $d_k=64$），投影参数量恒为 $4 \times 512^2 = 1{,}048{,}576$。

**（3）为什么多头优于单头？**

**(a) 子空间多样性**

单头（$d_k=512$）将所有信息压缩到一个高维注意力空间中做一次平均——相当于"用同一个标准衡量所有词之间的关系"。
多头将 $d_{\text{model}}$ 拆分为 $h$ 个低维子空间（$d_k=64$），每个 head 在**不同的投影子空间**中独立计算注意力。

以句子 `"The cat sat on the mat because it was tired"` 为例：
- **Head 1** 可能关注**句法依赖**：`it` → `cat`（指代消解），学习主语-代词关系。
- **Head 2** 可能关注**位置邻近**：`sat` ↔ `on`（局部搭配）。
- **Head 3** 可能关注**语义角色**：`tired` → `cat`（属性-主体）。
- 其他 Head 关注其他模式。

不同 head 的 $\mathbf{W}_i^Q, \mathbf{W}_i^K$ 将输入投影到不同子空间 → 注意力模式多样化 → 模型可以同时捕捉多种类型的依赖关系。

**(b) 计算效率**

虽然参数量相同，但多头注意力的每个 head 的注意力矩阵大小为 $n \times n$，计算复杂度为 $O(n^2 \cdot d_k) = O(n^2 \cdot d_{\text{model}}/h)$，$h$ 个头合计 $O(n^2 \cdot d_{\text{model}})$——**计算量级不变**。

但关键优势在于**并行性**：$h$ 个 head 的 $\mathbf{Q}\mathbf{K}^\top$ 计算彼此独立 → 可在 GPU 上用批量矩阵乘法（batch matmul）一次完成 → 将 $h$ 个头打包为一个 batch 维度，计算时间接近单头。

**（4）手算验证**

- $d_{\text{model}} = 4$，$h = 2$，$d_k = d_v = 2$，$n = 3$
- 输入 $\mathbf{X} \in \mathbb{R}^{3 \times 4}$（3 个 token，每个 $d_{\text{model}} = 4$）
- 经投影后：
  - $\mathbf{Q}_1 = \mathbf{X}\mathbf{W}_1^Q \in \mathbb{R}^{3 \times 2}$（head_1 的 Q）
  - $\mathbf{K}_1 = \mathbf{X}\mathbf{W}_1^K \in \mathbb{R}^{3 \times 2}$，$\mathbf{V}_1 = \mathbf{X}\mathbf{W}_1^V \in \mathbb{R}^{3 \times 2}$
  - $\text{head}_1 = \text{softmax}\!\left(\frac{\mathbf{Q}_1\mathbf{K}_1^\top}{\sqrt{2}}\right)\mathbf{V}_1 \in \mathbb{R}^{3 \times 2}$
  - 同理 $\text{head}_2 \in \mathbb{R}^{3 \times 2}$
- **Concat**：$\text{Concat}(\text{head}_1, \text{head}_2) \in \mathbb{R}^{3 \times 4}$
- **输出投影**：$\mathbf{W}^O \in \mathbb{R}^{4 \times 4}$，最终输出 $\in \mathbb{R}^{3 \times 4}$——与输入形状一致，支持残差连接。

---

### 习题 4：自注意力（Self-Attention）vs 交叉注意力（Cross-Attention）

> **难度**：⭐⭐ 中等　|　**类型**：对比分析

#### 题目

（1）**定义对比**：完成下表，区分自注意力和交叉注意力。

| 维度 | 自注意力（Self-Attention） | 交叉注意力（Cross-Attention） |
|:---|:---|:---|
| $\mathbf{Q}$ 来源 | ① | ② |
| $\mathbf{K}$ 来源 | ③ | ④ |
| $\mathbf{V}$ 来源 | ⑤ | ⑥ |
| 一句话本质 | ⑦ | ⑧ |
| Transformer 中的典型位置 | ⑨ | ⑩ |

（2）**Transformer 架构中的位置**：在原始 Transformer（Vaswani et al., 2017）中，Encoder 和 Decoder 各自包含哪些注意力类型？用图示标出三处注意力：
- Encoder Self-Attention
- Decoder Self-Attention（含 causal mask）
- Decoder Cross-Attention

（3）**Causal Mask（因果掩码）**：Decoder 的自注意力为什么需要 causal mask？写出 $3 \times 3$ 的因果掩码矩阵（下三角为 0，上三角为 $-\infty$），并解释 softmax 之前加 $-\infty$ 如何阻止信息从未来位置泄露。

（4）**应用拓展**：举出交叉注意力的两个非 NLP 应用（如在视觉或多模态中），并说明各自场景中 Q/K/V 分别对应什么。

#### 前置知识

- Transformer Encoder-Decoder 架构
- Softmax 的性质：$\exp(-\infty) = 0$
- 序列建模中因果性的重要性（自回归生成）

---

> [!question]- **习题 4 答案解析**

**（1）定义对比表**

| 维度 | 自注意力（Self-Attention） | 交叉注意力（Cross-Attention） |
|:---|:---|:---|
| $\mathbf{Q}$ 来源 | ① **输入序列自身**（当前层输入 $\mathbf{X}$） | ② **目标序列**（Decoder 的上一子层输出） |
| $\mathbf{K}$ 来源 | ③ **输入序列自身**（同 $\mathbf{Q}$ 的来源） | ④ **源序列**（Encoder 的最终输出） |
| $\mathbf{V}$ 来源 | ⑤ **输入序列自身**（同 $\mathbf{Q}$ 的来源） | ⑤ **源序列**（Encoder 的最终输出） |
| 一句话本质 | ⑦ **序列内部交互**——每个位置"看"同序列的所有位置，建立内部依赖 | ⑧ **序列间交互**——目标序列"查询"源序列，提取跨序列信息 |
| Transformer 中的典型位置 | ⑨ Encoder 的 MHA 层 + Decoder 的 Masked MHA 层 | ⑩ Decoder 中 Encoder-Decoder Attention 层 |

核心判断标准：**$\mathbf{Q}$ 和 $\mathbf{K}$ 是否来自同一个序列**——是则为自注意力，否则为交叉注意力。

**（2）Transformer 架构中的三处注意力**

```
Encoder:
  Input → [Self-Attention (Q=K=V=Encoder输入) → FFN] × N → Encoder输出

Decoder:
  Input → [Masked Self-Attention (Q=K=V=Decoder输入, causal mask) →
           Cross-Attention (Q=Decoder, K=V=Encoder输出) →
           FFN] × N → 输出概率
```

- **Encoder Self-Attention**：$\mathbf{Q} = \mathbf{K} = \mathbf{V}$，均来自 Encoder 的输入嵌入。每个位置可以"看到"所有其他位置（双向，无 mask）。
- **Decoder Masked Self-Attention**：$\mathbf{Q} = \mathbf{K} = \mathbf{V}$，均来自 Decoder 的输入嵌入。加 causal mask 确保位置 $i$ 只能看到位置 $1 \ldots i$（单向，保持自回归性）。
- **Decoder Cross-Attention**：$\mathbf{Q}$ 来自 Decoder 前一个子层的输出，$\mathbf{K} = \mathbf{V}$ 来自 Encoder 的最终输出。Decoder 的每个位置"查询"Encoder 的所有位置——这是**信息从源序列流向目标序列的桥梁**。

**（3）Causal Mask**

Decoder 在自回归生成时，位置 $t$ 的预测只能依赖已生成的 $1 \ldots t-1$ 位置，不能偷看未来。Causal mask 强制实现这一约束。

$3 \times 3$ 因果掩码（加到 $\mathbf{Q}\mathbf{K}^\top/\sqrt{d_k}$ 上，再送入 softmax）：

$$\mathbf{M} = \begin{bmatrix}
0 & -\infty & -\infty \\
0 & 0 & -\infty \\
0 & 0 & 0
\end{bmatrix}$$

- 位置 1 只能注意位置 1（第一行只有(1,1)为 0）
- 位置 2 可以注意位置 1 和 2
- 位置 3 可以注意全部

加入 mask 后的 softmax：

$$\alpha_{ij} = \frac{\exp(s_{ij} + M_{ij})}{\sum_{k} \exp(s_{ik} + M_{ik})}$$

当 $M_{ij} = -\infty$，$\exp(-\infty) = 0$ → $\alpha_{ij} = 0$，梯度也为 0 → 信息完全阻隔。实现上通常用一个极大的负数（如 $-10^9$）近似 $-\infty$。

**（4）非 NLP 的交叉注意力应用**

| 应用 | $\mathbf{Q}$ | $\mathbf{K} = \mathbf{V}$ | 说明 |
|:---|:---|:---|:---|
| **Stable Diffusion**（文本→图像） | 图像 latent 特征（U-Net 中间层） | 文本编码（CLIP text encoder 输出） | 噪声图像的每个空间位置"查询"文本 token，决定"这里应该生成什么" |
| **DETR**（目标检测） | Object queries（可学习的检测查询向量） | CNN 提取的图像特征图 | 每个 object query"问"图像特征"哪里有目标"，交叉注意力定位目标位置和类别 |
| **Perceiver IO**（多模态） | 任务相关的 latent array | 原始输入（图像像素/文本/音频） | 一个小的 latent array 通过交叉注意力"查询"任意模态的大规模输入，实现模态无关的架构 |

---

### 习题 5：Positional Encoding 的必要性与正弦编码设计

> **难度**：⭐⭐⭐ 较难　|　**类型**：推导 + 设计

#### 题目

（1）**置换等变性**：自注意力机制对输入序列的**位置**做了什么假设？证明：若将输入 $\mathbf{X} = (\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_n)$ 置换为 $\mathbf{X}' = (\mathbf{x}_{\pi(1)}, \mathbf{x}_{\pi(2)}, \ldots, \mathbf{x}_{\pi(n)})$（$\pi$ 为任意排列），自注意力的输出（不加位置编码时）如何变化？这一性质为什么在序列建模中是致命的？

（2）**正弦位置编码**：Transformer 原始论文使用正弦/余弦位置编码：

$$\text{PE}(pos, 2i) = \sin\!\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$$

$$\text{PE}(pos, 2i+1) = \cos\!\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$$

其中 $pos$ 为位置索引（0-based），$i$ 为维度索引（$0, 1, \ldots, d_{\text{model}}/2 - 1$）。

- (a) 为什么使用**不同频率**的正弦/余弦函数？频率随 $i$ 如何变化？画出 $i=0$、$i=1$、$i=15$ 时 PE 随 $pos$ 的变化曲线的定性草图（横轴 $pos$ 0→100，纵轴 PE 值）。
- (b) 解释为什么偶数维用 $\sin$、奇数维用 $\cos$。相邻的 $\sin/\cos$ 对（$2i, 2i+1$）如何编码同一个频率的相位信息？

（3）**相对位置的线性表达**：正弦位置编码的一个优雅性质是：存在线性变换矩阵 $\mathbf{M}_{\Delta}$，使得 $\text{PE}(pos + \Delta)$ 可由 $\text{PE}(pos)$ 经 $\mathbf{M}_{\Delta}$ 线性变换得到。以单频率为例，给出 $\text{PE}(pos) = [\sin(\omega \cdot pos), \cos(\omega \cdot pos)]^\top$，推导 $\text{PE}(pos + \Delta)$ 如何用旋转矩阵表达。这一性质对 Transformer 学习相对位置关系有什么潜在好处？

（4）**可学习 vs 正弦**：Transformer 也可以使用可学习的位置嵌入（Learned Positional Embedding，如 BERT 的做法）。对比两种方案的优劣（训练长度泛化、参数效率、归纳偏置三个维度）。

#### 前置知识

- 三角恒等式：$\sin(a+b) = \sin a \cos b + \cos a \sin b$，$\cos(a+b) = \cos a \cos b - \sin a \sin b$
- 旋转矩阵：$\mathbf{R}(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$
- 序列模型的马尔可夫性 vs 位置感知

---

> [!question]- **习题 5 答案解析**

**（1）置换等变性**

自注意力中 $\alpha_{ij} = \text{softmax}_j(\mathbf{q}_i^\top \mathbf{k}_j / \sqrt{d_k})$——注意力权重仅依赖于 $\mathbf{q}_i$ 和 $\mathbf{k}_j$ 的**内容**（通过投影后的向量内积），与位置 $j$ 无关。

若置换输入序列：$\mathbf{x}_1 \to \mathbf{x}_{\pi(1)}$ 等。则新的注意力权重满足 $\alpha'_{\pi(i), \pi(j)} = \alpha_{i, j}$——**注意力权重随位置一同置换**。最终输出：

$$\text{Attention}(\mathbf{X}') = \pi(\text{Attention}(\mathbf{X}))$$

即输出被完全相同地置换——自注意力是**置换等变**（permutation equivariant）的。

**致命性**：在语言中，"A 追 B"和"B 追 A"含义完全不同，但自注意力无法区分——它把输入视为"一堆特征向量的集合"而非"有序序列"。位置编码打破了这种置换对称性，使模型能感知顺序。

> 数学本质：不加 PE 时，自注意力对输入的行置换群 $\mathcal{S}_n$ 是等变的——这是它作为"集合函数"而非"序列函数"的根本原因。PE 的加法 $\mathbf{x}_i + \mathbf{p}_i$ 使不同位置的 embedding 区分开来，打破了置换等变性。

**（2）正弦位置编码**

**(a) 多频率设计**

频率 $\omega_i = 1 / 10000^{2i/d_{\text{model}}}$。

- $i = 0$：$\omega_0 = 1 / 1 = 1$（高频，周期约 $2\pi$，波长 ≈ 6 个位置）→ 捕捉**局部位置差异**（相邻位置 PE 差异大）
- $i = 15$（$d_{\text{model}} = 512$）：$\omega_{15} = 1 / 10000^{30/512} \approx 1 / 10000^{0.0586} \approx 1 / 1.73 \approx 0.58$（中频）
- $i = d_{\text{model}}/2 - 1$：$\omega_{\max} = 1 / 10000^{1} \approx 10^{-4}$（极低频，波长 ≈ 10000）→ 捕捉**长程位置趋势**

定性草图（$i=0$：高频震荡，$i=1$：中频，$i=15$：几乎平坦的缓慢变化）。

**设计意图**：不同维度编码不同尺度的时间信息——类似信号的傅里叶分解，低维编码精细位置，高维编码粗略位置区域。这使得模型可以同时分辨"相邻词"和"前1/3段落"等不同粒度的位置信息。

**(b) $\sin/\cos$ 配对**

相邻维度 $(2i, 2i+1)$ 使用同一频率 $\omega_i$，但相位差 $\pi/2$：

$$\text{PE}(pos, 2i) = \sin(\omega_i \cdot pos)$$
$$\text{PE}(pos, 2i+1) = \cos(\omega_i \cdot pos)$$

这等价于在每个频率上编码一个**二维旋转向量** $[\sin(\omega_i \cdot pos), \cos(\omega_i \cdot pos)]^\top$。原因见（3）。

**（3）相对位置的线性表达**

设 $\mathbf{p}_{pos} = [\sin(\omega \cdot pos), \cos(\omega \cdot pos)]^\top$。

$$\mathbf{p}_{pos+\Delta} = \begin{bmatrix}
\sin(\omega(pos + \Delta)) \\
\cos(\omega(pos + \Delta))
\end{bmatrix} = \begin{bmatrix}
\sin(\omega \cdot pos)\cos(\omega \cdot \Delta) + \cos(\omega \cdot pos)\sin(\omega \cdot \Delta) \\
\cos(\omega \cdot pos)\cos(\omega \cdot \Delta) - \sin(\omega \cdot pos)\sin(\omega \cdot \Delta)
\end{bmatrix}$$

$$= \underbrace{\begin{bmatrix}
\cos(\omega \cdot \Delta) & \sin(\omega \cdot \Delta) \\
-\sin(\omega \cdot \Delta) & \cos(\omega \cdot \Delta)
\end{bmatrix}}_{\mathbf{M}_{\Delta}}
\begin{bmatrix}
\sin(\omega \cdot pos) \\
\cos(\omega \cdot pos)
\end{bmatrix}
= \mathbf{M}_{\Delta} \cdot \mathbf{p}_{pos}$$

$\mathbf{M}_{\Delta}$ 是旋转矩阵 $\mathbf{R}(-\omega \cdot \Delta)$（顺时针旋转 $\omega \cdot \Delta$），**只依赖于相对偏移 $\Delta$，与绝对位置 $pos$ 无关**。

**潜在好处**：如果 Transformer 的注意力机制或后续线性层能够学习到这种旋转矩阵的等价操作，它就能天然地利用相对位置信息——两个位置 $pos_1$ 和 $pos_2$ 的 PE 内积仅依赖于 $pos_1 - pos_2$（通过旋转矩阵的性质）。这为模型提供了学习相对位置关系的**归纳偏置**（inductive bias）——这正是后来 RoPE（旋转位置编码）的核心思想。

**（4）可学习 vs 正弦位置编码**

| 维度 | 正弦 PE（Sinusoidal） | 可学习 PE（Learned，如 BERT） |
|:---|:---|:---|
| **训练长度泛化** | ✅ 可外推到训练时未见过的长度（公式定义在任意 $pos$） | ❌ 受限于训练时的 max_seq_len，超出部分需截断或插值 |
| **参数效率** | ✅ 零参数（确定性函数，不参与训练） | ❌ 需学习 $L \times d_{\text{model}}$ 参数（对大 $L$ 是负担） |
| **归纳偏置** | ✅ 内嵌相对位置结构（$\sin/\cos$ 可通过旋转矩阵关联） | ❌ 无内置位置结构，完全从数据学习位置语义 |
| **灵活性** | ❌ 固定函数形式，无法适应任务特定的位置模式 | ✅ 可自由学习任务相关的位置表示 |
| **典型使用** | Transformer（原始论文）、大多数 Seq2Seq 模型 | BERT、GPT、ViT（大多数预训练模型） |

实践中，可学习 PE 更流行（因为预训练-微调范式中长度泛化不那么关键），但正弦 PE 在需要长度外推的场景（如长文本生成）仍有优势。

---

### 习题 6：Transformer Encoder 完整前向流程

> **难度**：⭐⭐ 中等　|　**类型**：流程推导

#### 题目

Transformer Encoder 由 $N$ 个相同的层堆叠而成，每层包含：
- Multi-Head Self-Attention（MHA）
- Add & Norm（残差连接 + 层归一化）
- Feed-Forward Network（FFN，位置独立的两层 MLP）
- Add & Norm

（1）**完整流程**：设输入为 token 序列 $\mathbf{X}^{(0)} \in \mathbb{R}^{n \times d_{\text{model}}}$（$n$ 个 token，每个 $d_{\text{model}}$ 维），

- (a) 写出第 $l$ 层 Encoder 的完整前向计算过程（共 4 步，从 $\mathbf{X}^{(l-1)}$ 到 $\mathbf{X}^{(l)}$）。
- (b) 标注每一步的**输出维度**（假设 $d_{\text{model}} = 512$，$d_{\text{ff}} = 2048$）。
- (c) 画出这一层的数据流示意图（文字框图即可），标出残差连接的"绕行"路径。

（2）**残差连接（Add）的作用**：为什么 Transformer 需要残差连接？如果不加残差，深层 Encoder 面临什么问题？从**梯度流动**和**信息保持**两个角度回答。

（3）**层归一化（LayerNorm）vs 批归一化（BatchNorm）**：Transformer 为什么选用 LayerNorm 而非 BatchNorm？

- (a) 写出 LayerNorm 的公式：对每个样本的 $d_{\text{model}}$ 个特征做归一化。
- (b) 为什么在序列建模中，batch 维度的统计量不可靠？

（4）**FFN 的位置独立性**：Encoder 中的 FFN 对每个 token 位置**独立**应用相同的两层 MLP：

$$\text{FFN}(\mathbf{x}) = \text{ReLU}(\mathbf{x}\mathbf{W}_1 + \mathbf{b}_1)\mathbf{W}_2 + \mathbf{b}_2$$

为什么 FFN 需要位置独立（同一组权重应用于所有位置）？如果每个位置用不同的 FFN 权重，会发生什么问题？

#### 前置知识

- 残差连接：$\text{Output} = \text{Layer}(\text{Input}) + \text{Input}$
- LayerNorm：沿特征维归一化（每个样本独立）
- ReLU 激活函数
- 参数共享 vs 位置特定参数

---

> [!question]- **习题 6 答案解析**

**（1）完整前向流程**

**(a) 第 $l$ 层的前向计算（4 步）**

设输入为 $\mathbf{X} = \mathbf{X}^{(l-1)} \in \mathbb{R}^{n \times 512}$。

**Step 1：Multi-Head Self-Attention**

$$\mathbf{A} = \text{MultiHead}(\mathbf{X}, \mathbf{X}, \mathbf{X}) \in \mathbb{R}^{n \times 512}$$

其中 $\mathbf{Q} = \mathbf{X}\mathbf{W}^Q$，$\mathbf{K} = \mathbf{X}\mathbf{W}^K$，$\mathbf{V} = \mathbf{X}\mathbf{W}^V$，8 个头各输出 $n \times 64$，拼接后 $n \times 512$，经 $\mathbf{W}^O$ 投影仍为 $n \times 512$。

**Step 2：Add & Norm（第一次）**

$$\mathbf{X}_{\text{mid}} = \text{LayerNorm}\big(\mathbf{X} + \mathbf{A}\big) \in \mathbb{R}^{n \times 512}$$

残差连接 $\mathbf{X} + \mathbf{A}$ 形状不变；LayerNorm 沿 $d_{\text{model}}$ 维归一化。

**Step 3：Feed-Forward Network**

$$\mathbf{F} = \text{FFN}(\mathbf{X}_{\text{mid}}) = \text{ReLU}(\mathbf{X}_{\text{mid}}\mathbf{W}_1 + \mathbf{b}_1)\mathbf{W}_2 + \mathbf{b}_2$$

- $\mathbf{W}_1 \in \mathbb{R}^{512 \times 2048}$，$\mathbf{b}_1 \in \mathbb{R}^{2048}$
- $\mathbf{W}_2 \in \mathbb{R}^{2048 \times 512}$，$\mathbf{b}_2 \in \mathbb{R}^{512}$
- 中间激活：$n \times 2048$（经 ReLU）
- 输出：$\mathbf{F} \in \mathbb{R}^{n \times 512}$

**Step 4：Add & Norm（第二次）**

$$\mathbf{X}^{(l)} = \text{LayerNorm}\big(\mathbf{X}_{\text{mid}} + \mathbf{F}\big) \in \mathbb{R}^{n \times 512}$$

**(b) 维度追踪表**

| 步骤 | 运算 | 输出维度 | 说明 |
|:---|:---|:---:|:---|
| 输入 | $\mathbf{X}^{(l-1)}$ | $n \times 512$ | — |
| 1 | MHA($\mathbf{X}, \mathbf{X}, \mathbf{X}$) | $n \times 512$ | 自注意力汇聚 |
| 2 | $\text{LayerNorm}(\mathbf{X} + \mathbf{A})$ | $n \times 512$ | 残差 + 归一化 |
| 3-中间 | $\mathbf{X}_{\text{mid}}\mathbf{W}_1 + \mathbf{b}_1$ | $n \times 2048$ | FFN 第一层（扩张 4×） |
| 3-激活 | $\text{ReLU}(\cdot)$ | $n \times 2048$ | 非线性 |
| 3-输出 | $\cdot \mathbf{W}_2 + \mathbf{b}_2$ | $n \times 512$ | FFN 第二层（投影回 $d_{\text{model}}$） |
| 4 | $\text{LayerNorm}(\mathbf{X}_{\text{mid}} + \mathbf{F})$ | $n \times 512$ | 残差 + 归一化 |

**(c) 数据流示意图**

```
X^(l-1)  ─────────────────────────────┐
   │                                   │
   ▼                                   │
┌──────────┐                           │
│  MHA     │  (n×512 → n×512)         │
│ Self-Att │                           │
└──────────┘                           │
   │                                   │
   ▼                                   ▼
   A                              (残差连接)
   │                                   │
   └─────────── (+) ───────────────────┘
                  │
                  ▼
            LayerNorm  ────────────────┐
                  │                    │
                  ▼                    │
            ┌──────────┐               │
            │  FFN     │               │
            │ 512→2048 │               │
            │ ReLU     │               │
            │ 2048→512 │               │
            └──────────┘               │
                  │                    │
                  ▼                    ▼
                  F              (残差连接)
                  │                    │
                  └───── (+) ─────────┘
                          │
                          ▼
                      LayerNorm
                          │
                          ▼
                      X^(l)  (n×512)
```

**（2）残差连接的作用**

| 角度 | 无残差连接的问题 | 残差连接的解决 |
|:---|:---|:---|
| **梯度流动** | 深层网络中梯度经多层非线性变换后指数衰减（梯度消失），浅层参数几乎不更新 | 残差路径提供了梯度的"高速公路"：$\frac{\partial (\mathbf{X} + F(\mathbf{X}))}{\partial \mathbf{X}} = \mathbf{I} + \frac{\partial F}{\partial \mathbf{X}}$，单位矩阵 $\mathbf{I}$ 保证梯度至少为 1 → 梯度可无损反传至浅层 |
| **信息保持** | 每层必须学习"有用的变换"——如果某层学不好（如注意力分散），输出反而比输入差 | 残差连接使层只需学习**残差** $F(\mathbf{X})$（即对输入的修正），最差情况 $F(\mathbf{X}) \to 0$ → 该层退化为恒等映射 → 网络深度增加至少不会变差 |

这也是 Transformer 可以堆叠到 24 层（BERT-large）甚至 96 层（GPT-3）的关键设计——没有残差连接，深层 Transformer 根本无法训练。

**（3）LayerNorm vs BatchNorm**

**(a) LayerNorm 公式**

对单个样本 $\mathbf{x} \in \mathbb{R}^{d_{\text{model}}}$：

$$\mu = \frac{1}{d_{\text{model}}}\sum_{j=1}^{d_{\text{model}}} x_j, \quad \sigma^2 = \frac{1}{d_{\text{model}}}\sum_{j=1}^{d_{\text{model}}} (x_j - \mu)^2$$

$$\hat{x}_j = \frac{x_j - \mu}{\sqrt{\sigma^2 + \epsilon}}, \quad y_j = \gamma_j \hat{x}_j + \beta_j$$

其中 $\gamma, \beta \in \mathbb{R}^{d_{\text{model}}}$ 为可学习的缩放和平移参数，$\epsilon$ 为防止除零的微小常数。

关键：$\mu$ 和 $\sigma^2$ 是沿**特征维度**（$d_{\text{model}}$）计算的，每个样本独立。

**(b) 为什么不用 BatchNorm？**

BatchNorm 沿 batch 维度计算统计量 $\mu_{\text{batch}}, \sigma^2_{\text{batch}}$。在序列建模中：

- **序列长度不一**：同一 batch 中不同句子长度不同 → padding 位置破坏了统计量的语义（padding token 的特征不应参与归一化统计）。
- **Batch 间统计不稳定**：小 batch（受 GPU 显存限制，NLP 中常见 batch_size = 16 或 32）时 batch 统计量方差大。
- **训练-推理不一致**：BatchNorm 在推理时需用训练集的滑动平均统计量 → 若推理时遇到与训练分布不同的序列长度，统计量不匹配。
- **自回归生成**：推理时逐 token 生成，batch_size = 1 → BatchNorm 完全失效。

LayerNorm 每个样本独立归一化 → 训练和推理行为完全一致，对 batch size 不敏感，且天然处理变长序列。

**（4）FFN 的位置独立性**

FFN 对每个位置 $pos = 1, \ldots, n$ 独立应用相同的 $\mathbf{W}_1, \mathbf{W}_2$：

$$\mathbf{F}_{pos,:} = \text{ReLU}(\mathbf{X}_{pos,:}\mathbf{W}_1 + \mathbf{b}_1)\mathbf{W}_2 + \mathbf{b}_2$$

**为什么位置独立？**

- **参数效率**：共享权重使参数量不随序列长度增长——无论 $n=10$ 还是 $n=1000$，FFN 参数量固定为 $2 \times d_{\text{model}} \times d_{\text{ff}} \approx 2 \times 512 \times 2048 \approx 2.1\text{M}$。若每个位置独立，参数量 $\propto n$，无法处理变长序列。
- **泛化能力**：共享 FFN 学到的是"对任意 token 的特征变换"（如"将主语相关的特征放大"），而非"对位置 5 的特定变换"——前者泛化到未见过的位置和新长度。
- **位置信息已在 Attention 中处理**：MHA 负责跨位置的信息交互（"谁和谁相关"），FFN 负责逐位置的非线性特征变换（"每个 token 内部的语义加工"）——这是 Transformer 的基本分工。

若每位置用不同 FFN 权重：参数量爆炸、无法处理变长序列、位置 5 的权重对位置 500 毫无意义 → 完全破坏序列模型的泛化能力。

---

## 📐 使用说明

1. **作答前先写"作答前信心：__/100"**，完成后写"作答后信心：__/100"，对比校准元认知。
2. **推导题**写出完整推导过程（如题2的方差推导、题3的参数量证明），不跳步。
3. **错题记录**错因，24h / 72h / 7d 重测，形成间隔复习。
4. **建议学习路径**：先看完 [[Transformer与自注意力]] 知识卡 → 做题 1（建立直觉）→ 题 2（深入缩放原理）→ 题 3（掌握维度拆分）→ 题 4（理清架构角色）→ 题 5（理解位置编码设计）→ 题 6（贯通完整流程）。

---

## 🔗 相关知识卡

- [[Transformer与自注意力]] — 核心概念知识卡
- [[Softmax与交叉熵损失]] — Softmax 梯度与饱和行为
- [[反向传播与计算图]] — 残差连接的梯度流
- [[线性代数基础CV]] — 矩阵乘法维度规则、方差推导
- [[梯度下降CV]] — 梯度消失与训练稳定性
