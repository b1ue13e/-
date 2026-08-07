---
type: study
topic: "高级MCMC"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段2-推断算法]]"
flow: knowledge
kind: concept
difficulty: advanced
upstream: ["[[概率图模型-Gibbs与MH采样]]", "[[概率图模型-MCMC收敛与诊断]]"]
concept: ["哈密顿蒙特卡洛", "NUTS", "Swendsen-Wang", "辅助变量"]
related: ["概率图模型-Gibbs与MH采样", "概率图模型-MCMC收敛与诊断"]
tags: [概率图模型, MCMC, HMC, NUTS]
---

# 概率图模型-高级MCMC

> 基础 MCMC（Gibbs/MH）在**高维连续空间**中混合极慢（随机游走行为）。本卡介绍三类进阶方法：**HMC** 利用梯度信息高效探索连续后验；**NUTS** 自动确定 HMC 步长与轨迹长度（PyMC/Stan 默认）；**Swendsen-Wang** 用辅助变量同时翻转一大块相关变量，破解 Ising/Potts 模型的慢混合。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：MH 的提议是局部随机游走，在高维空间中需要海量步数才能移动到独立区域（每一步移动距离小、接受率与维数矛盾）。HMC 引入"动量 + 哈密顿动力学"，让采样沿着等高线"滚动"，大幅提高有效步长；Swendsen-Wang 解决**高度相关离散变量**（如图像像素）无法单独更新的问题。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：HMC/NUTS 是现代贝叶斯编程（PyMC/NumPyro/Stan）的默认引擎，处理几十到几百维连续后验；Swendsen-Wang 是统计物理与图像模型的标准工具。
- **实际应用场景**：贝叶斯神经网络后验采样、分层模型推断、Ising/Potts 图像分割采样。
- **高频考点**：HMC 的物理直觉、NUTS 的自适应机制、辅助变量方法的思路。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-Gibbs与MH采样]]**：MH 接受框架、混合问题。
2. **[[概率图模型-MCMC收敛与诊断]]**：为什么混合慢是问题（自相关/ESS）。
3. 微积分：梯度、能量函数；物理直觉：动能/势能。

---

## 4. 定义与核心公式

### 4.1 哈密顿蒙特卡洛（Hamiltonian Monte Carlo, HMC）

**核心思想**：把目标分布写成**能量**形式 $p(\mathbf{x}) \propto e^{-U(\mathbf{x})}$（$U = -\log\tilde p$），引入辅助**动量** $\mathbf{r} \sim \mathcal{N}(0, M)$，构造联合分布
$$p(\mathbf{x}, \mathbf{r}) \propto e^{-U(\mathbf{x})} e^{-\frac{1}{2}\mathbf{r}^\top M^{-1}\mathbf{r}}$$
（$M$ 是质量矩阵，常取单位阵。）

**算法**：
1. 重采样动量：$\mathbf{r} \sim \mathcal{N}(0, M)$；
2. **蛙跳积分（leapfrog）** 模拟哈密顿动力学 $L$ 步，步长 $\epsilon$：
   $$\mathbf{r} \leftarrow \mathbf{r} - \frac{\epsilon}{2}\nabla U(\mathbf{x}),\quad \mathbf{x} \leftarrow \mathbf{x} + \epsilon M^{-1}\mathbf{r},\quad \mathbf{r} \leftarrow \mathbf{r} - \frac{\epsilon}{2}\nabla U(\mathbf{x})$$
3. 接受/拒绝：$\alpha = \min(1, e^{-[H(\mathbf{x}',\mathbf{r}') - H(\mathbf{x},\mathbf{r})]})$（$H = U + K$ 为哈密顿量）；
4. 丢弃动量，保留 $\mathbf{x}$。

**为什么快**：动力学沿能量等高线"滚动"，轨迹跨越分布的大部分区域，**每步独立距离远大于随机游走**（理想情况 $\text{ESS}$ 提高一个量级）；$\nabla U$ 提供方向信息。

### 4.2 NUTS（No-U-Turn Sampler）

**问题**：HMC 需要手动调 $\epsilon$ 与轨迹长度 $L$——$L$ 太短混合差，太长浪费。

**NUTS**：自动构建轨迹——不断扩展蛙跳轨迹，直到轨迹"转弯"（$\mathbf{r} \cdot (\mathbf{x} - \mathbf{x}_0) \le 0$），再从候选点中按概率选取。配合**双平均（dual averaging）**自适应 $\epsilon$ 使接受率 ≈ 0.8。

**特点**：几乎免调参；PyMC/NumPyro/Stan 的默认采样器。

### 4.3 Swendsen-Wang（SW，辅助变量法）

**问题**：Ising/Potts 模型中相邻变量强相关，单变量 Gibbs 更新极慢（一个像素的翻转被邻居"钉住"）。

**SW 算法**：
1. **绑定（bond）**：对每条边 $(i,j)$，以概率 $p_{ij} = 1 - e^{-\beta J \mathbb{1}[x_i = x_j]}$ 生成"活跃边"（只有同色边才可能激活）；
2. **聚类**：活跃边连接的节点形成簇；
3. **翻转（flip）**：对每个簇独立随机重采样整簇颜色（均匀/按外部场）。

**效果**：一次翻转一大块相关变量，大幅降低自相关，混合速度提升指数级（在相变点附近尤其显著）。

---

## 5. 关键推导

**推导：HMC 接受率与详细平衡**。
蛙跳是**辛积分**（保体积、可逆），配合动量翻转（$\mathbf{r} \to -\mathbf{r}$）使转移对称，接受率中提议比 = 1，只剩能量差：$\alpha = \min(1, e^{-\Delta H})$。由于蛙跳近似保留 $H$（$\Delta H \approx 0$），接受率接近 1，且 $\Delta H$ 的离散化误差随 $\epsilon^2$ 减小。∎

**推导：NUTS 停止条件直觉**。
轨迹扩展时，若当前点与起点的高斯内积 $\mathbf{r}_t \cdot (\mathbf{x}_t - \mathbf{x}_0) \le 0$，说明"动量与位移方向相反"，轨迹开始折返（转弯）——继续前进只会重复已探索区域，故停止。∎

**推导：SW 与详细平衡**。
SW 的转移由"绑定随机图 + 簇翻转"构成，可构造满足详细平衡的对称转移（绑定概率的选择使同色绑定与异色绑定的概率比匹配能量差），故以 Ising 分布为平稳分布。∎

---

## 6. 最小可手算例子

**例（HMC 一维手算）**：$U(x) = x^2/2$（标准正态，$\nabla U = x$），$M=1$，$\epsilon=0.5$，$L=2$。起点 $x=0$，动量 $\mathbf{r}=1$。

蛙跳：
- 半步：$r \leftarrow 1 - 0.25\times0 = 1$；$x \leftarrow 0 + 0.5\times1 = 0.5$；$r \leftarrow 1 - 0.25\times0.5 = 0.875$；
- 第二步：$r \leftarrow 0.875 - 0.25\times0.5 = 0.75$；$x \leftarrow 0.5 + 0.5\times0.75 = 0.875$；$r \leftarrow 0.75 - 0.25\times0.875 = 0.531$；
- 终点 $(x, r) = (0.875, 0.531)$；$H$ 变化：$\Delta H = (0.875^2 - 0)/2 + (0.531^2 - 1)/2 = 0.383 - 0.359 = 0.024$ → 接受率 $e^{-0.024} \approx 0.98$。一次提案从 0 到 0.875，远超随机游走步长。

**例（SW 直觉）**：2×2 Ising 全 +1，$\beta J$ 大。Gibbs：每次只翻一个像素，能量惩罚极大，几乎永远不翻。SW：四条边全部激活 → 整块作为一个簇 → 一次全部翻为 -1（或保留 +1），实现大尺度更新。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| HMC 不需要调参 | **错**。$\epsilon, L, M$ 都要调（或交给 NUTS 自适应）；$\epsilon$ 太大接受率崩、太小混合慢 |
| HMC 只能用于连续空间 | **对**。离散变量需先松弛（如 Gumbel-softmax）或用专门离散 MCMC |
| NUTS 一定能收敛 | **错**。NUTS 改善混合但不保证；病态后验（多峰、强相关）仍需诊断（$\hat R$） |
| SW 适合所有 MRF | **不精确**。SW 设计给 Potts/Ising 类"全局同色聚类"模型；一般因子图未必适用 |
| 高级 MCMC 一定比 Gibbs 快 | **不精确**。取决于问题结构；低维/简单模型 Gibbs 足够，高维连续/强相关才值得 HMC/SW |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. HMC 的哈密顿量由哪两部分组成？
2. NUTS 解决的 HMC 两个超参数是什么？

### #自测题/中等
3. 解释蛙跳积分"保体积 + 可逆"为何让 HMC 接受率接近 1。
4. SW 的"绑定-聚类-翻转"三步各解决什么问题？

### #自测题/较难
5. 为什么高维连续后验中 HMC 的有效步长远大于随机游走 MH？用"轨迹沿等高线"解释。

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. 势能 $U(\mathbf{x}) = -\log\tilde p(\mathbf{x})$ 与动能 $K(\mathbf{r}) = \frac12\mathbf{r}^\top M^{-1}\mathbf{r}$。
2. 步长 $\epsilon$ 与轨迹长度 $L$。
3. 辛积分近似守恒哈密顿量（$\Delta H = O(\epsilon^2)$），接受率 $e^{-\Delta H} \approx 1$；可逆性使提议对称，详细平衡成立。
4. 绑定：识别"值得一起动"的边；聚类：把强相关变量打包；翻转：一次更新整块，避免单变量被邻居钉住。
5. 随机游走 MH 每步距离 $\propto \sqrt{L}$（扩散）；HMC 沿等高线"惯性滚动"，位移 $\propto L$，有效步长线性增长，且梯度引导方向避免无谓震荡。
</details>

---

## 9. 通过标准

- [ ] 能**默写** HMC 蛙跳步骤与 NUTS 停止条件；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**说明** HMC/SW 各自解决的混合问题；
- [ ] 能在 PyMC/NumPyro 中调用 NUTS 并读取 $\hat R$。

---

## 10. 来源

- Neal (2011). *MCMC using Hamiltonian dynamics*. Handbook of MCMC.
- Hoffman & Gelman (2014). The No-U-Turn Sampler. *JMLR*.
- Swendsen & Wang (1987). Nonuniversal critical dynamics in Monte Carlo simulations. *PRL*.
- 访问日期：2026-08-07。

---

## 11. 学完后可以完成

```dataview
LIST
FROM "03-Projects/14-概率图模型"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/14-概率图模型"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

> 直接下游：阶段 6 的 [[PyMC]]/[[NumPyro]]/[[Stan]] 概率编程实践、课程 Capstone（采样部分）。
