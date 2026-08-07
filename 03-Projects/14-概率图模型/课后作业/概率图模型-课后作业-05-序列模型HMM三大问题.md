---
type: project
project_type: homework
topic: "序列模型HMM三大问题"
course: "14-概率图模型"
assignment_id: "概率图模型-课后作业-05"
assignment_level: lesson
assignment_format: problem-set
stage_id: "5"
requires:
  - "[[概率图模型-隐马尔可夫模型HMM]]"
  - "[[概率图模型-前向后向算法与BaumWelch]]"
  - "[[概率图模型-Viterbi解码]]"
  - "[[概率图模型-条件随机场]]"
source_type: open_textbook_exercise
created: 2026-08-07
updated: 2026-08-07
status: planned
flow: project
kind: project
difficulty: intermediate
tags: [作业, 14-概率图模型, HMM, 序列模型]
---

# 概率图模型 - 课后作业 05：序列模型 HMM 三大问题

> 本作业验证阶段 5 的**HMM 三大基本问题**：评估（前向算法）、解码（Viterbi）、学习（Baum-Welch），并对比 CRF。以**手算 + 最小实现**为主。

---

## 0. 学习目标

完成后能够证明：

1. 手算前向/后向变量与 $P(O \mid \lambda)$；
2. 手算 Viterbi 解码并回溯最优状态序列；
3. 理解 Baum-Welch 的 $\gamma$/$\xi$ 与 EM 的关系；
4. 说出 HMM 与 CRF 在建模对象、假设、学习上的差异。

---

## 1. 任务背景与边界

- 纸笔推导为主，允许最小 Python（numpy）。
- 禁止 `hmmlearn`/`pgmpy` 的 HMM API（考察手算）。
- 每题展示**递推中间值**（前向表/δ 表/回溯指针），不能只给最终答案。

---

## 2. 详细题目

给定 HMM：状态 $S = \{1,2\}$，观测 $O = \{0,1\}$，$T=2$。
- $\pi = (0.5, 0.5)$；
- $A = \begin{pmatrix}0.7 & 0.3 \\ 0.4 & 0.6\end{pmatrix}$；
- $B$：$b_1(0)=0.9, b_1(1)=0.1$；$b_2(0)=0.2, b_2(1)=0.8$。
- 观测序列 $O = (0, 1)$。

### 题 1（前向算法，25 分）

1. 计算 $\alpha_1(1), \alpha_1(2)$；
2. 计算 $\alpha_2(1), \alpha_2(2)$（写出递推过程）；
3. 计算 $P(O \mid \lambda)$；
4. 说明：复杂度 $O(N^2T)$ 与直接枚举 $N^T$ 的差异。

### 题 2（Viterbi 解码，25 分）

同一模型，$O = (0, 1)$。

1. 计算 $\delta_1(1), \delta_1(2)$；
2. 计算 $\delta_2(1), \delta_2(2)$ 与回溯指针 $\psi_2$；
3. 回溯最优状态序列 $q_1^*, q_2^*$，给出 $P^*$；
4. 对比：$P(O)$（题 1）与 $P^*$ 的关系（哪个更大？为什么？）。

### 题 3（Baum-Welch 与 EM，25 分）

1. 写出 $\gamma_t(i)$ 与 $\xi_t(i,j)$ 的定义式；
2. 用题 1 的 $\alpha, \beta$（需先算后向 $\beta$）计算 $\gamma_1(1)$；
3. 写出 $\hat\pi_i, \hat a_{ij}, \hat b_j(k)$ 的更新公式；
4. 说明：Baum-Welch 是 EM 的 HMM 特例（隐状态 = 缺失数据）。

### 题 4（HMM vs CRF，25 分）

1. 对比表：建模对象 / 观测假设 / 特征 / 学习 / 收敛性；
2. 设计 2 个 CRF 特征（针对词性标注），说明 HMM 为何难以使用它们；
3. 说明：CRF 的似然是凹函数而 HMM 的不是（收敛性差异）；
4. 各举一个 HMM / CRF 的典型应用。

---

## 3. 环境与复现

- **Python**：3.11+；依赖仅 `numpy`；
- 题 1-2 可用 numpy 逐表验证；题 3-4 纸笔；
- 无需随机种子。

---

## 4. 提交产物

1. `answers.md`：4 题推导（含前向表/δ 表）；
2. `verify.py`（可选）：前向 + Viterbi 的最小实现（约 40 行）；
3. 一句"卡点/收获"。

---

## 5. 验收标准与 Rubric

| 维度 | 分值 | 通过要求 |
|:---|---:|:---|
| 题 1 前向 | 25 | $\alpha_1 = (0.45, 0.10)$、$\alpha_2 = (0.0355, 0.156)$、$P(O)=0.1915$ |
| 题 2 Viterbi | 25 | 最优序列 $(1,2)$、$P^*=0.108$、回溯正确 |
| 题 3 Baum-Welch | 25 | $\gamma$ 计算正确、更新公式正确 |
| 题 4 CRF 对比 | 25 | 对比表与特征设计合理 |
| **总计** | **100** | **≥ 75 且题 2 不低于 20** |

---

## 6. 引导与自检

- **检查点 1**：题 1——前向表每列和 ≤ 1（非概率，是联合）；$P(O) = \sum_i\alpha_T(i)$；
- **检查点 2**：题 2——Viterbi 用 $\max$（联合最优），$P^* = 0.108 < P(O) = 0.1915$（求和 > 最大单项）；回溯从 $\psi_2$ 反推；
- **检查点 3**：题 3——$\gamma_t(i) = \frac{\alpha_t(i)\beta_t(i)}{P(O)}$，需先算后向 $\beta$（$\beta_2 = (1,1)$）；
- **常见错误**：$\beta_T(i)$ 设 0（应为 1）；Viterbi 用逐时刻 argmax；Baum-Welch 更新忘归一化；把 $P^*$ 当 $P(O)$。
- **提交前清单**：递推表完整；$\sum_i\gamma_t(i)=1$；回溯正确。

---

## 7. 知识依赖与后续

- 所需知识见 frontmatter `requires`（阶段 5 HMM/CRF 卡）；
- 完成后可衔接 [[概率图模型-NER与POS应用]] 与课程 Capstone（若选 HMM 部分）；
- 前向/后向与 Viterbi 是阶段 4 [[概率图模型-动态贝叶斯网络]] 滤波/解码的基础。

---

## 8. 来源

- Rabiner (1989). A tutorial on HMMs and selected applications in speech recognition. *Proc. IEEE* 习题改编。
- Bishop (2006). *PRML*, Springer. Chapter 13 习题改编。
- 课程内部整理题（`open_textbook_exercise`）。访问日期：2026-08-07。
