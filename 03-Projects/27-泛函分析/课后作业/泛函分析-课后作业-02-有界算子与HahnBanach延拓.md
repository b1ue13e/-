---
type: project
project_type: homework
course: "泛函分析"
assignment_id: "泛函分析-HW02"
assignment_level: lesson
assignment_format: problem-set
stage_id: "01"
requires: ["[[泛函分析-有界线性算子与算子范数]]", "[[泛函分析-Hahn-Banach定理]]"]
source_type: official_assignment
created: 2026-08-09
status: active
flow: project
tags: [作业, 泛函分析, 算子范数, Hahn-Banach, 对偶]
---

# 泛函分析-课后作业-02-有界算子与HahnBanach延拓

> 对应知识点：[[泛函分析-有界线性算子与算子范数]]、[[泛函分析-Hahn-Banach定理]]
> 官方来源基准：MIT 18.102 Problem Set 2 & 3 (Bounded Operators, Dual Spaces, and Hahn-Banach)

---

## 🎯 学习目标与任务背景

### 1. 学习目标
1. 熟练计算积分算子与序列移位算子的算子范数，并证明上确界可达性。
2. 掌握连续对偶空间 $X^*$ 的结构分析与等距同构表示（如 $(l^1)^* \cong l^\infty$）。
3. 熟练应用 Hahn-Banach 定理构造分离超平面、对偶支撑泛函与赋范空间向二次对偶空间的保范嵌入。

### 2. 任务背景与边界
本作业涵盖有界算子范数计算、连续对偶同构与 Hahn-Banach 延拓定理应用。题目假定在标准标量域上进行，要求将算子范数的上界估计与取等测试函数构造完整写出。

---

## 📝 作业题目清单 (满分 100 分)

### 题 1：Volterra 积分算子的范数与有界性证明 (25 分)
设 $X = C[0, 1]$ 赋上确界范数 $\|f\|_\infty = \max_{t \in [0,1]} |f(t)|$。
定义 Volterra 积分算子 $T: X \to X$ 为：
$$(Tf)(t) = \int_0^t f(s) ds, \quad t \in [0, 1]$$
1. 证明 $T$ 是线性的有界算子，并精确计算其算子范数 $\|T\|_{\mathcal{B}(X)}$。(12 分)
2. 计算复合算子 $T^n = T \circ T \circ \cdots \circ T$ 的显式积分表达式，并计算其范数 $\|T^n\|$。(13 分)

---

### 题 2：序列空间 $(l^1)^*$ 对偶同构的严格推导 (25 分)
设 $l^1 = \{x = (x_k) \mid \sum_{k=1}^\infty |x_k| < \infty\}$ 赋范数 $\|x\|_1 = \sum |x_k|$。
1. 对任一 $y = (y_k) \in l^\infty$，定义泛函 $f_y(x) = \sum_{k=1}^\infty x_k y_k$。证明 $f_y \in (l^1)^*$ 且 $\|f_y\|_{(l^1)^*} = \|y\|_\infty$。(10 分)
2. 反之，证明对任意连续线性泛函 $f \in (l^1)^*$，必定存在唯一的 $y \in l^\infty$ 使得 $f = f_y$。从而证明 $(l^1)^* \cong l^\infty$ 是保范等距同构。(15 分)

---

### 题 3：Hahn-Banach 构造性延拓应用 (25 分)
设 $X = C[-1, 1]$ 赋无穷范数。设子空间 $M = \{f \in X \mid f(0) = 0\}$。
1. 设 $x_0(t) \equiv 1$ 为常数函数。计算距离 $\operatorname{dist}(x_0, M) = \inf_{m \in M} \|x_0 - m\|_\infty$。(10 分)
2. 利用 Hahn-Banach 定理（或其推论），显式构造一个连续线性泛函 $F \in X^*$，使得 $\left.F\right|_M = 0$，$F(x_0) = 1$，且 $\|F\|_{X^*} = 1$。(15 分)

---

### 题 4：超平面分离定理证明应用 (25 分)
设 $X$ 为实赋范线性空间，$M \subset X$ 是线性子空间。
证明：$M$ 在 $X$ 中**稠密**（即 $\overline{M} = X$）当且仅当对于任意 $f \in X^*$，若 $\left.f\right|_M = 0$，则必有 $f \equiv 0$（即 $M$ 的零化子为平凡空间 $M^0 = \{0\}$）。(25 分)

---

## 📦 提交产物与交付要求

1. 包含 4 道题完整证明推导的 Markdown 报告或扫描文档。
2. 对偶同构映射的线性性、双射性与等距性必须逐一列出。

---

## 📊 100 分 Rubric 验收标准

| 评分维度 | 权重 | 评分标准 |
| :--- | :---: | :--- |
| **算子范数推导** | 30% | 包含“上界估计”与“取等测试函数构造”两部分，无猜想式结论。 |
| **对偶同构严密性** | 30% | 显式通过基向量作用提取对偶序列，严格验证收敛性与双射等距。 |
| **Hahn-Banach 应用** | 30% | 能够将几何分离与代数泛函延拓对应，反证法逻辑严丝合缝。 |
| **数学符号规范** | 10% | 算子范数下标、对偶记号与积分上下限准确。 |

---

## 🔍 引导自检与检查点

- 💡 **自检 1**：在题 1(2) 中，通过归纳法可证 $(T^n f)(t) = \frac{1}{(n-1)!} \int_0^t (t-s)^{n-1} f(s) ds$，进而 $\|T^n\| = \frac{1}{n!}$。注意当 $n \to \infty$ 时 $\|T^n\| \to 0$（谱半径为 0）。
- 💡 **自检 2**：在题 4 充分性证明中，若 $\overline{M} \ne X$，必存在 $x_0 \in X \setminus \overline{M}$，直接套用 Hahn-Banach 闭子空间分离推论引出矛盾。
