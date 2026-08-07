---
type: study
topic: "变分推断 (Variational Inference & ELBO)"
course: "14-概率图模型"
created: 2026-07-27
status: learning
stage_moc: "[[🧭 阶段2-推断算法]]"
flow: knowledge
kind: derivation
difficulty: advanced
upstream: ["[[概率图模型-贝叶斯网络]]", "[[概率图模型-KL散度]]"]
importance: "A"
anki_deck: "概率图模型::02-推断算法"
anki_tags: [概率图模型, 变分推断, ELBO]
tags: [学习, 概率图模型, 变分推断, VI, ELBO, 证据下界, KL散度, 贝叶斯推断]
---

# 🎯 变分推断 (Variational Inference & ELBO)

---

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：变分推断（Variational Inference, VI）由 Jordan、Blei 等人推动发展，是**贝叶斯统计与现代概率图模型（PGM）中两大近似推断支柱之一**（另一支柱为 MCMC 蒙特卡洛采样）。它将极其困难甚至无法计算的高维概率后验积分问题，巧夺天工般地转化为一个**连续最优化问题（Optimization Problem）**。不搞懂变分推断和证据下界（ELBO），就无法真正从统计数学源头上理解 VAE、贝叶斯神经网络（BNN）以及大规模主题模型（LDA）。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem (我们遇到了什么麻烦)**：
> 在贝叶斯统计中，我们已知观测数据 $\mathbf{x}$，希望计算隐变量/参数 $\mathbf{z}$ 的后验概率分布 $p(\mathbf{z} \mid \mathbf{x}) = \frac{p(\mathbf{x}, \mathbf{z})}{p(\mathbf{x})}$。
> 算这个后验的分母需要计算边缘概率积分 $p(\mathbf{x}) = \int p(\mathbf{x}, \mathbf{z}) d\mathbf{z}$。
> 然而对于复杂的深层概率模型，这个高维积分在数学上是**无法精确求解的（Intractable）**！传统的 MCMC 采样虽然精确，但在大规模大数据集上**采样速度慢到令人发指**。
> 我们迫切需要一种**能把高维积分转化为求导优化、可以利用 GPU 大规模并行快速计算**的替代方案。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：变分推断是现代“深度贝叶斯学习”（Deep Bayesian Learning）的桥梁。它把概率推断降维成了类似梯度下降的连续优化，直接孕育了变分自编码器 (VAE) 和扩散模型 (Diffusion) 的目标函数推导。
- **实际应用场景**：LDA 主题模型文档分类、变分自编码器 (VAE)、贝叶斯神经网络 (BNN) 权重不确定性估计、高斯混合模型 (GMM) 变分求解。
- **高频考点/任务**：ELBO (Evidence Lower Bound) 从 Jensen 不等式与 KL 散度两条主线的完美双推导、平均场变分族 (Mean-Field Variational Family) 假设、坐标上升变分推断 (CAVI) 算法递推。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[22-概率论与数理统计/01-基础/贝叶斯公式|贝叶斯后验概率]]**：先验 $p(\mathbf{z})$ 结合似然 $p(\mathbf{x}|\mathbf{z})$ 得到后验 $p(\mathbf{z}|\mathbf{x})$。
2. **[[14-概率图模型/变分推断|KL 散度 (KL-Divergence)]]**：衡量两个分布 $q(\mathbf{z})$ 与 $p(\mathbf{z})$ 接近程度的指标：$\mathcal{D}_{KL}(q \parallel p) = \mathbb{E}_q [\ln q(\mathbf{z}) - \ln p(\mathbf{z})]$。

---

## 4. 用直觉语言解释它

> «“这东西其实就像……”»

- **直觉类比**：变分推断就像一个**用手办模型逼近真人雕塑的雕刻家**：
  - 真实复杂的后验分布 $p(\mathbf{z} \mid \mathbf{x})$ 就像一座藏在迷雾里、形状极度扭曲复杂的奇特雕塑（数学上算不出来）；
  - 雕刻家放弃去精确测量迷雾雕塑，而是**自备一套简单的可调塑胶手办模型 $q_{\phi}(\mathbf{z})$**（比如由均值 $\mu$ 和方差 $\sigma^2$ 控制的圆润高斯分布）；
  - 雕刻家拧动手办模型的各个关节螺丝（调整参数 $\phi$），**捏到手办与迷雾里的真实雕塑最贴合（使得 KL 散度极小）**。
  - 最后，用捏好的简单手办 $q_{\phi}(\mathbf{z})$ 完美替代那个算不出来的复杂雕塑！
- **为什么很自然**：把求不出的高维积分 $p(z|x)$，变成了捏螺丝优化 $q_\phi(z)$ 参数的极值问题，直接套用梯度下降即可！
- **一句话直觉本质**：用族内简单的变分分布逼近复杂的真实后验，将不可计算的概率积分转化为可优化的 ELBO 最大化。

---

## 5. 正式定义、核心公式、符号解释

### 1. 核心定义与优化目标
设真实后验为 $p(\mathbf{z} \mid \mathbf{x})$，定义变分分布族 $\mathcal{Q} = \{q_{\phi}(\mathbf{z})\}$。变分推断旨在寻找最佳参数 $\phi^*$ 最小化 KL 散度：
$$\phi^* = \arg\min_{\phi} \mathcal{D}_{KL}\left( q_{\phi}(\mathbf{z}) \parallel p(\mathbf{z} \mid \mathbf{x}) \right)$$

### 2. 证据下界 (ELBO, Evidence Lower Bound) 黄金分解式
由于真实的 $\mathcal{D}_{KL}(q \parallel p(\mathbf{z}|\mathbf{x}))$ 包含不可算的 $p(\mathbf{z}|\mathbf{x})$，通过数学展开可得：
$$\ln p(\mathbf{x}) = \mathcal{L}_{ELBO}(q) + \mathcal{D}_{KL}\left( q(\mathbf{z}) \parallel p(\mathbf{z} \mid \mathbf{x}) \right)$$
其中证据下界 (ELBO) 表达为：
$$\mathcal{L}_{ELBO}(q) = \mathbb{E}_{q(\mathbf{z})} \left[ \ln p(\mathbf{x}, \mathbf{z}) \right] - \mathbb{E}_{q(\mathbf{z})} \left[ \ln q(\mathbf{z}) \right] = \mathbb{E}_{q(\mathbf{z})} [\ln p(\mathbf{x} \mid \mathbf{z})] - \mathcal{D}_{KL}(q(\mathbf{z}) \parallel p(\mathbf{z}))$$

### 3. 平均场假设 (Mean-Field Variational Family)
假设隐变量之间相互独立，变分分布可因式分解为：
$$q(\mathbf{z}) = \prod_{j=1}^m q_j(z_j)$$

### 4. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\mathbf{x}$ | 观测数据 (Observed Variables) | $\mathbb{R}^D$ | 已知的输入数据 |
| $\mathbf{z}$ | 隐变量 / 未知参数 (Latent Variables) | $\mathbb{R}^K$ | 需要推断的内部变量 |
| $q_{\phi}(\mathbf{z})$ | 变分分布 (Variational Distribution) | 概率密度 | 结构简单、可调参数的近似分布 |
| $\ln p(\mathbf{x})$ | 边际对数似然 / 证据 (Evidence) | $(-\infty, 0]$ | **因 $\mathcal{D}_{KL} \ge 0$，故 $\ln p(x) \ge \mathcal{L}_{ELBO}$** |
| $\mathcal{L}_{ELBO}$ | 证据下界 (Evidence Lower Bound) | $(-\infty, \ln p(x)]$ | **变分推断真正最大化的标量目标** |

---

## 6. 推导思路和思想来源

- **最初困难**：想最小化 $\mathcal{D}_{KL}(q(\mathbf{z}) \parallel p(\mathbf{z}|\mathbf{x})) = \int q(\mathbf{z}) \ln \frac{q(\mathbf{z})}{p(\mathbf{z}|\mathbf{x})} d\mathbf{z}$。展开后发现包含 $-\int q(\mathbf{z}) \ln p(\mathbf{z}|\mathbf{x}) d\mathbf{z}$，这里面依然含有算不出的后验 $p(\mathbf{z}|\mathbf{x})$，陷入死循环！
- **关键转念 1（转换靶心到 ELBO）**：
  根据贝叶斯公式 $p(\mathbf{z}|\mathbf{x}) = \frac{p(\mathbf{x}, \mathbf{z})}{p(\mathbf{x})}$ 代入展开：
  $$\mathcal{D}_{KL}(q \parallel p(\mathbf{z}|\mathbf{x})) = \mathbb{E}_q \left[ \ln q(\mathbf{z}) - \ln \frac{p(\mathbf{x}, \mathbf{z})}{p(\mathbf{x})} \right] = \mathbb{E}_q [\ln q(\mathbf{z})] - \mathbb{E}_q [\ln p(\mathbf{x}, \mathbf{z})] + \ln p(\mathbf{x})$$
  移项重排：
  $$\ln p(\mathbf{x}) = \underbrace{\mathbb{E}_q [\ln p(\mathbf{x}, \mathbf{z})] - \mathbb{E}_q [\ln q(\mathbf{z})]}_{\mathcal{L}_{ELBO}(q)} + \mathcal{D}_{KL}(q(\mathbf{z}) \parallel p(\mathbf{z} \mid \mathbf{x}))$$
- **关键转念 2（确定性不等式）**：
  注意观察上式：数据对数似然 $\ln p(\mathbf{x})$ 是一个与变分分布 $q$ **完全无关的常数**！
  而 KL 散度恒大于等于 0（$\mathcal{D}_{KL} \ge 0$）。
  **这就意味着：最大化 $\mathcal{L}_{ELBO}(q)$，等价于完美最小化 KL 散度 $\mathcal{D}_{KL}(q \parallel p(\mathbf{z}|\mathbf{x}))$！** 且 ELBO 里面只包含已知的联合分布 $p(\mathbf{x}, \mathbf{z})$，完全避开了无法计算的后验！

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（ELBO 组成项数值手算）
- **题目**：已知某模型采样下的联合概率对数期望 $\mathbb{E}_q [\ln p(\mathbf{x}, \mathbf{z})] = -15.0$，变分分布的熵 $\mathbb{E}_q [-\ln q(\mathbf{z})] = 3.0$（即负期望 $\mathbb{E}_q [\ln q(\mathbf{z})] = -3.0$）。求当前的 ELBO 证据下界值。
- **解答过程**：
  代入 ELBO 定义公式：
  $$\mathcal{L}_{ELBO} = \mathbb{E}_q [\ln p(\mathbf{x}, \mathbf{z})] - \mathbb{E}_q [\ln q(\mathbf{z})] = -15.0 - (-3.0) = -15.0 + 3.0 = -12.0$$
- **🤔 追问**：如果真实数据似然 $\ln p(\mathbf{x}) = -10.0$，此时变分分布与真后验的 KL 散度为多少？
  - *答*：$\mathcal{D}_{KL} = \ln p(\mathbf{x}) - \mathcal{L}_{ELBO} = -10.0 - (-12.0) = 2.0$。

### 例子 2：中等例子（平均场坐标上升变分推断 CAVI 公式推导）
在平均场假设 $q(\mathbf{z}) = \prod_j q_j(z_j)$ 下，固定其他所有因子 $q_{k \neq j}$，单个因子 $q_j^*(z_j)$ 的最优更新公式为：
$$\ln q_j^*(z_j) \propto \mathbb{E}_{q_{-j}} [\ln p(\mathbf{x}, \mathbf{z})]$$
即 $q_j^*(z_j) \propto \exp\left( \mathbb{E}_{q_{-j}} [\ln p(\mathbf{x}, \mathbf{z})] \right)$。这构成了经典的坐标上升变分推断算法（CAVI）！

### 例子 3：实际应用（PyTorch 手写一维高斯分布变分推断求后验）

```python
import torch
import torch.optim as optim

# 模拟真实观测数据 x ~ N(mu=5.0, sigma=1.0)
torch.manual_seed(42)
x_data = torch.randn(100) * 1.0 + 5.0

# 变分推断目标：用 q(mu) = N(mu_q, sigma_q^2) 去逼近先验为 N(0, 10^2) 的真实后验 p(mu | x)
mu_q = torch.tensor(0.0, requires_grad=True)
log_sigma_q = torch.tensor(0.0, requires_grad=True) # 使用 log 方差保持正数

optimizer = optim.Adam([mu_q, log_sigma_q], lr=0.05)

for step in range(500):
    optimizer.zero_grad()
    
    sigma_q = torch.exp(log_sigma_q)
    # 重参数采样 20 个 mu_sample
    eps = torch.randn(20)
    mu_samples = mu_q + sigma_q * eps # [20]
    
    # 1. 计算对数似然 log p(x | mu)
    # x_data: [100], mu_samples: [20] -> [20, 100]
    log_likelihood = -0.5 * ((x_data.unsqueeze(0) - mu_samples.unsqueeze(1))**2).sum(dim=-1)
    
    # 2. 计算先验对数 log p(mu) ~ N(0, 10^2)
    log_prior = -0.5 * (mu_samples / 10.0)**2
    
    # 3. 计算变分分布熵 -log q(mu)
    log_q = -0.5 * eps**2 - log_sigma_q
    
    # 4. 计算 ELBO = E_q [log p(x, mu) - log q(mu)]
    elbo = (log_likelihood + log_prior - log_q).mean()
    
    # 变分推断最大化 ELBO (即最小化 -ELBO)
    loss = -elbo
    loss.backward()
    optimizer.step()

print(f"变分推断完成！均值估计 mu_q = {mu_q.item():.3f} (真实均值 5.0)，标准差 sigma_q = {torch.exp(log_sigma_q).item():.3f}")
```

---

## 8. 常见误区和易混概念

### 误区 1：变分推断 (VI) 和 MCMC 采样是一回事
- **错误直觉**：“都是求解概率后验的方法，本质没有区别。”
- **为什么错**：原理和工程特性截然不同！
  - **MCMC**：通过马尔可夫链非参数化地**直接采样**粒子，理论上无限采样可无偏收敛到真实后验，但极慢，无法适应大数据；
  - **VI**：把推断变成**连续函数优化**，用已知简单分布去拟合后验，速度极快且极度适合 GPU/深度学习，但受限于变分族的表达能力，解往往是有偏的（偏向于 underestimate 方差）。

### 概念对比表

| 特性 | 变分推断 (Variational Inference) | 蒙特卡洛采样 (MCMC) |
| :--- | :--- | :--- |
| **算法本质** | 确定性最优化问题 ($\mathcal{L}_{ELBO}$ 最大化) | 随机蒙特卡洛采样 (Markov Chain) |
| **求解速度与并行度** | **极快，天然支持 GPU 和 Mini-batch 梯度下降**| 较慢，串行采样难以大规模并行 |
| **准确性** | 有偏估计（取决于变分族 $\mathcal{Q}$ 的假设） | 渐进无偏（采样趋于无限时收敛于真后验） |
| **代表算法/模型** | **VAE、CAVI、LDA、贝叶斯神经网络** | **Metropolis-Hastings、Gibbs 采样** |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[14-概率图模型/01-基础概念/贝叶斯网|贝叶斯网]]：概率图模型的联合分布 $p(\mathbf{x}, \mathbf{z})$ 定义。
- [[22-概率论与数理统计/01-基础/贝叶斯公式|贝叶斯公式]]：后验概率不可算的背景原因。

### 下游延伸
- [[17-机器学习/03-正则优化/VAE 变分自编码器|VAE 变分自编码器]]：将变分推断与深度神经网络结合的生成模型。

### 横向关联
- [[14-概率图模型/03-近似推断/MCMC|MCMC 采样]] ↔ [[14-概率图模型/变分推断|变分推断]]：PGM 近似推断两大双雄。

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清楚变分推断解决什么问题（将高维不可算后验积分转化为可求解的 ELBO 最大化优化）。
- [ ] 2. 用直觉语言解释它（«“这东西其实就像用手办塑胶模型去贴合迷雾里的真实雕塑……”»）。
- [ ] 3. 默写 $\ln p(\mathbf{x}) = \mathcal{L}_{ELBO} + \mathcal{D}_{KL}$ 的分解等式。
- [ ] 4. 写出 ELBO 的两种常见等价表达式（联合概率期望式与重构+KL散度式）。
- [ ] 5. 说明为什么最大化 ELBO 等价于最小化变分分布与真实后验的 KL 散度。
- [ ] 6. 解释平均场假设 (Mean-Field Assumption) 的数学含义。
- [ ] 7. 手算简单的 ELBO 与 KL 散度数值。
- [ ] 8. 对比变分推断 (VI) 与 MCMC 采样的优缺点。
- [ ] 9. 手写基于 PyTorch 的简单的变分推断代码。
- [ ] 10. 简述变分推断在 VAE 模型中的应用。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 证据下界 ELBO 与真实似然的关系 |
| 2 | 公式计算 | 基础 | ELBO 数值计算 |
| 3 | 条件判断 | 中等 | 平均场假设对变量独立性的限制 |
| 4 | 变式/综合 | 中等 | 为什么变分推断往往会“低估”真实后验的方差 (Variance Underestimation) |
| 5 | 开放/推导 | 较难 | 利用 Jensen 不等式直接推导 ELBO 公式 |

### 题目与解析

#### 1. 关于变分推断 (Variational Inference) 中 ELBO 的说法，正确的是？
- A. ELBO 的值永远大于等于真实数据的边缘对数似然 $\ln p(\mathbf{x})$
- B. 训练过程中，ELBO 越大，变分分布 $q(\mathbf{z})$ 与真实后验 $p(\mathbf{z} \mid \mathbf{x})$ 的距离越远
- C. ELBO 为数据对数似然 $\ln p(\mathbf{x})$ 提供了数学下界，即 $\mathcal{L}_{ELBO} \le \ln p(\mathbf{x})$
- D. 计算 ELBO 需要提前已知精确的后验概率分布 $p(\mathbf{z} \mid \mathbf{x})$

> [!question]- 答案解析
> - **答案**：C
> - **解析**：因为 $\ln p(\mathbf{x}) = \mathcal{L}_{ELBO} + \mathcal{D}_{KL}$ 且 $\mathcal{D}_{KL} \ge 0$，所以 $\mathcal{L}_{ELBO} \le \ln p(\mathbf{x})$，即 ELBO 是对数似然的下界；最大化 ELBO 会使该下界逼近似然，同时缩小 KL 散度。
> - **对应误区**：误区 1。

#### 2. 在变分推断中，使用逆向 KL 散度 $\mathcal{D}_{KL}(q \parallel p)$ 代替正向 KL 散度 $\mathcal{D}_{KL}(p \parallel q)$ 优化，会导致拟合出的变分分布呈现什么几何特征？
> [!question]- 答案解析
> - **答案**：表现出“避模 (Mode-Seeking / Variance Underestimation)”特性。
> - **解析**：逆向 KL 散度 $\mathbb{E}_q [\ln q - \ln p]$ 要求当 $p(z) \to 0$ 时，$q(z)$ 必须极速趋近于 0（否则损失暴增）；因此变分分布 $q$ 会宁可收缩方差避开低概率区，只锁定多峰分布中的某一个主峰（低估真实方差）。

#### 3. 平均场变分族 (Mean-Field Variational Family) 假设 $q(\mathbf{z}) = \prod_{j=1}^m q_j(z_j)$ 在数学上带来了什么巨大便利？
> [!question]- 答案解析
> - **答案**：将复杂的全局多元变分优化解耦为各个单变量因子的坐标上升交替更新 (CAVI)。
> - **解析**：平均场假设打破了隐变量间复杂的联立耦合，使得固定其他变量时，单个因子 $q_j^*(z_j) \propto \exp(\mathbb{E}_{-j}[\ln p(\mathbf{x}, \mathbf{z})])$ 拥有极佳的闭式解析解更新形式。

#### 4. 【推导】利用 Jensen 不等式，从 $\ln p(\mathbf{x}) = \ln \int p(\mathbf{x}, \mathbf{z}) d\mathbf{z}$ 直接推导 $\mathcal{L}_{ELBO}$。
> [!question]- 答案解析
> - **推导**：
>   $$\ln p(\mathbf{x}) = \ln \int p(\mathbf{x}, \mathbf{z}) d\mathbf{z} = \ln \int q(\mathbf{z}) \frac{p(\mathbf{x}, \mathbf{z})}{q(\mathbf{z})} d\mathbf{z} = \ln \mathbb{E}_{q(\mathbf{z})} \left[ \frac{p(\mathbf{x}, \mathbf{z})}{q(\mathbf{z})} \right]$$
>   由于对数函数 $\ln(u)$ 为凹函数，由 Jensen 不等式 $\ln \mathbb{E}[U] \ge \mathbb{E}[\ln U]$：
>   $$\ln p(\mathbf{x}) \ge \mathbb{E}_{q(\mathbf{z})} \left[ \ln \frac{p(\mathbf{x}, \mathbf{z})}{q(\mathbf{z})} \right] = \mathbb{E}_{q(\mathbf{z})} [\ln p(\mathbf{x}, \mathbf{z})] - \mathbb{E}_{q(\mathbf{z})} [\ln q(\mathbf{z})] = \mathcal{L}_{ELBO}$$
>   证毕！极其简练干净！

#### 5. 【开放/理论】为什么变分推断 (VI) 在深度学习时代超越了传统 MCMC 采样，成为了 VAE、扩散模型等现代 AIGC 生成模型的基础？
> [!question]- 答案解析
> - **答案**：优化导向、可微重参数化与 Mini-batch 梯度的工程契合。
> - **解析**：变分推断把统计推断转化为标量函数优化。借助 PyTorch 自动求导与重参数技巧 (Reparameterization Trick)，ELBO 可以无缝接入 SGD / Adam 优化器，利用 GPU 对大规模 Mini-batch 数据做并行梯度更新；而 MCMC 的串行 Sampling 无法方便地与深度学习端到端反向传播和 GPU 并行机制融合。

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

## 12. 学完后可以完成





---

## 13. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/14-概率图模型/`
- **建议双链**：
  - [[14-概率图模型/01-基础概念/贝叶斯网|贝

---

## 检索练习与通过标准

- **检索练习（闭卷自检）**：变分推断与 ELBO 的卡内 Python 自测断言与闭卷复述为最小验收；完成后方可进入依赖该卡的下游阶段。
- **通过标准**：能独立完成 ELBO 的双推导（Jensen 与 KL 两条主线）；能写出平均场更新与重参数化；完成卡内 10 项闭卷任务与 5 道自测题；能解释 VI vs MCMC 的取舍。
- **可执行产物**：卡内 Python 自测脚本（可运行验证）。


## 🃏 Anki 卡片

- ELBO 的定义式::L(q) = E_q[log p(x,z)] − E_q[log q(z)] = log p(x) − KL(q‖p)
- 为什么变分推断用 KL(q‖p) 而非 KL(p‖q)::KL(q‖p) 对 q 可优化且呈 mode-seeking 行为；KL(p‖q) 需要知道 p 的归一化常数，计算困难
- log p(x) 与 ELBO 的关系::log p(x) = ELBO + KL(q‖p) ≥ ELBO，故 ELBO 是证据下界
