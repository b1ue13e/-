---
type: study
course: "05-计算机视觉"
topic: "生成模型：GAN与Diffusion"
created: 2026-08-05
status: ongoing
difficulty: advanced
concept: ["生成模型","GAN","Diffusion","生成器","判别器","去噪"]
prerequisites: ["卷积神经网络CNN","反向传播"]
related: ["VAE","StableDiffusion","自监督学习"]
flow: knowledge
upstream: ["[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/卷积神经网络CNN]]", "[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/反向传播与计算图]]", "[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/Softmax与SVM损失函数]]"]
stage_moc: "[[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🚀 第四阶段：前沿架构探索]]"
kind: concept
source: "D2L Ch.17; CS231n A3"
anki_deck: "05-计算机视觉::04-前沿架构探索"
anki_tags: ["计算机视觉","生成模型","GAN","Diffusion"]
tags: [学习,计算机视觉,生成模型,GAN,Diffusion]
---

# 🔷 生成模型：GAN 与 Diffusion

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：生成模型是深度学习从"判别"走向"创造"的分水岭。GAN（Goodfellow et al., 2014）首次用对抗博弈实现逼真的单步图像生成；Diffusion（Ho et al., 2020 的 DDPM）以热力学扩散的严谨框架，一举解决 GAN 训练不稳定与模式崩溃，成为 Stable Diffusion、Midjourney、DALL·E 3、Sora 的共同底层引擎。不搞懂 minimax 博弈与加噪-去噪范式，就无法进入生成式 AI。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem**：
> 判别模型只能学习 $P(Y|X)$——给定图判断是猫是狗。若要**从无到有创造全新图像**，必须学习数据本身的联合分布 $P(X)$。直接在高维像素空间（$\sim 200,000$ 维）精确建模 $P(X)$ 极其困难——分布高度复杂、非凸、结构化。核心困难：(1) 如何定义"像不像真的"——MSE 不懂语义；(2) 如何在高维空间中稳定采样。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：GAN 用判别器充当"可学习的损失函数"，Diffusion 用马尔可夫链将单步生成分解为千步去噪——两种思路深刻影响了所有后续生成式架构。
- **实际应用**：文本到图像生成（Stable Diffusion / Midjourney / DALL·E）、图像超分与修复、风格迁移（CycleGAN / pix2pix）、DeepFake、药物分子与蛋白质生成、视频生成（Sora）。
- **高频考点**：写出 GAN minimax 公式并解释每项、推导 DDPM 前向闭式解 $x_t = \sqrt{\bar{\alpha}_t}x_0 + \sqrt{1-\bar{\alpha}_t}\epsilon$、解释 non-saturating loss 的梯度动机、对比四类生成模型。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[卷积神经网络CNN]]**：GAN 的生成器用转置卷积上采样，判别器用 Strided Conv 下采样；Diffusion 的 U-Net 大量使用卷积与残差块。
2. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/反向传播与计算图]]与梯度下降**：GAN 交替训练需理解梯度如何从 $D$ 穿过 $G$、何时冻结谁。
3. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/Softmax与SVM损失函数|交叉熵 / BCE 损失]]**：GAN 判别器做二分类——不理解 BCE 就读不懂 minimax 公式。
4. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🎯 VAE 变分自编码器 (Variational Autoencoder)]]（建议了解）**：VAE 用显式编码-解码 + KL 散度做生成，是理解 GAN 和 Diffusion 的重要参照系——Diffusion 本质是 $T$ 步深度 VAE。
5. **[[02-Knowledge/🧠 学习系统/24-随机过程/02-马尔可夫与泊松过程/马尔可夫与泊松过程-应用入口-1]]**：Diffusion 的前向与反向过程都是马尔可夫链。

---

## 4. 用直觉语言解释它

> «"这东西其实就像……"»

### GAN：造假钞的骗子 vs 验钞机

- **生成器 $G$（骗子）**：输入噪声 $z$，输出假钞，一开始像废纸。
- **判别器 $D$（验钞机）**：输入钞票，输出真伪概率，不断学习鉴别。
- **对抗博弈**：骗子根据验钞机反馈改进；验钞机不断升级。魔高一尺道高一丈。
- **最终纳什均衡**：假钞与真钞一模一样，验钞机只能瞎猜 50%。$G$ 即为完美生成器！
- **一句话直觉**：用可学习的判别器替代人工设计的损失函数——让网络自己学会"什么叫像真的"。

### Diffusion：雕刻大师恢复被风化的雕像

- **前向（毁坏/加噪）**：精美雕像（高清图 $x_0$），每天泼强酸（加高斯噪声），持续 1000 天 → 彻底风化成沙尘（纯噪声 $x_T$）。
- **反向（雕刻/去噪）**：训练神经网络雕刻师，给它看第 $t$ 天沙尘，让它**预测"昨天落下了哪些沙尘（噪声 $\epsilon$）"**——学会去噪就能步步恢复。
- **生成新图像**：随机抓纯沙尘 $x_T$，雕刻师倒退 1000 步 → 全新雕像诞生！
- **一句话直觉**：把困难的"一步生成"分解为 1000 步"微小去噪"——每一步只需做非常简单的事。

---

## 5. 正式定义、核心公式、符号解释

### 5.1 四大流派总览

| 流派 | 建模 | 目标 | 优缺点 |
| :--- | :--- | :--- | :--- |
| **自回归** | $P(x)=\prod_i P(x_i\mid x_{\lt i})$ | 最大似然 | 似然精确，采样逐token慢 |
| **VAE** | $P(x)=\int P(x\mid z)P(z)dz$ | ELBO | 训练稳定、隐空间连续，但模糊 |
| **GAN** | 隐式分布（无显式 $P(x)$） | Minimax 对抗 | 高清逼真，但不稳定、模式崩溃 |
| **Diffusion** | 马尔可夫链逐步去噪 | MSE（去噪得分匹配） | 训练极稳、质量顶级，但采样慢 |

### 5.2 GAN：Minimax 博弈

$G(\mathbf{z})$：噪声 $\mathbf{z} \sim p_z$ → 假样本。$D(\mathbf{x})$：样本 → $[0, 1]$ 为真概率。

$$\min_G \max_D \; \mathbb{E}_{\mathbf{x} \sim p_{\text{data}}}[\log D(\mathbf{x})] + \mathbb{E}_{\mathbf{z} \sim p_z}[\log(1 - D(G(\mathbf{z})))]$$

- 第1项：$D$ 想给真样本打高分 → $\max_D$
- 第2项：$D$ 想让 $D(G) \to 0$（此项 $\to 0$）→ $\max_D$；$G$ 想让 $D(G) \to 1$（此项 $\to -\infty$）→ $\min_G$

**交替训练**：每次迭代先训 $D$（$k$ 步，真→1/假→0，$G$ 冻结），再训 $G$（1 步，non-saturating: 最大化 $\log D(G)$，$D$ 冻结）。

### 5.3 GAN 训练不稳定原因

1. **梯度消失**：$G$ 弱时 $D(G)\approx 0$，原始 $\log(1-D(G))$ 梯度极平 → **non-saturating loss** 改为最大化 $\log D(G)$，初期梯度大。
2. **模式崩溃**：$G$ 发现几种"安全输出"能骗 $D$ 就只生成这些——minimax 对分布覆盖无显式约束。
3. **不收敛/振荡**：追不断变化的鞍点，$D$ 太强 → $G$ 梯度消失，$G$ 太强 → $D$ 梯度无意义。
4. **判别器崩塌**：$D$ 完美区分（loss→0）→ $G$ 梯度为零；均衡时 $D$ 恒输出 0.5，loss $\approx 1.38$。

### 5.4 DDPM：前向加噪 + 反向去噪

#### 前向加噪（固定，不可学）

$T$ 步马尔可夫链：$q(\mathbf{x}_t \mid \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1 - \beta_t}\,\mathbf{x}_{t-1}, \beta_t \mathbf{I})$，$\beta_t \in (0, 1)$ 预设递增（如 $10^{-4} \to 0.02$）。

**重参数化与闭式解**：令 $\alpha_t = 1 - \beta_t$，$\bar{\alpha}_t = \prod_{s=1}^{t} \alpha_s$。利用高斯可加性压缩 $T$ 步为一步：

$$\boxed{\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\,\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\,\boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(0, \mathbf{I})}$$

重参数化将随机性 $\boldsymbol{\epsilon}$ 抽离为确定性变换，使梯度可穿过采样回传。$t=0$：$\bar{\alpha}_0=1$ → 原图；$t \to T$：$\bar{\alpha}_T \to 0$ → 纯噪声。

#### 反向去噪（神经网络拟合）

$\boldsymbol{\epsilon}_{\theta}(\mathbf{x}_t, t)$ 预测噪声后推导 $\mathbf{x}_{t-1}$：

$$p_{\theta}(\mathbf{x}_{t-1} \mid \mathbf{x}_t) = \mathcal{N}\left(\mathbf{x}_{t-1}; \frac{1}{\sqrt{\alpha_t}}\left(\mathbf{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}}\boldsymbol{\epsilon}_{\theta}(\mathbf{x}_t, t)\right), \sigma_t^2 \mathbf{I}\right)$$

#### 核心训练目标

经 ELBO 展开化简后，Ho et al. (2020) 发现最简单的 MSE 效果最好：

$$\boxed{L_{\text{simple}}(\theta) = \mathbb{E}_{t, \mathbf{x}_0, \boldsymbol{\epsilon}}\left[\left\|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_{\theta}\left(\sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\boldsymbol{\epsilon},\; t\right)\right\|^2\right]}$$

随机选 $\mathbf{x}_0, t, \boldsymbol{\epsilon}$ → 闭式解生成 $\mathbf{x}_t$ → U-Net 预测噪声 → MSE。极其优雅！

### 5.5 符号说明表

| 符号 | 含义 | 维度 / 范围 | 备注 |
| :--- | :--- | :--- | :--- |
| $\mathbf{x}_0$ | 原始真实图像 | $\mathbb{R}^{C \times H \times W}$ | 训练集干净样本 |
| $\mathbf{x}_t$ | 第 $t$ 步加噪图像 | $\mathbb{R}^{C \times H \times W}$ | $t=T$ 时近似纯噪声 |
| $\mathbf{z}$ | GAN 隐空间噪声 | $\mathbb{R}^{d_z}$，$\sim \mathcal{N}(0, \mathbf{I})$ | 生成器输入 |
| $G(\mathbf{z})$ | 生成器输出 | $\mathbb{R}^{C \times H \times W}$ | 生成的假图像 |
| $D(\mathbf{x})$ | 判别器输出 | $[0, 1]$ | 判别为真的概率 |
| $\beta_t$ | 第 $t$ 步噪声方差 | $(0, 1)$，如 $10^{-4} \to 0.02$ | 预设超参数 |
| $\bar{\alpha}_t$ | 累乘衰减系数 | $\prod_{s=1}^t (1-\beta_s)$ | 控制信号残留比 |
| $\boldsymbol{\epsilon}$ | 标准高斯噪声 | $\sim \mathcal{N}(0, \mathbf{I})$ | 前向加的噪声，反向预测目标 |
| $\boldsymbol{\epsilon}_{\theta}$ | 去噪 U-Net 网络 | $\mathbb{R}^{C \times H \times W}$ | 输入加噪图 + 时间步，预测噪声 |
| $T$ | 扩散总步数 | 典型值 1000 | DDPM 使用 $T=1000$ |

---

## 6. 推导思路和思想来源

### GAN 的推导

- **困难**：如何定义"像不像真的"？MSE 像素空间无意义。
- **转念（Goodfellow, 2014）**：让神经网络当损失函数！$D$ 学习区分真假，$G$ 骗过 $D$——通过对抗**隐式**逼近 $p_{\text{data}}$。
- **数学本质**：GAN 目标函数即二元交叉熵。当 $D$ 最优时 $D^*(x) = \frac{p_{\text{data}}(x)}{p_{\text{data}}(x) + p_g(x)}$，$G$ 的目标等价于最小化 Jensen-Shannon 散度。

### DDPM 的推导

- **困难**：反向 $q(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$ 不可解（需不可知的 $q(\mathbf{x}_{t-1})$）。
- **转念 1**：条件于 $\mathbf{x}_0$ 后 $q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)$ 是精确可解的高斯！贝叶斯展开：
  $$q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0) = q(\mathbf{x}_t \mid \mathbf{x}_{t-1}) \cdot \frac{q(\mathbf{x}_{t-1} \mid \mathbf{x}_0)}{q(\mathbf{x}_t \mid \mathbf{x}_0)}$$
  三项已知高斯 → 代入展开得均值闭式解。
- **转念 2**：均值公式中唯一未知是前向噪声 $\boldsymbol{\epsilon}$ → **神经网络只需预测噪声**，将复杂生成降维为简单去噪回归！
- **闭式解来源**：高斯叠加——$\mathbf{x}_1 = \sqrt{\alpha_1}\mathbf{x}_0 + \sqrt{1-\alpha_1}\boldsymbol{\epsilon}_1$ 代入 $\mathbf{x}_2$，独立噪声方差相加 $\alpha_2(1-\alpha_1)+(1-\alpha_2)=1-\alpha_1\alpha_2$，归纳得 $\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t}\boldsymbol{\epsilon}$。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础 — 手算 GAN 最优判别器

**题目**：$p_{\text{data}}$ 在 $\{0, 1\}$ 上，$P(X=0)=0.3$，$P(X=1)=0.7$。$G$ 固定输出 $p_g$：$P(G=0)=0.6$，$P(G=1)=0.4$。求 $D^*(1)$。

**解答**：
$$D^*(x) = \frac{p_{\text{data}}(x)}{p_{\text{data}}(x) + p_g(x)} \;\Longrightarrow\; D^*(1) = \frac{0.7}{0.7 + 0.4} \approx 0.636$$

- **🤔 追问**：$D(1)=0.636$ 意味着什么？
  - *答*：当 $D$ 看到 $x=1$ 时，估计它有 63.6% 的概率来自真实分布——因为真分布更倾向 $x=1$（70% vs 40%）。

### 例子 2：中等 — 推导前向加噪闭式解（归纳法）

**题目**：已知 $\mathbf{x}_t = \sqrt{\alpha_t}\mathbf{x}_{t-1} + \sqrt{1-\alpha_t}\boldsymbol{\epsilon}_t$，各步噪声独立。证明 $\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t}\boldsymbol{\epsilon}$。

**推导**：$t=1$ 成立。设 $t-1$ 成立，代入：
$$\mathbf{x}_t = \sqrt{\alpha_t}\left(\sqrt{\bar{\alpha}_{t-1}}\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_{t-1}}\boldsymbol{\epsilon}_{\text{prev}}\right) + \sqrt{1-\alpha_t}\boldsymbol{\epsilon}_t$$
$$= \sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \underbrace{\sqrt{\alpha_t(1-\bar{\alpha}_{t-1})}\boldsymbol{\epsilon}_{\text{prev}} + \sqrt{1-\alpha_t}\boldsymbol{\epsilon}_t}_{\text{两独立高斯合并}}$$

合并方差：$\alpha_t(1-\bar{\alpha}_{t-1}) + (1-\alpha_t) = 1 - \alpha_t\bar{\alpha}_{t-1} = 1 - \bar{\alpha}_t$。故可写为 $\sqrt{1-\bar{\alpha}_t}\,\boldsymbol{\epsilon}_{\text{new}}$。证毕！

### 例子 3：DCGAN 训练循环（PyTorch）

```python
# 网络: G = ConvTranspose+BN+ReLU→Tanh; D = Conv+LeakyReLU+Sigmoid
G, D = Generator(z_dim=100).cuda(), Discriminator().cuda()
opt_G = torch.optim.Adam(G.parameters(), lr=2e-4, betas=(0.5, 0.999))
opt_D = torch.optim.Adam(D.parameters(), lr=2e-4, betas=(0.5, 0.999))
BCE = nn.BCELoss()

for real, _ in dataloader:
    bs = real.size(0)
    # 训 D: 真→1, 假→0 (G 冻结 via detach)
    z = torch.randn(bs, 100).cuda()
    loss_D = (BCE(D(real), torch.ones(bs).cuda()) +
              BCE(D(G(z).detach()), torch.zeros(bs).cuda())) / 2
    opt_D.zero_grad(); loss_D.backward(); opt_D.step()

    # 训 G (non-saturating): 让 D(假)→1 (D 冻结)
    z = torch.randn(bs, 100).cuda()
    loss_G = BCE(D(G(z)), torch.ones(bs).cuda())
    opt_G.zero_grad(); loss_G.backward(); opt_G.step()
```

### 例子 4：DDPM 训练与采样

```python
class DDPM:
    def __init__(self, T=1000, b1=1e-4, bT=0.02):
        self.betas = torch.linspace(b1, bT, T)
        self.alphas = 1. - self.betas
        self.a_cum = torch.cumprod(self.alphas, dim=0)
        self.sqrt_a = torch.sqrt(self.a_cum)
        self.sqrt_1m = torch.sqrt(1. - self.a_cum)

    def q_sample(self, x0, t, noise=None):       # 前向闭式加噪
        if noise is None: noise = torch.randn_like(x0)
        a = self.sqrt_a[t].view(-1,1,1,1); b = self.sqrt_1m[t].view(-1,1,1,1)
        return a*x0 + b*noise, noise

    def train_step(self, model, x0):              # 训练: 预测噪声 MSE
        t = torch.randint(0, len(self.betas), (x0.size(0),), device=x0.device)
        xt, noise = self.q_sample(x0, t)
        return F.mse_loss(model(xt, t), noise)

    @torch.no_grad()
    def p_sample(self, model, xt, t, idx):        # 单步反向去噪
        at, ab = self.alphas[idx], self.a_cum[idx]
        pred = model(xt, t)
        mean = (xt - (1-at)/torch.sqrt(1-ab)*pred) / torch.sqrt(at)
        if idx == 0: return mean
        return mean + torch.sqrt(self.betas[idx]) * torch.randn_like(xt)
```

---

### 7.5 Textual Inversion：用文本向量学习新概念

**问题**：SD/扩散模型只能生成预训练时见过的概念——想生成"我家猫"或某个特定艺术风格，没有对应 token。

**思路（Textual Inversion, Gal et al., 2022）**：不微调模型权重，只学一个**新文本嵌入向量** $v_*$（≈ 新伪 token `<cat-of-mine>`），冻结 U-Net 与 text encoder 其余参数，用少量目标图像（3-5 张）优化：

$$v_* = \arg\min_v \; \mathbb{E}_{z_t, t, \epsilon} \left\lVert \epsilon - \epsilon_\theta(z_t, t, \text{cond}(v)) \right\rVert^2$$

（即标准扩散去噪损失，唯一可训练变量是条件中的文本嵌入。）

**训练后**：输入 prompt `"a photo of <cat-of-mine> in the park"` 就能生成"我家猫在公园"——新概念被"写进"了文本空间，无需修改模型。

**相关方法**：
- **DreamBooth**：微调整个扩散模型，概念保真度更高但会"遗忘"原模型能力（需 prior preservation）；
- **LoRA/ControlNet 风格的轻量微调**：控制生成结构/风格；
- Textual Inversion 最轻量（只学 ~768 维向量），适合风格迁移与个性化，但表达能力有限（无法学复杂姿态）。

## 8. 常见误区和易混概念

### 误区 1：GAN 训练到最后，判别器 loss 越小越好
- **错误**：训练分类器 loss 越小越好。**真相**：$D$ loss→0 意味着 $G$ 收不到有效梯度。理想纳什均衡下 $D$ 恒输出 0.5，loss $\approx 1.38$。训练失衡信号：$D$ 持续降而 $G$ 不降。

### 误区 2：自回归（Autoregressive）和自注意力（Self-Attention）是一回事
- **澄清**：自回归是逐 token 生成范式（PixelCNN, GPT），自注意力是序列内交互机制（Transformer）。中文翻译带"自"字但完全无关。

### 误区 3：Diffusion 的反向去噪可以一步到位
- **错误**：前向有闭式解一步 $x_0 \to x_T$，反向也该一步。**真相**：前向是线性高斯叠加，反向对应非线性流形逆映射，必须多步（50~1000）微分迭代。

### 误区 4：GAN 的 non-saturating loss 只是"工程 hack"
- **澄清**：虽最大化 $\log D(G)$ 偏离理论 minimax，但在最优解处等价。它解决了训练初期梯度消失，是理论与实践的必要调和。

### 概念对比表：GAN vs Diffusion

| 维度 | GAN | Diffusion (DDPM) |
| :--- | :--- | :--- |
| **生成** | 单步 $\mathbf{z} \to G(\mathbf{z})$ | $T$ 步迭代去噪 |
| **目标** | Minimax 对抗（BCE） | MSE（预测噪声） |
| **稳定性** | 极不稳定——振荡、模式崩溃 | **极稳定**——MSE 天然收敛 |
| **质量** | 极高 | **顶级超高清** |
| **多样性** | 不足（模式崩溃） | **极好** |
| **采样** | **1 步**（实时） | 50~1000 步（需加速） |
| **理论** | 博弈论 + JS 散度 | 非平衡热力学 + 得分匹配 |
| **可控** | 需额外设计（cGAN） | 天然支持条件注入 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游
- [[卷积神经网络CNN]]、[[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🎯 VAE 变分自编码器 (Variational Autoencoder)]]、[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/Softmax与SVM损失函数|BCE]]、[[02-Knowledge/🧠 学习系统/24-随机过程/02-马尔可夫与泊松过程/马尔可夫与泊松过程-应用入口-1]]

### 下游
- StableDiffusion（Latent Diffusion + 文本条件）、ControlNet（空间可控）、StyleGAN（GAN 最高形态）、CycleGAN（无配对域翻译）

### 横向
- [[自监督学习SimCLR与CLIP|CLIP]]：SD 文本条件核心编码器；[[LoRA]]：扩散模型低秩微调
- **范式转移**：GAN（对抗式隐式建模）→ Diffusion（逐步去噪显式建模）→ Flow Matching（新前沿）

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清生成模型与判别模型的根本区别。
- [ ] 2. 用"造假钞 vs 验钞机"类比解释 GAN 的对抗博弈。
- [ ] 3. 写出 GAN 的 minimax 目标函数，解释 $\max_D$ 和 $\min_G$ 各自追求什么。
- [ ] 4. 简述 GAN 两阶段交替训练流程（$D$ 和 $G$ 各做什么、何时冻结对方）。
- [ ] 5. 解释 GAN 模式崩溃的原因及 non-saturating loss 解决的问题。
- [ ] 6. 用"风化雕像逆向恢复"类比解释 Diffusion 的前向加噪和反向去噪。
- [ ] 7. 写出 DDPM 前向闭式解公式，说明重参数化技巧如何使梯度可回传。
- [ ] 8. 写出 $L_{\text{simple}}$，解释为什么预测噪声比直接预测 $x_0$ 更好。
- [ ] 9. 列出四类生成模型（自回归/VAE/GAN/Diffusion）并对比优劣。
- [ ] 10. 对比 GAN 和 Diffusion 的训练稳定性、生成质量与采样速度。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | GAN 的纳什均衡状态 |
| 2 | 公式解读 | 基础 | DDPM 前向闭式解含义 |
| 3 | 条件判断 | 中等 | GAN 训练失衡诊断 |
| 4 | 计算推导 | 中等 | 前向加噪的高斯方差合并 |
| 5 | 综合对比 | 较难 | GAN vs Diffusion 范式差异 |

### 题目与解析

#### 1. 当 GAN 达到完美纳什均衡时，判别器对任意输入的输出应接近多少？
- A. 真图→1，假图→0  B. 真图→0.5，假图→0  C. 所有输入→0.5  D. 所有输入→1.0

> [!question]- 答案解析
> - **答案**：C。纳什均衡下 $p_g = p_{\text{data}}$，$D^*(x) = \frac{p_{\text{data}}}{p_{\text{data}} + p_g} = 0.5$。

#### 2. DDPM 前向公式 $\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t}\boldsymbol{\epsilon}$ 中，$t=0$ 和 $t=T$ 时分别化简为什么？

> [!question]- 答案解析
> - $t=0$：$\bar{\alpha}_0=1$ → $\mathbf{x}_0=\mathbf{x}_0$（原图）。$t=T$：$\bar{\alpha}_T\to 0$ → $\mathbf{x}_T\approx\boldsymbol{\epsilon}$（纯噪声）。$\bar{\alpha}_t$ 平滑过渡即 noise schedule 核心。

#### 3. 训练 GAN 时，判别器 loss 迅速降至 0.01，生成器 loss 持续上升。最可能的诊断？
- A. 训练良好  B. 判别器太强  C. 生成器已收敛  D. 需增大 D 学习率

> [!question]- 答案解析
> - **答案**：B。$D$ 完美区分 → $D(G(z))\approx 0$ → Sigmoid 饱和 → $G$ 梯度为零。需削弱 $D$ 或增强 $G$ 训练频率。

#### 4. 证明 $\mathbf{x}_2 = \sqrt{\alpha_1\alpha_2}\mathbf{x}_0 + \sqrt{1-\alpha_1\alpha_2}\,\boldsymbol{\epsilon}_{\text{new}}$（已知单步加噪公式）。

> [!question]- 答案解析
> - 代入 $\mathbf{x}_1$ 得 $\mathbf{x}_2 = \sqrt{\alpha_1\alpha_2}\mathbf{x}_0 + \sqrt{\alpha_2(1-\alpha_1)}\boldsymbol{\epsilon}_1 + \sqrt{1-\alpha_2}\boldsymbol{\epsilon}_2$。两独立高斯方差相加：$\alpha_2(1-\alpha_1)+(1-\alpha_2)=1-\alpha_1\alpha_2$。合并即得，归纳至 $T$ 步得 DDPM 闭式解。

#### 5. 从训练目标、生成机制和推理效率对比 GAN 和 Diffusion。为什么 Diffusion 取代 GAN 成为 AIGC 主流？

> [!question]- 答案解析
> - **训练**：GAN = 鞍点优化不保证收敛；Diffusion = MSE 凸优化稳定收敛。
> - **机制**：GAN = 单步前向；Diffusion = $T$ 步迭代去噪。
> - **效率**：GAN 完胜（1 vs 50~1000 步）。
> - **胜出原因**：AIGC 时代质量与多样性优先——Stable Diffusion 经 Latent Diffusion + DDIM 压至 20~50 步后可接受。GAN 的模式崩溃与训练不稳定在大规模多类别上无解；Diffusion 的 MSE 训练极稳定且易扩展（文本条件、空间控制、LoRA）。

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

- **归档目录**：`04-前沿架构探索/`（已在此）
- **建议双链**：
  - 生成模型GAN与Diffusion — 可拆分的细节卡（训练技巧、WGAN、LSGAN 等变体）
  - [[🎯 Diffusion 扩散模型 (DDPM)|Diffusion (DDPM)]] — 可拆分的细节卡（完整推导、DDIM 加速）
  - StableDiffusion — Diffusion 工业落地形态（Latent Diffusion + 文本条件）
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/🎯 VAE 变分自编码器 (Variational Autoencoder)]] — 共同参照系
  - ControlNet — Diffusion 空间可控生成延伸
  - [[LoRA]] — 扩散模型低秩微调
  - [[自监督学习SimCLR与CLIP|CLIP]] — Stable Diffusion 文本条件核心编码器
  - [[Transformer与自注意力]] — DiT (Diffusion Transformer) 连接点
- **建议标签**：`#学习` `#计算机视觉` `#生成模型` `#GAN` `#Diffusion` `#DDPM` `#AIGC`
- **拆分建议**：本卡为概念主卡，覆盖 GAN 与 Diffusion 的核心对比。后续可拆分 GAN 稳定性专题（WGAN/WGAN-GP）、Diffusion 加速专题（DDIM/DPM-Solver）、Flow Matching 新范式。

---
---

## 学完后可以完成

- [[03-Projects/05-计算机视觉/大作业/05-计算机视觉-大作业-开放课程项目|HW06]]：

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
