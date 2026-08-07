---
type: study
topic: "MCMC收敛与诊断"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段2-推断算法]]"
flow: knowledge
kind: concept
difficulty: intermediate
upstream: ["[[概率图模型-Gibbs与MH采样]]"]
concept: ["burn-in", "自相关", "Gelman-Rubin统计量", "有效样本量"]
related: ["概率图模型-Gibbs与MH采样", "概率图模型-高级MCMC"]
tags: [概率图模型, MCMC, 收敛诊断]
anki_deck: "概率图模型::02-推断算法"
anki_tags: [概率图模型, MCMC, 收敛诊断]
---

# 概率图模型-MCMC收敛与诊断

> MCMC 的正确性**依赖收敛**：只有链进入平稳分布后，样本才服从目标分布。本卡讲解为什么需要 burn-in、如何量化自相关、如何用 $\hat R$（Gelman-Rubin）与有效样本量（ESS）诊断链的质量，以及"看起来收敛但实际没收敛"的陷阱。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：Gibbs/MH 声称"渐近精确"，但实践中我们只运行有限步。如果链还没收敛（还在往高概率区"爬行"），样本就**不服从目标分布**，估计就有偏差。更糟的是，链可能"看起来稳定"（在某个模式附近徘徊）却从未探索全分布（混合失败）。收敛诊断回答：**现在可以停了吗？样本可信吗？**

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：MCMC 的每一步都可能被质疑"没收敛"；诊断是 MCMC 结果可信性的**必要证据**（论文/报告必报 $\hat R$、ESS）。
- **实际应用场景**：PyMC/Stan 自动报告 $\hat R$；贝叶斯推断交付前必须展示收敛诊断。
- **高频考点**：burn-in 的意义、$\hat R$ 的计算与阈值、ESS 与自相关的关系、混合失败识别。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-Gibbs与MH采样]]**：链的构造、平稳分布概念。
2. 统计基础：方差、协方差、样本均值估计。

---

## 4. 定义与核心公式

### 4.1 Burn-in（预热期）

**定义**：链从初始点 $\mathbf{x}^{(0)}$ 到近似进入平稳分布所需的迭代数 $B$。

**处理**：丢弃前 $B$ 个样本。选择 $B$：画 trace plot（轨迹图），取"看起来稳定后"的位置，或根据 $\hat R$/ESS 确定。

> 初始点远离高概率区域时，早期样本偏差大；burn-in 就是"让链忘掉初始点"。

### 4.2 自相关（Autocorrelation）

**定义**：链上相隔 $k$ 步的样本之间的相关系数
$$\rho_k = \text{Corr}(x^{(t)}, x^{(t+k)})$$

**含义**：MCMC 样本不独立，$\rho_k > 0$ 意味着有效信息量少于样本数。**自相关越高，链"走得越慢"**（探索效率低）。

### 4.3 有效样本量（ESS）

**定义**：与 $N$ 个相关样本等效的独立样本数
$$\text{ESS} = \frac{N}{1 + 2\sum_{k\ge1}\rho_k} \approx \frac{N}{\tau}$$
（$\tau$ 是积分自相关时间。）

**经验规则**：ESS ≥ 400（单链）或 ≥ 100/链 × 4 链 是常见下限；ESS 远小于 $N$ 时需更长的链或更好的提议。

### 4.4 Gelman-Rubin 统计量（$\hat R$，分势缩减因子）

**算法**：跑 $M \ge 2$ 条链，各 $N$ 步（不同初始点）。
- 链间方差：$B = \frac{N}{M-1}\sum_m (\bar x_m - \bar x)^2$；
- 链内方差：$W = \frac{1}{M}\sum_m s_m^2$（$s_m^2$ 为链 $m$ 的样本方差）；
- 后验方差估计：$\widehat{\text{Var}} = \frac{N-1}{N}W + \frac{1}{N}B$；
- **$\hat R = \sqrt{\widehat{\text{Var}} / W}$**。

**判读**：$\hat R \to 1$ 表示链间与链内方差可比（收敛）。**阈值：$\hat R < 1.01$（或经典 < 1.05）**。$\hat R \gg 1$ 说明链从不同起点未达成一致（未收敛或混合差）。

---

## 5. 关键推导

**推导：为什么 $\hat R \approx 1$ 表示收敛**。

若链已收敛，所有链都从同一平稳分布采样：链间方差 $B \approx 0$（不同链的均值相同），$\widehat{\text{Var}} \approx W$，$\hat R \approx 1$。若未收敛，某些链还停在低概率区，链间均值差异大 → $B$ 大 → $\hat R > 1$。∎

**推导：ESS 为什么除以自相关和**。

对相关样本的均值估计：$\text{Var}(\bar x) = \frac{\sigma^2}{N}\left(1 + 2\sum_{k\ge1}\rho_k\right)$。令该方差等于独立样本（$N_{\text{eff}}$ 个）的方差 $\sigma^2/N_{\text{eff}}$，解得 $N_{\text{eff}} = \frac{N}{1+2\sum\rho_k}$。∎

**推导：减薄（thinning）何时有效**。
若 $\rho_k$ 在 $k \ge K$ 后接近 0，每隔 $K$ 步取一个样本可降低自相关；但若 $\rho_k$ 缓慢衰减（长自相关），减薄不能解决根本问题（链本身混合慢），应改善提议/参数化。∎

---

## 6. 最小可手算例子

**例（$\hat R$ 手算）**：两条链各 3 步：链 1 = {1, 2, 3}，链 2 = {3, 4, 5}。
- 链均值：2, 4；总均值 3；
- $B = \frac{3}{1}[(2-3)^2 + (4-3)^2] = 3\times2 = 6$；
- 链内方差：$s_1^2 = 1$，$s_2^2 = 1$，$W = 1$；
- $\widehat{\text{Var}} = \frac{2}{3}\times1 + \frac{1}{3}\times6 = 2.667$；
- $\hat R = \sqrt{2.667/1} \approx 1.63$ → **未收敛**（两链差异大）。

**例（trace plot 判断）**：链从 $x=0$ 出发向高概率区爬升，前 200 步单调上升（burn-in），200 步后在均值附近振荡 → 丢弃前 200 步，用 200 步后样本。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| trace plot 平稳 = 收敛 | **不充分**。多峰分布中链可能困在一个峰（混合失败），trace 看似平稳但 $\hat R$ 或跨峰占比异常 |
| 单链 $\hat R = 1$ | **无意义**。$\hat R$ 需要**多链**才能计算；单链只能用 trace/ESS 辅助判断 |
| 样本越多越可信 | **错**。若链未收敛，更多样本只会更精确地估计**错误的分布** |
| burn-in 越长越好 | **部分错**。过长浪费计算；关键是链确实进入平稳区，可用诊断量化 |
| ESS 小只是"不够快" | **错**。ESS 小可能反映混合失败（未探索全部支撑集），必须处理而非硬等 |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 什么是 burn-in？为什么必须丢弃？
2. 写出 $\hat R$ 的阈值与含义。

### #自测题/中等
3. 计算示例中两条链（链1={1,2,3}，链2={3,4,5}）的 $\hat R$，判断是否收敛。
4. 解释自相关为什么导致 ESS < N。

### #自测题/较难
5. 双峰分布中，单链 Gibbs 从峰 A 出发、trace 稳定在峰 A——为什么 $\hat R$ 可能仍 > 1（与另一条从峰 B 出发的链比较）？这种"混合失败"如何检测？

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. 链从初始点到平稳分布前的迭代；早期样本不来自目标分布，丢弃以消除偏差。
2. $\hat R < 1.01$（保守）/ < 1.05（经典）表示链间-链内方差可比，收敛。
3. 见 §6：$\hat R \approx 1.63 > 1.05$，未收敛。
4. 相关样本的均值方差 = $\sigma^2/N(1+2\sum\rho_k)$，等效独立样本数减少。
5. 两条链各困一个峰：链内方差小、链间均值差异大 → $B$ 大 → $\hat R > 1$。检测：多初始点、检查跨峰跳跃频率、对比链间分布（KS 检验）、用并行 tempering。
</details>

---

## 9. 通过标准

- [ ] 能**默写** $\hat R$ 公式与阈值、ESS 公式；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**阅读 trace plot 并计算 $\hat R$/ESS**；
- [ ] 能**识别**混合失败并说明检测手段。

---

## 10. 来源

- Gelman & Rubin (1992). Inference from iterative simulation. *Statistical Science*.
- Koller & Friedman (2009). *Probabilistic Graphical Models*, MIT Press. Chapter 12.4.
- Vehtari et al. (2021). Rank-normalization, folding, and localization: An improved $\hat R$ (Stan). 访问日期：2026-08-07。

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

> 直接下游：阶段作业-02（采样收敛 $\hat R < 1.05$ 硬验收）、课程 Capstone（采样一致性审计）、阶段 6 的 PyMC/NumPyro 实践。

## 🃏 Anki 卡片

- Burn-in 是什么::链从初始点到达近似平稳分布所需的迭代数 B，前 B 个样本应丢弃
- 自相关高的含义::相邻样本高度相关 → 链探索效率低、有效样本量远小于样本总数
- 常用收敛诊断::Gelman-Rubin R-hat（多链方差比，≈1 收敛）、有效样本量 ESS、轨迹图目测
