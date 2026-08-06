---
type: study
course: "05-计算机视觉"
topic: "Diffusion 扩散模型 (DDPM)"
created: 2026-08-05
status: ongoing
difficulty: intermediate
concept:
  - Diffusion
  - DDPM
  - 去噪
  - 重参数化
  - 生成模型
prerequisites:
  - VAE
  - 概率分布
  - 马尔可夫链
related:
  - StableDiffusion
  - GAN
  - ControlNet
flow: knowledge
stage_moc: "[[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🚀 第四阶段：前沿架构探索]]"
kind: concept
source: "论文+讲义; CS231n A3"
anki_deck: "05-计算机视觉::04-前沿架构探索"
anki_tags:
  - 学习
  - 深度学习
  - AIGC
  - 扩散模型
  - DDPM
  - 去噪
tags:
  - 学习
  - 深度学习
  - AIGC
  - 扩散模型
  - DDPM
  - 去噪
---

# 🎯 Diffusion 扩散模型 (DDPM)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：扩散模型（Diffusion Models，以 DDPM 为代表）由 Jonathan Ho 等人于 2020 年提出，是当下**AIGC 与文本生成图像（Text-to-Image）时代的绝对基石**（Stable Diffusion、Midjourney、DALL-E 3、Sora 的底层核心驱动引擎）。它打破了 GAN 训练不稳定、模式崩溃的困境，通过优雅的马尔可夫链前向加噪与反向去噪过程，实现了前所未有的超高质量图像生成。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem (我们遇到了什么麻烦)**：
> 在扩散模型之前，生成模型主要依赖 GAN 和 VAE：
> - **GAN**：生成质量极高，但对抗训练极度不稳定，容易发生模式崩溃（Mode Collapse，只生成某几种特定的猫）；
> - **VAE**：训练非常稳定，但生成的图像总是模糊不清。
> 我们迫切需要一种**既具备 VAE 极强稳定性与理论完备性，又具备 GAN 顶级高清细节生成能力**的新一代生成范式。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：扩散模型将“图像生成”转化成了“一步步去除高斯噪声”的拟合过程。不搞懂 DDPM 的前向加噪闭式解与反向去噪推导，就无法理解 Conditional Control (ControlNet)、Latent Diffusion (SD) 以及视频生成模型 (Sora)。
- **实际应用场景**：AI 画图（Stable Diffusion）、图像修复与超分辨率（Inpainting/Super-resolution）、生物分子蛋白质结构生成、音频/视频生成。
- **高频考点/任务**：前向加噪重参数闭式解 $x_t = \sqrt{\bar{\alpha}_t}x_0 + \sqrt{1-\bar{\alpha}_t}\epsilon$ 推导、简化目标函数 $L_{simple}(\theta)$ 为什么是拟合噪声、U-Net 时间步嵌入 (Time Embedding)、PyTorch 手写简单 DDPM 去噪网络。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🎯 VAE 变分自编码器 (Variational Autoencoder)|VAE 与变分下界]]**：扩散模型本质上是一个显式包含 $T$ 个隐步长的超深变分自编码器，目标函数也是由变分下界 (ELBO) 逐步简化推导而来。
2. **[[02-Knowledge/🧠 学习系统/24-随机过程/02-马尔可夫与泊松过程/马尔可夫与泊松过程-应用入口-1|马尔可夫链 (Markov Chain)]]**：当前状态 $x_t$ 仅依赖于上一时刻状态 $x_{t-1}$ 的离散随机过程。

---

## 4. 用直觉语言解释它

> «“这东西其实就像……”»

- **直觉类比**：扩散模型就像**雕刻大师恢复被侵蚀的雕像**：
  - **前向过程（毁坏/加噪）**：拿一尊精美的雕像（高清图像 $x_0$），每天往上面刮风下雨滴几滴强酸（加一点点高斯噪声），持续 1000 天（$T=1000$）。最后雕像彻底被风化成了一堆毫无形状的沙尘（纯高斯噪声 $x_T$）。
  - **反向过程（雕刻/去噪）**：训练一个无比聪明的神经网络（U-Net 雕刻师）。给他看第 $t$ 天风化严重的沙尘，让他**预测“昨天下雨时具体落下了哪些微小沙尘（噪声 $\epsilon$）”**。
  - **生成新图像**：随机抓一堆纯高斯沙尘 $x_T$，让雕刻师连续倒退 1000 步去除沙尘，一尊全新的精美雕像（新图像 $x_0$）就此诞生！
- **为什么很自然**：一步到位生成高清大图太难了；但把生成任务拆解成 1000 步“微小去噪”，每一步都极其简单自然！
- **一句话直觉本质**：用马尔可夫链把大生成分解为千步微小去噪，用神经网络拟合每一步加入的高斯噪声。

---

## 5. 正式定义、核心公式、符号解释

### 1. 前向加噪过程 (Forward Process, 固定不可学)
从真实图像 $x_0 \sim q(x)$ 出发，按马尔可夫链逐步添加高斯噪声（预定义噪声方差序列 $\beta_1, \dots, \beta_T$）：
$$q(x_t \mid x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t} x_{t-1}, \beta_t \mathbf{I})$$

### 2. 前向加噪闭式解 (无需一步步迭代，直接求 $x_t$)
定义 $\alpha_t = 1 - \beta_t$，$\bar{\alpha}_t = \prod_{s=1}^t \alpha_s$，则 $x_t$ 可直接由 $x_0$ 表达为：
$$\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(0, \mathbf{I})$$

### 3. 反向去噪过程 (Reverse Process, 神经网络拟合)
由神经网络 $\boldsymbol{\epsilon}_{\theta}(\mathbf{x}_t, t)$ 参数化估计高斯噪声：
$$p_{\theta}(\mathbf{x}_{t-1} \mid \mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; \boldsymbol{\mu}_{\theta}(\mathbf{x}_t, t), \boldsymbol{\Sigma}_{\theta}(\mathbf{x}_t, t))$$

### 4. 简化后的核心训练目标函数 ($L_{simple}$)
非常优雅！只要求神经网络预测加入的噪声 $\boldsymbol{\epsilon}$ 与真实噪声的 MSE 损失：
$$L_{simple}(\theta) = \mathbb{E}_{t, \mathbf{x}_0, \boldsymbol{\epsilon}} \left[ \| \boldsymbol{\epsilon} - \boldsymbol{\epsilon}_{\theta}(\mathbf{x}_t, t) \|^2 \right]$$

### 5. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\mathbf{x}_0$ | 原始真实图像数据 | $\mathbb{R}^{C \times H \times W}$ | 训练集真实样本 |
| $\mathbf{x}_t$ | 第 $t$ 步时刻的带噪图像 | $\mathbb{R}^{C \times H \times W}$ | 当 $t=T$ 时几乎为纯噪声 |
| $\beta_t$ | 第 $t$ 步设定的噪声方差 | $(0, 1)$，如 $10^{-4} \to 0.02$ | 预先指定的超参数 Schedule |
| $\bar{\alpha}_t$ | 累乘衰减系数 | $\prod_{s=1}^t (1-\beta_s) \in (0, 1)$ | 控制 $x_0$ 残留信号比例 |
| $\boldsymbol{\epsilon}_{\theta}(\mathbf{x}_t, t)$ | 去噪 U-Net 神经网络 | $\mathbb{R}^{C \times H \times W}$ | 输入带噪图与时间步 $t$，预测噪声 |

---

## 6. 推导思路和思想来源

- **最初困难**：想求反向去噪分布 $q(x_{t-1}|x_t)$，利用贝叶斯公式 $q(x_{t-1}|x_t) = \frac{q(x_t|x_{t-1}) q(x_{t-1})}{q(x_t)}$，但由于不知道无噪全局分布 $q(x_{t-1})$，这个反向步骤无法直接求解。
- **关键转念 1**：**如果给定原始干净图像 $x_0$，反向条件分布 $q(x_{t-1} | x_t, x_0)$ 是完全可精确求解的高斯分布！**
  - 利用贝叶斯定理展开：
    $$q(x_{t-1} \mid x_t, x_0) = q(x_t \mid x_{t-1}, x_0) \frac{q(x_{t-1} \mid x_0)}{q(x_t \mid x_0)}$$
  - 右边三项均是前向闭式高斯分布！将三项的高斯概率密度展开指数项，配平方项后惊奇地发现：其均值 $\tilde{\boldsymbol{\mu}}_t$ 精确等于：
    $$\tilde{\boldsymbol{\mu}}_t = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \boldsymbol{\epsilon} \right)$$
- **关键转念 2**：既然均值公式中唯一的未知量就是加进去的噪声 $\boldsymbol{\epsilon}$，那么**神经网络只需要去预测输入图像 $\mathbf{x}_t$ 中包含的真实噪声 $\boldsymbol{\epsilon}$ 即可！**

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（前向闭式加噪计算）
- **题目**：设某个单像素值 $x_0 = 1.0$，在第 $t$ 步时累乘系数 $\bar{\alpha}_t = 0.64$（即 $\sqrt{\bar{\alpha}_t} = 0.8$）。若抽样到的标准高斯噪声 $\epsilon = 0.5$。求生成的带噪像素 $x_t$。
- **解答过程**：
  代入前向闭式公式：
  $$x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon = 0.8 \times 1.0 + \sqrt{1 - 0.64} \times 0.5 = 0.8 + 0.6 \times 0.5 = 0.8 + 0.3 = 1.1$$
- **🤔 追问**：当 $t \to T=1000$ 时，$\bar{\alpha}_T \to 0$，此时 $x_T$ 会变成什么？
  - *答*：$\sqrt{\bar{\alpha}_T} \approx 0 \implies x_T \approx \sqrt{1} \cdot \epsilon = \epsilon \sim \mathcal{N}(0, 1)$，完全变成了纯标准高斯噪声！

### 例子 2：中等例子（DDPM 采样生成单步递推推导）
推导由神经网络预测出噪声 $\hat{\boldsymbol{\epsilon}}_{\theta}$ 后，如何从 $x_t$ 计算得到前一步 $x_{t-1}$。
- **递推采样公式**：
  $$\mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \boldsymbol{\epsilon}_{\theta}(\mathbf{x}_t, t) \right) + \sigma_t \mathbf{z}, \quad \mathbf{z} \sim \mathcal{N}(0, \mathbf{I})$$
  当 $t=1$ 时，加噪项 $\mathbf{z} = 0$，得到最终生成的干净图像 $\mathbf{x}_0$。

### 例子 3：实际应用（PyTorch 核心 DDPM 训练与采样伪代码）

```python
import torch
import torch.nn as nn

class MiniDDPM:
    def __init__(self, timesteps=1000, beta_start=1e-4, beta_end=0.02):
        self.timesteps = timesteps
        # 1. 预计算 noise schedule 参数
        self.betas = torch.linspace(beta_start, beta_end, timesteps)
        self.alphas = 1.0 - self.betas
        self.alphas_cumprod = torch.cumprod(self.alphas, dim=0) # \bar{\alpha}_t
        self.sqrt_alphas_cumprod = torch.sqrt(self.alphas_cumprod)
        self.sqrt_one_minus_alphas_cumprod = torch.sqrt(1.0 - self.alphas_cumprod)

    def q_sample(self, x_0, t, noise=None):
        # 2. 前向闭式加噪: x_t = sqrt(\bar\alpha_t)*x_0 + sqrt(1-\bar\alpha_t)*noise
        if noise is None:
            noise = torch.randn_like(x_0)
        sqrt_alpha_bar = self.sqrt_alphas_cumprod[t].view(-1, 1, 1, 1)
        sqrt_one_minus_alpha_bar = self.sqrt_one_minus_alphas_cumprod[t].view(-1, 1, 1, 1)
        return sqrt_alpha_bar * x_0 + sqrt_one_minus_alpha_bar * noise, noise

    def p_losses(self, denoise_model, x_0, t):
        # 3. 训练 Loss: 让 U-Net 预测输入的真实 noise
        x_noisy, noise = self.q_sample(x_0, t)
        predicted_noise = denoise_model(x_noisy, t)
        loss = nn.functional.mse_loss(predicted_noise, noise)
        return loss

    @torch.no_grad()
    def p_sample(self, model, x, t, t_index):
        # 4. 反向去噪采样单步
        beta_t = self.betas[t_index]
        sqrt_one_minus_alpha_bar_t = self.sqrt_one_minus_alphas_cumprod[t_index]
        sqrt_recip_alpha_t = torch.sqrt(1.0 / self.alphas[t_index])
        
        # 预测均值
        model_mean = sqrt_recip_alpha_t * (x - beta_t / sqrt_one_minus_alpha_bar_t * model(x, t))
        if t_index == 0:
            return model_mean
        else:
            posterior_variance = beta_t # 简化方差
            noise = torch.randn_like(x)
            return model_mean + torch.sqrt(posterior_variance) * noise
```

---

## 8. 常见误区和易混概念

### 误区 1：扩散模型的反向去噪过程可以直接一步到位
- **错误直觉**：“既然前向加噪可以闭式解一步求出 $x_T$，反向去噪也可以一步把 $x_T$ 变成 $x_0$。”
- **为什么错**：前向加噪是已知的线性高斯加噪；而反向去噪对应的数据流形（Manifold）高度非线性复杂。一次性大步去噪会导致极其严重的偏离与模糊，必须通过多步（如 50-1000 步）小步微分迭代（或借助 DDIM 加速）。

### 概念对比表

| 模型 | 生成机制 | 训练稳定度 | 图像细节质量 | 采样步数 (推理速度) |
| :--- | :--- | :--- | :--- | :--- |
| **GAN** | 单步生成器对抗判别器 | 极不稳定 (易 Mode Collapse) | 极高 | **1 步**（极快） |
| **VAE** | 编码至 Latent 采样单步解码 | 极稳定 | 偏模糊 | **1 步**（极快） |
| **Diffusion (DDPM)** | 马尔可夫链多步迭代去噪 | **极稳定** (MSE损失) | **顶级超高清** | **50 - 1000 步**（较慢，需加速） |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🎯 VAE 变分自编码器 (Variational Autoencoder)]]：DDPM 的变分下界推导与目标函数简化源泉。
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/🎯 ResNet (残差网络)]]：DDPM 去噪主干网络 U-Net 中大量使用了 ResNet 残差块。

### 下游延伸
- LatentDiffusion：Stable Diffusion 核心，将 DDPM 从像素空间移至 VAE 隐空间以大幅加速。

### 横向关联
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/生成模型GAN与Diffusion]] ↔ 🎯 Diffusion 扩散模型 (DDPM)：生成模型两大王者，Diffusion 凭借训练稳定性和多模态可控性超越 GAN。

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清楚 Diffusion 解决什么问题（平衡生成质量与训练稳定性）。
- [ ] 2. 用直觉语言解释它（«“这东西其实就像风化雕像的逆向雕刻恢复……”»）。
- [ ] 3. 写出前向加噪的闭式解公式 $x_t = \sqrt{\bar{\alpha}_t}x_0 + \sqrt{1-\bar{\alpha}_t}\epsilon$。
- [ ] 4. 写出 DDPM 简化后的训练损失函数 $L_{simple}(\theta)$。
- [ ] 5. 说明为什么神经网络去预测噪声 $\epsilon$ 比直接预测干净图像 $x_0$ 效果更好。
- [ ] 6. 解释时间步 $t$ 是如何输入到 U-Net 中的（Time Embedding）。
- [ ] 7. 对比 GAN、VAE 与 Diffusion 的优缺点。
- [ ] 8. 解释什么是前向过程、什么是反向过程。
- [ ] 9. 手写 DDPM 前向加噪函数与损失计算代码。
- [ ] 10. 简述为什么 Stable Diffusion 需要结合 VAE（Latent Diffusion）。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | DDPM 前向加噪是否需要学习参数？ |
| 2 | 公式推导 | 基础 | 累乘因子 $\bar{\alpha}_t$ 的定义 |
| 3 | 条件判断 | 中等 | 为什么 DDPM 推理速度比 GAN 慢？ |
| 4 | 变式/综合 | 中等 | DDIM (Denoising Diffusion Implicit Models) 加速原理 |
| 5 | 开放/架构 | 较难 | 从贝叶斯展开推导反向条件分布均值 $\tilde{\boldsymbol{\mu}}_t$ |

### 题目与解析

#### 1. 关于 DDPM 前向加噪过程（Forward Process）的说法，正确的是？
- A. 前向过程包含大量卷积层需要反向传播训练
- B. 前向过程是预先定义好高斯噪声 Schedule 的无参数可学过程
- C. 前向过程的中间状态 $x_t$ 必须一步步循环计算得到
- D. 前向过程最终会把任何图像变成纯黑图像

> [!question]- 答案解析
> - **答案**：B
> - **解析**：前向加噪过程完全由预定义的超参数 $\beta_t$ 决定，不包含任何可学习参数；且由于高斯分布叠加性质，存在闭式解可直接一步计算 $x_t$。
> - **对应误区**：误区 1。

#### 2. 在 DDPM 中，为什么去噪网络 U-Net 除了输入带噪图像 $x_t$ 外，还必须显式输入时间步 $t$ (Time Embedding)？
> [!question]- 答案解析
> - **答案**：因为不同时间步 $t$ 下图像的加噪程度（信噪比 SNR）截然不同。
> - **解析**：当 $t$ 很小（如 $t=5$）时，图像只有微小噪声，网络需要预测细粒度高频细节噪声；当 $t$ 很大（如 $t=950$）时，图像几乎全为噪声，网络需要根据整体轮廓预测大格局噪声。时间步 Embedding 告知 U-Net 当前所处去噪阶段。

#### 3. DDIM (隐式扩散模型) 是如何将传统 DDPM 动辄 1000 步的采样过程缩短到 20-50 步的？
> [!question]- 答案解析
> - **答案**：将前向过程改为非马尔可夫链 (Non-Markovian)。
> - **解析**：DDIM 构建了一个具有相同边缘分布但非马尔可夫的前向加噪过程，使得反向采样变成确定性的日常常微分方程 (ODE) 轨迹，从而可以跳步（Sub-sampling）采样，仅用 20-50 步即可获得同等画质。

#### 4. 【推导】已知 $x_1 = \sqrt{\alpha_1}x_0 + \sqrt{1-\alpha_1}\epsilon_1$，且 $x_2 = \sqrt{\alpha_2}x_1 + \sqrt{1-\alpha_2}\epsilon_2$，其中 $\epsilon_1, \epsilon_2 \sim \mathcal{N}(0, \mathbf{I})$ 独立。证明 $x_2 = \sqrt{\alpha_1 \alpha_2}x_0 + \sqrt{1-\alpha_1 \alpha_2}\epsilon_{new}$。
> [!question]- 答案解析
> - **证明**：
>   将 $x_1$ 代入 $x_2$ 公式：
>   $$x_2 = \sqrt{\alpha_2}\left( \sqrt{\alpha_1}x_0 + \sqrt{1-\alpha_1}\epsilon_1 \right) + \sqrt{1-\alpha_2}\epsilon_2 = \sqrt{\alpha_1\alpha_2}x_0 + \sqrt{\alpha_2(1-\alpha_1)}\epsilon_1 + \sqrt{1-\alpha_2}\epsilon_2$$
>   两项独立高斯噪声相加：$\sqrt{\alpha_2(1-\alpha_1)}\epsilon_1 + \sqrt{1-\alpha_2}\epsilon_2$ 的方差为：
>   $$\text{Var} = \alpha_2(1-\alpha_1) + (1-\alpha_2) = \alpha_2 - \alpha_1\alpha_2 + 1 - \alpha_2 = 1 - \alpha_1\alpha_2$$
>   因此两项可合并为单个高斯噪声项 $\sqrt{1-\alpha_1\alpha_2}\epsilon_{new}$！
>   归纳即得前向闭式解 $x_t = \sqrt{\bar{\alpha}_t}x_0 + \sqrt{1-\bar{\alpha}_t}\epsilon$。证毕！

#### 5. 【开放/大模型迁移】在 Stable Diffusion (Latent Diffusion Model) 中，为什么不直接在 512x512 的像素空间跑 Diffusion，而是要先用 VAE 压缩到 64x64 的 Latent 空间？
> [!question]- 答案解析
> - **答案**：降低计算复杂度并去除高频不感知冗余。
> - **解析**：高分辨率像素空间存在海量感知不到的高频像素噪音，直接计算会导致 U-Net 的注意力与卷积开销按像素数 $O(H \times W)$ 呈二次方暴增。利用预训练 VAE 将空间维度压缩 8 倍（面积缩小 64 倍），在低维语义隐空间进行扩散去噪，极大地降低了显存需求并加快了训练/推理速度。

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

### 我的推导复现
> 不看上文，尝试写出核心公式或推导主线：

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
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🎯 VAE 变分自编码器 (Variational Autoencoder)]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/🎯 ResNet (残差网络)]]
  - LatentDiffusion
- **建议标签**：`#学习` `#深度学习` `#AIGC` `#Diffusion` `#DDPM` `#扩散模型` `#UNet`

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
