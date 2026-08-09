---
type: study
topic: "Kruskal-Wallis与Friedman多组秩检验"
course: "非参数统计"
created: 2026-08-08
status: active
stage_moc: "[[🧭 阶段2-经典非参数推断]]"
flow: knowledge
kind: concept
importance: "A"
tags: [学习, 非参数统计, 知识卡]
proof_mode: true
---

# 非参数统计-Kruskal-Wallis与Friedman多组秩检验

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（多组比较与实验设计非参数主干）**
- **判断理由**：单因素方差分析 (One-way ANOVA) 依赖各组正态且方差齐性。Kruskal-Wallis 检验是单因素完全随机设计的非参数替代；Friedman 检验是双因素随机区组（配伍组）设计的非参数核心。
- **验收模式说明**：$H$ 统计量加权平方和推导、自由度与卡方渐近证明、事后多重检验 (Nemenyi)。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 评估 4 种不同的推荐算法在多个用户群体上的留存时长（多组偏态数据），直接做 ANOVA 会由于方差不齐导致假阳性失控。如果两两做 Mann-Whitney 检验，则会产生严重的多重比较假阳性膨胀。
> **核心痛点**：如何构建一个全局的、控制整体错误率的多组非参数检验统计量？

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：它是非参数方差分析体系的基石，连接了单因素设计、配伍区组设计与事后检验理论。
- **实际应用场景**：多组算法性能基准评测、多批次工艺质量一致性检验、问卷多选打分排序分析。
- **高频考点**：Kruskal-Wallis $H$ 统计量系数 $\frac{12}{N(N+1)}$ 的推导来源。

---

## 3. 学它之前需要哪些前置知识？

1. **[[非参数统计-Mann-Whitney-Wilcoxon秩和检验]]**：全局混合排序与秩和分配。
2. **卡方分布 $\chi^2$**：二次型渐近极限定理。

---

## 4. 定义复述

### 1. Kruskal-Wallis 检验（单因素独立多组）

设有 $k$ 个独立处理组，样本量分别为 $n_1, \dots, n_k$，总样本量 $N = \sum n_j$。
混合排秩后，设第 $j$ 组的秩和为 $R_j$，平均秩为 $\bar{R}_j = R_j / n_j$。
全局平均秩为 $\bar{R} = \frac{N+1}{2}$。
定义 $H$ 统计量为组间平均秩偏离加权平方和的标准化形式：
$$H = \frac{12}{N(N+1)} \sum_{j=1}^k n_j \left(\bar{R}_j - \frac{N+1}{2}\right)^2 = \frac{12}{N(N+1)} \sum_{j=1}^k \frac{R_j^2}{n_j} - 3(N+1)$$
在 $H_0$ 下，当各组 $n_j \ge 5$ 时：
$$H \xrightarrow{d} \chi^2(k - 1)$$

### 2. Friedman 检验（双因素随机区组 / 重复测量）

设有 $b$ 个区组（Block，如受试者），每个区组内接受 $k$ 种处理。
在**每个区组内部独立**对 $k$ 种处理进行排秩 $1, \dots, k$。
设第 $j$ 种处理在所有 $b$ 个区组内的秩和为 $R_j$。
定义 Friedman 统计量：
$$Q = \frac{12}{bk(k+1)} \sum_{j=1}^k R_j^2 - 3b(k+1) \xrightarrow{d} \chi^2(k - 1)$$

---

## 5. 推导推演：$H$ 统计量归一化常数 $\frac{12}{N(N+1)}$ 的来源

1. 连续整数 $1, \dots, N$ 的总体方差为：
   $$\sigma^2 = \frac{1}{N} \sum_{i=1}^N \left(i - \frac{N+1}{2}\right)^2 = \frac{N^2 - 1}{12}$$
2. 在原假设下，每一组的平均秩 $\bar{R}_j$ 的方差满足：
   $$\text{Var}(\bar{R}_j) = \frac{\sigma^2}{n_j} \cdot \frac{N - n_j}{N - 1} \approx \frac{N(N+1)}{12 n_j}$$
3. 对标准化变量求平方和 $\sum \frac{(\bar{R}_j - \bar{R})^2}{\text{Var}(\bar{R}_j)}$，其归一化分母自然产生常数 $\frac{12}{N(N+1)}$。

---

## 6. 事后多重比较：Nemenyi 检验

当 Kruskal-Wallis 拒绝 $H_0$ 后，为了确定具体哪两组之间存在显著差异，采用 Nemenyi 双双比较临界差值 (Critical Difference, CD)：
$$CD = q_\alpha \sqrt{\frac{N(N+1)}{12} \left(\frac{1}{n_i} + \frac{1}{n_j}\right)}$$
若 $|\bar{R}_i - \bar{R}_j| \ge CD$，则判定第 $i$ 组与第 $j$ 组差异显著。

---

## 7. 经典反例与误区

### 误区 1：区组数据误用 Kruskal-Wallis 检验
- **错误**：在重复测量（如每个患者同时体验 3 种药物）中，打破区组进行全局混合排秩。
- **后果**：丢失了个体间的配对控制效应，大幅降低统计功效。此时必须使用行内排秩的 Friedman 检验。

---

## 8. 条件变式

| 变式 | 适用结构 | 统计量 | 零分布 |
| :--- | :--- | :--- | :---: |
| **Kruskal-Wallis** | 单因素 $k$ 独立组 | $H = \frac{12}{N(N+1)}\sum \frac{R_j^2}{n_j} - 3(N+1)$ | $\chi^2(k-1)$ |
| **Friedman** | 双因素 $b$ 区组 $\times k$ 处理 | $Q = \frac{12}{bk(k+1)}\sum R_j^2 - 3b(k+1)$ | $\chi^2(k-1)$ |

---

## 9. 相关知识点与双链建议

### 上游依赖
- [[非参数统计-Mann-Whitney-Wilcoxon秩和检验]]

### 下游延伸
- [[非参数统计-置换检验Permutation-Test]]：多组置换方差分析 (Permutation ANOVA)。

---

## 10. 闭卷验收（数学模式）

- [ ] **公式默写**：独立写出 Kruskal-Wallis $H$ 统计量与 Friedman $Q$ 统计量的计算公式。
- [ ] **系数推导**：阐明 $\frac{12}{N(N+1)}$ 与离散均匀方差 $\frac{N^2-1}{12}$ 之间的代数关系。

---

## 11. 分级习题

| 题号 | 类型 | 难度 | 来源 | 考查点 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 手算题 | 基础 | Wasserman Ch.10 Ex.4 | 3 组样本秩和与 $H$ 统计量手算 |
| 2 | 区组分析 | 中等 | IMS Ch.14 Lab | $b=3, k=3$ 下 Friedman 统计量排秩与计算 |

### 题目与解析

#### 1. Kruskal-Wallis 手算
> [!question]- 答案与解析（复盘阶段查看）
> - **数据**：组1 $(2, 5)$，组2 $(7, 8)$，组3 $(1, 9)$。$N=6, k=3, n_j=2$。
> - **总排序**：$1(3), 2(1), 5(1), 7(2), 8(2), 9(3)$。
> - **各组秩**：组1 $\{2, 3\}\to R_1=5$；组2 $\{4, 5\}\to R_2=9$；组3 $\{1, 6\}\to R_3=7$。
> - **代入公式**：$\sum R_j^2/n_j = (25 + 81 + 49)/2 = 155/2 = 77.5$。
> - $H = \frac{12}{6 \times 7}(77.5) - 3(7) = \frac{12 \times 77.5}{42} - 21 = 22.143 - 21 = 1.143$。查 $\chi^2(2)$ 表，$p > 0.05$，不显著。

---

## 12. 我的主动回忆区
> 闭卷复述：Friedman 检验与 Kruskal-Wallis 检验在“排秩范围”上有何本质不同？

---

## 13. 给 Obsidian 的归档建议
- **归档目录**：`02-Knowledge/🧠 学习系统/32-非参数统计/02-经典非参数推断/`
- **标签**：`#学习 #非参数统计 #多组检验 #ANOVA`


---

## 🎯 学完后可以完成

```dataview
LIST
FROM "03-Projects/32-非参数统计"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
