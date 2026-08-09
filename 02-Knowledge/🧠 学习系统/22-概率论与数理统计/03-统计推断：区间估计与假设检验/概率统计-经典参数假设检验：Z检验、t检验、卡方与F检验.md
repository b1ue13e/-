---
type: study
topic: "概率统计-经典参数假设检验：Z检验、t检验、卡方与F检验"
course: "22-概率论与数理统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段3-统计推断：区间估计与假设检验]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["假设检验", "Z检验", "t检验", "双样本t检验", "配对t检验", "卡方方差检验", "F方差齐性检验", "p值"]
upstream: ["[[概率统计-假设检验原理与Neyman-Pearson引理]]", "[[概率统计-抽样与三大抽样分布]]"]
related: ["[[概率统计-似然比检验与拟合优度检验]]", "[[概率统计-方差分析ANOVA与单因素效应]]"]
tags: [学习, 概率论与数理统计, 假设检验, Z检验, t检验, F检验, p值]
---

# 概率统计-经典参数假设检验：Z检验、t检验、卡方与F检验

---

## 1. 经典参数检验全景速查矩阵

### 1. 单正态总体检验（总体 $X \sim \mathcal{N}(\mu, \sigma^2)$）

| 检验名称 | 原假设 $H_0$ | 备择假设 $H_1$ | 检验统计量公式 | $H_0$ 下分布 | 拒绝域形式（显著性 $\alpha$） |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **单样本 $Z$ 检验** | $\mu = \mu_0$ ($\sigma$ 已知) | $\mu \ne \mu_0$ | $Z = \frac{\bar{X} - \mu_0}{\sigma / \sqrt{n}}$ | $\mathcal{N}(0, 1)$ | $\|Z\| \ge z_{\alpha/2}$ |
| **单样本 $t$ 检验** | $\mu = \mu_0$ ($\sigma$ 未知) | $\mu \ne \mu_0$ | $t = \frac{\bar{X} - \mu_0}{S / \sqrt{n}}$ | $t(n-1)$ | $\|t\| \ge t_{\alpha/2}(n-1)$ |
| **单样本卡方方差检验** | $\sigma^2 = \sigma_0^2$ | $\sigma^2 \ne \sigma_0^2$ | $\chi^2 = \frac{(n-1)S^2}{\sigma_0^2}$ | $\chi^2(n-1)$ | $\chi^2 \ge \chi^2_{\alpha/2}(n-1)$ 或 $\le \chi^2_{1-\alpha/2}(n-1)$ |

### 2. 双正态总体均值差检验（$X \sim \mathcal{N}(\mu_1, \sigma_1^2), Y \sim \mathcal{N}(\mu_2, \sigma_2^2)$）

| 检验名称 | 适用条件 | 检验统计量公式 | $H_0: \mu_1 = \mu_2$ 下分布 |
| :--- | :--- | :--- | :---: |
| **两独立样本 Pooled $t$ 检验** | 方差未知但假定**齐次**（$\sigma_1^2 = \sigma_2^2$） | $t = \frac{\bar{X} - \bar{Y}}{S_w \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}$，其中合并方差 $S_w^2 = \frac{(n_1-1)S_1^2 + (n_2-1)S_2^2}{n_1+n_2-2}$ | $t(n_1+n_2-2)$ |
| **Welch-Satterthwaite $t$ 检验** | 方差未知且**不齐次**（$\sigma_1^2 \ne \sigma_2^2$） | $t' = \frac{\bar{X} - \bar{Y}}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}$ | 近似 $t(df^*)$，自由度按 Satterthwaite 公式修正 |
| **配对样本 $t$ 检验** | 成对数据 $(X_i, Y_i)$（如用药前后） | 作差 $D_i = X_i - Y_i$，退化为单样本 $t$ 检验：$t = \frac{\bar{D}}{S_D / \sqrt{n}}$ | $t(n-1)$ |
| **双样本 $F$ 方差齐性检验** | 检验 $H_0: \sigma_1^2 = \sigma_2^2$ | $F = \frac{S_1^2}{S_2^2}$ | $F(n_1-1, n_2-1)$ |

---

## 2. $p$ 值（$p$-value）的严格定义与现代诠释

**定义**：在原假设 $H_0$ 为真的前提下，观察到**当前样本统计量或比当前样本更极端（更利于备择假设）结果的概率**：
$$p\text{-value} = P_{H_0}\big(T(\mathbf{X}) \text{ 比 } T_{\text{obs}} \text{ 更极端}\big)$$

**决策准则**：
- 若 $p\text{-value} \le \alpha$ $\implies$ **拒绝 $H_0$**（差异具有统计显著性）；
- 若 $p\text{-value} > \alpha$ $\implies$ **不拒绝 $H_0$**。

---

## 3. 统计显著性（Significance）vs 实际效应量（Effect Size）

> [!IMPORTANT]
> **大样本陷阱**：
> 当样本量 $n \to \infty$ 时，标准误 $S/\sqrt{n} \to 0$。哪怕真实均值差异微乎其微（如 $\mu_1 - \mu_2 = 0.0001$），也会使得 $t$ 统计量极大，$p\text{-value} < 0.0001$（具有极高统计显著性）。
> - **结论**：汇报假设检验结果时，必须同时汇报 **$p$ 值** 与 **效应量（如 Cohen's $d = \frac{\bar{X}_1 - \bar{X}_2}{S_w}$）**及置信区间。

---

## 4. Python 实现双样本 t 检验与 F 检验

```python
import numpy as np
import scipy.stats as stats

np.random.seed(42)
# 模拟 A/B 测试两组数据
group_A = np.random.normal(loc=10.0, scale=2.0, size=30)
group_B = np.random.normal(loc=11.2, scale=2.0, size=35)

# 1. 先做 F 检验检查方差齐性
var_A = np.var(group_A, ddof=1)
var_B = np.var(group_B, ddof=1)
F_stat = var_A / var_B
p_F = 2 * min(stats.f.cdf(F_stat, len(group_A)-1, len(group_B)-1), 
              1 - stats.f.cdf(F_stat, len(group_A)-1, len(group_B)-1))
print(f"方差齐性 F 检验: F={F_stat:.4f}, p={p_F:.4f}")

# 2. 独立双样本 t 检验
t_stat, p_t = stats.ttest_ind(group_A, group_B, equal_var=True)
print(f"双样本 t 检验: t={t_stat:.4f}, p={p_t:.4f}")

# 计算 Cohen's d 效应量
n1, n2 = len(group_A), len(group_B)
s_pooled = np.sqrt(((n1-1)*var_A + (n2-1)*var_B) / (n1 + n2 - 2))
cohen_d = (group_B.mean() - group_A.mean()) / s_pooled
print(f"Cohen's d 效应量: {cohen_d:.4f}")
```

---

## 5. 闭卷自测

- [ ] 给出双独立样本 Pooled $t$ 检验合并方差 $S_w^2$ 的公式与自由度推导；
- [ ] 解释配对 $t$ 检验与双独立样本 $t$ 检验的适用条件差异；
- [ ] 阐述 $p$ 值的严格概率定义，并纠正“$p$ 值是原假设为真的概率”这一常见错误。

---

## 6. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
