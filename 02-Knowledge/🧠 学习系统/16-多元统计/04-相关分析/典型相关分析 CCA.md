---
title: "典型相关分析 CCA"
date: "2026-08-04"
type: concept
course: "多元统计"
importance: "A"
tags: [学习, 多元统计, 相关分析]
upstream: ["多元正态分布与性质", "矩阵代数基础"]
downstream: ["协方差结构检验"]
status: learning
concept: ["典型相关分析", "典型变量", "典型相关系数", "特征分解"]
sources:
  - "Penn State STAT 505 Lesson 13 (Canonical Correlation Analysis; Setting the Stage; Test for Relationship; Estimates; Coefficients; Interpretation)"
---

# 典型相关分析 CCA

---

> **⏱ 预计耗时**：45–60 分钟（第 0-6 节理解 + 第 7 节例子 + 第 10/11 节闭卷自测）
> **🎯 行为目标**：完成本卡后，
> - **学完你能**：
>   - 用一句话说清它解决什么问题（能讲给外行听）；
>   - 不看笔记写出核心公式并解释每个符号；
>   - 手算/口算出至少 1 道基础题；
>   - 说出 2 个常见误区及其正确理解。

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**——CCA 研究两组变量之间的整体相关结构。
- **判断理由**：CCA 是"两组变量间的 PCA"，把相关矩阵的分块结构（$\boldsymbol\Sigma_{12}$）压缩成少数典型相关对；它统一了回归（一组=单变量时退化）、判别（组指示变量时）等许多方法。不挖透，两组变量关联性分析（如健康指标 vs 生活方式）无工具。
- **实际应用场景**：学术成绩 vs 心理特质；销售数据（产品 vs 促销）；基因表达 vs 临床指标。
- **高频题型/任务**：求典型变量与典型相关系数；检验典型相关显著性；解释典型载荷。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 有两组变量 $\mathbf{X}=(X_1,\dots,X_p)$（如 3 个健康指标）与 $\mathbf{Y}=(Y_1,\dots,Y_q)$（如 4 个生活习惯指标），想知道两组之间有没有关联、关联多强。逐对算相关系数有 $p\times q$ 个且忽略组内结构。问题：能不能找到"X 的线性组合"与"Y 的线性组合"，使它们的相关最大，并逐级提取不相关的组合？

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：不学它，两组变量关联分析缺失统一框架；CCA 的广义特征值问题 $\boldsymbol\Sigma_{12}\boldsymbol\Sigma_{22}^{-1}\boldsymbol\Sigma_{21}\mathbf{a}=\lambda\boldsymbol\Sigma_{11}\mathbf{a}$ 是多元分析的核心数学结构。
- **实际应用场景**：行为-健康关联、化学-感官指标关联、多模态数据融合。
- **高频题型/任务**：写典型相关方程组；计算典型变量；检验 $\rho_i=0$（Wilks 型检验）；解释载荷。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景（各 200 字以内）：

1. **[[主成分分析 PCA]]**：特征分解与方差最大化。
2. **[[多元正态分布与性质]]**：分块协方差矩阵与条件分布。

---

## 4. 用直觉语言解释它

- **直觉类比**：找两组变量各自的方向，使它们的线性组合最相关。
- **一句话直觉本质**：CCA = 两组变量之间的“PCA”，通过广义特征分解提取典型相关对。

---

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义

设 $\mathbf{Z}=\begin{pmatrix}\mathbf{X}\\\mathbf{Y}\end{pmatrix}\sim N_{p+q}(\boldsymbol\mu,\boldsymbol\Sigma)$，$\boldsymbol\Sigma=\begin{pmatrix}\boldsymbol\Sigma_{11}&\boldsymbol\Sigma_{12}\\\boldsymbol\Sigma_{21}&\boldsymbol\Sigma_{22}\end{pmatrix}$。

**第一对典型变量**：找 $\mathbf{a},\mathbf{b}$ 使 $\rho=\operatorname{Corr}(\mathbf{a}'\mathbf{X},\mathbf{b}'\mathbf{Y})$ 最大：
$$\rho_1=\max_{\mathbf{a},\mathbf{b}}\frac{\mathbf{a}'\boldsymbol\Sigma_{12}\mathbf{b}}{\sqrt{\mathbf{a}'\boldsymbol\Sigma_{11}\mathbf{a}}\sqrt{\mathbf{b}'\boldsymbol\Sigma_{22}\mathbf{b}}}.$$

后续典型对与前面所有对不相关，依次最大化。

### 2. 核心公式

$\mathbf{a},\mathbf{b}$ 满足广义特征方程：
$$\boldsymbol\Sigma_{11}^{-1}\boldsymbol\Sigma_{12}\boldsymbol\Sigma_{22}^{-1}\boldsymbol\Sigma_{21}\mathbf{a}=\rho^2\mathbf{a},\qquad \boldsymbol\Sigma_{22}^{-1}\boldsymbol\Sigma_{21}\boldsymbol\Sigma_{11}^{-1}\boldsymbol\Sigma_{12}\mathbf{b}=\rho^2\mathbf{b}.$$

典型相关数 $=\min(p,q)$；第 $k$ 个典型相关系数 $\rho_k$ 是 $\boldsymbol\Sigma_{11}^{-1}\boldsymbol\Sigma_{12}\boldsymbol\Sigma_{22}^{-1}\boldsymbol\Sigma_{21}$ 的第 $k$ 大特征值的平方根。

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\boldsymbol\Sigma_{ij}$ | 协方差分块 | $p\times q$ 等 | $\boldsymbol\Sigma_{12}'=\boldsymbol\Sigma_{21}$ |
| $\mathbf{a},\mathbf{b}$ | 典型载荷 | $\mathbb{R}^p,\mathbb{R}^q$ | 单位方差约束 |
| $\rho_k$ | 典型相关系数 | $[0,1]$ | 降序 |
| $U_k,V_k$ | 典型变量 | 标量 | $\mathbf{a}_k'\mathbf{X},\mathbf{b}_k'\mathbf{Y}$ |

### 4. 常见变体与适用条件

- **适用条件**：两组变量，各 $\ge2$ 维；正态假设用于显著性检验。
- **限制条件**：$\boldsymbol\Sigma_{11},\boldsymbol\Sigma_{22}$ 需可逆；典型变量解释困难（同 PCA）；小样本不稳。

---

## 6. 推导思路和思想来源

- **最初困难**：$p\times q$ 个相关系数杂乱无章。
- **直接方法局限**：最大化 $\operatorname{Corr}(\mathbf{a}'\mathbf{X},\mathbf{b}'\mathbf{Y})$ 是带两个约束的优化。
- **关键"转念"**：先标准化（令 $\operatorname{Var}(\mathbf{a}'\mathbf{X})=\operatorname{Var}(\mathbf{b}'\mathbf{Y})=1$），最大化 $\mathbf{a}'\boldsymbol\Sigma_{12}\mathbf{b}$；用拉格朗日乘子求导，得到**广义特征方程**——两组各自的"主轴"通过交叉协方差耦合。
- **推导主线与动机**：两约束拉格朗日 ⟹ $\boldsymbol\Sigma_{12}\mathbf{b}=\lambda\boldsymbol\Sigma_{11}\mathbf{a}$ 与 $\boldsymbol\Sigma_{21}\mathbf{a}=\lambda\boldsymbol\Sigma_{22}\mathbf{b}$ ⟹ 消去 $\mathbf{b}$ 得 $\boldsymbol\Sigma_{11}^{-1}\boldsymbol\Sigma_{12}\boldsymbol\Sigma_{22}^{-1}\boldsymbol\Sigma_{21}\mathbf{a}=\rho^2\mathbf{a}$。
- **为什么自然得到此结论**：$\rho^2$ 作为广义特征值出现——"最大相关"问题天然是谱问题，与 PCA 同构但交叉耦合。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）
- **题目**：$\boldsymbol\Sigma_{11}=\boldsymbol\Sigma_{22}=I$，$\boldsymbol\Sigma_{12}=\begin{pmatrix}0.8&0\\0&0.3\end{pmatrix}$。
- **解题思路与关键步骤**：$\boldsymbol\Sigma_{11}^{-1}\boldsymbol\Sigma_{12}\boldsymbol\Sigma_{22}^{-1}\boldsymbol\Sigma_{21}=\boldsymbol\Sigma_{12}\boldsymbol\Sigma_{12}'=\operatorname{diag}(0.64,0.09)$；特征值 $0.64,0.09$。
- **最终答案**：$\rho_1=0.8$（$U_1=X_1,V_1=Y_1$），$\rho_2=0.3$。
- **易错点**：忘记 $\rho$ 是特征值平方根。

### 例子 2：中等例子（条件判断与多步推理）
- **题目与完整解答**：Sales 数据（产品销量 3 变量 vs 促销投入 3 变量）：计算样本 $\mathbf{S}_{ij}$，广义特征分解得 $\hat\rho_1=0.9,\hat\rho_2=0.5$；Wilks 检验 $\rho_1$ 显著、$\rho_2$ 不显著，保留第一对典型变量解释。

### 例子 3：实际应用例子（真实场景/代码）
- **实际价值与转化**：`sklearn.cross_decomposition.CCA(n_components=2)`；`cca.fit(X, Y)` 得到载荷与典型得分；用于两组变量相关性可视化与多模态融合特征。

---

## 8. 常见误区和易混概念

### 误区 1：CCA = 两组变量分别做 PCA 再算相关
- **错误直觉**：先各自 PCA 再相关即可。
- **为什么错**：PCA 各自最大化组内方差，忽略组间耦合；CCA 联合最大化组间相关。
- **正确理解**：CCA 是"耦合的谱分解"，不是两个独立 PCA 的组合。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| 典型相关 CCA | 两组变量的整体相关 | 组间耦合谱分解 | 两组变量关联 |
| 主成分 PCA | 单组最大方差 | 组内特征分解 | 降维 |
| 多元回归 | 一组预测另一组 | 有响应/预测角色 | 预测 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[主成分分析 PCA]]：谱方法思想。
- [[多元正态分布与性质]]：分块协方差。

### 下游延伸
- [[协方差结构检验]]：模型拟合检验。

### 横向关联
- [[主成分分析 PCA]] ↔ [[典型相关分析 CCA]]：CCA 是两组变量的 PCA 推广。

### 应用场景
- [[多元统计 - HW01：Fisher 判别分析与 EM-GMM 聚类阶梯作业]]：判别是 CCA 的特例（组指示变量）。

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
- [ ] 1. 用一句话说清楚它解决什么问题。
- [ ] 2. 用直觉语言解释它（«“找两组变量各自的方向，使它们最相关”»）。
- [ ] 3. 写出典型相关优化问题。
- [ ] 4. 写出广义特征方程。
- [ ] 5. 解释每个符号的含义。
- [ ] 6. 讲出拉格朗日推导主线。
- [ ] 7. 手算对角例子。
- [ ] 8. 说出两个常见误区。
- [ ] 9. 说出它和 PCA 的关系。
- [ ] 10. 说出一个真实应用场景。

---

## 11. 自测题：5 道

> [!important] 先闭卷作答，再展开核对
> 合上笔记独立完成下列题目；**全部写完后再逐题展开答案对照**。
> 直接看答案 = 测试效应归零，等于没练。

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | CCA vs PCA |
| 2 | 公式运用 | 基础 | 典型相关计算 |
| 3 | 条件判断 | 中等 | 典型对数量 |
| 4 | 变式/综合 | 中等 | 广义特征方程 |
| 5 | 开放/证明 | 较难 | 显著性检验 |

### 题目与解析

#### 1. CCA 与 PCA 的本质区别？
> [!question]- 答案解析
> - **答案**：PCA 最大化单组方差；CCA 最大化两组线性组合的**相关**，耦合组间结构。
> - **解析**：目标不同。
> - **易错原因**：以为 CCA=PCA×2。

#### 2. $\boldsymbol\Sigma_{11}^{-1}\boldsymbol\Sigma_{12}\boldsymbol\Sigma_{22}^{-1}\boldsymbol\Sigma_{21}$ 特征值 0.81，$\rho_1$？
> [!question]- 答案解析
> - **答案**：$\rho_1=\sqrt{0.81}=0.9$。
> - **解析**：特征值是 $\rho^2$。
> - **易错原因**：直接把特征值当相关。

#### 3. $p=3,q=5$，最多几对典型变量？
> [!question]- 答案解析
> - **答案**：$\min(3,5)=3$ 对。
> - **解析**：典型对数 = 较小维数。
> - **易错原因**：误答 5。

#### 4. 写出广义特征方程并说明 $\rho^2$ 的角色
> [!question]- 答案解析
> - **答案**：$\boldsymbol\Sigma_{11}^{-1}\boldsymbol\Sigma_{12}\boldsymbol\Sigma_{22}^{-1}\boldsymbol\Sigma_{21}\mathbf{a}=\rho^2\mathbf{a}$；$\rho^2$ 是广义特征值。
> - **解析**：谱分解给出全部典型对。
> - **易错原因**：$\boldsymbol\Sigma_{22}^{-1}$ 位置写错。

#### 5. 如何检验典型相关是否显著？
> [!question]- 答案解析
> - **答案**：Wilks 型似然比：$\Lambda_k=\prod_{i=k}^{\min(p,q)}(1-\rho_i^2)$，$\chi^2$ 近似（Bartlett），逐对检验。
> - **解析**：STAT 505 L13.3。
> - **易错原因**：只检验第一个。

---

## 12. 我的主动回忆区

> **用法**：合上笔记，按引导填空。填不出 = 没掌握，回到第 4-5 节重读再重填。写不出来 = 卡点，记入下方。

### 我的闭卷复述
> 用 3 句话解释「典型相关分析 CCA」：
> 1. 它解决什么问题：______
> 2. 它怎么做的（直觉）：______
> 3. 它的关键公式/条件：______

### 我的推导复现
> 不看上文，写出核心推导主线：
> - 第 1 步：______
> - 关键"转念"：______
> - 我能独立推到哪一步：______（卡住的步骤 = 复习重点）

### 我的错误与卡点
- 我填不出的空：______
- 我搞混的概念：______
- 修正后的理解：______

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/16-多元统计/04-相关分析/`
- **关联已有笔记**：`[[🔗 第四阶段：相关分析]]`、`[[典型相关分析的基本理论及方法]]`
- **建议标签**：`#学习` `#多元统计` `#相关`
- **拆分建议**：显著性检验可拆为独立题型卡。
