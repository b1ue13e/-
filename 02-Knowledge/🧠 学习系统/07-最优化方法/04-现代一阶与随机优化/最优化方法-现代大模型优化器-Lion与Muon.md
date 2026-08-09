---
type: study
topic: "现代大模型优化器-Lion与Muon"
course: "07-最优化方法"
created: 2026-08-08
status: completed
flow: knowledge
kind: concept
stage_moc: "[[🧭 阶段4-现代一阶与随机优化]]"
difficulty: advanced
upstream:
  - "[[最优化方法-Adam与自适应学习率]]"
  - "[[最优化方法-动量法与重球法]]"
---
# 最优化方法-现代大模型优化器-Lion与Muon

## 1. 这个知识点解决什么问题？
> **我们遇到了什么麻烦**：
> 传统的 AdamW 优化器需要维护两个独立的二阶矩状态（一阶动量 $m_t$ 与二阶平方矩 $v_t$），在千亿参数大语言模型（LLM）训练中带来了极其高昂的 **$2 \times 4\text{ Bytes}/\text{param}$ 显存开销**；同时，AdamW 的坐标级缩放（Coordinate-wise Scaling）在处理权重矩阵时忽略了矩阵的整体谱结构（Singular Spectrum），容易导致梯度奇异值过度膨胀或坍缩。
> **回答**：
> 1. **Lion (EvoLved Sign Momentum)**：通过进化算法搜索发现的符号动量优化器，仅保留一阶动量，完全移除二阶矩 $v_t$，将优化器显存开销减少 $50\%$，并通过 $\text{sign}(\cdot)$ 算子使每个参数的更新步长拥有严格一致的 $L_\infty$ 范数界；
> 2. **Muon (Momentum Orthogonalized by Newton-Schulz)**：专为大模型 2D 权重矩阵设计的二阶谱优化器。它通过快速 **Newton-Schulz 矩阵五阶多项式迭代**，将动量矩阵极快地正交化为最近的酉/正交矩阵（$\mathcal{O}_{d_1 \times d_2}$），确保参数矩阵在每个方向上的更新能量完全均衡，显著加快预训练收敛速度。

---
## 2. 为什么它重要？它有什么用？
- **连接大图景**：它是从 2014 年 AdamW 走向 2024+ 现代大模型前沿优化器的关键跳跃；代表了从“元素级独立启发式自适应”向“符号几何约束”与“矩阵谱正交化”的范式演进。
- **实际应用场景**：
  - **LLM 预训练加速**：Moonshot AI (Kimi)、Keller Jordan (Muon 创作者) 等在 LLaMA/GPT 架构训练中将 Muon 用于线性投影层（$W_q, W_k, W_v, W_{\text{out}}, W_{\text{mlp}}$），实现 1.5x~2x 的样本效率提升；
  - **超大规模显存瘦身**：Lion 广泛用于 Diffusion 图像生成与多模态大模型微调，减少数十 GB 的 GPU 显存占用。
- **高频面试/研究任务**：推导 Newton-Schulz 矩阵正交化迭代、分析 Lion 符号动量在非凸优化中的有界更新性质、对比 AdamW 与 Lion/Muon 的显存与计算复杂度。

---
## 3. 学它之前需要哪些前置知识？
1. **[[最优化方法-Adam与自适应学习率]]**：理解指数移动平均（EMA）与 AdamW 的解耦权重衰减。
2. **[[最优化方法-动量法与重球法]]**：理解 Polyak 动量与指数平滑更新机制。
3. **[[最优化方法-向量范数与特征值基础]]**：理解矩阵谱范数（Spectral Norm）与奇异值分解（SVD）。

---
## 4. 用直觉语言解释它
> «"AdamW 就像给每个参数装了一个温度计，根据各自的历史方差微调步长，但要带双倍背包（两份状态）；
> Lion 丢掉了温度计，只看风向（动量的正负符号），每一步都迈出整齐划一的刚毅步伐（Sign）；
> Muon 则是矩阵层面的瑜伽大师，不管动量矩阵被拉伸得多么扭曲畸变，都通过几步矩阵乘法（Newton-Schulz）把它迅速扳成一个各个方向均匀施力的‘正交旋转矩阵’。"»

- **一句话本质**：**Lion 用纯符号统一更新步长界，Muon 用矩阵正交化拉平奇异值谱。**

---
## 5. 正式定义、核心公式、符号解释

### 1. Lion (EvoLved Sign Momentum) 算法
给定损失函数 $f(\theta)$，学习率 $\eta$，动量超参数 $\beta_1, \beta_2 \in (0, 1)$，权重衰减 $\lambda$：
1. **计算插值动量方向**：
   $$ c_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t $$
2. **符号更新参数**：
   $$ \theta_t = \theta_{t-1} - \eta \left( \text{sign}(c_t) + \lambda \theta_{t-1} \right) $$
3. **更新动量缓存**：
   $$ m_t = \beta_2 m_{t-1} + (1 - \beta_2) g_t $$

> **关键差异**：用于更新参数的方向 $c_t$（依赖 $\beta_1$）与用于沉淀为历史动量的 $m_t$（依赖 $\beta_2$）显式解耦，通常设置 $\beta_1 = 0.9, \beta_2 = 0.99$。

---

### 2. Muon (Momentum Orthogonalized by Newton-Schulz) 算法
设 2D 权重矩阵 $W \in \mathbb{R}^{d_1 \times d_2}$（假设 $d_1 \le d_2$），梯度为 $G_t$：
1. **经典 Nesterov/Polyak 动量累积**：
   $$ M_t = \mu M_{t-1} + G_t $$
2. **Newton-Schulz 五阶矩阵多项式正交化**：
   令 $X_0 = \frac{M_t}{\|M_t\|_F + \epsilon} \cdot \alpha$（通过谱范数上界做初始缩放），迭代 5~6 次：
   $$ X_{k+1} = \frac{1}{16} X_k \left( 68 I - 159 B_k + 140 B_k^2 - 49 B_k^3 \right), \quad B_k = X_k X_k^T $$
   迭代收敛至最近的正交化矩阵 $U = \text{NewtonSchulz}(M_t) \approx U_M V_M^T$（其中 $M_t = U_M \Sigma_M V_M^T$ 为 SVD 分解）。
3. **按谱尺度更新权重**：
   $$ W_t = W_{t-1} - \eta \cdot \text{RMS\_Scale}(W_{t-1}, d_1, d_2) \cdot U $$

---

### 3. 符号与复杂度对比表

| 优化器 | 状态显存开销 (Bytes/param) | 核心算子 | 适用参数类型 | 奇异值谱特性 |
| :--- | :---: | :---: | :---: | :--- |
| **AdamW** | $8\text{ B}$ ($m_t, v_t$ fp32) | 坐标级二阶除法 | 1D/2D 通用 | 坐标拉平，非矩阵谱不变 |
| **Lion** | $4\text{ B}$ ($m_t$ 仅一阶) | $\text{sign}(\cdot)$ 元素符号 | 1D/2D 通用 | $L_\infty$ 刚性投影，抗噪强 |
| **Muon** | $4\text{ B}$ ($M_t$ 仅一阶) | Newton-Schulz 矩阵乘 | 专用于 2D 权重矩阵 | **所有奇异值严格拉平为 1** |

---

## 6. 推导思路与思想来源

### 为什么 Newton-Schulz 可以替代极其昂贵的 SVD？
要将矩阵 $M$ 投影到最近的等距正交矩阵集合 $\mathcal{S} = \{ Q \in \mathbb{R}^{d_1 \times d_2} \mid Q Q^T = I \}$，数学上的解析解为极分解（Polar Decomposition）：
$$ Q^* = \arg\min_{Q Q^T = I} \| Q - M \|_F = U_M V_M^T $$
然而在 GPU 上对一个 $4096 \times 4096$ 的矩阵进行直接 SVD 的时间复杂度为 $\mathcal{O}(d^3)$ 且极难高度并行。

**Newton-Schulz 思想**：构造零点迭代函数 $f(X) = X X^T - I = 0$。通过 Padé 近似或泰勒展开构造仅含矩阵乘法（GEMM）的高阶多项式迭代：
$$ X_{k+1} = a X_k + b X_k(X_k^T X_k) + c X_k(X_k^T X_k)^2 + \dots $$
选取系数使得在奇异值区间 $\sigma(X) \in (0, \sqrt{3})$ 内，映射函数 $g(\sigma) = \frac{1}{16}\sigma(68 - 159\sigma^2 + 140\sigma^4 - 49\sigma^6)$ 快速超线性收敛到 $1$。5 次 GEMM 迭代即可达到浮点精度下 $X X^T \approx I$。

---

## 7. 例子：Python/NumPy 完整实现

```python
import numpy as np

def newton_schulz5(G: np.ndarray, steps: int = 5, eps: float = 1e-7) -> np.ndarray:
    """
    Newton-Schulz 5阶多项式正交化算法 (Muon 核心)
    输入: G 动量矩阵 (d1, d2)
    输出: U 近似正交矩阵 (d1, d2)，满足 U @ U.T ≈ I (假设 d1 <= d2)
    """
    transposed = False
    if G.shape[0] > G.shape[1]:
        G = G.T
        transposed = True
        
    d1, d2 = G.shape
    # 初始归一化确保奇异值落在收敛域 (0, sqrt(3)) 内
    norm = np.linalg.norm(G, 'fro') + eps
    X = G / norm * np.sqrt(d1)
    
    # 5 阶多项式系数
    a, b, c, d = 68.0 / 16.0, -159.0 / 16.0, 140.0 / 16.0, -49.0 / 16.0
    
    for _ in range(steps):
        # B = X @ X.T
        B = X @ X.T
        B2 = B @ B
        B3 = B2 @ B
        # X = a*X + b*B@X + c*B2@X + d*B3@X
        poly = a * np.eye(d1) + b * B + c * B2 + d * B3
        X = poly @ X
        
    return X.T if transposed else X


class LionOptimizer:
    """Lion 符号动量优化器最小实现"""
    def __init__(self, params, lr=1e-4, beta1=0.9, beta2=0.99, weight_decay=0.01):
        self.params = list(params)
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.wd = weight_decay
        self.exp_avg = [np.zeros_like(p) for p in self.params]

    def step(self, grads):
        for p, g, m in zip(self.params, grads, self.exp_avg):
            # 1. 权重衰减
            if self.wd != 0:
                p -= self.lr * self.wd * p
            # 2. 插值方向并取符号
            c = self.beta1 * m + (1.0 - self.beta1) * g
            update = np.sign(c)
            # 3. 参数更新
            p -= self.lr * update
            # 4. 动量累积
            m *= self.beta2
            m += (1.0 - self.beta2) * g
```

---

## 8. 常见误区与注意点
1. **误区：Lion 的学习率设置可以直接套用 AdamW**  
   - *纠错*：因为 Lion 的更新量是 $\text{sign}(\cdot)$（模长恒为 1），而 AdamW 的更新量通常在 $10^{-1} \sim 10^{-2}$ 数量级。因此 **Lion 的学习率通常需要设为 AdamW 的 $1/3 \sim 1/10$**，而权重衰减 $\lambda$ 通常需要放大 $3 \sim 10$ 倍。
2. **误区：Muon 可以无脑替换模型中的所有参数（如 LayerNorm、Embedding）**  
   - *纠错*：Muon 的正交化假设参数是**高维二维矩阵变换**。对于 1D 向量（偏置、LayerNorm 仿射参数）或稀疏 Embedding，应继续使用 AdamW 或 Lion，仅对 Attention/MLP 稠密投影矩阵使用 Muon。

---

## 9. 检索练习自测
1. **【闭卷自测】** Lion 相比 AdamW 为什么能省下整整一半的优化器显存？
2. **【推导题】** 若梯度全为正数，经过 Newton-Schulz 5 阶迭代后，输出矩阵 $U$ 的每个奇异值是多少？
3. **【应用题】** 为什么在深层 Transformer 预训练中，将动量矩阵正交化（Muon）能有效缓解梯度弥散与爆炸？

---

## 10. 🃏 Anki 卡片

```anki
deck: 07-最优化方法
tags: [最优化方法, 现代一阶与随机优化, Lion, Muon, 大模型优化器]

# Card 1
Q: Lion 优化器相比传统 AdamW 在状态显存上有什么巨大优势？其核心更新算子是什么？
A: 
1. **显存减少 50%**：移除了 AdamW 的二阶方差矩 $v_t$，只保留一阶动量 $m_t$（每个参数仅需 4 字节显存）；
2. **核心算子**：使用符号算子 $\text{sign}(\beta_1 m_{t-1} + (1-\beta_1) g_t)$ 进行有界刚性更新。
---
# Card 2
Q: 简述 Muon 优化器正交化梯度动量的数学目标及其采用的快速数值方法。
A: 
1. **数学目标**：将 2D 权重动量矩阵 $M$ 投影到最近的正交酉矩阵 $U_M V_M^T$（拉平所有奇异值为 1，各方向均匀更新）；
2. **数值方法**：采用 **Newton-Schulz 5 阶多项式迭代**（纯 GPU 矩阵乘法 GEMM），避免了昂贵的 SVD 分解。
```

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/07-最优化方法"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
