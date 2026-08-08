---
type: study
topic: "朴素贝叶斯与典型BN模型"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段4-贝叶斯网络]]"
flow: knowledge
kind: concept
difficulty: intermediate
upstream: ["[[概率图模型-贝叶斯网络]]", "[[概率图模型-BN参数学习]]"]
concept: ["朴素贝叶斯", "高斯贝叶斯网络", "专家系统"]
related: ["概率图模型-ChowLiu算法", "概率图模型-贝叶斯网络"]
tags: [概率图模型, 朴素贝叶斯, 高斯BN, 专家系统]
---

# 概率图模型-朴素贝叶斯与典型BN模型

> 本卡介绍三种**典型 BN 结构**：朴素贝叶斯（分类器）、高斯贝叶斯网络（连续变量）、专家系统（诊断 BN，如 MUNIN/MYCIN/PATHFINDER）。它们展示 BN 如何在不同领域落地，也是理解"结构决定能力"的案例集。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：学了 BN 的表示/推断/学习后，需要看"真实模型长什么样"。朴素贝叶斯是**最简单可解释**的分类模型；高斯 BN 处理连续变量（线性-高斯依赖）；专家系统展示 BN 在医学诊断中的经典应用。三者共同回答：**给定问题领域，怎么选/设计 BN 结构**。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：朴素贝叶斯的"朴素"假设（特征条件独立）是理解"强假设 vs 可学习性"的起点；高斯 BN 与线性模型、卡尔曼滤波衔接；专家系统是 PGM 最早的杀手级应用。
- **实际应用场景**：文本分类、垃圾邮件过滤（NB）；连续观测建模（高斯 BN）；医疗诊断（MUNIN 肌肉诊断、PATHFINDER 病理）。
- **高频考点**：NB 的假设与决策边界、高斯 BN 的参数、专家系统的建模流程。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-贝叶斯网络]]**：DAG/CPT 基础。
2. **[[概率图模型-BN参数学习]]**：参数估计。
3. **[[概率图模型-条件独立与d分隔]]**：NB 的独立性假设。

---

## 4. 定义与核心公式

### 4.1 朴素贝叶斯（Naive Bayes）

**结构**：类变量 $C \to X_1, \dots, X_n$（星形），假设特征在给定 $C$ 下**条件独立**。

**分类决策**：
$$\hat c = \arg\max_c P(c \mid \mathbf{x}) \propto P(c) \prod_{i=1}^{n} P(x_i \mid c)$$

**参数**：$P(c)$（先验）+ 每特征每类的 $P(x_i \mid c)$（如高斯/多项）。

**"朴素"的含义与代价**：假设特征条件独立——现实中常违反（如"钱"与"银行"在垃圾邮件中共现）。但 NB 在小样本、高维下仍稳健（方差小、偏差可容忍），是**强基线**。

### 4.2 高斯贝叶斯网络（Gaussian BN）

**结构**：任意 DAG，但每个节点的条件分布是**线性-高斯**：

$$X_i = \sum_{j \in \text{Pa}(i)} w_{ij} X_j + \epsilon_i, \quad \epsilon_i \sim \mathcal{N}(0, \sigma_i^2)$$

**性质**：联合分布是多元高斯；参数为每节点的 $(w_{ij}, \sigma_i^2)$；用**精度矩阵（precision matrix）** $\Lambda = \Sigma^{-1}$ 表示时，无向边缺失 ⇔ 对应精度元素为 0（**条件独立与精度矩阵的零模式对应**）。

**高斯 BN vs MRF**：高斯 BN（有向）可用精度矩阵看依赖；高斯 MRF（无向）直接以精度矩阵定义稀疏依赖——两者在高斯情形可互相转换。

### 4.3 专家系统 BN（MUNIN/MYCIN/PATHFINDER）

**特征**：
- **MUNIN**：肌肉神经诊断，约 1000 节点、几千条边——展示 BN 的**大规模**应用；
- **MYCIN**：早期（非 BN）规则专家系统——对比"规则 vs 概率"；
- **PATHFINDER**：病理诊断，从规则系统转向 BN 后诊断准确率显著提升——BN 相对规则系统的优势案例。

**建模要点**：症状/检查 → 疾病（方向由因果语义定）；CPT 由专家估计或数据学习；推断回答"给定症状下各疾病概率"。

---

## 5. 关键推导

**推导：NB 决策规则来自贝叶斯定理**。

$P(c\mid\mathbf{x}) = \frac{P(c)\prod_i P(x_i\mid c)}{\sum_{c'}P(c')\prod_i P(x_i\mid c')}$——分子即判别式；分母与 $c$ 无关，比较时省略。∎

**推导：高斯 BN ⇒ 多元高斯（精度矩阵稀疏）**。

线性-高斯依赖下，$X = (I - W)^{-1}\epsilon$，$\Sigma = (I-W)^{-1}\text{diag}(\sigma^2)(I-W)^{-\top}$；其逆（精度）$\Lambda = (I-W)^\top\text{diag}(1/\sigma^2)(I-W)$——**无向缺失边（$\Lambda_{ij} = 0$）对应"不存在 $i,j$ 间的直接依赖"**。∎

**推导：为什么 NB 强假设仍好用（偏差-方差视角）**。
NB 的独立性假设带来**偏差**（模型错误），但大幅**降低方差**（参数少、估计稳定）。小样本/高维下方差主导误差 → NB 常优于复杂模型；数据充足时复杂模型才反超。∎

---

## 6. 最小可手算例子

**例（NB 分类）**：邮件分类，$C$ = {垃圾, 正常}，特征"含'优惠'"$X_1$、"含'会议'"$X_2$。
- $P(\text{垃圾}) = 0.5$，$P(X_1=1\mid\text{垃圾}) = 0.6$，$P(X_2=1\mid\text{垃圾}) = 0.1$；
- $P(X_1=1\mid\text{正常}) = 0.1$，$P(X_2=1\mid\text{正常}) = 0.5$。
- 观测 $X_1=1, X_2=0$：
  - 垃圾：$0.5 \times 0.6 \times 0.9 = 0.27$；
  - 正常：$0.5 \times 0.1 \times 0.5 = 0.025$；
  - **判垃圾**（0.27 > 0.025）。

**例（高斯 BN）**：$X_2 = 0.8 X_1 + \epsilon_2$，$\epsilon_2 \sim \mathcal{N}(0, 0.36)$，$X_1 \sim \mathcal{N}(0,1)$。则 $\Sigma = \begin{pmatrix}1 & 0.8\\0.8 & 1\end{pmatrix}$，精度 $\Lambda = \frac{1}{0.36}\begin{pmatrix}0.36 & -0.288\\-0.288 & 0.36\end{pmatrix}$——非对角非零（有边）。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| NB 总是比复杂模型差 | **错**。小样本/高维下 NB 是强基线（低方差）；违反条件独立时才有明显偏差 |
| 高斯 BN 的变量必须高斯边缘 | **部分对**。线性-高斯依赖下联合是多元高斯，边缘也是高斯 |
| 精度矩阵稀疏 = 有向图稀疏 | **错**。精度矩阵对应**无向**依赖；有向图需转道德化后对应 |
| 专家系统 = 规则系统 | **错**。BN 专家系统是概率图模型（处理不确定性），MYCIN 是规则系统（确定性逻辑），PATHFINDER 证明前者更优 |
| NB 的特征越多越好 | **不精确**。特征相关性强时 NB 的独立性假设被破坏更严重；需特征选择 |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 写出 NB 的分类决策公式。
2. 高斯 BN 的局部条件分布形式是什么？

### #自测题/中等
3. 用 §6 邮件数据判断另一观测 $X_1=0, X_2=1$ 的分类。
4. 说明精度矩阵的零元素与无向边缺失的关系。

### #自测题/较难
5. 为什么"朴素"假设在小样本下反而有利？给出偏差-方差解释。

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. $\hat c = \arg\max_c P(c)\prod_i P(x_i\mid c)$。
2. $X_i = \sum_j w_{ij}X_j + \epsilon_i$，$\epsilon_i \sim \mathcal{N}(0,\sigma_i^2)$。
3. 垃圾：$0.5\times0.4\times0.1 = 0.02$；正常：$0.5\times0.9\times0.5 = 0.225$ → 判正常。
4. $\Lambda_{ij} = 0$ ⇔ 给定其他变量后 $X_i \perp X_j$（无直接依赖）→ 无向图无边。
5. NB 参数少 → 估计方差小；独立性假设引入偏差但有限；小样本下方差主导，NB 更稳。
</details>

---

## 9. 通过标准

- [ ] 能**默写** NB 决策规则、高斯 BN 形式；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**手算** NB 分类与高斯 BN 精度矩阵；
- [ ] 能**说明**专家系统 BN 的建模思路与优势。

---

## 10. 来源

- Koller & Friedman (2009). *Probabilistic Graphical Models*, MIT Press. Ch. 3 / Ch. 7.
- Bishop (2006). *PRML*, Springer. §8.2.2 (Gaussian BN).
- Heckerman, Horvitz & Nathwani (1992). Toward normative expert systems: The Pathfinder project. *Methods of Information in Medicine*. 访问日期：2026-08-07。

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

> 直接下游：阶段 5 的 生成vs判别（NB vs CRF）、课程 Capstone（诊断 BN 建模部分）。
