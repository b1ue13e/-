---
type: study
topic: "概率统计-方差分析ANOVA与单因素效应"
course: "22-概率论与数理统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段4-渐近理论、计算推断与线性模型]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["方差分析", "ANOVA", "单因素效应", "平方和分解", "SST", "SSB", "SSW", "F检验", "多重比较"]
upstream: ["[[概率统计-经典参数假设检验：Z检验、t检验、卡方与F检验]]", "[[概率统计-前置-线性代数与二次型基础]]"]
related: ["[[概率统计-一元与多元线性回归的推断基础]]"]
tags: [学习, 概率论与数理统计, 假设检验, 方差分析, ANOVA, F检验]
---

# 概率统计-方差分析ANOVA与单因素效应

---

## 1. 单因素方差分析模型与假设

设有一因子 $A$，具有 $k$ 个不同水平（组别）。从第 $i$ 个水平中抽取容量为 $n_i$ 的样本：
$$X_{ij} = \mu_i + \varepsilon_{ij} \quad (i = 1, \dots, k; \; j = 1, \dots, n_i)$$
定义总样本量 $N = \sum_{i=1}^k n_i$。

**模型三大核心假定（Normality, Independence, Homoscedasticity）**：
1. **正态性**：各水平总体均服从正态分布；
2. **独立性**：误差项 $\varepsilon_{ij} \overset{\text{i.i.d.}}{\sim} \mathcal{N}(0, \sigma^2)$ 相互独立；
3. **同方差性（方差齐性）**：各组总体的方差均相等且为 $\sigma^2$。

**原假设与备择假设**：
$$H_0: \mu_1 = \mu_2 = \dots = \mu_k \quad \text{vs} \quad H_1: \mu_1, \dots, \mu_k \text{ 不全相等}$$

---

## 2. 平方和正交分解定理（Sum of Squares Decomposition）

定义：
- **第 $i$ 组样本均值**：$\bar{X}_{i\cdot} = \frac{1}{n_i}\sum_{j=1}^{n_i} X_{ij}$
- **总样本均值**：$\bar{X}_{\cdot\cdot} = \frac{1}{N}\sum_{i=1}^k\sum_{j=1}^{n_i} X_{ij}$

### 核心恒等式推导
总偏差可拆解为：
$$(X_{ij} - \bar{X}_{\cdot\cdot}) = \underbrace{(\bar{X}_{i\cdot} - \bar{X}_{\cdot\cdot})}_{\text{组间差异 (Between)}} + \underbrace{(X_{ij} - \bar{X}_{i\cdot})}_{\text{组内随机误差 (Within)}}$$
两边平方并对所有 $i, j$ 求和：
$$\sum_{i=1}^k\sum_{j=1}^{n_i} (X_{ij} - \bar{X}_{\cdot\cdot})^2 = \sum_{i=1}^k n_i(\bar{X}_{i\cdot} - \bar{X}_{\cdot\cdot})^2 + \sum_{i=1}^k\sum_{j=1}^{n_i} (X_{ij} - \bar{X}_{i\cdot})^2 + 2\sum_{i=1}^k (\bar{X}_{i\cdot} - \bar{X}_{\cdot\cdot}) \sum_{j=1}^{n_i} (X_{ij} - \bar{X}_{i\cdot})$$
由于 $\sum_{j=1}^{n_i} (X_{ij} - \bar{X}_{i\cdot}) = 0$，交叉项严格恒等于 0！

因此得到**总变异平方和分解公式**：
$$SST = SSB + SSW \quad (\text{或 } SS_{\text{Total}} = SS_{\text{Between}} + SS_{\text{Within}})$$

---

## 3. 标准 ANOVA 汇总表与 $F$ 检验

| 变异来源 | 平方和 (SS) | 自由度 (df) | 均方 (MS = SS / df) | 统计量 $F$ | $H_0$ 下理论分布 |
| :--- | :--- | :---: | :--- | :---: | :---: |
| **组间 (Between)** | $SSB = \sum_{i=1}^k n_i(\bar{X}_{i\cdot} - \bar{X}_{\cdot\cdot})^2$ | $k - 1$ | $MSB = \frac{SSB}{k-1}$ | $F = \frac{MSB}{MSW}$ | $F(k-1, N-k)$ |
| **组内 (Within / Error)** | $SSW = \sum_{i=1}^k\sum_{j=1}^{n_i} (X_{ij} - \bar{X}_{i\cdot})^2$ | $N - k$ | $MSW = \frac{SSW}{N-k}$ | — | — |
| **总和 (Total)** | $SST = \sum_{i=1}^k\sum_{j=1}^{n_i} (X_{ij} - \bar{X}_{\cdot\cdot})^2$ | $N - 1$ | — | — | — |

**决策规则**：
- 若 $F = \frac{MSB}{MSW} \ge F_\alpha(k-1, N-k)$（或 $p\text{-value} \le \alpha$），**拒绝 $H_0$**，说明组间存在显著差异。

---

## 4. Python 实现单因素方差分析

```python
import numpy as np
import scipy.stats as stats

np.random.seed(42)
# 模拟 3 个产品组别的评分数据
group1 = np.random.normal(loc=80, scale=5, size=20)
group2 = np.random.normal(loc=82, scale=5, size=20)
group3 = np.random.normal(loc=86, scale=5, size=20)

# 1. Scipy 官方单因素 ANOVA
f_stat, p_val = stats.f_oneway(group1, group2, group3)

# 2. 从零手写 ANOVA 矩阵运算验证
groups = [group1, group2, group3]
k = len(groups)
N = sum(len(g) for g in groups)
grand_mean = np.mean(np.concatenate(groups))

ssb = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
ssw = sum(np.sum((g - np.mean(g))**2) for g in groups)
sst = sum(np.sum((g - grand_mean)**2) for g in groups)

msb = ssb / (k - 1)
msw = ssw / (N - k)
manual_f = msb / msw

print(f"平方和分解恒等性: SST ({sst:.4f}) == SSB+SSW ({ssb+ssw:.4f})")
print(f"F 统计量: {f_stat:.4f} (手写: {manual_f:.4f})")
print(f"p-value: {p_val:.4e}")

assert np.isclose(sst, ssb + ssw), "平方和分解不守恒！"
assert np.isclose(f_stat, manual_f), "F 统计量手算与库函数不一致！"
```

---

## 5. 闭卷自测

- [ ] 给出总变异平方和分解式 $SST = SSB + SSW$ 交叉项为 0 的详细推导；
- [ ] 解释为什么做多组两两 $t$ 检验会导致第一类错误率膨胀；
- [ ] 写出单因素方差分析中 $MSB$ 与 $MSW$ 自由度的来源。

---

## 6. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
