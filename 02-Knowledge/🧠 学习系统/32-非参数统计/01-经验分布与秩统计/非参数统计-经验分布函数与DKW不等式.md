---
type: study
topic: "经验分布函数与DKW不等式"
course: "非参数统计"
created: 2026-08-08
status: active
stage_moc: "[[🧭 阶段1-经验分布与秩统计]]"
flow: knowledge
kind: concept
importance: "A"
tags: [学习, 非参数统计, 经验分布, DKW不等式, 极限定理]
upstream: ["[[非参数统计-前置-参数推断局限与分布无关思想]]", "[[非参数统计-前置-样本分位数与渐近正态性]]"]
proof_mode: true
---

# 非参数统计-经验分布函数与DKW不等式

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（非参数统计第一大基本定理）**
- **判断理由**：经验分布函数 (EDF) 是非参数推断的万物起源。无论是 Kolmogorov-Smirnov 检验、Bootstrap 重采样还是非参数函数估计，本质都是将总体 $F$ 替换为样本 $F_n$。DKW 不等式给出了有限样本下 $F_n$ 逼近 $F$ 的严格概率界。
- **验收模式说明**：Glivenko-Cantelli 定理陈述、DKW 边界公式推导、构造无分布置信带、闭卷自测。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 给定未知连续分布的独立同分布样本 $X_1, \dots, X_n$，如何给出一个对**整个未知函数曲线** $F(x)$ 的全局点估计，并给出在全定义域上一致成立的 $(1-\alpha)$ 置信带？
> **核心痛点**：点态 CLT 只能保证单点 $x$ 处收敛，无法控制全实数轴上上确界误差 $\sup_{x \in \mathbb{R}} |F_n(x) - F(x)|$ 的尾部概率。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：Glivenko-Cantelli 定理被称为“统计学基本定理”；DKW (Dvoretzky-Kiefer-Wolfowitz) 不等式则为现代经验过程论 (Empirical Process Theory) 与一致收敛泛化界奠定了基础。
- **实际应用场景**：金融损失分布无偏重构、非参数拟合优度检验、机器学习中经验风险最小化 (ERM) 泛化误差界。
- **高频考点**：DKW 不等式的精确常数应用、置信带宽度 $\epsilon_n = \sqrt{\frac{1}{2n}\ln\frac{2}{\alpha}}$ 的推导。

---

## 3. 学它之前需要哪些前置知识？

1. **[[非参数统计-前置-参数推断局限与分布无关思想]]**：概率积分变换定理。
2. **伯努利大数定律**：点态无偏性 $E[F_n(x)] = F(x)$ 与方差 $\text{Var}(F_n(x)) = \frac{F(x)(1-F(x))}{n}$。

---

## 4. 定义复述

### 1. 精确定义

设 $X_1, X_2, \dots, X_n \stackrel{i.i.d.}{\sim} F$。
- **经验分布函数 (Empirical Distribution Function, EDF)** 定义为阶梯函数：
  $$F_n(x) = \frac{1}{n} \sum_{i=1}^n \mathbb{I}(X_i \le x) = \frac{\#\{X_i \le x\}}{n}, \quad x \in \mathbb{R}$$

### 2. 核心定理陈述

1. **Glivenko-Cantelli 定理 (统计学基本定理)**：
   $$\sup_{x \in \mathbb{R}} |F_n(x) - F(x)| \xrightarrow{a.s.} 0 \quad (n \to \infty)$$
2. **DKW 不等式 (Massart 1990 最优常数形式)**：
   对任意 $\epsilon > 0$ 和任意分布 $F$：
   $$P\left(\sup_{x \in \mathbb{R}} |F_n(x) - F(x)| > \epsilon\right) \le 2 e^{-2n\epsilon^2}$$

### 3. 非参数一致置信带构造

令 $2e^{-2n\epsilon_n^2} = \alpha$，解得临界边界：
$$\epsilon_n = \sqrt{\frac{1}{2n} \ln\left(\frac{2}{\alpha}\right)}$$
则关于真实分布 $F(x)$ 的全局 $(1-\alpha)$ 非参数置信带为：
$$L(x) = \max(F_n(x) - \epsilon_n, 0), \quad U(x) = \min(F_n(x) + \epsilon_n, 1)$$
满足：
$$P(\forall x \in \mathbb{R}, L(x) \le F(x) \le U(x)) \ge 1 - \alpha$$

---

## 5. 直觉与图像

- **几何直觉**：$F_n(x)$ 是在样本点处跳跃大小为 $1/n$ 的单调阶梯曲线。随着样本量 $n$ 增大，阶梯越碎，整条阶梯带在全实数轴上像拉链一样把未知的真实平滑曲线 $F(x)$ 牢牢夹在上下置信带 $[L(x), U(x)]$ 之间。
- **一句话本质**：DKW 不等式给出了样本分布逼近真实分布的指数级集中度保证。

---

## 6. 证明要点与技巧迁移

### 1. 证明关键转念
- 利用概率积分变换 $U_i = F(X_i) \sim \text{Uniform}(0, 1)$，将任意复杂连续分布 $F$ 的上确界误差分布无关化：
  $$\sup_{x \in \mathbb{R}} |F_n(x) - F(x)| \stackrel{d}{=} \sup_{u \in [0, 1]} |G_n(u) - u|$$
  其中 $G_n$ 为标准均匀分布的经验分布函数。
- 应用鞅论与 Doob 极大值不等式或 Hoeffding 集中不等式，导出指数衰减因子 $e^{-2n\epsilon^2}$。

---

## 7. 经典反例与边界

### 反例 1：点态置信区间不等于一致置信带
- **错误做法**：对每个固定点 $x$，根据正态近似计算 $F_n(x) \pm z_{\alpha/2}\sqrt{F_n(x)(1-F_n(x))/n}$，并声称这是 $F(x)$ 的全局置信带。
- **崩溃原因**：多重检验与局部极大值效应导致真实曲线在至少某一点跳出该区间的概率远高于 $\alpha$。必须使用 DKW 临界值 $\epsilon_n$ 保证一致覆盖。

---

## 8. 条件变式

| 变式 | 条件改动 | 结论变化 | 成立/不成立 | 依据 |
| :--- | :--- | :--- | :---: | :--- |
| 离散分布 $F$ | 存在大量结 (Ties) | 依然成立且更保守 | 成立 | 离散跳跃使得上确界只能在子集取得，误差不增反降 |
| 相关时间序列 | 样本间存在 $\alpha$-混合自相关 | 需修正指数常数 $2 \to 2(1-\rho)/(1+\rho)$ | 变式成立 | 依赖性降低有效样本容量 |

---

## 9. 闭卷验收与学完后可以完成

### 闭卷验收（数学模式）
- [ ] **公式默写**：写出经验分布函数 $F_n(x)$ 与 DKW 不等式上界公式 $2e^{-2n\epsilon^2}$。
- [ ] **推导置信带**：写出给定 $\alpha=0.05$ 时的置信带半宽 $\epsilon_n$ 计算公式。
- [ ] **反例辨析**：解释为什么点态 CLT 区间不能拼成一致置信带。

### 学完后可以完成
```dataview
LIST
FROM "03-Projects/32-非参数统计"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---

## 10. 分级习题

| 题号 | 类型 | 难度 | 来源 | 考查点 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 计算题 | 基础 | Wasserman Ch.2 Ex.1 | 给定 $n=100, \alpha=0.05$，求 DKW 置信带半宽 |
| 2 | 性质证明 | 中等 | IMS Ch.11 Lab | 证明 $E[F_n(x)] = F(x)$ 与 $\text{Cov}(F_n(s), F_n(t)) = \frac{F(s)(1-F(t))}{n}$ ($s \le t$) |

### 题目与解析

#### 1. DKW 置信带半宽计算
> [!question]- 答案与解析（复盘阶段查看）
> - **解答**：$\epsilon_n = \sqrt{\frac{1}{200}\ln\left(\frac{2}{0.05}\right)} = \sqrt{\frac{\ln(40)}{200}} \approx \sqrt{\frac{3.68888}{200}} \approx \sqrt{0.01844} \approx 0.1358$。
> - 即在样本量为 100 时，我们在 $95\%$ 置信度下保证整个真实分布曲线都在 $F_{100}(x) \pm 0.1358$ 的包络线内。

---

## 11. 我的主动回忆区
> 闭卷复述：Glivenko-Cantelli 定理与 DKW 不等式有何本质区别？（前者是渐近确定性，后者是有限样本指数界限）

---

## 12. 给 Obsidian 的归档建议
- **归档目录**：`02-Knowledge/🧠 学习系统/32-非参数统计/01-经验分布与秩统计/`
- **标签**：`#学习 #非参数统计 #经验分布 #DKW不等式`
