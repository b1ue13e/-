---
title: "Radon-Nikodym与条件期望"
date: "2026-08-03"
type: concept
course: "测度论"
importance: "A"
tags: [学习, 测度论]
upstream: [单调收敛定理与积分收敛, Lp空间与完备性, 可测函数与收敛模式]
downstream: [泛函分析, 概率论与数理统计, 概率与分析应用-密度与条件期望-change of measure]
status: learning
concept: ["Radon-Nikodym定理", "条件期望", "符号测度"]
prerequisites: ["单调收敛定理与积分收敛", "Lp空间与完备性", "Lebesgue测度与可测集", "符号测度"]
related: ["Lebesgue分解", "Hahn分解", "条件期望", "概率与分析应用-密度与条件期望-change of measure"]
flow: project
kind: concept
template: Obsidian单知识点深度学习模板
created: 2026-08-03
---

# Radon-Nikodym与条件期望

---
## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：Radon-Nikodym（RN）定理是 [[测度论 - HW01：单调收敛定理与 Radon-Nikodym 证明阶梯作业]] 的最终目标（MCT → RN 全链），也是 HW06 的验收核心；条件期望 = RN 定理的直接推论，是概率论（鞅、马尔可夫过程、统计推断）的引擎。证明主线本身是"MCT 构造法"的巅峰示范——值得闭卷重建。

---
## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 概率论里"密度函数 $f_X$"人人都用：$P(X \in A) = \int_A f_X\,dx$。但"密度存在吗？何时存在？"在测度论框架下是个深刻问题：把 $P(X \in \cdot)$ 看成 Lebesgue 测度 $m$ 之外的另一个测度 $\nu$，问的是**两个测度何时可以互相"求导"**：$\nu(E) = \int_E f\,d\mu$ 的 $f$ 何时存在？答案：当且仅当 $\nu \ll \mu$（绝对连续）——这就是 RN 定理。它同时回答：$\nu$ 在 $\mu$ 的零测集上"作弊"（如点质量 $\delta_0$ 对 Lebesgue 测度）时，密度不存在。条件期望 $E[X|\mathcal{G}]$ 则是同一定理换个马甲：在子 $\sigma$ 代数 $\mathcal{G}$ 上"用 $\mathcal{G}$-可测函数逼近 $X$"。

---
## 2. 为什么它重要？它有什么用？

- **连接大图景**：RN 定理收束 HW01-HW06 全链（MCT 证明主线 → RN → 条件期望）；$L^2$ 视角下条件期望 = 正交投影，连接 [[Lp空间与完备性]]；Lebesgue 分解把"任意测度对任意测度"拆成绝对连续 + 奇异两部分。
- **实际应用场景**：概率密度存在性判据、贝叶斯统计（后验密度 = RN 导数）、测度变换（change of measure / Girsanov 定理的测度论根基）、鞅论（条件期望是鞅的定义运算）、强化学习与随机控制（条件期望无处不在）。
- **高频题型/任务**：判断 $\nu \ll \mu$ 是否成立；写出/验证密度 $d\nu/d\mu$；用 RN 证条件期望存在性；证明条件期望性质（塔性质、可测因子提出）；构造"不绝对连续故无密度"的反例；Lebesgue 分解。

---
## 3. 学它之前需要哪些前置知识？

1. **[[单调收敛定理与积分收敛]]**：RN 证明用 MCT 构造密度候选；积分与测度的对应关系 $\nu(E) = \int_E f$。
2. **[[Lp空间与完备性]]**：$L^2$ 方法（Folland 版 RN 证明）与条件期望的投影视角。
3. **[[积分与收敛-符号测度入口-符号测度]]**：符号测度、Jordan 分解 $\nu = \nu^+ - \nu^-$、Hahn 分解、全变差 $|\nu|$——RN 定理的陈述语言。

---
## 4. 用直觉语言解释它

> «RN 定理像"测度界的换汇"：$\mu$ 是美元，$\nu$ 是欧元，汇率 $f = d\nu/d\mu$ 在每个"面额"（集合）上把 $\mu$ 换成 $\nu$——但前提是 $\nu$ 从不"凭空印钱"：$\mu$ 认为零的集合（零测集），$\nu$ 也必须认零，否则汇率不存在。条件期望像"用粗粒度信息的最优估计"：只允许看 $\mathcal{G}$ 这块"模糊玻璃"（子 $\sigma$ 代数）来猜 $X$，$E[X|\mathcal{G}]$ 就是看得见的信息下最好的猜测。»

- **直觉类比/几何图像**：密度 $f = d\nu/d\mu$ 是"逐点汇率"：$\nu(E)$ = 在 $E$ 上按汇率 $f$ 兑换 $\mu$ 的总量。条件期望：$L^2(\Omega)$ 中 $X$ 向闭子空间 $L^2(\mathcal{G})$ 的**正交投影**——最好的 $\mathcal{G}$-可测近似。
- **为什么很自然**：$\nu \ll \mu$ 说"$\nu$ 的零集不细于 $\mu$"，即 $\nu$ 的信息完全由 $\mu$ 决定——有信息就能定价（存在密度）；反例 $\delta_0$：单点 $\{0\}$ 对 $m$ 是零测的，但对 $\delta_0$ 是 1——$\delta_0$ 拥有 $m$ 没有的信息，无法用 $m$ 定价。
- **一句话直觉本质**：**$\nu \ll \mu$（零测集一致）⟺ $\nu$ 可由 $\mu$ 积分"定价"，定价函数即密度 $d\nu/d\mu$（RN 定理）；条件期望 = 在子 $\sigma$ 代数 $\mathcal{G}$ 上看得到的积分信息——$Y$ 是 $\mathcal{G}$-可测且与 $X$ 在 $\mathcal{G}$ 上积分一致，存在性由 RN 保证。**

---
## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义
- **符号测度**：$\nu: \mathcal{M} \to \overline{\mathbb{R}}$ 可数可加（至多取一个 $\pm\infty$）；Jordan 分解 $\nu = \nu^+ - \nu^-$（Hahn 分解 $X = P \cup N$，$\nu^+(E) = \nu(E \cap P)$）；全变差 $|\nu| = \nu^+ + \nu^-$。
- **绝对连续**：$\nu \ll \mu$ ⟺ $\mu(E) = 0 \Rightarrow \nu(E) = 0$。有限测度时等价于 $\varepsilon$-$\delta$ 刻画：$\forall \varepsilon > 0,\ \exists \delta > 0,\ \mu(E) < \delta \Rightarrow |\nu(E)| < \varepsilon$。
- **Radon-Nikodym 定理**：$\mu, \nu$ $\sigma$-有限，$\nu \ll \mu$ ⟹ 存在**唯一**（模 a.e.）可测 $f \ge 0$ 使对一切可测 $E$：$\nu(E) = \int_E f\,d\mu$。记 $f = \dfrac{d\nu}{d\mu}$（RN 导数 / 密度）。
- **条件期望**：概率空间 $(\Omega, \mathcal{F}, P)$，$\mathcal{G} \subset \mathcal{F}$ 子 $\sigma$ 代数，$X \in L^1$。$Y = E[X|\mathcal{G}]$ 是满足以下两条件的（唯一 a.s.）随机变量：(i) $Y$ 是 $\mathcal{G}$-可测；(ii) 对一切 $G \in \mathcal{G}$，$\int_G Y\,dP = \int_G X\,dP$。

### 2. 核心公式
$$\nu \ll \mu \iff \left[\mu(E) = 0 \Rightarrow \nu(E) = 0\right]$$
$$\text{RN:}\ \nu \ll \mu \implies \exists!\, f \ge 0 \text{ 可测}:\ \nu(E) = \int_E f\,d\mu,\ \forall E \in \mathcal{M},\quad f = \frac{d\nu}{d\mu}$$
$$\text{条件期望:}\ Y = E[X|\mathcal{G}] \iff \left[Y \ \mathcal{G}\text{-可测} \ \wedge\ \forall G \in \mathcal{G},\ \int_G Y\,dP = \int_G X\,dP\right]$$

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\nu \ll \mu$ | $\nu$ 对 $\mu$ 绝对连续 | 零测集一致 | 密度的存在条件 |
| $\nu \perp \mu$ | $\nu$ 与 $\mu$ 互异（奇异） | 存在 $A$：$\mu(A)=0=\nu(A^c)$ | 无密度的极端情形 |
| $d\nu/d\mu$ | RN 导数（密度） | 非负可测 | 模 a.e. 唯一 |
| $E[X|\mathcal{G}]$ | 条件期望 | 随机变量 | 不是数！$\mathcal{G}$-可测 |
| $\mathcal{G}$ | 子 $\sigma$ 代数 | 信息量 | $\sigma(X)$ = $X$ 生成的信息 |

### 4. 常见变体与适用条件
- **适用条件**：RN 要求 $\mu, \nu$ $\sigma$-有限；条件期望要求 $X \in L^1$。
- **限制条件**：$\mu$ 非 $\sigma$-有限时 RN 可失败（见第 8 节变式 2）；$\nu \not\ll \mu$ 时无密度。
- **条件变式**：Lebesgue 分解 $\nu = \nu_{ac} + \nu_s$（$\nu_{ac} \ll \mu$，$\nu_s \perp \mu$）；RN 导数链式法则 $\frac{d\nu}{d\lambda} = \frac{d\nu}{d\mu}\frac{d\mu}{d\lambda}$（$\lambda \ll \mu \ll \nu$ 情形）；条件期望的塔性质与 Jensen 不等式。

---
## 6. 推导思路和思想来源

- **最初困难**：两个测度如何"相除"？$d\nu/d\mu$ 想模仿微积分的 $dy/dx$，但 $\nu$ 可能包含 $\mu$ 没有的信息（$\delta_0$ 对 $m$），此时"导数"无意义——必须先刻画"信息可定价"的精确条件。
- **直接方法局限**：试图逐点定义 $f(x) = \lim \nu(B(x,r))/\mu(B(x,r))$ 行不通：密度可以是任意可测函数，逐点比值的极限不存在也不可测。
- **关键"转念"**：**不求"逐点汇率"，改求"全局最优定价函数"**：在集合 $\mathcal{F} = \{f \ge 0 \text{ 可测} : \int_E f\,d\mu \le \nu(E),\ \forall E\}$ 中找"预算用满"的 $f^*$（$\int f^*$ 最大）。每个 $f \in \mathcal{F}$ 是一份"不超支的价目表"；最大者恰好把 $\nu$ 全部定价。
- **推导主线与动机**：
  1. **$\mathcal{F}$ 非空且对 max 封闭**：$f_1, f_2 \in \mathcal{F} \Rightarrow \max(f_1, f_2) \in \mathcal{F}$（对 $E_1 = \{f_1 \ge f_2\}$ 与 $E_1^c$ 分别用不等式相加）。由此可取 $f_n \in \mathcal{F}$ 使 $\int f_n \to a := \sup_{f\in\mathcal{F}}\int f$（有限，因 $\le \nu(X)$），换成 $\tilde f_n = \max(f_1,\dots,f_n) \uparrow$。
  2. **MCT 取极限**：$\tilde f_n \uparrow f^*$，MCT 保 $\int_E \tilde f_n \le \nu(E)$ 于极限：$f^* \in \mathcal{F}$ 且 $\int f^* = a$ 最大。
  3. **平顶矛盾**：令 $\nu_0 = \nu - f^*\mu \ge 0$（非负，因 $f^* \in \mathcal{F}$）。若 $\nu_0 \ne 0$，取 $E$ 使 $\nu_0(E) > 0$；选 $\varepsilon > 0$ 与 $A \subset E$（$\nu_0 - \varepsilon\mu$ 的 Hahn 正集）使 $\nu_0(B) \ge \varepsilon\mu(B)$ 对 $B \subset A$，且 $\nu_0(A) > 0$、$\mu(A) > 0$（后者由 $\nu \ll \mu$：$\mu(A) = 0 \Rightarrow \nu_0(A) = 0$ 矛盾）。则 $f^* + \varepsilon\mathbb{1}_A \in \mathcal{F}$：对任意 $B$，$\int_B(f^* + \varepsilon\mathbb{1}_A) = \int_B f^* + \varepsilon\mu(B\cap A) \le \int_B f^* + \nu_0(B\cap A) \le \nu(B)$。但 $\int(f^* + \varepsilon\mathbb{1}_A) = \int f^* + \varepsilon\mu(A) > \int f^*$——与最大性矛盾。故 $\nu_0 = 0$，即 $\nu(E) = \int_E f^*\,d\mu$。
  4. **唯一性**：若 $f, g$ 都满足，$\int_E(f-g) = 0$ 对一切 $E$，取 $E = \{f > g\}$ 得 $f \le g$ a.e.，对称得 $f = g$ a.e.。$\sigma$-有限情形用可数个有限测度块拼装。
- **条件期望的存在性 = RN 推论**：固定 $\mathcal{G}$，定义符号测度 $\nu(G) = \int_G X\,dP$（$G \in \mathcal{G}$），它关于 $P|_\mathcal{G}$ 绝对连续（$P(G)=0 \Rightarrow \nu(G)=0$）；RN 给出 $\mathcal{G}$-可测 $Y$ 使 $\nu(G) = \int_G Y\,dP$——正是条件期望两条公理。**一条定理，两副面孔。**
- **为什么自然得到此结论**：max 封闭 + MCT = "上确界可被单调逼近"，这是 [[单调收敛定理与积分收敛]] 精神的正用；"平顶加价"是"最优性 ⟹ 预算耗尽"的经济学直觉——**RN 的证明本质是变分法**。

---
## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）
- **题目**：$X = [0,1]$，$m$ 为 Lebesgue 测度，$\nu(E) = \int_E x\,dm$。求 $d\nu/dm$ 并验证。
- **解题思路与关键步骤**：显然 $\nu \ll m$（零测集上积分为 0），RN 导数即被积函数 $f(x) = x$。验证：$\nu([0, 1/2]) = \int_0^{1/2} x\,dx = 1/8$；用密度：$\int_{[0,1/2]} x\,dm = 1/8$ ✓。
- **最终答案**：$d\nu/dm = x$，$\nu([a,b]) = (b^2 - a^2)/2$。
- **易错点**：把"$\nu \ll \mu$ 存在密度"与"密度连续"混为一谈——$f$ 只需可测，$\mathbb{1}_A$ 这类不连续函数同样合法。
- **🤔 追问**：若 $\nu(E) = \int_E \mathbb{1}_{\mathbb{Q}\cap[0,1]}\,dm$？——$\nu \equiv 0$（被积函数 a.e. 为 0），密度 a.e. 为 0。

### 例子 2：中等例子（条件判断与多步推理）
- **题目与完整解答**：$X, Y$ 为离散随机变量，$X \in \{a_1, a_2\}$ 各以概率 $1/2$，$\mathcal{G} = \sigma(X)$。求 $E[Y|\mathcal{G}]$。$\mathcal{G}$-可测函数必形如 $c_1\mathbb{1}_{\{X=a_1\}} + c_2\mathbb{1}_{\{X=a_2\}}$；由公理 (ii) 在 $\{X = a_i\}$ 上：$c_i P(X = a_i) = \int_{\{X=a_i\}} Y\,dP = E[Y \cdot \mathbb{1}_{\{X=a_i\}}]$，故 $c_i = E[Y | X = a_i]$（经典条件期望）。**结论**：$E[Y|\mathcal{G}] = E[Y|X=a_1]\mathbb{1}_{\{X=a_1\}} + E[Y|X=a_2]\mathbb{1}_{\{X=a_2\}}$——离散情形的条件期望是"按 $X$ 的取值逐块取平均"，$\mathcal{G}$-可测性就是"只依赖 $X$ 的信息"。

### 例子 3：实际应用 + 反例——非绝对连续时无密度
- **题目**：$\nu = \delta_0$（Dirac 点质量）于 $(\mathbb{R}, \mathcal{B}, m)$。$\nu \ll m$ 是否成立？密度存在吗？
- **关键步骤**：$m(\{0\}) = 0$ 但 $\nu(\{0\}) = 1$，故 $\nu \not\ll m$。若存在 $f$ 使 $\nu(E) = \int_E f\,dm$，取 $E = \{0\}$：$1 = \nu(\{0\}) = \int_{\{0\}} f\,dm = 0$，矛盾。
- **反例结论**：**点质量对 Lebesgue 测度无密度**——$\delta_0$ 拥有 $m$ 看不到的信息（"$x$ 恰为 0"是 $m$-零测事件）。更强的反例：Cantor 测度 $\mu_C$（Cantor 集上均匀分布）不绝对连续于 $m$（$\mu_C(C^c) = 0$ 而 $m(C^c) = 1$，即 $\mu_C \perp m$），但 $\mu_C(\{x\}) = 0$ 对单点——"无密度"不能靠单点检测，这正是奇异连续测度。**在统计里这解释"为什么有些分布（如 Cantor 型）没有密度函数"。**

---
## 8. 常见误区和易混概念

### 误区 1：以为"$\nu \ll \mu$ 就是 $\nu(E) \le \mu(E)$ 对一切 $E$"
- **错误直觉**：绝对连续 = 点态小。
- **为什么错**：$\nu = 2\mu$ 满足 $\nu \ll \mu$（零测集一致）但 $\nu(E) = 2\mu(E) > \mu(E)$。
- **正确理解**：$\nu \ll \mu$ 只约束**零测集**；大小关系由密度 $f = d\nu/d\mu$ 的取值决定（$f$ 可任意大）。

### 误区 2：以为"$E[X|\mathcal{G}]$ 是一个数"
- **错误直觉**：条件期望 = "给定 $X = x$ 时的平均"，是个数值。
- **为什么错**：$\mathcal{G}$ 只给"部分信息"（如只看 $X$ 的符号），$E[X|\mathcal{G}]$ 必须对每个 $\mathcal{G}$-事件取平均——整体是一个 $\mathcal{G}$-可测**随机变量**。
- **正确理解**：离散情形它是"逐块常数"的变量；$E[X]$ 是 $E[X|\{\emptyset,\Omega\}]$ 的特例（平凡 $\sigma$ 代数，信息为 0）。

### 条件变式（本路径特色）
- **变式 1（$\sigma$-有限条件必要）**：取 $\mu$ 为计数测度于 $[0,1]$（非 $\sigma$-有限）、$\nu = m$（Lebesgue 限制）：$\nu \ll \mu$（$\mu(E) = 0 \Rightarrow E = \emptyset \Rightarrow \nu(E) = 0$）但无密度——任何 $f$ 给 $\int_{\{x\}} f\,d\mu = f(x)$，而 $\nu(\{x\}) = 0$，推得 $f \equiv 0$，矛盾于 $\nu \ne 0$。**$\sigma$-有限性是硬条件。**
- **变式 2（Lebesgue 分解）**：去掉绝对连续：$\nu = \nu_{ac} + \nu_s$ 唯一分解，$\nu_{ac} \ll \mu$、$\nu_s \perp \mu$——$\delta_0 = 0 + \delta_0$，纯奇异部分。
- **变式 3（条件期望版本）**：塔性质 $E[E[X|\mathcal{G}_1]|\mathcal{G}_2] = E[X|\mathcal{G}_2]$（$\mathcal{G}_2 \subset \mathcal{G}_1$）；可测因子提出 $E[ZX|\mathcal{G}] = ZE[X|\mathcal{G}]$（$Z$ $\mathcal{G}$-可测有界）；条件 Jensen：$\varphi$ 凸 ⟹ $E[\varphi(X)|\mathcal{G}] \ge \varphi(E[X|\mathcal{G}])$；条件 MCT/DCT 对 $\mathcal{G}$ 逐点成立。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| $\nu \ll \mu$ | 零测集一致 | 密度存在（RN） | 密度存在性判据 |
| $\nu \perp \mu$ | 支撑互斥 | 无密度（最坏情形） | $\delta_0$、Cantor 测度 |
| 密度 $d\nu/d\mu$ | 逐点汇率 | 模 a.e. 唯一 | 测度变换、贝叶斯 |
| 条件期望 $E[X|\mathcal{G}]$ | 信息受限的最优估计 | 是变量不是数 | 鞅、统计推断 |

---
## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[单调收敛定理与积分收敛]]：RN 证明用 MCT 构造密度；HW01 证明阶梯的顶点。
- [[Lp空间与完备性]]：$L^2$ 投影视角的条件期望（Folland 版 RN 证明）。
- [[积分与收敛-符号测度入口-符号测度]]：Jordan/Hahn 分解是陈述与证明的语言。

### 下游延伸
- [[概率与分析应用-密度与条件期望-条件期望]]：原子卡层面的条件期望性质与应用。
- [[概率与分析应用-密度与条件期望-change of measure]]：测度变换 = RN 导数的工程应用（Girsanov 的思想源头）。
- [[概率与分析应用-密度与条件期望-密度]]：密度与分布函数的对应。

### 横向关联
- [[概率与分析应用-密度与条件期望-绝对连续]] ↔ 本知识点：绝对连续原子卡与本卡定理陈述互证。
- [[Lp空间与结构-对偶与结构-线性泛函]] ↔ 本知识点：$L^2$ 上 $\nu \mapsto \int f\,d\nu$ 的对偶配对即 RN 导数的函数观。
- [[02-Knowledge/🧠 学习系统/27-泛函分析/🗺️ 泛函分析学习路径|泛函分析]]：RN 定理是 Riesz 表示定理的测度版。

### 应用场景
- [[🧭 开源作业体系-测度论]]：HW01（RN 证明阶梯）与 HW06（RN → 条件期望 + 定理依赖图 Capstone）。
- [[测度论 - HW01：单调收敛定理与 Radon-Nikodym 证明阶梯作业]]：本卡的证明主线对应其 L2 → L3 台阶。
- [[🚀 第四阶段：概率与分析应用]]：条件期望进入鞅论与统计推断。

---
## 10. 闭卷复现任务

合上笔记后，请独立完成：
- [ ] **闭卷复述定义**：写出绝对连续定义、RN 定理完整陈述（含 $\sigma$-有限与唯一性）、条件期望两条公理。
- [ ] **闭卷重建证明**：重建 RN 证明主线（$\mathcal{F}$ 集合 → max 封闭 → MCT 取 $f^*$ → 平顶 $\varepsilon\mathbb{1}_A$ 矛盾 → 唯一性）。
- [ ] **默写反例**：默写 $\delta_0$ 对 $m$ 无密度（$1 = \nu(\{0\}) \ne \int_{\{0\}} f\,dm = 0$）；说出 Cantor 测度为什么是更强反例。
- [ ] 从 RN 定理推出条件期望存在性（$\nu(G) = \int_G X\,dP$ 关于 $P|_\mathcal{G}$）。
- [ ] 写出条件期望五大性质（线性、塔、可测因子、Jensen、条件 DCT）。

---
## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 绝对连续 vs 奇异 |
| 2 | 公式运用 | 基础 | 由密度算测度 |
| 3 | 条件判断 | 中等 | RN 定理条件与失效 |
| 4 | 证明题 | 较难 | RN 导数唯一性 |
| 5 | 反例构造 | 较难 | 非绝对连续无密度 |

### 题目与解析

#### 1. 判断：$\nu(E) = \int_E x^2\,dm$（$E \subset [0,1]$）是否绝对连续于 $m$？$\delta_0$ 呢？
> [!question]- 答案解析
> - **答案**：$\nu \ll m$（$m(E) = 0 \Rightarrow \int_E x^2 = 0$），密度 $d\nu/dm = x^2$；$\delta_0 \not\ll m$（$m(\{0\}) = 0$ 但 $\delta_0(\{0\}) = 1$）。
> - **解析**：绝对连续只看零测集；积分定义的测度自动绝对连续。
> - **易错原因**：用"$\nu$ 是否小于 $\mu$"判断绝对连续。
> - **Obsidian 标签建议**：`#自测题/基础`

#### 2. 设 $d\nu/dm = x^2$ 于 $[0,1]$，求 $\nu([0, 1/2])$。
> [!question]- 答案解析
> - **答案**：$\nu([0,1/2]) = \int_0^{1/2} x^2\,dx = [x^3/3]_0^{1/2} = 1/24$。
> - **解析**：密度积分的直接代入；$m$ 限制到 $[0,1]$ 与普通 Riemann 积分一致。
> - **易错原因**：忘记先验证 $\nu \ll m$ 再套 RN（本例显然成立）。

#### 3. 判断：$\mu$ 为 $[0,1]$ 上计数测度（非 $\sigma$-有限），$\nu = m$ 限制。$\nu \ll \mu$ 吗？RN 定理为何不适用？
> [!question]- 答案解析
> - **答案**：$\nu \ll \mu$（$\mu(E) = 0 \Rightarrow E = \emptyset$）；但 $\mu$ 非 $\sigma$-有限，RN 定理结论失败：若 $\nu(E) = \int_E f\,d\mu$，取 $E = \{x\}$ 得 $0 = \nu(\{x\}) = f(x)$ 对一切 $x$，则 $\nu \equiv 0$，矛盾。
> - **解析**：$\sigma$-有限性是 RN 的硬条件；计数测度"太细"，Lebesgue 测度"太粗"，无法互相定价。
> - **易错原因**：只验证 $\nu \ll \mu$ 就断言密度存在。
> - **Obsidian 标签建议**：`#自测题/中等`

#### 4. 证明题：证明 RN 导数的唯一性：若 $f, g \ge 0$ 都可测且 $\int_E f\,d\mu = \int_E g\,d\mu$ 对一切可测 $E$，则 $f = g$ a.e.。
> [!question]- 答案解析
> - **答案**：设 $E = \{f > g\}$，则 $0 = \int_E f - \int_E g = \int_E (f - g) \ge 0$，故 $\int_E (f-g) = 0$，而 $E$ 上 $f - g > 0$，得 $\mu(E) = 0$；对称地 $\mu\{f < g\} = 0$。故 $f = g$ a.e.。
> - **解析**：非负函数在正集合上的积分为 0 ⟹ 集合零测——这是"积分决定函数（a.e.）"的标准杠杆。
> - **易错原因**：忘记先取 $E = \{f > g\}$（可测性由 $f, g$ 可测保证），直接断言逐点相等。
> - **Obsidian 标签建议**：`#自测题/较难`

#### 5. 反例构造：构造 $\nu \not\ll m$（$m$ 为 Lebesgue 测度）并证明 $\nu$ 无密度；再举一个 $\nu(\{x\}) = 0$ 对单点却仍无密度的例子。
> [!question]- 答案解析
> - **答案**：$\nu = \delta_0$：$m(\{0\}) = 0$，$\nu(\{0\}) = 1$，故 $\nu \not\ll m$；若 $\nu(E) = \int_E f\,dm$，取 $E = \{0\}$ 得 $1 = 0$，矛盾。更强反例：Cantor 测度 $\mu_C$：$\mu_C \perp m$（Cantor 集 $C$：$m(C) = 0$ 而 $\mu_C(C) = 1$），故无密度，但 $\mu_C(\{x\}) = 0$ 对每个单点——无密度不能靠"单点质量"检测。
> - **解析**：奇异连续测度"把质量放在零测但稠密的 Cantor 集上"，是 $\delta_0$ 与 Lebesgue 之间的第三形态。
> - **易错原因**：以为"无密度 ⟺ 存在单点正质量"。
> - **Obsidian 标签建议**：`#自测题/较难`

---
## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

### 我的推导复现
> 不看上文，尝试写出 RN 证明主线（$\mathcal{F}$ 最大元 + 平顶矛盾）与条件期望存在性推导：

### 我的错误与卡点
-

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---
## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/25-测度论/`
- **关联已有笔记**：[[🧭 开源作业体系-测度论]]（HW01/HW06）、[[测度论 - HW01：单调收敛定理与 Radon-Nikodym 证明阶梯作业]]、[[单调收敛定理与积分收敛]]、[[Lp空间与完备性]]、[[概率与分析应用-密度与条件期望-条件期望]]
- **建议标签**：`#学习` `#测度论` `#概念`
- **拆分建议**：条件期望性质（塔性质、Jensen、条件 DCT）自成体系，若概率论课程深入可拆出"条件期望运算手册"题型笔记；RN 证明主线已由 HW01 说明书承载，本卡保持概念级。
