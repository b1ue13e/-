---
type: project
topic: "D2L Ch.17 GAN课后习题"
created: 2026-08-05
status: active
flow: project
tags: [计算机视觉, 课后习题, D2L, GAN, 生成模型]
---

# 🎭 D2L-Ch17 生成对抗网络习题册

> 基于 [Dive into Deep Learning (D2L) Ch.17 Generative Adversarial Networks](https://d2l.ai/chapter_generative-adversarial-networks/index.html)（CC BY-SA 4.0），共 6 道习题。
> 每道题标注考查知识点、难度和对应笔记，形成「学→练→测」闭环。

---

## 📋 题目总览

| 题号 | 类型 | 难度 | 考查知识点 | 前置知识卡 |
|:---:|:---|:---:|:---|:---|
| 1 | 公式推导 + 简答 | ⭐⭐ 中等 | GAN minimax 博弈公式、最优判别器 | [[生成模型GAN与Diffusion]], [[Softmax与交叉熵损失]] |
| 2 | 简答 + 流程描述 | ⭐ 基础 | 生成器与判别器的交替训练策略、non-saturating loss | [[生成模型GAN与Diffusion]], [[反向传播与计算图]] |
| 3 | 原因分析 | ⭐⭐ 中等 | GAN 训练不稳定原因（梯度消失/振荡/判别器崩塌） | [[生成模型GAN与Diffusion]], [[梯度下降CV]] |
| 4 | 架构分析 + 简答 | ⭐ 基础 | DCGAN 架构改进：BatchNorm / 全卷积 / LeakyReLU | [[生成模型GAN与Diffusion]], [[卷积神经网络CNN]], [[批归一化BatchNorm]] |
| 5 | 现象分析 + 简答 | ⭐⭐ 中等 | 模式坍缩（Mode Collapse）的现象与原因 | [[生成模型GAN与Diffusion]] |
| 6 | 综合对比 | ⭐⭐⭐ 较难 | GAN vs VAE vs Diffusion 生成范式对比 | [[生成模型GAN与Diffusion]], [[VAE]] |

---

## 📝 习题与解析

---

### 习题 1：GAN Minimax 博弈公式

> **难度**：⭐⭐ 中等　|　**类型**：公式推导 + 简答

#### 题目

（1）写出 GAN 的 minimax 目标函数 $V(D, G)$，并逐项解释 $\max_D$ 和 $\min_G$ 各自追求什么。

（2）证明：当生成器 $G$ 固定时，最优判别器为

$$D^*_G(\mathbf{x}) = \frac{p_{\text{data}}(\mathbf{x})}{p_{\text{data}}(\mathbf{x}) + p_g(\mathbf{x})}$$

（3）将 $D^*_G$ 代回 $V(D, G)$，化简得 $\min_G V(D^*_G, G) = -\log 4 + 2 \cdot \text{JSD}(p_{\text{data}} \| p_g)$。据此解释：为什么 GAN 的全局最优对应于 $p_g = p_{\text{data}}$？

#### 前置知识

- 二元交叉熵损失 $-\big[y\log\hat{y} + (1-y)\log(1-\hat{y})\big]$
- 期望 $\mathbb{E}$ 的线性性质
- Jensen-Shannon 散度定义：$\text{JSD}(P\|Q) = \frac{1}{2}\text{KL}(P\|M) + \frac{1}{2}\text{KL}(Q\|M)$，$M = \frac{P+Q}{2}$

---

> [!question]- **习题 1 答案解析**

**（1）目标函数**

$$\min_G \max_D V(D, G) = \mathbb{E}_{\mathbf{x} \sim p_{\text{data}}}[\log D(\mathbf{x})] + \mathbb{E}_{\mathbf{z} \sim p_z}[\log(1 - D(G(\mathbf{z})))]$$

逐项解释：

| 项 | $\max_D$ 视角 | $\min_G$ 视角 |
|:---|:---|:---|
| $\mathbb{E}_{p_{\text{data}}}[\log D(\mathbf{x})]$ | $D$ 想给真样本打高分 → $\log D(\mathbf{x})$ 尽量大（接近 0） | $G$ 不影响此项（无 $G$ 出现） |
| $\mathbb{E}_{p_z}[\log(1 - D(G(\mathbf{z})))]$ | $D$ 想让假样本 $D(G) \to 0$，此项 $\to \log 1 = 0$ | $G$ 想让 $D(G) \to 1$，此项 $\to \log 0 = -\infty$ |

- **$\max_D$**：$D$ 希望真样本高分、假样本低分——做好二分类器。
- **$\min_G$**：$G$ 只控制第二项，希望生成的假样本骗过 $D$（$D(G) \to 1$）。

**（2）最优判别器推导**

固定 $G$，$V$ 作为 $D$ 的泛函：

$$V(D, G) = \int_{\mathbf{x}} p_{\text{data}}(\mathbf{x}) \log D(\mathbf{x}) + p_g(\mathbf{x}) \log(1 - D(\mathbf{x})) \, d\mathbf{x}$$

对每个 $\mathbf{x}$ 独立最大化被积函数 $f(D) = a\log D + b\log(1-D)$（$a = p_{\text{data}}(\mathbf{x})$, $b = p_g(\mathbf{x})$）。

求导：$\frac{df}{dD} = \frac{a}{D} - \frac{b}{1-D} = 0 \;\Longrightarrow\; D^* = \frac{a}{a+b}$。

代入得 $D^*_G(\mathbf{x}) = \frac{p_{\text{data}}(\mathbf{x})}{p_{\text{data}}(\mathbf{x}) + p_g(\mathbf{x})}$。由于 $D(\mathbf{x}) \in [0, 1]$，该解在定义域内，即为全局最优。

**（3）代入化简与全局最优**

将 $D^*_G$ 代回 $V$（过程省略，见 Goodfellow et al. 2014 或 D2L 17.2.2 节）：

$$\min_G V(D^*_G, G) = -\log 4 + 2 \cdot \text{JSD}(p_{\text{data}} \| p_g)$$

- $\text{JSD}(P\|Q) \ge 0$，当且仅当 $P = Q$ 时取 0。
- 故 $\min_G V = -\log 4$，当且仅当 $p_g = p_{\text{data}}$。
- **直观**：当生成分布与真实分布完全一致，判别器无法区分（$D^* = 0.5$），生成器达到全局最优。

---

### 习题 2：生成器与判别器的交替训练策略

> **难度**：⭐ 基础　|　**类型**：简答 + 流程描述

#### 题目

（1）GAN 训练采用"先训 $D$ $k$ 步，再训 $G$ $1$ 步"的交替策略。为什么通常取 $k = 1$（或较小的 $k$）？$k$ 过大会导致什么问题？

（2）早期的 minimax loss 使用 $\min_G \mathbb{E}[\log(1 - D(G))]$。实际训练中，Goodfellow 建议改用 non-saturating loss $\max_G \mathbb{E}[\log D(G)]$。请解释这一修改的**梯度动机**：画出 $\log(1 - D)$ 和 $-\log D$ 在 $D \in (0, 1)$ 上的曲线草图，说明在训练初期 $D(G) \approx 0$ 时，两种 loss 的梯度差异。

（3）用 PyTorch 伪代码写出 GAN 的一次训练迭代（含 $D$ 更新和 $G$ 更新），标注哪里用 `.detach()` 以及为什么。

#### 前置知识

- 反向传播与计算图冻结（`.detach()` / `torch.no_grad()`）
- Sigmoid 函数及其梯度特性
- BCE loss

---

> [!question]- **习题 2 答案解析**

**（1）$k$ 的取值**

通常 $k = 1$（交替各一步）。原因：
- $k$ 过大 → $D$ 过强 → $D(G) \to 0$ → $G$ 梯度消失（Sigmoid 饱和区梯度 ≈ 0）。
- GAN 是一个追鞍点问题，而非固定目标优化。$D$ 的"最优"随 $G$ 变化而漂移，过拟合当前 $G$ 的 $D$ 不能给下一轮 $G$ 提供有效梯度。
- 实践中 $k=1$ 计算开销最小且效果可接受；部分变体（如 WGAN）建议 $k=5$，因改用 Wasserstein 距离后 $D$ 需更精确近似。

**（2）Non-saturating loss 的梯度动机**

| $D(G)$ 值 | $\log(1-D)$ 梯度 | $-\log D$ 梯度 |
|:---|:---|:---|
| 接近 0（训练初期） | $\frac{-1}{1-D} \approx -1$（平） | $\frac{-1}{D}$ → $-\infty$（陡） |
| 接近 1（训练后期） | $\frac{-1}{1-D}$ → $-\infty$（陡） | $\frac{-1}{D} \approx -1$（平） |

- **早期**（$G$ 弱，$D(G) \approx 0$）：$\log(1-D)$ 曲线平坦，梯度微小，$G$ 几乎不更新 → **梯度消失**。$-\log D$ 在 $D \to 0$ 时梯度爆炸式增长，给 $G$ 强信号。
- **后期**（$G$ 强，$D(G) \approx 0.5$）：两种 loss 梯度相当，non-saturating loss 不影响收敛方向。
- **结论**：non-saturating loss 以偏离理论 minimax 为代价，换取了训练初期的有效梯度——是理论与实践的必要调和。

**（3）PyTorch 伪代码**

```python
for real, _ in dataloader:
    bs = real.size(0)
    # ---- 训 D：真 → 1，假 → 0（G 冻结） ----
    z = torch.randn(bs, z_dim)
    fake = G(z).detach()          # ★ detach：切断 G 的计算图
    loss_D = (BCE(D(real), torch.ones(bs)) +
              BCE(D(fake), torch.zeros(bs))) / 2
    opt_D.zero_grad(); loss_D.backward(); opt_D.step()

    # ---- 训 G：让 D(假) → 1（D 冻结，non-saturating） ----
    z = torch.randn(bs, z_dim)
    loss_G = BCE(D(G(z)), torch.ones(bs))
    opt_G.zero_grad(); loss_G.backward(); opt_G.step()
```

关键点：
- 训 $D$ 时 `G(z).detach()`：假样本不向 $G$ 回传梯度，$D$ 更新不影响 $G$。
- 训 $G$ 时不需 `.detach()` $D$：`opt_G` 只持有 $G$ 的参数，`loss_G.backward()` 虽流经 $D$ 但 `opt_G.step()` 只更新 $G$，$D$ 参数不变。

---

### 习题 3：GAN 训练不稳定的原因分析

> **难度**：⭐⭐ 中等　|　**类型**：原因分析

#### 题目

GAN 的训练以不稳定著称。请从以下三个角度分析其原因，并给出每种问题的**诊断信号**（训练中如何发现）和**缓解手段**：

（1）**梯度消失**：为什么 $G$ 的梯度会消失？non-saturating loss 如何缓解？

（2）**判别器崩塌**：完美判别器为什么有害？纳什均衡下 $D$ 的理想输出应是多少？

（3）**不收敛 / 振荡**：GAN 的优化目标为什么不是凸优化？追鞍点（而非固定目标）为什么导致振荡？

#### 前置知识

- Sigmoid 饱和特性
- 凸优化与鞍点优化的区别
- JS 散度的性质

---

> [!question]- **习题 3 答案解析**

**（1）梯度消失**

- **原因**：$G$ 弱 → $D(G) \approx 0$ → 原始 loss $\log(1 - D(G))$ 在 $D \approx 0$ 时的导数 $\frac{-1}{1-D} \approx -1$，而 Sigmoid 输出端的实际梯度还要乘以 $\sigma'(x) = \sigma(x)(1-\sigma(x))$，当 $\sigma(x) \approx 0$ 时 $\sigma' \approx 0$ → 双重衰减 → $G$ 收不到有效梯度。
- **诊断信号**：$D$ loss 迅速降至接近 0，$G$ loss 居高不下或停滞。
- **缓解**：non-saturating loss $\max \log D(G)$，在 $D(G) \to 0$ 时梯度 $\to \infty$（见习题 2）。

**（2）判别器崩塌**

- **原因**：$D$ 完美区分真假 → $D$ 对 $G(z)$ 输出 0 → $G$ 梯度为 0 → $G$ 停止学习。$D$ 越强，$G$ 越弱——恶性循环。
- **诊断信号**：$D$ 准确率接近 100%，$D$ loss → 0，$G$ loss 不降。
- **理想均衡**：纳什均衡下 $p_g = p_{\text{data}}$，$D^*(x) = \frac{p_{\text{data}}}{p_{\text{data}} + p_g} = 0.5$。$D$ 对所有输入输出 0.5，对应的 BCE loss ≈ $-\log 0.5 - \log 0.5 = 2\log 2 \approx 1.38$。
- **缓解**：标签平滑（label smoothing，真 → 0.9 而非 1）、梯度惩罚（WGAN-GP）、削弱 $D$（加噪声 / Dropout）。

**（3）不收敛 / 振荡**

- **原因**：
  - GAN 目标 $\min_G \max_D V(D, G)$ 是鞍点问题，非凸优化。在参数空间中，$G$ 沿梯度下降方向更新，而每步更新后 $D$ 的最优点也漂移了——这不再是"走向固定最低点"，而是"追移动的鞍点"。
  - JS 散度在高维空间中，当 $p_g$ 和 $p_{\text{data}}$ 支撑集不重叠时恒为 $\log 2$（常数），梯度为 0 → 无法提供有意义的优化方向。
- **诊断信号**：$D$ 和 $G$ 的 loss 均剧烈振荡，生成质量时好时坏，不收敛。
- **缓解**：WGAN（用 Wasserstein 距离替代 JS 散度，处处可导）、WGAN-GP（梯度惩罚替代权重裁剪）、谱归一化（Spectral Normalization）稳定 $D$。

---

### 习题 4：DCGAN 的架构改进

> **难度**：⭐ 基础　|　**类型**：架构分析 + 简答

#### 题目

DCGAN（Radford et al., 2016）首次将 CNN 成功应用于 GAN，提出了四条核心架构改进。请逐一回答：

（1）**用跨步卷积（Strided Conv）替代池化层**：为什么池化层不适合 GAN？跨步卷积如何让网络**自己学习**空间下采样/上采样？

（2）**在生成器和判别器中均使用 BatchNorm**：BatchNorm 在 $G$ 和 $D$ 中各起什么作用？为什么 $G$ 的输出层和 $D$ 的输入层**不加** BatchNorm？

（3）**去掉全连接层，改用全卷积**：去掉全连接层的两个好处是什么？（提示：参数量、空间结构）

（4）**$G$ 用 ReLU（输出层 Tanh），$D$ 用 LeakyReLU**：为什么 $G$ 不用 Sigmoid 输出？为什么 $D$ 用 LeakyReLU 而非普通 ReLU？

#### 前置知识

- 卷积 / 转置卷积（ConvTranspose2d）
- BatchNorm 的训练/推理模式差异
- ReLU / LeakyReLU / Tanh 激活函数特性

---

> [!question]- **习题 4 答案解析**

**（1）跨步卷积替代池化**

- **池化不适合 GAN 的原因**：池化（max pooling / average pooling）是固定的、不可学习的下采样——它丢弃了空间位置信息。对 $G$ 而言，上采样若用固定插值（最近邻/双线性），同样缺乏可学习性。
- **跨步卷积的优势**：
  - $D$ 中用 `stride=2` 的卷积替代池化 → 网络自己学习如何下采样，保留对分类有用的空间特征。
  - $G$ 中用转置卷积（`ConvTranspose2d`，stride > 1）替代固定插值上采样 → 网络自己学习如何从低分辨率特征恢复高分辨率细节。
- **一句话**：让网络自己学"怎样压缩/放大"，而非用固定规则。

**（2）BatchNorm 的使用与例外**

- **在 $G$ 中**：稳定生成器的层间激活分布，防止梯度爆炸/消失，加速收敛。
- **在 $D$ 中**：同上，稳定判别器的训练。
- **$G$ 输出层不加 BN**：输出层需要精确映射到 $[-1, 1]$（Tanh 范围），BN 的缩放和偏移会破坏这一约束，且引入 batch 间的统计依赖。
- **$D$ 输入层不加 BN**：输入是真实/生成图像，BN 会在 batch 内混合真假样本的统计量，引入不必要的耦合，使 $D$ 难以学到清晰的决策边界。

**（3）去掉全连接层的好处**

- **参数量**：全连接层参数 $O(n_{\text{in}} \times n_{\text{out}})$，如 128×7×7 → 1024 需 $\approx 6.4\text{M}$ 参数。全卷积用 $1\times 1$ conv 或直接 reshape，参数大幅减少。
- **空间结构**：全连接将特征展平丢失空间拓扑，而全卷积保留空间维度 → $G$ 可以在不同位置生成一致纹理，$D$ 可以在不同位置检测模式。
- **额外好处**：全卷积使 $G$ 可接受任意尺寸的 latent code（全局平均池化后进入分类），增强了灵活性。

**（4）激活函数选择**

- **$G$ 用 ReLU + Tanh 输出**：
  - ReLU 在 $G$ 的隐藏层中提供稀疏梯度，加速训练且避免 Sigmoid 的饱和问题。
  - 输出层用 Tanh（$[-1, 1]$）：图像像素值归一化到 $[-1, 1]$ 是 DCGAN 的标准预处理。Tanh 以零为中心，梯度比 Sigmoid 更稳定，且生成效果在实践中优于 Sigmoid。
- **$D$ 用 LeakyReLU**：
  - 普通 ReLU 在 $x < 0$ 时梯度为 0 → 神经元可能永久死亡。
  - LeakyReLU（$\alpha = 0.2$）在负半轴保留小梯度 → 即使某个神经元对当前 batch 输出负值，仍有梯度信号可以恢复。
  - GAN 训练不稳定 → 任何可以避免"信息彻底丢失"的设计都值得采用。LeakyReLU 比 ReLU 更能容忍训练中的剧烈波动。

---

### 习题 5：模式坍缩（Mode Collapse）

> **难度**：⭐⭐ 中等　|　**类型**：现象分析 + 简答

#### 题目

（1）**现象描述**：用 MNIST 训练 GAN 为例，描述模式坍缩的典型表现。如果数据集有 10 个数字类别，发生完全模式坍缩和部分模式坍缩分别是什么样子？

（2）**数学原因**：从 minimax 目标和 JS 散度的角度，解释为什么 GAN 倾向于模式坍缩。提示：$G$ 的最优策略为什么是"找到 $p_{\text{data}}$ 的一个高密度模式并只生成它"？

（3）**缓解方法**：列举至少三种缓解模式坍缩的技术，并简要说明各自的原理。

#### 前置知识

- Kullback-Leibler 散度 vs Jensen-Shannon 散度
- minimax 博弈的纳什均衡
- Minibatch discrimination / WGAN / 多样性正则化

---

> [!question]- **习题 5 答案解析**

**（1）现象描述**

以 MNIST（手写数字 0-9，10 类）为例：

- **完全模式坍缩**：$G$ 对所有 $\mathbf{z}$ 只生成同一个数字（如总是"1"）。无论 latent code 如何变化，输出几乎相同。判别器在这个数字上无法区分真假，但对其他 9 个数字的覆盖率为 0。
- **部分模式坍缩**：$G$ 只覆盖了 2-3 个数字（如"1""7""0"），其他数字从不出现。生成的"1"质量可能很高，但多样性严重不足。
- **检测方法**：生成大量样本 → 用预训练分类器（如 MNIST 的 LeNet）统计生成样本的类别分布 → 若某些类别频率 ≈ 0，则发生了模式坍缩。

**（2）数学原因**

- GAN 的 minimax 目标在最优 $D$ 下等价于最小化 $2\cdot\text{JSD}(p_{\text{data}}\|p_g) - \log 4$。
- **JS 散度的关键缺陷**：当 $p_g$ 和 $p_{\text{data}}$ 的支撑集不重叠（或重叠测度极小），$\text{JSD} = \log 2$（常数），梯度为 0。
- **贪心策略**：$G$ 的梯度更新只关心"当前生成的样本能否骗过 $D$"，而不关心"是否覆盖了 $p_{\text{data}}$ 的全部模式"。如果 $G$ 发现某个模式（如"1"）容易生成且能稳定骗过 $D$，它会将所有 probability mass 集中到该模式——因为覆盖更多模式需要更多"努力"，而 loss 不会因覆盖不全而惩罚 $G$。
- **本质**：minimax 目标缺少对分布**多样性**的显式约束。$D$ 只告诉 $G$"这个样本像不像真的"，不告诉它"你漏掉了哪些模式"。

**（3）缓解方法**

| 方法 | 原理 |
|:---|:---|
| **Minibatch Discrimination** | 让 $D$ 看到整个 minibatch 的统计特征（而非单样本），从而检测"这 batch 里的样本都太像了"——$G$ 被迫增加多样性来骗过这种 group-level 判别。 |
| **WGAN / WGAN-GP** | 用 Wasserstein 距离替代 JS 散度。Wasserstein 距离在支撑集不重叠时仍然连续可导，提供有意义的梯度信号 → $G$ 被迫向 $p_{\text{data}}$ 的所有模式移动。 |
| **Unrolled GAN** | 在更新 $G$ 时，展开 $D$ 的多步更新（unrolling），让 $G$"预见" $D$ 对当前 $G$ 的反应，而非只对当前 $D$ 做最优响应 → 抑制了 $G$ 的贪心行为。 |
| **多样性正则化** | 在 loss 中加入鼓励样本多样性的项（如 pairwise 相似度惩罚），显式惩罚生成样本之间的相似性。 |
| **经验重放（Experience Replay）** | 在 $D$ 训练时混入 $G$ 的历史生成样本，防止 $G$ 通过"来回切换模式"欺骗当前 $D$。 |

---

### 习题 6：GAN vs VAE vs Diffusion 生成范式对比

> **难度**：⭐⭐⭐ 较难　|　**类型**：综合对比

#### 题目

生成模型的三大主流范式——VAE、GAN、Diffusion——从不同角度解决"学习 $p(\mathbf{x})$ 并采样"这一问题。

（1）**填表**：完成下表中的空缺项。

| 维度 | VAE | GAN | Diffusion (DDPM) |
|:---|:---|:---|:---|
| **建模方式** | 显式：$p(\mathbf{x}) = \int p(\mathbf{x}\|\mathbf{z})p(\mathbf{z})d\mathbf{z}$ | ① | 显式：$T$ 步马尔可夫链 $p_\theta(\mathbf{x}_{0:T})$ |
| **训练目标** | ② | Minimax（BCE） | ③ |
| **生成机制** | $\mathbf{z} \sim p(\mathbf{z})$ → Decoder → $\hat{\mathbf{x}}$ | ④ | $\mathbf{x}_T \sim \mathcal{N}(0,\mathbf{I})$ → $T$ 步去噪 → $\mathbf{x}_0$ |
| **生成质量** | 模糊（MSE/ELBO 倾向于平均） | ⑤ | 顶级超高清 |
| **多样性** | 好（随机采样 $\mathbf{z}$） | ⑥ | 极好 |
| **训练稳定性** | ⑦ | 差（鞍点/振荡/模式坍缩） | ⑧ |
| **采样速度** | 1 步（快） | ⑨ | ⑩ |

（2）**分析题**：2022 年后 Diffusion 模型（Stable Diffusion、DALL·E 3、Midjourney）在 AIGC 领域取代 GAN 成为主流。从训练稳定性、生成多样性和可扩展性三个角度分析这一范式转移的原因。GAN 是否有 Diffusion 无法替代的优势？

#### 前置知识

- VAE 的 ELBO 与重参数化技巧
- GAN 的 minimax 博弈
- DDPM 的前向闭式解与反向去噪

---

> [!question]- **习题 6 答案解析**

**（1）填表答案**

| 维度 | VAE | GAN | Diffusion (DDPM) |
|:---|:---|:---|:---|
| **建模方式** | 显式：$p(\mathbf{x}) = \int p(\mathbf{x}\|\mathbf{z})p(\mathbf{z})d\mathbf{z}$ | ① **隐式**：无显式 $p(\mathbf{x})$，通过 $G(\mathbf{z})$ 定义隐式分布 | 显式：$T$ 步马尔可夫链 $p_\theta(\mathbf{x}_{0:T})$ |
| **训练目标** | ② **ELBO**（重构 loss + KL 散度） | Minimax（BCE） | ③ **MSE**（预测噪声 $\|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta\|^2$） |
| **生成机制** | $\mathbf{z} \sim p(\mathbf{z})$ → Decoder → $\hat{\mathbf{x}}$ | ④ $\mathbf{z} \sim p(\mathbf{z})$ → $G(\mathbf{z})$ **单步前向** | $\mathbf{x}_T \sim \mathcal{N}(0,\mathbf{I})$ → $T$ 步去噪 → $\mathbf{x}_0$ |
| **生成质量** | 模糊（MSE/ELBO 倾向于平均） | ⑤ **高清逼真**（但可能模式坍缩） | 顶级超高清 |
| **多样性** | 好（随机采样 $\mathbf{z}$） | ⑥ **差**（模式坍缩风险） | 极好 |
| **训练稳定性** | ⑦ **极稳定**（ELBO 是凸下界） | 差（鞍点/振荡/模式坍缩） | ⑧ **极稳定**（MSE 天然收敛） |
| **采样速度** | 1 步（快） | ⑨ **1 步（极快，实时）** | ⑩ **50~1000 步（慢，需加速）** |

**（2）分析题**

**Diffusion 取代 GAN 的原因**：

- **训练稳定性**：Diffusion 的 MSE 目标是凸优化问题（给定 $\mathbf{x}_t$ 预测噪声），天然稳定收敛。GAN 的 minimax 是鞍点优化，不保证收敛，且 JS 散度在支撑集不重叠时梯度为零。Diffusion 的 $L_{\text{simple}}$ 不需要交替训练两个网络——只需训一个 U-Net → 调试成本极低。
- **生成多样性**：Diffusion 从纯噪声出发，经 $T$ 步随机去噪，每一步注入随机性 → 天然保证多样性。GAN 的 minimax 目标无显式多样性约束 → 模式坍缩是系统性问题。在大规模多类别数据集（如 LAION-5B）上，GAN 的模式坍缩几乎是必然的。
- **可扩展性**：Diffusion 架构极易扩展——加文本条件（Cross-Attention → Stable Diffusion）、加空间控制（ControlNet）、低秩微调（LoRA）、潜在空间压缩（Latent Diffusion）。GAN 的条件生成（cGAN）同样可行，但训练不稳定性随条件复杂度放大。

**GAN 的不可替代优势**：

- **采样速度**：GAN 单步前向 → 实时生成（<10ms），Diffusion 需 20-50 步（DDIM 加速后仍需数百毫秒至秒级）。在需要实时/低延迟生成的场景（如视频游戏纹理、交互式图像编辑），GAN 仍有优势。
- **隐空间语义**：GAN 的 $\mathbf{z}$ 空间经 StyleGAN 发展出高度解耦的语义方向（如"年龄""表情""姿态"），可直接做语义编辑。Diffusion 的隐空间编辑（如 DDIM Inversion → 编辑 → 去噪）更复杂且可能引入伪影。
- **未来可能**：GAN + Diffusion 混合（如 GAN 做快速预览、Diffusion 做精修）是活跃研究方向。

---

## 📐 使用说明

1. **建议顺序**：习题 1-2 → 习题 4 → 习题 3-5 → 习题 6，由浅入深。
2. **基础路径**（必做）：习题 1(1)、2、4、5(1) —— 覆盖 GAN 核心公式、训练策略、DCGAN 架构和模式坍缩现象。
3. **进阶路径**（选做）：习题 1(2)(3)、3、5(2)(3)、6 —— 含推导证明和跨范式对比。
4. **动手实践**：习题 2(3) 建议实际运行 DCGAN 训练代码（如 D2L 官方 Notebook），观察 loss 曲线和生成质量演变。

---

## 🔗 相关笔记

- [[生成模型GAN与Diffusion]] — 主知识卡（GAN + Diffusion 对比）
- [[GAN]] — GAN 细节卡（待完善）
- [[VAE]] — VAE 参照系
- [[卷积神经网络CNN]] — DCGAN 的卷积骨干
- [[批归一化BatchNorm]] — DCGAN 关键组件
- [[反向传播与计算图]] — 交替训练的梯度流向
- [[Softmax与交叉熵损失]] — BCE loss 基础
- [[梯度下降CV]] — 优化基础
