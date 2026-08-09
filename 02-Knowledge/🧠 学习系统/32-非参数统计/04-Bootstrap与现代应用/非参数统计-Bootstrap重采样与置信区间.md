---
type: study
topic: "Bootstrap重采样与置信区间"
course: "非参数统计"
created: 2026-08-08
status: active
stage_moc: "[[🧭 阶段4-Bootstrap与现代应用]]"
flow: knowledge
kind: concept
importance: "A"
tags: [学习, 非参数统计, 知识卡]
proof_mode: true
---

# 非参数统计-Bootstrap重采样与置信区间

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（现代计算统计第一方法）**
- **判断理由**：Bradley Efron 提出的 Bootstrap（自助法）是非参数估计中的革命性突破。它将“从真实总体中抽样获取分布”的不可行操作，转化为“从经验分布 $F_n$ 中有放回重抽样”的计算机模拟操作。掌握百分位、Studentized 与 BCa 置信区间的阶数精度是统计学进阶的关键指标。
- **验收模式说明**：插件原理推导、4 种 Bootstrap 置信区间公式对比、二阶精度推导、Bootstrap 失效案例。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 针对一个极其复杂的统计量（如相关系数 $\hat{\rho}$、中位数比值、PCA 第一特征向量），其理论渐近方差公式无法推导或形式极其冗长。
> **核心痛点**：如何在不求导、不推导渐近方差的前提下，利用计算重抽样自动得到高精度的标准误 $\\widehat{\text{SE}}$ 与非对称置信区间？

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：它是机器学习中 Bagging（如随机森林 Random Forest）、模型稳定性评估以及高维统计推断的通用工具。
- **实际应用场景**：非线性回归参数置信区间构造、金融资产组合风险 VaR 与夏普比率置信上限。
- **高频考点**：经验百分位区间 $[q_{\alpha/2}^*, q_{1-\alpha/2}^*]$ 与基本 Bootstrap 区间的转换、BCa (Bias-Corrected and Accelerated) 的二阶精度 $O(1/n)$。

---

## 3. 学它之前需要哪些前置知识？

1. **[[非参数统计-经验分布函数与DKW不等式]]**：$F_n$ 对 $F$ 的强一致性是 Bootstrap 成立的数学根基。
2. **多项重抽样**：$n$ 个样本有放回抽取 $n$ 次的概率模型（包含某特定样本的概率为 $1 - (1-1/n)^n \approx 1 - 1/e \approx 63.2\%$）。

---

## 4. 定义复述

### 1. 插件原理 (The Plug-in Principle)

设参数 $\theta = T(F)$ 是真实分布 $F$ 的某个统计泛函。
Bootstrap 估计量直接将未知分布 $F$ 替换为样本经验分布 $F_n$：
$$\hat{\theta} = T(F_n)$$
从 $F_n$ 中以有放回等概率抽取样本 $\mathbf{X}^* = (X_1^*, \dots, X_n^*)$，计算 Bootstrap 重复值 $\hat{\theta}^* = T(\mathbf{X}^*)$。

### 2. Bootstrap 标准误估计

重复有放回重抽样 $B$ 次（通常 $B \ge 1000$），得到 $\hat{\theta}^*_1, \dots, \hat{\theta}^*_B$。
Bootstrap 标准误定义为样本经验标准差：
$$\\widehat{\text{SE}}_{\text{boot}} = \sqrt{\frac{1}{B - 1} \sum_{b=1}^B (\hat{\theta}^*_b - \bar{\theta}^*)^2}, \quad \text{其中 } \bar{\theta}^* = \frac{1}{B}\sum_{b=1}^B \hat{\theta}^*_b$$

---

## 5. 四类 Bootstrap 置信区间对比

| 区间类型 | 构造公式 | 覆盖误差阶数 | 转换不变性 | 优缺点与适用场景 |
| :--- | :--- | :---: | :---: | :--- |
| **标准正态区间** | $\hat{\theta} \pm z_{\alpha/2} \\widehat{\text{SE}}_{\text{boot}}$ | $O(n^{-1/2})$ | 否 | 简单粗糙，强行对称化 |
| **基本 (Empirical) 区间** | $[2\hat{\theta} - \hat{\theta}^*_{(1-\alpha/2)}, 2\hat{\theta} - \hat{\theta}^*_{(\alpha/2)}]$ | $O(n^{-1/2})$ | 否 | 由估计误差分布推导而来 |
| **百分位 (Percentile) 区间** | $[\hat{\theta}^*_{(\alpha/2)}, \hat{\theta}^*_{(1-\alpha/2)}]$ | $O(n^{-1/2})$ | **是** | 直观抗噪，适合偏态参数 |
| **BCa (偏倚修正与加速) 区间** | $[\hat{\theta}^*_{(\alpha_1)}, \hat{\theta}^*_{(\alpha_2)}]$ | **$O(n^{-1})$ (二阶精度)** | **是** | **最高精度**，修正了非正态偏倚与方差对参数的依赖 |

---

## 6. BCa 置信区间的数学机制

BCa 将标准百分位数的分位点进行非线性转换：
$$\alpha_1 = \Phi\left( \hat{z}_0 + \frac{\hat{z}_0 + z_{\alpha/2}}{1 - a(\hat{z}_0 + z_{\alpha/2})} \right)$$
其中：
- **偏倚修正参数 $\hat{z}_0$**：$\hat{z}_0 = \Phi^{-1}\left( \frac{\#\{\hat{\theta}^*_b < \hat{\theta}\}}{B} \right)$，衡量重采样估计值落于原估计值左侧的比例偏离度。
- **加速度参数 $a$**：由留一法 (Jackknife) 的三阶矩计算，衡量标准误随参数真实值的变化率（偏度校正）。

---

## 7. 经典反例：Bootstrap 什么时候会彻底失效？

### 反例 1：样本极大值估计
- **问题**：设 $X_i \sim U(0, \theta)$，参数为上界 $\theta$。点估计为 $\hat{\theta} = X_{(n)}$。
- **崩溃原因**：在任何一次 Bootstrap 重抽样中，$\hat{\theta}^*$ 取得最大值 $X_{(n)}$ 的概率恰为 $1 - (1 - 1/n)^n \to 1 - 1/e \approx 0.632$。即有 $63.2\%$ 的概率重抽样极大值等于原极大值，无法产生平滑的连续逼近。
- **结论**：对**支撑集边界参数或极值**，标准 Bootstrap 彻底失效！必须改用 $m$-out-of-$n$ Bootstrap（$m \to \infty, m/n \to 0$）。

---

## 8. 闭卷验收（数学模式）

- [ ] **区间公式**：准确写出经验百分位置信区间与基本 Bootstrap 区间的定义式。
- [ ] **失效率计算**：独立证明 Bootstrap 重抽样不包含某个特定数据点的概率收敛于 $1/e \approx 36.8\%$。
- [ ] **失效判别**：举出 2 个标准 Efron Bootstrap 失效的数学场景（极值分布、柯西无一阶矩分布）。

---

## 9. 分级习题

| 题号 | 类型 | 难度 | 来源 | 考查点 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 概率计算 | 基础 | Efron & Tibshirani Ch.2 | 重采样中不重复样本数的期望值 $n(1 - 1/e)$ 推导 |
| 2 | 算法实现 | 中等 | IMS Ch.13 Lab | Python 实现样本中位数的百分位与 BCa 区间比较 |

---

## 10. 给 Obsidian 的归档建议
- **归档目录**：`02-Knowledge/🧠 学习系统/32-非参数统计/04-Bootstrap与现代应用/`
- **标签**：`#学习 #非参数统计 #Bootstrap #重抽样 #置信区间`


---

## 🎯 学完后可以完成

```dataview
LIST
FROM "03-Projects/32-非参数统计"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
