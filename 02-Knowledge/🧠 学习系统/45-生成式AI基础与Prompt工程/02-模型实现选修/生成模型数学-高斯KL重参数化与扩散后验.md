---
type: study
topic: "高斯 KL、重参数化与扩散后验"
course: "生成式AI基础与Prompt工程"
tags: [学习, 45-生成式AI基础与Prompt工程, 生成模型, 扩散模型]
created: 2026-08-05
status: completed
mastery: not_started
difficulty: advanced
stage_moc: "[[🧭 阶段2-模型实现选修]]"
concept: ["高斯KL散度", "重参数化", "扩散后验"]
prerequisites: ["课程前置-概率向量与Softmax最小补丁", "深度学习工程-PyTorch张量自动微分与训练循环"]
related: ["生成式AI-模型家族-VAE-GAN与扩散模型", "生成式AI-多模态-条件生成与基础模型"]
upstream: ["[[生成式AI-模型家族-VAE-GAN与扩散模型]]", "[[深度学习工程-PyTorch张量自动微分与训练循环]]"]
flow: knowledge
kind: derivation
source: "MIT OCW 6.7960 Deep Learning Fall 2024 Homework 5 and Lectures 14-16, CC BY-NC-SA 4.0"
source_url: "https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0"
anki_deck: "45-生成式AI基础与Prompt工程::生成模型数学"
anki_tags: [Gaussian, KL, VAE, Diffusion, Reparameterization]
---

# 生成模型数学：高斯 KL、重参数化与扩散后验

## 0. 学习边界

- **类别**：A 类（MIT 6.7960 HW5 Q1–Q12 的数学主卡）。
- **判断理由**：模型家族概览不足以完成高斯组合、KL 展开、反向条件分布和噪声参数化。本卡把 VAE 与 DDPM 共享的高斯工具完整串起。

## 1. 这个知识点解决什么问题？

> VAE 怎样对随机潜变量反向传播？扩散为什么能一步采到任意 $x_t$？已知 $x_t$ 和 $x_0$ 时，$x_{t-1}$ 的条件分布为什么仍是高斯？训练目标怎样化成噪声预测平方误差？

如果跳过方差、常数或条件变量，就无法判断公式对哪个随机变量成立，也无法实现正确的训练/采样过程。

## 2. 为什么它重要？它有什么用？

- **VAE**：闭式高斯 KL 与重参数化使 ELBO 可低方差优化。
- **扩散**：线性高斯马尔可夫链允许闭式前向采样和后验推导。
- **实现**：均值、方差、log-variance 和标准差混淆是常见静默错误。
- **作业定位**：支撑 MIT HW5 Q1–Q5、Q7–Q12/Q14。

## 3. 学它之前需要哪些前置知识？

1. 概率基础：独立变量、条件分布、期望和方差；若不会，先补 [[🗺️ 概率论与数理统计学习路径|概率论路径]]。
2. [[深度学习工程-PyTorch张量自动微分与训练循环]]：理解参数化分布、loss 和梯度路径。

## 4. 用直觉语言解释它

> “高斯像一团由中心和宽度决定的雾。VAE 把每个样本编码成一团雾；扩散则按计划不断把数据雾化，再学习每一步怎样去掉新增噪声。”

- 重参数化把“随机节点”改写成“固定参数的可导变换 + 参数无关噪声”。
- 线性组合的独立高斯仍是高斯，所以多步加噪可合并成一步。
- 两个关于同一变量的高斯密度相乘仍与一个高斯成比例，给出扩散后验。
- 一句话本质：**高斯闭包性把难处理的随机过程化为可计算的均值、方差和噪声预测。**

## 5. 正式定义、核心公式、符号解释

### 1. 高斯线性组合

若 $X\sim\mathcal N(\mu_X,\sigma_X^2)$、$Y\sim\mathcal N(\mu_Y,\sigma_Y^2)$ 独立，则

$$aX+bY\sim\mathcal N(a\mu_X+b\mu_Y,\ a^2\sigma_X^2+b^2\sigma_Y^2).$$

### 2. 对角高斯 KL

对 $q=\mathcal N(\mu_q,\operatorname{diag}(\sigma_q^2))$ 与
$p=\mathcal N(\mu_p,\operatorname{diag}(\sigma_p^2))$：

$$D_{KL}(q\Vert p)=\frac12\sum_i\left[
\log\frac{\sigma_{p,i}^2}{\sigma_{q,i}^2}
+\frac{\sigma_{q,i}^2+(\mu_{q,i}-\mu_{p,i})^2}{\sigma_{p,i}^2}-1
\right].$$

若 $p=\mathcal N(0,I)$，则

$$D_{KL}(q\Vert p)=\frac12\sum_i(\mu_i^2+\sigma_i^2-1-\log\sigma_i^2).$$

### 3. VAE 重参数化与 ELBO

$$\epsilon\sim\mathcal N(0,I),\qquad z=\mu_\phi(x)+\sigma_\phi(x)\odot\epsilon,$$
$$\mathcal L_{ELBO}=\mathbb E_{q_\phi(z|x)}[\log p_\theta(x|z)]-D_{KL}(q_\phi(z|x)\Vert p(z)).$$

实现常输出 `logvar`，使用 $\sigma=\exp(0.5\,\text{logvar})$；把 `logvar` 直接当标准差会错。

### 4. 扩散前向过程

令 $\alpha_t=1-\beta_t$，$\bar\alpha_t=\prod_{s=1}^t\alpha_s$：

$$q(x_t|x_{t-1})=\mathcal N(\sqrt{\alpha_t}x_{t-1},\beta_t I),$$
$$q(x_t|x_0)=\mathcal N(\sqrt{\bar\alpha_t}x_0,(1-\bar\alpha_t)I),$$
$$x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon,\quad\epsilon\sim\mathcal N(0,I).$$

### 5. 真实后验

$$q(x_{t-1}|x_t,x_0)=\mathcal N(\tilde\mu_t(x_t,x_0),\tilde\beta_t I),$$
$$\tilde\beta_t=\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\beta_t,$$
$$\tilde\mu_t=
\frac{\sqrt{\bar\alpha_{t-1}}\beta_t}{1-\bar\alpha_t}x_0
+\frac{\sqrt{\alpha_t}(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}x_t.$$

用 $x_0=(x_t-\sqrt{1-\bar\alpha_t}\epsilon)/\sqrt{\bar\alpha_t}$ 代入，可把均值写成噪声形式：

$$\mu_\theta(x_t,t)=\frac1{\sqrt{\alpha_t}}
\left(x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(x_t,t)\right).$$

常用简化训练目标为

$$\mathcal L_{simple}=\mathbb E_{x_0,t,\epsilon}
\|\epsilon-\epsilon_\theta(x_t,t)\|_2^2.$$

| 符号 | 含义 | 边界 |
| :--- | :--- | :--- |
| $\beta_t$ | 第 t 步噪声方差 | 通常在 $(0,1)$ |
| $\alpha_t$ | 信号保留率 $1-\beta_t$ | 不是累计量 |
| $\bar\alpha_t$ | 从 1 到 t 的累计乘积 | 随 t 通常下降 |
| $\tilde\beta_t$ | 条件后验方差 | 不等于简单的 $\beta_t$ |
| $\epsilon_\theta$ | 网络预测噪声 | 输入需含时间 t |

## 6. 推导思路和思想来源

### 1. 多步前向闭式

把 $x_t=\sqrt{\alpha_t}x_{t-1}+\sqrt{\beta_t}\epsilon_t$ 递归代入。信号系数相乘成 $\sqrt{\bar\alpha_t}$；独立高斯噪声方差相加，得到 $1-\bar\alpha_t$。

### 2. 后验均值

利用 Bayes 比例：

$$q(x_{t-1}|x_t,x_0)\propto q(x_t|x_{t-1})q(x_{t-1}|x_0).$$

对 $x_{t-1}$ 展开两个高斯指数中的二次项，合并 $x_{t-1}^2$ 系数得到精度，合并一次项后除以精度得到 $\tilde\mu_t$。归一化常数与 $x_{t-1}$ 无关，但在完整 KL 数值中不能随意丢失。

### 3. 噪声参数化

由闭式前向表达解出 $x_0$，代入后验均值；用网络预测真实采样噪声 $\epsilon$。固定或已知方差时，两个高斯的 KL 对均值差是加权平方误差，因此得到噪声预测 MSE（严格 ELBO 的时间权重与简化目标可不同）。

### 4. 重参数化

原本 $z\sim q_\phi(z|x)$ 的采样分布依赖 $\phi$。改写为参数无关 $\epsilon$ 经过可导变换后，可把梯度移入期望并对 $\mu_\phi,\sigma_\phi$ 反传。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

若 $q=\mathcal N(1,4)$、$p=\mathcal N(0,1)$，一维 KL 为
$\frac12(1^2+4-1-\log4)\approx1.3069$，非负且方向不对称。

### 例子 2：中等例子

$\alpha_1=0.9,\alpha_2=0.8$，则 $\bar\alpha_2=0.72$。无需先生成 $x_1$，可直接采
$x_2=\sqrt{0.72}x_0+\sqrt{0.28}\epsilon$。这允许训练时随机抽一个时间步。

### 例子 3：实际应用例子（可运行 Python）

```python
# 输入：一维高斯和两步噪声日程；输出：KL、x_t 与真实后验参数。
import math

def gaussian_kl(mu_q, var_q, mu_p=0.0, var_p=1.0):
    return 0.5 * (math.log(var_p / var_q) + (var_q + (mu_q - mu_p) ** 2) / var_p - 1)

def q_sample(x0, alpha_bar, noise):
    return math.sqrt(alpha_bar) * x0 + math.sqrt(1 - alpha_bar) * noise

def posterior(x0, xt, alpha_t, alpha_bar_t, alpha_bar_previous):
    beta_t = 1 - alpha_t
    variance = beta_t * (1 - alpha_bar_previous) / (1 - alpha_bar_t)
    mean = (
        math.sqrt(alpha_bar_previous) * beta_t / (1 - alpha_bar_t) * x0
        + math.sqrt(alpha_t) * (1 - alpha_bar_previous) / (1 - alpha_bar_t) * xt
    )
    return mean, variance

alpha1, alpha2 = 0.9, 0.8
alpha_bar2 = alpha1 * alpha2
x0, noise = 1.0, 0.25
x2 = q_sample(x0, alpha_bar2, noise)
mean, variance = posterior(x0, x2, alpha2, alpha_bar2, alpha1)
print(round(gaussian_kl(1.0, 4.0), 4), round(x2, 4), round(mean, 4), round(variance, 4))
assert gaussian_kl(0.0, 1.0) == 0.0
assert variance > 0.0
```

## 8. 常见误区和易混概念

- **误区 1**：方差、标准差、log-variance 可互换。它们分别是 $\sigma^2$、$\sigma$、$\log\sigma^2$。
- **误区 2**：$D_{KL}(q\Vert p)=D_{KL}(p\Vert q)$。KL 有方向，交换后权重和期望分布变化。
- **误区 3**：$\alpha_t$ 与 $\bar\alpha_t$ 是同一个量。后者是从 1 到 t 的乘积。
- **误区 4**：简化噪声 MSE 就是逐项完全相等的 ELBO。常见简化会重加权或固定方差。
- **误区 5**：训练去噪一步就能从纯噪声生成。标准 DDPM 采样仍按多个反向时间步迭代。

| 概念 | 条件变量 | 作用 | 关键区别 |
| :--- | :--- | :--- | :--- |
| $q(x_t|x_0)$ | 已知干净样本 | 训练时直接加噪 | 可跨多步闭式采样 |
| $q(x_{t-1}|x_t,x_0)$ | 已知 $x_t,x_0$ | 真实后验/训练推导 | 采样时 $x_0$ 未知 |
| $p_\theta(x_{t-1}|x_t)$ | 只知 $x_t$ | 学习的反向过程 | 用网络近似后验均值/噪声 |
| VAE 重参数化 | 潜变量 $z$ | 低方差反传 | 单次潜变量而非时间链 |

## 9. 课程连接

- [[生成式AI-模型家族-VAE-GAN与扩散模型]] 给出 VAE/扩散的宏观位置，[[深度学习工程-PyTorch张量自动微分与训练循环]] 提供实现与梯度边界。
- [[课程前置-概率向量与Softmax最小补丁]] 只提供最小概率直觉；若无法独立展开高斯条件分布，应返回正式概率论课程补学。
- [[生成式AI-多模态-条件生成与基础模型]] 使用这些机制，但 Prompt 主线不要求先完成本卡推导。

## 10. 闭卷复现任务

- [ ] 写出独立高斯线性组合的均值和方差。
- [ ] 写出两个对角高斯的 KL。
- [ ] 化简到标准正态先验的 KL。
- [ ] 解释 VAE 重参数化的梯度路径。
- [ ] 区分 variance、std 和 logvar。
- [ ] 从递推写出 $q(x_t|x_0)$。
- [ ] 写出 $\bar\alpha_t$ 定义。
- [ ] 用两个高斯密度相乘说明后验仍为高斯。
- [ ] 写出 $\tilde\mu_t$ 与 $\tilde\beta_t$。
- [ ] 从 $x_t$ 解出 $x_0$ 并说明噪声 MSE 的来源。

## 11. 自测题：5 道

1. 两个独立标准高斯相加的方差是多少？ `#自测题/基础`
2. 当 $q=p$ 时 KL 为何为 0？ `#自测题/基础`
3. 网络输出 `logvar=0` 时标准差是多少？ `#自测题/中等`
4. 给定 $\alpha_1=0.9,\alpha_2=0.8$，写出 $x_2$ 的直接采样式。 `#自测题/中等`
5. 从 Bayes 比例展开一维 $q(x_{t-1}|x_t,x_0)$ 的二次项，恢复后验精度、均值和方差。 `#自测题/较难`

> [!question]- 参考答案与评分点
> 1. 2。2. 均值差为 0、方差比为 1，各项抵消。3. $\exp(0/2)=1$。4. $x_2=\sqrt{0.72}x_0+\sqrt{0.28}\epsilon$。5. 明确两个似然的精度相加，一次项相加后除以总精度；结果应等于第 5 节的 $\tilde\mu_t,\tilde\beta_t$。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/45-生成式AI基础与Prompt工程"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 12. 我的主动回忆区

- **高斯 KL**：
- **前向闭式**：
- **后验推导卡点**：
- [ ] 明天  [ ] 3 天后  [ ] 7 天后  [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- 本卡保留一条完整的 VAE/扩散高斯推导链；模型家族卡继续负责宏观比较。
- 做 HW5 时先在一维标量上核对均值与方差，再迁移到 batch、channel 和 image shape。

## 🃏 Anki 卡片

Q: 扩散前向过程怎样一步采样任意 $x_t$？
A: $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$，其中 $\bar\alpha_t=\prod_{s=1}^t\alpha_s$。

Q: VAE 为什么使用重参数化？
A: 将依赖参数的随机采样改写为参数无关噪声经过可导变换，使梯度可对均值和方差参数反传。

