---
title: "MANOVA"
date: "2026-08-04"
type: study
course: "多元统计"
importance: "A"
tags: [学习, 多元统计]
upstream: ["Hotelling T² 检验", "均值向量与协方差矩阵估计"]
downstream: ["判别分析：LDA与QDA", "多重比较与检验校正"]
status: learning
proof_mode: true
concept: ["MANOVA", "SSCP 矩阵", "Wilks' Lambda", "多元方差分析"]
sources:
  - "Penn State STAT 505 Lesson 8 (Multivariate Analysis of Variance; Test Statistics for MANOVA; Two-way MANOVA)"
---

# MANOVA

---

> **⏱ 预计耗时**：45–60 分钟（第 0-6 节理解 + 第 7 节例子 + 第 10/11 节闭卷自测）
> **🎯 行为目标**：完成本卡后，
> - **学完你能**：
>   - 精确复述定义与定理（量词一个不差）；
>   - 不看笔记重建证明主线并指出关键"转念"；
>   - 独立构造 1 个反例并说明哪个条件不能省；
>   - 对 2 个条件变式给出成立/不成立的判断。

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**——MANOVA 是 ANOVA 的多元推广，是比较多个组均值向量的标准工具。
- **判断理由**：MANOVA 的 SSCP 分解、四种检验统计量（Wilks' Lambda、Pillai、Hotelling-Lawley、Roy）、假设检验流程是多元推断的核心；判别分析依赖 MANOVA 的组间差异度量。不挖透，多组比较与判别分类都缺根基。
- **验收模式说明**：本卡验收看「定义复述、证明重建、反例、条件变式、闭卷验收」五项。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 一元 ANOVA 比较多个组的一个变量均值（$F$ 检验）。但陶器数据（Pottery data）有 5 个化学成分变量、分 4 个考古遗址组——要同时比较多个组的**多个变量均值**。逐变量 ANOVA 忽略相关性与多重比较问题。问题：怎么构造一个综合的多元组间比较？

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：不学它，判别分析（组间差异最大方向）、正交对比、双因素 MANOVA 都无法建立；它是"多元方差分析"的总纲。
- **实际应用场景**：生物医学多指标组间比较、市场细分、工业质量的多变量工艺比较。
- **高频考点**：SSCP 分解（总=组间+组内）；Wilks' Lambda 与 $F$ 近似；四种检验统计量选择；假设检验（正态、等协方差、独立性）。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景（各 200 字以内）：

1. **[[Hotelling T² 检验]]**：两样本 T² 是 MANOVA 的特例（两组）。
2. **[[多元正态分布与性质]]**：各组正态假设；Wishart 分布。

---

## 4. 定义复述

### 1. 精确定义

设 $g$ 个组，组 $k$ 有 $n_k$ 个观测，总样本量 $n=\sum n_k$，$\bar{\mathbf{x}}_k$ 为组均值，$\bar{\mathbf{x}}$ 为总均值。

**SSCP 分解**：$\mathbf{T}=\mathbf{B}+\mathbf{W}$，其中
$$\mathbf{T}=\sum_{k=1}^{g}\sum_{j=1}^{n_k}(\mathbf{x}_{kj}-\bar{\mathbf{x}})(\mathbf{x}_{kj}-\bar{\mathbf{x}})'\quad(\text{总}),$$
$$\mathbf{B}=\sum_{k=1}^{g}n_k(\bar{\mathbf{x}}_k-\bar{\mathbf{x}})(\bar{\mathbf{x}}_k-\bar{\mathbf{x}})'\quad(\text{组间}),$$
$$\mathbf{W}=\sum_{k=1}^{g}\sum_{j=1}^{n_k}(\mathbf{x}_{kj}-\bar{\mathbf{x}}_k)(\mathbf{x}_{kj}-\bar{\mathbf{x}}_k)'\quad(\text{组内}).$$

**检验**：$H_0:\boldsymbol\mu_1=\cdots=\boldsymbol\mu_g$，常用统计量：
- **Wilks' Lambda**：$\Lambda=\frac{|\mathbf{W}|}{|\mathbf{T}|}=\frac{|\mathbf{W}|}{|\mathbf{B}+\mathbf{W}|}$
- **Pillai's Trace**：$V=\operatorname{tr}[\mathbf{W}^{-1}\mathbf{B}]$ 的变形 $\sum\frac{\lambda_i}{1+\lambda_i}$
- **Hotelling-Lawley**：$U=\operatorname{tr}[\mathbf{W}^{-1}\mathbf{B}]$
- **Roy's Largest Root**：$\theta_1$（$\mathbf{W}^{-1}\mathbf{B}$ 最大特征值）

其中 $\lambda_i$ 是 $\mathbf{W}^{-1}\mathbf{B}$ 的特征值。

### 2. 等价形式

| 形式 | 表述 | 适用场景 |
| :--- | :--- | :--- |
| Wilks | $|\mathbf{W}|/|\mathbf{T}|$ | 最常用 |
| Pillai | $\sum\lambda_i/(1+\lambda_i)$ | 稳健，样本不均衡 |
| Roy | 最大根 | 单方向强分离 |
| Hotelling-Lawley | $\sum\lambda_i$ | 经典 |

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $g,n_k$ | 组数、组样本量 | 正整数 | $\sum n_k=n$ |
| $\mathbf{T},\mathbf{B},\mathbf{W}$ | SSCP 矩阵 | $p\times p$ 对称半正定 | 分解 |
| $\Lambda$ | Wilks' Lambda | $(0,1]$ | 越小差异越大 |
| $\lambda_i$ | $\mathbf{W}^{-1}\mathbf{B}$ 特征值 | $\ge0$ | 判别根 |

---

## 5. 直觉与图像

- **直觉类比/几何图像**：ANOVA 把总平方和拆成"组间+组内"；MANOVA 把标量平方和换成**矩阵**（SSCP），Wilks' Lambda = "组内散布体积 ÷ 总散布体积"——比值越小，说明组间差异占主导。$\mathbf{W}^{-1}\mathbf{B}$ 的特征值像"判别维度"上的组间/组内信号比。
- **为什么很自然**：$H_0$ 下 $\mathbf{B}$ 相对 $\mathbf{W}$ 应该很小，$|\mathbf{W}|/|\mathbf{B}+\mathbf{W}|$ 接近 1；组间差异大时 $\mathbf{B}$ 使分母膨胀，$\Lambda\to0$。
- **一句话直觉本质**：MANOVA 比较"组间散布体积"与"总散布体积"，Wilks' Lambda 是两者的比值；判别根 $\lambda_i$ 是多元信号强度的度量。

> ⚠️ 直觉只是导航，不是证明。任何直觉表述都要能回到第 4 节的精确定义。

---

## 6. 定理陈述与证明重建

### 1. 定理陈述

**定理（Wilks' Lambda 的分布）**：$H_0$（各组均值相等、正态、等协方差）下，
$$\Lambda=\frac{|\mathbf{W}|}{|\mathbf{T}|}\sim \Lambda(p, n-g, g-1),$$
可用 Bartlett 近似 $-\ln\Lambda$ 变换为 $\chi^2$：
$$-\left(n-1-\frac{p+g}{2}\right)\ln\Lambda\ \dot\sim\ \chi^2_{p(g-1)}.$$

**前提**：正态、$\boldsymbol\Sigma_1=\cdots=\boldsymbol\Sigma_g$、独立性。
**结论**：Wilks 分布（或 $\chi^2$ 近似）。
**出处**：STAT 505 L8.3。

### 2. 证明主线（骨架）

- **第 1 步（SSCP 分解）**：$\mathbf{T}=\mathbf{B}+\mathbf{W}$（组内与组间交叉项为零），自由度 $n-1=(g-1)+(n-g)$。
- **第 2 步（独立性）**：正态假设下 $\mathbf{W}\sim W_p(n-g,\boldsymbol\Sigma)$ 与 $\mathbf{B}\sim W_p(g-1,\boldsymbol\Sigma)$（在 $H_0$ 下）独立。
- **第 3 步（Lambda 的似然比性质）**：$\Lambda=|\mathbf{W}|/|\mathbf{T}|$ 是"等均值"约束下似然比检验统计量；由两个独立 Wishart 的行列式比得到 Wilks 分布。
- **第 4 步（$\chi^2$ 近似）**：Wilks 分布与 $\chi^2$ 的关系 $-\ln\Lambda\approx\chi^2_{p(g-1)}/(n)$，Bartlett 修正改进有限样本精度。
- **关键"转念"**：把"多组多元均值检验"翻译成"两个独立 Wishart 行列式之比"——矩阵版的 $F$ 检验，Wilks 分布是 $F$ 的多元推广。

### 3. 证明重建检查

> 合上笔记，独立写出完整证明，然后对照：
> - [ ] 每一步的根据（SSCP 分解、Wishart 独立性、似然比）是否写全？
> - [ ] 量词与边界情形（自由度 $n-g,g-1$）是否处理？
> - [ ] 哪一步是我默写时卡住的？卡点原因是什么？

### 4. 证明技巧迁移

- "SSCP 分解"：迁移到回归的多元 F 检验、重复测量 MANOVA。
- "Wilks → $\chi^2$ 近似"：迁移到似然比检验的一般渐近。

---

## 7. 经典反例库

> 数学的边界由反例划定。每个反例回答一个问题：「这个条件能省吗？」

### 反例 1：逐变量 ANOVA ≠ MANOVA

- **问题**：对每个变量分别做 ANOVA 可以替代 MANOVA 吗？
- **反例构造**：$p=2$，变量强相关，每个变量单独 ANOVA 不显著，但联合 MANOVA 显著（组间差异沿相关主轴）。
- **结论崩塌点**：忽略相关结构 + 多重比较膨胀第一类错误。

### 反例 2：协方差不等时检验失真

- **问题**：$\boldsymbol\Sigma_1\neq\boldsymbol\Sigma_2$ 时 Wilks' Lambda 还可靠吗？
- **反例构造**：一组方差远大于另一组，$H_0$ 下 $\Lambda$ 分布偏移，拒绝率异常（需 Box's M 检验先检查等协方差）。
- **教训**：等协方差假设是精确分布的前提。

### 反例 3：样本不均衡时 Roy's 根偏激进

- **问题**：样本量严重不均衡时选哪种统计量？
- **反例构造**：$n_1=50,n_2=5$：Roy's Largest Root 对"单方向差异"敏感但可能错过其他方向，Pillai 更稳健。
- **教训**：统计量选择依赖数据结构。

---

## 8. 条件变式

> 把条件改一改，结论还成立吗？

| 变式 | 条件改动 | 结论变化 | 成立/不成立 | 依据（证明或反例） |
| :--- | :--- | :--- | :---: | :--- |
| 弱化 1 | 逐变量 ANOVA | 漏联合差异 | 不成立 | 反例 1 |
| 加强 1 | 等协方差 | Wilks 精确 | 成立 | 定理 |
| 换条件 1 | 协方差不齐 | 分布偏移 | 不成立 | 反例 2 |
| 有限→无限 | 双因素 | 需交互项 SSCP | 成立 | STAT505 L8.9 |
| 换空间 | 非正态 | 置换 MANOVA | 成立 | 非参数方法 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[Hotelling T² 检验]]：两组情形。
- [[均值向量与协方差矩阵估计]]：SSCP。

### 下游延伸
- [[判别分析：LDA与QDA]]：用组间差异构造分类方向。
- [[多重比较与检验校正]]：MANOVA 显著后的事后比较。

### 横向关联
- [[Hotelling T² 检验]] ↔ [[MANOVA]]：MANOVA 是多组 T² 的推广。

---

## 10. 闭卷验收（数学模式）

合上笔记，独立完成以下 5 项：

- [ ] **定义复述**：写出 SSCP 分解与四种检验统计量。
- [ ] **定理陈述**：陈述 Wilks' Lambda 分布与 $\chi^2$ 近似。
- [ ] **证明重建**：写出 SSCP 分解 + Wishart 独立的证明主线。
- [ ] **反例复现**：构造逐变量 ANOVA 失效的反例。
- [ ] **条件变式**：对 2 个变式给出成立/不成立的判断与依据。

---

## 11. 分级习题

> [!important] 先闭卷作答，再展开核对
> 合上笔记独立完成下列题目；**全部写完后再逐题展开答案对照**。
> 直接看答案 = 测试效应归零，等于没练。

题目来源标注教材章节或 OCW 作业编号；解答独立完成，复盘阶段才对照。

| 题号 | 类型 | 难度 | 来源 | 考查点 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 定义复述/判断题 | 基础 | STAT505 L8.2 | SSCP 分解 |
| 2 | 简单证明 | 基础 | STAT505 L8.3 | Wilks 计算 |
| 3 | 构造/反例 | 中等 | STAT505 L8.4 | 假设检查 |
| 4 | 综合证明 | 中等 | STAT505 L8.5 | Pottery 数据分析 |
| 5 | 开放/研究型 | 较难 | STAT505 L8.9 | 双因素 MANOVA |

### 题目与解析

#### 1. 解释 $\mathbf{T}=\mathbf{B}+\mathbf{W}$ 并给出自由度
> [!question]- 答案与解析（复盘阶段查看）
> - **答案/证明**：$\mathbf{T}$ 自由度 $n-1$，$\mathbf{B}$ 自由度 $g-1$，$\mathbf{W}$ 自由度 $n-g$；交叉项 $\sum_k n_k(\bar{\mathbf{x}}_k-\bar{\mathbf{x}})(\bar{\mathbf{x}}_{kj}-\bar{\mathbf{x}}_k)'=0$。
> - **解析**：方差分解的矩阵版。
> - **易错原因**：忘记交叉项为零的原因（组内均值差和为零）。

#### 2. 计算给定 SSCP 的 Wilks' Lambda
> [!question]- 答案与解析（复盘阶段查看）
> - **答案/证明**：$|\mathbf{W}|/|\mathbf{T}|$；例：$\mathbf{W}=\begin{pmatrix}10&0\\0&5\end{pmatrix},\mathbf{B}=\begin{pmatrix}40&0\\0&20\end{pmatrix}$ ⟹ $\Lambda=\frac{50}{300}\approx0.167$。
> - **解析**：行列式之比。
> - **易错原因**：误用迹之比。

#### 3. 列出 MANOVA 的三大假设并说明检查方法
> [!question]- 答案与解析（复盘阶段查看）
> - **答案/证明**：①多元正态（Q-Q 图/$\chi^2$ 图）；②等协方差（Box's M）；③独立性（实验设计）；违反时考虑变换或稳健方法。
> - **解析**：STAT 505 L8.4。
> - **易错原因**：跳过 Box's M。

#### 4. 分析 Pottery 数据：5 变量 4 组的 MANOVA 流程
> [!question]- 答案与解析（复盘阶段查看）
> - **答案/证明**：计算 $\mathbf{W},\mathbf{B}$，$\Lambda$，Bartlett 近似 $\chi^2$，拒绝 $H_0$（$p<0.05$），再做正交对比定位组差异。
> - **解析**：STAT 505 L8.5 完整案例。
> - **易错原因**：拒绝后不做事后分析。

#### 5. 说明双因素 MANOVA 的 SSCP 分解
> [!question]- 答案与解析（复盘阶段查看）
> - **答案/证明**：$\mathbf{T}=\mathbf{B}_A+\mathbf{B}_B+\mathbf{B}_{AB}+\mathbf{W}$，对应主效应 A、B、交互、误差四项 SSCP。
> - **解析**：可加模型假设。
> - **易错原因**：漏交互项。

---

## 12. 我的主动回忆区

> **用法**：合上笔记，按引导填空。填不出 = 没掌握，回到第 4-6 节重读再重填。写不出来 = 卡点，记入下方。

### 我的闭卷复述
> 复述「MANOVA」的精确定义：
> - 前提条件：______
> - 结论：______
> - 符号含义（至少 3 个）：______

### 我的证明重建
> 不看上文，写出证明主线：
> - 第 1 步：______
> - 关键"转念"：______
> - 我卡住的证明步骤：______（复习重点）

### 我的反例与卡点
- 我构造的反例：______（对应哪个条件不能省）
- 我默写时卡住的步骤：______
- 修正后的理解：______

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/16-多元统计/01-基础矩阵/`
- **关联已有笔记**：`[[🔢 第一阶段：基础矩阵]]`
- **建议标签**：`#学习` `#多元统计` `#题型`
- **拆分建议**：四种检验统计量可拆为独立对比卡。

